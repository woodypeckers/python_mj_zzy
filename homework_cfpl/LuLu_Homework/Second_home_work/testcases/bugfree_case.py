#!/user/bin/env python
#encoding:utf-8


import  unittest
from  bugfree_login_logout import BugfreeLoginLogout
import  time
class BugfreeCase(BugfreeLoginLogout):

    def test_bugfree_1(self):
        #操作cookites
        print self.driver.get_cookies()
        self.driver.add_cookie({"name":"zhangsan","value":"this is a test"})
        cookier=self.driver.get_cookies()
        #a是list
        for a  in cookier:
            print "name is  %s,text  is %s" %(a['name'],a['value'])
        #检查是否插入成功
        self.assertTrue("this is a test",cookier[1])
        self.assertTrue("zhangsan",cookier[0])


    def test_bugfree_2(self):
        #窗口切换
        self.driver.find_element_by_link_text("统计报表").click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(3)
        self.driver.close()
        time.sleep(3)


    def  test_bugfree_3(self):
        #页面前进，后退，刷新
        self.driver.find_element_by_link_text("Case").click()
        self.driver.back()
        time.sleep(3)
        self.driver.forward()
        time.sleep(3)
        self.driver.refresh()
        time.sleep(3)

    def  test_bugfree_4(self):

        #接受弹出窗
        self.driver.find_element_by_xpath(".//*[@id='case']/a").click()
        self.driver.find_element_by_link_text("批量运行").click()
        time.sleep(3)
        self.driver.switch_to.alert.accept()
        time.sleep(3)

