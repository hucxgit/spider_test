#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import Queue
import multiprocessing
import time

from lib.MyQueue import SafeQueue
from lib.Utils.ProcessorUtil import ProcessorUtil


class Scheduler(multiprocessing.Process):
    ''''
    def __init__(self, interval):
        multiprocessing.Process.__init__(self)
        self.interval = interval
    '''
    def run(self):
        print(self._name)
        preQueue = self._args[0]
        offset = self._args[1]
        num = self._args[2]
        while True:
            try:
                objs = ProcessorUtil.findUnUpdatedList("B0015042AF",offset,num)
                print(self._name +" 发网络请求去抓取数据 获取了"+str(len(objs))+"条数据")
                for obj in objs:
                    preQueue.put(obj[0],block=False)

                print(self._name + " 待抓取的队列有" + str(preQueue.qsize()) + "条数据")
                time.sleep(60)
                if len(objs) <=1:
                    time.sleep(5)
                offset +=num
            except Queue.Full as e:
                print(self._name +" 待抓取队列满了  ")
                print(e)
            finally:
                pass

def runScheduler():
    scheduler = Scheduler(name="scheduler", args=(SafeQueue.preCrawlQueue,0,100))
    #scheduler.start()

    #加入池子
    SafeQueue.processList.append(scheduler)
    pass


if __name__ == '__main__':
    runScheduler()
    pass