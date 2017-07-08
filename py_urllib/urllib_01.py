#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urlparse#解析
"""
URL6个部件，prot_sch,net_loc,path,params,query,frag
"""
a = urlparse.urlparse('http://www.python.org/doc/FAQ.html')#urlparse()解析成6元祖
b = urlparse.urlunparse(a)#urlunparse()与之相反
c = urlparse.urljoin('http://www.python.org/doc/FAQ.html','current/lib/lib.html')#拼接成完整的url
print a,"\n" ,b, "\n",c
print "--"*50

"""
quote*()获取url数据，将其编码（一些不能被打印的或不背web服务器视为有效的特殊字符串）
"""
name = 'mj mama'
number = 9
base = 'http://www/~foo/cgi-bin/s.py'
final='%s?name=%s&num=%d'% (base,name,number)
print final
print "quote()进行编码后的:", urllib.quote(final)
print "quote_plus()进行编码后的:", urllib.quote_plus(final)
print "unquote()字母转换ASCII码值：", urllib.unquote(final)
print "unquote_plus()字母转换ASCII码值：", urllib.unquote_plus(final)



aDict= {'name':'Jia Xiao ', 'hmdir':'~~ggar'}
print urllib.urlencode(aDict)