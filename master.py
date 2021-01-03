import requests
from bs4 import BeautifulSoup
from redis import Redis
from rqueue import CustomQueue
import sys
import os 
from config import locatieDisk

def alexa_request(link, prefix, country_links):
    response = requests.get(link)  #iau HTML-ul de pe pagina
    soup = BeautifulSoup(response.text, features="html.parser") #initializam BeautifulSoup  (care ne ajuta sa parsam HTML-ul)

    links = []  
    for link in soup.findAll('a'):  #caut tag-urile HTML a
        if country_links == True:
            link_text = link.text
            link = "https://www.alexa.com/topsites/" + link.get('href')
        else:
            link = link.get('href')
        
        if prefix in link:
            if country_links == True:
                links.append((link,link_text))
            else:
                links.append(link.replace("/siteinfo/", ""))

    return links

def get_country_links():
    return alexa_request("https://www.alexa.com/topsites/countries", "countries/", True)

def get_top_links(country_link):
    return alexa_request(country_link, "siteinfo/", False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Trebuie dat ca argument numele cozi din redis")
        exit(0)
    redis_name = sys.argv[1]
    q = CustomQueue(Redis(), redis_name)
    q.empty_queue()

    country_links = get_country_links()

    for country_link, country_text in country_links:
        country_text = country_text.replace(" ", "")
        top_links = get_top_links(country_link)
        for link in top_links:
            locatieDiskTemp = os.path.join(locatieDisk, country_text)
            q.enqueue(link,locatieDiskTemp)
        break

