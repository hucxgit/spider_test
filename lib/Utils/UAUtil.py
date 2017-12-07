# !/usr/bin/env python
# -*- coding:utf-8 -*-
import random
UA = []
class UAUtil:
    split="wkzf"
    def __init__(self,env=None):
        print("__init__ method")
        self.readFile()
        pass

    @staticmethod 
    def readFile():
        txtpath="lib/config/UA.conf"
        fp=open(txtpath)
        for lines in fp.readlines():
            lines=lines.replace("\n","").split("wkzf")
            if len(lines)>0:
                tmp = lines[0]
                UA.append(str(tmp))
        fp.close()
        #print("=================================")
        #print(UA)
    
    @staticmethod   
    def getUA():
        if len(UA)==0:
            #print("读取文件")
            UAUtil.readFile()
        index = random.randint(0,len(UA)-1)
        ua = UA[index]
        if "\r" in ua:
            ua = ua.replace("\r", "")
        return ua