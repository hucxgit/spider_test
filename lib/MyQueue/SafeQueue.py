#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import multiprocessing
preCrawlQueue = multiprocessing.Queue(maxsize=200000)
donwCrawlQueue = multiprocessing.Queue(maxsize=1000)
#把调度器 抓取器 处理器 放入
processList = []