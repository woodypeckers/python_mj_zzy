#-*- coding:utf-8 -*- 
'''模拟器作为Server端需要完成的各接口处理Handler'''
import json
import tornado.web
from utils.logger import logger
from global_v import G_state_dict
from  models import *
from tornado import gen
#from tornado import asynchronous



# 通用功能，打印请求包的包头和包体
def log_request(request):
    req_headers = request.headers
    req_str = request.body
    try:
        req_obj = json.loads(req_str.decode('utf-8'))
    except Exception,e:
        #非json格式
        #如果是采用post body为&分隔的参数，则改一下：req_obj = req_str.lstrip(body=).split('&') 变成key=value的字符串List
        req_obj={}
        tmp_list = [li for li in req_str.split('&')]
        for li in tmp_list:
            key= li.split('=')[0]
            value= li.split('=')[1]
            req_obj.setdefault(key,value)
    

    logger.info('收到 HTTP POST Request---------------')
    logger.info('HTTP POST Package Headers：\r\n%s' % req_headers)
    logger.info('HTTP POST Package Body:\r\n%s' % req_str)
    return req_obj

def log_response(resp_str):
    logger.info('返回包体----------------:\n%s' % resp_str)

#1. 实时账单接口
class GetBillHandler(tornado.web.RequestHandler):
    #@asynchronous
    @gen.coroutine
    def post(self):
        req_obj = log_request(self.request)
        print req_obj
        if 'start_month' in req_obj.keys():
            start_month = req_obj["start_month"]
        else:
            start_month = '201001'
        #start_month = req_obj["start_month"]
        if 'end_month' in req_obj.keys():
            end_month = req_obj["end_month"]
        else:
            end_month = '209910'
        #end_month = req_obj["end_month"]
        if 'sett_id' in req_obj.keys():
            sett_id = '%'+req_obj["sett_id"]
        else:
            sett_id = '%%'
        #sett_id = req_obj["sett_id"]
        if 'sett_type'  in req_obj.keys():
            sett_type = req_obj["sett_type"]
        else:
            sett_type = '%%'
        #sett_type = req_obj["sett_type"]
        if 'sett_name' in req_obj.keys():
            sett_name = req_obj["sett_name"]
        else:
            sett_name='%%'
        #jssp_flag = req_obj["jssp_flag"]
        if 'sett_flag' in req_obj.keys():
            sett_flag = req_obj["sett_flag"]
        else:
            sett_flag = '1'
        #sett_flag = req_obj["sett_flag"]
        if 'page_current' in req_obj.keys():
            page_current = req_obj["page_current"]
        else:
            page_current = 1
        if 'page_size'  in req_obj.keys():
            page_size = req_obj["page_size"]
        else:
            page_size=10000
        
        #这里写逻辑

        (total_size,bill_list) = query_bill_list(sett_id=sett_id,start_month=start_month,stop_month=end_month,
                                    sett_type=sett_type,sett_name=sett_name.decode('utf-8'),
                                    page_current=page_current, page_size=page_size)
        #由列表生成返回包:
        if bill_list == []:
            resp_str = '''{ "flag": "false", "reason": "响应异常"}'''
        else:
            data_str = pin_data_str(bill_list)
            #print data_str
            resp_str = '''{ 
	"flag": "true",
	"totalSize": "%s",
	"data": [
        %s
	]
}
'''  % (total_size, data_str)
        resp_str = json_format(resp_str,encoding='utf-8')
        self.set_header('Content-Type','application/x-www-form-urlencoded')
        self.set_header('Content-Length',len(resp_str))
        self.write(resp_str)
        log_response(resp_str)
       
 
#2. 暂停信息获取接口        
class getPauseInfoHandler(tornado.web.RequestHandler):
    def post(self):
        '''这个接口比较简单,单值返回，所以后面的基本上都以这个模式来处理就行了'''
        req_obj = log_request(self.request)
        sett_month = req_obj["sett_month"]
        sett_id = req_obj["sett_id"]
        obj = query_pause_info(sett_month,sett_id)
        if obj == None:
            resp_str = '''{ "flag": "false", "reason": "响应异常"}'''
        else:
            resp_str = '''{"flag": "true","data":{ 
		"pause_type": "%s",
	"sett_id": "%s",
	"sett_month": "%s",
	"recovery_month": "%s",
	"comments": "%s"
		}
}''' % (obj.pause_type.encode('utf-8'),obj.sett_id.encode('utf-8'),obj.sett_month.encode('utf-8'),
        obj.recovery_month.encode('utf-8'),obj.comments.encode('utf-8'))

        resp_str = json_format(resp_str,encoding='utf-8')
        self.set_header('Content-Type','application/x-www-form-urlencoded')
        self.set_header('Content-Length',len(resp_str))
        self.write(resp_str)
        log_response(resp_str)

#3. 实时账单明细接口
class getBillDetailHandler(tornado.web.RequestHandler):
    def post(self):
       req_obj = log_request(self.request)
       sett_id = req_obj["sett_id"]
       sett_month = req_obj["sett_month"]
       obj = query_bill_detail(sett_month,sett_id)
       if obj == None:
            resp_str = '''{ "flag": "false", "reason": "响应异常"}'''
       else:
			resp_str = '''{"flag": "true","data":{
			"sett_id": "%s",
		    "sett_name": "%s",
		    "fee_hf": "%s",
		    "fee_fhf": "%s",
		    "fee_dl": "%s",
		    "fee_vgop": "%s",
		    "fee_kh": "%s",
		    "fee_tz": "%s",
		    "fee_sett": "%s",
		    "vatrate": "%s",
		    "fee_exvat": "%s",
		    "fee_vat": "%s",
		    "fee_invat": "%s",
		    "payable_vat":"%s"
			}
			}''' % (obj.sett_id.encode('utf-8'),obj.sett_name.encode('utf-8'),obj.fee_hf.encode('utf-8')\
			,obj.fee_fhf.encode('utf-8'),obj.fee_dl.encode('utf-8'),obj.fee_vgop.encode('utf-8'),obj.fee_kh.encode('utf-8')\
			,obj.fee_tz.encode('utf-8'),obj.fee_sett.encode('utf-8'),obj.vatrate.encode('utf-8'),obj.fee_exvat.encode('utf-8')\
			,obj.fee_vat.encode('utf-8')\
			,obj.fee_invat.encode('utf-8')\
			,obj.payable_vat.encode('utf-8'))
       resp_str = json_format(resp_str,encoding='utf-8')
       self.set_header('Content-Type','application/x-www-form-urlencoded')
       self.set_header('Content-Length',len(resp_str))
       self.write(resp_str)
       log_response(resp_str)
 

      

#4. 实时账单话费类接口
class getBillDetailHfHandler(tornado.web.RequestHandler):
    def post(self):
        req_obj = log_request(self.request)
        sett_id = req_obj["sett_id"]
        sett_month = req_obj["sett_month"]
        sett_type = req_obj["sett_type"]
        page_current = req_obj["page_current"]
        page_size = req_obj["page_size"]
        
        #这里写逻辑

        (total_size,bill_list) = query_bill_DetailHf(sett_id=sett_id,sett_month=sett_month,sett_type=sett_type,page_current=page_current, page_size=page_size)
        #由列表生成返回包:
        if bill_list == []:
            resp_str = '''{ "flag": "false", "reason": "响应异常"}'''
        else:
            data_str = pin_data_str_hf(bill_list)
            resp_str = '''{ 
	"flag": "true",
	"totalSize": "%s",
	"data": [
        %s
	]
}
'''  % (total_size, data_str)
        resp_str = json_format(resp_str,encoding='utf-8')
        self.set_header('Content-Type','application/x-www-form-urlencoded')
        self.set_header('Content-Length',len(resp_str))
        self.write(resp_str)
        log_response(resp_str)
       
       

#5. 实时账单非话费类接口
class getBillDetailFhfHandler(tornado.web.RequestHandler):
    def post(self):
        req_obj = log_request(self.request)
        sett_id = req_obj["sett_id"]
        sett_month = req_obj["sett_month"]
        sett_type = req_obj["sett_type"]
        page_current = req_obj["page_current"]
        page_size = req_obj["page_size"]
        
        #这里写逻辑
        (total_size,bill_list) = query_bill_DetailFHf(sett_id=sett_id,sett_month=sett_month,sett_type=sett_type,page_current=page_current, page_size=page_size)
        #由列表生成返回包:
        if bill_list == []:
            resp_str = '''{ "flag": "false", "reason": "响应异常"}'''
        else:
            data_str = pin_data_str_fhf(bill_list)
            resp_str = '''{ 
	"flag": "true",
	"totalSize": "%s",
	"data": [
        %s
	]
}
'''  % (total_size, data_str)
        resp_str = json_format(resp_str,encoding='utf-8')
        self.set_header('Content-Type','application/x-www-form-urlencoded')
        self.set_header('Content-Length',len(resp_str))
        self.write(resp_str)
        log_response(resp_str)
       
       

#6. 实时账单代理收入接口
class getBillDetailDlHandler(tornado.web.RequestHandler):
    def post(self):
        req_obj = log_request(self.request)
        sett_id = req_obj["sett_id"]
        sett_month = req_obj["sett_month"]
        page_current = req_obj["page_current"]
        page_size = req_obj["page_size"]
        
        #这里写逻辑
        (total_size,bill_list) = query_bill_DetailDl(sett_id=sett_id,sett_month=sett_month,page_current=page_current, page_size=page_size)
        #由列表生成返回包:
        if bill_list == []:
            resp_str = '''{ "flag": "false", "reason": "响应异常"}'''
        else:
            data_str = pin_data_str_dl(bill_list)
            resp_str = '''{ 
	"flag": "true",
	"totalSize": "%s",
	"data": [
        %s
	]
}
'''  % (total_size, data_str)
        resp_str = json_format(resp_str,encoding='utf-8')
        self.set_header('Content-Type','application/x-www-form-urlencoded')
        self.set_header('Content-Length',len(resp_str))
        self.write(resp_str)
        log_response(resp_str)
       
       
  
        
        

##结算拼串
def pin_data_str(bill_list):
    '''拼串'''
    result_list = []
    for li in bill_list:
        sett_month = li.sett_month.encode('utf-8')
        sett_id = li.sett_id.encode('utf-8')
        jssp_flag = li.jssp_flag.encode('utf-8')
        fee_invat = li.fee_invat
        tax_rate = li.tax_rate
        sett_flag = li.sett_flag.encode('utf-8')
        comments = li.comments.encode('utf-8')
        update_time = li.update_time.encode('utf-8')
        sett_name = li.sett_name.encode('utf-8')
        result_list.append('''"sett_month": "%s","sett_id": "%s","jssp_flag": "%s","fee_invat": %0.2f,"tax_rate": "%0.2f","sett_flag": "%s","comments": "%s","update_time": "%s","sett_name":"%s"''' % (sett_month,sett_id,jssp_flag,fee_invat,tax_rate,sett_flag,comments,update_time,sett_name))
    print result_list
    if result_list == []:
           result = ""
    else:
           result = "{" + "},{".join(result_list) + "}"
    return result

##话单类拼串
def pin_data_str_hf(bill_list):
    '''拼串'''
    result_list = []
    for li in bill_list:
        sett_month = li.sett_month.encode('utf-8')
        sett_id = li.sett_id.encode('utf-8')
        sett_type = li.sett_type.encode('utf-8')
        sett_name = li.sett_name.encode('utf-8')
        content_id = li.content_id.encode('utf-8')
        content_name = li.content_name.encode('utf-8')
        sub_ch_code = li.sub_ch_code.encode('utf-8')
        sub_ch_name = li.sub_ch_name.encode('utf-8')
        dis_info_fees = li.dis_info_fees.encode('utf-8')
        audit_fee = li.audit_fee.encode('utf-8')
        js_ratio = li.js_ratio.encode('utf-8')
        js_yj_settfee = li.js_yj_settfee.encode('utf-8')
        result_list.append('''"sett_month": "%s","sett_id": "%s","sett_type ": "%s","sett_name": "%s","content_id": "%s","content_name": "%s","sub_ch_code": "%s","sub_ch_name": "%s"\
        ,"dis_info_fees": "%s","audit_fee": "%s","js_ratio": "%s","js_yj_settfee": "%s"'''% (sett_month,sett_id,sett_type,sett_name,content_id,content_name,sub_ch_code\
        ,sub_ch_name,dis_info_fees,audit_fee,js_ratio,js_yj_settfee))
    result = "{" + "},{".join(result_list) + "}"
    return result

##非话单类拼串
def pin_data_str_fhf(bill_list):
    '''拼串'''
    result_list = []
    for li in bill_list:
        sett_month = li.sett_month.encode('utf-8')
        sett_id = li.sett_id.encode('utf-8')
        sett_type = li.sett_type.encode('utf-8')
        sett_name = li.sett_name.encode('utf-8')
        content_id = li.content_id.encode('utf-8')
        content_name = li.content_name.encode('utf-8')
        sub_ch_code = li.sub_ch_code.encode('utf-8')
        sub_ch_name = li.sub_ch_name.encode('utf-8')
        dis_info_fees = li.dis_info_fees.encode('utf-8')
        audit_fee = li.audit_fee.encode('utf-8')
        js_ratio = li.js_ratio.encode('utf-8')
        js_yj_settfee = li.js_yj_settfee.encode('utf-8')
        result_list.append('''"sett_month": "%s","sett_id": "%s","sett_type ": "%s","sett_name": "%s","content_id": "%s","content_name": "%s","sub_ch_code": "%s","sub_ch_name": "%s"\
        ,"dis_info_fees": "%s","audit_fee": "%s","js_ratio": "%s","js_yj_settfee": "%s"'''% (sett_month,sett_id,sett_type,sett_name,content_id,content_name,sub_ch_code\
        ,sub_ch_name,dis_info_fees,audit_fee,js_ratio,js_yj_settfee))
    result = "{" + "},{".join(result_list) + "}"
    return result

##实时账单代理
def pin_data_str_dl(bill_list):
    '''拼串'''
    result_list = []
    for li in bill_list:
        sett_month = li.sett_month.encode('utf-8')
        dl_comp = li.dl_comp.encode('utf-8')
        month_id = li.month_id.encode('utf-8')
        cp_code = li.cp_code.encode('utf-8')
        cp_name = li.cp_name.encode('utf-8')
        oper_code = li.oper_code.encode('utf-8')
        oper_name = li.oper_name.encode('utf-8')
        info_fee = li.info_fee.encode('utf-8')
        result_list.append('''"sett_month": "%s","dl_comp": "%s","month_id": "%s","cp_code": "%s","cp_name": "%s","oper_code": "%s","oper_name": "%s"\
        ,"info_fee": "%s"'''% (sett_month,dl_comp,month_id,cp_code,cp_name,oper_code\
        ,oper_name,info_fee))
    result = "{" + "},{".join(result_list) + "}"
    return result
def json_format(somestr,encoding='utf-8'):
    json_obj=json.loads(somestr)
    return json.dumps(json_obj,sort_keys=False,indent=4).decode("unicode-escape").encode(encoding)