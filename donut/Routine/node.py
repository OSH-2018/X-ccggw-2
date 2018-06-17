from operator import itemgetter
import heapq

class Node:
    def __init__(self, node_id, l_id=None, r_id=None, ip=None, port=None):
        self.id = node_id
        self.l_id = l_id
        self.r_id = r_id
        self.ip = ip
        self.port = port
        self.long_id = int(node_id.hex(), 16)

    def sameHomeAs(self, node):
        return self.ip == node.ip and self.port == node.port

    def distanceTo(self, node):
        """
        获得距离
        """
        return self.long_id ^ node.long_id

    def __iter__(self):
        return iter([self.id, self.ip, self.port])

    def __repr__(self):
        return repr([self.long_id, self.ip, self.port])

    def __str__(self):
        return "%s:%s" % (self.ip, str(self.port))

class NodeHeap(object):
    """
    用堆由近到远地储存节点序列
    """
    def __init__(self, node, maxsize):
        self.node = node
        #作为测量距离使用的node
        self.heap = []
        self.contacted = set()
        self.maxsize = maxsize

    def remove(self, peerIDs):
        """
        移除peerID
        """
        peerIDs = set(peerIDs)
        if len(peerIDs) == 0:
            return
        nheap = []
        for distance, node in self.heap:
            if node.id not in peerIDs:
                heapq.heappush(nheap, (distance, node))
        self.heap = nheap

    def getNodeById(self, node_id):
        for _, node in self.heap:
            if node.id == node_id:
                return node
        return None

    def allBeenContacted(self):
        return len(self.getUncontacted()) == 0

    def getIDs(self):
        return [n.id for n in self]

    def markContacted(self, node):
        self.contacted.add(node.id)

    def popleft(self):
        if len(self) > 0:
            return heapq.heappop(self.heap)[1]
        return None

    def push(self, nodes):
        """
        节点加入list
        """
        if not isinstance(nodes, list):
            nodes = [nodes]

        for node in nodes:
            if node not in self:
                distance = self.node.distanceTo(node)
                heapq.heappush(self.heap, (distance, node))

    def __len__(self):
        return min(len(self.heap), self.maxsize)

    def __iter__(self):
        nodes = heapq.nsmallest(self.maxsize, self.heap)
        return iter(map(itemgetter(1), nodes))

    def __contains__(self, node):
        for _, n in self.heap:
            if node.id == n.id:
                return True
        return False

    def getUncontacted(self):
        return [n for n in self if n.id not in self.contacted]