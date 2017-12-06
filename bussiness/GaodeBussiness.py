#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import lib.MyDecorator as MyDecorator
from lib.Utils.ProcessorUtil import ProcessorUtil
from lib.Utils import HttpUtil

@MyDecorator.SchedulerDecorator(name="gaodeScheduler")
def getTask(*args,**kwargs):
    offset = args[0]
    num = args[1]
    objs = ProcessorUtil.findUnUpdatedList("B0015042AF", offset, num)
    return objs



@MyDecorator.FetcherDecorator(name="gaodeFetcher")
def fetcher(*args,**kwargs):
    preQueue = kwargs['preQueue']
    id = preQueue.get(block=False)
    crawlResultDic = HttpUtil.httpRequest(id[0])
    return crawlResultDic



@MyDecorator.ProcessorDecorator(name="gaodeFetcher")
def processor(*args,**kwargs):
    import copy,time
    downQueue = kwargs['downQueue']
    preToUpdate = kwargs['preToUpdate']
    if downQueue.qsize() >= 100:
        for i in range(100):
            orderDic = downQueue.get(block=False)
            preToUpdate.append(orderDic)
        data = copy.deepcopy(preToUpdate)
        preToUpdate = []
        ProcessorUtil.updateListBatch(data)
        time.sleep(3)
        pass
    else:
        time.sleep(3)



def runTask(self):
    preQueue = self._args[0]
    offset = self._args[1]
    num = self._args[2]
    getTask(offset,num,preQueue=preQueue)
    pass

def runFetcher(self):
    preCrawlQueue = self._args[0]
    donwCrawlQueue = self._args[1]
    fetcher(preQueue=preCrawlQueue,downQueue=donwCrawlQueue)
    pass

def runProcessor(self):
    donwCrawlQueue = self._args[0]
    preToUpdate = self._args[1]
    processor(downQueue=donwCrawlQueue,preToUpdate=preToUpdate)
    pass