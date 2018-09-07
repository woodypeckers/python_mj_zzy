# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from HTMLTestRunner import HTMLTestRunner
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import random
from pro_sample_mj.config import *
from pro_sample_mj.testcases.bussiness_common_steps.bussiness_common_steps import *


class ProductManagement(unittest.TestCase):
    def setUp(self):
        #driver封装
        self.executable_path = ie_driver
        self.driver = webdriver.Ie(executable_path=self.executable_path)
        # self.derver = webdriver.Chrome(r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe")
        self.driver.maximize_window()
        self.url = "http://localhost/bugfree"
        #封装url
        open_url(self.driver, self.url)
        self.assertEqual(u"登录 - BugFree", self.driver.title)
        #登录
        Bugfree_Login(self.driver, "admin", "123456")

    def tearDown(self):
        self.driver.quit()

    def test_product_management(self):
        """后台管理中产品的查询"""
        driver = self.driver
        # Select(driver.find_element_by_id("target_table")).select_by_visible_text(u"自定义字段")
        Select(driver.find_element_by_id("target_table")).select_by_visible_text(u"产品管理")
        driver.find_element_by_id("name").clear()
        driver.find_element_by_id("name").send_keys("abcd_%s",random.randint(1,21))
        driver.find_element_by_css_selector("input.btn").click()
        time.sleep(1)
        Select(driver.find_element_by_id("pageSize")).select_by_visible_text("35")
        time.sleep(1)
        get_screenshot_immediately(driver)

    def test_back_stage_management(self):
        """后台管理中系统设置的操作"""
        driver = self.driver
        driver.find_element_by_link_text(u"后台管理").click()
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_link_text(u"系统设置").click()
        driver.find_element_by_link_text(u"编辑").click()
        driver.find_element_by_id("TestOption_option_value").clear()
        driver.find_element_by_id("TestOption_option_value").send_keys("%s" % random.randrange(1,33,2))
        # driver.find_element_by_id("name").clear()
        driver.find_element_by_id("name").send_keys("2")
        #指定截图位置
        get_screenshot_immediately(path=r"C:\\cap\\bugfree_%s.jpg" % time.strftime("%Y-%m-%d %H-%M-%S"))

    """
    Select(driver.find_element_by_class_name("required")).select_by_value("internal")
    Select 可以换成下面的
    driver.find_element_by_class_name("required").find_elements_by_tag_name("option")[1].click()
    """





