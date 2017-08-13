# -*- coding: utf-8 -*-

'''
Created on 2015-5-29

@author: wangmianjie
'''

from twisted.web.resource import Resource

from admin.tmpFileAdmin import TmpFileAdmin
from admin.expMsgAdmin import ExpMsgAdmin
from admin.expectQuery import ExpectQuery

class TemplateAdmin( Resource ):


    def __init__( self ):
        Resource.__init__( self )
        self.putChild( "", self )

    def getChild( self, path, request ):
        if path in ['admin', 'favicon.ico']:
            return TmpFileAdmin( 'conf/template' )
        elif path == 'simQuery':
            return ExpectQuery()
        else :
            return  ExpMsgAdmin()
