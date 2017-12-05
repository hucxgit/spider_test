#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import Queue,copy,time
import multiprocessing

from lib.MyQueue import SafeQueue
from lib.Utils.ProcessorUtil import ProcessorUtil


class Processor(multiprocessing.Process):
    ''''
    def __init__(self, interval):
        multiprocessing.Process.__init__(self)
        self.interval = interval
    '''
    def run(self):
        print(self._name)
        downQueue = self._args[0]
        preToUpdate = self._args[1]
        while True:
            try:
                if downQueue.qsize()>=100:
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
            except Queue.Empty as e:
                print(self._name +" 去取抓取结果 准备更新 抓取结果对列空了")
                time.sleep(0.5)
                print(e)
            except Exception as e:
                print(self._name + " 执行sql导致了异常")
                print(e)
            finally:
                pass

def runProcessor():
    processor = Processor(name="processor", args=(SafeQueue.donwCrawlQueue,[]))
    #processor.start()

    # 加入池子
    SafeQueue.processList.append(processor)
    pass


if __name__ == '__main__':
    runProcessor()
    pass