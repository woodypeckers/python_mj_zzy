#!/usr/bin/env python
# author : mj
# -*- coding: utf-8 -*-
# Created by iFantastic on 2018/7/7
import xlrd

class ExcelUtil():
    def __init__(self,excelpath,sheetname):
        self.data = xlrd.open_workbook(excelpath)
        self.table = self.data.sheet_by_name(sheetname)

        self.keys = self.table.row_values(0)

        self.rowNum = self.table.nrows
        self.colNum = self.table.ncols

    def dict_data(self):
        if self.rowNum <= 1:
            print('the sum of line is less than 1')

        else:
            r = []
            j = 1
            for i in range(self.rowNum-1):
                s = {}
                values = self.table.row_values(j)
                for x in range(self.colNum):
                    s[self.keys[x]] = values[x]
                r.append(s)
                j+=1
            return  r

if __name__ == "__main__":
    filepath = "./test.xlsx"
    sheetName = "Sheet1"
    data = ExcelUtil(filepath, sheetName)
    print (data.dict_data())
