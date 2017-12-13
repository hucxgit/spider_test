#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import multiprocessing
from lib.MyQueue import SafeQueue
class Scheduler(multiprocessing.Process):
    def run(self):
        func = self._kwargs['func']
        if func is not None:
            print("开始调用")
            print(func)
            func(self)
        pass

def runScheduler(func=None):
    # 其实就是实例化了的一个进程并放进列表里
    preCrawlQueue = SafeQueue.preCrawlQueue
    scheduler = Scheduler(name="scheduler", args=(preCrawlQueue,5000,600),kwargs={'func':func})
    #加入池子
    SafeQueue.processList.append(scheduler)
    pass


if __name__ == '__main__':
    runScheduler()
    pass
