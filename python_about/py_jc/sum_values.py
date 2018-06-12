#!/usr/bin/env python
# -*- coding: utf-8 -*-

def sum(value):
    result = 0
    for i in range(1, value+1):
        result += i
        # result = result + i
    return result

def sum_reduce(x,y):
    return x+y

print reduce(sum_reduce,range(1,101))



if __name__ == '__main__':
    print sum(100)
    sum_reduce