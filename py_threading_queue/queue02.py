#!/usr/bin/env python
# -*- coding: utf-8 -*-
# autor:mj
import Queue

# FIFO即First in First Out,先进先出
q = Queue.Queue(maxsize=0)
for i in range(6):
    q.put(i)  #放

while not q.empty():
    print q.get() #取
    # while not q.empty():
    #     print q.get() #取


#LIFO即Last in First Out,后进先出
# Q = Queue.LifoQueue()
# for i in range(5):
#     Q.put(i)
#
#     while not Q.empty():
#         print Q.get()

