#!/usr/bin/python
# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from HTMLTestRunner import HTMLTestRunner
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class Sel_Web_baidu(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)#智能等待
        self.driver.maximize_window()#窗口最大化
        self.base_url = "http://www.baidu.com"
        self.verificationErrors = []
        self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()

    def test_baidu_sz(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        link1 = driver.find_element_by_link_text(u"设置")
        ActionChains(driver).move_to_element(link1).perform()# move to element移动到元素，perform执行
        # ActionChains(driver).double_click(link).perform()  双击操作
        # ActionChains(driver).drag_and_drop(element, target).perform()  鼠标拖放操作
        time.sleep(2)
        # driver.find_element_by_link_text(u"搜索设置").click()
        driver.find_element_by_class_name("setpref").click()
        time.sleep(2)
        # driver.find_element_by_partial_link_text(u"是否希望在搜索时显示")
        """检查点1：部分匹配"""
        driver.find_element_by_id("sh_1").click()
        driver.find_element_by_id("sh_2").click()
        driver.find_element_by_link_text(u"保存设置").click()
        print driver.switch_to.alert.text
        driver.switch_to.alert.accept()#switch to alert弹出框，accept接受
        # driver.get_screenshot_as_png()
        driver.get_screenshot_as_file(r"C:\\cap\\baidu_screen.jpg")#需要在本地创建对应目录

    def test_baidu_control(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text(u"新闻").click()
        driver.find_elements_by_partial_link_text(u"百度新闻搜索")
        """检查title1：百度新闻搜索——全球最大的中文新闻平台"""
        driver.find_element_by_id("ww").clear()
        driver.find_element_by_id("ww").send_keys(u"论测试的重要性与背锅侠")
        time.sleep(2)
        driver.find_element_by_id("ww").send_keys(Keys.BACK_SPACE * 4)
        driver.find_element_by_class_name("btn").click()
        time.sleep(2)
        # driver.find_element_by_partial_link_text(u"找到相关新闻")
        """检查2：页面是否部分匹配"""
        # driver.find_element_by_id("nav-hot-link").click()
        driver.find_element_by_id("help").click()
        time.sleep(2)
        driver.back()
        """????????????????"""
        # driver.find_element_by_class_name("qafeedback").click()#给百度提意见
        # driver.switch_to.iframe("iframeu2398766_0")
        # driver.find_element_by_xpath("html/body/div[1]/div/div/a[2]").click()
        # driver.find_element_by_class_name("fb-textarea fb-content-block").send_keys(u"百度很难看")
        # driver.find_element_by_class_name("fb-phone-txt").send_keys(u"18000001111")
        # driver.find_element_by_id("fb_right_canvas_save").click()
        # driver.switch_to.window(driver.window_handles[1])# 切换到新打开的窗口
        # driver.close()#关闭当前窗口

    def test_baidu_login(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_css_selector("#u1 > a[name=\"tj_login\"]").click()
        driver.find_element_by_link_text(u"QQ帐号").click()
        driver.switch_to.window(driver.window_handles[1])
        """????"""
        # driver.find_element_by_id("switcher_plogin").click()
        # time.sleep(2)
        # driver.find_element_by_id("u").clear()
        # driver.find_element_by_id("u").send_keys("171012089")
        # driver.find_element_by_id("p").clear()
        # driver.find_element_by_id("p").send_keys("liuniancongmang")
        # driver.find_element_by_id("login_button").click()

if __name__ == '__main__':
    suit = unittest.TestSuite()
    loader = unittest.TestLoader()
    suit.addTests(loader.loadTestsFromTestCase(Sel_Web_baidu))

    fp = open("./test_result_%s.html"% time.strftime("%Y-%m-%d %H-%M-%S"),'wb')
    runner = HTMLTestRunner(
        stream=fp,
        title=u'百度搜索测试报告',
        description=u"测试用例执行情况：")

    runner.run(suit)
    fp.close()
