#!/usr/bin/env python()
# -*- coding: utf-8 -*-

class Student(object):

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def detail(self):
        print "A  student name is %s,age is %s" % (self.name, self.age)


class MiddleStundent(Student):
    def lol(self):
        print "A  MiddleStundent name is %s,age is %s" % (self.name,self.age)

class PrimaryStudent(Student):

    def __init__(self, name, age, playing):
        self.name = name
        self.age = age
        self.playing = playing

    def play(self):
        print "A primary student name is %s , age is %s ,playing is %s" % \
              (self.name, self.age, self.playing)


if __name__ == "__main__":

    obj2 = PrimaryStudent('小王', 16, "youxi")
    obj2.play()
    obj2.detail()

    obj1 = MiddleStundent('aaa', 22)
    obj1.lol()
    obj1.detail()
