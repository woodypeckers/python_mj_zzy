#-*- coding:utf-8 -*- 
import tornado.web
import tornado.httpclient
from utils.logger import logger

#本接口实现作为client端发起的Handler
#在Migu_PRM的结算接口中，没有使用到，删除这个文件也没有多大关系，实际上没有什么用
class ClientHandler(tornado.web.RequestHandler):

    def post(self):
        '''需要发送的URL直接在headers['To-Url']中获取
           发起时头也直接从req头中获取
           发起POST请求后，得到的Response包头和包体原封不动，返回
           此过程不存储任何东东
        '''
        to_url = self.request.headers['To-Url']
        logger.info('ClientHandler-- 要求发起http client请求')
        logger.info('To-Url:%s' % to_url)
        req_str = self.request.body
        req_headers_dict = self.request.headers
        logger.info('org headers:\n%s' % req_headers_dict)
        logger.info('org body:\n%s' % req_str)
        try:
            http_client = tornado.httpclient.HTTPClient()
            http_request = tornado.httpclient.HTTPRequest(to_url,
                            method='POST',body=req_str,
                            headers=req_headers_dict)
            respObj = http_client.fetch(http_request)
            resp_str = respObj.body
            resp_headers_dict = respObj.headers
            logger.info('resp_headers:\n%s' % resp_headers_dict)
            logger.info('resp_str:\n%s' % resp_str)
        except Exception,e1:
            Desc = 'HTTP连接错误, exception信息为:%s' % e1
            self.write(Desc)
            return
        for head_name, head_value in resp_headers_dict.iteritems():
            self.set_header(head_name, head_value)
        self.write(resp_str)      

    


     