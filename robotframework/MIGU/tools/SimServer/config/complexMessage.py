# -*- coding: utf-8 -*-

'''
Created on 2015-11-27

@author: wangmianjie
'''

from config.xmlMessage import XmlMessage
from config.field import Field, Schema
from lxml import etree
from utils.jsonXmlTool import *
from config.xmlParameter import XmlParameter

class ComplexMessage():
    
    fieldList = []
    schemaList = []
    
    def __init__(self, fileName, msgFormat, direction, tmpType):
        self.paramList = []
        self.replaceParamList = []
        
#         self.tmpContent = open(fileName).read()
        self.tmpContent = fileName
        self.direction = direction        
        self.msgFormat = msgFormat
        self.tmpType = tmpType
        
        self.parseTemplate()
    
    '''  加载模板配置  '''    
    def parseTemplate(self):
        root = etree.XML(self.tmpContent)
        
        #message
        messageNode = root.find('message') 
        for field in messageNode:
            fieldName = field.text
            
            fieldAttr = field.attrib
            for attr in fieldAttr:
                if attr == 'fieldType':
                    fieldType = fieldAttr[attr]
                elif attr == 'count':
                    count = fieldAttr[attr]
                elif attr == 'default':
                    default = fieldAttr[attr]
                elif attr == 'desc':
                    desc = fieldAttr[attr]
                
            self.fieldList.append(Field(fieldName, fieldType, default, desc, count))
            
            
        #解析scheme
        schemaListNode = root.find('schemaList') 
        for schemaNode in schemaListNode:
            schemaAttr = schemaNode.attrib
            for attr in fieldAttr:
                if attr == 'name':
                    schemaName = fieldAttr[attr]
            
            schemaFieldList = {}
             
            for field in schemaNode:
                fieldName = field.text
                 
                fieldAttr = field.attrib
                for attr in fieldAttr:
                    if attr == 'fieldType':
                        fieldType = fieldAttr[attr]
                    elif attr == 'count':
                        count = fieldAttr[attr]
                    elif attr == 'default':
                        default = fieldAttr[attr]
                    elif attr == 'desc':
                        desc = fieldAttr[attr]
                schemaFieldList.append(Field(fieldName, fieldType, default, desc, count))
            schema = Schema(schemaName, schemaFieldList)
            self.schemaList.append(schema)
         
        
    
    def assembleTemplate(self):
        
        for node in self.fieldList:
            
            
        
        return
     

        
        
 if __name__=="__main__":
    xmlStr = '''<?xml version="1.0" encoding="UTF-8" ?>
<template>    
  <message> 
    <field fieldType="Request_schema" count="1" default="" desc="">Request</field> 
  </message>  
  <schemaList> 
    <schema name="Request_schema"> 
      <field fieldType="apkInfos_schema" count="1" default="apkInfos_schema" desc="">apkInfos</field> 
    </schema>  
    <schema name="apkInfos_schema"> 
      <field fieldType="int"            count="1" default="0" desc="">apkType</field>  
      <field fieldType="string"         count="1" default="" desc="·">notifyURL</field>  
      <field fieldType="apkInfo_schema" count="N" default="" desc="">apkInfo</field> 
    </schema>  
    <schema name="apkInfo_schema"> 
      <field fieldType="int"    count="1" default="" desc="">contentId</field>  
      <field fieldType="string" count="1" default="" desc="">contentName</field>  
      <field fieldType="string" count="1" default="" desc="">cpId</field>  
      <field fieldType="string" count="1" default="" desc="">filePath</field>  
    </schema> 
  </schemaList> 
</template>'''
    
    comlexTmp = ComplexMessage(xmlStr, 'xml', 'req', 'complex')       
        
        
