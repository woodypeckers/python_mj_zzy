# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class Eamil163(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Ie(r"C:\Program Files (x86)\Internet Explorer\iexplore.exe")
        self.driver.implicitly_wait(30)
        self.base_url = "http://mail.163.com"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_Eamil163(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("lbNormal").click()
        driver.switch_to.frame("x-URS-iframe")
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys("zhangzhanyong886")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("zelin0504")
        # driver.find_element_by_id("dologin").click()
        # self.assertEqual(u"网易邮箱6.0版", driver.title)
        # driver.find_element_by_link_text(u"退出").click()

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
