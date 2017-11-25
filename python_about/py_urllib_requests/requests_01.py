#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author : mj
import requests

# print(dir(requests))#查看支持方法
# url = 'http://www.bai.com'
# r = requests.get(url)
# print(r.text)
# print(r.status_code)
# print(r.encoding)
#
# #传递参数
# #params = {'k1':'v1','k2':'k2'}
# params = {'k1':'v1','k2':'[1,2,3]'}
# r = requests.get('http://httpbin.org/get',params)
# print(r.url)
#
# #处理二进制数据
# from io import BytesIO
# from PIL import Image
# r = requests.get('https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1510053844214&di=5e75e278bcc8d5933f03452f92af7f49&imgtype=0&src=http%3A%2F%2Ff.hiphotos.baidu.com%2Fzhidao%2Fpic%2Fitem%2F8326cffc1e178a82dce3d7a5f603738da877e8dc.jpg')
# image = Image.open(BytesIO(r.content))
# image.save('sanyecao.jpg')
#
# #json处理
# r = requests.get('https://github.com/timeline.json')# r 的 Response 对象
# print(type(r.json))
# print r.status_code
# print r.headers['content-type']
# print r.encoding
# print r.text
#
# #原始数据
# r = requests.get('https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1510053844214&di=5e75e278bcc8d5933f03452f92af7f49&imgtype=0&src=http%3A%2F%2Ff.hiphotos.baidu.com%2Fzhidao%2Fpic%2Fitem%2F8326cffc1e178a82dce3d7a5f603738da877e8dc.jpg',stream =True)
# #stream = True 流数据格式，读一点，写一点
# with open('sanyecao.jpg','wb+')as f:#wb+ 写打开二进制，+号，删除原来的
#     for chunk in r.iter_content(1024):
#         f.write(chunk)
#
# #提交表单form
# """根据头信息判断文件类型"""
# import json
# form = {"username":"admin","password":"123456"}
# r = requests.post('http://httpbin.org/post',data=form)
# print(r.text)
# r = requests.post('http://httpbin.org/post',data=json.dumps(form))

#cookie
# url = 'http://www.bai.com'
# r = requests.get(url)
# cookies = r.cookies
# for k, v in cookies.get_dict().items():
#     print(k,v)

# cookies = {"c1":"v1","c2":"v2"}
# r = requests.get('http://httpbin.org/cookies',cookies=cookies)
# print(r.text)
#
# #重定向和重定向历史
# r = requests.get('http://github.com',allow_redirects = True)#allow_redirects允许重定向
# print(r.url)
# print(r.status_code)
# print(r.history)

#代理
'''
proxies = {'http':'1','https':'2'}
r = requests.get('http://github.com',proxies=proxies)
'''


