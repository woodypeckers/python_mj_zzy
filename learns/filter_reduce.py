#!/usr/bin/env python
# encoding:utf-8

"""
filter,reduce 的例子
"""
list1 = [1, 2, 3, 4, 5, 6]
list2 = reduce(lambda x, y: x+y, list1)
print list1, list2
#filter 相当于列表推导,list comprehension
#filter(fun,iterable)