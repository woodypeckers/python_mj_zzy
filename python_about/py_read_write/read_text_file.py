#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author : mj
import os  #"create text file"
ls = os.linesep #字符串给出当前平台的行终止符，Windows使用'\r\n'，Linux使用'\n'而Mac使用'\r'
fname =raw_input('Enter filename:')
print#打印空行

try:
    fobj=open(fname,'r')
except IOError,e:
    print "file open error:",e
else:
    for Eachline in fobj:
        print Eachline, # 文件读取时print后面的‘,’去除空行
    fobj.close()