#!/usr/bin/env python
# -*- coding: utf-8 -*-


def test_while():
    count = 0

    while (count < 9):
        print "当前数字是: %s" % (count)
        count = count + 1
        print "good bye"

def test_for():
    name = "liu nian cong mang"
    for i in name:
        if i == " ":
            break
        print i

if __name__ == '__main__':
    test_while()
    test_dict()
    test_for()

