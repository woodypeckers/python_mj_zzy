# -*- coding: utf-8 -*-
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
#parseaddr 解析地址 接受地址， formataddr 格式地址,这里指发送地址


def format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def send_eamil():
    smtp_driver = u"smtp.163.com"  #邮箱服务器
    from_addr = u"zhangzhanyong88@163.com"   #发件人
    password = u"zhang001"  # 163设置的第三方授权码"
    to_addr = u"zhangzhanyong88@163.com" #收件人
    test_res =u"test_result_2017-07-12 20-15-14.html" #内容

    # fp = open(test_res,'r')  #原来的读写方式
    # data = fp.read()
    # fp.close()

    with open(test_res) as fp:
        data_html = fp.read()  # 把文本内容一次性读入内存
        msg = MIMEText(data_html,'utf-8','html')
        msg["From"]=format_addr(u'发件人昵称 <%s>'% from_addr)
        msg["To"]= format_addr(u'开发昵称 <%s>' % to_addr)
        # msg['To'] = _format_addr(u'开发人员 <%s>' % to_addr)
        msg['Subject']=Header(u'自动化测试报告2017-07-12','utf-8').encode()

    server = smtplib.SMTP(smtp_driver)#通过smtp协议调用邮箱服务器
    server.set_debuglevel(1) #调试等级
    server.login(from_addr, password)
    server.sendmail(from_addr,[to_addr],msg.as_string())
    server.quit()
    print "sent ok!!!"

if __name__ == "__main__":
    send_eamil()