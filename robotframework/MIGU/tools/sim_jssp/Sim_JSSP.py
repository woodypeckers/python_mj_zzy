#-*- coding:utf-8 -*- 
'''目标：模拟器　for MIGU PRM结算模拟
总共６个接口，逻辑全部写在handler/serverhandler.py中
'''
import tornado.ioloop
import tornado.web
from tornado.options import options
import signal
from utils.logger import logger
from handler.serverHandlers import *
from handler.clientHandler import ClientHandler
from handler.rfHandler import RFSetHandler, RFGetHandler
from global_v import G_state_dict

is_closing = False

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        '''这个页面用于查全局变量G_state_dict，不需要任何改动！'''
        for var_name,var_value in G_state_dict.iteritems():
            if var_name.lower().find('list') == -1:
                self.write("<h3>%s:%s</h3>" % (var_name,var_value))
        for var_name,var_value in G_state_dict.iteritems():
            if var_name.lower().find('list') != -1:
                #对于列表变量，其中每一个子元素都是dict
                self.write("<h3>%s</h3>" % var_name)
                tmp_list = var_value
                if tmp_list not in [None,'None',[],'[]']:
                    self.write("<table border='1'>")
                    self.write("<tr>")
                    #logger.error(tmp_list)
                    for key,value in tmp_list[0].iteritems():
                        self.write("<th>%s</th>" % key)
                    self.write("</tr>")
                    
                    for one_dict in tmp_list:
                        self.write("<tr>")
                        for key,value in one_dict.iteritems():
                            self.write("<td>%s</td>" % value)
                        self.write("</tr>")
                    self.write("</table>")
    
    def post(self):
        '''没有任何实现'''
        pass
       
####### tool functions， 用于tornado服务器接受ctrl+C的中止
def signal_handler(signum, frame):
    global is_closing
    is_closing = True

def try_exit(): 
    global is_closing
    if is_closing:
        tornado.ioloop.IOLoop.instance().stop()

#######################################################
# 路由配置，这是各种模拟器需要改的地方        
#######################################################        
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/migu/app/getData/getBill", GetBillHandler),                       #1. 实时账单接口
    (r"/migu/app/getData/getPauseInfo", getPauseInfoHandler),             #2. 暂停信息获取接口
    (r"/migu/app/getData/getBillDetail", getBillDetailHandler),           #3. 实时账单明细接口
    (r"/migu/app/getData/getBillDetailHf", getBillDetailHfHandler),       #4. 实时账单话费类接口
    (r"/migu/app/getData/getBillDetailFhf", getBillDetailFhfHandler),     #5. 实时账单非话费类接口
    (r"/migu/app/getData/getBillDetailDl", getBillDetailDlHandler),       #6. 实时账单代理收入接口
    (r"/RFCommand/get", RFGetHandler),  # get?var_name=XXXX
    (r"/RFCommand/set", RFSetHandler),  # set?var_name=XXXX&var_value=NNN
],
debug=True,
autoreload=True,
)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    signal.signal(signal.SIGINT, signal_handler)
    application.listen(7779)    
    tornado.ioloop.PeriodicCallback(try_exit, 100).start() 
    tornado.ioloop.IOLoop.instance().start()

