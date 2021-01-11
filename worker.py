import os
import sys
from multiprocessing import Process

import requests
from redis import Redis

from rqueue import CustomQueue


def get_html(data):
    """
    Extrage HTML-ul de pe pagina data si il salveaza in fisierul corespunzator
    :param data: un dictionar cu link-ul de unde sa descarc HTML-ul si locatia unde trebuie salvat HTML-ul
    """
    r = requests.get("http://" + data["link"], timeout=10)
    # daca nu exista folderul pentru tara respectiva deja
    if not os.path.exists(data["locatieDisk"]):
        os.mkdir(data["locatieDisk"])  # creez folderul pentru tara
    # path-ul pentru site-ul descarcat
    file_path = os.path.join(data["locatieDisk"], data["link"] + '.html')
    with open(file_path, 'w') as file:
        file.write(r.text)  # scriu continutul HTML al site-ului in fisier


def worker_process(redis_name):
    """
    Iau elemente din coada Redis si descarc paginile corespunzatoare
    :param redis_name: numele cozii Redis
    """
    q = CustomQueue(Redis(), redis_name)
    while q.get_len():

        data = q.dequeue()  # scoatem primul element din coada (de la dreapta)
        print(data)
        for _ in range(3):  # incercam de 3 ori in caz de eroare
            try:
                get_html(data)
                print("Numar element din coada: ", q.get_len())
                break  # iesim din for daca nu a fost nicio eroare
            except Exception as ex:
                print(ex)
                print("Eroare la citire: ", data["link"])
                print("Incercam din nou")


if __name__ == "__main__":
    if not len(sys.argv) >= 2:  # primul argument e obligatoriu (numele cozii)
        print("Trebuie dat ca argument numele cozi din redis")
        exit(0)
    processes_number = 4
    if len(sys.argv) >= 3 and sys.argv[2]:
        # daca e dat nr proceselor ca parametru
        processes_number = int(sys.argv[2])
    redis_name = sys.argv[1]

    processes = []
    for _ in range(processes_number):
        # initializez un proces ce apeleaza functia worker_process cu parametrul redis_name
        p = Process(target=worker_process, args=(redis_name,))
        processes.append(p)
        p.start()  # pornim procesul

    for p in processes:
        p.join()  # astept ca procesul p sa se termine

    print("Toate site-urile au fost salvate")
