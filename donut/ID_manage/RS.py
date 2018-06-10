import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from multiprocessing import Queue, Process
import os
import _thread
import random
file_path_index = {"组成原理": r"D:\RuiRui_Doc\Desktop\OSH资料\组成原理.rar",
                       "可行性分析（技术依据）": r"D:\RuiRui_Doc\Desktop\OSH资料\可行性分析（技术依据）.docx"}


class Server(object):

    def get_ID_block(self, ID):          #接受请求ID表块的请求
        queue.put(["getIDblock", ID])
        return "Success request"

    def send_ID_block(self, ID, IDblock): #接受发送到达的ID表块（列表）
        queue.put(["receiveIDblock", ID, IDblock])
        return "Sending success"

    # 以下三个是用于接受下载软件块请求的，buf函数不由客户调用
    def Download(self, filename):
        print("Download start...")
        file = file_path_index[filename]
        f = open(file, 'rb')
        return xmlrpc.client.Binary(f.read())
        f.close()


    def getsize(self, path):
        return os.path.getsize(path)


class Client(object):
    pass

# 以下两个函数用于处理其他节点请求
def receive(name, queue):
    server = Server()
    s = SimpleXMLRPCServer(("0.0.0.0", int(port)))
    print("start service...")
    s.register_instance(server)
    s.serve_forever()


def background_processing():
    pass


def main(name, queue):
    pass
    #调用Client类中方法操作


if __name__ == "__main__":
    queue = Queue()
    size = 1024 * 1024
    port = "1234"  # 监听端口
    receive_process = Process(target=receive, args=("Receive", queue))
    main_process = Process(target=main, args=("Main", queue))
    receive_process.start()
    main_process.start()
    receive_process.join()
    main_process.join()