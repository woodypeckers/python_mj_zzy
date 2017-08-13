#-*- coding:utf-8 -*-
import json
import copy 


def json_loads(some_str, encoding=None):
    return json.loads(some_str,encoding=None)

def json_dumps(json_obj):
    return json.dumps(json_obj)

    
def json_get(json_obj,somepath):
    '''返回json对象中指定路径的节点值，返回一个list: [nodevalue,nodetype]
    somepath类似于/a/b/c
    '''
    pass
    
def json_set(json_obj,somepath,value,value_type="str"):
    '''把json对象中的满足path定义的内容，替换成指定值
       somepath类似于/a/b/c
    '''
    result_obj = copy.copy(json_obj)
    pathlist = somepath.split('/')[1:-1]
    json_sub_obj = result_obj
    for li in pathlist:
        json_sub_obj = json_sub_obj[li]
        print '***',json_sub_obj
    if json_sub_obj != result_obj:
        if value_type == 'int':
            value = int(value)
        elif value_type == 'float':
            value = float(value)
        json_sub_obj.update(pathlist[-1],value)
        print json_sub_obj
    print '------'
    print result_obj
    return result_obj
    
    pass
    
def json_remove(json_obj,somepath):
    '''把json中指定节点删除，返回新的json对象
    somepath类似于/a/b/c
    '''
    result_obj = copy.copy(json_obj)
    pass
    
if __name__=="__main__":
    pass