#!/usr/bin/env python
# encoding:utf-8
# author:mj
import unittest, os,time
from selenium import webdriver
from lib.utils import read_excel
from config import *
from testcases.bussiness_common_steps.bussiness_common_steps import *


class Login_logout_parameter(unittest.TestCase):
    def setUp(self):
        self.executable_path = chrome_driver
        self.driver = webdriver.Chrome(executable_path=self.executable_path)
        self.url = "http://localhost/bugfree"
        open_url(self.driver, self.url)
        self.data_dict = read_excel(os.getcwd()+"/docs/xlrd_excel.xlsx")

    def tearDown(self):
        self.driver.quit()

    def test_login_sucess(self):
        """登录成功"""
        driver = self.driver
        username, password, flag = self.data_dict[1]
        print username, password, flag
        Bugfree_Login(driver, username, password)
        get_screenshot_immediately(driver)
        self.assertEqual(flag, driver.title)

    def test_bugfree_login_fail_invalid_password(self):
        """登录Bugfree失败，用户名和密码不匹配 """
        driver = self.driver
        username, password, flag = self.data_dict[2]
        print username, password, flag
        Bugfree_Login(driver, username, password)
        get_screenshot_immediately(driver)
        time.sleep(2)
        self.assertIn(flag, driver.page_source)

    def test_bugfree_login_fail_invalid_username(self):
        """登录Bugfree失败，用户名不存在"""
        driver = self.driver
        username, password, flag = self.data_dict[3]
        print username, password, flag
        Bugfree_Login(driver, username, password)
        get_screenshot_immediately(driver)
        self.assertIn(flag, driver.page_source)