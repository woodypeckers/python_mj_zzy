#!/usr/bin/env python
# -*- coding: utf-8 -*-

a = frozenset(["foo","bar"])
print a

f = open("numbers.txt",'w')
for i in range(5):
    f.write("%d,"%i)
f.close()

f = open("numbers.txt",'r')
print set(f)

f.close()
#----------------------------------------
"""输入3次密码"""
valid = False
count =3
mimalist= ["ab",'bb','cc']
while count>0:
    input = raw_input("Enter  passwd:")
    for mima in mimalist:
        if input == mima:
            valid= True
            print "ok"
            break
    if not valid:
        print "invalid input"
        count -=1
        continue
    else:
        break
