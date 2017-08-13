#-*- coding:cp936 -*-
from lxml import etree
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

def read_interface_file(fileName):
    #读取本地文件，将本地文件的内容存储到内存变量${interface_xml_content}中
    xml_str = open(fileName,'r+').read()
    builtin = BuiltIn()
    builtin.set_test_variable('${interface_xml_content}', xml_str)
    return xml_str
    

def change_node_text(text, nodePath):
    #读取内存中的变量${interface_xml_content}
    builtin = BuiltIn()
    xml_str = builtin.get_variable_value('${interface_xml_content}')    
    root=etree.fromstring(xml_str)
    
    if nodePath.find('/') == -1:
        nodePath = '//%s' % nodePath
    node_list = root.xpath(nodePath)
    for li in node_list:
        li.text = text
        logger.debug(u'节点%s的text修改为%s' % (li, text))
    #node = node_list[0]
    #node.text = text
    modify_xml_str = etree.tostring(root, encoding='GBK')
    builtin.set_test_variable('${interface_xml_content}', modify_xml_str)
    #open(fileName,'w+').write(modify_xml_str)
    return modify_xml_str

def remove_interface_node(nodePath):
    '''使用时xpath定位准确一些，方法上是找到节点的父节点，remove节点，再返回xmlstr'''
    builtin = BuiltIn()
    xml_str = builtin.get_variable_value('${interface_xml_content}')    
    root=etree.fromstring(xml_str)
    if nodePath.find('/') == -1:
        nodePath = '//%s' % nodePath
    node_list = root.xpath(nodePath)
    if node_list != []:
        node = node_list[0]
        parent = node.getparent()
        parent.remove(node)
    else:
        logger.debug(u'未发现节点')
    modify_xml_str = etree.tostring(root, encoding='GBK')
    builtin.set_test_variable('${interface_xml_content}', modify_xml_str)
    return modify_xml_str
    
#if __name__=="__main__":
#    org_xml_file='../xml/AddCnSimsToPrm.xml'
#    print change_node_text(read_file(org_xml_file), u'陈振武',u'CompanyName')
#    print remove_node(read_file(org_xml_file),'Version')