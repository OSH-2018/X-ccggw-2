# 这里是本地节点对自我的软件包管理部分

import hashlib
import os
import urllib
import config


# 本地文件管理器
class LocalAdmin:
    def __init__(self):
        self.installed = []
        self.extract_installed_list()

    # 从dpkg索引中读取所有安装好的软件
    def extract_installed_list(self):
        resq = os.popen('dpkg -l | grep ^ii | awk \'{print $2, $3}\'').readlines()
        self.installed = [p.rstrip('\n') for p in resq]
        self.installed = {p.split(' ')[0]: p.split(' ')[1] for p in self.installed}

    # 对于一个软件包给出其所有的DEBAIN控制文件
    def get_debian_files(selff, package_name: str):
        path = '/var/lib/dpkg/info'
        allFiles = os.listdir(path)
        allFiles = [file for file in allFiles if file.startswith(package_name + '.')]
        # 最终应赋予的文件名
        allName = [file[file.index('.') + 1:] for file in allFiles]
        # 各文件所在的路径
        allPath = [os.path.join(path, file) for file in allFiles]
        pathList = dict(zip(allName, allPath))
        return pathList

    def collector_file(self, package: str):
        """get the information from system, and collect them"""
        command = "dpkg-query -L {0}".format(package)
        resq = os.system(command).read()
        file_list = []
        folder_list = []
        with open(self.location_file, 'r') as file:
            path = file.readlines()
            for p in path[1:]:
                file_list.append(p.strip())
        length = len(file_list)
        for i in range(length):
            for p in file_list[1 + i:]:
                if file_list[i] in p and p.count('/') > file_list[i].count('/'):
                    folder_list.append(file_list[i])
                    file_list[i] = ''
                    break
        for i in range(len(folder_list)):
            file_list.remove('')
        self.copy_file(set(file_list), set(folder_list))

    def get_list_from_apt(self):
        items = os.popen('apt list').readlines()
        data = [item.split('/')[0] for item in items[1:]]
        with open('./data/all.list', "w") as f:
            f.writelines(data)

    # 从本地软件包索引缓存中查找需要的软件包, 并返回软件包名哈希值
    def search_package(self, package_name: str, version=None):
        # 转换为小写
        package_name = package_name.lower()
        # 从config读取meta文件位置
        meta_path = config.meta

        if not config['general'].__contains__('meta'):
            url = config.meta_url
            file_name = 'packages' + '.list'
            if url != 'apt':
                content = urllib.urlopen(url)
                data = content.read()
                with open(meta_path, "w") as f:
                    f.write(data)
            else:
                if not os._exists('./data/all.list'):
                    self.get_list_from_apt()
                meta_path = './data/all.list'

        # 读取meta文件
        with open(meta_path, 'r') as f:
            lines = f.readlines()

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
                           'what do you force to do?(y/n)\n'.format(info))
            if choose == 'n' or 'N':
                return None
            elif choose == 'y' or 'Y':
                return hashlib.md5(str.encode(info))


a = LocalAdmin()
a.extract_installed_list()
print(a.get_debian_files('gcc'))
