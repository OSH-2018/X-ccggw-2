# 这里是本地节点为其他节点提供的rpc常驻服务

import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import os

from IDblock import IDop

class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):pass

class Server(IDServer):
    def __init__(self, id, blocks):
        super(Server, self).__init__()
        self.id = id
        # 使用函数确认身份




    # 询问身份和存储id表块
    def getStatus(self):
        pass

    # 以下两个方法为仅管理者需要处理的
    # 被通知新节点上线
    def new_owner(self):
        pass

    # 被通知节点下线
    def del_owner(self):
        pass

    def Download(self, filename):
        print("Download start...")
        file = file_path_index[filename]
        f = open(file, 'rb')
        return xmlrpc.client.Binary(f.read())
        f.close()

    def getsize(self, filename):
        return os.path.getsize(file_path_index[filename])


if __name__ == "__main__":
    port = "1234"                   #监听端口
    # 伪文件路径字典 get_file_path_index(file_path_index)
    file_path_index = {"组成原理_0": r"data/test.deb",
                       "组成原理_1": r"data/out.zip"}
    server = Server()
    s = ThreadXMLRPCServer(("0.0.0.0", int(port)))
    print("start service...")
    s.register_instance(server)
    s.serve_forever()