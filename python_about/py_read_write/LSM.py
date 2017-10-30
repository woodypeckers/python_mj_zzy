#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
make_text_file.py和read_text_file.py中os.path.exists和异常处理2种方法，后者更强大"""
import os  #"create text file"
ls = os.linesep #字符串给出当前平台的行终止符，Windows使用'\r\n'，Linux使用'\n'而Mac使用'\r'
# fname = raw_input("Enter file name:")
while True:
    fname = raw_input("Enter file name:")
    try:
        fobj = open(fname,'r')
    except IOError,e:
        all = []
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
        exit()
    else:
        print "ERROR:%s already exists" %  fname




