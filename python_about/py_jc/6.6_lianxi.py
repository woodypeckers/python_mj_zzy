#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author : mj

"""py2和py3的写入文件"，py3中需要加入encode,在打开文件后，必须加b （即wb）"""
f3 = open("c:\\py3.txt", "wb")
s3="py3中，历史，12345"
b = s3.encode("gbk")
f3.write(b)
c=bytearray( "王五","gbk")
f3.write( c )
f3.close()

# f2 = open("c:\\py2.txt", "wb")
# s2 = "p2中，张三李四abcd1234,"
# f2.write(s2)
# c=bytearray( "王五")
# f2.write(c)
# f2.close()

def sum_n(values):
    reslut=0
    for i in range(1,values+1):
        reslut+=i
    return reslut

import random,string
def guess_n():
    n=random.randint(40,43)
    while True:
        u_n=input("enter in num between 40 and 43")
        if n ==int(u_n):
            print("ok")
            break

        elif str.upper(u_n)in("q","qiut"):
            print("game over")
            break
        else:
            print("jixu")

def multiplication_p3():
    for i in range(1,10):
        for j in range(1,i+1):
            print("{}x{}={}\t".format(i,j,i*j),end='')
        print()
		
"""乘法表"""
print('\n'.join([' '.join(['%s*%s=%-2s' % (y,x,x*y) for y in range(1,x+1)]) for x in range(1,10)]))#-2s补位符
print('\n'.join([' '.join(['%s*%s=%-10s' % (y,x,x*y) for y in range(1,x+1)]) for x in range(1,10)]))
print('\n'.join([' '.join(['%s*%s=%s' % (y,x,x*y) for y in range(1,x+1)]) for x in range(1,10)]))

if __name__ == '__main__':
    print(sum_n(100))
    guess_n()
    multiplication_p3()
