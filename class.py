#!/usr/bin/env python()
# -*- coding: utf-8 -*-


# class student(object):
#     """无访问限制，"""
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def detail(self):
#         print "student name is %s ,\n age is %s " % (self.name,self.age)
#
#
# mj = student("mj",12)
# mj.age = 20
# mj.detail()


class stu(object):
    """访问限制，只能内部修改"""
    def __init__(self, name, age):
        self.__name = name
        self.__age  = age

    def s_xu(self):
        print "my name is %s ,age is %s :" % (self.__name, self.__age)

    def get_name(self):
        return self.__name

    def get_age(self):
        return self.__age

    def set_age(self, age):
        self.__age = age

mj = stu("mj",12)
mj.set_age(33)
print mj.get_name(), mj.get_age()
