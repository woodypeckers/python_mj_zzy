#!/usr/bin/env python
# encoding:utf-8
# author:mj

import ConfigParser
import os,string,sys
config = ConfigParser.ConfigParser()
config.read("IP_config.ini")
print "config is null:",config
#添加部件 section
# config.add_section("HOME")
# config.set("HOME", "IP", "127.0.0.1")
# config.set("HOME", "Mask", "255.255.255.0")
# config.set("HOME", "Gateway", "192.168.1.1")
# config.set("HOME", "DNS", "0.0.0.1")
# config.write(open("IP_config.ini", "w"))
try:
    config.set("HOME", "IP", "127.0.0.1")
    config.set("HOME", "Mask", "255.255.255.0")
    config.set("HOME", "Gateway", "192.168.1.1")
    config.set("HOME", "DNS", "0.0.0.1")
    config.write(open("IP_config.ini", "w"))
except ConfigParser.DuplicateSectionError:#重复节点错误
    print("Section 'HOME' already exists")

try:
    config .add_section("Woody")
    config.set("Woody", "IP", "192.168..2.11")
    config.set("Woody", "Mask", "255.255.255.0")
    config.set("Woody", "Gateway", "192.168.2.1")
    config.set("Woody", "DNS", None)
except ConfigParser.DuplicateSectionError:#重复节点错误
    print("Section 'Woody' already exists")

config.write(open("IpConfig.ini", "w"))
ip = config.get("HOME", "IP")
mask = config.get("HOME", "mask")
gateway = config.get("HOME", "Gateway")
dns = config.get("HOME", "DNS")
print(ip,mask,gateway,dns)