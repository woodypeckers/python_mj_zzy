#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author : mj
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import random,string
import unittest, time, re


class BugLoginLogout(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.base_url = "http://10.1.3.76:8092/admin"
        driver = self.driver
        driver.get(self.base_url + "/portal/login.jsp")
        driver.switch_to.frame("loginPage")
        driver.find_element_by_id("loginName").clear()
        driver.find_element_by_id("loginName").send_keys("taotao19")
        driver.find_element_by_xpath("//*[@id='artiPwd']").click()
        # driver.find_element_by_class_name("login-pwd enter-submit").find_element(self,by="password",value="password")
        time.sleep(2)
        driver.find_element_by_name("password").send_keys("aaa111")
        driver.find_element_by_id("loginButton").click()
        # time.sleep(3)
        # fp =open('./name%s_.png '% time.strftime("%Y-%m-%s %H-%M-%S",'wb'))
        # driver.save_screenshot(fp)
        time.sleep(2)
        # print self.driver.title()
        # self.assertEqual(u"统一工作平台", driver.title)


    def test_mywork(self):
        driver = self.driver
        driver.get(self.base_url + "/workbench/main.jsp")
        # driver.find_element_by_id("workBench").click()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[0])
        driver.find_element_by_xpath(".//*[@id='header']/div[2]").click()
        time.sleep(2)
        # ActionChains(driver).move_to_element(link1).perform()# move to element移动到元素，perform执行
        # ActionChains(driver).double_click(link1).perform()  #双击操作
    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    #suite.addTest(unittest.FunctionTestCase(testSomething))
    suite.addTest(BugLoginLogout('test_mywork'))
    unittest.TextTestRunner(verbosity=2).run(suite)






"""制图"""
from PIL import Image
import os, sys
def toImage():
    mw = 100
    ms = 20

    msize = mw * ms
    toImage = Image.new("RGBA", (2000, 2000))

    for y in range(1, 21):
        for x in range(1, 21):
            try:
                fromImage = Image.open(
                    r"C:/Users/zhangzhanyong/Desktop/FAQ/%s.jpg" % str(ms * (y - 1) + x)
                )
                fromImage = fromImage.resize((100, 100), Image.ANTIALIAS)
                toImage.paste(fromImage, ((x - 1) * mw, (y - 1) * mw))
            except IOError:
                pass
    toImage.show()
    toImage.save("D://sanyecao2.jpg")






