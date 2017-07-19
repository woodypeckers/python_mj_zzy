#!/usr/bin/env python
# encoding:utf-8
# author:mj
import time
import unittest
from HTMLTestRunner import HTMLTestRunner
from testcases.ProductManagement import ProductManagement
from testcases.bugfree_import.bugfree_import import BugfreeImport
from testcases.bugfree_login_logout.login_logout import Login_logout_parameter
def suites():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    # suite.addTests(loader.loadTestsFromTestCase(ProductManagement))
    suite.addTests(loader.loadTestsFromTestCase(Login_logout_parameter))
    # suite.addTests(loader.loadTestsFromTestCase(BugfreeImport))
    return suite

if __name__ == '__main__':
    suite = suites()
    # fp = open("./reports/results_%s.html" % time.strftime("%Y-%m-%d %H:%M:%S"), 'wb')
    fp = open("./reports/results_%s.html" % time.strftime("%Y-%m-%d %H-%M-%S"), 'wb')
    runner_test = HTMLTestRunner(
        stream=fp,
        title=u"BugFree的测试报告",
        description=u"测试用例执行情况：")
    runner_test.run(suite)
