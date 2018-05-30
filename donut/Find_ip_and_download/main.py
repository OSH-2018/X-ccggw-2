# 1. 根据软件包名称在本地缓存搜索对应的软件包组合名 -- done
# 2. 根据软件包组合名hash取余得到物理机id -- done
# 3. 从十分表读取最近的id -- wait
# 4. 向其请求得到软件id表块
# 5. 接收到10个,退出
# 6. 恢复成软件包

# 这里的变量最后会改成动态控制
config_file_name = 'Release'
find_package_name = 'numpy'

import configparser
import hashlib
import csv
import os
import xml
import zerorpc # need to be replaced

from tools import dict_add

# 从本地软件包索引缓存中查找需要的软件包, 并返回软件包名哈希值
def search_package(package_name: str, version=None):
    # 转换为小写
    package_name = package_name.lower()
    # 从config读取meta文件位置
    config = configparser.ConfigParser()
    config.read(config_file_name)
    meta_path = config['general']['meta']

    # 读取meta文件
    with open(meta_path, 'r') as f:
        lines = list(csv.reader(f))

    # 提取所有软件包名
    lines = [line[0] for line in lines]
    # 查找出本软件包的不同版本
    names = [package for package in list(lines) if package_name in package]
    # 未输入版本号,默认使用存在的最新版本
    if version == None:
        info = max(names)
        print('getting packing {0} from local...'.format(info))
        return hashlib.md5(str.encode(info))
    # 输入的版本号存在,进一步查找
    elif package_name + '-' + version in names:
        info = package_name + '-' + version
        print('getting packing {0} from local...'.format(info))
        return hashlib.md5(str.encode(info))
    # 输入的版本号未找到,提示是否继续
    else:
        info = package_name + '-' + version
        choose = input('cannot find packing-{0} at local...\n'
                       'what do you want to do?\n'
                       '1. update local package lists\n'
                       '2. force continue\n'
                       'else. quit\n'.format(info))
        if choose == 1:
            raise NotImplementedError
        elif choose == 2:
            return hashlib.md5(str.encode(info))
        else:
            return None

# 用软件包名哈希值计算出拥有id表块的索引值
def cal_node_id(hash: str):
    # 从config读取meta文件位置
    config = configparser.ConfigParser()
    config.read(config_file_name)

    # 读取最大节点数目和最大储存数目
    max_node = int(config['source']['maxNode'])
    restore = int(config['source']['restore'])

    # 计算应该带有id表块的节点
    store_nodes = []
    hash = int(hash, 16)
    print(hash)
    remain = hash % (max_node // restore)

    for i in range(restore):
        store_nodes.append(i * (max_node // restore) + remain)

    return store_nodes

# 从理论节点查找出实际存在的节点
def ensure_actual_node(nodes: list):
    # 从十分表中获取实际的节点
    # 因为10分表结构未知所以暂不完成
    # 返回ip和port
    pass

# 向一个节点发送下载申请
def _download_from_ip(path: str, package: str, index: str, ip: str, port: str):
    cli = zerorpc.Client()
    cli.connect('tcp://' + ip + ':' + port)
    # 此处参照DownloadTestAPI,但是下载API需要如下修改:
    # 1.不再使用绝对路径,根据numpy-v2.4这类信息索引本地包
    # 2. index为对面拥有的块序号,类型str
    # 3. 如果对面掉线会怎么办?这里需要加一个错误处理并且返回外层调用,写入diedNode
    data = cli.download(package, index)
    # 绝对路径
    abs_path = path + 'tmp_' + package + index
    with open(abs_path, 'w') as f:
        f.write(data)
    return abs_path

# 校验下载到的块是否正确
# 需要块内部结构API支持
def _check_block(part_path):
    return True

# 向所有计算出的节点进行下载
def download_package(package: str, nodes: list):
    # 从config读取需求份数
    config = configparser.ConfigParser()
    config.read(config_file_name)
    # 需求最少块数
    need = int(config['source']['split'])
    # 可用的临时路径
    path = config['general']['path']
    # 单一节点最大尝试次数
    retry = int(config['general']['retry'])
    parts = []
    # 记录失效节点
    died_node = []
    # 记录错误节点和错误次数
    fault_node = {}
    # 此处可以使用多线程优化
    now_has_blocks = 0
    while now_has_blocks < need + 2:
        for node in nodes:
            # 为预防有人给虚假块,必须多要两个
            if now_has_blocks >= need + 2:
                break
            address = node[0]
            port = node[1]
            # 不再访问离线节点
            if address in died_node:
                continue
            # 不再访问出错过多的节点
            if fault_node.__contains__(address) and fault_node[address] > retry:
                continue
            # 此处直接试图询问下一块,后期需修改到先询问对面拥有的块数选择一块
            part_path = _download_from_ip(path, package, now_has_blocks, address, port)
            block_is_valid = _check_block(part_path)
            if not block_is_valid:
                os.remove(part_path)
                # 记录一次失误
                dict_add(fault_node, address)
            else:
                now_has_blocks += 1
                parts.append(part_path)

# 调用apt update 更新缓存
def update_list():
    pass
hash = search_package('numpy').hexdigest()
print(cal_node_id(hash))
# search_package('numpy', '4.1')
# search_package('numpy', '9.2')
