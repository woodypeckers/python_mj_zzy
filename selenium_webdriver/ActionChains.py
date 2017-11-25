#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：mj
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# 要使用鼠标操作，首先需要引入ActionChains包
from selenium.webdriver.common.action_chains import ActionChains
import time

# 1、鼠标右键操作
driver = webdriver.Ie()
driver.get("http://www.mxvpnjsq.cc/member.php?mod=logging&action=login")
# 输入用户名、密码，回车登陆
driver.find_element_by_name("username").send_keys("1290800466")
driver.find_element_by_name("username").send_keys(Keys.TAB)
driver.find_element_by_name("password").send_keys("15866584957")
driver.find_element_by_name("password").send_keys(Keys.ENTER)
time.sleep(5)
# 定位到要右击的元素
qqq = driver.find_element_by_id("mn_Nfb8a")
# 对定位到的元素执行鼠标右键操作
ActionChains(driver).context_click(qqq).perform()
time.sleep(3)
# 按 下 键，进入右键菜单第一个选项
driver.find_element_by_id("mn_Nfb8a").send_keys(Keys.DOWN)
# 直接按回车或单击进入
# driver.find_element_by_id("mn_Nfb8a").send_keys(Keys.ENTER)
# 鼠标单击操作
driver.find_element_by_id("mn_Nfb8a").click()
time.sleep(3)  # 休眠3秒
driver.close()

# 2、鼠标双击操作
driver = webdriver.Ie()
driver.get("http://www.mxvpnjsq.cc/space-uid-269119.html")
# 定位到要双击的元素
qqq = driver.find_element_by_id("spacename")
# 对定位到的元素执行鼠标双击操作
ActionChains(driver).double_click(qqq).perform()
time.sleep(3)  # 休眠3秒
driver.close()

# 3、鼠标拖放操作
driver = webdriver.Ie()
driver.get("http://www.mxvpnjsq.cc/space-uid-269119.html")
time.sleep(5)
# 定位元素的原位置
element = driver.find_element_by_id("domainurl")
# 定位元素要移动到的目标位置
target = driver.find_element_by_id("a_poke_269119")
# 执行元素的移动操作
ActionChains(driver).drag_and_drop(element, target).perform()
# 鼠标拖放过程详解：首先是鼠标点击并按住element元素，然后执行鼠标移动动作，
# 移动到 target 元素位置或者是 (xOffset, yOffset) 位置，再执行鼠标的释放动作
# 如上所示的目标位置既可以用某一元素位置表示，也可用坐标表示
time.sleep(5)  # 休眠3秒

driver.quit()

"""ActionChains 类鼠标操作的常用方法：
context_click() 右击
double_click() 双击
drag_and_drop() 拖动
move_to_element() 鼠标悬停在一个元素上
click_and_hold() 按下鼠标左键在一个元素上"""