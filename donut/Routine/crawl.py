from collections import Counter
import logging

from node import Node,Nodeheap

log = logging.getLogger(__name__)

async def gather_dict(d):
    cors = list(d.values())
    results = await asyncio.gather(*cors)
    return dict(zip(d.keys(), results))


class SpiderCrawl(object):
    """
    响应寻找符合id的节点的过程
    """
    def __init__(self, protocol, node, peers, ksize, alpha):

        self.protocol = protocol
        #协议文件即protocal.py
        self.ksize = ksize
        #自定义参数ksize
        self.alpha = alpha
        #一个可变参数
        self.node = node
        #节点
        self.nearest = NodeHeap(self.node, self.ksize)
        #用堆储存最近节点序列
        self.lastIDsCrawled = []
        #储存上次的结果
        log.info("creating spider with peers: %s", peers)
        self.nearest.push(peers)
        #peers作为入口

    async def _find(self, rpcmethod):
        """
        寻找由近到远的一列节点
        """
        log.info("crawling network with nearest: %s", str(tuple(self.nearest)))
        count = self.alpha
        if self.nearest.getIDs() == self.lastIDsCrawled:
            count = len(self.nearest)
        self.lastIDsCrawled = self.nearest.getIDs()
        #储存上次的结果

        ds = {}
        for peer in self.nearest.getUncontacted()[:count]:
            #对未连接的节点进行遍历
            ds[peer.id] = rpcmethod(peer, self.node)
            self.nearest.markContacted(peer)
            #操作完成后加入连接列表
        found = await gather_dict(ds)
        return await self._nodesFound(found)

    async def _nodesFound(self, responses):
        raise NotImplementedError


class ValueSpiderCrawl(SpiderCrawl):
    def __init__(self, protocol, node, peers, ksize, alpha):
        SpiderCrawl.__init__(self, protocol, node, peers, ksize, alpha)
        self.nearestWithoutValue = NodeHeap(self.node, 1)

    async def find(self):
        '''
        查找 
        '''
        return await self._find(self.protocol.callFindValue)

    async def _nodesFound(self, responses):
        """
        返回查找请求的结果.
        """
        toremove = []
        foundValues = []
        for peerid, response in responses.items():
            response = RPCFindResponse(response)
            if not response.happened():
                toremove.append(peerid)
            elif response.hasValue():
                foundValues.append(response.getValue())
            else:
                peer = self.nearest.getNodeById(peerid)
                self.nearestWithoutValue.push(peer)
                self.nearest.push(response.getNodeList())
        self.nearest.remove(toremove)

        if len(foundValues) > 0:
            return await self._handleFoundValues(foundValues)
        if self.nearest.allBeenContacted():
            # 未找到的情况
            return None
        return await self.find()

    async def _handleFoundValues(self, values):
        """
        对结果进行操作
        """
        valueCounts = Counter(values)
        if len(valueCounts) != 1:
            log.warning("Got multiple values for key %i: %s",
                        self.node.long_id, str(values))
        value = valueCounts.most_common(1)[0][0]

        peerToSaveTo = self.nearestWithoutValue.popleft()
        if peerToSaveTo is not None:
            await self.protocol.callStore(peerToSaveTo, self.node.id, value)
        return value


class NodeSpiderCrawl(SpiderCrawl):
    async def find(self):
        """
        寻找最近节点
        """
        return await self._find(self.protocol.callFindNode)

    async def _nodesFound(self, responses):
        """
        对_find迭代结果进行处理
        """
        toremove = []
        for peerid, response in responses.items():
            response = RPCFindResponse(response)
            if not response.happened():
                toremove.append(peerid)
            else:
                self.nearest.push(response.getNodeList())
        self.nearest.remove(toremove)

        if self.nearest.allBeenContacted():
            return list(self.nearest)
        return await self.find()


class RPCFindResponse(object):
    def __init__(self, response):

        self.response = response
        #包括接收到的应答和值的一个tuple

    def happened(self):
        """
        检查是否是有效应答
        """
        return self.response[0]

    def hasValue(self):

        return isinstance(self.response[1], dict)

    def getValue(self):

        return self.response[1]['value']

    def getNodeList(self):
        '''
         获得节点序列
        '''
        nodelist = self.response[1] or []
        return [Node(*nodeple) for nodeple in nodelist]