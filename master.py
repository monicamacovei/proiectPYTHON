import requests
from bs4 import BeautifulSoup



def get_country_links():
    response = requests.get("https://www.alexa.com/topsites/countries")  #iau HTML-ul de pe pagina
    soup = BeautifulSoup(response.text) #initializam BeautifulSoup  (care ne ajuta sa parsam HTML-ul)

    links = set()  #folosesc set pentru a nu avea duplicate in link-uri
    for link in soup.findAll('a'):  #caut tag-urile HTML a
        link = "https://www.alexa.com/topsites/" + link.get('href')
        if "countries/" in link:
            links.add(link)

    return list(links)

if __name__ == "__main__":
    country_links = get_country_links()
    print(country_links)