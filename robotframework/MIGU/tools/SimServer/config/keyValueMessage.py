# -*- coding: utf-8 -*-

'''
Created on 2015-7-4

@author: wangmianjie
'''

from lxml import etree
from gExpectAdmin import *

import logger
from urllib import unquote



class KeyValueMessage():
    
    def __init__(self, path, msgFormat, direction ):
        self.fieldDict = {}
        self.paramDict = {}
        self.replaceParamDict = {}
        self.msgContent = open(path).read()
        self.direction = direction        
        self.msgFormat = msgFormat
                
        self.loadParamList()
    
    '''  加载模板配置  '''    
    def loadParamList(self):
        fields = etree.XML(self.msgContent)
        
        for field in fields:
            tag = field.tag
            text = field.text
            if text == None :
                text = ''
            
            self.fieldDict[tag] = text
            
            if ( text <> ''):
                if text.find('$${') >= 0 and text.find('}$$') > 0 :
                    self.paramDict[tag] = text
                
                '''  应答消息要处理替换参数  '''
                if self.direction == 'rsp':
                    if text.find('##{') >= 0 and text.find('}##') > 0:
                        self.replaceParamDict[tag] = text
    
    '''  将请求消息和模拟器的期望消息比较  '''    
    def reqMsgCompare(self, expMsg, reqMsgStr):
        reqMsgDict = self.parseReqMsg(reqMsgStr.strip() )
        
        verifyMode = expMsg.getVerifyMode()
        
        if verifyMode == 'NOCHECK':
            return True
        elif verifyMode == 'NORMAL' or verifyMode == 'XPATH' : 
            ''' 期望消息参数数量 ''' 
            expParamNum = len(expMsg.reqParamDict)
            ''' 模板中的参数数量 '''
            tmpParamNum = len(self.paramDict )   
            if expParamNum == tmpParamNum: 
                for key in expMsg.reqParamDict :
                    expectValue = expMsg.reqParamDict[key]
                    realValue = unquote(reqMsgDict[key])
                    
                    logger.log( '接收消息字段: "%s" 实际值是: "%s", 期望值是: "%s"' % (key, realValue, expectValue )  )
                    if realValue <> expectValue : 
                        logger.log( '消息比较错误, 实际消息是： %s， 期望消息是：％s' %  (reqMsgStr,  expMsg.msgContent) )
                        return False
    
                logger.log('请求消息匹配成功')
    #             setExpMsgMatchStatus(expMsg)
            else :
                logger.log( '模板中，请求消息的参数个数与期望消息中的参数个数不匹配')
                return False

        return True
            
            
        
    def getRspMsg(self, expMsg, reqMsg):      
        rspMsg = ''  
        if len(self.paramDict) == len(expMsg.rspParamDict) :
            self.procRspParam(expMsg)
            self.procReplaceParam(reqMsg) 
            
            for (k, v) in self.fieldDict.items():
                rspMsg += k + '=' + v + '&'
                
            rspMsg = rspMsg[0:-1]
        return rspMsg
        
    '''  将请求中的要替换的值替换  '''
    def procReplaceParam(self,reqMsg):
        
        reqMsgDict = self.parseReqMsg(reqMsg)
        for paramKey in self.replaceParamDict:
            
            '''  根据参数的tag找到请求消息中对应的值  '''
            self.fieldDict[paramKey] = reqMsgDict[paramKey]
            
        '''  将请求中的要替换的值替换  '''
    def procRspParam(self,expMsg):
        
        for paramKey in self.paramDict:
            
            '''  根据参数的key找到请求消息中对应的值  '''
            self.fieldDict[paramKey] = expMsg.rspParamDict[paramKey]

            
    def parseReqMsg(self, reqMsg):
        reqMsgDict = {}
        
        fieldList = reqMsg.split('&')
        for field in fieldList:
            key = field.split('=')[0]
            value = field.split('=')[1]
            reqMsgDict[key]= value
        
        return reqMsgDict

