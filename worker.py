import requests
from rqueue import CustomQueue
from redis import Redis


def get_html(link):
    r = requests.get(link)
    with open('file.txt', 'w') as file:
        file.write(r.text)

q = CustomQueue(r=Redis())
print(q.dequeue())