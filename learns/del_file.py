#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author : mj
import os
import shutil
import traceback
import glob
import logging

def misc_init():
    current_path = os.path.split(os.path.realpath(__file__))[0]
    except_folders = glob.Except_Folders
    current_filelist = os.listdir(current_path)
    for f in current_filelist:
        if os.path.isdir(os.path.join(current_path,f)):
            if f in except_folders:
                continue
            else:
                real_folder_path = os.path.join(current_path, f)
                try:
                    for root, dirs, files in os.walk(real_folder_path):
                        for name in files:
                            # delete the log and test result
                            del_file = os.path.join(root, name)
                            os.remove(del_file)
                            logging.info('remove file[%s] successfully' % del_file)
                    shutil.rmtree(real_folder_path)
                    logging.info('remove foler[%s] successfully' % real_folder_path)
                except Exception, e:
                    traceback.print_exc()