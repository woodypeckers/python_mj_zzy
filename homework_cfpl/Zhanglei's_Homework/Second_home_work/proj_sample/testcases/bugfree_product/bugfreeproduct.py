#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: zhanglei
import time
import unittest
#from config import *
from proj_sample.config import *
from selenium import webdriver
from proj_sample.testcases.inpublic.inpublic import open_url

from proj_sample.testcases.inpublic.inpublic import bugfree_login
from proj_sample.testcases.inpublic.inpublic import *



class BugfreeProduct(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(chrome_driver)
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost"
        driver = self.driver
        #driver.get(self.base_url + "/bugfree/index.php/site/login")
        open_url(driver, self.base_url + "/bugfree")
        bugfree_login(driver,"admin","123456")


    def test_product002(self):
        """编辑产品信息"""
        driver = self.driver
        driver.get(self.base_url + "/bugfree/index.php/bug/list/1")
        driver.find_element_by_link_text(u"后台管理").click()
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_partial_link_text(u"产品管理")  # 检查跳转的页面部分匹配“产品管理”
        driver.find_element_by_xpath(r".//*[@id='SearchResultDiv']/table/tbody/tr[1]/td[6]/a[1]").click()
        # driver.find_element_by_xpath(u"(//a[contains(text(),'编辑')])[4]").click()
        driver.find_element_by_id("Product_product_manager").click()
        driver.find_element_by_id("Product_display_order").clear()
        driver.find_element_by_id("Product_display_order").send_keys("111")
        driver.find_element_by_id("Product_name").clear()
        driver.find_element_by_id("Product_name").send_keys(u"产品1")
        driver.find_element_by_id("Product_bug_severity").clear()
        driver.find_element_by_id("Product_bug_severity").send_keys("2")
        driver.find_element_by_id("Product_bug_priority").clear()
        driver.find_element_by_id("Product_bug_priority").send_keys("2")
        driver.find_element_by_id("Product_case_priority").clear()
        driver.find_element_by_id("Product_case_priority").send_keys("2")
        driver.find_element_by_name("yt0").click()
        time.sleep(3)
        driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.find_element_by_link_text(u"退出").click()


    def tearDown(self):

        time.sleep(3)
        self.driver.quit()
        #self.assertEqual([], self.verificationErrors)

