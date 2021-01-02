import requests
from bs4 import BeautifulSoup
from redis import Redis
from rqueue import CustomQueue
import sys

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
        print("Trebuie dat ca argument locatieDisk")
        exit(0)
    locatieDisk = sys.argv[1]
    q = CustomQueue(Redis())

    country_links = get_country_links()
    print(len(country_links))

    for country_link, country_text in country_links:
        print(country_link)
        print(country_text)
        top_links = get_top_links(country_link)
        for link in top_links:
            continue
            q.enqueue(link,"home")
        break

