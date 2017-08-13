# -*- coding: utf-8 -*-

'''
Created on 2015-5-29

@author: wangmianjie
'''

from lxml import etree
import time


class ExpectMessage():

    def __init__( self, data ):
        ''' 请求和应答参数列表， 保存每个参数的path和值 '''
        self.reqParamDict = {}
        self.rspParamDict = {}
        self.customHeaderDict = {}

        self.validTime = 0
        self.msgType = ''
        self.hostIp = ''
        self.delay = 0

        ''' 验证模式
        NORMAL: 默认模式
        XPATH: xpath校验方式
        NOCHECK: 不做校验
        '''
        self.verifyMode = 'NORMAL'
        
        '''
        NORMAL:默认模式
        CDATA:返回CDATA
        NORESP: 不返回（返回http消息体为空）
        '''
        self.respMode='NORMAL'
        
        self.msgContent = data
        self.startTime = time.time()
        self.matchStatus = False

        # 消息检验模式
        self.reqVerifyMode = ''

        self.paraser( data )

    '''  解析请求 '''
    def paraser( self, data ):

        root = etree.XML( data )
        self.hostIp = root.find( 'hostIp' ).text
        self.validTime = int( root.find( 'validTime' ).text )
        self.msgType = root.find( 'msgType' ).text
        self.delay = int( root.find( 'delay' ).text )
        
        reqNode = root.find( 'request' )
        reqAttr = reqNode.attrib
        for attr in reqAttr:
            if attr == 'verifyMode':
                self.verifyMode = reqAttr[attr]
                
        #验证模式为xpath
        if self.verifyMode == 'XPATH' :
            xpathListNode = reqNode.find( 'xpathList')
        
            for xpathNode in xpathListNode:
                path = xpathNode.find('path').text
                expValue = xpathNode.find('expValue').text
                
                self.reqParamDict[path] = expValue
        
        #默认模式，精确匹配        
        elif self.verifyMode == 'NORMAL' :
            for req in reqNode :
                key = req.tag
                value = req.text
                if value == None:
                    value = ''
                self.reqParamDict[key] = value
        elif self.verifyMode == 'NOCHECK':
            self.reqParamDict = {}
                
    
        rspNode = root.find( 'response' )
        rspAttr = reqNode.attrib
        
        for attr in reqAttr:
            if attr == 'respMode':
                self.respMode = reqAttr[attr]
                
        for rsp in rspNode :
            key = rsp.tag
            value = rsp.text
            if value == None:
                value = ''
            self.rspParamDict[key] = value

        # add custom header
        customHeaderNode = root.find('custom_header')
        if customHeaderNode != None:
            for custom_header in customHeaderNode:
                key = custom_header.tag
                value = custom_header.text
                self.customHeaderDict.setdefault(key,value)


    def toString( self ):
        rstStr = 'hostIp is: %s' % self.hostIp + '\n'
        rstStr += 'msgType is: %s' % self.msgType + '\n'
        rstStr += 'validTime is:%s' % self.validTime + '\n'
        rstStr += 'startTime is:%s' % self.startTime + '\n'
        rstStr += 'matchStatus: %s' % self.matchStatus + '\n'
        rstStr += 'delay: %s' % str( self.delay ) + '\n'
        rstStr += 'custom_header:%s' %  str(self.customHeaderDict) + '\n'

        rstStr += 'request verifyMode is %s' % self.reqVerifyMode + '\n'
        rstStr += 'request parameter total of %d' % len( self.reqParamDict ) + '\n'
        for reqParam in self.reqParamDict:
            value = self.reqParamDict[reqParam]

            if value == None :
                value = ''
            rstStr = rstStr + '    ' + reqParam + ':' + value + '\n'

        rstStr += 'response parameter  total of %d' % len( self.rspParamDict ) + '\n'
        for rspParam in self.rspParamDict:
            value = self.rspParamDict[rspParam]

            if value == None :
                value = ''
            rstStr = rstStr + '    ' + rspParam + ':' + value + '\n'

        if not isinstance( rstStr, bytes ):
            rstStr = rstStr.encode( 'utf-8' )

        return rstStr

    def equal( self, expMsg ):
        if( expMsg.msgType == self.msgType ) \
          and ( expMsg.validTime == self.validTime ) \
          and ( expMsg.hostIp == self.hostIp ) \
          and ( expMsg.reqParamDict == self.reqParamDict ) \
          and ( expMsg.rspParamDict == self.rspParamDict ) :
            return True

        return False


    def getExpired( self ):
        return self.validTime

    def getHostIp( self ):
        return self.hostIp

    def getMsgType( self ):
        return self.msgType

    ''' 判断是否超时 '''
    def isExpired( self ):
        curTime = time.time()
        tmp = float( curTime ) - float( self.startTime )
        if tmp >= self.validTime :
            return True

        return False

    def setMatchStatus( self ):
        self.matchStatus = True

    def getMatchStatus( self ):
        return self.matchStatus

    def hasCustomHeader(self):
        return self.customHeaderDict != {}
    
    def getVerifyMode(self):
        return self.verifyMode
    
    def getRespMode(self):
        return self.respMode
