import os
import sys

import requests
from bs4 import BeautifulSoup
from redis import Redis

from config import locatieDisk
from rqueue import CustomQueue


def alexa_request(link, prefix, country_links):
    """
    Extrage date de pe site-ul https://www.alexa.com in functie de parametrii dati
    :param link: Link-ul de la tara curenta sau de la lista cu toate tarile
    :param prefix: Prefixul din link, daca e de la tara curenta, e "siteinfo/", daca e de la lista cu tari, e "countries/"
    :param country_links: Daca se apeleaza pentru lista cu tari, atunci va fi True. Altfel, va fi False
    :return links: Link-urile extrase de pe alexa (lista cu link-ul tarilor sau lista cu link-ul site-urilor din top)
    """
    response = requests.get(link)  # iau HTML-ul de pe pagina
    # initializam BeautifulSoup  (care ne ajuta sa parsam HTML-ul)
    soup = BeautifulSoup(response.text, features="html.parser")

    links = []
    for link in soup.findAll('a'):  # caut tag-urile HTML a
        if country_links:  # daca luam numele si link-ul tarilor
            link_text = link.text  # iau numele tarii din texul tag-ului "a"
            link = "https://www.alexa.com/topsites/" + \
                link.get('href')  # creez link-ul tarii
        else:
            link = link.get('href')  # pentru top sites am nevoie doar de link

        if prefix in link:
            if country_links:
                # iau link-ul tarii si numele ei
                links.append((link, link_text))
            else:
                # doar link-ul site-ului si sterg /siteinfo/ din link
                links.append(link.replace("/siteinfo/", ""))

    return links


def get_country_links():
    """
    Extrage link-urile tuturor tarilor de pe www.alexa.com
    :return : link-urile extrase sau o lista goala daca apare eroare de 3 ori la rand
    """
    for _ in range(3):
        try:
            return alexa_request(
                "https://www.alexa.com/topsites/countries", "countries/", True
            )
        except Exception as ex:
            print(ex)
    return []


def get_top_links(country_link):
    """
    Extrage link-urile site-urilor din top pentru tara data ca parametru
    :param country_link: link-ul cu site-uri din top din tara curenta
    :return : link-urile extrase sau o lista goala daca apare eroare de 3 ori la rand
    """
    for _ in range(3):
        try:
            return alexa_request(country_link, "siteinfo/", False)
        except Exception as ex:
            print(ex)
    return []


if __name__ == "__main__":
    if not len(sys.argv) >= 2:  # primul argument e obligatoriu (numele cozii)
        print("Trebuie dat ca argument numele cozi din redis")
        exit(0)
    redis_name = sys.argv[1]  # numele cozii
    # initializam coada custom definita in rqueue.py
    q = CustomQueue(Redis(), redis_name)
    # golim coada initializata (in caz ca au ramas date de la ultima rulare)
    q.empty_queue()

    country_links = get_country_links()

    for country_link, country_text in country_links:
        # stergem spatiul din numele tarii
        country_text = country_text.replace(" ", "")
        top_links = get_top_links(country_link)
        for link in top_links:
            # locatia paginii descarcate va fi
            # folderul setat in config si numele tarii
            locatieDiskTemp = os.path.join(locatieDisk, country_text)
            q.enqueue(link, locatieDiskTemp)  # adauga in coada
        # break  #ca sa testam pentru o singura tara
