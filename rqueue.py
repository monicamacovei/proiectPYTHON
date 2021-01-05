
import json


class CustomQueue:
    def __init__(self, r, name="default"):
        self.name = name
        self.r = r

    def enqueue(self, link, locatieDisk):
        # transform din dictionar in string JSON
        data = json.dumps({"link": link, "locatieDisk": locatieDisk})
        print(data)
        self.r.lpush(self.name, data)  # adaugam in redis (la inceputul cozii)

    def dequeue(self):

        # luam din coada self.name ultimul element
        # de la dreapta (adica primul adaugat)
        data = self.r.rpop(self.name)
        if not data:
            return None
        data = data.decode()  # transformam din biti in string
        return json.loads(data)  # transformam string-ul cu JSON in dictionar

    def get_len(self):
        return self.r.llen(self.name)

    def empty_queue(self):
        self.r.delete(self.name)  # golim toata coada self.name
