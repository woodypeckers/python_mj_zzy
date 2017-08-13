# -*- coding:utf-8 -*-
import chardet


def detectEncoding(str):
    """对于GBK编码的，Python的chardet判断，有时会时windows-1252,或者ISO-8859-2"""
    strEncoding = chardet.detect(str)['encoding']
    result = ''
    if strEncoding in ['windows-1252', 'ISO-8859-2',  'windows-936', 'KOI8-R']:  # 后面1个编码是估计的
         result = 'GBK'
         if str.startswith('\x20\x00'):
             result ='UTF-16LE'
    #有时chardet检查为None,目前在UTF-16LE中发现,所以这里加上
    elif strEncoding == None:
        try:
            str.decode('UTF-16LE').encode('UTF-8')
            result = 'UTF-16LE'
        except Exception,e:
            print e
    else:
        result = strEncoding
    return result


def encodeTo(str, to_encoding):
    """转换成指定编码"""
    org_encoding = detectEncoding(str)
    # if org_encoding == None:
    #     try:
    #         str.decode('UTF-16LE')
    #     except Exception,e:
    #         print e
    #     str = str.decode(org_encoding)
    # if str.startswith('<?xml'):
    #     idx = str.find('?>')
    #     str = str[idx+2:]
    #     et = etree.fromstring(xmlStr)
    #     return etree.tostring(et, encoding=to_encoding, pretty_print=True, xml_declaration=True)
    #对于xml，转码之外，还需要先去掉前面的declare的第一行

    #     if org_encoding == 'GBK':
    #         org_encoding = 'cp936'
    #     if someencoding.upper() == 'UNICODE':
    #         return str.decode( org_encoding ).lstrip( u'\ufeff' )
    #     else:
    #         return str.decode( org_encoding ).lstrip( u'\ufeff' ).encode( to_encoding )
    return str.decode(org_encoding).encode(to_encoding)
