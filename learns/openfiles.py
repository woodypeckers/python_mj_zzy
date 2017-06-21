#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 小文件读取
def read_file():
    h = open("data.txt","r")
    for i in h.readlines():
        print i

# 大文件读取
def with_open():
    with open("data.txt","r") as f:
        while True:
            data = f.read(2048)
            if not data: break
            print data

if __name__ == "__main__":
    # read_file()
    with_open()