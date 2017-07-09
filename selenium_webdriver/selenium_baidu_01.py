# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class SeleniumBaidu01(unittest.TestCase):
    def setUp(self):
        # self.driver = webdriver.Ie(r'C:\Program Files\Internet Explorer\IEDriverServer.exe')
        self.executable_path = r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\ChromeDriver.exe'
        self.driver = webdriver.Chrome(executable_path=self.executable_path)
        #self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.baidu.com"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_selenium_baidu01(self):
        driver = self.driver
        driver.get(self.base_url +"/")
        driver.find_element_by_id("kw").click()
        driver.find_element_by_id("kw").clear()
        driver.find_element_by_id("kw").send_keys(u"selenium ide")
        driver.find_element_by_id("kw").send_keys(Keys.BACK_SPACE*4) # 后退4个位置
        driver.find_element_by_id("su").click()
        time.sleep(3)
        driver.back() #浏览器的回退
        driver.find_element_by_id("su").click()
        driver.forward()  #前进
        driver.refresh() #刷新
 
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
