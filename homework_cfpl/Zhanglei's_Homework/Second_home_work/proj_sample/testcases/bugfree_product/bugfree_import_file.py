#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: zhanglei
import unittest
from selenium import webdriver
from config import *
from testcases.inpublic.inpublic import *

class BugfreeImportFile(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(chrome_driver)
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost"
        driver = self.driver
        open_url(driver,self.base_url + "/bugfree/index.php/site/login")
        bugfree_login(driver,"admin","123456")

    def teardown(self):
        self.driver.quit()

    def test_bugfree_import_file(self):
        driver=self.driver
        driver.find_element_by_link_text(u"导入").click()

        # 打开选择文件对话框，然后选择文件，最后点确定
        click_element_by_id_with_sleep(driver,"casefilename")

        #打开windows窗口，选择文件导入
        input_filename_click_ok()
        #选择文件后截取当前窗口图
        get_screenshot_immediately(driver)
        #点击【导入】按钮
        click_element_by_id_with_sleep(driver,"uploadbutton")
        driver.switch_to.alert.accept()
        get_screenshot_immediately(driver)
        driver.quit()




