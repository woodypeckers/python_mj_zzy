# -*- coding: utf-8 -*-

'''
Created on 2015-5-29

@author: wangmianjie
'''


from twisted.web.resource import Resource 
from admin.expectMessage import ExpectMessage
from  gExpectAdmin import G_ExpectMsg_List
from utils.jsonXmlTool import *

import logger

class ExpMsgAdmin(Resource):
    
    isLeaf=True 
    
    def __init__(self):  
        Resource.__init__(self)  
        
    def render(self, request):
        data = request.content.read()
        logger.log( '接收到模拟器调用请求: \n%s' % data )
        expMsg = ExpectMessage(data)
        G_ExpectMsg_List.append(expMsg)
        
        logger.log( '模拟器消息队列数: %d' % len(G_ExpectMsg_List))

        return expMsg.toString()

