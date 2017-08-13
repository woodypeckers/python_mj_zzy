#-*- coding:cp936 -*-
from lxml import etree
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

def read_interface_file(fileName):
    #��ȡ�����ļ����������ļ������ݴ洢���ڴ����${interface_xml_content}��
    xml_str = open(fileName,'r+').read()
    builtin = BuiltIn()
    builtin.set_test_variable('${interface_xml_content}', xml_str)
    return xml_str
    

def change_node_text(text, nodePath):
    #��ȡ�ڴ��еı���${interface_xml_content}
    builtin = BuiltIn()
    xml_str = builtin.get_variable_value('${interface_xml_content}')    
    root=etree.fromstring(xml_str)
    
    if nodePath.find('/') == -1:
        nodePath = '//%s' % nodePath
    node_list = root.xpath(nodePath)
    for li in node_list:
        li.text = text
        logger.debug(u'�ڵ�%s��text�޸�Ϊ%s' % (li, text))
    #node = node_list[0]
    #node.text = text
    modify_xml_str = etree.tostring(root, encoding='GBK')
    builtin.set_test_variable('${interface_xml_content}', modify_xml_str)
    #open(fileName,'w+').write(modify_xml_str)
    return modify_xml_str

def remove_interface_node(nodePath):
    '''ʹ��ʱxpath��λ׼ȷһЩ�����������ҵ��ڵ�ĸ��ڵ㣬remove�ڵ㣬�ٷ���xmlstr'''
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
        logger.debug(u'δ���ֽڵ�')
    modify_xml_str = etree.tostring(root, encoding='GBK')
    builtin.set_test_variable('${interface_xml_content}', modify_xml_str)
    return modify_xml_str
    
#if __name__=="__main__":
#    org_xml_file='../xml/AddCnSimsToPrm.xml'
#    print change_node_text(read_file(org_xml_file), u'������',u'CompanyName')
#    print remove_node(read_file(org_xml_file),'Version')