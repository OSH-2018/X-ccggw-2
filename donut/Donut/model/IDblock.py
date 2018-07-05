import json
import hashlib
import socket
import os
from os.path import join

import config

myname = socket.getfqdn(socket.gethostname())
myip = socket.gethostbyname(myname)
# 默认DNSip，可初始化修改
DNSip = "192.168.43.195"
# 默认软件使用端口
DNSport = "1234"
port = "1234"
# 默认ID表块数
num = 6

''' 加入deleID     get_downloadID'''


class IDServer(object):

    #   常驻的关于被动ID表块更新，创建，管理备份的类

    def __init__(self):
        self.addID()
        self.create_IDblock()
        self.path = config.path

    # ID表块项的添加
    def addID(self, blockname, ID):
        # 判断表块是否存在，若不存在先创建
        if not os.path.exists(join(self.path, '%s.txt') % blockname):
            self.create_IDblock(blockname)

        # 添加新的表块ID项
        with open(join(self.path, '%s.txt') % blockname, 'r+') as f:
            block = json.loads(f.read())
            block["IDlist"].append(ID)
            json_block = json.dumps(block)
            f.write(json_block)

        # 重新生成验证信息
        verification = hashlib.md5(json_block)
        with open(join(self.path, '%s.md5') % blockname, 'w') as f:
            f.write(verification)
        return 1  # 成功更新

    def create_IDblock(self, blockname):

        # 若是已经存在则不需要创建
        if os.path.exists(join(self.path, blockname + '.txt')):
            return 0

        # 初始化信息
        block = {}
        IDlist = []
        """
            结构为：{
                "name" : %s
                "IDlist": []
            }
        """
        block["IDlist"] = IDlist
        block["name"] = blockname

        # 导为json字符串
        json_block = json.dumps(block)

        # 生成验证信息，并保存块与验证信息
        verification = hashlib.md5(json_block)
        with open(join(self.path, "%s.txt") % blockname, 'w') as f:
            f.write(json_block)
        with open(join(self.path, "%s.md5") % blockname, 'w') as f:
            f.write(verification)
        return 1  # 成功创建

    def deleID(self, blockname, ID):
        # 判断表块是否存在，若不存在先创建
        if not os.path.exists(join(self.path, '%s.txt') % blockname):
            return "target block Not exist!"

        # 删除表块ID项
        with open(join(self.path, '%s.txt') % blockname, 'r+') as f:
            block = json.loads(f.read())
            block["IDlist"].remove(ID)
            json_block = json.dumps(block)
            f.write(json_block)

        # 重新生成验证信息
        verification = hashlib.md5(json_block)
        with open(join(self.path, '%s.md5') % blockname, 'w') as f:
            f.write(verification)
        return 1  # 成功更新
