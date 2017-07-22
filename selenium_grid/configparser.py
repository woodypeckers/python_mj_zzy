#!/usr/bin/env python
# encoding:utf-8
# author:mj
"""基本的读取配置文件
     -read(filename) 直接读取ini文件内容
     -sections() 得到所有的section，并以列表的形式返回
     -options(section) 得到该section的所有option
     -items(section) 得到该section的所有键值对
     -get(section,option) 得到section中option的值，返回为string类型
     -getint(section,option) 得到section中option的值，返回为int类型，还有相应的getboolean()和getfloat() 函数。"""
import sys,os,string
import ConfigParser
cf = ConfigParser.ConfigParser()
cf.read("test.conf")

secs = cf.sections()#返回所有的部件 #sections()
print "secs:", secs

opts = cf.options("db")#选择
print "opts all values:", opts

key_valuses = cf.items('db')#返回可遍历的(键, 值) 元组数组。
print "key_vulues  :", key_valuses

#取出db 的值
db_host = cf.get("db", "db_host")
db_port = cf.getint("db", "db_port")#getint()强制转化
db_user = cf.get("db", "db_user")
db_pass = cf.get("db", "db_pass")
#取出concurrent 的值
processors = cf.getint("concurrent", "processor")
threads = cf.getint("concurrent", "thread")
print "db_host:", db_host
print "db_port:", db_port
print "db_user:", db_user
print "db_pass:", db_pass
print "processor:", processors
print "thread:", threads

#修改一个值并写入文件
cf.set("db", "db_pass", "xml")
cf.set("db", "db_user", "mj")
cf.write(open("test.conf", "w"))
print "db_pass修改后的值：", db_pass
print "db_user修改后的值：", db_user

