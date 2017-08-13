#!/usr/bin/env python
# -*- coding: utf-8 -*-
import  string


# range()和len()一起用于字符串索引
foo = 'abc'
for i in range(len(foo)):
    print foo[i],'(%d)' % i

# 列表解析
squared = [x ** 2 for x  in range(6)]
for i in squared:
    print i

# 列表解析条件符合的值 偶数
squared_o = [x ** 2 for x in range(6) if not x%2]
for i in squared_o:
    print i

# # 文件访问 ?需要解决乱码问题
# filename = raw_input('enter file name :')
# fobj = open(filename,'r',)
# for eachline in fobj:
#     print eachline
# fobj.close()

d = []
for i in range(1,5):
    for j in range(1,5):
        for k in range(1,5):
            if (i != k != j):
                d.append([j,i,k])
                print j,k,j
print "总数：" ,len(d)
print d


# try :
#     filename = raw_input('enter file name:')
#     fobj = open(filename , 'r')
#     for eachline in fobj:
# except IOError, e:
#     print "file open error:",e
a  =0
while a<11:
    print a
    a+=1



 i = 2
while(i < 100):
   j = 2
   while(j <= (i/j)):
      if not(i%j): break
      j = j + 1
   if (j > i/j) : print i, " 是素数"
   i = i + 1

print "Good bye!"
    
