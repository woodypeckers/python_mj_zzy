#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author : mj
import os,random
ls = os.linesep #字符串给出当前平台的行终止符，Windows使用'\r\n'，Linux使用'\n'而Mac使用'\r'
fname = raw_input("Enter file name:")
while True:
    if os.path.exists(fname):#文件名是否存在路径中‘exists存在’
        print "ERROR: '%s' already exists " % fname
    else:
        break

all = []
print "\nEnter lines ('.' by itself to quit).\n"

while True:
    entry = raw_input('> ')
    if entry == '.':
        break
    else:
        all.append(entry)

fobj = open(fname,'w')
fobj.writelines(['%s%s' % (x,ls) for x in all])
fobj.close()
print 'done!'
