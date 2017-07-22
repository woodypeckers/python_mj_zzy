#!/user/bin/env python
#encoding:utf-8
from selenium.webdriver.support.select import Select
import random,time
from bugfree_login_logout import BugfreeLoginLogout
from config.config import Varies
from selenium import webdriver
import xlrd,os
from libs.common_def import  *
class BugfreeResult(BugfreeLoginLogout,Varies):

    def test_bugfree_1(self):

        #多项下拉框选择
        self.driver.find_element_by_class_name("selectedtab").click()
        self.driver.find_element_by_xpath(".//*[@id='SearchConditionRow0']/td[7]/a/img").click()
        Select(self.driver.find_element_by_id("BugFreeQuery_field1")).select_by_visible_text(u"ID")
        Select(self.driver.find_element_by_id("BugFreeQuery_operator1")).select_by_visible_text(u"等于")
        self.driver.find_element_by_id("PostQuery").click()


    def  test_bugfree_2(self):

         #保存查询
         self.driver.find_element_by_link_text("Result").click()
         self.driver.find_element_by_id("SaveQuery").click()
         self.driver.find_element_by_id("dialogQueryTitle").send_keys("test_ ",random.randint(1,99))
         time.sleep(3)


    # def  test_bugfree_3(self):
    #
    #     #用户登陆页面验证
    #     self.driver.quit()
    #     self.driver=webdriver.Ie(self.ie_path)
    #     self.driver.get(self.base_url)
    #     #current_dir=os.getcwd()
    #     dict=username_password(u"E:\TEST\pycharmcode\python_wanjl_code\201707170800\data\登陆用户名单.xls")
    #     for i in range(self.table.nrows):
    #
    #         self.driver.find_element_by_id("LoginForm_username").clear()
    #         self.driver.find_element_by_id("LoginForm_username").send_keys(dict[i]["username"])
    #         self.driver.find_element_by_id("LoginForm_password").clear()
    #         self.driver.find_element_by_id("LoginForm_password").send_keys(dict[i]["password"])
    #         self.driver.find_element_by_id("SubmitLoginBTN").click()
    #         if self.assertEqual("BugFree",self.driver.title):
    #             break





















