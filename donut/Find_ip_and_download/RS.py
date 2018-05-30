import zerorpc
from multiprocessing import Queue, Process
import os
import random


class Server(object):

    def get_ID_block(self, ID):          #接受请求ID表块的请求
        queue.put(["getIDblock", ID])
        return "Success request"

    def send_ID_block(self, ID, IDblock): #接受发送到达的ID表块（列表）
        queue.put(["receiveIDblock", ID, IDblock])
        return "Sending success"

    # 以下三个是用于接受下载软件块请求的，buf函数不由客户调用
    def buf(self, f):
        while 1:
            data = f.read(size)
            if not data:
                print("End")
                break
            #print(data)
            yield data
        f.close()

    @zerorpc.stream
    def Download(self, file):
        print("in")
        f = open(file, 'rb')
        return self.buf(f)

    def getsize(self, path):
        return os.path.getsize(path)


class Client(object):
    pass

# 以下两个函数用于处理其他节点请求
def receive(name, queue):
    s = zerorpc.Server(Server())
    s.bind("tcp://*:1234")
    s.run()


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