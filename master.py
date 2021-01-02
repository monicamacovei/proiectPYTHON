import requests
from bs4 import BeautifulSoup



def get_country_links():
    response = requests.get("https://www.alexa.com/topsites/countries")  #iau HTML-ul de pe pagina
    soup = BeautifulSoup(response.text, features="html.parser") #initializam BeautifulSoup  (care ne ajuta sa parsam HTML-ul)

    links = set()  #folosesc set pentru a nu avea duplicate in link-uri
    for link in soup.findAll('a'):  #caut tag-urile HTML a
        link = "https://www.alexa.com/topsites/" + link.get('href')
        if "countries/" in link:
            links.add(link)

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
    country_links = get_country_links()
    top_links = get_top_links("https://www.alexa.com/topsites/countries/ES");
    print(top_links)