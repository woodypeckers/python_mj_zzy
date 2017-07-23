#!/user/bin/env python
# encoding:utf-8
import  time
import unittest
from selenium import webdriver
from testcases.bussiness_common_steps.bussiness_common_steps import *
from config import *

class BugfreeImport(unittest.TestCase):
    def setUp(self):
        #driver封装
        self.executable_path = chrome_driver
        self.driver = webdriver.Chrome(executable_path=self.executable_path)
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

    def test_bugfree_import(self):
        """测试导入文件的功能"""
        driver = self.driver
        driver.find_element_by_link_text(u"导入").click()# BUG页面 下面的导入链接
        # driver.implicitly_wait(3)
        """
        driver.find_element_by_id("casefilename").click()#浏览按钮
        中间选择或输入文件名
        driver.find_element_by_id("uploadbutton").click()#浏览按钮 下面的导入按钮
        """
        # click_element_id_with_sleep(driver,id="casefilename",sleep =0)#默认为2
        #浏览按钮，显示输入文件名
        click_element_id_with_sleep(driver,"casefilename",0)#上面写法也正确
        input_filename_click()
        # import os
        # cur = os.getcwd()
        # os.system("%s/tools/upload_filexml.exe" % cur)
        get_screenshot_immediately(driver)
        #导入
        click_element_id_with_sleep(driver,"uploadbutton",0)
        driver.switch_to.alert.accept()#接受弹框