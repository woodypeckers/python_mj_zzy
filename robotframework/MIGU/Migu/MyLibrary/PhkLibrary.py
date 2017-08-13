#-*- coding:utf-8 -*-
import os
from robot.libraries.BuiltIn import BuiltIn
from Selenium2Library import utils
from robot.api import logger
import time
import hashlib
import types
import sys
from selenium.webdriver.common.keys import Keys

def press_key_by_character(locator, input_text):
    '''
    主要解决的问题是起草公告选择时发布对象"按合作编码，公司名称选择"，能精确匹配出需要选择的记录
    '''
    builtin = BuiltIn().get_library_instance('BuiltIn')
    selenium2lib = BuiltIn().get_library_instance('Selenium2Library')
    element = selenium2lib._element_find(locator, True, True)
    for i in range(0, len(input_text)):
        element.send_keys(input_text[i])     
        time.sleep(0.2)

def sign_product(activity_code, req_sys, req_date_time, secret_key):
    '''咪咕或者PRM与基地进行消息交互时，会进行sign的校验。调用此方法，可以生成sign。
    sign生成的方式：byte2hex(md5(ActivityCode+ ReqSys +ReqDateTime+密钥))'''
    str_by_passwd = activity_code + req_sys + req_date_time + secret_key
    if type(str_by_passwd) is types.StringType: #判断传入的是否是字符串
        m = hashlib.md5()
        m.update(str_by_passwd)
        return m.hexdigest() #返回sign
    else:
        return ''
    
def judge_file_exist(filename):
    '''判断文件是否存在,如果文件不存在，则关闭浏览器'''
    if os.path.exists(filename):
        return
    else:
        close_browser_if_exist()
        
def close_browser_if_exist():
    '''suite teardown时需要判断如果当前存在browser，则才进行关闭的动作'''
    try:
        selenium2lib = BuiltIn().get_library_instance('Selenium2Library')
        open_browser_list = selenium2lib._cache.get_open_browsers()
        logger.trace(u'打印dir(selenium2lib._cache):%s' % dir(selenium2lib._cache))
    except Exception:
        logger.info(u'未采用Selenium2Library，因此不用close browser,直接退出')
        return
    logger.trace('open_browser_list:%s' % open_browser_list)
    if open_browser_list != []:
        #browser = selenium2lib._current_browser()
        logger.trace(u'open_brwoser_list！＝[]，因此还是需要作关闭操作')
        if selenium2lib._cache.current:
            logger.info(u'关闭浏览器, selenium2lib_cache:%s' %  selenium2lib._cache)
            try:
                selenium2lib._cache.close()
            except Exception:
                logger.warn(u'关闭浏览器失败，直接selenium2lib._cache.empty_cache()')
                selenium2lib._cache.empty_cache()       
                
def arabic_numerals__str_transform_chinese_str(sourceStr):
    '''输入一个由阿拉伯数字组成的字符串，返回一个中文数字字符串
    背景：PRM1.0.2.003之后，公司中文名称不支持数字此函数将公司中文名称里面的阿拉伯数字修改为中文数字'''
    targetStr = ''
    for i in range(len(sourceStr)):
        i = arabic_numerals_transform_chinese(sourceStr[i])
        targetStr = targetStr + i
  
    return targetStr.decode('utf-8')    #将utf-8转换为unicode
 
def arabic_numerals_transform_chinese(num): 
    '''将阿拉伯数字转换为中文数字'''
    if num == '1':
        return '一'
    elif num == '2':
        return '二'
    elif num == '3':
        return '三'
    elif num == '4':
        return '四'
    elif num == '5':
        return '五'
    elif num == '6':
        return '六'
    elif num == '7':
        return '七'
    elif num == '8':
        return '八'
    elif num == '9':
        return '九'
    elif num == '0':
        return '零'
        
def reload_page_until_element_is_visivble(element_locator, wait_time=0, reload_count=5):
    """
    PRM登录进去以后，有时候会出现首页面 id=toHomepage找不到的情况。这个时候就刷新页面，直到这个元素出现。
    不适用于这个元素包含在frame里面的情况。
    多次刷新页面，直到页面某元素可见。默认最多刷新5次.每次刷新页面后等待元素出现的时间加两s
    """
    builtin = BuiltIn().get_library_instance('BuiltIn')
    selenium2lib = BuiltIn().get_library_instance('Selenium2Library')
    time.sleep(float(wait_time))
    
    for li in range(1,int(reload_count)):
        element_finder = selenium2lib._element_find(element_locator, True, False)
        logger.info(u'等待时间为：%s' %wait_time)
        if element_finder != None:
            logger.info(u'找到子元素，直接返回')
            return
        else:
            logger.info(u'未找到子元素')
        logger.info(u'重新重试的重试次数为:%s' % li)
        wait_time = wait_time + 2
        selenium2lib.reload_page()
        time.sleep(float(wait_time))
    return 

def get_credit_code(sourceStr):
    '''
    2016-1-28 彭亨康
    PRM侧新增了一个统一社会信用代码证的填写，其中第十八位是根据前面17位计算出来的，必须符合一定的规则，因此这个组织机构代码必须正确填写，否则
    会报错。调用此方法只需要输入统一社会信用代码证的前17位，然后会自动返回一个18位的返回要求的统一社会信用代码
    '''
    #各位置序号上的加权因子
    w = [1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28]
    
    #前面十七位每个字符对应的值
    dict1 = {'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'A':10, 'B':11, 'C':12, 'D':13, 'E':14, 'F':15, 'G':16,\
            'H':17, 'J':18, 'K':19, 'L':20, 'M':21, 'N':22, 'P':23, 'Q':24, 'R':25, 'T':26, 'U':27, 'W':28, 'X':29, 'Y':30}
    #第十八位换算过后的值
    dict2 = {0:'0', 1:'1', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10:'A', 11:'B', 12:'C',\
            13:'D', 14:'E', 15:'F', 16:'G', 17:'H', 18:'J', 19:'K', 20:'L', 21:'M', 22:'N', 23:'P', 24:'Q',\
            25:'R', 26:'T', 27:'U', 28:'W', 29:'X', 30:'Y'}
    
    #将传进来的字符串遍历保存到一个列表里面
    c = []
    for i in sourceStr:
        c.append(i)
    
    #每个字符串换算成值之后和加权因子相乘，然后求和
    sum = 0
    for i in range(len(sourceStr)):
        sum = sum + w[i]*dict1[c[i]]
        
    #求组织机构代码第18位对应的字符
    the_eighteen = dict2[31 - sum%31]
    
    #返回完整的统一社会信用代码
    return sourceStr+the_eighteen    