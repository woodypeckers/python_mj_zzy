# -*- coding: utf-8 -*-

'''
Created on 2015-6-24

@author: wangmianjie
'''

'''某些Json节点...... '''

import json
import xmltodict
from lxml import etree
from encoding import detectEncoding, encodeTo
import chardet


def xmlToJson(xmlStr):
    xmlObj = xmltodict.parse(xmlStr)
    jsonStr = json.dumps(xmlObj)
    jsonStr = delRoot(jsonStr)
    index = jsonStr.find(': null')
    if index > 0:
        jsonStr = jsonStr[0:index] + ': {}' + jsonStr[index + 6:]

    return jsonStr


def jsonToXml(jsonStr):
    '''这个功能是做什么用的？ 从名字来看，把json转xml, utf-8没问题，gbk怎么转？统一转为UTF-8后再处理？'''
    org_json_encoding = detectEncoding(jsonStr)
    jsonStr = addRoot(jsonStr)
    jsonStr = encodeTo(jsonStr, 'UTF-8')
    jsonobj = json.loads(jsonStr)
    xmlstr = xmltodict.unparse(jsonobj) # 此时xmlstr是带declare的unicode　string
    root = etree.fromstring(xmlstr.encode('UTF-8'))     #此时把declare的那行去掉了
    xmlstr = etree.tostring(root,encoding=org_json_encoding,xml_declaration=True) #此时xmlstr是编码正常的，带declare的串
    return xmlstr


def addRoot(jsonStr):
    # 这里做了一下处理，如果原始文件是UTF-16LE的unicode编码，直接在前后加是有问题的，先去BOM，再转为UTF-8编码后，最后加头和尾
    if detectEncoding(jsonStr) == 'UTF-16LE':
        jsonStr = jsonStr.decode(detectEncoding(jsonStr)).lstrip(u'\ufeff').encode('UTF-8')
    return ' {"root" : ' + jsonStr + '}'


def delRoot(jsonStr):
    jsonStr = jsonStr.strip()
    length = len(jsonStr)

    rstJsonStr = ''

    i = 0
    status = 'start'

    while i < length:
        curChar = jsonStr[i]

        if status == 'start':  # 去掉{"root":root中的 {
            if curChar == '{':
                status = 'root-1'
        elif status == 'root-1':  # 去掉{"root":root中前面的"
            if curChar == '"':
                status = 'root'
        elif status == 'root':  # 去掉{"root":root中的root
            if jsonStr[i:i + 4] == 'root':
                status = 'root+1'
                i = i + 3  # 跳过" : "
        elif status == 'root+1':  # 去掉"root"}后面的"
            if curChar == '"':
                status = 'root+2'
        elif status == 'root+2':  # ȥ��{"root":�ĵ�ð�ţ�
            if curChar == ':':
                rstJsonStr = jsonStr[i + 1: length - 1]
                return rstJsonStr

        i = i + 1

    return rstJsonStr


def xmlStrFormat(xmlStr,encoding):
    '''这个function只是用于打印日志的，由于打印日志时已经把编码也写入信息了，所以这里只用打印UTF-8的编码即可'''
    # 对于xml文件，由于编码已经决定，所以第一行的declare读取时是会报错的,直接去掉编码，然后再decode到unicode处理
    xmlStr = xmlStr.decode(encoding)
    if xmlStr.startswith('<?xml'):
        idx = xmlStr.find('?>')
        xmlStr = xmlStr[idx+2:]
    et = etree.fromstring(xmlStr)
    return etree.tostring(et, encoding='UTF-8', pretty_print=True, xml_declaration=True)


def jsonStrFormat(jsonStr, encoding):
    #对于两种编码实现，需要去掉BOM之后再做转码工作 TBD:对于UTF-32怎么处理，后续可能还需要加特殊处理
    if encoding in ['UTF-16LE','UTF-16BE']:
        jsonStr = jsonStr.lstrip('\xff\xfe' ).lstrip('\xfe\xff')
        jsonobj = json.loads(jsonStr.decode(encoding))
    else:
        jsonobj = json.loads(jsonStr, encoding)
    jsonStr = json.dumps(jsonobj, indent=4)
    return jsonStr


def msgStrFormat(msgStr, msgFormat, encoding):
    if msgFormat == 'xml':
        return xmlStrFormat(msgStr,encoding)
    elif msgFormat == 'json':
        return jsonStrFormat(msgStr, encoding)
    else:
        return msgStr


if __name__ == "__main__":
    # dictStr={"orderId": ["19"], "refundnotifyurl": [""], "amount": ["300"], "version": ["2.0.0"], "REFUND_RULE_DETAIL": [""], "type": ["OrderRefund"], "merchantId": ["USERNAME1"]}
    # reqMessage = json.dumps(dictStr);
    # xmlStr = jsonToXml(reqMessage)
    # jsonStr= xmlToJson(xmlStr)
    # print xmlStr
    # print jsonStr

    # jsonStr='{"Request":{"BusiParams":{"OrderNo":"20150721174852780728","OrigReqTransID":"ISMP.201507211753441000303","OrigReqDate":"20150721175344","PayNum":300,"OrigReqSys":"11","VirtualUserID":"11"},"BusiCode":"OI_Rollback"},"PubInfo":{"TransactionId":"ISMP.201507211754341000304","TransactionTime":"20150721175434","OpId":"OpId","OrgId":"OrgId","InterfaceId":"6110","InterfaceType":"51"}}'
    #
    # print jsonStrFormat(jsonStr)
    data = '<?xml version="1.0" encoding="UTF-8" ?><message> <hostIp>10.12.8.145</hostIp> <validTime>10</validTime> <msgType>OI_PrepayOrReleasePayOrder</msgType> <delay>20</delay> <request> <PayMode>01</PayMode> <CommodityID>王绵杰</CommodityID> <BusiCode>OI_PrepayOrReleasePayOrder</BusiCode> <MobNum>15012880663</MobNum> <OrderNo>20150717152416352310</OrderNo> <UserID>1</UserID> <PayType>02</PayType> <Unit>01</Unit> </request> <response> <Code>00001</Code> </response> </message>'
    print xmlStrFormat(data)
