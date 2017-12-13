#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from fetcher import Fetcher
from scheduler import Scheduler
from processor import Processor
import lib.MyQueue.SafeQueue as SafeQueue
import click



def main(cls):
    #开启调度器
    Scheduler.runScheduler(func=cls.runTask)
    #开启抓取器
    Fetcher.runFetcher(processNum=5,func=cls.runFetcher)
    #开启处理器
    Processor.runProcessor(func=cls.runProcessor)

    for p in SafeQueue.processList:
        p.start()
    for p in SafeQueue.processList:
        p.join()


@click.group()
@click.pass_context
def cli(ctx,**kwargs):
    print("可以存放共用变量")
    return ctx


@cli.command()
@click.pass_context
def anjuke(ctx,**kwargs):
    from bussiness import AnjukeBussiness
    main(AnjukeBussiness)
    pass

@cli.command()
@click.pass_context
def gaode(ctx,**kwargs):
    from bussiness import GaodeBussiness
    main(GaodeBussiness)
    pass

#dev
if __name__ == '__main__':
    #cli()
    from bussiness import AnjukeBussiness
    main(AnjukeBussiness)