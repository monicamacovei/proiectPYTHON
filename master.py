import requests
from bs4 import BeautifulSoup



def get_country_links():
    response = requests.get("https://www.alexa.com/topsites/countries")  #iau HTML-ul de pe pagina
    soup = BeautifulSoup(response.text)

    links = set()
    for link in soup.findAll('a'):
        link = link.get('href')
        if "countries/" in link:
            links.add(link)

    print(links)

if __name__ == "__main__":
    get_country_links()