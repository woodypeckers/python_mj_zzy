#!/usr/bin/env python
# author : mj
# -*- coding: utf-8 -*-
# Created by iFantastic on 2018/6/11

#python最大递归层数
#可以设置最大递归层数，超大会导致崩溃
def foo(n):
    print(n)
    n += 1
    foo(n)


if __name__ == '__main__':
    foo(1)

#运算符
v1 = 1 or 3
v2 = 1 and 3
v3 = 0 and 2 and 1
v4 = 0 and 2 or 1
v5 = 0 and 2 or 1 or 4
# v6 = 0 or Flase and 1
print v1,v2,v3,v4,v5


#xreadlines和readlines的区别
#返回类型不同，功能相同，readlines返回list，xreadlines返回迭代器
f= open('C:/Users/zhangzhanyong/Desktop/learn/test.txt','rb')
print f.xreadlines()
print f.readlines()

for line in f.readlines():
    print 'readlines',line,
print type(line)

f= open('C:/Users/zhangzhanyong/Desktop/learn/test.txt','rb')
for linex in f.xreadlines():
    print 'xreadlines',linex,
print type(linex)
f.close()

#items()遍历key
dict = {'Name': 'Runoob', 'Age': 7}
for i,j in dict.items():
    print(i, ':\t', j)

