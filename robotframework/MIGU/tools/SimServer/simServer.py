# -*- coding: utf-8 -*-

'''
Created on 2015-4-23

@author: wangmianjie
'''
from twisted.internet import reactor
from twisted.web.server import Site

from net.httpServer import HttpServer
from config.systemConfig import SystemConfig
from admin.templateAdmin import TemplateAdmin

import logger 

class SimulatorServer():

    systemConfig='conf\system.xml'

    httpServList = []
    tcpServList = []
    
    sysPort = 0
        
    def __init__(self):
        self.loadConfig(self.systemConfig)

    def loadConfig(self, sysConfig):
        
        sysConfig = SystemConfig(sysConfig)
#         self.httpServList = sysConfig.getHttpServerList()
        self.httpServList = sysConfig.httpServerList
        self.sysPort = sysConfig.getSysPort()
       
        
    def startServer(self):
        reactor.listenTCP(self.sysPort, Site( TemplateAdmin() ))
        logger.log( '模拟器管理服务启动, 端口 : %s' % self.sysPort)
        
        for httpServ in self.httpServList:
            httpPort = httpServ.port
            servDesc = httpServ.desc
            reactor.listenTCP(int(httpPort), Site(HttpServer(httpServ)) )
            logger.log( 'Start HttpServer "%s", port: %s' % (servDesc, httpPort) )
            
        reactor.run()

sim = SimulatorServer()
sim.startServer()
