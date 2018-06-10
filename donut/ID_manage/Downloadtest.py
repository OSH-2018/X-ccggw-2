import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
import os


class Server(object):

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
    file_path_index = {"组成原理": r"D:\RuiRui_Doc\Desktop\OSH资料\组成原理.rar",
                       "可行性分析（技术依据）": r"D:\RuiRui_Doc\Desktop\OSH资料\可行性分析（技术依据）.docx"}
    server = Server()
    s = SimpleXMLRPCServer(("0.0.0.0", int(port)))
    print("start service...")
    s.register_instance(server)
    s.serve_forever()