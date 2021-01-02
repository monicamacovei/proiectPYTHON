
import json
class CustomQueue:
    def __init__(self, r, name="default"):
        self.name = name
        self.r = r
    
    def enqueue(self, link, locatieDisk):
        data = json.dumps({"link": link, "locatieDisk": locatieDisk})
        print(data)
        self.r.lpush(self.name, data)
    
    def dequeue(self):

        data = self.r.rpop(self.name)
        if not data:
            return None
        data = data.decode()
        return json.loads(data)