#-*- coding:utf-8 -*-

import xml.etree.ElementTree as et

def get_rsp_code(xmlstr):
    #判断同步给PRM的信息是否成功，如果成功，返回"success"；如果失败，返回"failure"
    xml_str = xmlstr.replace('"GBK"?>','"utf-8"?>').decode('GBK','ignore').encode('utf-8')
        
    root = et.fromstring(xml_str)
    #获取所有CompanyName节点 
    parentNode = root.findall('Header')
    for node in parentNode:
        resCode = node.find('RspCode').text

    if resCode == '000000':
        return 'success'
    else:
        return 'failure'