# 这里是本地节点可以执行的与远程交互的操作
import os
import sys

import xmlrpc
from ..model.LocalAdmin import LocalAdmin

from .IDops import addmyID, collectIDblock, get_downloadID
from .DOWNops import download_package


def init_network(admin: LocalAdmin, server, serverip: str, port: str):
    communication = xmlrpc.client.ServerProxy("http://" + serverip + ":" + port + "/")

    # 新节点向dns服务器申请id
    server.id = communication.get_myID()
    # 新节点下载完整的映射表
    ## 此处留待补充
    communication.download_all()

    admin.extract_installed_list()
    for package in admin.installed.keys():
        filename = package + '_' + admin.installed[package]
        addmyID(filename)


def download(package: str):
    need = 4
    _, blockfilenames = collectIDblock()
    nodes = get_downloadID(blockfilenames, 10)
    download_package(package, nodes, need)


# 请求root
def ask_root():
    # 申请root权限
    if os.geteuid():
        args = [sys.executable] + sys.argv
        os.execlp('sudo', 'sudo', *args)


# 能解决依赖的dpkg安装调用
def dpkg_install(path: str):
    ask_root()
    resq = os.popen('dpkg -i {0}'.format(path))
    print(resq.read())

