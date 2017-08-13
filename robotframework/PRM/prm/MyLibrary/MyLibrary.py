#-*- coding:utf-8 -*-
'''
增加一些关键字，减少案例的复杂度
BuiltIn()的使用方式，需要RobotFramework2.7.5及以上版本的支撑
好处是：　在单一进程内可以结合多个库，例如BuiltIn和Selenium2Library
'''
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
import time,datetime
import copy
import httplib
import os
from xml.etree import ElementTree as ET
from Selenium2Library import utils

def get_element_text(locator):
    """返回Element的text()
    """
    builtin = BuiltIn().get_library_instance('BuiltIn')
    selenium2lib = BuiltIn().get_library_instance('Selenium2Library')
    element = selenium2lib._element_find(locator, True, True)
    if element is None:
        raise ValueError("Element '%s' not found." % (locator))
    text = element.text
    logger.info(u'元素的text()为:%s'  % (text,))
    return text

def element_visible(locator):
    '''
    Desc: 对当前frame中的element visible进行判断，retrun True/False
    BTW: Selenium2Library中大量的方法均为校验类
    　　但_is_visible()为私有函数，而其它均非流程判断类，所以新增此方法
    '''
    result = False
    selenium2lib = BuiltIn().get_library_instance('Selenium2Library')
    if selenium2lib._is_visible(locator) == True:
        result = True
    return result

def run_keyword_if_element_visible(locator, keyword, *args):
    '''
    Desc: 如果locator可见，则运行keyword以及相关参数
    BTW: 将BuiltIn与Selenium2Library结合，以便简化脚本逻辑
         此功能需要robotframework2.7.5的支撑,详见robotframework-userguide
    '''
    builtin = BuiltIn().get_library_instance('BuiltIn')
    status = element_visible(locator)
    builtin.run_keyword_if(status, keyword , *args)

def run_keyword_if_page_contains_element(locator, keyword, *args):
    '''
    Desc: 如果页面包含该locator，则运行keyword以及相关参数
    BTW: 将BuiltIn与Selenium2Library结合，以便简化脚本逻辑
         此功能需要robotframework2.7.5的支撑,详见robotframework-userguide
    用法：主要用户咪咕admin端展开查询框的问题。此处查询框的展开是通过执行
         JavaScript实现的。由于不同地方的查询框对应的ID不一样，所以展开查
         询框的时候先判断页面是否包含该查询框      --penghengkang   
    '''
    builtin = BuiltIn().get_library_instance('BuiltIn')
    selenium2lib = BuiltIn().get_library_instance('Selenium2Library')
    status = selenium2lib._is_element_present(locator)
    builtin.run_keyword_if(status, keyword , *args)    
    
def run_keyword_if_element_not_visible(locator, keyword, *args):
    '''
    Desc: 如果locator不可见，则运行keyword以及相关参数
    BTW: 将BuiltIn与Selenium2Library结合，以便简化脚本逻辑
         此功能需要robotframework2.7.5的支撑,详见robotframework-userguide
    '''
    builtin = BuiltIn().get_library_instance('BuiltIn')
    status = element_visible(locator)
    builtin.run_keyword_unless(status, keyword, *args)

def select_frame_by_chain(chain='default content'):
    '''
    Desc: 对于嵌套iframe default->a->b->c，执行select_frame_by_chain('a->b->c')
          过程是先switch_to_default_content()，然后再按顺序一层一层进入
    '''
    selenium2lib = BuiltIn().get_library_instance('Selenium2Library')
    frame_list = chain.split('->')
    selenium2lib._current_browser().switch_to_default_content()
    if chain == 'default content':
        return 
    for frame in frame_list:
        selenium2lib.select_frame(frame)
    
def record_iframe_list(from_default_content = 'True'):
    '''记录到Suite变量中，可以返回最后一个不是_uploadFrame的iframe id
    这里修改成，不再做增量添加了，调用时，每次都从default_content刷新，并取最后值
    '''
    selenium2lib = BuiltIn().get_library_instance('Selenium2Library')
    builtin = BuiltIn()
    browser = selenium2lib._current_browser()
    if from_default_content == 'True':
        browser.switch_to_default_content()
    iframe_elements = selenium2lib._element_find('xpath=//iframe',
                                                 first_only=False, 
                                                 required=True)
    if iframe_elements == None:
        return None
    iframes_id_list = []
    for li in iframe_elements:
        iframe_id = li.get_attribute('id')
        if iframe_id not in ['_uploadFrame','expIframe','hideFrame']:
            iframes_id_list.append('id=%s' % iframe_id)
            logger.debug('iframe id =  %s' % iframe_id)

    builtin.set_suite_variable('@{IFRAME_LIST}', iframes_id_list)
    logger.info(u'操作后，当前的@{IFRAME_LIST}: %s' % iframes_id_list)
    return iframes_id_list[-1]
    
def test_variable1():
     builtin = BuiltIn()
     tmp = builtin.get_variables()
     logger.info(tmp)
     v1 = builtin.get_variable_value('@{DYNAMIC_IFRAME_LIST}')
     logger.info('Get @{DYNAMIC_IFRAME_LIST} ==>> %s' % v1)

     new_list = [u'陈振武','a']
     builtin.set_test_variable('@{DYNAMIC_IFRAME_LIST2}', new_list)
     logger.info('SET @{DYNAMIC_IFRAME_LIST2} ==>> %s' % new_list)
     v2 = builtin.get_variable_value('@{DYNAMIC_IFRAME_LIST2}')
     logger.info('Get @{DYNAMIC_IFRAME_LIST2} ==>> %s' % v2)
     logger.info('builtin.set_test_variable()  only valid in current testcase')

def _get_screen_shot_name():
    '''截屏时，返回带日期的文件名，这里只返回文件名的字符串，不做截屏操作'''
    builtin = BuiltIn()
    timestr = datetime.datetime.now().strftime('%Y%m%d-%H%M%d-%f')[:-3]
    testsuit = builtin.get_variable_value('${SUITE_NAME}')
    testcase = builtin.get_variable_value('${TEST_NAME}')
    if testsuit == None:
        testsuit = "None"
    if testcase == None:
        testcase = "None"
    filename = '%s.%s.%s.png' % (testsuit,testcase,timestr)
    return filename

def capture_page_screenshot2():
    '''生成截屏文件：${SUIT_NAME}.${TEST_NAME}.timestamp.png

    举例：SIMS RIDE Demo.测试集.中文locator测试.20121205_133205.png
    BWT: 之所以单独放一个function，是减少log中一堆的合成字符串的日志
    '''
    filename = _get_screen_shot_name()
    selenium2lib = BuiltIn().get_library_instance('Selenium2Library')
    selenium2lib.capture_page_screenshot(filename)


def wait_until_ajax_load_complete(wait_str=u'正在加载内容...',timeout=15):
    '''根据传入ajax提示字符串，进行超时等待。超时时间为15s

    如果不传参数，则对以下几个字符串，分别等待15s 
    [ u'正在加载内容', u'正在向服务器发送请求']
    
    登录时采用的是//span, 而登录后进入某菜单用的是//div，所以两者同时处理
    '''
    selenium2lib = BuiltIn().get_library_instance('Selenium2Library')
    wait_str_list = [u'正在加载内容...', u'正在向服务器发送请求...']
    if wait_str not in  [None,u'']:
            element_xpath_div = u"xpath=//div[text()='%s']" % wait_str
            element_xpath_span = u"xpath=//span[text()='%s']" % wait_str
            selenium2lib.wait_until_page_not_contains_element(element_xpath_div, timeout)
            selenium2lib.wait_until_page_not_contains_element(element_xpath_span, timeout)
            logger.info(u'等待直到页面不存在字符串:[%s],  超时时间15s' % wait_str)
    else:
        for li in wait_str_list:
            element_xpath_div = u"xpath=//div[text()='%s']" % li
            element_xpath_span = u"xpath=//span[text()='%s']" % li
            selenium2lib.wait_until_page_not_contains_element(element_xpath_div, timeout)
            selenium2lib.wait_until_page_not_contains_element(element_xpath_span, timeout)
            logger.info(u'等待直到页面不存在字符串:[%s],  超时时间15s' % li)
    
def click_menu_chains(menuchain=u'SP信用积分与投诉管理->履约情况->短信->出席会议情况'):
    selenium2lib = BuiltIn().get_library_instance('Selenium2Library')
    browser = selenium2lib._current_browser()
    browser.switch_to_default_content()
    browser_name = browser.capabilities.get('browserName')
    menulist = menuchain.split('->')
    for li in range(1,3):
        if  selenium2lib._is_visible(u"//div[@class='x-layout-collapsed x-layout-collapsed-west x-layout-cmini-west']"):
            logger.info('因发现有menu分隔线，所以点击分隔线')
            selenium2lib.click_element(u"//div[@class='x-layout-collapsed x-layout-collapsed-west x-layout-cmini-west']")
    for menu in menulist[:-1]:
        current_menu_index = menulist.index(menu)
        fullpath = u"xpath=//" + u"/parent::a/parent::div/parent::li/ul/li/div/a/".join( \
                        [u"span[text()='%s']" % li for li in menulist[:current_menu_index+1]])
        fullpath_next = u"xpath=//" + u"/parent::a/parent::div/parent::li/ul/li/div/a/".join( \
                        [u"span[text()='%s']" % li for li in menulist[:current_menu_index+2]])
        for iter in range(1,10):    #每个菜单上最多停2秒,这个好象没有起到作用
            if not selenium2lib._is_visible(fullpath) : 
                logger.debug(u'menu %s 未发现，sleep 0.2秒' % menu)
                time.sleep(0.2)
            else:
                break
        #if browser_name=='chrome':
        #    time.sleep(0.2)
        if not selenium2lib._is_visible(fullpath_next):
            selenium2lib.click_element(fullpath)
            if selenium2lib._is_visible(u"xpath=//div[contains(@class,'x-window-dlg')]"):
                dlg_info_element = selenium2lib._element_find("//div[contains(@class,'x-window-dlg')]//span[@class='ext-mb-text']",first_only=True, required=False)
                logger.info(u"出现提示窗口,提示信息为:%s" % dlg_info_element.text)
                selenium2lib.click_element(u"xpath=//div[contains(@class,'x-window-dlg')]//button[text()='是']")
    if browser_name in ['chrome','firefox']:         
        time.sleep(0.2)
    lastframe = ''
    for li in range(1,3):
        fullxpath = u"xpath=//" + u"/parent::a/parent::div/parent::li/ul/li/div/a/".join([u"span[text()='%s']" % li for li in menulist])
        logger.debug('last menu xpath : %s'  % fullxpath)
        #selenium2lib.click_element(u"xpath=//span[text()='%s']" % menu)
        if not selenium2lib._is_visible(fullpath):
            time.sleep(0.2)
        selenium2lib.click_element(fullxpath)
        if selenium2lib._is_visible(u"xpath=//div[contains(@class,'x-window-dlg')]"):
            dlg_info_element = selenium2lib._element_find("//div[contains(@class,'x-window-dlg')]//span[@class='ext-mb-text']",first_only=True, required=False)
            logger.info(u"出现提示窗口,提示信息为:%s" % dlg_info_element.text)
            selenium2lib.click_element(u"xpath=//div[contains(@class,'x-window-dlg')]//button[text()='是']")
        wait_until_ajax_load_complete(u'正在加载内容...')
        lastframe = record_iframe_list()
        if  lastframe != 'iframe-homepage':
            break
    wait_until_ajax_load_complete(u'正在加载内容...')
    selenium2lib.select_frame(lastframe)
    #实际操作时发现，如果不做第二次ajax等待的话，实际的界面仍在查询的mask提示中。 做两次看起来重复，减少了很多不必要的错误，而且后续操作没有必要立即加上wait的动作
    wait_until_ajax_load_complete(u'正在加载内容...')

def get_datalist_from_table():
    '''返回table中的所有内容数据，形成列表，例如[[第1行第1列，第1行第2列,....],[第2行第1列,第2行第2列]]
    并设置到@{TABLE_DATALIST}的test变量中
    '''
    selenium2lib = BuiltIn().get_library_instance('Selenium2Library')
    builtin = BuiltIn()
    #var_table_datalist = builtin.get_variable_value('@{TABLE_DATALIST}')
    rows = selenium2lib._element_find("//div[contains(@class, 'x-grid3-row')]",first_only=False, required=False)
    result_list = []
    if rows not in [None,[]]:
        for row in rows:
            row_data_list = row.text.split('\n')
            #logger.debug('row_data_list: %s' % row_data_list)
            result_list.append(row_data_list)
    #logger.debug(result_list)
    builtin.set_test_variable('@{TABLE_DATALIST}', result_list)
    return result_list

def table_row_assert(row_condition='1:abc$$2:cba', value='3:456$$4:789'):
    builtin = BuiltIn()
    datalist = []
    var_table_datalist = builtin.get_variable_value('@{TABLE_DATALIST}')
    if var_table_datalist not in [None,[]]:
        datalist = var_table_datalist[0]
    else:
        datalist = get_datalist_from_table()
    condition_list = row_condition.split('$$')
    arg_list = []
    for li in condition_list:
        col_num = int(li.split(':')[0]) - 1
        col_value = li.split(':')[1]
        arg_list.append([col_num,col_value])
    line  = None
    for li in datalist:
        #所有条件都满足了，则为此行
        
        for ll in arg_list:
            if li[ll[0]] == col_value:
                pass
            else:
                break

                
#def execute_javascript2(element_xpath):
#    selenium2lib = BuiltIn().get_library_instance('Selenium2Library')
#    element =  selenium2lib._element_find(element_xpath,first_only=True, required=True)
    
        
    
def param_value(one_param):
    '''主要用于传参使用，例如get_param_value('argA=v1'), return v1。 
    robot框架本身在传参时，将会把argA=v1的unicode串传到后面的keyword中，
    经测试，如果作为变量传递时，locator,以及判断语句时，不是取的v1,而为整个串。
    此处只是简单split取last元素, 此功能对于新版本的robotframework已无用'''
    if one_param == None:
        return None
    else:
        return one_param.split('=')[-1].strip()
    
    
def get_current_dropdown_list():
    '''下拉框列表是动态产生的，连id都是动态的。
       这里通过祖元素的style中包含visible串来判断，并返回当前下拉框的item列表
       xpath模式如下：
            xpath=//div[contains(@style,"visible")]/div[@class="x-combo-list-inner"]/div[contains(@class,"x-combo-list-item")]
    '''
    selenium2lib = BuiltIn().get_library_instance('Selenium2Library')
    builtin = BuiltIn()
    browser = selenium2lib._current_browser()

    var_current_dropdown_list = builtin.get_variable_value('@{CURRENT_DROPDOWN_LIST}')
    current_item_elements = selenium2lib._element_find('xpath=//div[contains(@style,"visible")]/div[@class="x-combo-list-inner"]/div[contains(@class,"x-combo-list-item")]',
                                                 first_only=False, 
                                                 required=False)
    item_list = []
    for li in current_item_elements:
        item_text = li.text
        item_list.append(item_text)
        logger.debug('dropdown list item text()=  %s' % item_text)

    return item_list    
    
def download_file_by_url(url, abs_filename):
    if not url.startswith('http://'):
        selenium2lib = BuiltIn().get_library_instance('Selenium2Library')
        #browser = selenium2lib._current_browser() 
        location = selenium2lib.get_location()
        location_list = location.split('/')
        url = 'http://'+ location_list[2] + url
    logger.info(u'下载文件， 另存为%s, URL：%s' % (abs_filename, url))
    somelist = url.split('/')
    host_port = somelist[2]
    abs_url = '/' + '/'.join(somelist[3:])
    httpclient = httplib.HTTPConnection(host_port)
    httpclient.request("GET", abs_url)
    response = httpclient.getresponse()
    content_type = response.getheader('content-type')
    content = response.read()
    if os.path.exists(abs_filename):
        os.remove(abs_filename)
    mode='w+'
    # excel文件为application/vnd.ms-excel
    if content_type.startswith('application'):
        mode='wb+'
    open(abs_filename,mode).write(content)

def parse_xml_gb2312(str_or_file):
    '''返回root'''
    xmlstr = ''
    if str_or_file.lstrip(' ').startswith('<'):
        xmlstr = str_or_file.replace('gb2312','utf-8').replace('GB2312','utf-8').decode('gbk').encode('utf-8')
    else:
        xmlstr = ''.join([li for li in open(str_or_file,'r+').readlines() if not li.startswith('<?xml')]).decode('gbk').encode('utf-8')
    root = ET.fromstring(xmlstr)
    return root

def select_frame_until_element_visible(frame_locator, element_locator, iter_count=15, sleep_time=1):
    """多次select frame,直到frame中的元素可见
    """
    builtin = BuiltIn().get_library_instance('BuiltIn')
    selenium2lib = BuiltIn().get_library_instance('Selenium2Library')
    iframe_finder = selenium2lib._element_find(frame_locator, True, True)
    if iframe_finder != None:
        selenium2lib.select_frame(frame_locator)
    for li in range(1,int(iter_count)):
        subelement_finder = selenium2lib._element_find(element_locator, True, False)
        iframe_finder = selenium2lib._element_find(frame_locator, True, False)
        if subelement_finder != None:
            logger.info(u'找到子元素，直接返回')
            return
        logger.info(u'重新重试的重试次数为:%s' % li)
        iframe_finder = selenium2lib._element_find(frame_locator, True, False)
        if iframe_finder == None:
            logger.info(u'未找到子元素，但检查iframe时发现已经进入了iframe,所以只能等 %s 秒' % sleep_time)
            pass
        else:
            logger.info(u'未找到子元素，但检查iframe时未进入了iframe,所以重新select该frame:%s,再等 %s 秒' % (frame_locator,sleep_time))
            selenium2lib.select_frame(frame_locator)
        time.sleep(float(sleep_time))
    return     
    
def open_or_reuse_browser(url, browser='firefox', alias=None,remote_url=False,
                desired_capabilities=None,ff_profile_dir=None):
    '''新开一个浏览器，或者重用当前已有的浏览器，主要用于处理setup时已有浏览器的情况'''
    selenium2lib = BuiltIn().get_library_instance('Selenium2Library')
    open_browser_list = selenium2lib._cache.get_open_browsers()
    if open_browser_list != []:
        browser = selenium2lib._current_browser()
    else:
        logger.debug(u'没有已打开的浏览器,只能new一个')
        browser = selenium2lib._make_browser(browser,desired_capabilities,ff_profile_dir,remote_url)
        selenium2lib._cache.register(browser, alias)
    browser.get(url)

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
            