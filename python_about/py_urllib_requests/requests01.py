#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

r=requests.get('https://github.com/timeline.json')# r 的 Response 对象
print r.status_code
print r.headers['content-type']
print r.encoding
print r.text
r=requests.post("http://httpbin.org/post")

