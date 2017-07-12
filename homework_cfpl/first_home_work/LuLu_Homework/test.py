#!/user/bin/env python
#encoding:utf-8

#__auth__=='__wanjl__'

import unittest
from selenium import webdriver
import time
from HTMLTestRunner import HTMLTestRunner
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import  random
import win32gui
import  win32api

class TestCase1(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.url = "http://localhost/bugfree"
        #time.sleep(2)
        self.driver.get(self.url+"/index.php/site/login")
        self.driver.find_element_by_id("LoginForm_username").clear()
        self.driver.find_element_by_id("LoginForm_username").send_keys("admin")
        self.driver.find_element_by_id("LoginForm_password").clear()
        self.driver.find_element_by_id("LoginForm_password").send_keys("123456")
        self.driver.find_element_by_id("LoginForm_rememberMe").click()
        #self.driver.find_element_by_class_name("loginbutton btn").click()
        #self.driver.find_element_by_css_selector(".loginbutton btn").click()
        self.driver.find_element_by_id("SubmitLoginBTN").click()

    def test_bugfree_bug1(self):
        #截屏保存
        driver=self.driver
        #driver.switch_to.window(driver.window_handles[0])
        driver.find_element_by_link_text("自定义显示").click()
        driver.get_screenshot_as_file(r"D:\pythoncode\pycharm\201707080800\1.jpg")
        driver.find_element_by_xpath(".//*[@id='CustomSetTable']/tbody/tr[2]/td/input[1]").click()


    def test_bugfree_bug2(self):
        #下拉框多项选择
        driver = self.driver
        driver.find_element_by_link_text("Case").click()
        Select(driver.find_element_by_id("BugFreeQuery_andor1")).select_by_visible_text(u"或者")
        self.driver.find_element_by_id("SaveQuery").click()
        #这里有个问题：send_keys写死会弹出window窗口是否报错修改
        self.driver.find_element_by_id("dialogQueryTitle").send_keys("test_",random.randint(1,99))
        time.sleep(2)
        self.driver.find_element_by_name("yt0").click()
        driver.close()
    #
    def test_bugfree_bug3(self):
        #"+","-"图标操作
        driver=self.driver
        driver.find_element_by_xpath(".//*[@id='SearchConditionRow0']/td[7]/a/img").click()
        time.sleep(2)
        driver.find_element_by_xpath(".//*[@id='SearchConditionRow1']/td[7]/a[2]/img").click()


    def tearDown(self):
        self.driver.quit()

class TestCase2(TestCase1):

    def test_bugfree_bug1(self):
         #页面前进后退刷新
         driver=self.driver
         #driver.find_element_by_id("SearchResultDiv").click()    跳不过去，为什么？
         driver.find_element_by_link_text("Result").click()
         time.sleep(2)
         driver.back()
         time.sleep(2)
         driver.forward()
         time.sleep(2)
         driver.refresh()
         time.sleep(2)
         driver.find_element_by_link_text(u"退出").click()


    # def  test_bug_free_bug2(self):
    #     result  导出   windows的弹出窗怎么处理？
    #     self.driver.close()
    #     self.fp=webdriver.FirefoxProfile()
    #     self.fp.set_preference('browser.download.dir','D:\\')
    #     self.fp.set_preference("browser.download.FolderList",2)
    #     self.fp.set_preference("browser.download.manager.ShowWhenStarting",False)
    #     self.fp.set_preference("browser.helpApps.neverAsk.saveToDisk","application/x-xml")
    #
    #     self.driver = webdriver.Firefox(firefox_profile=self.fp)
    #     driver = self.driver
    #     driver.get('http://localhost/bugfree/index.php/bug/list/1')
    #     self.driver.find_element_by_id("LoginForm_username").clear()
    #     self.driver.find_element_by_id("LoginForm_username").send_keys("admin")
    #     self.driver.find_element_by_id("LoginForm_password").clear()
    #     self.driver.find_element_by_id("LoginForm_password").send_keys("123456")
    #     self.driver.find_element_by_id("LoginForm_rememberMe").click()
    #     self.driver.find_element_by_id("SubmitLoginBTN").click()
    #     self.driver.find_element_by_xpath(".//*[@id='searchresult-grid']/div[1]/a[2]").click()
    #     print win32gui.FindWindow(u"正在打开",None)

    def test_bugfree_bug2(self):
        #取消弹出框
        driver=self.driver
        #driver.find_element_by_xpath(".//*[@id='searchresult-grid']/div[1]/a[3]").click()
        driver.find_element_by_link_text(u"导入").click()
        #driver.implicitly_wait(3)
        driver.find_element_by_id("uploadbutton").click()
        time.sleep(3)
        driver.switch_to.alert.dismiss()
        time.sleep(3)


    def test_bugfree_bug3(self):

        #操作cookies
        driver=self.driver
        driver.add_cookie({"name":"test1","value":"1111"})
        for a in driver.get_cookies():
            print  u"名称 is %s,内容 is  %s " %(a['name'],a['value'])
        driver.close()


class TestCase3(TestCase1):

    def test_bugfree_bug1(self):
        #接受弹出框
        driver=self.driver
        #driver.find_element_by_xpath(".//*[@id='searchresult-grid']/div[1]/a[3]").click()
        driver.find_element_by_link_text(u"导入").click()
        #driver.implicitly_wait(3)
        driver.find_element_by_id("uploadbutton").click()
        time.sleep(3)
        driver.switch_to.alert.accept()
        time.sleep(3)


    def test_bugfree_bug2(self):
        #窗口切换
        driver=self.driver
        driver.find_element_by_link_text(u"后台管理").click()
        driver.switch_to.window(driver.window_handles[1])
        #driver.implicitly_wait(3)   这种隐式等待时间不明显  为什么？
        time.sleep(3)
        driver.close()

    def  test_bugfree_bug3(self):
        #换IE浏览器
        self.driver = webdriver.Ie(executable_path=u'C:\Program Files\Internet Explorer\IEDriverServer.exe')
        driver = self.driver
        driver.get("http://localhost/bugfree/index.php/case/list/1")
        driver.find_element_by_id("LoginForm_username").clear()
        driver.find_element_by_id("LoginForm_username").send_keys("admin")
        driver.find_element_by_id("LoginForm_password").clear()
        driver.find_element_by_id("LoginForm_password").send_keys("123456")
        self.driver.find_element_by_id("SubmitLoginBTN").click()



if __name__ == "__main__":

    #unittest.main()
    suits=unittest.TestSuite()
    loader=unittest.TestLoader()
    suits.addTests(loader.loadTestsFromTestCase(TestCase1))
    suits.addTests(loader.loadTestsFromTestCase(TestCase2))
    suits.addTests(loader.loadTestsFromTestCase(TestCase3))
    # #fp = open(r'D:\pythoncode\pycharm\201707080800\test_result_%s.html' % time.strftime("%Y-%m-%d %H-%M-%S"), 'wb')
    # #runner = HTMLTestRunner(stream=fp,
    #                         #title=u'bugfree测试报告',
    #                         #description=u"测试用例执行情况：")
    # #runner.run(suits)
    unittest.TextTestRunner(verbosity=2).run(suits)









