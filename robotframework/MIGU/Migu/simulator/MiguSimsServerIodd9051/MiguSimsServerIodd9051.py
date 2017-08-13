#-*- coding:utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import string
import json
import urllib
import xml.etree.ElementTree as et
from lxml import etree
import time
import cx_Oracle
import os

class PostHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Parse the form data posted
        raw_post_data = ''
        if self.headers.dict.has_key("content-length"):
            content_length = string.atoi(self.headers.dict["content-length"])
            raw_post_data = self.rfile.read(content_length)
        else:
            raw_post_data = self.rfile.read()
        
        #模拟器收到的码流需要转码
        if raw_post_data.find('<') == -1:
            xml_str = open(raw_post_data, 'r+').read().replace('"GBK"?>','"utf-8"?>').decode('GBK').encode('utf-8')
        else:
            xml_str = raw_post_data.replace('"GBK"?>','"utf-8"?>').decode('GBK').encode('utf-8')
        
        #获取Header节点和Body节点
        root = et.fromstring(xml_str)
        headerNode = root.findall('Header')
        bodyNode = root.findall('Body')
        
        for hnode in headerNode:
            activityCode = hnode.find('ActivityCode').text  #接口类型编码
            reqDateTime = hnode.find('ReqDateTime').text    #消息接收时间
            reqTransID = hnode.find('ReqTransID').text  #消息ID
        
        if activityCode == u'020007' or activityCode == u'020008':
            for node in bodyNode:
                companyName = node.find('CompanyName').text    #公司中文名称
                orgCode = node.find('OrgCode').text    #组织机构代码
        
        #判断接口类型
        if activityCode == u'020007':   #公司编码申请接口
            return_msg = getCompanyNo(companyName, orgCode, reqDateTime, reqTransID)
        elif activityCode == u'020009': #公司商用时间戳生成接口
            return_msg = getTimeStamp(reqDateTime, reqTransID)
        else:
            print "error"
        
        content = return_msg#.decode('utf-8').encode('GBK')
        # 发送应答包
        response = "HTTP/1.0 200 OK\r\n"
        response += "Content-Type: application/json;charset=utf-8\r\n"
        response += "Content-Length: " + str(len(content)) + "\r\n"
        response += "\r\n"
        response += content           
        self.wfile.write(response)    
        return

def getTimeStamp(reqDateTime, reqTransID):
    '''获取当前系统时间戳'''
    temp = get_sys_time()
    recDateTime = temp
    rcvTransID = '999' + temp
    change_node_text('020009response.xml', reqDateTime, '/Msg/Header/ReqDateTime')
    change_node_text('020009response.xml', reqTransID, '/Msg/Header/ReqTransID')
    change_node_text('020009response.xml', recDateTime, '/Msg/Header/RcvDateTime')
    change_node_text('020009response.xml', rcvTransID, '/Msg/Header/RcvTransID')
    
    change_node_text('020009response.xml', temp, '/Msg/Body/TimeStamp')
    
    return_msg = read_xml('020009response.xml')
    return return_msg 
        
def getCompanyNo(companyName, orgCode, reqDateTime, reqTransID):
    '''获取公司编码'''
    #修改返回码流xml文件中节点的值
    temp = get_sys_time()
    recDateTime = temp
    rcvTransID = '999' + temp
    change_node_text('020007response.xml', reqDateTime, '/Msg/Header/ReqDateTime')
    change_node_text('020007response.xml', reqTransID, '/Msg/Header/ReqTransID')
    change_node_text('020007response.xml', recDateTime, '/Msg/Header/RcvDateTime')
    change_node_text('020007response.xml', rcvTransID, '/Msg/Header/RcvTransID')   
    
    cnNo = ''
    responsCode = ''
    resDesc= ''
    #sql = "SELECT t.COMPANY_NO FROM AUTO_COMPANY_CODE t WHERE t.CN_NAME='" +companyName+ "' AND t.ORG_CODE='" +orgCode+ "';"
    #根据公司中文名称查公司编码
    sql1 = "SELECT t.COMPANY_NO FROM AUTO_COMPANY_CODE t WHERE t.CN_NAME='" +companyName+ "';"
    result1 = exec_sql(sql1)
    #根据公司中文名称查公司编码
    sql2 = "SELECT t.COMPANY_NO FROM AUTO_COMPANY_CODE t WHERE t.ORG_CODE='" +orgCode+ "';"
    result2 = exec_sql(sql2)
    
    if result1 == [] and result2 != []:
        responsCode = '022999'
        resDesc = 'failed'
    if result1 != [] and result2 == []:
        responsCode = '022999'
        resDesc = 'failed'
    if result1 != [] and result2 != [] and result1 != result2:
        responsCode = '022999'
        resDesc = 'failed'
    if result1 != [] and result2 != [] and result1 == result2:
        responsCode = '000000'
        resDesc = 'succes'
        cnNo = result1
    if result1 == [] and result2 == []:
        #如果公司编码不存在，则生成一个新的公司编码
        responsCode = '000000'
        cnNo = getNewCnNo(companyName, orgCode)

    change_node_text('020007response.xml', responsCode, '/Msg/Header/RspCode')
    change_node_text('020007response.xml', resDesc, '/Msg/Header/RspDesc')
    change_node_text('020007response.xml', cnNo, '/Msg/Body/CompanyNo')
    
    return_msg = read_xml('020007response.xml')
    return return_msg 
 
def getNewCnNo(companyName, orgCode):
    '''生成一个新的公司编码'''
    #获取SEQ_COMPANY_NO的nextval，作为公司编码
    sql1 = 'SELECT SEQ_COMPANY_NO.Nextval FROM dual;'
    result1 = exec_sql(sql1)
    sql2 = "SELECT ltrim(to_char(" +result1+ ",'00000000')) AS Id FROM dual;"
    result2 = exec_sql(sql2)
    cnNo = 'No.' + result2
    #插入生成的公司编码记录
    sql3 = "INSERT INTO AUTO_COMPANY_CODE (COMPANY_NO, CN_NAME, ORG_CODE) VALUES('" +cnNo+ "', '" +companyName+ "', '" +orgCode+ "');"
    exec_sql(sql3)
    
    return cnNo
    
def read_xml(fileName):
    xmlstr = open(fileName, 'r+').read()
    return xmlstr

def change_node_text(fileName, text, nodePath):
    #修改xml文件节点的值
    root=etree.fromstring(open(fileName,'r+').read())

    node_list = root.xpath(nodePath)
    node = node_list[0]
    node.text = text

    modify_xml_str = etree.tostring(root, encoding='GBK')
    open(fileName,'w+').write(modify_xml_str)

def get_sys_time():
    #获取年月日时分秒，格式为：年年年年月月时时分分秒秒（20140924134802）
	return time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    
def exec_sql( sql, connstr = 'migu_auto/migu_prm_auto@10.12.3.197:1521/ora11g' ):
    '''修改成兼容模式
    mode1: rf/rf@emms227
    mode2: rf/rf@10.1.4.227:1521/emms
    '''
    conn = _get_connect( connstr )
    #print conn.encoding
    cursor = conn.cursor()
    #cursor.execute( sql.decode( 'gbk' ).encode( 'utf-8' ) )
    sql = sql.encode('gbk').strip().rstrip(';')
    cursor.execute( sql )
    result = None
    if not sql.lower().startswith('s'):
        conn.commit()
        cursor.close()
        conn.close()
        cursor = None
        conn=None
        return result
    result_tuple = cursor.fetchall()
    cursor.close()
    conn.close()
    cursor = None
    conn = None
    result = list( [list( li ) for li in result_tuple] )
    #如果返回值只有一个，进行格式转换,返回str，如[['a']],返回为a
    if len(result) == 1:
        s=str(result)
        return s.replace('[','').replace(']','').replace("'",'')
    else:
        return result

def _get_connect( connstr = 'prm_auto/prm_auto_1000@10.12.3.197:1521/ora11g' ):
    conn = None
    if connstr.find(':') != -1:
        username = connstr.split('/')[0]
        password = connstr.split('/')[1].split('@')[0]
        [ip,port] = connstr.split('/')[1].split('@')[1].split(':')
        sid = connstr.split('/')[-1]
        dsn = cx_Oracle.makedsn(ip, port, sid)
        conn = cx_Oracle.connect(username, password, dsn)
    else:
        conn = cx_Oracle.connect( connstr )
    return conn  

    
def read_xml(fileName):
    xmlstr = open(fileName, 'r+').read()
    return xmlstr

def change_node_text(fileName, text, nodePath):
    #修改xml文件节点的值
    root=etree.fromstring(open(fileName,'r+').read())

    node_list = root.xpath(nodePath)
    node = node_list[0]
    node.text = text

    modify_xml_str = etree.tostring(root, encoding='GBK')
    open(fileName,'w+').write(modify_xml_str)

def get_sys_time():
    #获取年月日时分秒，格式为：年年年年月月时时分分秒秒（20140924134802）
	return time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
 
if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('0.0.0.0', 9051), PostHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()