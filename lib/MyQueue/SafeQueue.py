#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import multiprocessing
preCrawlQueue = multiprocessing.Queue(maxsize=200000)
donwCrawlQueue = multiprocessing.Queue(maxsize=1000)
processList = []