#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from fetcher import Fetcher
from scheduler import Scheduler
from processor import Processor
import lib.MyQueue.SafeQueue as SafeQueue
def main():
    #开启调度器
    Scheduler.runScheduler()
    #开启抓取器
    Fetcher.runFetcher(processNum=10)
    #开启处理器
    Processor.runProcessor()
    # print(u"cpu 个数:" + str(multiprocessing.cpu_count()))
    # for fetcher in multiprocessing.active_children():
    #     fetcher.join()
    #     print("child   p.name:" + fetcher.name + "\tp.id" + str(fetcher.pid))

    for p in SafeQueue.processList:
        p.start()
    for p in SafeQueue.processList:
        p.join()

#dev
if __name__ == '__main__':
    main()

