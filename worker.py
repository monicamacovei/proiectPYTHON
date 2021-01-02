import requests
from rqueue import CustomQueue
from redis import Redis


def get_html(link):
    r = requests.get("http://www." + link)
    with open(link + '.html', 'w') as file:
        file.write(r.text)

q = CustomQueue(r=Redis())

i=0
while q.get_len():
    print(q.dequeue())
    i+=1
    print(i)