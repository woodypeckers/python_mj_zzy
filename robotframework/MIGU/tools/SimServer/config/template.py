# -*- coding: utf-8 -*-

'''
Created on 2015-4-30

@author: wangmianjie
'''

from config.xmlMessage import XmlMessage
from config.keyValueMessage import KeyValueMessage

class Template():
    def __init__( self, templateNode, msgFormat ):
        self.msgFormat = msgFormat
        self.reqTemplate = None
        self.rspTemplate = None
        self.msgType = ''
        self.delayms = ''
        self.desc = ''

        nodeAttr = templateNode.attrib

        for attr in nodeAttr:
            if attr == 'msgType':
                self.msgType = nodeAttr[attr]
            if attr == 'delayms':
                self.delayms = nodeAttr[attr]
            if attr == 'desc':
                self.desc = nodeAttr[attr]

        reqNode = templateNode.find( 'request' )
        rspNode = templateNode.find( 'response' )
        reqTmpFile = reqNode.text
        rspTmpFile = rspNode.text

        if msgFormat == 'xml' or msgFormat == 'json':
            self.reqTemplate = XmlMessage( reqTmpFile, self.msgFormat, 'req' )
            self.rspTemplate = XmlMessage( rspTmpFile, self.msgFormat, 'rsp' )
        elif msgFormat == 'KeyValue' :
            self.reqTemplate = KeyValueMessage( reqTmpFile, self.msgFormat, 'req' )
            self.rspTemplate = KeyValueMessage( rspTmpFile, self.msgFormat, 'rsp' )

    def getMsgType( self ):
        return self.msgType

    def getMsgFormat( self ):
        return self.msgFormat

    def getDesc( self ):
        self.desc

    def getDelayms( self ):
        return self.delayms

    def getReqTmp( self ):
        return self.reqTemplate

    def getRspTmp( self ):
        return self.rspTmplate

