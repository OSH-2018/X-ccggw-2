import json
import xmlrpc.client
import hashlib
import socket
import os
from client import Download


myname = socket.getfqdn(socket.gethostname())
myip = socket.gethostbyname(myname)
DNSip = "192.168.43.195"
DNSport = "1234"
port = "1234"
num = 6


def divideIDblock(filename):
    "%sIDblock.txt" % filename
    pass


def composeIDblock(filename):
    pass


def create_IDblock(filename, initID):
    block = {}
    IDlist = []
    IDlist.append(initID)
    block["IDlist"] = IDlist
    block["name"] = filename
    json_block = json.dumps(block)
    verification = hashlib.md5(json_block)
    with open("./%sIDblock.txt" % filename, 'w') as f:
        f.write(json_block)
    with open("./%sIDblock.md5" % filename, 'w') as f:
        f.write(verification)


def distr_block(blockname):
    DNSc = xmlrpc.client.ServerProxy("http://" + DNSip + ":" + DNSport + "/")
    idealID = hashlib.md5(blockname)
    sign = False
    while not sign:
        ID = IDfind(idealID)                  # 找到最终的ID-----------------------------------------
        ip = DNSc.getip(ID)                     # ID到ip的映射-----------------------------------------
        c = xmlrpc.client.ServerProxy("http://" + ip + ":" + port + "/")
        if c.sign(("distr_block", blockname, myip)) == "Success":   # 传递表块接受请求, 接受成功回复True
            sign = True
        if not sign:
            print("Fail to connect to target node!")
            return ID
            #for i in range(3):
            #    if DNSc.lostnode(ID) == "Success":
            #        break
            #    else:
            #        print("Fail to connect to DNS service! %d..." % (i+1))


def strcmplmt(x):
    return x + ".txt"


def collectIDblock(filename):
    blocknames = []
    for i in range(num):
        blocknames.append("%sIDblock_%d" % (filename, i))
    targetID = list(map(hashlib.md5, blocknames))
    DNSc = xmlrpc.client.ServerProxy("http://" + DNSip + ":" + DNSport + "/")
    targetip = list(map(DNSc.getip, targetID))                                 #-------------------
    multiDownload(targetip, list(map(strcmplmt, blocknames)))                # 多线程下载 multiDownload(ip[, file[,)
    verification = ["%sIDblock.md5" % filename for x in range(num)]
    multiDownload(targetip, verification)


def addID(filename):
    ID = get_myID()
    collectIDblock(filename)
    composeIDblock(filename)
    with open("%sIDblock.txt" % filename, "r") as f:
        IDblock = json.loads(f.read())
    IDblock["IDlist"].append(ID)
    with open("%sIDblock.txt" % filename, "w") as f:
        f.write(json.dumps(IDblock))


def update(filename):
    addID(filename)
    divideIDblock(filename)
    for i in range(num):
        distr_block("%sIDblock_%d.txt" % (filename, i))


def localupdate():
    if


def saveIDblock():
    sign = Queue.get()
    if sign[0] == "distr_block":
        Download(sign[2], "1234", sign[1], "./%s" % sign[1])
        if os.path.exists('./IDblockdir.txt'):
            with open("IDblockdir.txt", "r+") as f:
                IDblockdir = json.loads(f.read())
                if sign[1] in IDblockdir.keys:
                    IDblockdir[sign[1]] =



if __name__ == "__main__":

    pass