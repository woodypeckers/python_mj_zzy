#!/usr/bin/env python
# encoding:utf-8
# author:mj
import unittest,time
import os  #加载operation system


# class BugfreeClass(unittest.TestCase):
def Bugfree_Login(driver, admin, passwd):
    """登录的公共部分"""
    driver.find_element_by_id("LoginForm_username").clear
    driver.find_element_by_id("LoginForm_username").send_keys(admin)
    driver.find_element_by_id("LoginForm_username").clear
    driver.find_element_by_id("LoginForm_password").send_keys(passwd)
    driver.find_element_by_id("SubmitLoginBTN").click()

def click_element_id_with_sleep(driver, id, sleep=2):
    """通过id去点击，判断是否存在，不存在pass"""
    try:
        driver.find_element_by_id(id)
    except:
        pass
    finally:
        time.sleep(2)

def input_filename_click():
    """输入文件名，点击确定
    os  #加载operation system
    os.getcwd  #使用os.getcwd()可以获得当前的工作目录（current working directory），
    注意：getcwd函数不需要参数，它返回的是当前地址
    """
    cur = os.getcwd()
    print cur
    os.system("%s/tools/upload_file_x64.exe" % cur)


def open_url(driver, url):
    """打开URL 网络编程"""
    driver.get(url)

def get_screenshot_immediately(driver, path=None):
    """截图 --判断路径"""
    if path is None:
        driver.get_screenshot_as_file(r"./screen_shots/shots_%s.jpg" % time.strftime("%Y-%m-%d %H-%M-%S"))
    else:
        driver.get_screenshot_as_file(path)

