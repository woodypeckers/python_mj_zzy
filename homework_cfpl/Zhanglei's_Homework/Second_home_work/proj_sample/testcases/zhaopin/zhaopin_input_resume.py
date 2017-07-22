#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: zhanglei

import unittest,os,xlrd
from proj_sample.config import *
from selenium import webdriver
from proj_sample.testcases.inpublic.inpublic import open_url
from selenium.webdriver.support.ui import Select
from proj_sample.testcases.inpublic.inpublic import bugfree_login
from proj_sample.testcases.inpublic.inpublic import *
from proj_sample.lib.input_resume import zhaopin_read_excel


class ZhaoPin(unittest.TestCase):
    # def setUp(self):
    #     self.driver = webdriver.Firefox()
    #     self.driver.implicitly_wait(30)
    #     self.base_url = "http://test.zhaopin.oa.com/"
    #     self.verificationErrors = []
    #     self.accept_next_alert = True
    #     driver = self.driver
    #     driver.get(
    #         self.base_url + "ResumePlus/ResumeInputOffline/ResumeInput")
    #     driver.find_element_by_id("txtLoginName").clear()
    #     driver.find_element_by_id("txtLoginName").send_keys("kals")
    #     driver.find_element_by_id("txtPassword").clear()
    #     driver.find_element_by_id("txtPassword").send_keys("1")
    #     driver.find_element_by_id("ibnLogin").click()
    def setUp(self):
        self.driver = webdriver.Chrome(chrome_driver)
        self.driver.implicitly_wait(30)
        #self.base_url = "test.zhaopin.oa.com"
        #self.url="test.zhaopin.oa.com/ResumePlus/ResumeInputOffline/ResumeInput"
        self.url ="http://passtest.oa.com/modules/passport/signin.ashx?title" \
                  "=Resume&url=http%3a%2f%2ftest.zhaopin.oa.com%2fResumePlus%2fL" \
                  "ogin%3fReturnUrl%3d%252fResumePlus%252fResumeInputOffline%252fResumeInput"
        #driver.get(self.base_url + "/bugfree/index.php/site/login")
        #open_url(self.driver, self.base_url + "/ResumePlus/ResumeInputOffline/ResumeInput")
        open_url(self.driver, self.url)
        self.driver.implicitly_wait(30)
        zhaopin_login(self.driver,"kals","123456")

        self.data_dict = zhaopin_read_excel(os.getcwd() + "/data/login_account.xlsx")

    def test_zhaopin001(self):
        """开始录入简历"""
        driver = self.driver
        data = xlrd.open_workbook(os.getcwd() + "/data/login_account.xlsx")
        sheet = data.sheets()[0]
        nrows = sheet.nrows
        for i in range(nrows):
            if i == 0:
                continue
            firstName, gender, telPhone, email, lastSchoolName, topDegree, channelParent, channel= self.data_dict[i]
            driver.find_element_by_link_text(u"录入面试简历").click()
            time.sleep(3)
            # driver.find_element_by_name("firstName").clear()
            # driver.find_element_by_name("firstName").send_keys(u"朱香香01")
            clear_element_by_name_with_send_keys(driver,"firstName",firstName)
            if gender==u"女":
                driver.find_element_by_xpath(#性别选择
                    "//div[@id='TLFrightlayer']/div[2]/form/div[2]/table/tbody/tr/td[4]/span[2]").click()
            else:
                driver.find_element_by_xpath(  # 性别选择
                    "//div[@id='TLFrightlayer']/div[2]/form/div[2]/table/tbody/tr/td[4]/span[1]").click()
            # driver.find_element_by_xpath(  # 性别选择
            #     "//div[@id='TLFrightlayer']/div[2]/form/div[2]/table/tbody/tr/td[4]/span[2]").click()
            # driver.find_element_by_name("telPhone").clear()
            # driver.find_element_by_name("telPhone").send_keys("15855210161")
            clear_element_by_name_with_send_keys(driver, "telPhone", telPhone)
            # driver.find_element_by_name("email").clear()
            # driver.find_element_by_name("email").send_keys("15244874761@qq.com")
            clear_element_by_name_with_send_keys(driver, "email", email)
            # driver.find_element_by_name("lastSchoolName").clear()
            # driver.find_element_by_name("lastSchoolName").send_keys(u"深圳大学")
            clear_element_by_name_with_send_keys(driver, "lastSchoolName", lastSchoolName)
            Select(driver.find_element_by_name("topDegreeID")).select_by_visible_text(topDegree)
            Select(driver.find_element_by_name("channelParent")).select_by_visible_text(channelParent)
            Select(driver.find_element_by_name("channel")).select_by_visible_text(channel)
            driver.find_element_by_css_selector("button.hrc-tag-button").click()
            time.sleep(3)
            driver.find_element_by_xpath(".//*[@id='hrcboxClose']").click()
            time.sleep(3)

    def tearDown(self):

        #time.sleep(3)
        self.driver.quit()