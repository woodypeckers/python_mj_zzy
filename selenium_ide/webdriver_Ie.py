#!/usr/bin/python
# -*- coding: UTF-8 -*-
import unittest, time, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

class baidu_refresh(unittest.TestCase):
    def setUp(self):
        # self.driver = webdriver.Ie(r"C:\Program Files (x86)\Internet Explorer\iexplore.exe")
        self.driver = webdriver.Chrome(r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\Chrome.exe")
        self.driver.implicitly_wait(30)#智能等待
        self.driver.maximize_window()#窗口最大化
        self.base_url = "https://www.baidu.com"
        self.verificationErros = []#错误验证
        self.accept_next_alert = True #接受报警

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErros)

    def test_baidu_refresh(self):
        self.driver.get(self.base_url + '/')
        # driver = self.driver
        # driver.get(self.base_url + "/")
        self.driver.find_element_by_id('kw').click()
        self.driver.find_element_by_id('kw').clear()
        self.driver.find_element_by_id('kw').send_keys(u"百度一下")
        self.driver.find_element_by_id('su').click()
        self.driver.back()#回退
        time.sleep(3)
        self.driver.forward()#前进
        time.sleep(3)
        self.driver.refresh()#刷新

if __name__ == "__main__":
    unittest.main()