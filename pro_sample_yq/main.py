#!/usr/bin/env python
# encoding:utf-8
# author:mj
import time
import unittest
import HTMLTestRunner3
# from HTMLTestRunner import HTMLTestRunner
from testcases.ProductManagement import ProductManagement
from testcases.bugfree_import.bugfree_import import BugfreeImport
from testcases.bugfree_login_logout.login_logout import Login_logout_parameter
from testcases.login_logout1111 import Login_logout_parameter1
from lib.Logger import Logger
import logging


def suites():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    # suite.addTests(loader.loadTestsFromTestCase(ProductManagement))
    suite.addTests(loader.loadTestsFromTestCase(Login_logout_parameter1))
    # suite.addTests(loader.loadTestsFromTestCase(BugfreeImport))
    return suite


    # suite = suites()
    # # fp = open("./reports/results_%s.html" % time.strftime("%Y-%m-%d %H:%M:%S"), 'wb')
    # fp = open("./reports/results_%s.html" % time.strftime("%Y-%m-%d %H-%M-%S"), 'wb')
    # runner = HTMLTestRunner(
    #     stream=fp,
    #     title=u"BugFree的测试报告",
    #     description=u"测试用例执行情况：")
    # runner.run(suite)
if __name__ == '__main__':
    logger = Logger(loglevel=logging.INFO).getlog()
    logger.info(u'日志开始')

    try:
        suite = suites()
        fp = open('./reports/results_%s.html' % time.strftime("%Y-%m-%d %H-%M-%S"), 'wb')
        #%H:%M:%S 会报错
        # fp = open('./reports/results_%s.html' % time.strftime("%Y-%m-%d %H:%M:%S"), 'wb')
        runner = HTMLTestRunner3.HTMLTestRunner(
            stream=fp,
            title=u"xxx测试报告",
            description=u"测试用例执行情况：")
        runner.run(suite)
    except Exception as e:

        raise e
    finally:
        fp.close()

    logging.info(u'日志结束')
