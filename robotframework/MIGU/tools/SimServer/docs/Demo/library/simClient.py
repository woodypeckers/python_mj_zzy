# -*- coding: utf-8 -*-

'''
Created on 2015-6-17

@author: wangmianjie
'''

''' 
 模拟器调用函数
参数说明：
ip：                     被测系统ip，请求消息验证时的参数
timeout: 超时时间, 从模拟器接收到调用请求后， 超过该时间没有介绍大被测系统请求认为超时
request： 模板请求参数
response： 模板应答参数
delay:     模拟器返回应答的延迟时间,默认值为0
'''
from robot.api import logger

clcr = u'\r\n'
def simReqPkg(ip, validTime, msgType, request, response, delay, custom_header, verifyMode, respMode):
    reqPkg = u'<?xml version="1.0" encoding="UTF-8" ?><message>' + clcr
    reqPkg += u'<hostIp>' + ip + u'</hostIp>' + clcr
    reqPkg += u'<validTime>' + validTime + u'</validTime>' + clcr
    reqPkg += u'<msgType>' + msgType + u'</msgType>' + clcr
    reqPkg += u'<delay>' + str(delay) + u'</delay>' + clcr
    
    if custom_header not in [None,'','{}']:
        reqPkg += u'<custom_header>'
        reqPkg += dictToXml(custom_header)
        reqPkg += u'</custom_header>'
        
    if verifyMode in [None, '']:
        verifyMode = 'NORMAL'
    
    if respMode in [None, '']:
        respMode = 'NORMAL'
        
    reqPkg += u'<request verifyMode="'+ verifyMode + '">' + clcr
    
    if verifyMode == 'NOCHECK':
        pass
    elif verifyMode =='NORMAL':        
        reqPkg += dictToXml(request)
    elif verifyMode == 'XPATH':
        reqPkg += dictToXpath(request)
        
    reqPkg += u'</request>' + clcr
    
    reqPkg += u'<response respMode="' + respMode + '">' + clcr
    reqPkg += dictToXml(response)
    reqPkg += u'</response>' + clcr
    
    reqPkg += u'</message>' + clcr
    return reqPkg

def dictToXml(dictStr):
    xmlStr = ''
    logger.info(dictStr)
    dictObj = eval(dictStr)
    #logger.info('type(dictObj):%s' % type(dictObj))
    #logger.info(dictObj)
    #cpName = dictObj['cpName']
    #logger.info('%s:%s' % (cpName, type(cpName)))
    for (k,v) in dictObj.items():
        try:
            k = k.decode('UTF-8')
            v = v.decode('UTF-8')
        except:
            pass
        xmlStr += u'<' + k + u'>' + v + u'</' + k + u'>'
    return xmlStr


def dictToXpath(dictStr):
    dictObj = eval(dictStr)
    xmlStr = '<xpathList>'+ clcr
    
    for (k, v) in dictObj.items():
        
        try:
            k = k.decode('UTF-8')
            v = v.decode('UTF-8')
        except:
            pass
        xmlStr += '<xpath>'+ clcr
        
        xmlStr += u'<path>' + k + u'</path>' + clcr
        xmlStr += u'<expValue>' + v + u'</expValue>' + clcr
        xmlStr += '</xpath>'+ clcr
    
    xmlStr += '</xpathList>'    
    return xmlStr
    

if __name__=="__main__":    
    ip = '10.1.25.61'
    timeout = '10'
    msgType = '/test/xml/default_utf8' 
    delay = '0'
    validTime = '4'
    custom_header = ''
    verifyMode = 'XPATH'
    respMode = 'NORMAL'
    request = u'{"Request/apkInfo/contentId":"123456789012","Request/apkInfo/contentName":"愤怒的小鸟","Request/apkInfo/cpId":"123456","Request/apkInfo/cpName":"南京市游戏设计有限责任公司"}'
    response = u'{"Infos_returnCode":"0","Info_returnCode":"0"}'
    
        
    req = simReqPkg(ip, validTime, msgType, request, response, delay, custom_header, verifyMode, respMode)
    print req
