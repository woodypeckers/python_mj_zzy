# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from HTMLTestRunner import HTMLTestRunner
import unittest, time, re

class Product(unittest.TestCase):
    """Bugfree登录"""

    def setUp(self):
        self.driver = webdriver.Chrome(
            executable_path=r'C:\Users\v_leiizhang\AppData\Local\Google\Chrome\Application\chromedriver.exe')
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost"
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.get(self.base_url + "/bugfree/index.php/site/login")
        # Warning: assertTextPresent may require manual changes
        # self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*记住密码[\s\S]*$")
        driver.find_element_by_id("LoginForm_username").clear()
        driver.find_element_by_id("LoginForm_username").send_keys("admin")
        driver.find_element_by_id("LoginForm_password").clear()
        driver.find_element_by_id("LoginForm_password").send_keys("123456")
        driver.find_element_by_id("LoginForm_rememberMe").click()
        driver.find_element_by_id("LoginForm_rememberMe").click()
        driver.find_element_by_id("SubmitLoginBTN").click()

    def test_product001(self):
        """新增产品"""
        driver = self.driver
        driver.get(self.base_url + "/bugfree/index.php/bug/list/1")
        driver.find_element_by_link_text(u"后台管理").click()
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_link_text(u"添加产品").click()
        driver.find_element_by_id("Product_name").clear()
        driver.find_element_by_id("Product_name").send_keys("Product2")
        driver.find_element_by_id("Product_display_order").clear()
        driver.find_element_by_id("Product_display_order").send_keys("2")
        #driver.find_element_by_id("Product_product_manager").click()
        # driver.find_element_by_css_selector("li.ac_even").click()
        # driver.find_element_by_css_selector("span").click()
        # driver.find_element_by_name("Product[group_name][]").click()
        # driver.find_element_by_id("Product[group_name][]").click()
        driver.find_element_by_id("Product_bug_severity").clear()
        driver.find_element_by_id("Product_bug_severity").send_keys("1,2,3,4,5")
        driver.find_element_by_id("Product_bug_priority").clear()
        driver.find_element_by_id("Product_bug_priority").send_keys("1,2,3,4,5")
        driver.find_element_by_id("Product_case_priority").clear()
        driver.find_element_by_id("Product_case_priority").send_keys("1,2,3,4,5")
        driver.find_element_by_name("yt0").click()
        time.sleep(3)
        driver.close()
    
    def test_product002(self):
        """编辑产品信息"""
        driver = self.driver
        driver.get(self.base_url + "/bugfree/index.php/bug/list/1")
        driver.find_element_by_link_text(u"后台管理").click()
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_partial_link_text(u"产品管理")#检查跳转的页面部分匹配“产品管理”
        driver.find_element_by_xpath(r".//*[@id='SearchResultDiv']/table/tbody/tr[1]/td[6]/a[1]").click()
        #driver.find_element_by_xpath(u"(//a[contains(text(),'编辑')])[4]").click()
        driver.find_element_by_id("Product_product_manager").click()
        driver.find_element_by_id("Product_display_order").clear()
        driver.find_element_by_id("Product_display_order").send_keys("111")
        driver.find_element_by_id("Product_name").clear()
        driver.find_element_by_id("Product_name").send_keys(u"产品1")
        driver.find_element_by_id("Product_bug_severity").clear()
        driver.find_element_by_id("Product_bug_severity").send_keys("2")
        driver.find_element_by_id("Product_bug_priority").clear()
        driver.find_element_by_id("Product_bug_priority").send_keys("2")
        driver.find_element_by_id("Product_case_priority").clear()
        driver.find_element_by_id("Product_case_priority").send_keys("2")
        driver.find_element_by_name("yt0").click()
        time.sleep(3)
        driver.close()

    def test_product003(self):
        """复制产品信息"""
        driver = self.driver
        driver.get(self.base_url + "/bugfree/index.php/bug/list/1")
        driver.find_element_by_link_text(u"后台管理").click()
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_xpath(r".//*[@id='SearchResultDiv']/table/tbody/tr[1]/td[6]/a[2]").click()
        #driver.switch_to.window(driver.window_handles[2])
        driver.find_element_by_id("Product_name").clear()
        driver.find_element_by_id("Product_name").send_keys(u"产品2")
        driver.find_element_by_id("Product_display_order").clear()
        driver.find_element_by_id("Product_display_order").send_keys("113")
        driver.find_element_by_name("yt0").click()
        time.sleep(3)
        driver.close()
    
    def tearDown(self):
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.find_element_by_link_text(u"退出").click()
        time.sleep(3)
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    #unittest.main()
    suite = unittest.TestSuite() #创建一个测试套
    loader = unittest.TestLoader()#创建一个加载器
    suite.addTests(loader.loadTestsFromTestCase(Product))#把类中所有的用例加载后添加到测试套中

    fp = open('./test_result_%s.html' % time.strftime("%Y-%m-%d %H-%M-%S"), 'wb')#生成测试报告，固定用法
    runner = HTMLTestRunner(stream=fp,
                            title=u'产品管理模块测试报告',
                            description=u"测试用例执行情况：")
    runner.run(suite)
    fp.close()