# -*- coding: utf-8 -*-

'''
Created on 2015-12-1

@author: wangmianjie
'''

class Field():
    
    
    def __init__(self, fieldName, fieldType, default, desc, count, attrList):
        
        #字段名, 字段类型， 默认值, 字段描述
        self.fieldName = fieldName
        self.fieldType = fieldType
        self.defualt = default
        self.desc = desc
        self.count = count
        self.attrList = attrList
        

class Schema():        
    
    def __init__(self, schemaName, fieldList):
        self.schemaName = schemaName
        self.fieldList = fieldList
        
class Attrib():
    
    def __init__(self, attrName, default, desc):
        self.attrName = attrName
        self.default = default
        self.desc = desc