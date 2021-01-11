
import json


class CustomQueue:
    """
    Coada customizata Redis
    """

    def __init__(self, r, name="default"):
        """
        Initializeaza clasa CustomQueue
        :param r: coada Redis
        :param name: numele cozii
        """
        self.name = name
        self.r = r

    def enqueue(self, link, locatieDisk):
        """
        Adauga elemente in coada dupa ce le transformam in JSON
        :param link: link-ul din site-ul din top curent
        :param locatieDisk: locatia unde trebuie salvat HTML-ul
        """
        data = json.dumps({"link": link, "locatieDisk": locatieDisk})
        print(data)
        self.r.lpush(self.name, data)  # adaugam in redis (la inceputul cozii)

    def dequeue(self):
        """
        Ia ultimul element din coada si il transforma din JSON in dictionar
        :return :ultimul element din coada. Daca nu exista,
        atunci returneaza None
        """
        # luam din coada self.name ultimul element
        # de la dreapta (adica primul adaugat)
        data = self.r.rpop(self.name)
        if not data:
            return None
        data = data.decode()  # transformam din biti in string
        return json.loads(data)  # transformam string-ul cu JSON in dictionar

    def get_len(self):
        """
        Calculeaza lungimea cozii curente
        :return : lungimea cozii curente
        """
        return self.r.llen(self.name)

    def empty_queue(self):
        """
        Goleste coada curenta
        """
        self.r.delete(self.name)  # golim toata coada self.name
