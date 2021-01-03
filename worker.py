import requests
from rqueue import CustomQueue
from redis import Redis
import os
import sys
from multiprocessing import Process


def get_html(data):
    r = requests.get("http://" + data["link"], timeout=10)
    if not os.path.exists(data["locatieDisk"]):
        os.mkdir(data["locatieDisk"])
    file_path = os.path.join(data["locatieDisk"],data["link"] + '.html')
    with open(file_path, 'w') as file:
        file.write(r.text)

def worker_process(redis_name):
    q = CustomQueue(Redis(), redis_name)
    while q.get_len():
        
        data = q.dequeue()
        print(data)
        for _ in range(3):
            try:
                get_html(data)
                print("Numar element din coada: ", q.get_len())
                break
            except Exception as ex:
                print(ex)
                print("Eroare la citire: ", data["link"])
                print("Incercam din nou")
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Trebuie dat ca argument numele cozi din redis")
        exit(0)
    redis_name = sys.argv[1]

    processes = []
    for _ in range(4):
        p = Process(target=worker_process, args=(redis_name,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
    

