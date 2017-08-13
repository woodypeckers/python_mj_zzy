# -*- coding: utf-8 -*-

'''
Created on 2015-6-18

@author: wangmianjie
'''

from twisted.web.resource import Resource 
from admin.expectMessage import ExpectMessage
from  gExpectAdmin import *
from utils.jsonXmlTool import *

import copy

import logger


class ExpectQuery(Resource):
    isLeaf=True 
    
    def __init__(self):  
        Resource.__init__(self)  
        
    def render(self, request):
        rspMsg = 'fail'
        data = request.content.read()
        qeuryMsg = ExpectMessage(data)
        
        hostIp = request.client.host
        port = request.client.port
        
        logger.log('接收到来自"%s:%d"模拟器查询消息:\n%s' % ( hostIp, port, xmlStrFormat(data) ))
        logger.log('模拟器消息列表数量 %d' % len(G_ExpectMsg_List) )
        tmpExpMsgList =  copy.deepcopy(G_ExpectMsg_List)
        i = 1
        for msg in tmpExpMsgList:
            
            logger.log( '从模拟器期望消息队列取第"%d"条消息与查询请求对比' % i)
            
            if msg.equal(qeuryMsg) :
                logger.log('模拟器期望消息与查询消息相同')
                if msg.getMatchStatus():
                    rspMsg = 'success'
                    logger.log('模拟器查询，有匹配消息，从模拟器列表删除消息:\n%s' % msg.toString())
                    removeExpMsgByGlob(msg)
                    logger.log('模拟器查询结果返回成功')
                    return rspMsg
                else :
                    rspMsg = 'fail'
                    logger.log('模拟器消息列表数量 %d, 模拟器期望消息的状态为不匹配， 模拟器未收到被测系统请求, 从模拟器列表删除消息:\n%s' % (len(G_ExpectMsg_List),msg.toString()))
                    removeExpMsgByGlob(msg)
                    logger.log('模拟器消息列表数量 %d' % len(G_ExpectMsg_List) )
                    logger.log('模拟器查询结果返回失败')
                    
                    return rspMsg
                    
            else:
                logger.log('模拟器期望消息与查询消息不同')
                if msg.isExpired() :               
                    logger.log('模拟器消息列表数量 %d, 模拟器消息已过期,从模拟器列表删除消息:\n%s' %(len(G_ExpectMsg_List), msg.toString()))
                    removeExpMsgByGlob(msg)
                
                logger.log('取下一条对比')
            
            i += 1
            logger.log( '--------------------' )
                
        logger.log('模拟器消息列表数量 %d' % len(G_ExpectMsg_List) )
        return rspMsg
        