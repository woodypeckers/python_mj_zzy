#!/usr/bin/env python
# author : mj
# -*- coding: utf-8 -*-
# Created by iFantastic on 2018/7/7


import xlrd
class EecelUtil(object):
    def __init__(self,execelpath,sheetname):
        self.data = xlrd.open_workbook(execelpath)
        self.table = self.data.sheet_by_name(sheetname)

        self.row