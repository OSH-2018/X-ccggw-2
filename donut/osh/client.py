# 等待整合
import xmlrpc.client

# class Receiver():

def Download(targetip: str, port: str, remotefilename: str, savepath: str):
    c = xmlrpc.client.ServerProxy("http://" + targetip + ":" + port + "/")
    i = 0
    # 远程文件名称，本地保存的地址
    with open(savepath, "wb") as f:
        filesize = c.getsize(remotefilename) / (1024 * 1024)
        print("size:%.2fM" % filesize)
        f.write(c.Download(remotefilename).data)
        print("Download Completed")
        # data = c.Download(remotepath)
        # for buf in data:
        #    f.write(buf)
        #    i = i + 1
        #    print(round(i/(filesize)*100), '%')

# Download("localhost", "1234", "可行性分析（技术依据）")