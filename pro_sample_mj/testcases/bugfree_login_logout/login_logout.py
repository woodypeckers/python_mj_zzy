#!/usr/bin/env python
# encoding:utf-8
# author:mj
import unittest, os
from selenium import webdriver
from lib.utils import read_excel
from config import *
from testcases.bussiness_common_steps.bussiness_common_steps import *


class Login_logout_parameter(unittest.TestCase):
    def setUp(self):
        driver = self.driver
        self.executable_path = chrome_driver
        self.driver = webdriver.Chrome(executable_path=self.executable_path)
        driver.url = "http://localhost/bugfree"
        open_url(self.driver, self.url)
        self.data_dict = read_excel(os.getcwd()+"/docs/xlrd_excel.xlsx")

    def tearDown(self):
        self.driver.quit()

    def test_login_sucess(self):
        """登录成功"""
        driver = self.driver
        username, password, flag = self.ret_dict[1]
        print username, password, flag
        Bugfree_Login(driver, username, password)
        self.assertEqual(flag, driver.title)