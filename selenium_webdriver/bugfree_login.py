# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

def testSomething():
    assert True

class BugLoginLogout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print "setUpClas is called."

    def tearDown(self):
        self.driver.quit()

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
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
        if not driver.find_element_by_id("LoginForm_rememberMe").is_selected():
            driver.find_element_by_id("LoginForm_rememberMe").click()
        if driver.find_element_by_id("LoginForm_rememberMe").is_selected():
            driver.find_element_by_id("LoginForm_rememberMe").click()
        driver.find_element_by_id("SubmitLoginBTN").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*BugFree[\s\S]*$")

    def test_new_bug(self):
        driver = self.driver
        driver.get(self.base_url + "/bugfree/index.php/info/edit?type=bug&action=opened&product_id=1")
        time.sleep(3)

    def test_assert_new_bug(self):
        driver = self.driver
        driver.get(self.base_url + "/bugfree/index.php/info/edit?type=bug&action=opened&product_id=1")
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        print "tearDownClas is called."

if __name__ == "__main__":
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    #suite.addTest(unittest.FunctionTestCase(testSomething))
    suite.addTest(BugLoginLogout('test_assert_new_bug'))
    unittest.TextTestRunner(verbosity=2).run(suite)