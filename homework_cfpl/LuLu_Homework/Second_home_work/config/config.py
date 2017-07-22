#!/user/bin/env python
#encoding:utf-8

#程序配置变量设置
import time
class  Varies(object):

    chrome_path=r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe'
    ie_path=r"C:\Program Files\Internet Explorer\IEDriverServer.exe"
    base_url="http://localhost/bugfree/index.php/bug/list/1"
    save_path=r"C:\Users\Administrator\Desktop\%s.png" % time.strftime("%Y-%m-%d %H-%M-%S")