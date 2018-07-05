import os
import hashlib
import xmlrpc
import socket
import random
import json
from ..Operations.DOWNops import rpc_download
from ..config import path

from ..model.routingtable import RouteClient, get_myID

# 获取已得到的ID表块中的ID（块名s，数量）
def get_downloadID(blockfilenames, volume):
    L = []
    for blockfilename in blockfilenames:
        with open(blockfilename, 'r') as f:
            List = json.loads(f.read())['IDlist']
            for ID in List:
                L.append(ID)
    base = random.randint(1, len(L))
    reL = []
    for i in range(volume):
        reL.append(L[(base + i) % (len(L) + 1)])
    return reL


def addmyID(filename: str, client: RouteClient):
    # 通知加入本节点ID入表块的方法

    ID = get_myID()

    # 算出本ID应存入的表块号
    blocknum = hashlib.md5(ID) % num

    # 执行一系列翻译
    _targetID = hashlib.md5("%sIDblock_%d" % (filename, blocknum))
    targetID = client.findID(_targetID)  # 找到最终的ID-----------------------------------------
    DNSc = xmlrpc.client.ServerProxy("http://" + DNSip + ":" + DNSport + "/")
    targetip = DNSc.getip(targetID)

    # 通知执行更新表块操作
    communication = xmlrpc.client.ServerProxy("http://" + targetip + ":" + port + "/")
    if communication.addID("%sIDblock_%d" % (filename, blocknum), ID) == "addID success":
        return 0
    else:
        print("Fail to connect to target node!")
        DNSc.dele(ID)  # ID掉线
        return -1


def identity_judge(client: RouteClient):
    # 获取自身与自身两侧最近的节点的ID
    ID = get_myID()
    IDl, IDr = client.get_mylrID()

    # 获取自身与自身两侧最近节点所保存的ID表块的信息
    blocknamedir = client.get_blocknamedir()

    """
        1遍历左节点中保存的ID表块
        2验证身份
                1）若左节点是管理者，则备份左节点的此表块
                2）若本节点是管理者且未存此表块（常在本节点刚上线时出现），则下载左节点的此表块
                3）若其他节点是管理者，则与本节点无关
    """
    for blockname in blocknamedir['leftID']:
        managerID = client.findID(hashlib.md5(blockname))
        if managerID == IDl or (managerID == ID and not blockname in blocknamedir['myID']):
            DNSc = xmlrpc.client.ServerProxy("http://" + DNSip + ":" + DNSport + "/")
            targetip = DNSc.getip(IDl)
            rpc_download(targetip, port, path + '/' + blockname + '.txt', path + '/' + blockname + '.txt')
            rpc_download(targetip, port, path + '/' + blockname + '.md5', path + '/' + blockname + '.md5')

    """
        同上遍历右节点的ID表块
    """
    for blockname in blocknamedir['rightID']:
        managerID = client.findID(hashlib.md5(blockname))
        if managerID == IDr or (managerID == ID and not blockname in blocknamedir['myID']):
            DNSc = xmlrpc.client.ServerProxy("http://" + DNSip + ":" + DNSport + "/")
            targetip = DNSc.getip(IDr)
            rpc_download(targetip, port, path + '/'+blockname + '.txt', path + '/'+blockname + '.txt')
            rpc_download(targetip, port, path + '/' + blockname + '.md5', path + '/' + blockname + '.md5')

    """
        1遍历本节点的ID表块
        2判断管理者是否在左本右三个节点之间
                若不在，则本节点无需存此表块，执行删除表块及其验证信息的操作
    """
    for blockname in blocknamedir['myID']:
        managerID = client.findID(hashlib.md5(blockname))
        if managerID != ID and managerID != IDl and managerID != IDr:
            blockfile = './%s.txt' % blockname
            verifyfile = './%s.md5' % blockname
            if os.path.exists(blockfile):
                os.remove(blockfile)
            if os.path.exists(verifyfile):
                os.remove(verifyfile)

# 获取ID表块
myname = socket.getfqdn(socket.gethostname())
myip = socket.gethostbyname(myname)
# 默认DNSip，可初始化修改
DNSip = "192.168.43.195"
# 默认软件使用端口
DNSport = "1234"
port = "1234"
# 默认ID表块数
num = 6


def strcmplmt(x):
    return x + ".txt"

def collectIDblock(filename, client: RouteClient):
    # 收集ID表块

    blocknames = ['%sIDblock_%d' % (filename, x) for x in range(num)]
    _targetID = list(map(hashlib.md5, blocknames))
    targetID = list(map(client.findID, _targetID))
    DNSc = xmlrpc.client.ServerProxy("http://" + DNSip + ":" + DNSport + "/")
    targetip = list(map(DNSc.getip, targetID))  # -------------------
    blockfilenames = list(map(strcmplmt, blocknames))
    for i in range(len(targetip)):
        rpc_download(targetip[i], port, path +'/'+blockfilenames[i], path +'/'+blockfilenames[i])
    verifications = ["%sIDblock_%d.md5" % (filename, x) for x in range(num)]
    for i in range(len(targetip)):
        rpc_download(targetip[i], port, path +'/'+verifications[i], path +'/'+verifications[i])
    # 验证文件完整
    errorlist = []
    for i in range(num):
        with open(verifications[i], 'r') as fv:
            with open(blockfilenames[i], 'r') as fb:
                if hashlib.md5(fb.read()) != fv.read():
                    errorlist.append(i)
    return errorlist, blockfilenames  # 返回验证失败的块号