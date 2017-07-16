# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from HTMLTestRunner import HTMLTestRunner
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
class Bf_Htai(unittest.TestCase):
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
    
    def test_bf_htai_glrzlog(self):
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

    def test_bf_htai_xtsz(self):
        driver = self.driver
        driver.get(self.base_url + "/bugfree/index.php/bug/list/1")
        driver.find_element_by_link_text(u"后台管理").click()
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_link_text(u"系统设置").click()
        driver.find_element_by_link_text(u"编辑").click()
        driver.find_element_by_id("TestOption_option_value").clear()
        driver.find_element_by_id("TestOption_option_value").send_keys("12")
        driver.find_element_by_name("yt0").click()
        driver.find_element_by_link_text(u"修改者").click()
        driver.find_element_by_id("name").clear()
        driver.find_element_by_id("name").send_keys("2")
        driver.find_element_by_css_selector("input.btn").click()
        driver.get_screenshot_as_file(r"C:\\cap\\bugfree_xtsz05.jpg")

    def test_bf_yhgl(self):
        driver = self.driver
        time.sleep(2)
        driver.find_element_by_xpath(".//*[@id='top']/div[3]/a[2]").click()
        driver.switch_to.window(driver.window_handles[1])
        # driver.find_elements_by_xpath(".//*[@id='user_management']/a").click()
        driver.find_element_by_id("user_management").click()
        driver.find_element_by_link_text(u"添加用户").click()
        # Select(driver.find_element_by_id("TestUser_authmode")).select_by_visible_text(u"内部帐号")
        time.sleep(2)
        # Select(driver.find_element_by_id("TestUser_authmode")).select_by_value("internal")
        # driver.find_element_by_class_name("required").find_elements_by_tag_name("option")[1].click()
        Select(driver.find_element_by_class_name("required")).select_by_value("internal")
        time.sleep(2)
        driver.find_element_by_id("TestUser_username").clear()
        driver.find_element_by_id("TestUser_username").send_keys("user_b")
        driver.find_element_by_id("TestUser_realname").send_keys("b")
        driver.find_element_by_id("TestUser_password").clear()
        driver.find_element_by_id("TestUser_password").send_keys("123456")
        driver.find_element_by_id("TestUser_email").clear()
        driver.find_element_by_id("TestUser_email").send_keys("11@11.com")
        driver.find_element_by_name("yt0").click()
        driver.find_element_by_link_text(u"禁用").click()
        driver.get_screenshot_as_file(r"C:\\cap\\bugfree_yhgl06.jpg")
        # self.assertEqual(u"确定进行此操作？", self.close_alert_and_get_its_text())

if __name__ == "__main__":
    suit = unittest.TestSuite()
    loader = unittest.TestLoader()
    suit.addTests(loader.loadTestsFromTestCase(Bf_Htai))

    fp = open("./test_result_%s.html"% time.strftime("%Y-%m-%d %H-%M-%S"),'wb')
    runner = HTMLTestRunner(
        stream=fp,
        title=u'百度搜索测试报告',
        description=u"测试用例执行情况：")
    runner.run(suit)
    fp.close()
