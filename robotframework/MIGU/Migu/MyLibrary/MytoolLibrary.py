#-*- coding:utf-8 -*-

'''操作数据库和字符串，减少testcaes处理逻辑
'''
import cx_Oracle
import string
import xlrd
from robot.api import logger
import os
from robot.libraries.BuiltIn import BuiltIn
from lxml import etree 
import datetime

#db_user = 'sims_zdh2200'
#db_paswd = 'sims_zdh2200_10g'
#db_dsn = '192.168.60.130:1521/orcl'
#db_user = 'sims_fj3050'
#db_paswd = 'sims_fj3050_10g'
#db_dsn = '10.12.3.164:1521/ora11g'
db_user ='prm_auto '
db_paswd ='prm_auto_1000'
db_dsn ='10.12.3.197:1521/ora11g'
#db_user = 'sims_bj2200'
#db_paswd = 'sims_bj2200_10g'
#db_dsn = '10.1.4.59:1521/ora10g'


#第一个参数：查询语句，第二个参数：查询条件值，用|分隔
def select_oracle_table(sqlstring,condition,isblog='N'):
    '''connect oracle database, select by sql string, return table contents.
        first parameter:sql string, second parameter:condition, which Separated by Vertical lines
    '''

    condition_list = []
    condition_map = {}
    args = 0
    #condition = str(condition)
    if condition.find("|") == -1:
        condition_map["argv0"] = condition
    else:
        condition_list = condition.split('|')
        for clist in condition_list: 
            mapkey = "argv%s"%args
            condition_map[mapkey] = clist
            args=args+1
        
    db = cx_Oracle.connect(db_user, db_paswd, db_dsn)
    cursor_fetch = db.cursor()
    logger.info("sql is %s , condition is %s"%(sqlstring, condition_map))
    cursor_fetch.execute(sqlstring,condition_map)
    result = cursor_fetch.fetchall()

    if len(result) == 0:
        return u'0'
        
    if isblog == 'Y':
        return result[0][0].read()
        
    return result

def select_oracle_table_by_count(sqlstring,condition):
    '''connect oracle database, select by sql string, return table counts.
        first parameter:sql string, second parameter:condition, which Separated by Vertical lines
    '''
    condition_list = []
    condition_map = {}
    args = 0
    condition = str(condition)
    if condition.find("|") == -1:
        condition_map["argv0"] = condition
    else:
        condition_list = condition.split('|')
        for clist in condition_list: 
            mapkey = "argv%s"%args
            condition_map[mapkey] = clist
            args=args+1
        
    db = cx_Oracle.connect(db_user, db_paswd, db_dsn)
    cursor_fetch = db.cursor()
    logger.info("sql is %s , condition is %s"%(sqlstring, condition_map))
    cursor_fetch.execute(sqlstring,condition_map)
    result = cursor_fetch.fetchall()

    return len(result)

def execute_procedure_func(proc_name):
    '''
    根据数据库存储过程输入参数，执行存储过程，由于robot框架传递参数是字符串，
    需要将存储过程有多个输入参数的内容，转换为数组类型，参数按位置顺序以"|"分隔
    注意：编写存储过程输入参数类型用字符类型，
    参数1：存储过程名称，参数2：存储过程参数，例如：execute_procedure_func('proc_zdh_clear_credit_data','2|0024')
    '''
   
        
    db = cx_Oracle.connect(db_user, db_paswd, db_dsn)
    cursor_fetch = db.cursor()
    result = cursor_fetch.callproc(proc_name)
    cursor_fetch.close()
    db.commit()
    return result
    
def get_colunm_value_error(list_content, keyword, values):
    key_map = {}
    value_list = []
    if values.find(":") == -1:
        value_list.append(value)
    else:
        value_list = values.split(":")
    result = []
    if keyword.find(":") == -1:
        mapkey = keyword.split("|")[0]
        key_map[mapkey] = keyword.split("|")[1]
    else:
        key_list = keyword.split("|")[0].split(":")
        tmp0 = 0
        for lia in key_list:
            mapkey = lia
            key_map[mapkey] = keyword.split("|")[1].split(":")[tmp0]
            tmp0 = tmp0+1
                   
    count = len(key_map)
    for lia in list_content:
        flag = 0
        for keya in key_map.keys():
            tmp1 = string.atoi(keya)
            if lia[tmp1] == key_map[keya]:
                flag =flag + 1
        if flag == count:
            for li in value_list:
                tmp2 = string.atoi(li)
                result.append(lia[tmp2])
    return result
    
#期望结果和实际结果比较
def check_data_is_same(leftdata,rightdata):
    logger.info("type left is %s, type right is %s"%(type(leftdata),type(rightdata)))
    if type(leftdata) != type(u'a'):
        leftdata = str(leftdata).decode("utf-8")
    if type(rightdata) != type(u'a'):
        rightdata = str(rightdata).decode("utf-8")
        
    if leftdata == rightdata:
        logger.info("%s is same with %s"%(leftdata, rightdata))
        return 0
    else:
        msg = "%s is not same with %s"%(leftdata, rightdata)
        raise AssertionError(msg)
        
#根据变量组装查询列表元素的xpath路径
def get_xpath_by_element(xpath,element):
    '''find xpath by element,return new xpath 
    first parameter:xpath which doesn't complete,some content should be replace, 
    second parameter:condition, which Separated by Vertical lines
    '''
    element_map = {}
    args = 0
    
    if element.find("|") == -1:
        element_map["argv0"] = element
    else:
        element_list = element.split('|')
        for clist in element_list: 
            mapkey = "argv%s"%args
            element_map[mapkey] = clist
            args=args+1

    for keya in element_map.keys():
        xpath = xpath.replace(keya,element_map[keya])
    logger.info("return result is %s"%xpath)

    return xpath
    
def join_element_by_symbol(firstElement,secondElement,symbol_a="|"):
    newElement = firstElement + symbol_a + secondElement
    return newElement

def open_excel(filename='file.xls'):
    '''read excelfile, parameter: filename Absolute path
    '''
    try:
        data = xlrd.open_workbook(filename)
        return data
    except Exception,e:
        print str(e)

def get_excel_by_linelist(filename,row_begin,sheetx=0,mode=u'byindex'):
    '''read excel,return all content by line as list,mode 'byindex' or 'byname',
    default 'byindex' mode, sheetx should be same with mode   
    '''   
    data = open_excel(filename)
    if mode == u'byindex':
        table = data.sheet_by_index(sheetx)
    else:
        table = data.sheet_by_name(sheetx)
    nrows = table.nrows
    
    row_list = []
    for tmp in range(row_begin, nrows):
        row_data = table.row_values(tmp)
        row_list.append(row_data)
    return row_list

def get_excel_by_cellvalue(filename,row,cols,sheetx=0,mode=u'byindex'):
    '''read excel,return one cell value ,mode 'byindex' or 'byname',
    default 'byindex' mode, sheetx should be same with mode   
    '''   
    data = open_excel(filename)
    if mode == u'byindex':
        table = data.sheet_by_index(sheetx)
    else:
        table = data.sheet_by_name(sheetx)
    
    cell_value = table.cell_value(row,cols)
    return cell_value

def get_excel_by_lineCount(filename,sheetx=0,mode=u'byindex'):
    '''read excel,return lines and cols as list, first is line count, secode is cols count,
    mode 'byindex' or 'byname',default 'byindex' mode, sheetx should be same with mode   
    '''   
    data = open_excel(filename)
    count = []
    if mode == u'byindex':
        table = data.sheet_by_index(sheetx)
    else:
        table = data.sheet_by_name(sheetx)
    count.append(table.nrows)
    count.append(table.ncols)
    return count

def get_excel_by_special_key(filename,row_begin,cols_key,cols_value,sheetnum=0):
    '''read excel as byindex default 0 ,return map for ceslls value, 
    second parameter: line begin
    third parameter:  cols used for map key, Separated by ':'
    fourth parameter: cols used for map value, Separated by ':'
    '''   
    data = open_excel(filename)
    table = data.sheet_by_index(sheetnum)
    nrows = table.nrows

    cell_map = {}
    key_list = []
    value_list = []
    flag = ':'
    
    if cols_key.find(":") == -1:
        key_list.append(cols_key)
    else:
        key_list = cols_key.split(":")
    
    if cols_value.find(":") == -1:
        value_list.append(cols_value)
    else:
        value_list = cols_value.split(":")
        
    for tmp in range(row_begin, nrows):
        row_data = table.row_values(tmp)
        mapkey = []
        mapvalue = []
        for keys in key_list:
            mapkey.append(row_data[string.atoi(keys)])
        for values in value_list:
            mapvalue.append(row_data[string.atoi(values)])
        cell_map[flag.join(mapkey)] = flag.join(mapvalue)
        
    return  cell_map       

def compared_excel_with_database(filename,row_begin,cols_key,cols_value,db_list,forms,code_mode=0,sheetnum=0):
    '''
    read excel as byindex default 0 ,record in map, and compare with database data
    second parameter: line begin
    third parameter:  cols used for map key, Separated by ':'
    fourth parameter: cols used for map value, Separated by ':'
    fifth parameter: database data, by double list
    sixth parameter: database record's key and value position,Separated by ':' and '|','0:2|1:3'
    seventh parametre: code_mode,0:string,1:int
    '''   
    data = open_excel(filename)
    table = data.sheet_by_index(sheetnum)
    nrows = table.nrows

    cell_map = {}
    excel_key_list = []
    excel_value_list = []
    flag = ':'
    
    if cols_key.find(":") == -1:
        excel_key_list.append(cols_key)
    else:
        excel_key_list = cols_key.split(":")
    
    if cols_value.find(":") == -1:
        excel_value_list.append(cols_value)
    else:
        excel_value_list = cols_value.split(":")
 
    for tmp in range(string.atoi(str(row_begin)), string.atoi(str(nrows))):
        row_data = table.row_values(tmp)
        mapkey = []
        mapvalue = []
        for keys in excel_key_list:
            mapkey.append(str(row_data[string.atoi(keys)].encode('GBK')))
            print str(row_data[string.atoi(keys)].encode('GBK'))
        for values in excel_value_list:
            if code_mode == 0:
                mapvalue.append(str(row_data[string.atoi(values)]))
            if code_mode == 1:
                mapvalue.append(int(row_data[string.atoi(values)]))
        cell_map[flag.join(mapkey)] = flag.join(mapvalue)
    
    db_key_list = []
    db_value_list = []
    
    db_tmp_list = forms.split('|')
    if db_tmp_list[0].find(':') == -1:
        db_key_list.append(str(db_tmp_list[0])) 
    else:
        db_key_list = db_tmp_list[0].split(':')
    if db_tmp_list[1].find(':') == -1:
        db_value_list.append(str(db_tmp_list[1])) 
    else:
        db_value_list = db_tmp_list[1].split(':')
    
    for db in db_list:
        db_keys = []
        db_values = []
        for db_key in db_key_list:
            db_keys.append(str(db[string.atoi(db_key)]))  
        for db_value in db_value_list:
            if code_mode == 0:
                db_values.append(str(db[string.atoi(db_value)]))
            if code_mode == 1:
                db_values.append(int(db[string.atoi(db_value)]))
        
        if cell_map.has_key(flag.join(db_keys)) is False:
            msg = "database record  %s does not exist in Excel"%(flag.join(db_keys)) 
            raise AssertionError(msg)
        elif cell_map[flag.join(db_keys)] != flag.join(db_values):
            msg = "database record  %s does not same with Excel %s"%(flag.join(db_values), cell_map[flag.join(db_keys)]) 
            raise AssertionError(msg)
        else:
            pass
    return 0 

def write_to_file(filename,strings):
    '''write strings to files as overwrite
    '''
    fp = open(filename, 'w+')
    #print strings
    #print type(strings)
    if type(strings) == unicode:
        logger.info('%s encode to gbk'%strings)
        strings = strings.encode('gbk')
    fp.write(strings)
    fp.close() 

def read_from_file(filename):
    '''read file, and return all lines
    '''
    fp = open(filename, 'r')
    allLines = [li.rstrip('\n').decode('gbk') for li in fp.readlines() if li not in ['','\n', None]]
    fp.close()
    return allLines   


def transform_str2list_by_delimiter(strings, delimiter=':'):
    trans_list = []
    if strings.find(delimiter) == -1:
        trans_list.append(strings)
    else:
        trans_list = strings.split(delimiter)
    return trans_list
    
def check_two_list_is_same_by_keys(list1, list2, keys, values):

    check_map = {}
    key_list = []
    value_list = []
    tag = ':'
    
    key_list = transform_str2list_by_delimiter(keys)
    value_list = transform_str2list_by_delimiter(values)
    
    for st1 in list1:
        check_map_key = []
        check_map_value = []
        for klist in key_list:
            check_map_key.append(str(st1[string.atoi(klist)]))
        for vlist in value_list:
            check_map_value.append(str(st1[string.atoi(vlist)]))
        if check_map.has_key(tag.join(check_map_key)) is False:
            check_map[tag.join(check_map_key)] = tag.join(check_map_value)
        else:
            logger.error("data has wrong,has same key in dict")
            
    for st2 in list2:
        check_map_key2 = []
        check_map_value2 = []
        for klist in key_list:
            check_map_key2.append(str(st2[string.atoi(klist)]))
        for vlist in value_list:
            check_map_value2.append(str(st2[string.atoi(vlist)]))
            
        if check_map.has_key(tag.join(check_map_key2)) is False:
            logger.info('keys:%s is not in list1'%(check_map_key2))
            return -1
        else:
            if check_map[tag.join(check_map_key2)] != tag.join(check_map_value2):
                logger.info('list1:%s, list2:%s is not same with list1'%(check_map[tag.join(check_map_key2)], tag.join(check_map_value2)))
                return -1
            else:
                pass
    return 0   

def update_dict_for_testdata(dict_key, dict_value):
    testdata = {}
    builtin = BuiltIn().get_library_instance('BuiltIn')
    testdata = builtin.get_variable_value('${testcase_data}')
    testdata[dict_key] = dict_value
    builtin.set_test_variable('${testcase_data}', testdata)
    
    return testdata
    
def compare_integer_by_range(leftdata, rightdata, range):
    print type(range)
    abs_differ = abs(leftdata - rightdata)
    
    if abs_differ > string.atoi(range):
        msg = "spacing is %s,expected is  %s "%(abs_differ, range)
        raise AssertionError(msg) 
    else:
        return 1
    
    
def parse_message_xmlstring(xmlstring):
    '''
                解析xml报文
    '''
    builtin = BuiltIn().get_library_instance('BuiltIn')
    fp = open(r'./message_tmp.xml', "wb")
    fp.write(xmlstring.decode('GBK').encode('utf-8'))
    fp.close()
    
    parser = etree.XMLParser(strip_cdata=False)
    xmls = etree.parse(r'./message_tmp.xml', parser)
    
    builtin.set_test_variable('${XML_DATA}', xmls)
            
    return xmls


def parse_message_xmlstring_by_xpath(xmlstring,node_xpath,find_key):
    '''
    对于存在相同节点的xml，通过xpath根据关键字查找对应的节点内容
    '''
    fp = open(r'./req_tmp.xml', "wb")
    fp.write(xmlstring.decode('GBK').encode('utf-8'))
    fp.close()
    
    parser = etree.XMLParser(strip_cdata=False)
    xmls = etree.parse(r'./req_tmp.xml', parser)
    
    '''for node in  xmls.xpath(node_xpath,name=find_key):
        print "node is %s, tag is %s, text is %s"%(node,node.tag,node.text)'''
        
    return xmls.xpath(node_xpath,name=find_key.encode('GBK'))[0].text

def get_value_from_xmls_by_node(messge_node):
    '''
    根据xml节点获取对应的值
    '''
    builtin = BuiltIn().get_library_instance('BuiltIn')
    xmls = builtin.get_variable_value('${XML_DATA}')

    for xms in xmls.getiterator():
        if messge_node == xms.tag:
            messge_data = xms.text 
    return messge_data

def get_value_from_xmls_by_xpath(node_xpath,find_key):
    '''
    由于存在xml中相同子节点的情况，采用xpath方式获取指定节点内容
    '''
    builtin = BuiltIn().get_library_instance('BuiltIn')
    xmls = builtin.get_variable_value('${XML_DATA}')

    return xmls.xpath(node_xpath,name=find_key)[0].text
    
def check_message_with_database(messge_data,db_data,str_format):
    '''
    参数1：消息blob中的字段节点内容，参数2：数据库中的值
    '''   
    #logger.info("%s is  %s"%(type(messge_data), type(db_data)))
    if messge_data is None:
        messge_data = ''
    if db_data is None:
        db_data = ''
    if type(messge_data) != type(db_data):
        messge_data = messge_data.encode('GBK')
    #对于特殊格式的字符串比较，需要进行特定转换，例如时间有yyyymmdd,yyyymmddhh24MMss,yyyymmdd hh24MMss等格式
    if str_format != 'null':
        #对于oracle date类型需要转换，引用datetime包
        if type(db_data) == datetime.datetime and str_format == 'yyyymmdd':
            db_data = str(db_data).split(' ')[0].replace('-','')
        elif type(db_data) == datetime.datetime and str_format == 'yyyymmddhh24MMss':
            db_data = str(db_data).replace('-','').replace(' ','').replace(':','')
        elif type(db_data) == datetime.datetime and str_format == 'yyyymmdd hh24:MM:ss':
            db_data = str(db_data)
        else:
            db_data = str(db_data)
            
    if messge_data == db_data:
        logger.info("%s is same with %s"%(messge_data, db_data))
        return 0
    else:
        msg = "%s is not same with %s"%(messge_data, db_data)
        raise AssertionError(msg)    
    