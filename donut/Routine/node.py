from operator import itemgetter
import heapq

class Node:
    def __init__(self,node_id, ip=None, port=None):
        self.id = node_id
        self.l_id = None
        self.r_id = None
        self.id = node_id
        self.ip = ip
        self.port = port
        self.long_id = int(node_id.hex(), 16)

    def sameHomeAs(self, node):
        return self.ip == node.ip and self.port == node.port

    def distanceTo(self, node):
        """
        Get the distance between this node and another.
        """
        return self.long_id ^ node.long_id

    def __iter__(self):
        """
        Enables use of Node as a tuple - i.e., tuple(node) works.
        """
        return iter([self.id, self.ip, self.port])

    def __repr__(self):
        return repr([self.long_id, self.ip, self.port])

    def __str__(self):
        return "%s:%s" % (self.ip, str(self.port))