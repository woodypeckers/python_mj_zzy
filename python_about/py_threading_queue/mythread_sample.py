#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：mj
"""Python多线程编程中常用方法：

1、join()方法：如果一个线程或者在函数执行的过程中调用另一个线程，并且希望待其完成操作后才能执行，那么在调用线程的时就可以使用被调线程的join方法join([timeout]) timeout：可选参数，线程运行的最长时间

2、isAlive()方法：查看线程是否还在运行

3、getName()方法：获得线程名

4、setDaemon()方法：主线程退出时，需要子线程随主线程退出，则设置子线程的setDaemon()"""

import threading
import time
class mythread(threading.Thread):
    def __init__(self,threadname):
        threading.Thread.__init__(self,name=threadname)
    def run(self):
        global x
        lock.acquire()#获得锁
        for i in range(3):
            x = x+1
        time.sleep(1)
        print x
        lock.release()#释放锁

if __name__ == '__main__':
    lock = threading.RLock()
    t1 = []
    for i in range(10):
        t = mythread(str(i))
        t1.append(t)
    x = 0
    for i in t1:
        i.start()