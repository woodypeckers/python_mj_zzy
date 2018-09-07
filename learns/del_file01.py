#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author : mj   https://www.2cto.com/kf/201009/74908.html
import os
import shutil
import traceback
import glob
import logging

# def misc_init():
#     current_path = os.path.split(os.path.realpath(__file__))[0]
#     print current_path
    # except_folders = glob.Except_Folders
    # current_filelist = os.listdir(current_path)
    # print current_filelist
    # for f in current_filelist:
    #     if os.path.isdir(os.path.join(current_path,f)):
    #         if f in except_folders:
    #             continue
    #         else:
    #             real_folder_path = os.path.join(current_path, f)
    #             try:
    #                 for root, dirs, files in os.walk(real_folder_path):
    #                     for name in files:
    #                         # delete the log and test result
    #                         del_file = os.path.join(root, name)
    #                         os.remove(del_file)
    #                         logging.info('remove file[%s] successfully' % del_file)
    #                 shutil.rmtree(real_folder_path)
    #                 logging.info('remove foler[%s] successfully' % real_folder_path)
    #             except Exception, e:
    #                 traceback.print_exc()


# import shutil
# path = 'D://python_zhanyong/git_branch_mj/a01/a02'
# shutil.rmtree(path)#rmtree只能删除空文件夹

#======================================================
import os
def remove_dir(dir):
    dir = dir.replace('\\', '/')#\\替换成/
    if(os.path.isdir(dir)):#isdir()括号内是一个存在的目录，则返回True。否则返回False。
        for p in os.listdir(dir):#os.listdir列出当前路径下的文件夹
            remove_dir(os.path.join(dir,p))#os.remove删除掉文件
        if(os.path.exists(dir)):#os.path.exists() 用于判断变量、文件等是否存在
            os.rmdir(dir)#os.rmdir(path)删除目录 path，要求path必须是个空目录,否则抛出OSError错误
    else:
        if(os.path.exists(dir)):
            os.remove(dir)#os.remove(path)删除文件 path. 如果path是一个目录， 抛出 OSError错误。

remove_dir(r'D:/python_zhanyong/git_branch_mj/a01/a02') #函数使用
print 'ok'

''' 可查看http://book.51cto.com/art/201405/440067.htm   
os.path.join(path1[, path2[, ...]])  
将多个路径组合后返回，第一个绝对路径之前的参数将被忽略。
>>> os.path.join('c:\\', 'csv', 'test.csv')   
'c:\\csv\\test.csv'   
>>> os.path.join('windows\temp', 'c:\\', 'csv', 'test.csv')   
'c:\\csv\\test.csv'   
>>> os.path.join('/home/aa','/home/aa/bb','/home/aa/bb/c')   
'/home/aa/bb/c'   '''
#==========================================================
#方法2：利用python的成熟的模块
import shutil
shutil.rmtree()
__import__('shutil').rmtree()
