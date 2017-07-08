#!/usr/bin/env python()
# -*- coding: utf-8 -*-
# 我们首先创建一个学生类，这个类是所有学生的爸爸
# class Student(object):
#
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def detail(self):
#         print "A  student name is %s,age is %s" % (self.name,self.age)
#
# # 然后，我们创建一个小学生类，小学生特点是，LOL sala无敌
# class PrimaryStudent(Student):#因为是继承于学生类，所以我们写在括号内
#     # 这里我们可以不写构造函数，于是我们就是直接沿用Student类的构造函数
#     def lol(self): # 我们有一些新的独有的方法，会被叠加起来
#         print('正在打LOL！')
#
#
# class MiddleStundent(Student):
#
#     def under(self):
#         print "A  undergraduate name is" # %s,age is %s" % (self.name,self.age)
# # 接下来，我们创建一个大学生类，大学生特点是，额，每个人都有个妹子。。
# class CollegeStudent(Student):
#
#     def __init__(self, name, age, gf): #这里，我们改写一下构造函数
#         # 于是爸爸的__init__()会被直接overwrite
#         self.name = name
#         self.age = age
#         self.gf = gf
#
#     def gf_detail(self):
#         print"this is gf_detail %s" % self.gf
#
# # 来，我们来创建一下
# obj1 = PrimaryStudent('aaa', 22)
# obj1.lol() # 独有的方法
# obj1.detail()#继承与爸爸的方法
#
# obj2 = CollegeStudent('刘强东', 35, '奶茶妹妹')
# obj2.detail()
# obj2.gf_detail()

"""读取文件"""
def read_f():
    fname = raw_input("Enter file name:")
    try:
        fobj = open(fname, 'r')
    except IOError,e:
        print "***  file open error",e
    else:
        for ehcoline in fobj:
            print ehcoline
        fobj.close()

def read_file():
    f = open("data.txt","r")
    for i in f.readlines() :
        print i.split()
    f.close()

def write_file():
    # fname = raw_input("Enter file neirou:")
    # obj =open(fname, 'w')
    flist = [u"张三",u"历史",u"w问问"]
    fname = open("write_file.txt",'w')
    for i in flist:
        fname.write(i.encode("utf-8")+'\n')
    fname.close()

if __name__ =="__main__":
    # read_f()
    # read_file()
    write_file()