#-*- coding:utf8 -*-
import time

def getHms():
	return time.strftime('%H%M%S',time.localtime(time.time()))
	
def getYmd():
	return time.strftime('%y%m%d',time.localtime(time.time()))
	
def getYmdhms():
    #获取年月日时分秒，格式为：年年年年月月时时分分秒秒（20140924134802）
	return time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
	
	
