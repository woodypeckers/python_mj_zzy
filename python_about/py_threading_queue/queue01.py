#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint
from Queue import Queue
from time import sleep
from mythread_sample import mythread

def writeQ(queue):
    print 'producing#生产 object for Q...',queue.put('abcd',1)
    print 'size now',queue.qsize()

def readQ(queue):
    val = queue.get(1)
    print 'consumed#消耗 object for q ... size now ',queue.qsize()

def writer(queue,loops):
    for i in range(loops):
        writeQ(queue)
        sleep(randint(1,3))

def reader(queue,loops):
        for i in range(loops):
            readQ(queue)
            sleep(randint(2,5))

funcs = [writer,reader]
nfuncs = range(len(funcs))

def main():
    nloops = randint(2,5)
    q = Queue(32)

    threads = []
    for i in nfuncs:
        t = mythread(funcs[i],(q,nloops),funcs[i].__name__)
        threads[i].append(t)

    for i in nfuncs:
        threads[i].start()

    for i in nfuncs:
        threads[i].join()

    print "all DONE"

if __name__ == '__main__':
    main()



