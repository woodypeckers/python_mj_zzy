#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep,ctime
import thread

def loop0():
    print "start loop 0 at:",ctime()
    sleep(4)
    print "loop 0 done at:",ctime()

def loop1():
    print "start loop 1 at:",ctime()
    sleep(2)
    print "loop 1 done at:",ctime()

def main():
    print "Starting at:",ctime()
    # loop0()
    # loop1()
    """loop0,loop1为所以运行时间总和"""
    thread.start_new_thread(loop0, ())#创建一个线程，指定的参数，**kwargs可选
    thread.start_new_thread(loop1, ())
    """start_new_thread(),必须要有前2个参数，不带参数加空元祖,()
    --> loop1,loop0并发执行,运行时间为最长循环的运行时间和其他代码的时间总和"""
    sleep(6)#作用：让主线程停下来，等待所以子线程运行结束，再退出
    print "All done at:",ctime()

if __name__ == '__main__':
    main()
