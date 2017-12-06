# !/usr/bin/env python
# -*- coding:utf-8 -*-
import time
class CommonUtil(object):
    #判断是否是纯数字
    @staticmethod
    def isNumber(num):
        try:
            int(num)
            return True
        except ValueError:
            return False



