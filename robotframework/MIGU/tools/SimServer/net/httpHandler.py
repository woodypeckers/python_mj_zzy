# -*- coding: utf-8 -*-

'''
Created on 2015-5-26

@author: wangmianjie
'''

from twisted.web.resource import Resource
from utils.encoding import detectEncoding

from  gExpectAdmin import *
from utils.jsonXmlTool import *

import logger
import time

import copy


class HttpHandler(Resource):
    isLeaf = True

    def __init__(self, httpServConfig):
        Resource.__init__(self)
        self.httpServConfig = httpServConfig

    def render(self, request):
        reqMsgType = ''

        msgTypeFlag = self.httpServConfig.msgTypeFlag
        msgFormat = self.httpServConfig.msgFormat
        encoding = 'UTF-8'
        if self.httpServConfig.encoding not in [None, '']:
            encoding = self.httpServConfig.encoding

        ''' 请求消息体  '''
        reqMessage = request.content.read()
        reqHeaders = request.getAllHeaders()  # 返回类型为dict
        reqHeaderEncoding = 'UTF-8'  # 包头中定义的encoding
        if reqHeaders.has_key('content-type') and reqHeaders['content-type'].find('charset') != -1:
            reqHeaderEncoding = reqHeaders['content-type'].split('charset=')[1].strip()
        reqEncoding = detectEncoding(reqMessage)  # 包体中检测的encoding

        hostIp = request.client.host
        port = request.client.port

        ''' 收到消息类型  '''
        if msgTypeFlag == 'url':
            reqMsgType = request.path
        elif msgFormat == 'xml' or msgFormat == 'json':
            reqMsgType = self.getMsgType(reqMessage, msgTypeFlag, msgFormat)
        logger.log('接收到来自"%s:%d"业务系统请求消息(encoding=%s):\n %s\n %s' %
                   (hostIp, port, reqEncoding, reqHeaders,msgStrFormat(reqMessage, msgFormat, reqEncoding)))

        if reqEncoding.upper() != reqHeaderEncoding.upper():
            logger.log('Warnning：请求包的包头中的encoding＝%s，但是检测到包体的encoding＝%s, 两者不一致！' % \
                       (reqHeaderEncoding, reqEncoding))

        logger.log('接收消息类型为：%s' % reqMsgType)

        ''' 应答消息体  '''
        rspMessage = ''
        '''  根据请求消息类型找到对应的模板 '''
        template = self.httpServConfig.getTemplateForMsgtype(reqMsgType)

        if template == None:
            logger.log('未能匹配到模板  "%s" 模板 ' % reqMsgType)
            return rspMessage

        ''' 请求消息，模板和期望消息列表对比 '''
        logger.log('模拟器消息列表数量 %d' % len(G_ExpectMsg_List))
        i = 0
        if G_ExpectMsg_List.__len__() > 0:
            i += 1
            tmpHEspMsgList = copy.deepcopy(G_ExpectMsg_List)

            for expMsg in tmpHEspMsgList:
                ''' IP比较和消息类型比较 '''
                logger.log('从模拟器消息队列取第"%d"条消息与业务系统请求对比' % i)
                if hostIp == expMsg.getHostIp() and template.msgType == expMsg.getMsgType():
                    logger.log('请求消息与期望消息ip和消息类型匹配成功')
                    logger.log('模拟器消息队列消息 : \n%s' % expMsg.toString())

                    if expMsg.getMatchStatus():
                        logger.log('已经已经匹配过的消息，取下一条消息')
                        #break
                    elif expMsg.isExpired():
                        logger.log('该消息已经过期，从模拟器消息队列删除，取下一条消息')
                        removeExpMsgByGlob(expMsg)
                        #break
                    elif template.reqTemplate.reqMsgCompare(expMsg, reqMessage):

                        if expMsg.getMatchStatus():
                            logger.log('请求消息与期望消息匹配成功, 但是模拟器已经返回应答')
                            logger.log('从模拟器队列删除期望消息')
                            setExpMsgMatchStatus(expMsg)

                        ''' 如果期望消息没有超时   '''
                        if not expMsg.isExpired():
                            expMsg.setMatchStatus()
                            delay = expMsg.delay
                            if (delay > 0):
                                logger.log('模拟器超时"%d"秒, 不返回' % delay)
                                time.sleep(delay)
                                return 1

                            '''   设置为已经匹配   '''
                            # setExpMsgMatchStatus(expMsg)

                            logger.log('请求消息与期望消息匹配成功, 模拟器生成返回消息包')
                            rspMessage = template.rspTemplate.getRspMsg(expMsg, reqMessage, encoding=self.httpServConfig.encoding)

                            # 获取返回包的编码，转为unicode后按服务器配置进行转码后输出要求的编码格式
                            #try:
                            #    rspMessage = rspMessage.decode(rspMessageEncoding).encode(self.httpServConfig.encoding)
                            #except Exception, e:
                            #    logger.log('警告：返回包体实际编码%s,按服务器定义的编码%s进行转换时失败！--\n%s' % (
                            #        rspMessageEncoding, self.httpServConfig.encoding, e))
                            rspMessageEncoding = detectEncoding(rspMessage)
                            rspMessage_fmt =msgStrFormat(rspMessage, msgFormat, self.httpServConfig.encoding)
                            logger.log('模拟器发送消息到:  %s:%d, 消息包(encoding=%s): \n%s' %
                                    (hostIp, port, rspMessageEncoding,rspMessage_fmt))
                            # 在返回包体前，可以进行自定义头的操作，如果不是REPLY就回值，否则从request中获取头的值设置到返回包头中
                            if expMsg.hasCustomHeader():
                                for key,value in expMsg.customHeaderDict.iteritems():
                                    if value == 'REPLY':
                                        #获取请求包头中的内容,放在回复包中, 这里有一个问题,继承IResource,没有方法调用,只能inspect对象再设置值
                                        if reqHeaders.has_key(key):
                                            req_header_value = reqHeaders[key]
                                            request.responseHeaders.addRawHeader(key, req_header_value)
                                        else:
                                            logger.log('模拟器在请求包中未找到头:　%s' % key)
                                            return 
                                    else:
                                        request.responseHeaders.addRawHeader(key, value)

                            #TODO:debug  把Resonse包体内容写到R:/rspMessage.txt,主要用于查HTTP返回的包体内容及编码
                            #open('R:/rspMessage.txt','w+').write(rspMessage)


                            #匹配成功之后,即将返回response前,从全局列表中清除已匹配过的消息对象
                            removeExpMsgByGlob(expMsg)

                            return rspMessage
                        else:
                            logger.log('模拟器等待超时:')
                            logger.log('模拟器消息列表数量 %d' % len(G_ExpectMsg_List))
                            logger.log('从模拟器队列删除期望消息')
                            removeExpMsgByGlob(expMsg)
                            logger.log('模拟器消息列表数量变更为 %d' % len(G_ExpectMsg_List))
                            return
                    else:
                        logger.log('与模拟器中所有消息匹配失败')
                        logger.log('取期望消息队列下一条比较')

                else:
                    logger.log('请求消息与期望消息Ip不一致，或消息类型不一致')
                    logger.log('请求 ip: "%s", 模拟器期望 ip: "%s"' % (hostIp, expMsg.getHostIp()))
                    logger.log('请求 消息类型: %s, 模拟器期望 消息类型: %s' % (template.msgType, expMsg.getMsgType()))
                    logger.log('取期望消息队列下一条比较')
                    # end for
        else:
            logger.log('模拟器期望消息列表为空')

        return

    def getMsgType(self, reqMessage, msgTypeFlag, msgFormat):

        if msgFormat == 'json':
            jsonStr = ' {"root" : ' + reqMessage + '}'
            jsonobj = json.loads(jsonStr)
            reqMessage = xmltodict.unparse(jsonobj).encode('utf-8')

        tree = etree.XML(reqMessage)
        et = etree.ElementTree(tree)

        if msgTypeFlag == '$$root$$':
            if msgFormat == 'xml':
                root = et.getroot()
                return root.tag
            elif msgFormat == 'json':
                root = et.getroot()
                childs = root.getchildren()
                return childs[0].tag
        else:
            for ele in et.iter(msgTypeFlag):
                return ele.text
