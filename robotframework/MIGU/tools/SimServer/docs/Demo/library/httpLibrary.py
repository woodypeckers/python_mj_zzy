# -*- coding: utf-8 -*-

'''
Created on 2015-6-12

@author: wangmianjie
'''

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
import httplib 
import socket
import urllib


class HttpRepsonseHeaderError(RuntimeError):
    '''
    如果HTTP返回不是200，则出此错
    出此错后，案例继续进行
   '''
    #ROBOT_EXIT_ON_FAILURE = True
    ROBOT_CONTINUE_ON_FAILURE = True
    
class SocketError(RuntimeError):
    '''
    URL无法访问，一般是端口未监听
   '''
    #ROBOT_EXIT_ON_FAILURE = True
    ROBOT_CONTINUE_ON_FAILURE = True
    
class ResponseNoContentLengthError(RuntimeError):
    ROBOT_CONTINUE_ON_FAILURE = True

class ResponseNoExpactedKeyValueError(RuntimeError):
    ROBOT_CONTINUE_ON_FAILURE = True

def http_post(url,data):
    logger.info(data)
    logger.info(type(data))
    data = data.encode('UTF-8')
    
    urlsplit = httplib.urlsplit(url)    
    path = urlsplit.path
    logger.info('path:%s' %  path)
    
    if path =='':
        path = '/'
    conn = httplib.HTTPConnection(urlsplit.hostname, urlsplit.port)
    
    headers = {"Content-Type":"application/xml",   
               "Accept":"application/xml",
               "Connection":"Keep-Alive",
               "Content-Length":"%s" % len(data)}
        
    try:
        #logger.info('Send message is:\n%s' % data)
        logger.info('path:%s' % path)
        #encode_data = urllib.urlencode(data)
        conn.request(method="POST", url=str(path), body=data, headers=headers)
    except socket.error:
        logger.info(u'*ERROR* socket error, url不可访问!  please check url!')
        raise SocketError
    
    response = conn.getresponse()
    if response.status != 200: 
        logger.info('*ERROR* Http  status: %s' %  response.status ,also_console=True)
        conn.close()
        raise HttpRepsonseHeaderError
    else:
        
        if response.msg.getheader('content-length'):
            rspStr =  response.read(response.msg.getheader('content-length'))
            logger.info('Receive response is:\n%s' % rspStr)
        else:
            logger.info('response no header: "content-length"')
            raise ResponseNoContentLengthError
        conn.close()
        return rspStr
#####其他一些小功能
def addHttpCustomHeader(keyvalue):
    '''典型的例子是keyvalue串: content-type=text/xml; charset=UTF-8
    目标是将其放入缺省的dict变量&{http_custom_headers}这个字典中去
    return: None
    '''
    builtin = BuiltIn().get_library_instance('BuiltIn')
    custom_headers_dict = builtin.get_variable_value('${http_custom_headers_obj}')
    if custom_headers_dict in [None,'']:
        custom_headers_dict = {}
    logger.info('org ${http_custom_headers_obj}: %s ' % custom_headers_dict)
    [key,value] = str(keyvalue).split('=',1)
    if not custom_headers_dict.has_key(key):
        custom_headers_dict.setdefault(key,value)
    else:
        custom_headers_dict[key] = value
    builtin.set_test_variable('${http_custom_headers_obj}', custom_headers_dict)
    logger.info('modified ${http_custom_headers_obj}: %s ' % custom_headers_dict)
    return 
    
    
def getBaseUrlByUrl(url):
    urlsplit = httplib.urlsplit(url)    
    sheme = urlsplit.scheme
    netloc = urlsplit.netloc
    baseurl = '%s://%s' % (sheme,netloc)
    return baseurl

def getHostByUrl(url):
    urlsplit = httplib.urlsplit(url)    
    netloc = urlsplit.netloc
    return netloc

def getUriByUrl(url):
    urlsplit = httplib.urlsplit(url)    
    path = urlsplit.path
    return path    

# data = '''<?xml version="1.0" encoding="UTF-8" ?>
# <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sch="http://www.monternet.com/ismp/schemas">
#    <soapenv:Header>
#       <sch:TransactionID>?</sch:TransactionID>
#    </soapenv:Header>
# <soapenv:Body>
# <sch:SynUserInfoReq>
# <MsgType>SynUserInfoReq</MsgType>
# <TransactionID></TransactionID>
# <Versio>1.0.0</Version>
# <Send_Address>
#     <DeviceType>100</DeviceType>
#     <DeviceID>1111</DeviceID>
# </Send_Address>
# <Send_Address>
#     <DeviceType>0</DeviceType>
#     <DeviceID>0</DeviceID>
# </Dest_Address>
# <OprCode>01</OprCode>
# <RegDate>20150612143000</RegDate>
# <User_Info>
#     <LoginName>wmj000001</LoginName>
#     <LoginPassword>wmj000001</LoginPassword>
#     <Msisdn>13600000000</Msisdn>
#     <Email>13600000000@139.com</Email>
#     <QQ></QQ>
#     <UserType>01</UserType>
#     <NickName></NickName>
#     <Name></Name>
#     <PayPassword></PayPassword>
#     <ContactAddress></ContactAddress>
#     <CertificateType></CertificateType>
#     <CertificateNo></CertificateNo>
#     <MailAddress></MailAddress>
#     <PostCode></PostCode>
#     <UserLevel></UserLevel>
#     <UserRegion></UserRegion>       
# </User_Info>
# <sch:SynUserInfoReq>
# '''
# url = 'http://10.1.5.80:8989/ws'
# # url = 'http://10.1.4.220:1990/ws'
# 
# my_post = http_post(url,data)
