#-*- coding:utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import string
import json
import urllib
import xml.etree.ElementTree as et  
import urllib2
import httplib
import socket

class PostHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Parse the form data posted
        raw_post_data = ''
        if self.headers.dict.has_key("content-length"):
            content_length = string.atoi(self.headers.dict["content-length"])
            raw_post_data = self.rfile.read(content_length)
        else:
            raw_post_data = self.rfile.read()
        
        #将消息发送个PRM IODD
        return_msg = post_xml(raw_post_data, "http://10.12.12.157:28080/iodd/baseXmlHttp")
        
        #content = return_msg.decode('utf-8').encode('GBK')
        content = return_msg
        # 发送应答包
        response = "HTTP/1.0 200 OK\r\n"
        response += "Content-Type: application/json\r\n"
        response += "Content-Length: " + str(len(content)) + "\r\n"
        response += "\r\n"
        response += content           
        self.wfile.write(response)    
        return

def post_xml(xml_str, url):
    '''
       input: request xmlstr
       output: response str
    '''
    #xmlstr = open(raw_post_data, 'r+').read().replace('"GBK"?>','"utf-8"?>').decode('GBK').encode('utf-8')
    
    headers = {"Content-Type":"xml/text",   
                "Accept":"application/json",
                "Connection":"Keep-Alive",
                "Content-Length":"%s" % len(xml_str)}
    urlsplit = urllib2.urlparse.urlsplit(url)
    netloc = urlsplit.netloc
    path = urlsplit.path
    if path =='':
        path = '/'
    conn = httplib.HTTPConnection(netloc)
    try:
        conn.request("POST", path, body=xml_str, headers=headers)
    except socket.error:
        print '*ERROR* socket error, url无法到达!  please check url!'
        #raise SocketError
    response = conn.getresponse()
    resp_str =  response.read(response.msg.getheader('content-length'))
    return resp_str
        
if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('0.0.0.0', 9003), PostHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()