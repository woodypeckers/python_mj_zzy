#!/usr/bin/env python
# -*- coding: utf-8 -*-


class DictTest(object):

    def dict1(self):
        dictmj = {"name": 'mj', "age": 18, "adr": 'sz'}
        self.dictmj =dictmj
        for i in dictmj:
            print "**第一种** the key is %s, the values is %s" % (i, dictmj[i])

    def dict2a(self):
        dict2 =self.dictmj
        for key in dict2.keys():
            print "**第二种** key : %s, values : %s " % (key ,dict2[key])

    def dict3a(self):
        dict3 = dict([['x','a'],['t','b'],['s','c']])
        print dict3
        print dict([('xyts'[i-1], i) for i in range(1, 5)])
    @staticmethod
    def dict4a(self):
        dict4 = dict(m=1, n=2)
        dict5 =dict(**dict4)
        dict6 = dict4.copy()
        print dict4,dict5,dict6,  len(dict4)
if __name__ == '__main__':
