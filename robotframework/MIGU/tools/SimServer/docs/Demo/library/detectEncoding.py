#-*- coding:utf-8 -*-
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
import chardet


def detectEncoding():
    '''获取test变量resposne_body字符串的encoding，转为大写返回，例如UTF-8'''
    builtin = BuiltIn().get_library_instance('BuiltIn')
    response_body = builtin.get_variable_value('${response_body}')
    #这里的麻烦在于：UTF-16LE过来之后，无法判断
  
    encoding = chardet.detect(response_body)['encoding']

    #json包如果是UTF-8编码的，通过网络传送后再在chardet.detect，结果发现是ascii编码
    #if encoding in ['ASCII','ascii']:
    #    encoding = 'UTF-8'
    #if encoding == None:
    #    try:
    #        response_body.decode('UTF-16LE')
    #        return 'UTF-16LE'
    #    except Exception,e:
    #        logger.warn(u'detectEncoding结果为None,按UTF-16LE解码失败，错误信息如下:\n\s' % e)
    if encoding == None:
        if response_body.startswith('<\x00'):
            try:
                response_body.decode('UTF-16LE').encode('GBK')
                return 'UTF-16LE'
            except Exception,e:
                logger.warn(u'chardet检测encoding=None, 也按UTF-16LE解码,仍然报错,所以只能返回None')
        return None
    elif encoding == 'KOI8-R':          #中文两个字,在chardet下识别的就是KOI8-R
        return 'GB2312'
    elif encoding == 'windows-1252':        #这个是没有办法,现在也只能这么处理了,写文件查了是UTF-16LE,但chardet检测出来还是windows1252
        if response_body.startswith('\x20\x00'):
            return 'UTF-16LE'
    else:
        return encoding.upper()