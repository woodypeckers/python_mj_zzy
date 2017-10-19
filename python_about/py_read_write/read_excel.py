#!/usr/bin/env python
# -*- coding: utf-8 -*-

# __author__ = 'sss'
import xlrd,os
def read_excel():
    data = xlrd.open_workbook('user_data.xlsx')
    #查看文件中所有的sheet名称
    print data.sheets()[0]

    #得到一个工作表，或者通过索引顺序 或sheets表名称
    table1= data.sheets()[0]
    #table1 = data.sheets_by_index(0) #索引
    #table1 = data.sheets_by_name('account') #sheets名称
    print table1

    #获取行数和列数
    nrows = table1.nrows
    ncols = table1.ncols
    print nrows , ncols

    #获取整行和整列的值（数组）
    print table1.row_values
    print table1.col_values

    #遍历sheet
    for i  in range(nrows):
        print "row %s: %s" % (i, table1.row_values(i))

    #获取单元格



    #分别使用行列索引
