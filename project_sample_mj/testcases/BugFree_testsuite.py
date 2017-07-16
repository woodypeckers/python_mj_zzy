# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from HTMLTestRunner import HTMLTestRunner
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from bussiness_common_steps.bussiness_common_steps import *

class BugFree_Test1(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.base_url = "http://localhost"
        driver = self.driver
        driver.get(self.base_url + "/bugfree/index.php/site/login")
        self.assertEqual(u"登录 - BugFree", driver.title)
        driver.BugfreeClass(self.driver, "admin", "123456")

    def tearDown(self):
        self.driver.quit()
    
    def test_bf_houtai01(self):
        driver = self.driver
        driver.get(self.base_url + "/bugfree/index.php/adminAction/index")
        Select(driver.find_element_by_id("target_table")).select_by_visible_text(u"自定义字段")
        time.sleep(2)
        Select(driver.find_element_by_id("target_table")).select_by_visible_text(u"产品管理")
        time.sleep(2)
        driver.find_element_by_id("name").clear()
        driver.find_element_by_id("name").send_keys("123")
        driver.find_element_by_css_selector("input.btn").click()
        time.sleep(2)
        Select(driver.find_element_by_id("pageSize")).select_by_visible_text("35")
        # Select(driver.find_element_by_id("pageSize")).deselect_by_index(2)
        time.sleep(2)
        driver.find_element_by_xpath(u"//input[@value='重置查询']").click()
        driver.get_screenshot_as_file(r"C:\\cap\\bugfree_glrzlog04.jpg")
    #
    # def test_bf_houtai02(self):
    #     driver = self.driver
    #     driver.get(self.base_url + "/bugfree/index.php/bug/list/1")
    #     driver.find_element_by_link_text(u"后台管理").click()
    #     driver.switch_to.window(driver.window_handles[1])
    #     driver.find_element_by_link_text(u"系统设置").click()
    #     driver.find_element_by_link_text(u"编辑").click()
    #     driver.find_element_by_id("TestOption_option_value").clear()
    #     driver.find_element_by_id("TestOption_option_value").send_keys("12")
    #     driver.find_element_by_name("yt0").click()
    #     driver.find_element_by_link_text(u"修改者").click()
    #     driver.find_element_by_id("name").clear()
    #     driver.find_element_by_id("name").send_keys("2")
    #     driver.find_element_by_css_selector("input.btn").click()
    #     driver.get_screenshot_as_file(r"C:\\cap\\bugfree_xtsz05.jpg")
    #
    # def test_bf_houtai03(self):
    #     driver = self.driver
    #     time.sleep(2)
    #     driver.find_element_by_xpath(".//*[@id='top']/div[3]/a[2]").click()
    #     driver.switch_to.window(driver.window_handles[1])
    #     # driver.find_elements_by_xpath(".//*[@id='user_management']/a").click()
    #     driver.find_element_by_id("user_management").click()
    #     driver.find_element_by_link_text(u"添加用户").click()
    #     # Select(driver.find_element_by_id("TestUser_authmode")).select_by_visible_text(u"内部帐号")
    #     time.sleep(2)
    #     # Select(driver.find_element_by_id("TestUser_authmode")).select_by_value("internal")
    #     # driver.find_element_by_class_name("required").find_elements_by_tag_name("option")[1].click()
    #     Select(driver.find_element_by_class_name("required")).select_by_value("internal")
    #     time.sleep(2)
    #     driver.find_element_by_id("TestUser_username").clear()
    #     driver.find_element_by_id("TestUser_username").send_keys("user_b")
    #     driver.find_element_by_id("TestUser_realname").send_keys("b")
    #     driver.find_element_by_id("TestUser_password").clear()
    #     driver.find_element_by_id("TestUser_password").send_keys("123456")
    #     driver.find_element_by_id("TestUser_email").clear()
    #     driver.find_element_by_id("TestUser_email").send_keys("11@11.com")
    #     driver.find_element_by_name("yt0").click()
    #     driver.find_element_by_link_text(u"禁用").click()
    #     driver.get_screenshot_as_file(r"C:\\cap\\bugfree_yhgl06.jpg")
    #     self.assertEqual(u"确定进行此操作？", self.close_alert_and_get_its_text())


# class BugFree_Test2(BugFree_Test1):
#
#     def test_bf_kz01(self):
#         driver = self.driver
#         driver.find_element_by_xpath(".//*[@id='top']/div[3]/a[2]").click()
#         driver.switch_to.window(driver.window_handles[1])
#         driver.find_element_by_xpath(".//*[@id='group_management']/a").click()
#         driver.find_element_by_xpath("html/body/div[1]/div[2]/div[2]/form/a").click()
#         driver.find_element_by_class_name("row").send_keys(u"乘风破浪小队")
#         time.sleep(2)
#         driver.find_element_by_class_name("row").send_keys(Keys.BACK_SPACE * 2)
#         driver.back()
#         time.sleep(2)
#         driver.forward()
#         driver.close()
#
#     def test_bf_kz02(self):
#         driver = self.driver
#         driver.find_element_by_xpath(".//*[@id='name']").send_keys("abc")
#         driver.find_element_by_xpath("html/body/div[1]/div[2]/div[2]/form/input[3]").click()
#         Select(driver.find_element_by_id("pageSize")).select_by_visible_text("20")
#         driver.close()
#
#     @staticmethod
#     def test_baidu_kz03(self):
#         values = [u"论测试的重要性与背锅侠", u"浪里个浪啦啦啦", u"嗷嗷嗷叫~~~"]
#         for i in values:
#             driver = self.driver
#             driver.get(self.base_url + "/")
#             driver.find_element_by_link_text(u"新闻").click()
#             driver.find_elements_by_partial_link_text(u"百度新闻搜索")
#             """检查title1：百度新闻搜索——全球最大的中文新闻平台"""
#             driver.find_element_by_id("ww").clear()
#             driver.find_element_by_id("ww").send_keys(i)
#             time.sleep(2)
#             driver.find_element_by_id("ww").send_keys(Keys.BACK_SPACE * 4)
#
#
# class BugFree_Test3(BugFree_Test1):
#     def test_bf_bj_wdxx(self):
#         driver = self.driver
#         time.sleep(2)
#         driver.find_element_by_class_name("user-info").click()
#         driver.switch_to.window(driver.window_handles[1])
#         time.sleep(2)
#         # driver.find_element_by_partial_link_text(u"编辑我的信息")
#         driver.find_element_by_class_name("margin-left-190")
#         driver.back()#后退
#         time.sleep(2)
#         driver.forward()#前进
#         driver.find_element_by_id("TestUser_email").clear()
#         driver.find_element_by_id("TestUser_email").send_keys("11@11.com")
#         driver.find_element_by_id("change_password").click()
#         driver.find_element_by_id("TestUser_password_old").clear()
#         driver.find_element_by_id("TestUser_password_old").send_keys("123456")
#         driver.find_element_by_id("TestUser_password").clear()
#         driver.find_element_by_id("TestUser_password").send_keys("123456")
#         driver.find_element_by_id("TestUser_password_repeat").clear()
#         driver.find_element_by_id("TestUser_password_repeat").send_keys("123456")
#         driver.find_element_by_name("yt0").click()
#         driver.get_screenshot_as_file(r"C:\\cap\\bugfree_wdxx01.jpg")
#
#     def test_bf_cp_xz01(self):
#         driver = self.driver
#         time.sleep(2)
#         driver.find_element_by_xpath(".//*[@id='top']/div[3]/a[2]").click()
#         driver.switch_to.window(driver.window_handles[1])
#         driver.find_element_by_link_text(u"添加产品").click()
#         driver.find_element_by_id("Product_name").clear()
#         driver.find_element_by_id("Product_name").send_keys(u"乘风破浪")
#         driver.find_element_by_id("Product_display_order").clear()
#         driver.find_element_by_id("Product_display_order").send_keys("001")
#         driver.find_element_by_id("Product[group_name][]").click()
#         driver.find_element_by_name("Product[group_name][]").click()
#         driver.find_element_by_name("Product[group_name][]").click()
#         driver.find_element_by_css_selector("label.hover").click()
#         driver.find_element_by_name("Product[group_name][]").click()
#         driver.find_element_by_xpath("//form[@id='product-form']/div[5]/label").click()
#         driver.find_element_by_id("Product_bug_severity").clear()
#         driver.find_element_by_id("Product_bug_severity").send_keys("1,2,3,4")
#         driver.find_element_by_id("Product_bug_priority").clear()
#         driver.find_element_by_id("Product_bug_priority").send_keys("1,2,3,4")
#         driver.find_element_by_id("Product_case_priority").clear()
#         driver.find_element_by_id("Product_case_priority").send_keys("1,2,3,4")
#         driver.find_element_by_name("yt0").click()
#         driver.find_element_by_xpath(u"(//a[contains(text(),'编辑')])[2]").click()
#         driver.find_element_by_xpath("(//a[contains(text(),'Bug')])[2]").click()
#         driver.find_element_by_link_text(u"添加新字段").click()
#         driver.find_element_by_id("FieldConfig_field_name").clear()
#         driver.find_element_by_id("FieldConfig_field_name").send_keys("omg")
#         Select(driver.find_element_by_id("FieldConfig_field_type")).select_by_visible_text(u"单选下拉框")
#         driver.find_element_by_id("FieldConfig_field_value").clear()
#         driver.find_element_by_id("FieldConfig_field_value").send_keys("1")
#         driver.find_element_by_id("FieldConfig_default_value").clear()
#         driver.find_element_by_id("FieldConfig_default_value").send_keys("1")
#         driver.find_element_by_id("FieldConfig_is_required").click()
#         driver.find_element_by_id("FieldConfig_field_label").clear()
#         driver.find_element_by_id("FieldConfig_field_label").send_keys("1")
#         driver.find_element_by_id("FieldConfig_is_required").click()
#         Select(driver.find_element_by_id("FieldConfig_belong_group")).select_by_visible_text(u"其它信息")
#         driver.find_element_by_name("yt0").click()
#         driver.find_element_by_id("FieldConfig_display_order").clear()
#         driver.find_element_by_id("FieldConfig_display_order").send_keys("1")
#         driver.find_element_by_name("yt0").click()
#         driver.find_element_by_xpath("//a[@id='FieldConfig[editable_action_name][]']/span").click()
#         driver.find_element_by_name("FieldConfig[editable_action_name][]").click()
#         driver.find_element_by_name("FieldConfig[editable_action_name][]").click()
#         driver.find_element_by_css_selector("label.hover > input[name=\"FieldConfig[editable_action_name][]\"]").click()
#         driver.find_element_by_xpath("//form[@id='field-config-form']/div[12]").click()
#         driver.find_element_by_name("yt0").click()
#         driver.get_screenshot_as_file(r"C:\\cap\\bugfree_xz02.jpg")
#
#     def test_bf_cp_xz02(self):
#         driver = self.driver
#         time.sleep(2)
#         driver.find_element_by_xpath(".//*[@id='top']/div[3]/a[2]").click()
#         driver.switch_to.window(driver.window_handles[1])
#         driver.find_element_by_xpath(".//*[@id='SearchResultDiv']/table/tbody/tr[2]/td[6]/a[4]").click()
#         driver.find_element_by_id("ProductModule_name").send_keys(u"乘风破浪的子模块")
#         # Select(driver.find_element_by_id("ProductModule_add_owner_name")).select_by_visible_text(u"系统管理员")
#         driver.find_element_by_id("ProductModule_display_order").send_keys("2")
#         driver.find_element_by_class_name("margin-left-190").click()
#         driver.refresh()#刷新
#         time.sleep(2)
#         driver.find_element_by_id("ztree_product_module_tree_2_span").click()
#         driver.find_element_by_xpath(".//*[@id='edit']/input[7]").click()
#         driver.get_screenshot_as_file(r"C:\\cap\\bugfree_xz03.jpg")
#         time.sleep(3)
#         driver.switch_to.alert.accept() #接受弹出框
#

if __name__ == "__main__":
    suit = unittest.TestSuite()
    loader = unittest.TestLoader()
    suit.addTests(loader.loadTestsFromTestCase(BugFree_Test1))

    fp = open("./test_result_%s.html"% time.strftime("%Y-%m-%d %H-%M-%S"),'wb')
    runner = HTMLTestRunner(
        stream=fp,
        title=u'百度搜索测试报告',
        description=u"测试用例执行情况：")
    runner.run(suit)
    fp.close()
