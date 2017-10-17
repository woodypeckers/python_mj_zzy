#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：mj
import time
import threading

def music():
    for i in range(10):
        print u'正在听音乐 %s' % time.ctime()
        time.sleep(1)

def movie():
    for i in range(10):
        print u'正在看电影 %s' % time.ctime()
        time.sleep(1)

def main():
    threads = []
    t1 = threading.Thread(target=music, args=())
    threads.append(t1)
    t2 = threading.Thread(target=movie)
    threads.append(t2)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
print "All done"

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print u"一共执行了: %s 秒" % (end-start)