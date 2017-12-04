#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import Queue
import multiprocessing
import time

from lib.MyQueue import SafeQueue
from lib.Utils import HttpUtil


class Fetcher(multiprocessing.Process):
    '''
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        multiprocessing.Process.__init__(self,group=group, target=target, name=name, args=args, kwargs=kwargs)
    '''
    def run(self):
        print(self._name)
        preQueue = self._args[0]
        downQueue = self._args[1]
        while True:
            try:
                print(self._name + "  发网络请求去抓取数据")
                id = preQueue.get(block=False)
                crawlResultDic = HttpUtil.httpRequest(id)
                if crawlResultDic is not None:
                    downQueue.put(crawlResultDic, block=False)
                else:
                    print("网络获取返回结果为空")
                    pass
                time.sleep(3)
            except Queue.Full as e:
                print(self._name + "  抓取结果对列满了 ")
                print(e)
            except Queue.Empty as e:
                print(self._name +  " 待抓取队列为空 从待抓取队列获取异常 ")
                print(e)

            finally:
                pass

def runFetcher(processNum=1):
    for i in range(processNum):
        fetcher = Fetcher(name="Fetcher"+str(i), args=(SafeQueue.preCrawlQueue, SafeQueue.donwCrawlQueue))
        #fetcher.start()

        # 加入池子
        SafeQueue.processList.append(fetcher)
    pass
if __name__ == '__main__':
    runFetcher(processNum=2)
    print("main end")
