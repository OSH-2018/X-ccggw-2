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
        self.storage = storage
        self.sourceNode = sourceNode

    def rpc_get_id(self, sender):
      '''
      得到id信息
      '''
      source = Node(nodeid, sender[0], sender[1])
      self.welcomeIfNewNode(source)
      dic={}
      dic['id']=self.sourceNode.id
      dic['l_id'] = self.sourceNode.l_id
      dic['r_id'] = self.sourceNode.r_id
      return dic

    def rpc_ping(self, sender, nodeid):
        ''' 
        ping操作,检测是否在线
        '''
        source = Node(nodeid, sender[0], sender[1])
        self.welcomeIfNewNode(source)
        return self.sourceNode.id

    def rpc_find_node(self, sender, nodeid, key):
        '''
        寻找节点
        '''
        log.info("finding neighbors of %i in local table",
                 int(nodeid.hex(), 16))
        source = Node(nodeid, sender[0], sender[1])
        self.welcomeIfNewNode(source)
        node = Node(key)
        neighbors = self.router.findNeighbors(node, exclude=source)
        return list(map(tuple, neighbors))


    async def callFindNode(self, nodeToAsk, nodeToFind):
        address = (nodeToAsk.ip, nodeToAsk.port)
        result = await self.find_node(address, self.sourceNode.id,
                                      nodeToFind.id)
        return self.handleCallResponse(result, nodeToAsk)


    async def callPing(self, nodeToAsk):
        address = (nodeToAsk.ip, nodeToAsk.port)
        result = await self.ping(address, self.sourceNode.id)
        return self.handleCallResponse(result, nodeToAsk)

    async def callGetId(self, nodeToAsk):
        address = (nodeToAsk.ip, nodeToAsk.port)
        result = await self.get_id(address, self.sourceNode.id)
        return self.handleCallResponse(result, nodeToAsk)


    def welcomeIfNewNode(self, node):
        '''
        对新节点进行处理 （未完成
        '''
        if not self.router.isNewNode(node):
            return
        '''
        log.info("never seen %s before, adding to router", node)
        for key, value in self.storage.items():
            keynode = Node(digest(key))
            neighbors = self.router.findNeighbors(keynode)
            if len(neighbors) > 0:
                last = neighbors[-1].distanceTo(keynode)
                newNodeClose = node.distanceTo(keynode) < last
                first = neighbors[0].distanceTo(keynode)
                thisNodeClosest = self.sourceNode.distanceTo(keynode) < first
            if len(neighbors) == 0 or (newNodeClose and thisNodeClosest):
                asyncio.ensure_future(self.callStore(node, key, value))
        self.router.addContact(node)

     '''
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