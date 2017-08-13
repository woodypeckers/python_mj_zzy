# -*- coding: utf-8 -*-

'''
Created on 2015-6-4

@author: wangmianjie
'''

from config.parameter import  Parameter

class XmlParameter(Parameter):
    
    def __init__(self, paramName, path, tag):
        Parameter.__init__(self, path, paramName)
        self.tag = tag
        
    def toString(self):
        tag = 'tag is:%s\n' % self.tag 
        paramName = "parameter name is: %s\n" % self.paramName
        path = 'xpath is: %s\n' % self.paramName
        
        return tag + paramName + path
        
    