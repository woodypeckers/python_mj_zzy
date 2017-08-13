#-*- coding:utf-8 -*-
'''本文件的初始想法，是在robotframework的外部打补丁,
这样未来可以不用再修改robotframework中的内容,
修订全部集中在这个文件中

新增方法：新增方法也是一样的，只不过原来的类中可能没有这个方法
    例如：　前面先实现new_method(self,xxx),然后
            SomeClass.new_method = new_method
删除方法：例如　del SomeClass.method

对于非类实现，module相当于类；
对于包中加类，操作方式应该是类似的。
'''
from robot.api import logger


'''robotframework'''
#解决output.xml中的msg中的参数部分，中文列表常显示的是\uxxxx\uxxxx，看不明白的问题
from robot.output.xmllogger import XmlLogger
def xmllogger_write_message(self, msg):
    attrs = {'timestamp': msg.timestamp or 'N/A', 'level': msg.level}
    if msg.html:
        attrs['html'] = 'yes'
    #patch add two lines
    if msg.message.find('\u') != -1:
        try:
            msg.message = msg.message.decode('unicode-escape')
        except Exception,e:
            pass
    #patch end
    self._writer.element('msg', msg.message, attrs)

XmlLogger._write_message = xmllogger_write_message


#解决 Oracle返回的失败信息中一堆的\xNNNN的内容，原来是gbk的编码
from robot.utils import unic
def unic(item):
    if isinstance(item, unicode):
        return item
    if isinstance(item, (bytes, bytearray)):
        try:
            #return item.decode('ASCII')
            return item.decode('cp936')
        except UnicodeError:
            return u''.join(chr(b) if b < 128 else '\\x%x' % b
                            for b in bytearray(item))
    try:
        try:
            return unicode(item)
        except UnicodeError:
            return unic(str(item))
    except:
        return _unrepresentable_object(item)
unic.unic = unic


'''Selenim2Library'''
#解决selenium2library中的失败时截屏，文件名中加入时间串，防止大规模并行时截屏合并导致的相互覆盖
try:
    from Selenium2Library.keywords._screenshot import _ScreenshotKeywords
    import datetime,random,os,robot
    def _get_screenshot_paths(self, filename):
        if not filename:
            self._screenshot_index += 1
            # start
            timestr = datetime.datetime.now().strftime('%Y%m%d-%H%M%d-%f')[:-3]
            randstr = random.randint(1,9999)
            filename = 'selenium-screenshot-%s-%d-%d.png' % (timestr,self._screenshot_index,randstr)
            # end
        else:
            filename = filename.replace('/', os.sep)
        logdir = self._get_log_dir()
        path = os.path.join(logdir, filename)
        link = robot.utils.get_link_path(path, logdir)
        return path, link  
    _ScreenshotKeywords._get_screenshot_paths = _get_screenshot_paths
except Exception,e:
    pass

'''HttpLibrary'''
try:    
    #解决HttpLibrary POST包会自动encoding成UTF-8的问题
    import HttpLibrary
    from HttpLibrary import HTTP
    def set_request_body_patch(self, body):
        """
        Set the request body for the next HTTP request.
         Example:
        | Set Request Body           | user=Aladdin&password=open%20sesame |
        | POST                       | /login                              |
        | Response Should Succeed  |                                     |
        """
        logger.info('Request body set to "%s".' % body)
        #self.context.request_body = body.encode("utf-8")
        if self.context.request_body_encoding == None:
            self.context.request_body_encoding = "utf-8"
        self.context.request_body = body.encode(self.context.request_body_encoding)
    HTTP.set_request_body = set_request_body_patch

    from robot.libraries.BuiltIn import BuiltIn
    from robot.api import logger
    def set_httplibrary_request_encoding(encoding):
        """在原有的库上加方法，根据RF当前的情况，是没有办法直接patch的，所以采用mylibrary的方式处理
        """
        builtin = BuiltIn().get_library_instance('BuiltIn')
        httplib = BuiltIn().get_library_instance('HttpLibrary.HTTP')
        logger.info('***********')
        logger.info(dir(httplib))
        httplib.context.request_body_encoding = encoding
        logger.info(httplib)
        logger.info(httplib.context.request_body_encoding)

    #解决HttpLibrary POST时，由于RF传入unicode导致的msg+=msg失败问题
    from HttpLibrary.livetest import TestApp
    import webtest
    def _do_httplib_request_patch(self, req):
        "Convert WebOb Request to httplib request."
        #headers = dict((name, val) for name, val in req.headers.iteritems())
        headers = dict((str(name), str(val)) for name, val in req.headers.iteritems())
        if req.scheme not in self.conn:
            self._load_conn(req.scheme)
        conn = self.conn[req.scheme]
        conn.request(req.method, req.path_qs, req.body, headers)
        webresp = conn.getresponse()
        res = webtest.TestResponse()
        res.status = '%s %s' % (webresp.status, webresp.reason)
        res.body = webresp.read()
        response_headers = []
        for headername in dict(webresp.getheaders()).keys():
            for headervalue in webresp.msg.getheaders(headername):
                response_headers.append((headername, headervalue))
        res.headerlist = response_headers
        res.errors = ''
        return res
    TestApp._do_httplib_request = _do_httplib_request_patch
except Exception,e:
    pass
'''paramiko patch '''
try:
    import paramiko.file
    def paramiko_file_u_patch(s, encoding='utf-8'):  # NOQA
        """cast bytes or unicode to unicode"""
        if isinstance(s, str):
            try:
                return s.decode(encoding)
            except UnicodeDecodeError,e:
                # If client $LANG is GBK, such as "zh_CN.GB18030"
                # decode('utf8') should throwgh Unicode Exception
                # So decode('gbk') is often in Chinese Envirment
                return s.decode('gbk')
        elif isinstance(s, unicode):
            return s
        elif isinstance(s, buffer):
            return s.decode(encoding)
        else:
            raise TypeError("Expected unicode or bytes, got %r" % s)
    paramiko.file.u = paramiko_file_u_patch
except Exception,e:
    pass
    
'''ride patch'''
try:
    #解决运行时总是报UnicodeDecodeError的问题
    from  robotide.contrib.testrunner.testrunner import StreamReaderThread
    def robotide_pop_patch(self):
        result = ""
        for _ in xrange(self._queue.qsize()):
            try:
                result += self._queue.get_nowait()
            except Empty:
                pass
        try:
            result = result.decode('GBK').encode('UTF-8')
        except:
            pass
        return result.decode('UTF-8')
    StreamReaderThread.pop = robotide_pop_patch
except Exception,e:
    pass    