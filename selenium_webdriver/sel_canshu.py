#coding=utf-8
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

    def test_bf_yhgl(self):
        user_name = [u'乘风破浪zzy05', u'乘风破浪zl', u'乘风破浪lulu']
        real_name = ['zzy05', 'zl', 'lulu']
        # for (user_name_instance, real_name_instance) in (user_name, real_name):
        """此写法错误"""
        for user_name_instance in user_name:
            for real_name_instance in real_name:
                driver = self.driver
                time.sleep(2)
                driver.find_element_by_xpath(".//*[@id='top']/div[3]/a[2]").click()
                driver.switch_to.window(driver.window_handles[1])
                driver.find_element_by_id("user_management").click()
                driver.find_element_by_link_text(u"添加用户").click()
                time.sleep(2)
                Select(driver.find_element_by_class_name("required")).select_by_value("internal")
                time.sleep(2)
                driver.find_element_by_id("TestUser_username").clear()
                driver.find_element_by_id("TestUser_username").send_keys(user_name_instance)
                driver.find_element_by_id("TestUser_realname").send_keys(real_name_instance)
                driver.find_element_by_id("TestUser_password").clear()
                driver.find_element_by_id("TestUser_password").send_keys("123456")
                driver.find_element_by_id("TestUser_email").clear()
                driver.find_element_by_id("TestUser_email").send_keys("11@11.com")
                driver.find_element_by_name("yt0").click()
                time.sleep(2)
                driver.refresh()
                driver.close()

                # driver.find_element_by_link_text(u"禁用").click()
                # driver.switch_to.alert.dismiss()
                # driver.get_screenshot_as_file(r"C:\\cap\\bugfree_yhgl06.jpg")
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
