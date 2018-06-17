import random
import asyncio
import logging

from rpcudp.protocol import RPCProtocol

from node import Node
from routing import RoutingTable
#from kademlia.utils import digest

log = logging.getLogger(__name__)



class Protocol(RPCProtocol):
    def __init__(self, sourceNode, storage, ksize):
        RPCProtocol.__init__(self)
        self.router = RoutingTable(self, ksize, sourceNode)
        self.idblock = storage
        self.sourceNode = sourceNode

    def store(self, sender, nodeid, key, value):
       '''
       移交id表块    
       '''
       source = Node(nodeid, sender[0], sender[1])
       self.welcomeIfNewNode(source)
       self.idblock[key] = value
       return True
       pass

    def ping(self, sender, nodeid):
        ''' 
        ping操作,检测是否在线
        '''
        source = Node(nodeid, sender[0], sender[1])
        self.welcomeIfNewNode(source)
        dic = {}
        dic['id'] = self.sourceNode.id
        dic['l_id'] = self.sourceNode.l_id
        dic['r_id'] = self.sourceNode.r_id
        #返回一个包含节点与它左右最近的节点的字典
        return dic

    def find_node(self, sender, nodeid, key):
        '''
        寻找节点
        '''
        log.info("finding neighbors of %i in local table",
                 int(nodeid.hex(), 16))
        source = Node(nodeid, sender[0], sender[1])
        self.welcomeIfNewNode(source)
        node = Node(key)
        neighbors = self.router.findNeighbors(node, exclude=source)
        #找出离目标节点最近的若干节点
        return list(map(tuple, neighbors))

    #协程操作
    async def callStore(self, nodeToAsk, key, value):
        address = (nodeToAsk.ip, nodeToAsk.port)
        result = await self.store(address, self.sourceNode.id, key, value)
        return self.handleCallResponse(result, nodeToAsk)

    async def callFindNode(self, nodeToAsk, nodeToFind):
        address = (nodeToAsk.ip, nodeToAsk.port)
        result = await self.find_node(address, self.sourceNode.id,
                                      nodeToFind.id)
        return self.handleCallResponse(result, nodeToAsk)


    async def callPing(self, nodeToAsk):
        address = (nodeToAsk.ip, nodeToAsk.port)
        result = await self.ping(address, self.sourceNode.id)
        return self.handleCallResponse(result, nodeToAsk)



    def welcomeIfNewNode(self, node):
        '''
        对新节点进行处理 
        '''
        if not self.router.isNewNode(node):
            return
        log.info("never seen %s before, adding to router", node)
        for key, value in self.storage.items():
        #检查节点是否离某些负责文件的id近
            keynode = Node(digest(key))
            neighbors = self.router.findNeighbors(keynode)
        #找出离目标节点最近的若干节点
            if len(neighbors) > 0:
                second = neighbors[1].distanceTo(keynode)
            if len(neighbors) == 0 or (node.distanceTo(keynode)<second):
                asyncio.ensure_future(self.callStore(node, key, value))
        #如果节点离负责id表块的id更近 则通知存储
        self.router.addContact(node)
        #将该节点加入路由表

    def handleCallResponse(self, result, node):
        """
        对回应进行处理
        """
        if not result[0]:
            log.warning("no response from %s, removing from router", node)
            self.router.removeContact(node)
            return result

        log.info("got successful response from %s", node)
        self.welcomeIfNewNode(node)
        return result