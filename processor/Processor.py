#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import multiprocessing
from lib.MyQueue import SafeQueue
class Processor(multiprocessing.Process):
    ''''
    def __init__(self, interval):
        multiprocessing.Process.__init__(self)
        self.interval = interval
    '''
    def run(self):
        func = self._kwargs['func']
        if func is not None:
            func(self)
        pass
def runProcessor(func=None):
    processor = Processor(name="processor", args=(SafeQueue.donwCrawlQueue,[]),kwargs={'func':func})
    # 加入池子
    SafeQueue.processList.append(processor)
    pass


if __name__ == '__main__':
    runProcessor()
    pass