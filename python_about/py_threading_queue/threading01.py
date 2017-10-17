#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep,ctime
import threading

loop_list = [4,2]
def loop(nloop,nsec):
    print 'start loop',nloop,'at:',ctime()
    sleep(nsec)
    print 'loop',nloop,'DNOE at:',ctime()

def main01():
    print 'starting at:',ctime()
    threads = []
    nl = range(len(loop_list))

    for i in nl:
        t = threading.Thread(target=loop, args=(i, loop_list[i]))#Tread类
        threads.append(t)

    for i in nl:
        threads[i].start()# start threads 启动线程

    for i in nl: #wait for all
        threads[i].join()#threads to finish

    print 'all DONE at:',ctime()

if __name__ == '__main__':
    main01()