import SimpleXMLRPCServer
from multiprocessing import Queue, Process
import os
import random

class Server(object):
    def  __init__(self):
        self.table={}

    def create_id(self,ip):
        id=random.random(0,2 ** 16)
        while id in self.table:
            id = random.random(0, 2 ** 16)
        add(id,ip)
        return id

    def add(self,id,ip):
        if(id in self.table):
            print("conflict")
            return -1
        self.table[id]=ip
        print("add success")
        return 0

    def get(self,id):
        if (id in self.table):
           return self.table[id]
        else:
            print("Nothing")


    def dele(self,id):
        if ((id in self.table)==-1):
           print("error")
           return -1
        else:
           del self.table[id]
           return 0

    def download_all(self):
        return self.table

if __name__ == "__main__":
    port = "1234"
    server = Server()
    s = SimpleXMLRPCServer(("0.0.0.0", int(port)))
    print("start service...")
    s.register_instance(server)
    s.serve_forever()
