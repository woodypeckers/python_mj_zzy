#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os  #"create text file"
ls = os.linesep
fname = raw_input("Enter file name:")
while True:
    if os.path.exists(fname):  #判断是否在此路径，当输入不存在的文件，返回false，中断
        print "ERROR:%s already exists" %  fname

        """第一次执行之后，生成text.txt ,（不删除text.txt）之后是个死循环, 待解决？？？"""
    else:
        break

all = []
print "\nEnter lines ('.'by itself to quit).\n"#一直输入， 每一行以“.”结束

while True:  #循环到终止输入
    entry = raw_input('> ')
    if entry == '.':
        break
    else:
        all.append(entry)


fobj = open(fname, 'w')
fobj.writelines(["%s%s" % (x, ls) for x in all])  #列表解析
fobj.close()
print "DONE"
