# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from HTMLTestRunner import HTMLTestRunner
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Bf_Ht(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.base_url = "http://localhost"
        driver = self.driver
        driver.get(self.base_url + "/bugfree/index.php/site/login")
        self.assertEqual(u"登录 - BugFree", driver.title)
        # assertTitle登录 - BugFree
        driver.find_element_by_id("LoginForm_username").clear()
        driver.find_element_by_id("LoginForm_username").send_keys("admin")
        driver.find_element_by_id("LoginForm_password").clear()
        driver.find_element_by_id("LoginForm_password").send_keys("123456")
        Select(driver.find_element_by_id("LoginForm_language")).select_by_value("en")
        Select(driver.find_element_by_id("LoginForm_language")).select_by_value("zh_cn")
        driver.find_element_by_id("SubmitLoginBTN").click()

    def tearDown(self):
        self.driver.quit()

    def test_bf_bj_wdxx(self):
        driver = self.driver
        time.sleep(2)
        driver.find_element_by_class_name("user-info").click()
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        # driver.find_element_by_partial_link_text(u"编辑我的信息")
        driver.find_element_by_class_name("margin-left-190")
        driver.back()#后退
        time.sleep(2)
        driver.forward()#前进
        driver.find_element_by_id("TestUser_email").clear()
        driver.find_element_by_id("TestUser_email").send_keys("11@11.com")
        driver.find_element_by_id("change_password").click()
        driver.find_element_by_id("TestUser_password_old").clear()
        driver.find_element_by_id("TestUser_password_old").send_keys("123456")
        driver.find_element_by_id("TestUser_password").clear()
        driver.find_element_by_id("TestUser_password").send_keys("123456")
        driver.find_element_by_id("TestUser_password_repeat").clear()
        driver.find_element_by_id("TestUser_password_repeat").send_keys("123456")
        driver.find_element_by_name("yt0").click()
        driver.get_screenshot_as_file(r"C:\\cap\\bugfree_wdxx01.jpg")

    def test_bf_cp_xz01(self):
        driver = self.driver
        time.sleep(2)
        driver.find_element_by_xpath(".//*[@id='top']/div[3]/a[2]").click()
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_link_text(u"添加产品").click()
        driver.find_element_by_id("Product_name").clear()
        driver.find_element_by_id("Product_name").send_keys(u"乘风破浪")
        driver.find_element_by_id("Product_display_order").clear()
        driver.find_element_by_id("Product_display_order").send_keys("001")
        driver.find_element_by_id("Product[group_name][]").click()
        driver.find_element_by_name("Product[group_name][]").click()
        driver.find_element_by_name("Product[group_name][]").click()
        driver.find_element_by_css_selector("label.hover").click()
        driver.find_element_by_name("Product[group_name][]").click()
        driver.find_element_by_xpath("//form[@id='product-form']/div[5]/label").click()
        driver.find_element_by_id("Product_bug_severity").clear()
        driver.find_element_by_id("Product_bug_severity").send_keys("1,2,3,4")
        driver.find_element_by_id("Product_bug_priority").clear()
        driver.find_element_by_id("Product_bug_priority").send_keys("1,2,3,4")
        driver.find_element_by_id("Product_case_priority").clear()
        driver.find_element_by_id("Product_case_priority").send_keys("1,2,3,4")
        driver.find_element_by_name("yt0").click()
        driver.find_element_by_xpath(u"(//a[contains(text(),'编辑')])[2]").click()
        driver.find_element_by_xpath("(//a[contains(text(),'Bug')])[2]").click()
        driver.find_element_by_link_text(u"添加新字段").click()
        driver.find_element_by_id("FieldConfig_field_name").clear()
        driver.find_element_by_id("FieldConfig_field_name").send_keys("omg")
        Select(driver.find_element_by_id("FieldConfig_field_type")).select_by_visible_text(u"单选下拉框")
        driver.find_element_by_id("FieldConfig_field_value").clear()
        driver.find_element_by_id("FieldConfig_field_value").send_keys("1")
        driver.find_element_by_id("FieldConfig_default_value").clear()
        driver.find_element_by_id("FieldConfig_default_value").send_keys("1")
        driver.find_element_by_id("FieldConfig_is_required").click()
        driver.find_element_by_id("FieldConfig_field_label").clear()
        driver.find_element_by_id("FieldConfig_field_label").send_keys("1")
        driver.find_element_by_id("FieldConfig_is_required").click()
        Select(driver.find_element_by_id("FieldConfig_belong_group")).select_by_visible_text(u"其它信息")
        driver.find_element_by_name("yt0").click()
        driver.find_element_by_id("FieldConfig_display_order").clear()
        driver.find_element_by_id("FieldConfig_display_order").send_keys("1")
        driver.find_element_by_name("yt0").click()
        driver.find_element_by_xpath("//a[@id='FieldConfig[editable_action_name][]']/span").click()
        driver.find_element_by_name("FieldConfig[editable_action_name][]").click()
        driver.find_element_by_name("FieldConfig[editable_action_name][]").click()
        driver.find_element_by_css_selector("label.hover > input[name=\"FieldConfig[editable_action_name][]\"]").click()
        driver.find_element_by_xpath("//form[@id='field-config-form']/div[12]").click()
        driver.find_element_by_name("yt0").click()
        driver.get_screenshot_as_file(r"C:\\cap\\bugfree_xz02.jpg")



    def test_bf_cp_xz02(self):
        driver = self.driver
        time.sleep(2)
        driver.find_element_by_xpath(".//*[@id='top']/div[3]/a[2]").click()
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_xpath(".//*[@id='SearchResultDiv']/table/tbody/tr[2]/td[6]/a[4]").click()
        driver.find_element_by_id("ProductModule_name").send_keys(u"乘风破浪的子模块")
        # Select(driver.find_element_by_id("ProductModule_add_owner_name")).select_by_visible_text(u"系统管理员")
        driver.find_element_by_id("ProductModule_display_order").send_keys("2")
        driver.find_element_by_class_name("margin-left-190").click()
        driver.refresh()#刷新
        time.sleep(2)
        driver.find_element_by_id("ztree_product_module_tree_2_span").click()
        driver.find_element_by_xpath(".//*[@id='edit']/input[7]").click()
        driver.get_screenshot_as_file(r"C:\\cap\\bugfree_xz03.jpg")
        time.sleep(3)
        driver.switch_to.alert.accept() #接受弹出框


if __name__ == "__main__":
    suit = unittest.TestSuite()
    loader = unittest.SkipTest()
    suit.addTests(loader.loadTestsFromTestCase(Bf_Ht))

    fp = open("./test_result_%s.html"% time.strftime("%Y-%m-%d %H-%M-%S"),'wb')
    runner = HTMLTestRunner(
        stream=fp,
        title=u'百度搜索测试报告',
        description=u"测试用例执行情况：")

    runner.run(suit)
    fp.close()
