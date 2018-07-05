import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
import socket

max_node_num = 10000
myname = socket.getfqdn(socket.gethostname())
myip = socket.gethostbyname(myname)
# 默认DNSip，可初始化修改
DNSip = "192.168.43.195"
# 默认软件使用端口
DNSport = "1234"
port = "1234"
table = {}
id = None
socket.setsockopt(1)


def get_myID():
    return id


class RouteServer(object):
    def __init__(self, id):
        self.id = id

    def help_find(self, targetid):
        # 协助寻找节点
        # 表中没有更近的节点就返回自身
        if min(map(lambda x: abs(x - targetid), table)) >= abs(self.id - targetid):
            return [abs(self.id - targetid), self.id]
        # 否则进行递归
        else:
            for i in table.keys():
                if (abs(i - targetid) < abs(self.id - targetid)):
                    c = xmlrpc.client.ServerProxy("http://" + i + ":" + port + "/")
                    return c.help_find(targetid)

    def update(self, id, ip):
        l = max_node_num / 2
        n = 1
        while n < l:
            min = abs(table.key()[0] - 1)
            minid = 0
            for i in table.key():
                if min > abs(i - (self.id - n) % max_node_num):
                    min = abs(i - (self.id - n) % max_node_num)
                    minid = i
            if abs(id - (self.id - n)) < min:
                table.pop(minid)
                table[id] = ip
        n = 1
        while n < l:
            min = abs(table.key()[0] - 1)
            minid = 0
            for i in table.key():
                if min > abs(i - (self.id + n) % max_node_num):
                    min = abs(i - (self.id + n) % max_node_num)
                    minid = i
            if abs(id - (self.id - n)) < min:
                table.pop(minid)
                table[id] = ip
        return 0

    def ping_response(self, ip):
        # 回应ping操作
        return

    def get_blocklist(self):
        # 返回id表块中的文件名
        list = []
        folder = './'
        for root, dirs, files in os.walk(folder):
            for f in files:
                if 'ID_block' in f:
                    list.append(f[:f.find('ID_blcok')])
        return list


class RouteClient(object):
    def __init__(self, dnsip):
        DNSc = xmlrpc.client.ServerProxy("http://" + dnsip + ":" + port + "/")
        self.id = DNSc.create_id(myip)
        id = self.id
        table[id] = myip
        t = DNSc.download_all()
        s = t.keys().sort()
        for i in range(len(s)):
            if (s[i] == self.id):
                pos = i
                break
        l = max_node_num / 2
        n = 1
        while n < l:
            # 向左遍历
            # 找到离理想节点最近的节点
            mindist = max_node_num
            mini = max_node_num
            for i in range(pos + 1):
                if (abs(s[pos - i] - (self.id - n) % max_node_num)) < mindist:
                    mini = pos - i
                    mindist = abs(s[pos - i] - (self.id - n) % max_node_num)
                else:
                    if mindist != max_node_num:
                        break
            exit_code = os.system("ping " + t[s[mini]])
            if not exit_code:
                # 获取长连接信息————插入
                n = n * 2
                table[s[mini]] = t[s[mini]]
                # 通知更新二分表————插入
                c = xmlrpc.client.ServerProxy("http://" + t[s[mini]] + ":" + port + "/")
                c.update(self.id, myip)
            else:
                # 插入服务器连接
                DNSc.dele(ID)
                s.remove(s[mini])

        while n < l:
            # 向右遍历
            # 找到离理想节点最近的节点
            mindist = max_node_num
            mini = max_node_num
            for i in range(pos + 1):
                if (abs(s[pos + i] - (self.id + n) % max_node_num)) < mindist:
                    mini = pos - i
                    mindist = abs(s[pos + i] - (self.id + n) % max_node_num)
                else:
                    if mindist != max_node_num:
                        break
            exit_code = os.system("ping " + t[s[mini]])
            if not exit_code:
                # 获取长连接信息————插入
                n = n * 2
                table[s[mini]] = t[s[mini]]
                # 通知更新二分表————插入
                c = xmlrpc.client.ServerProxy("http://" + t[s[mini]] + ":" + port + "/")
                c.update(self.id, myip)
            else:
                # 插入服务器连接
                DNSc.dele(ID)
                s.remove(s[mini])

    def get_mylrID(myID):
        L = []
        for key in table.keys():
            L.append(key)
        Ls = L.sort()
        pos = 1
        for i in range(len(Ls)):
            if Ls[i] == myID:
                pos = i
                break
        return Ls[pos - 1], Ls[pos + 1]

    def ping(self, ip):
        # 检查节点是否在线
        c = xmlrpc.client.ServerProxy("http://" + ip + ":" + port + "/")
        return c.ping_response(targetid)

    def findID(self, targetid):
        # 按id寻找节点
        dis = abs(targetid - self.id)
        ip = myip
        for i in table.keys():
            # 对表中节点遍历操作
            if (abs(i - targetid) < abs(self.id - targetid)):
                c = xmlrpc.client.ServerProxy("http://" + i + ":" + port + "/")
                # 用远程调用递归查询
                res = c.help_find(targetid)
                if (dis > res[0]):
                    dis = res[0]
                    ip = res[1]
        # 若没有更近的最近的就是自己
        return ip

    def get_blocknamedir(self):
        l, r = self.get_mylrID()
        blocknamedir = {}
        id = l
        s = xmlrpc.client.ServerProxy("http://" + id + ":" + port + "/")
        blocknamedir['leftID'] = s.get_blocklist()
        id = r
        s = xmlrpc.client.ServerProxy("http://" + id + ":" + port + "/")
        blocknamedir['rightID'] = s.get_blocklist()
        id = self.id
        s = xmlrpc.client.ServerProxy("http://" + id + ":" + port + "/")
        blocknamedir['myID'] = s.get_blocklist()


if __name__ == "__main__":
    port = "1234"
    c = Client(DNSip)
    server = Server(id)
    s = SimpleXMLRPCServer(("0.0.0.0", int(port)))
    print("start service...")
    s.register_instance(server)
    s.serve_forever()
