#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author : mj

"""__new__和__init__的区别"""


class Person(object):
    """__new__和__init__的区别"""

    def __new__(cls, *args, **kwargs):
        print("in __new__")
        instance = object.__new__(cls)  # python2中object.__new__(cls, *args, **kwargs)
        return instance

    def __init__(self, name, age):
        print("in __init__")
        self._name = name
        self._age = age


""" # python2中object.__new__(cls, *args, **kwargs)在python3中object.__new__(cls)"""
class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(
                cls
            )  # python2中object.__new__(cls, *args, **kwargs)

        return cls._instance



if __name__ == '__main__':
    Person("Wang", 33)

    s1 = Singleton()
    s2 = Singleton()
    print(s1)
    print(s2)
