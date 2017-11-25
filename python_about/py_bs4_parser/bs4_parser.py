#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：mj

#Beautiful Soup，处理html和xml
# 格式化后浏览数据
# 访问Tag
# 访问属性
# 获取文本
# 注释处理
# 搜索
# css选择器
from bs4 import BeautifulSoup
soup = BeautifulSoup(open('test.html'))
print(soup.prettify())
#Tag
print(type(soup.title))
print(soup.title.name)
print(soup.title)

#string
print(type(soup.title.string))
print(soup.title.string)

#comment 注释
print(type(soup.a.string))
print(soup.a.string)

#遍历
for item in soup.body.contents:
    print(item.name)

#css查询
print(soup.select('.sister'))
print(soup.select('#header'))#id
#================================================
from HTMLParser import HTMLParser
#markupbase
class myparser(HTMLParser):
    def handle_decl(self,dec):
        HTMLParser.handle_dcel(self,dec)
        print ('decl %s'% dec)

    def handle_starttag(self,tag,attrs):
        HTMLParser.handle_starttag(self,tag,attrs)
        print('<'+ tag +'>')

    def handle_endtag(self,tag):
        HTMLParser.handle_endtag(self,tag)
        print('</'+ tag +'>')
    #<br/>
    def handle_startedtag(self,tag,attrs):
        HTMLParser.handle_startedtag(self,tag,attrs)

    def handle_comment(self,data):
        HTMLParser.handle_comment(self,data)
        print('data %s'% data)

    def close(self):
        HTMLParser.close(self)
        print('close')

demo = myparser()
demo.feed(open('test.html').read())
demo.close()