import time
from appium import webdriver

# dict 规定要运行的参数信息
capabilities_config_5 = {
    "platformName": "Android",
    "platformVersion": "5",
    "deviceName": "android",
    "appPackage": "com.android.calculator2",
    "appActivity": ".Calculator",
    #"app": r"F:\aa.apk",
    "newCommandTimeout": 600,
    "unicodeKeyboard": True,  # 测试过程中如果输入中文，要设置
    "resetKeyboard": True
}
# 设置Appium Server的地址
server_url = "http://127.0.0.1:4723/wd/hub"

# 新建一个session连接
driver = webdriver.Remote(command_executor=server_url,
                          desired_capabilities=capabilities_config_5)

# 接下来，都是定位，或者是操作，获取元素的值
# 点击按钮1
driver.find_element_by_id("com.android.calculator2:id/digit_1").click()
time.sleep(2)
# 点击+号
driver.find_element_by_accessibility_id("加").click()
time.sleep(2)
# 点击 2
driver.find_element_by_xpath("//android.widget.Button[@text=2]").click()
time.sleep(2)
# 点击=号
driver.find_element_by_accessibility_id("等于").click()
time.sleep(3)

result = driver.find_element_by_xpath(
    "//*[@resource-id='com.android.calculator2:id/display']/android.widget.EditText").text
assert result == '3'
driver.quit()