#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author : mj

# def function(a, b):
#     print a, b
#
# apply(function, ("whither", "canada?"))
# apply(function, (1, 2 + 3))
import os  #"create text file"
ls = os.linesep #字符串给出当前平台的行终止符，Windows使用'\r\n'，Linux使用'\n'而Mac使用'\r'
# fname = raw_input("Enter file name:")
# while True:
#     fname = raw_input("Enter file name:")
#     if os.path.exists(fname):  #判断文件名是否在此路径，当输入不存在的文件，返回false，中断
#         print "ERROR:%s already exists" %  fname
#         """第一次执行之后生成text.txt ,（不删除text.txt）之后是个死循环, 解决死循环--把第5行，
#         放到while中（但是引发25行中写法不规范，但不影响运行），作用域引起的"""
#     else:
#         break
all = []
try:
    fname = raw_input("Enter file name:")
except IOError,e:
     print "ERROR:%s already exists" % e
else:
    print "\nEnter lines ('.'by itself to quit).\n"#一直输入， 每一行以“.”结束
	
    while True:  #循环到终止输入
        entry = raw_input('writing:')
        if entry == '.':
            break
        else:
            all.append(entry)

fobj = open(fname, 'w')
fobj.writelines(["%s%s" % (x, ls) for x in all])  #列表解析
fobj.close()
print "DONE"