import xmlrpc.client


def Download(targetip, port, remotefilename, savepath):
    c = xmlrpc.client.ServerProxy("http://" + targetip + ":" + port + "/")
    with open(savepath, "wb") as f:
        filesize = c.getsize(remotefilename) / (1024 * 1024)
        print("size:%.2fM" % filesize)
        f.write(c.Download(remotefilename).data)
        print("Download Completed")


#Download("192.168.43.195", "1234", "可行性分析（技术依据）",
#         r"D:\RuiRui_Doc\Desktop\OSH资料\test\可行性分析（技术依据）.docx")