# -*- coding:utf-8 -*-

import os
import shutil
from utils.encoding import detectEncoding

from twisted.web.static import File


class TmpFileAdmin(File):
    def _setContentHeaders(self, request, size=None):
        """
        Set the Content-length and Content-type headers for this request.

        This method is not appropriate for requests for multiple byte ranges;
        L{_doMultipleRangeRequest} will set these headers in that case.

        @param request: The L{Request} object.
        @param size: The size of the response.  If not specified, default to
            C{self.getFileSize()}.
        """
        if size is None:
            size = self.self.getsize()
        request.setHeader('content-length', str(size))
        if self.type:
            # request.setHeader( 'content-type', self.type )
            request.setHeader('content-type', 'text/html')
        if self.encoding:
            # request.setHeader( 'content-encoding', self.encoding )
            request.setHeader('content-encoding', 'UTF-8')

    def render_GET(self, request):
        self.restat(False)
        self.file_dir, self.file_name = os.path.split(self.path)
        if self.type is None:
            # self.type, self.encoding = getTypeAndEncoding( self.basename(),
            #                                               self.contentTypes,
            #                                               self.contentEncodings,
            #                                               self.defaultType )
            self.type = 'html/text'
            self.encoding = 'UTF-8'
        if not self.exists():
            return self.childNotFound.render(request)

        if self.isdir():
            return self.redirect(request)

        request.setHeader('accept-ranges', 'bytes')

        try:
            fileForReading = self.openForReading()
        except IOError, e:
            import errno
            if e[0] == errno.EACCES:
                return self.forbidden.render(request)
            else:
                raise

        # if request.setLastModified( self.getmtime() ) is http.CACHED:
        #    return ''
        filecontent = fileForReading.read()
        self.file_encoding = detectFileEncoding(self.path)
        if self.file_encoding == "GBK":
            filecontent = filecontent.decode('cp936').encode('UTF-8')
        elif self.file_encoding == "UTF-16LE":
            filecontent = filecontent.decode(self.file_encoding).encode('UTF-8')
        response = '''<html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        </head>
        <body>
        <h5>文件编码： <b>%s</b></h5>
        <hr/>
        <form action='%s' method='POST' id='modifyform'>
        <input type='submit' value="修改template文件内容" />
        </form>
        <textarea name="file_content" form="modifyform" rows='20' cols='100'>%s</textarea> 
        </body>
        </html>
        ''' % (self.file_encoding, self.file_name, filecontent)

        return response

    def render_POST(self, request):
        # req_body = request.content.read()
        # req_body_unquote = cgi.escape( request.args["file_content"][0].replace( '\r\n', '\n' ) )
        req_body_unquote = request.args["file_content"][0].replace('\r\n', '\n')
        #open ( 'r:/file_content.txt', 'w+' ).write( req_body_unquote )

        file_path = self.path
        self.file_encoding = detectFileEncoding(self.path)
        # 如果原始文件是gbk编码的，从post拿到的body是utf-8的，需要转码到GBK
        if self.file_encoding == 'GBK':
            req_body_unquote = req_body_unquote.decode('UTF-8').encode('cp936')
        elif self.file_encoding == "UTF-16LE":
            req_body_unquote = req_body_unquote.decode('UTF-8').encode('UTF-16LE')
        # 如果原始文件是UTF-8的，也就无所谓了
        shutil.copy(self.path, self.path + '.bak')

        # req_body_unquote是已转换html符号的安全串，写回文件时需要quote一把
        open(self.path, 'w+').write(req_body_unquote)

        # return 'POST:%s!\n%s' % ( self.file_encoding, req_body_unquote )
        return self.render_GET(request)


def detectFileEncoding(somefile):
    return detectEncoding(open(somefile, 'r+').read())
