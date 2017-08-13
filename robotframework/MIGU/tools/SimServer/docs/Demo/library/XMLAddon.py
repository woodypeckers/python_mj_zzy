#-*- coding:utf-8 -*- 
'''原始的RF的XML库中差了这么一个可以定义xml_declaration的string导出，这里加上'''

#下面这几句,是解决Python的encoding的坑
import sys
default_encoding = 'UTF-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

#下面是给RF的内置XML库打的补丁    
import lxml.etree

def xmlToString(element, encoding = 'UTF-8', xml_declaration= None, pretty_print = None  ):
    if xml_declaration != None:
        xml_declaration = True
    if pretty_print != None:
        pretty_print = True
    xmlstr = lxml.etree.tostring( element, 
                    encoding=encoding,
                    method='xml',
                    xml_declaration = xml_declaration, 
                    pretty_print = pretty_print)
    return xmlstr
