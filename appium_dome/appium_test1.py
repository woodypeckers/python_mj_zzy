#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：mj

import time
from appium import webdriver
# dict 规定要运行的参数信息
capabilities_config_5={"platformName":"Android",
                       "platformVersion":"5",
                       "deviceName":"emulator-5554",
                       "appPackage":"com.android.calculator2",
                       "appActivity":".Calculator",
                       "newCommandTimeout":600,
                       "unicodeKeyboard": True,
                       "resetKeyboard": True
                       }

# 设置Appium Server的地址
server_url = "http://127.0.0.1:4723/wd/hub"

# 新建一个session连接
driver = webdriver.Remote(command_executor=server_url,desired_capabilities=capabilities_config_5)
time.sleep(3)
# 接下来，都是定位，或者是操作，获取元素的值
driver.find_element_by_id("com.android.calculator2:id/digit_1").click()
time.sleep(2)
driver.find_element_by_id("com.android.calculator2:id/op_add").click()
time.sleep(2)
driver.find_element_by_xpath("//android.widget.Button[@text=2]").click()
# driver.find_element_by_xpath("//android.widget.Button[@text=2]").click()
time.sleep()
driver.find_element_by_accessibility_id("等于").click()
driver.quit()