#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import multiprocessing
from lib.MyQueue import SafeQueue
class Fetcher(multiprocessing.Process):
    def run(self):
        func = self._kwargs['func']
        if func is not None:
            func(self)
        pass

def runFetcher(processNum=1,func=None):
    # 实例化了进程并且放进了列表里
    for i in range(processNum):
        preCrawlQueue = SafeQueue.preCrawlQueue
        donwCrawlQueue = SafeQueue.donwCrawlQueue
        fetcher = Fetcher(name="Fetcher"+str(i), args=(preCrawlQueue,donwCrawlQueue),kwargs={'func':func})
        #加入池子
        SafeQueue.processList.append(fetcher)
    pass
if __name__ == '__main__':
    #runFetcher(processNum=2)
    #print("main end")
    pass