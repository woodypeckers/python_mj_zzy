#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep,ctime
import threading
from threading import Thread

loop_list = [4,2]
class ThreadFunc(object):
    def __init__(self, func, args, name=''):
        self.name = name
        self.func = func
        self.name = name

    def __call__(self):
        apply(self.func, self.args)

def loop( nloop, nsec):
    print 'start loop', nloop, 'at:', ctime()
    sleep(nsec)
    print 'loop', nloop, 'DONE at:', ctime()

def main02():
    print 'starting at:', ctime()
    threads = []
    nls = range(len(loop_list))

    for i in nls:
        t = threading.Thread(
                target=ThreadFunc(loop, (i, loop_list[i]),
                                  loop.__name__))
        threads.append(t)

    for i in nls:
        threads[i].start()

    for i in nls:
        threads[i].join()

    print 'all DONE at:',ctime()

if __name__ == '__main__':
    main02()