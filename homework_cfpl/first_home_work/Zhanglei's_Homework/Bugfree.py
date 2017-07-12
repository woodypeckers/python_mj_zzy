# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from HTMLTestRunner import HTMLTestRunner
import unittest, time, re

class Bugfree(unittest.TestCase):
    """Bugfree登录"""
    def setUp(self):
        #self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome(executable_path = r'C:\Users\v_leiizhang\AppData\Local\Google\Chrome\Application\chromedriver.exe')
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost"
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.get(self.base_url + "/bugfree/index.php/site/login")
        # Warning: assertTextPresent may require manual changes
        #self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*记住密码[\s\S]*$")
        driver.find_element_by_id("LoginForm_username").clear()
        driver.find_element_by_id("LoginForm_username").send_keys("admin")
        driver.find_element_by_id("LoginForm_password").clear()
        driver.find_element_by_id("LoginForm_password").send_keys("123456")
        driver.find_element_by_id("LoginForm_rememberMe").click()
        driver.find_element_by_id("LoginForm_rememberMe").click()
        driver.find_element_by_id("SubmitLoginBTN").click()

    def test_bugfree_test001(self):
        """Bugfree新建Bug"""
        driver = self.driver
        driver.find_element_by_link_text(u" 新建 Bug   ").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectWindow | 新建Bug | ]]
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_id("BugInfoView_title").clear()
        driver.find_element_by_id("BugInfoView_title").send_keys("test001")
        Sample_Product = driver.find_element_by_name('layer1_module')
        Sample_Product.find_element_by_xpath(".//option[@value='0']").click()
        driver.find_element_by_id("BugInfoView_assign_to_name").click()
        driver.find_element_by_css_selector("li.ac_even").click()
        Select(driver.find_element_by_id("BugInfoView_severity")).select_by_visible_text("2")
        Select(driver.find_element_by_id("BugInfoView_priority")).select_by_visible_text("2")
        Select(driver.find_element_by_id("Custom_BugType")).select_by_visible_text(u"新增需求")
        Select(driver.find_element_by_id("Custom_HowFound")).select_by_visible_text(u"单元测试")
        Select(driver.find_element_by_id("Custom_BugOS")).select_by_visible_text("Windows 7")
        driver.find_element_by_id("Custom_OpenedBuild").clear()
        driver.find_element_by_id("Custom_OpenedBuild").send_keys("001")
        driver.find_element_by_name("yt0").click()
        time.sleep(3)
        driver.close()

    def test_bugfree_test002(self):
        """后台管理冒烟测试"""
        driver = self.driver
        driver.get(self.base_url + "/bugfree/index.php/bug/list/1")
        driver.find_element_by_link_text(u"后台管理").click()
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_link_text(u"系统设置").click()
        driver.find_element_by_id("name").clear()
        driver.find_element_by_id("name").send_keys("db_version")
        driver.find_element_by_css_selector("input.btn").click()
        driver.find_element_by_link_text(u"管理日志").click()
        Select(driver.find_element_by_id("target_table")).select_by_visible_text(u"产品管理")
        driver.find_element_by_css_selector("input.btn").click()
        driver.find_element_by_xpath(u"//input[@value='重置查询']").click()
        driver.find_element_by_link_text(u"用户日志").click()
        driver.find_element_by_link_text(u"下一页").click()
        driver.find_element_by_link_text(u"下一页").click()
        time.sleep(3)
        driver.close()

    def test_bugfree_test003(self):
        """新增用户"""
        driver = self.driver
        driver.get(self.base_url + "/bugfree/index.php/bug/list/1")
        driver.find_element_by_link_text(u"后台管理").click()
        driver.switch_to.window(driver.window_handles[1]) ##切换窗口
        driver.find_element_by_link_text(u"用户管理").click()
        driver.find_element_by_link_text(u"添加用户").click()
        #aa=driver.find_element_by_xpath(".//*[@id='test-user-form']/div[1]/label")
        #aa.find_element_by_(u"登录验证")
        #aa.verifyTable(u"登录验证")
        Select(driver.find_element_by_id("TestUser_authmode")).select_by_visible_text(u"内部帐号")
        driver.find_element_by_id("TestUser_username").clear()
        driver.find_element_by_id("TestUser_username").send_keys("Jim")
        driver.find_element_by_id("TestUser_realname").clear()
        driver.find_element_by_id("TestUser_realname").send_keys(u"张磊")
        driver.find_element_by_id("TestUser_password").clear()
        driver.find_element_by_id("TestUser_password").send_keys("123456")
        driver.find_element_by_id("TestUser_email").clear()
        #driver.find_element_by_id("TestUser_email").send_keys("123456@qq.com")
        driver.find_element_by_xpath(".//*[@id='TestUser_email']").send_keys("234567@qq.com")
        driver.find_element_by_name("yt0").click()#点击按钮，保存
        driver.get_screenshot_as_file(r"F:\Learn_by_self\0708\pic_1.jpg")
        time.sleep(3) #等待3秒
        driver.close() #关闭窗口
    def test_bugfree_test004(self):
        """日志查询"""
        driver = self.driver
        driver.get(self.base_url + "/bugfree/index.php/bug/list/1")
        driver.find_element_by_link_text(u"后台管理").click()
        driver.switch_to.window(driver.window_handles[1])  ##切换窗口
        driver.find_element_by_link_text(u"管理日志").click()
        Select(driver.find_element_by_id("target_table")).select_by_visible_text(u"产品管理")
        driver.find_element_by_id("name").clear()
        driver.find_element_by_id("name").send_keys("3")
        #driver.find_element_by_css_selector("input.btn").click()
        driver.find_element_by_xpath(u"//input[@value='提交查询']").click()
        driver.find_element_by_xpath(u"//input[@value='重置查询']").click()
        Select(driver.find_element_by_id("target_table")).select_by_visible_text(u"产品管理")
        driver.find_element_by_id("name").clear()
        driver.find_element_by_id("name").send_keys("6")
        driver.find_element_by_css_selector("input.btn").click()
        driver.find_element_by_xpath(u"//input[@value='重置查询']").click()
        time.sleep(3)  # 等待3秒
        driver.close()  # 关闭窗口
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
    suite.addTests(loader.loadTestsFromTestCase(Bugfree))#把类中所有的用例加载后添加到测试套中

    fp = open('./test_result_%s.html' % time.strftime("%Y-%m-%d %H-%M-%S"), 'wb')#生成测试报告，固定用法
    runner = HTMLTestRunner(stream=fp,
                            title=u'chrome浏览器测试报告',
                            description=u"测试用例执行情况：")
    runner.run(suite)
    fp.close()
