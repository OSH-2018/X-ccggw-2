# 这里是本地节点为其他节点提供的rpc常驻服务

import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import os

from ..model.IDblock import IDServer


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer): pass


class Server(IDServer):
    def __init__(self):
        super(Server, self).__init__()
        # 新建ID表块管理器
        self.IDserver = IDServer()
        # 存留id
        self.id = -1

    # 询问身份和存储id表块
    def getStatus(self):
        pass

    # 以下两个方法为仅管理者需要处理的
    # 被通知新节点上线
    def new_owner(self, package, version, newID):
        blockname = package + '_' + version
        self.IDserver.addID(blockname, newID)

    # 被通知节点下线
    def del_owner(self, package, version, ID):
        blockname = package + '_' + version
        self.IDserver.deleID(blockname, ID)

    def Download(self, filename):
        print("Download start...")
        # 此处为高危操作，后期需要修改
        with open(filename, 'rb') as f:
            tmp = xmlrpc.client.Binary(f.read())
        return tmp

    def getsize(self, filename):
        return os.path.getsize(filename)
