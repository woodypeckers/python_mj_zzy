#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author : mj

import string
##--------------------1.类继承
# class A(object):
#     def show(self):
#         print "base show"
#
#
# class B(A):
#     def show(self):
#         print "derivd show"
#
# obj = B()
# obj.show()
# #__class__方法指向了类对象
# # obj.__class__ = A
# # obj.show()


# #--------------------2.方法对象
# class A(object):
#     def __init__(self,a,b):
#         self.__a = a
#         self.__b = b
#
#     def myprint(self):
#         print 'a=%s, a=%s' % (self.__a,self.__b)
#
#     def __call__(self,num):#__call__方法能让对象的实例直接被调a1()
#         print 'call:',num +self.__a
# a1=A(10,20)
# a1.myprint()
# a1(80)


# #--------------------3.new和init
# class B(object):
#     def fn(self):
#         print 'B fn'
#
#     def __init__(self):
#         print 'B init'
#
#
# class A(object):
#     def fn(self):
#         print 'A fn'
#
#     def __new__(cls, a):
#         print 'NEW',a
#         if a >10:
#             return super(A, cls).__new__(cls)
#         return B()
#     def __init__(self,a):
#         print 'INIT',a
#
# aa=A(5)
# aa.fn()
# a2=A(20)
# a2.fn()
##--------------------list和dict生成
# ls =  [1,2,3,4]
# list1 =[i for i in ls if i>2] #第一种写法
##--第二种写法
# list1 =[]
# for i in ls:
#     if i>2:
#         i=i*2
#         list1.append(i)
# print list1

# list2 = [i*2 for i in ls if i>2]
# print list2
#
# dict1= {x:x**2 for x in (2,4,6)}
# print dict1
#
# dict2 = {x:'item'+str(x**2) for x in (2,4,6)}
# print dict2
#
# set1= {x for x in 'hello world'if x not in 'low '}
# print set1
#
# ##--------------------全局变量(global)和局部变量
# num = 9
# def f1():
#     global num
#     num = 20
#
# def f2():
#     print num
#
# f2()
# f1()
# f2()
#变量值互换
# a,b=7,8
# (a,b)=(b,a)

##--------------------默认方法
# class A(object):
#     def __init__(self,a,b):
#         self.a1=a
#         self.b1=b
#     print 'init'

    # """
    # # def mydefault(self):
    # #     print 'default'
    # #
    # # def __getattr__(self, item):##方法__getattr__只有当没有定义的方法调用时，才调用他
    # #     return self.mydefault
    # a1=A(10,20)
    # a1.fn1()
    # a1.fn2()
    # a1.fn3()
    # """
    # def mydefault(self,*args):
    #     print 'default：'+ str(args[0])
    #
    # def __getattr__(self,name):
    #     print "other,fn:",name
    #     return self.mydefault()

# a1=A(10,20)
# a1.fn1(33)
# a1.fn2('hello')
# a1.fn3(10)

##--------------------包管理
##--------------------闭包
# def mulby(num):
#     def gn(val):
#         return num *val
#     return gn
# zw=mulby(7)
# print(zw(9))

#性能
# def strest1(num):
#     str = 'first'
#     for i in range(num):
#         str+='x'
#     return str
#     print str
# strest1(10)
#
# print '=='*50
# def foo():
#     print 'foo'
# foo = lambda x:x+1
# foo(1)
# def testfun():
#     temp = [lambda x:i*x for i in range(4)]
#     return temp

# for everylamda in testfun():
#     print(everylamda(2))
# temp = [lambda x:i*x for i in range(4)]
# temp=[]
# for x in range(4):
#     temp.append(x)
# print(temp)

# def testfun1():
#     temp1=[lambda x,i=i:i*x for i in range(4)]
#     return temp1
# for everylamda in testfun1():
#     print(everylamda(2))

temp1=[lambda x,i=i:i*x for i in range(4)]
print temp1
temp = [lambda x:i*x for i in range(4)]
n = temp1
nb = temp
# print type(temp)
# print temp
print n
print([lambda x:i*x for i in range(4)])
print    nb