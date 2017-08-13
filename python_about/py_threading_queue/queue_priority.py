#!/usr/bin/python
# encoding:utf-8
# autor:mj
"""优先级列队PriorityQueue()
q.task_done()，每次从queue中get一个数据之后，当处理好相关问题，最后调用该方法，以提示q.join()是否停止阻塞，让线程向前执行或者退出；
join()与setDaemon()的区别，作用相反
join ()方法：主线程A中，创建了子线程B，并且在主线程A中调用了B.join()，
那么，主线程A会在调用的地方等待，直到子线程B完成操作后，才可以接着往下执行，那么在调用这个线程时可以使用被调用线程的join方法。
setDaemon()方法。主线程A中，创建了子线程B，并且在主线程A中调用了B.setDaemon(),
这个的意思是，把主线程A设置为守护线程，这时候，要是主线程A执行结束了，就不管子线程B是否完成,一并和主线程A退出.
http://blog.csdn.net/zhangzheng0413/article/details/41728869/
http://www.cnblogs.com/itogo/p/5635629.html
"""
import Queue
import threading

class Job(object):
    def __init__(self, priority, description):#priority优先，description描述
        self.priority = priority
        self.description = description
        print 'Priority Job:',description
        return
    """__cmp__不需要比较？    与下面代码好像无关，注释不影响，作用是？
    http://www.cnblogs.com/superxuezhazha/p/5792099.html"""
    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

q = Queue.PriorityQueue()

q.put(Job(3, 'level 3 job'))
q.put(Job(10, 'level 10 job'))
q.put(Job(1, 'level 1 job'))

def process_job(q):
    while True:
        next_job = q.get()
        print 'for:', next_job.description
        q.task_done()  #调用完成
"""???这里2个进程，先启动的是主线程，如何判断谁先启动"""
workers = [threading.Thread(target=process_job, args=(q,)),
        threading.Thread(target=process_job, args=(q,))
        ]

for w in workers:
    w.setDaemon(True)  #主线程完成，就 退出
    w.start()

q.join()