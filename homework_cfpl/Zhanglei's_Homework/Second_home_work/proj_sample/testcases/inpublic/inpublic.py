#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: zhanglei
import time


def bugfree_login(driver,username,password):

    driver.find_element_by_id("LoginForm_username").clear()
    driver.find_element_by_id("LoginForm_username").send_keys(username)
    driver.find_element_by_id("LoginForm_password").clear()
    driver.find_element_by_id("LoginForm_password").send_keys(password)
    driver.find_element_by_id("SubmitLoginBTN").click()

def zhaopin_login(driver,username,password):
    driver.find_element_by_id("txtLoginName").clear()
    driver.find_element_by_id("txtLoginName").send_keys(username)
    driver.find_element_by_id("txtPassword").clear()
    driver.find_element_by_id("txtPassword").send_keys(password)
    driver.find_element_by_id("ibnLogin").click()

def open_url(driver,url):
    driver.get(url)

def click_element_by_id_with_sleep(driver, id, sleep=2):
    try:
        driver.find_element_by_id(id).click()
    except:
        pass
    finally:
        time.sleep(2)

def clear_element_by_name_with_send_keys(driver, name,value):
    try:
        driver.find_element_by_name(name).clear()
        driver.find_element_by_name(name).send_keys(value)
    except:
        pass
    finally:
        time.sleep(1)

def input_filename_click_ok():
    #导入文件
    import os
    cur_dir=os.getcwd()  #获取当前窗口的路径
    os.system("%s/tools/upload_file_company_x64.exe" % cur_dir)

def get_screenshot_immediately(driver,path=None):
    #截图
    if path is None:
        driver.get_screenshot_as_file(r"./pic/pic_%s.jpg" % time.strftime("%Y-%m-%d %H-%M-%S"))
    else:
        driver.get_screenshot_as_file(path)
