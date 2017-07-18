# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import unittest, time, re

class Baidu01(unittest.TestCase):
    def setUp(self):
        # self.driver = webdriver.Chrome(
        #     executable_path=r'C:\Users\v_leiizhang\AppData\Local\Google\Chrome\Application\chromedriver.exe')
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.baidu.com"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_baidu01(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("kw").click()
        driver.find_element_by_id("kw").clear()
        driver.find_element_by_id("kw").send_keys(u"感恩的心")
        time.sleep(1)
        driver.find_element_by_id("kw").send_keys(Keys.SPACE)
        time.sleep(1)
        driver.find_element_by_id("kw").send_keys(u"李瀚均")
        time.sleep(1)
        driver.find_element_by_id("kw").send_keys(Keys.SPACE)
        driver.find_element_by_id("kw").send_keys("2013")
        time.sleep(1)
        #driver.find_element_by_id("kw").send_keys(u"感恩的心 李瀚均 2013")
        driver.find_element_by_id("su").click() #点击按钮【百度一下】
        a1=driver.find_element_by_xpath(".//*[@id='1']/h3/a")
        a1.click()
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_id("query").send_keys(Keys.BACK_SPACE * 4)
        #driver.find_element_by_id("kw").send_keys(Keys.BACK_SPACE*4)
        time.sleep(1)
        driver.find_element_by_id("query").send_keys(Keys.SPACE*2)
        time.sleep(1)
        driver.find_element_by_id("query").send_keys("2017")
        time.sleep(1)
        #driver.find_element_by_id("query").send_keys(u"感恩  2017")
        driver.find_element_by_id("search").click()
        time.sleep(2)
        driver.find_element_by_link_text(u"网页").click()
        time.sleep(2)
        driver.maximize_window()
        time.sleep(1)
        #driver.find_element_by_link_text(u"下一页").click()
        #ActionChains(driver).move_to_element(link1).click()#perform()  # move to element移动到元素，perform执行
        driver.find_element_by_xpath(".//*[@id='page']/a[10]").click()

        time.sleep(2)
        driver.close()

    def test_baidu02(self):
        driver=self.driver
        driver.get(self.base_url + '/')
        driver.maximize_window()
        setting1=driver.find_element_by_link_text(u"设置")
        ActionChains(driver).move_to_element(setting1).perform()  # move to element移动到元素，perform执行
        time.sleep(2)
        setting2 = driver.find_element_by_link_text(u"高级搜索")
        ActionChains(driver).move_to_element(setting2).perform()
        time.sleep(1)
        driver.find_element_by_link_text(u"高级搜索").click()
        time.sleep(2)
        driver.find_element_by_xpath(".//*[@id='wrapper']/div[7]/span").click()
        driver.maximize_window()
        driver.find_element_by_id("kw").send_keys(u"天涯明月刀")
        time.sleep(1)
        driver.find_element_by_id("su").click()
        time.sleep(2)
        driver.find_element_by_partial_link_text(u"天涯明月刀OL")
        driver.find_element_by_link_text("天涯明月刀OL").click()
        driver.switch_to.window(driver.window_handles[1])
        driver.get_screenshot_as_file(r'./picture_%s.jpg' % time.strftime("%Y-%m-%d %H-%M-%S"))
        time.sleep(2)
        driver.close()

    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
