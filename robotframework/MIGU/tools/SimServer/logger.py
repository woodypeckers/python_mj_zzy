# -*- coding: utf-8 -*-

'''
Created on 2015-7-1

@author: wangmianjie
'''

import sys
import logging
from logging.handlers import RotatingFileHandler
from logging import StreamHandler

_unicode = True

class StreamHandlerUTF82GBK(StreamHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            fs = "%s\n"
            if not _unicode: #if no unicode support...
                stream.write(fs % msg)
            else:
                try:
                    if (isinstance(msg, unicode) and
                        getattr(stream, 'encoding', None)):
                        ufs = u'%s\n'
                        try:
                            stream.write(ufs % msg)
                        except UnicodeEncodeError:
                            #Printing to terminals sometimes fails. For example,
                            #with an encoding of 'cp1251', the above write will
                            #work if written to a stream opened or wrapped by
                            #the codecs module, but fail when writing to a
                            #terminal even when the codepage is set to cp1251.
                            #An extra encoding step seems to be needed.
                            stream.write((ufs % msg).encode(stream.encoding))
                    else:
                        # stream.write(fs % msg)
                        # encode to cp936 by chenzw  start
                        msg = msg.decode('utf-8').encode(stream.encoding)
                        try:
                            stream.write(fs % msg)
                        except IOError:
                            pass
                        # encode to cp936 by chenzw  end
                except UnicodeError:
                    stream.write(fs % msg.encode("UTF-8"))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)



logger = logging.getLogger('simServer')
formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')

runtimelog = RotatingFileHandler("simServer.log",  maxBytes=5*1024*1024, backupCount=3)
runtimelog.setFormatter(formatter)
logger.addHandler(runtimelog)
# 写屏功能，如不需要，则请注释下面三行（压力下，不写屏可达100TPS，写屏只有20TPS）
stdoutlog = StreamHandlerUTF82GBK(sys.stdout)
stdoutlog.setFormatter(formatter)
logger.addHandler(stdoutlog)

logger.setLevel(logging.DEBUG)   # DEBUG, INFO, WARNING, ERROR, CRITICAL ...etc

def log(logStr):    
    logger.info(logStr)
