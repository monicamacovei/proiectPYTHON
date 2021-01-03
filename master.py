import requests
from bs4 import BeautifulSoup
from redis import Redis
from rqueue import CustomQueue
import sys
import os 
from config import locatieDisk


def get_country_links():
    response = requests.get("https://www.alexa.com/topsites/countries")  #iau HTML-ul de pe pagina
    soup = BeautifulSoup(response.text, features="html.parser") #initializam BeautifulSoup  (care ne ajuta sa parsam HTML-ul)

    links = set()  #folosesc set pentru a nu avea duplicate in link-uri
    for link in soup.findAll('a'):  #caut tag-urile HTML a
        link_text = link.text
        url = "https://www.alexa.com/topsites/" + link.get('href')
        if "countries/" in url:
            links.add((url,link_text))

    return list(links)

def get_top_links(country_link):
    response = requests.get(country_link)
    soup = BeautifulSoup(response.text, features="html.parser") 

    links = set()  
    for link in soup.findAll('a'):  
        link = link.get('href')
        if "siteinfo/" in link:
            links.add(link.replace("/siteinfo/", ""))

    return list(links)

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

