import os
import xmlrpc
import threading
import config


# 校验下载到的块是否正确
# 需要块内部结构API支持
def _check_block(part_path):
    return True


def dict_add(target: dict, item):
    if target.__contains__(item):
        target[item] += 1
    else:
        target[item] = 1


def rpc_download(targetip: str, port: str, remotefilename: str, savepath: str):
    c = xmlrpc.client.ServerProxy("http://" + targetip + ":" + port + "/")
    i = 0
    # 远程文件名称，本地保存的地址
    with open(savepath, "wb") as f:
        filesize = c.getsize(remotefilename) / (1024 * 1024)
        print("size:%.2fM" % filesize)
        f.write(c.Download(remotefilename).data)
        print("Download Completed")


# 向一个节点发送下载申请
def _download_from_ip(path: str, package: str, index: int, ip: str, port: str):
    # 此处参照DownloadTestAPI,但是下载API需要如下修改:
    # 1.不再使用绝对路径,根据numpy-v2.4这类信息索引本地包
    # 2. index为对面拥有的块序号,类型str
    # 3. 如果对面掉线会怎么办?这里需要加一个错误处理并且返回外层调用,写入diedNode
    file_name = package + '_' + str(index)
    abs_path = path + '/tmp_' + package + '_' + str(index) + '.tmp'
    ## 此处等待对接
    remote = get_block(package, index)
    rpc_download(ip, port, remote, abs_path)
    # 绝对路径

    return abs_path


def download_task(path, package, now_has_blocks: list, address: str, port: str, fault_node: dict, parts: list,
                  index: int, dead_nodes: list):
    try:
        part_path = _download_from_ip(path, package, index, address, port)
        block_is_valid = _check_block(part_path)
    except ConnectionRefusedError:
        if address not in dead_nodes:
            dead_nodes.append(address)
        return
    if not block_is_valid:
        os.remove(part_path)
        # 记录一次失误
        dict_add(fault_node, address)
    else:
        now_has_blocks[0] += 1
        parts.append(part_path)


# 向所有计算出的节点进行下载
def download_package(package: str, nodes: list, need: int):
    # 下载所用线程数
    thread_num = config.threads
    # 可用的临时路径
    path = config.path
    # 单一节点最大尝试次数
    retry = int(config['general']['retry'])
    parts = []
    # 记录失效节点
    dead_node = []
    # 记录错误节点和错误次数
    fault_node = {}
    # 此处可以使用多线程优化
    # 注意到此处使用列表引用类型，用于多线程修改变量
    now_has_blocks = [0]

    # node索引
    node_index = 0
    # 块数
    blocks = [i for i in range(need)]
    while now_has_blocks[0] < need:
        # 执行一次，按照thread_num启动线程
        threads = []
        if len(dead_node) >= len(nodes):
            print('all node is bad!')
            break
        for i in range(thread_num):
            if now_has_blocks[0] >= need or len(blocks) == 0:
                break
            # 确认下一个可用节点
            good_node = False
            while not good_node:
                good_node = True
                if node_index == len(nodes):
                    node_index = 0
                    good_node = False
                # 取临时地址
                tmp_adr = nodes[node_index][0]
                # 不再访问离线节点
                if tmp_adr in dead_node:
                    node_index += 1
                    good_node = False
                # 不再访问出错过多的节点
                if fault_node.__contains__(tmp_adr) and fault_node[tmp_adr] > retry:
                    node_index += 1
                    good_node = False

            # 读取节点信息
            node = nodes[node_index]
            address = node[0]
            port = node[1]
            # 执行下载
            block = blocks.pop()
            t = threading.Thread(target=download_task,
                                 args=(path, package, now_has_blocks, address,
                                       port, fault_node, parts, block, dead_node))
            threads.append(t)
            node_index += 1

        for t in threads:
            t.start()
        for t in threads:
            t.join()
