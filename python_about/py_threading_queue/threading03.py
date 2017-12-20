#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep,ctime
import threading
from mythread_sample import mythread

loop_list = [4,2]
class MyThread(object):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__()
        self.name = name
        self.func = func
        self.name = name
        self.args = args

    def run(self):
        apply(self.func, self.args)

def loop(self, nloop, nsec):
    print 'start loop', nloop, 'at:', ctime()
    sleep(nsec)
    print 'loop', nloop, 'DONE at:', ctime()

def main03():
    print 'starting at:', ctime()
    threads = []
    nls = range(len(loop_list))

    for i in nls:
        t = mythread(loop, (i, loop_list[i]), loop.__name__)
        threads.append(t)

    for i in nls:
        threads[i].start()

    for i in nls:
        threads[i].join()

    print 'all DONE at:',ctime()

if __name__ == '__main__':
    main03()