#!/usr/bin/env python
# -*- coding: utf-8 -*-

guess = 2
while True:
    num = int(raw_input("please input an integer between 1 and 30:"))
    if num >30 or num <0:
        print"xiaotaoqi，you must input integer between 1 and 30"
        continue

    if num == guess:
        print "binggo，ok, you just guess it ,exit"
        break
    else:
        print "you are wrong, jixu"
        continue

