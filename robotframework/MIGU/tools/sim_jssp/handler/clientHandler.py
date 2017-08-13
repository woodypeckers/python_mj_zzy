#-*- coding:utf-8 -*- 
import tornado.web
import tornado.httpclient
from utils.logger import logger

#���ӿ�ʵ����Ϊclient�˷����Handler
#��Migu_PRM�Ľ���ӿ��У�û��ʹ�õ���ɾ������ļ�Ҳû�ж���ϵ��ʵ����û��ʲô��
class ClientHandler(tornado.web.RequestHandler):

    def post(self):
        '''��Ҫ���͵�URLֱ����headers['To-Url']�л�ȡ
           ����ʱͷҲֱ�Ӵ�reqͷ�л�ȡ
           ����POST����󣬵õ���Response��ͷ�Ͱ���ԭ�ⲻ��������
           �˹��̲��洢�κζ���
        '''
        to_url = self.request.headers['To-Url']
        logger.info('ClientHandler-- Ҫ����http client����')
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
            Desc = 'HTTP���Ӵ���, exception��ϢΪ:%s' % e1
            self.write(Desc)
            return
        for head_name, head_value in resp_headers_dict.iteritems():
            self.set_header(head_name, head_value)
        self.write(resp_str)      

    


     