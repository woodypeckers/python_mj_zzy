
# -*- coding: utf-8 -*-

'''
Created on 2015-5-21

@author: wangmianjie
'''

from config.xmlParameter import XmlParameter
from gExpectAdmin import *
from utils.jsonXmlTool import *

from lxml import etree

import logger

class XmlMessage():


    def __init__( self, path, msgFormat, direction ):
        self.paramList = []
        self.replaceParamList = []
        self.msgContent = open( path ).read()
        self.direction = direction
        self.msgFormat = msgFormat
        self.jsonContent = ''


        if self.msgFormat == 'json':
            self.jsonContent = self.msgContent
            self.msgContent = jsonToXml( self.msgContent )

        self.xml = etree.XML( self.msgContent )
        self.xmlET = etree.ElementTree( self.xml )


        self.loadParamList()

    '''  加载模板配置  '''
    def loadParamList( self ):

        for ele in self.xmlET.iter():
            param = []

            txt = ele.text
            xpath = self.xmlET.getpath( ele )
            tag = ele.tag

            if txt == None:
                txt = ''

            if ( txt <> '' ):
                if txt.find( '$${' ) >= 0 and txt.find( '}$$' ) > 0:
                    paramName = txt[txt.find( '$${' ) + 3:len( txt ) - 3]
                    param = XmlParameter( paramName, xpath, tag )
                    self.paramList.append( param )

                '''  应答消息要处理替换参数  '''
                if ( self.direction == 'rsp' ) :
                    if txt.find( '##{' ) >= 0 and txt.find( '}##' ) > 0:
                        paramName = txt[txt.find( '##{' ) + 3:len( txt ) - 3]
                        param = XmlParameter( paramName, xpath, tag )
                        self.replaceParamList.append( param )

    #求求消息与期望消息比较
    def reqMsgCompare( self, expMsg, reqMsg ):
        if self.msgFormat == 'json' or self.msgFormat == 'KeyValue':
            reqMsg = jsonToXml( reqMsg )

        tree = etree.XML( reqMsg )
        ns = tree.nsmap
        reqEt = etree.ElementTree( tree )


        expParamNum = len( expMsg.reqParamDict )
        tmpParamNum = len( self.paramList )
        
        verifyMode = expMsg.getVerifyMode()
        
        if verifyMode == 'NOCHECK':
            raise True
        elif verifyMode == "NORMAL":

            if expParamNum == tmpParamNum:
                i = 0
                while i < expParamNum:
                    xpath = self.paramList[i].path
                    #json转xml后加了一个root节点
                    if self.msgFormat == 'json':
                        xpath = '/' + xpath
                    realValue = reqEt.xpath( xpath, namespaces = ns )[0].text
    
                    expectValue = expMsg.reqParamDict[self.paramList[i].tag]
                    logger.log( u'接收消息字段: "%s" 实际值是: %s, 期望值是: %s' % ( reqEt.xpath( xpath, namespaces = ns )[0].tag, realValue, expectValue ) )
                    if realValue <> expectValue :
                        logger.log( '期望值与实际值匹配不一致' )
                        return False
    
                    i = i + 1
    
                logger.log( '请求消息匹配成功' )
    #             setExpMsgMatchStatus(expMsg)
                return True
            else :
                logger.log( '模板中，请求消息的参数个数与期望消息中的参数个数不匹配' )
                return False
        elif verifyMode == 'XPATH':
            for (xpath, expectValue) in expMsg.reqParamDict.items():
                print xpath
                print expectValue
                node = reqEt.xpath( xpath, namespaces = ns )[0]
                print node
                realValue =  node.text
                
                logger.log( u'接收消息字段: "%s" 实际值是: %s, 期望值是: %s' % ( node.tag, realValue, expectValue ) )
                if realValue <> expectValue :
                    logger.log( '期望值与实际值匹配不一致' )
                    return False
        
        return True

    def getRspMsg( self, expMsg, reqMsg, encoding ):
        '''这个功能的描述有些不太清楚，估计是从reqMsg找到对应的RspMsg'''
        if self.msgFormat == 'json' or self.msgFormat == 'KeyValue':
            reqMsg = jsonToXml(reqMsg )

        ns = self.xml.nsmap
        rspParamNum = len( expMsg.rspParamDict )
        i = 0
        while ( i < rspParamNum ):
            xpath = self.paramList[i].path
            ele = self.xmlET.xpath( xpath, namespaces = ns )

            value = expMsg.rspParamDict[self.paramList[i].paramName]
            ele[0].text = value

            i = i + 1
        self.procReplaceParam( reqMsg )
        #rspMsg = etree.tostring( self.xml, encoding = 'utf-8', xml_declaration = True )
        if self.msgFormat == 'xml':
            rspMsg = etree.tostring(self.xml, encoding=encoding, xml_declaration=True)
        else:
            rspMsg = etree.tostring( self.xml, encoding = 'utf-8', xml_declaration = False )


        if self.msgFormat == 'json' or self.msgFormat == 'KeyValue':
            # 前面rspMsg已经encoding成指定编码了,所以做法是转unicode后再转相应编码
            rspMsg = xmlToJson( rspMsg )
            rspMsg = rspMsg.decode("unicode-escape").encode(encoding)
            #open('r:/chenzw.txt','w+').write(rspMsg)
            if self.msgFormat == 'KeyValue':
                rspMsg = json

        return rspMsg

    '''  将请求中的要替换的值替换  '''
    def procReplaceParam( self, reqMsg ):
        reqMsgXml = etree.XML( reqMsg )
        reqET = etree.ElementTree( reqMsgXml )
        ns = self.xml.nsmap
        for replaceParam in self.replaceParamList:

            tag = replaceParam.paramName
            '''  根据参数的tag找到请求消息中对应的值  '''
            value = reqET.find( '//' + tag ).text

            xpath = replaceParam.path
            ele = self.xmlET.xpath( xpath, namespaces = ns )
            ele[0].text = value

