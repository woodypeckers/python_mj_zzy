#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urlparse#����
"""
URL6��������prot_sch,net_loc,path,params,query,frag
"""
a = urlparse.urlparse('http://www.python.org/doc/FAQ.html')#urlparse()������6Ԫ��
b = urlparse.urlunparse(a)#urlunparse()��֮�෴
c = urlparse.urljoin('http://www.python.org/doc/FAQ.html','current/lib/lib.html')#ƴ�ӳ�������url
print a,"\n" ,b, "\n",c
print "--"*50

"""
quote*()��ȡurl���ݣ�������루һЩ���ܱ���ӡ�Ļ򲻱�web��������Ϊ��Ч�������ַ�����
"""
name = 'mj mama'
number = 9
base = 'http://www/~foo/cgi-bin/s.py'
final='%s?name=%s&num=%d'% (base,name,number)
print final
print "quote()���б�����:", urllib.quote(final)
print "quote_plus()���б�����:", urllib.quote_plus(final)
print "unquote()��ĸת��ASCII��ֵ��", urllib.unquote(final)
print "unquote_plus()��ĸת��ASCII��ֵ��", urllib.unquote_plus(final)



aDict= {'name':'Jia Xiao ', 'hmdir':'~~ggar'}
print urllib.urlencode(aDict)