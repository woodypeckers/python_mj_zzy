# -*- coding:utf-8 -*-
#!/usr/bin/env python
# author : mj
# Created by iFantastic on 2018/7/9

import  requests
import json
"""发送请求"""
# r = requests.get('https://api.github.com/user',
#                  auth =('zhangzhanyong','ly'))
#
# print(r.status_code)
# print(r.headers)
# print(r.headers['content-type'])
# print(r.encoding)
# print(r.text)
# print(r.json())

# a = requests.get('http://httpbin.org/get')
# r = requests.get('https://api.github.com/events')
# print(a.status_code)
# """发送请求"""
# a = requests.post('http://httpbin.org/post', data = {'city':'sz','name':'mj'})
# print('text---',a.text)
# print('headers---',a.headers)
#
# a = requests.put('http://httpbin.org/put',data={'age':18})
# print(a)
# a = requests.delete('http://httpbin.org/delete')
# print('delete---',a.text)
# a = requests.options('http://httpbin.org/get')
# print(a.text)
# a = requests.head('http://httpbin.org/get')
# print(a.text)


# """传参"""
# payload={'xiao':'aaa','da':'bbb'}
# r = requests.get("http://httpbin.org/get",payload)
# # print('payload---',r.text)
# # print('url---',r.url)
#
# """响应内容"""
# r = requests.get('https://api.github.com/events')

# print(r.encoding)
# r.encoding = 'ISO-8859-1'
# print(r.text)

# print(r.content)"""二进制响应内容"""
#
# print(r.json())"""json"""

# """原始内容"""
# r = requests.get('https://api.github.com/events', stream=True)
# r.raw
# print(r.raw.read(10))
#
# """定制请求头"""
# payload2 = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
# r = requests.post("http://httpbin.org/post", data=payload2)
# print(r.text)
#
#
# payload1 = (('k1', 'v1'), ('k2', 'v2'))
# r = requests.post("http://httpbin.org/post", data=payload1)
# print(r.text)


#
# url = 'http://httpbin.org/post/user/endpoint'
# payload = {'user': 'data'}
# r = requests.post(url, data=json.dumps(payload))
# print(r.text)


# url = 'http://httpbin.org/post'
# files = {'file': open('test.xlsx', 'rb')}
# r = requests.post(url, files=files)
# print(r.text)


"""cookie"""
url = 'https://10.12.8.163:2999/cmcc/portal/login.jsp'
r = requests.get(url)
print(r.cookies)