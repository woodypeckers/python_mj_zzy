#!/usr/bin/env python
# encoding:utf-8
# author:mj
import unittest
from selenium import webdriver

def Bugfree_Login(driver, admin, passwd):
    self.base_url = "http://localhost"
    driver = self.driver
    driver.get(self.base_url + "/bugfree/index.php/site/login")
    self.assertEqual(u"登录 - BugFree", driver.title)
    # assertTitle登录 - BugFree
    driver.find_element_by_id("LoginForm_username").send_keys(admin)
    driver.find_element_by_id("LoginForm_password").send_keys(passwd)
