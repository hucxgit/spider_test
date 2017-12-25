#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import lib.MyDecorator as MyDecorator
from lib.Utils.ProcessorUtil import ProcessorUtil
from lib.Utils import HttpUtil
# from  import BaidumaoSpider,baidumap
import time
import redis
r = redis.StrictRedis(host='localhost',port=6379,db=0)
from BaiduSpider2_new import  BaidumaoSpider
@MyDecorator.SchedulerDecorator(name="baidumapScheduler")
def getTask(*args,**kwargs):
    offset = args[0]
    num = args[1]
    if offset == 5000:
        objs = r.lrange("maps",558080,568080)
        # args[1] = 5001
        return objs
    else:
        return []





@MyDecorator.FetcherDecorator(name="baidumapFetcher")
def fetcher(*args,**kwargs):
    preQueue = kwargs['preQueue']
    url = preQueue.get(block=False)
    # crawlResultDic = HttpUtil.httpRequest(id[0])
    resultlist = BaidumaoSpider.post_request(url)
    time.sleep(0.05)
    return resultlist



@MyDecorator.ProcessorDecorator(name="baidumapProcessor")
def processor(*args,**kwargs):
    import copy,time
    downQueue = kwargs['downQueue']
    preToUpdate = kwargs['preToUpdate']
    if downQueue.qsize()>0:
        # for i in range(100):
        resultlist = downQueue.get(block=False)
        resultlist=BaidumaoSpider.genresultlist(resultlist)
        BaidumaoSpider.save_data(resultlist)
        # preToUpdate.append(orderDic)
        # data = copy.deepcopy(preToUpdate)
        # preToUpdate = []
        # ProcessorUtil.updateListBatch(data)
        # time.sleep(3)
        pass
    else:
        time.sleep(1)



def runTask(self):
    preQueue = self._args[0]
    offset = self._args[1]
    num = self._args[2]
    getTask(offset,num,preQueue=preQueue,one=False)
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