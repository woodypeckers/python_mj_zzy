# -*- coding: utf-8 -*-

'''
Created on 2015-4-24

@author: wangmianjie
'''


from config.httpServerEntity import HttpServerEntity
from lxml import etree

import logger

class SystemConfig():

    def __init__( self, cfgFile ):
        self.httpServerList = []
        sysPort = 0

        '''加载系统配置文件配置 '''
        logger.log( 'load system config file: %s' % cfgFile )
        doc = etree.parse( cfgFile )
        self.sysPort = int( doc.find( 'system' ).find( 'port' ).text )
        logger.log( '模拟器端口: %s' % self.sysPort )

        httpServNodeList = doc.getiterator( 'httpServer' )
#         tcpServNodeList  = root.getiterator('tcpServer')

        logger.log( '加载http 服务器配置' )
        for httpServNode in httpServNodeList :
            httpServ = HttpServerEntity( httpServNode )
            self.httpServerList.append( httpServ )

    def getSysPort( self ):
        return self.sysPort

    def getHttpServerList( self ):
        return self.httpServerList
