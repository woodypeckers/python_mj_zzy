#!/usr/bin/python
#encoding:utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import random
import unittest, time, re

class Bf(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost"
        self.verificationErrors = []
        self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
    def test_login(self):
        driver = self.driver
        self.assertEqual(u"登录 - BugFree", driver.title)
        # assertTitle登录 - BugFree
        driver.find_element_by_id("LoginForm_username").clear()
        driver.find_element_by_id("LoginForm_username").send_keys("admin")
        driver.find_element_by_id("LoginForm_password").clear()
        driver.find_element_by_id("LoginForm_password").send_keys("123456")
        Select(driver.find_element_by_id("LoginForm_language")).select_by_value("en")
        Select(driver.find_element_by_id("LoginForm_language")).select_by_value("zh_cn")
        """判断状态 32--35行"""
        if not driver.find_element_by_id("LoginForm_rememberMe").is_selected():
            driver.find_element_by_id("LoginForm_rememberMe").click()
        if driver.find_element_by_id("LoginForm_rememberMe").is_selected():
            driver.find_element_by_id("LoginForm_rememberMe").click()
        driver.find_element_by_id("SubmitLoginBTN").click()

    def test_bf_yhgl(self):
        driver = self.driver
        self.get(self.base_url + '/bugfree/index.phpsite/login')
        driver.find_element_by_id("xxx")
        self.assertEqual(u"确定进行此操作？", self.close_alert_and_get_its_text())
        """检查点：一些使用方法"""
        print "当前url：" ,driver.current_url
        print "当前窗口：",driver.get_window_position(),driver.get_window_size()#position 位置 #size大小
        self.assertEqual(u"头",driver.title)#判断title
        self.assertSequenceEqual()#序列相同
        self.assert
        self.assertEqual(u"admin", driver.find_element_by_id("LoginForm_username").text)#验证输入

        print driver.find_element_by_css_selector("BODY").text #css
        print driver.page_source# 页面源代码

        self.assertRegexpMatches(driver.page_source, r"<title>BugFree</title>")
        """RegexpMatches--正则表达式匹配,判断页面存在元素,注意：r的转义功能"""
        self.assertSetEqual()#集合相等
        driver.back()
        driver.get("URL")
        driver.refresh()#刷新
        driver.forward()#前进
        driver.switch_to.alert.accept(), driver.switch_to.alert.dismiss()#处理弹出框
        """动作链"""
        link1 = driver.find_element_by_class_name("pf")#点击“pf”控件之后,弹出其他控件
        ActionChains(driver).move_to_element_with_offset(link1).perform()#??????
        ActionChains(driver).move_to_element(link1).perform()
        ActionChains(driver).double_click(link1).perform()  #双击操作
        ActionChains(driver).drag_and_drop(element, target).perform()  #鼠标拖放操作
        """#如何使用(element, target)???"""

        title = self.driver.title
        try:
            self.assertEqual(title,'BugFree')
        except AssertionError as e:
            print u"断言错误"

        """判断当前窗口driver.current_window_handle"""
        print u"当前窗口:{0}".format(self.driver.current_window_handle)

        """#先定位ID，再定位id内的元素"""
        options = self.driver.find_element_by_id("xxx").find_element_by_tag_name("sss")
        options.pop(2).click()
        """不重复新建"""
        driver.find_element_by_id("xxx").send_keys(u"创建："+ str(random.randrange(0,100)))



    """接口测试Pastman(chrome的插件)，RESTclient(firefox插件)思路和数据"""
   # git log --graph --pretty== oneline

