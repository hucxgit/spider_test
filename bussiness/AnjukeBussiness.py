#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import lib.MyDecorator as MyDecorator
from lib.Utils.ProcessorUtil import ProcessorUtil
from lib.Utils import HttpUtil

@MyDecorator.SchedulerDecorator(name="anjukeScheduler")
def getTask(*args,**kwargs):
    offset = args[0]
    num = args[1]
    objs = ProcessorUtil.findUnUpdatedListAnjuke("84771", offset, num)
    return objs



@MyDecorator.FetcherDecorator(name="anjukeFetcher")
def fetcher(*args,**kwargs):
    preQueue = kwargs['preQueue']
    obj = preQueue.get(block=False)

    import random,time
    sleepTime = random.randint(5, 10)
    time.sleep(sleepTime)
    resultObj = HttpUtil.httpRequestAnjuke(obj[0],obj[1])
    return resultObj



@MyDecorator.ProcessorDecorator(name="anjukeFetcher")
def processor(*args,**kwargs):
    import copy,time
    downQueue = kwargs['downQueue']
    #preToUpdate = kwargs['preToUpdate']
    preEstateData = []
    preEstateImageData = []
    if downQueue.qsize() >= 20:
        for i in range(20):
            obj = downQueue.get(block=False)
            preEstateData.append(obj[0])
            for tmp in obj[1]:
                preEstateImageData.append(tmp)
        ProcessorUtil.updateAnjukeListBatch(preEstateData)
        ProcessorUtil.updateAnjukeImageBatch(preEstateImageData)
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