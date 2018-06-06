# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author : mj


"""迷宫"""
print(''.join(__import__('random').choice('\u2571\u2572') for i in range(50*24)))
print(''.join(__import__('random').choice('/\\') for i in range(50*24)))

"""桃心"""
print('\n'.join([''.join([('AndyLove'[(x-y)%8]if((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3<=0 else' ')for x in range(-30,30)])for y in range(15,-15,-1)]))

"""乘法表"""
print('\n'.join([' '.join(['%s*%s=%-2s' % (y,x,x*y) for y in range(1,x+1)]) for x in range(1,10)]))#-2s补位符
print('\n'.join([' '.join(['%s*%s=%-10s' % (y,x,x*y) for y in range(1,x+1)]) for x in range(1,10)]))
print('\n'.join([' '.join(['%s*%s=%s' % (y,x,x*y) for y in range(1,x+1)]) for x in range(1,10)]))

print('\n'.join([''.join(['*'if abs((lambda a:lambda z,c,n:a(a,z,c,n))(lambda s,z,c,n:z if n==0else s(s,z*z+c,c,n-1))(0,0.02*x+0.05j*y,40))<2 else' 'for x in range(-80,20)])for y in range(-20,20)]))


def generate_square(n):
    i = 0
    while i < n:
        yield i * i
        i += 1

result = generate_square(10)
print(list(result))

def generate_square1(n):
    i = 0
    result = []
    while i < n:
        result.append(i * i)
        i += 1
    return result

result = generate_square1(10)
print(result)

"""容器（container）
像列表（list）、集合（set）、序列（tuple）、字典（dict）都是容器
容器是一种把多个元素组织在一起的数据结构，可以逐个迭代获取其中的元素"""

"""迭代器（iterator）
实现了__iter__和__next__方法的对象都称为迭代器
"""
a = ['a', 'b', 'c']
it = a.__iter__()
print(next(it))
print(next(it))
print(next(it))
# print(next(it))


""" 斐波那契数列-------------------------------------------------------------------"""
class Fib:
    def __init__(self):
        self.prev = 0
        self.curr = 1

    def __iter__(self):
        return self

    def __next__(self):
        self.curr, self.prev = self.prev + self.curr, self.curr
        return self.curr

fib = Fib()
for i in range(10):
    print(next(fib))


def fib1():
    prev, curr = 0, 1
    while True:
        yield curr
        curr, prev = prev + curr, curr

f = fib1()
for i in range(10):
    print(next(f))



def echo(n):
    while True:
        n = yield n

g = echo(1)
print(next(g))
print(next(g))



"""列表去重-------------------------------------------------------------------"""
#set关键字
list1 = [1, 2, 3, 4, 3, 4, 5, 6]
a=set(list1)
# 2.使用字典函数，
b = {}
b = b.fromkeys(a)
c = list(b.keys())
print("a:",a)
print("b:",b)
print(b.keys())
print("c:",c)

