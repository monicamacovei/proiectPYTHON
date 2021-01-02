import requests
from rqueue import CustomQueue
from redis import Redis


def get_html(data):
    r = requests.get("http://www." + data["link"])
    with open(data["locatieDisk"] + '.html', 'w') as file:
        file.write(r.text)

q = CustomQueue(r=Redis())

i=0
while q.get_len():
    data = q.dequeue()
    try:
        get_html(data)
        i+=1
        print(i)
    except Exception as ex:
        print("Eroare la citire: ", data["link"])
        print(ex)
        q.enqueue(data)