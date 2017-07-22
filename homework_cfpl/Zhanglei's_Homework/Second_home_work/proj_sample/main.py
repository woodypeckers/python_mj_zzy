#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: zhanglei
import time
import unittest
from HTMLTestRunner import HTMLTestRunner
from testcases.bugfree_product.bugfreeproduct import BugfreeProduct
from proj_sample.testcases.bugfree_product.bugfree_import_file import BugfreeImportFile
from testcases.zhaopin.zhaopin_input_resume import ZhaoPin


def suites():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    #suite.addTests(loader.loadTestsFromTestCase(BugfreeProduct))
    # suite.addTests(loader.loadTestsFromTestCase(BugfreeImportFile))
    suite.addTests(loader.loadTestsFromTestCase(ZhaoPin))
    return suite


if __name__ == "__main__":
    # # unittest.main()
    # suite = unittest.TestSuite()  # 创建一个测试套
    # loader = unittest.TestLoader()  # 创建一个加载器
    # suite.addTests(loader.loadTestsFromTestCase(BugfreeProduct))  # 把类中所有的用例加载后添加到测试套中
    suite=suites()
    fp = open('./reports/test_result_%s.html' % time.strftime("%Y-%m-%d %H-%M-%S"), 'wb')  # 生成测试报告，固定用法
    runner = HTMLTestRunner(stream=fp,
                            title=u'测试报告',
                            description=u"测试用例执行情况：")
    runner.run(suite)
    fp.close()