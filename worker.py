import requests
from rqueue import CustomQueue
from redis import Redis


def get_html(link):
    r = requests.get("http://www." + link)
    with open('data/' + link + '.html', 'w') as file:
        file.write(r.text)

q = CustomQueue(r=Redis())

i=0
while q.get_len():
    data = q.dequeue()
    try:
        get_html(data['link'])
        i+=1
        print(i)
    except Exception as ex:
        print("Eroare la citire: ", data["link"])
        print(ex)
        q.enqueue(data)