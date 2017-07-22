#!/user/bin/env python
#encoding:utf-8

import  unittest
from  config.config  import  Varies
from  testcases.bugfree_login_logout import BugfreeLoginLogout
import  time,os,selenium

class BugfreeBug(Varies,BugfreeLoginLogout):

    #自定义显示截屏保存
    def  test_bugfree_1(self):
        self.driver.find_element_by_id("CustomSetLink").click()
        screenshot=self.driver.get_screenshot_as_file(self.save_path)
        self.assertTrue(True,screenshot)
        self.driver.find_element_by_xpath(".//*[@id='CustomSetTable']/tbody/tr[2]/td/input[1]").click()


    def test_bugfree_2(self):

        #“+，-”图标操作
        driver=self.driver
        #driver.find_element_by_xpath(".//*[@id='SearchConditionRow0']/td[7]/a/img").click()
        driver.find_element_by_css_selector('a[class="add_search_button"]').click()
        time.sleep(3)
        driver.find_element_by_css_selector('a[class="cancel_search_button"]').click()
        time.sleep(3)


    # def test_bugfree_3(self):
    #
    #     #bug导出  有问题，文本前的按钮怎么定位
    #     fp=selenium.webdriver.FireFoxProfile()
    #     fp.set_perference("accessibility.tabfocus",2)
    #     driver=selenium.webdriver.FireFox(file_profile=fp)
    #     self.driver.get(self.base_url)
    #     self.driver.find_element_by_link_text("导出").click()
    #     time.sleep(3)
    #     os.system("export.exe")
    #     time.sleep(3)


    def test_bugfree_4(self):

        #导入
        self.driver.find_element_by_link_text(u"导入").click()
        self.driver.find_element_by_xpath(".//*[@id='casefilename']").click()
        current_dir=os.getcwd()
        os.system("%s/tools/import.exe" %current_dir)
        time.sleep(3)
        self.driver.find_element_by_id("uploadbutton").click()
        time.sleep(3)













