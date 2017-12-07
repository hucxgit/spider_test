#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# a_string = "This is a global variable"
# def foo():
#    b = 0
#    a_string = "tmp"
#    print locals()
# print globals() # doctest: +ELLIPSIS


#定义装饰器
def decorate(name):
    def wrapper(func):
        def sub_wrapper(*args,**kwargs):
            print(type(args))
            print(args)
            print(type(kwargs))
            print(kwargs)
            print(name)
            func(*args,**kwargs)
        return sub_wrapper
    return wrapper


@decorate(name="python")
def text1():
    print("text1")
@decorate(name="python")
def text2(a,b):
    print("text1")
@decorate(name={'w':'w'})
def text3(*args,**kwargs):
    print("text1")

if __name__ == '__main__':
    #text3(1,2,3,4,a=1,b=2,c=3)
    # import lib.MyQueue.SafeQueue as SafeQueue
    # for i in range(5):
    #     print(SafeQueue.preCrawlQueue)
    # pass

    #from lib.Utils import HttpUtil
    #HttpUtil.httpRequestAnjuke("beijing","1001159")

    #测试
    import multiprocessing
    a = multiprocessing.Queue(maxsize=2)
    a.put("1")
    a.put("2")
    print(a.qsize())
    print(a.full())



