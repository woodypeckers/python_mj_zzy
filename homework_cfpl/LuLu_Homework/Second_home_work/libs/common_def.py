#!/user/bin/env python
#encoding:utf-8
import os,xlrd

def  username_password(path):

    #登陆用户参数化
    data=xlrd.open_workbook(path)
    table=data.sheets()[0]
    for i in range(table.nrows):
        if i==0:
            continue

        dict[i]=table.row_values(i)
    return dict
