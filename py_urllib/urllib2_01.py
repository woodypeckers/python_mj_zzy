#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
login = 'wesc'
passwd = 'you\'llNerverGuess'
url = 'http://localhost'

def handler_version(url):# 分配基本认证处理器HTTPBasicAuthHandler，建立一个URL-opener()
    from urlparse import urlparse as up
    hd = urllib2.HTTPBasicAuthHandler()
    hd.add_password('Archives',up(url)[1],login,passwd)
    opener = urllib2.build_opener(hd)
    urllib2.install_opener(opener)
    return url
def request_version(url):
    from base64 import encodestring
    req = urllib2.Request(url)
    b64str = encodestring("%s:%s"%(login,passwd))[:-1]
    req.add_header('Authorization',"Basic%s"%b64str)
    return req

for funcType in ("handler","request"):
    print '*** Using %s:'% funcType.upper()
    urla = eval('%s_version')(url)#eval函数将字符串当成有效Python表达式来求值，并返回计算结果
    f = urllib2.urlopen(urla)
    print f.readlines()
    f.close()