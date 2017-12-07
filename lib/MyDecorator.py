#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import time
import Queue
#调度器装饰器
def SchedulerDecorator(name):
    def wrapper(func):
        def sub_wrapper(*args,**kwargs):
            print(name)
            preQueue = kwargs['preQueue']
            offset = args[0]
            num = args[1]
            while True:
                try:
                    if  preQueue._maxsize - preQueue.qsize < 600:
                        print(name + " 待抓取的队列有" + str(preQueue.qsize()) + "条数据  队列快满了 要等待30秒")
                        time.sleep(30)
                    objs = func(offset, num, **kwargs)
                    print(name + " 发网络请求去抓取数据 获取了" + str(len(objs)) + "条数据")
                    for obj in objs:
                        preQueue.put(obj, block=False)
                    print(name + " 待抓取的队列有" + str(preQueue.qsize()) + "条数据")
                    time.sleep(60)
                    if len(objs) <= 1:
                        time.sleep(60)
                    offset += num
                except Queue.Full as e:
                    print(name + " 待抓取队列满了  ")
                    print(e)
                except Exception as e:
                    print(name + " 从mysql读列表数据异常  ")
                    print(e)
                finally:
                    pass



        return sub_wrapper
    return wrapper

#抓取器器装饰器
def FetcherDecorator(name):
    def wrapper(func):
        def sub_wrapper(*args,**kwargs):
            print(name)
            downQueue = kwargs['downQueue']
            while True:
                try:
                    print(name + "  发网络请求去抓取数据")
                    crawlResultDic = func(*args,**kwargs)
                    if crawlResultDic is not None:
                        downQueue.put(crawlResultDic, block=False)
                    else:
                        print("网络获取返回结果为空")
                        pass
                    # time.sleep(0.1)
                except Queue.Full as e:
                    print(name + "  抓取结果对列满了 ")
                    print(e)
                    time.sleep(1)
                except Queue.Empty as e:
                    print(name + " 待抓取队列为空 从待抓取队列获取异常 ")
                    print(e)
                    time.sleep(1)
                finally:
                    pass
        return sub_wrapper
    return wrapper
#处理器装饰器皿
def ProcessorDecorator(name):
    def wrapper(func):
        def sub_wrapper(*args,**kwargs):
            #downQueue = kwargs['downQueue']
            #preToUpdate = kwargs['preToUpdate']
            while True:
                try:
                    func(*args, **kwargs)
                except Queue.Empty as e:
                    print(name + " 去取抓取结果 准备更新 抓取结果对列空了")
                    time.sleep(0.5)
                    print(e)
                except Exception as e:
                    print(name + " 执行sql导致了异常")
                    print(e)
                finally:
                    pass
        return sub_wrapper
    return wrapper