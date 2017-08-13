# -*- coding: utf-8 -*-

'''
Created on 2015-5-25

@author: wangmianjie
'''
# -*- coding: utf-8 -*-

'''
Created on 2015-5-13

@author: wangmianjie
'''

class Parameter():
    
    def __init__(self, path, paramName):
        self.path = path
        self.paramName = paramName
    

    

# text='''
#         <?xml version="1.0" encoding="UTF-8"?>
#         <DataFileDownLoad>
#             <EventId>0791_1001_0791_1005_20140704153100</EventId>
#             <DeviceType>$${param1}$$</DeviceType>
#             <OperationTarget>$${param2}$$</OperationTarget>
#             <DeviceId>0791</DeviceId>
#             <FileName>0791_1001_0791_1005_20140704153100_20140704153100.xml</FileName>
#         </DataFileDownLoad>
#         '''

# print text[60:70]
# param = Parameter()
# param.getParamList(text) 
# print param.paramList