import requests
from rqueue import CustomQueue
from redis import Redis
import os

def get_html(data):
    r = requests.get("http://www." + data["link"])
    if not os.path.exists(data["locatieDisk"]):
        os.mkdir(data["locatieDisk"])
    file_path = os.path.join(data["locatieDisk"],data["link"] + '.html')
    with open(file_path, 'w') as file:
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
        q.enqueue(data["link"], data["locatieDisk"])