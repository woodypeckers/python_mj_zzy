#!/usr/bin/env python
# author : mj
# -*- coding: utf-8 -*-
# Created by iFantastic on 2018/6/12


# def num():
#     return [lambda x:x*i for i in range(4)]
# print [m(2) for m in num()]

print map(str,[1,2,3])
print map(list,['1','2','3'])
a = ['1', '2', '3']
b = [int(i) for i in a]
print b


# dict.fromkeys(seq,[,value]),把[,value]当做一个值，添加到每个seq键中
v1 = dict.fromkeys(['k1','k2'],[])
print v1
v1['k1'].append(666)
print(v1)
v1['k1'] = 777
print(v1)


v2 = dict.fromkeys(['k1','k2'],[])
print v2
v2['k2'].append(666)
print(v2)
v2['k2'].append(777)
print(v2)


v3 = dict.fromkeys(['k1','k2'],['a','b'])
print v3
v3['k2'].append(666)
print(v3)
v3['k2'].append(777)
print(v3)