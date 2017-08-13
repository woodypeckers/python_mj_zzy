# -*- coding: utf-8 -*-

'''
Created on 2015-5-12

@author: wangmianjie
'''

from config.template import Template

class HttpServerEntity():

    def __init__( self, httpServNode ):
        self.templateList = []
        self.encoding = 'UTF-8'         #如果未配置，缺省按UTF-8处理，兼容以前的定义

        nodeAttr = httpServNode.attrib

        for attr in nodeAttr:
            if attr == 'version':
                self.version = nodeAttr[attr]
            if attr == 'port':
                self.port = nodeAttr[attr]
            if attr == 'msgTypeFlag':
                self.msgTypeFlag = nodeAttr[attr]
            if attr == 'msgFormat':
                self.msgFormat = nodeAttr[attr]
            if attr == 'desc':
                self.desc = nodeAttr[attr]
            if attr == 'encoding':
                self.encoding = nodeAttr[attr]

        tmpNodeList = httpServNode.getchildren()

        for tmpNode in tmpNodeList:
            template = Template( tmpNode, self.msgFormat )
            self.templateList.append( template )


    def getTemplateForMsgtype( self, msgType ):

        for template in self.templateList:
            if msgType == template.msgType:
                return template
