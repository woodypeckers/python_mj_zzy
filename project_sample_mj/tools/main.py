#!/usr/bin/env python
# encoding:utf-8
# author:mj
import time, unittest
from HTMLTestRunner import HTMLTestRunner



def suites():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase())
    return suite

if __name__ == '__main__':
    suite = suites()
    fp = open("./reports/results_s" % time.strftime("%Y-%m-%d %H-%M-%S"), 'wb')
    runner_test = HTMLTestRunner(
        stream=fp,
        title=u"BugFree的测试报告",
        description=u"测试用例执行情况：")
    runner_test.run(suite)