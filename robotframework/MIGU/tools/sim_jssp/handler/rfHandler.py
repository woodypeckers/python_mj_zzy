#-*- coding:utf-8 -*- 
import json
import tornado.ioloop
import tornado.web
from utils.logger import logger
from global_v import G_state_dict

##########################################
# 下面接口是给robotframework使用的，主要功能是获取信息和设置信息
##########################################       
class RFGetHandler(tornado.web.RequestHandler):
    def get(self):
        ''' get?var_name=XXXX&contentCode=YYYYY&transId=NNN
        如果transId=last，则取List的最后一条信息中的body'''
        #global G_state_dict
        params = self.request.arguments
        key = params['var_name'][0]
        value = 'None'
        if key.endswith('List'):         
            somelist = key
            transId = params['transId'][0]
            contentCode = params['contentCode'][0]
            if transId == 'last':                     #last则为最后一条数据
                if G_state_dict[somelist] == []:
                    self.write('No item in %s' % somelist)
                    return
                value = G_state_dict[somelist][-1]['req_str']
            else:
                tmp_list = G_state_dict[somelist]
                for li in tmp_list:
                    if li['transId']==transId and li['contentCode']==contentCode:
                        value = li['req_str']
                        break
        else:
            value = G_state_dict[key]
        if value.find('{') != -1:
            self.set_header('Content-Type', 'text/json')
        else:
            self.set_header('Content-Type', 'text/plain')
        self.write(value)
        

class RFSetHandler(tornado.web.RequestHandler):
    def get(self):
        ''' set?var_name=XXXX&var_value=NNN'''
        #global G_state_dict
        params = self.request.arguments
        key = params['var_name'][0]
        value = '0'
        #如果是对G_Request_List或者G_token_list操作，不用看var_value了，直接置[]
        if key == 'G_Request_List' :
            G_state_dict[key] = []
        #special_response_body在传过来时，如果是str类型的None,直接设置为None
        elif key == 'Special_Response_Body' and params['var_value'][0] == 'None':
            G_state_dict.update({key:None})
        else:
            value = params['var_value'][0]
            G_state_dict.update({key:value})
        self.set_header('Content-Type', 'text/plain')
        self.write('OK')        

    def post(self):
        '''set?var_name=XXX, 
        例如set?var_name=Special_Response_Body
        其实post接口可以接受一个json包
        '''
        #global G_state_dict
        params = self.request.arguments
        key = params['var_name'][0]
        req_headers = self.request.headers
        G_state_dict[key] = self.request.body

        resp_body='set Global G_state_dict["Special_Response_Body"] OK!'
        self.set_header('Content-Type', 'text/plain')
        self.write(resp_body)