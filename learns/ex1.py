#!/usr/bin/env python
# -*- coding: utf-8 -*-

def user():
    user = raw_input("Enter in :")
    print "user enter in :" ,user
    print type(user)

def user_int():
    user_int = int(raw_input("please input1:"))
    print user_int,"#被转换为int"
    print type(user_int)

def for_01():
    # h_name = "hello,xiaojia"
    h_name = (raw_input("please input2:"))
    for i in h_name:
        print i

def while_01():
    count = 0
    while count<10:
        count += count +1
        print count

def range_01():
    a =range(1,20,2)
    print a

def if_else():
    num = int(raw_input("please input number:"))
    if num == 0:
        print "this is num :", num
    elif num > 0:
        print num, "is positive integer（正整数）"
    else:
        print num, "is negative number（负数）"


if __name__ == "__main__":
    user()
    user_int()
    for_01()
    range_01()
    if_else()


