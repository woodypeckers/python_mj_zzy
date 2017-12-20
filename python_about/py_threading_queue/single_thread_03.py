#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author : mj
from time import sleep, ctime
import threading

def muisc(func):
    for i in range(2):
        print 'Start playing： %s! %s' %(func,ctime())
        sleep(2)

def move(func):
    for i in range(2):
        print 'Start playing： %s! %s' %(func,ctime())
        sleep(5)

def player(name):
    r = name.split('.')[1]
    if r == 'mp3':
        muisc(name)
    else:
        if r == 'mp4':
            move(name)
        else:
            print 'error: The format is not recognized!'

list = ['爱情买卖.mp3','阿凡达.mp4']

threads = []
files = range(len(list))

#创建线程
for i in files:
    t = threading.Thread(target=player,args=(list[i],))
    threads.append(t)

if __name__ == '__main__':
    #启动线程
    for i in files:
        threads[i].start()
    for i in files:
        threads[i].join()

    #主线程
    print 'end:%s' %ctime()