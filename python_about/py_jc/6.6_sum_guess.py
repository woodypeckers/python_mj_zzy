#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author : mj
def sum_num(values):
    result = 0
    for i in range(1,values+1):
        result+=i
    return result

import random
def guess_num():
    num = random.randint(40,43)
    while True:
        user_num =input("pleas input integer between 40 and 43:")
        if str.upper(user_num) in ('q','quit'):#在python2中，只能用string, python3中str
            break

        if num == int(user_num):
            print("year,you are right")
            break

        else:
            print("you are wrong,pleas input integer between 40 and 43")


def multiplication_table_py2():
    """py2写法"""
    for i in range(1,10):
        for j in range(1,i+1):
            print('{}x{}={}\t'.format(i,j,i*j) ),# end在python2.x报错 括号后面加个逗号
        print

def multiplication_table_py3():
    """py3写法"""
    for i in range(1,10):
        for j in range(1,i+1):
            print('{}x{}={}\t'.format(i,j,i*j), end='')# end在python2.x报错
        print()
"""乘法表"""
print('\n'.join([' '.join(['%s*%s=%-2s' % (y,x,x*y) for y in range(1,x+1)]) for x in range(1,10)]))#-2s补位符
print('\n'.join([' '.join(['%s*%s=%-10s' % (y,x,x*y) for y in range(1,x+1)]) for x in range(1,10)]))
print('\n'.join([' '.join(['%s*%s=%s' % (y,x,x*y) for y in range(1,x+1)]) for x in range(1,10)]))

if __name__ == '__main__':
    print(sum_num(input("pleas input  a number :")))
    guess_num()
    multiplication_table_py2()
    multiplication_table_py3()