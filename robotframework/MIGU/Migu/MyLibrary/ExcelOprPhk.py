# -*- coding: utf-8 -*-

import xlwt
import os
from xlutils.copy import copy
from xlrd import open_workbook

def create_excel(fileName='test.xls', sheetName='Sheet1'):
    '''
    创建一个excel文件
    '''
    file = xlwt.Workbook()
    table = file.add_sheet(sheetName)
    file.save(fileName)
    
def del_excel(fileName='test.xls'):
    '''
    删除excel文件
    '''
    os.remove(fileName)
    
def change_excel_cell_value(value, row, col, fileName='test.xls', sheetIndex='0'):
    '''
    修改excel某个单元格的值
    row：excel单元格行号（为0表示第一行） col：excel单元格列号（为0表示第一列）
    value：修改后的单元格的值 fileName:修改的excel文件的名称
    sheetIndex：修改的sheet的序列号（为0表示第一个sheet）
    
    Example:
    | Change excel cell value | 3 | 4 | iowe | 修改单元格4E的值为iowe
    | Change excel cell value | 3 | 4 | iowe | test.xls | 0 | 
    修改test.xls第一个sheet里面单元格4E的值为iowe
    '''
    #由于RFS里面传过来的值都为字符串，所有行号和列号先做一个整形的转换
    row = int(row)
    col = int(col)
    sheetIndex = int(sheetIndex)

    rb = open_workbook(fileName,formatting_info=True)  #formatting_info=True,会保存excel原来的格式
    #rs = rb.sheet_by_index(0) #通过sheet_by_index()获取的sheet没有write()方法
    wb = copy(rb)
    ws = wb.get_sheet(sheetIndex)
    ws.write(row, col, value)
    wb.save(fileName)

def change_excel_value_by_row(value, row=1, col=0, fileName='test.xls', sheetIndex='0'):
    '''
    往excel文档中插入一行记录
    从row+1行，col+1列的那个单元格开始，连续修改同一行单元格的值。
    value里面有多少个参数，就连续修改多少个单元格的值，value的参数用英文逗号分隔
    默认从A2开始写.也就是第二行第一个单元格开始写
    '''
    #由于RFS里面传过来的值都为字符串，所有行号和列号先做一个整形的转换
    startRow = int(row)
    startCol = int(col)
    sheetIndex = int(sheetIndex)
    
    cellValues = value.split(',')
    
    rb = open_workbook(fileName,formatting_info=True)  #formatting_info=True,会保存excel原来的格式
    wb = copy(rb)
    ws = wb.get_sheet(sheetIndex)
    
    for item in cellValues:
        ws.write(startRow, startCol, item)
        startCol = startCol + 1
    
    wb.save(fileName)
    
def change_excel_value_by_col(value, rows, startRow=1, fileName='test.xls', sheetIndex='0'):
    '''
    往excel插入多行记录。可以用来测试支持导入的最大记录数
    value:插入excel文件中每一行的值。每个单元格的值用英文逗号分隔
    rows:总共插入多少行记录
    默认从第二行开始
    '''
    #由于RFS里面传过来的值都为字符串，所有行号和列号先做一个整形的转换
    startRow = int(startRow)
    rows = int(rows)
    startCol = 0
    sheetIndex = int(sheetIndex)
    
    cellValues = value.split(',')
    
    rb = open_workbook(fileName,formatting_info=True)  #formatting_info=True,会保存excel原来的格式
    wb = copy(rb)
    ws = wb.get_sheet(sheetIndex)
    
    for i in range(rows):
        for item in cellValues:
            ws.write(startRow, startCol, item)
            startCol = startCol + 1
        startRow = startRow + 1
        startCol = 0
    wb.save(fileName)
