#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random,string


def guess_num():
    num = random.randint(40,45)
    while True:
        user_name = raw_input("请输入40到45之间的正整数：")
        if string.upper(user_name) in ("Q","QUIT"):
            break

        if num == int(user_name):
            print "对了，结束"
            break
        else:
            print "错了，继续"


if __name__ == "__main__":
    guess_num()
