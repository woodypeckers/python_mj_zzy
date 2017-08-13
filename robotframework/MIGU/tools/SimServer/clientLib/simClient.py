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

clcr = '\r\n'
def simReqPkg(ip, validTime, msgType, request, response, delay=0, custom_header, verifyMode,respMode):
    reqPkg = '<?xml version="1.0" encoding="UTF-8" ?><message>' + clcr
    reqPkg += '<hostIp>' + ip + '</hostIp>' + clcr
    reqPkg += '<validTime>' + validTime + '</validTime>' + clcr
    reqPkg += '<msgType>' + msgType + '</msgType>' + clcr
    reqPkg += '<delay>' + str(delay) + '</delay>' + clcr
    
    if custom_header not in [None,'','{}']:
        reqPkg += u'<custom_header>'
        reqPkg += dictToXml(custom_header)
        reqPkg += u'</custom_header>'
        
    if verifyMode in [None, '']:
        verifyMode = 'NORMAL'
    
    if respMode in [None, '']:
        respMode = 'NORMAL'
        
    reqPkg += '<request verifyMode="'+ respMode + '">' + clcr
    
    if verifyMode == 'NOCHECK':
        pass
    elif verifyMode =='NORMAL':        
        reqPkg += dictToXml(request)
    elif verifyMode == 'XPATH':
        reqPkg += dictToXpath(request)
        
    reqPkg += '</request>' + clcr
    
    reqPkg += '<response respMode="' + respMode + '">' + clcr
    reqPkg += dictToXml(response)
    reqPkg += '</response>' + clcr
    
    reqPkg += '</message>' + clcr

    return reqPkg.decode('utf8')

def dictToXml(dictStr):
    xmlStr = ''
    dictObj = eval(dictStr)
    for (k,v) in dictObj.items():
                
        if not isinstance(v, unicode):
            v = unicode(v,'utf-8')
            
        xmlStr += u'<' + k + u'>' + v + u'</' + k + u'>'  + clcr
    
    return xmlStr

def dictToXpath(dictStr):
    xmlStr = '<xpathList>'+ clcr
    dictObj = eval(dictStr)
    for (k, v) in dictObj.items():
        xmlStr += '<xpath>'+ clcr
        if not isinstance(v, unicode):
            v = unicode(v,'utf-8')
        
        xmlStr += '<path>' + k + '</path>' + clcr
        xmlStr += '<expValue>' + v + '</expValue>' + + clcr
    

if __name__=="__main__":    
    ip = '10.1.25.61'
    timeout = '10'
    msgType = '/ismp/boss/OI_PrepayOrReleasePayOrder'
    request = u'{"UserID":"1","MobNum":"15012880633","VirtulUserID":"","OrderNo":"20150617172054397283","PayMode":"01","CommodityID":"王绵杰","PayType":"01","PayNum":"100","Unit":"01","BusiCode":"OI_PrepayOrReleasePayOrder"}'
    response = u'{"code": "0000"}'
        
    req = simReqPkg(ip, timeout, msgType, request, response, 65)
    print type(req)
