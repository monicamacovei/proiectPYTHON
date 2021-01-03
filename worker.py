import requests
from rqueue import CustomQueue
from redis import Redis
import os
import sys
from multiprocessing import Process


def get_html(data):
    r = requests.get("http://" + data["link"], timeout=10) #iau HTML-ul de pe pagina
    if not os.path.exists(data["locatieDisk"]): #daca nu exista folderul pentru tara respectiva deja
        os.mkdir(data["locatieDisk"]) #creez folderul pentru tara 
    file_path = os.path.join(data["locatieDisk"],data["link"] + '.html') #path-ul pentru site-ul descarcat
    with open(file_path, 'w') as file:
        file.write(r.text) #scriu continutul HTML al site-ului in fisier

def worker_process(redis_name):
    q = CustomQueue(Redis(), redis_name) #initializam coada custom definita in rqueue.py
    while q.get_len():
        
        data = q.dequeue() #scoatem primul element din coada (de la dreapta)
        print(data)
        for _ in range(3): #incercam de 3 ori in caz de eroare
            try:
                get_html(data)
                print("Numar element din coada: ", q.get_len())
                break #iesim din for daca nu a fost nicio eroare
            except Exception as ex:
                print(ex)
                print("Eroare la citire: ", data["link"])
                print("Incercam din nou")
if __name__ == "__main__":
    if not len(sys.argv)>=2: #primul argument e obligatoriu (numele cozii)
        print("Trebuie dat ca argument numele cozi din redis")
        exit(0)
    processes_number = 4
    if len(sys.argv)>=3 and sys.argv[2]:
        processes_number = int(sys.argv[2]) #daca e dat nr proceselor ca parametru
    redis_name = sys.argv[1]

    processes = []
    for _ in range(processes_number):
        p = Process(target=worker_process, args=(redis_name,)) #initializez un proces ce apeleaza functia worker_process cu parametrul redis_name
        processes.append(p)
        p.start() #pornim procesul

    for p in processes:
        p.join() #astept ca procesul p sa se termine
        
    print("Toate site-urile au fost salvate")
    

