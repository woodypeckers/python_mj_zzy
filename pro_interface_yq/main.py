#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import unittest
from HTMLTestRunner import HTMLTestRunner
from testcases.weather import WeatherTest
from lib.Logger import Logger
import logging

def suites():
    suite=unittest.TestSuite()
    loader=unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(WeatherTest))
    #suite.addTests(loader.loadTestsFromTestCase(BugfreeImportFile))
    # suite.addTests(loader.loadTestsFromTestCase(ProductAdd))
    #suite.addTests(loader.loadTestsFromTestCase(LoginLogoutTest))
    return suite


if __name__ == "__main__":
    logger = Logger(loglevel=logging.ERROR).getlog()
    logger.info('日志开始')

    try:
        suite = suites()
        fp = open('./reports/results_%s.html' % time.strftime("%Y-%m-%d %H-%M-%S"), 'wb')
        runner = HTMLTestRunner(
            stream=fp,
            title=u'接口测试报告',
            description=u"测试用例执行情况：")
        runner.run(suite)
    except Exception, e:
        raise e
    finally:
        fp.close()
    logging.info('日志结束')
