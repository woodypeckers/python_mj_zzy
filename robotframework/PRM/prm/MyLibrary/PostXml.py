#-*- coding:utf8 -*-
import urllib2
import httplib
import socket
import xml.etree.ElementTree as et
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger

def post_interface_xml(url):
    '''
       input: request xmlstr
       output: response str
       往模拟器发送接口码流。返回PRM IODD的返回码，如果没有返回码，则返回555555
    '''
    #xmlstr = open(fileName, 'r+').read()#.replace('"GBK"?>','"utf-8"?>').decode('GBK').encode('utf-8')
    #读取内存中的变量${interface_xml_content}
    builtin = BuiltIn()
    xml_str = builtin.get_variable_value('${interface_xml_content}') 
    
    headers = {"Content-Type":"xml/text",   
                "Accept":"xml/text",
                "Connection":"Keep-Alive",
                "Content-Length":"%s" % len(xml_str)}
    urlsplit = urllib2.urlparse.urlsplit(url)
    netloc = urlsplit.netloc
    path = urlsplit.path
    if path =='':
        path = '/'
    conn = httplib.HTTPConnection(netloc)
    try:
        conn.request("POST", path, body=xml_str, headers=headers)
    except socket.error:
        print '*ERROR* socket error, url无法到达!  please check url!'
        #raise SocketError
    response = conn.getresponse()
 
    resp_str =  response.read(response.msg.getheader('content-length'))
    logger.trace(u'HTTP response.status: %s' % response.status)
    logger.trace(u'HTTP repsonse.reason: %s' % response.reason)
    logger.trace(u'HTTP repsonse.header: %s' % response.getheaders())

    encode_resp_str = resp_str
    try:
        et.fromstring(resp_str.replace('"GBK"?>','"utf-8"?>').decode('GBK','ignore').encode('utf-8'))
    except Exception:
        try:
            encode_resp_str = resp_str.decode('utf-8')
        except Exception:
            try:
                encode_resp_str = resp_str.decode('cp936')
            except Exception:
                pass
            pass
        logger.warn(u'收到的返回包为非法的xml串，具体内容如下：【%s】' % encode_resp_str)
    
    logger.trace(u'HTTP repsonse.Body: %s' % resp_str.decode('cp936'))
    #如果返回的content不为空，则返回content中的返回码，否则返回555555
    if len(resp_str) != 0:
        resActivityCode = get_rsp_activity_code(resp_str)
        if resActivityCode == '110016':
            #信用积分同步
            resCode = get_head_rsp_code(resp_str)
            return resCode
        elif resActivityCode == '110011':
            #发布结算单
            resCode = get_head_rsp_code(resp_str)
            return resCode
        elif resActivityCode == '110009':
            #合同同步
            resCode = get_head_rsp_code(resp_str)
            return resCode            
        else:
            resCode = get_head_rsp_code(resp_str)
            return resCode
    else:
        logger.warn(u'由于返回包内容为空，根据约定，直接返回555555')
        return '555555'

def post_xml_file(fileName, url):
    '''
       input: request xmlstr
       output: response str
    '''
    xmlstr = open(fileName, 'r+').read()#.replace('"GBK"?>','"utf-8"?>').decode('GBK').encode('utf-8')
    
    headers = {"Content-Type":"xml/text",   
                "Accept":"xml/text",
                "Connection":"Keep-Alive",
                "Content-Length":"%s" % len(xmlstr)}
    urlsplit = urllib2.urlparse.urlsplit(url)
    netloc = urlsplit.netloc
    path = urlsplit.path
    if path =='':
        path = '/'
    conn = httplib.HTTPConnection(netloc)
    try:
        conn.request("POST", path, body=xmlstr, headers=headers)
    except socket.error:
        print '*ERROR* socket error, url无法到达!  please check url!'
        #raise SocketError
    response = conn.getresponse()
    resp_str =  response.read(response.msg.getheader('content-length'))
    status = get_head_rsp_code(resp_str)
    return status

def get_head_rsp_code(xmlstr):
    #获取返回码
    xml_str = xmlstr.replace('"GBK"?>','"utf-8"?>').decode('GBK','ignore').encode('utf-8')
        
    root = et.fromstring(xml_str)
    parentNode = root.findall('Header')
    for node in parentNode:
        resCode = node.find('RspCode').text

    return resCode
    
def get_body_rsp_code(xmlstr):
    #获取返回码
    xml_str = xmlstr.replace('"GBK"?>','"utf-8"?>').decode('GBK','ignore').encode('utf-8')
        
    root = et.fromstring(xml_str)
    body = root.find('Body')
    dealresult = body.find('DealResult')
    resCode = dealresult.find('ErrorCode').text
    return resCode
    
def get_rsp_activity_code(xmlstr):
    #获取返回码
    xml_str = xmlstr.replace('"GBK"?>','"utf-8"?>').decode('GBK','ignore').encode('utf-8')
        
    root = et.fromstring(xml_str)
    parentNode = root.findall('Header')
    for node in parentNode:
        resCode = node.find('ActivityCode').text

    return resCode
    
#if __name__=="__main__":
    #post_xml("abc", "http://10.1.3.252:10000/dist")
    #post_interface_xml("aaa", "http://10.1.26.39:9002")