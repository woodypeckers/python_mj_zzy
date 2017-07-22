#!/user/bin/env python
#coding=utf-8
#__auth__=="__wanjl__"


import unittest
from testcases.bugfree_login_logout import BugfreeLoginLogout
from testcases.bugfree_bug import BugfreeBug
from testcases.bugfree_case import BugfreeCase
from testcases.bugfree_result import BugfreeResult


def main():

    suits=unittest.TestSuite()
    loader=unittest.TestLoader()
    # suits.addTests(loader.loadTestsFromTestCase(BugfreeBug))
    # suits.addTests(loader.loadTestsFromTestCase(BugfreeCase))
    suits.addTests(loader.loadTestsFromTestCase(BugfreeResult))

    unittest.TextTestRunner(verbosity=2).run(suits)



if __name__=="__main__":
    main()



