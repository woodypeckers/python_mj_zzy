#!/usr/bin/env python
# -*- coding: utf-8 -*-

def sum(value):
    result = 0
    for i in range(1, value+1):
        result += i
        # result = result + i
    return result
    

if __name__ == '__main__':
    print sum(100)