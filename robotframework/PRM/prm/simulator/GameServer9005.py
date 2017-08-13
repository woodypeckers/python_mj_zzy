#-*- coding:utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import string
import json
import urllib
import xml.etree.ElementTree as et
from lxml import etree
import time

#定义一个全局变量
#CU = 1

class PostHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Parse the form data posted
        raw_post_data = ''
        if self.headers.dict.has_key("content-length"):
            content_length = string.atoi(self.headers.dict["content-length"])
            raw_post_data = self.rfile.read(content_length)
        else:
            raw_post_data = self.rfile.read()
        
        #模拟器收到的码流需要转码
        if raw_post_data.find('<') == -1:
            xml_str = open(raw_post_data, 'r+').read().replace('"GBK"?>','"utf-8"?>').decode('GBK').encode('utf-8')
        else:
            xml_str = raw_post_data.replace('"GBK"?>','"utf-8"?>').decode('GBK').encode('utf-8')
        
        #获取Header节点和Body节点
        root = et.fromstring(xml_str)
        headerNode = root.findall('Header')
        
        for hnode in headerNode:
            activityCode = hnode.find('ActivityCode').text  #接口类型编码
            reqDateTime = hnode.find('ReqDateTime').text    #消息接收时间
            reqTransID = hnode.find('ReqTransID').text  #消息ID
            sign = hnode.find('Sign').text #sign
        
        #判断接口类型
        if activityCode == u'113801':
            return_msg ='''<?xml version='1.0' encoding='GBK'?><Msg><Header><Version>0001</Version><TestFlag>0</TestFlag><ActivityCode>113801</ActivityCode><ReqSys>2001</ReqSys><ReqDateTime>'''+reqDateTime+'''</ReqDateTime><ReqTransID>'''+reqTransID+'''</ReqTransID><ActionCode>1</ActionCode><Sign>'''+sign+'''</Sign><RcvSys>03801</RcvSys><RcvDateTime>'''+reqDateTime+'''</RcvDateTime><RcvTransID>'''+reqTransID+'''</RcvTransID><RspCode>000000</RspCode><RspDesc>成功</RspDesc></Header></Msg>'''
        
        if activityCode == u'113804':
            return_msg ='''<?xml version='1.0' encoding='GBK'?><Msg><Header><Version>0001</Version><TestFlag>0</TestFlag><ActivityCode>113804</ActivityCode><ReqSys>2001</ReqSys><ReqDateTime>'''+reqDateTime+'''</ReqDateTime><ReqTransID>'''+reqTransID+'''</ReqTransID><ActionCode>1</ActionCode><Sign>'''+sign+'''</Sign><RcvSys>03801</RcvSys><RcvDateTime>'''+reqDateTime+'''</RcvDateTime><RcvTransID>'''+reqTransID+'''</RcvTransID><RspCode>000000</RspCode><RspDesc>成功</RspDesc></Header></Msg>''' 
        
        content = return_msg#.decode('utf-8').encode('GBK')
        # 发送应答包
        response = "HTTP/1.0 200 OK\r\n"
        response += "Content-Type: application/json;charset=utf-8\r\n"
        response += "Content-Length: " + str(len(content)) + "\r\n"
        response += "\r\n"
        response += content           
        self.wfile.write(response)    
        return

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('0.0.0.0', 9005), PostHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
