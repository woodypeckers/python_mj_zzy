#!/usr/bin/env python
# author : mj
# -*- coding: utf-8 -*-
# Created by iFantastic on 2018/7/7
import unittest
from ddt import ddt, data, unpack


# @ddt
# class Mytestcase(unittest.TestCase):
#
#     @data(1,2,3)
#
#     def test_semothing(self,values):
#         self.assertEqual(values,2)

@ddt
class Mytestcase(unittest.TestCase):

    @data((1, 2),(2, 3))
    @unpack

    def test_semothing(self,values1,values2):
        print(values1, values2)
        self.assertEqual(values2, values1 + 1)



import  xlrd
data1 = xlrd.open_workbook('test.xlsx')
# table = data1.sheet_by_index(0)#通过索引顺序获取
# table = data1.sheets()[0] #通过索引顺序获取
table = data1.sheet_by_name('Sheet1')#通过名称来获取

nrows=table.nrows # 获取总行数
ncols=table.ncols # 获取总列数

print (table.row_values(0))#打印第一行
print (table.col_values(0))#打印第一列

if __name__ == '__main__':
    unittest.main()