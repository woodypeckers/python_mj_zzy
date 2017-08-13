# -*- coding: utf-8 -*-

'''
Created on 2014-5-7
NDMP HTTP模拟器
2个服务，监听2个端口
1。HTTP服务，接收NDMP消息并返回应答
2.XMLRPC服务, 接收robotframework消息，设置期望接收消息，校验条件，应答消息的状态码

@author: wangmianjie
'''


from twisted.web.resource import Resource

from net.httpHandler import HttpHandler


class HttpServer(Resource ):
   
    httpServConfig = None
    
    def __init__(self, httpServ):  
        Resource.__init__(self)  
        self.putChild("", self)
        self.httpServConfig = httpServ

    def getChild(self, path, request):
        rspMessage = HttpHandler(self.httpServConfig)        
        if rspMessage != 1:
            return rspMessage
            
    

    
