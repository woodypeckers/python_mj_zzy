#-*- coding:utf8 -*-
import cx_Oracle
import os
    
def exec_sql( sql, connstr = 'rf/rf@emms227' ):
    '''修改成兼容模式
    mode1: rf/rf@emms227
    mode2: rf/rf@10.1.4.227:1521/emms
    '''
    conn = _get_connect( connstr )
    #print conn.encoding
    cursor = conn.cursor()
    #cursor.execute( sql.decode( 'gbk' ).encode( 'utf-8' ) )
    sql = sql.encode('gbk').strip().rstrip(';')
    cursor.execute( sql )
    result = None
    if not sql.lower().startswith('s'):
        conn.commit()
        cursor.close()
        conn.close()
        cursor = None
        conn=None
        return result
    result_tuple = cursor.fetchall()
    cursor.close()
    conn.close()
    cursor = None
    conn = None
    result = list( [list( li ) for li in result_tuple] )
    #如果返回值只有一个，进行格式转换,返回str，如[['a']],返回为a
    if len(result) == 1:
        s=str(result)
        return s.replace('[','').replace(']','').replace("'",'')
    else:
        return result

def _get_connect( connstr = 'rf/rf@emms227' ):
    conn = None
    if connstr.find(':') != -1:
        username = connstr.split('/')[0]
        password = connstr.split('/')[1].split('@')[0]
        [ip,port] = connstr.split('/')[1].split('@')[1].split(':')
        sid = connstr.split('/')[-1]
        dsn = cx_Oracle.makedsn(ip, port, sid)
        conn = cx_Oracle.connect(username, password, dsn)
    else:
        conn = cx_Oracle.connect( connstr )
    return conn

def exec_many_sql( sql, connstr = 'aspiremsgcmb/aspiremsgcmb@vmoracle' ):
    conn = _get_connect(connstr)
    #print conn.encoding
    cursor = conn.cursor()
    #cursor.execute( sql.decode( 'gbk' ).encode( 'utf-8' ) )
    sql = sql.encode('gbk').strip().rstrip(';')
    cursor.executemany( sql )
    result = None
    if not sql.lower().startswith('s'):
        conn.commit()
        cursor.close()
        conn.close()
        cursor = None
        conn=None
        return result
    result_tuple = cursor.fetchall()
    cursor.close()
    conn.close()
    cursor = None
    conn = None
    result = list( [list( li ) for li in result_tuple] )
    return result    

def exec_call_proc( connstr, proc_name, paramlist_str):

    '''
    根据数据库存储过程输入参数，执行存储过程，由于robot框架传递参数是字符串，
    需要将存储过程有多个输入参数的内容，转换为数组类型，参数按位置顺序以"|"分隔
    注意：编写存储过程输入参数类型用字符类型，
    参数1：存储过程名称，参数2：存储过程参数，例如：exec_call_proc('proc_zdh_clear_credit_data','2|0024')
    '''
    conn = _get_connect(connstr)
    proc_list = []
    if paramlist_str.find("|") == -1:
        proc_list.append(paramlist_str)
    else:
        proc_list = paramlist_str.split("|")
    cursor = conn.cursor()
    proc_name = proc_name
    cursor.callproc(proc_name,proc_list)
    
    result = None
    cursor.close()
    conn.close()
    cursor = None
    conn = None

    
    
    
def int_2_intdesc(some_int):
    result_str = some_int
    some_int = int(some_int)
    if some_int > 10000:
        result_str = str(some_int/10000) + u'万'
    return  result_str

def intdesc_2_int(some_intdesc):
    result_str = some_intdesc
    if some_intdesc.endswith(u'万'):
        result_str = str( int(some_intdesc.rstrip(u'万')) * 10000) 
    return  result_str

    
if __name__=="__main__":
    sql = '''Select to_char(msgdate +1,'yyyy-mm-dd HH24:MI'),count(1) From MSG_Request_History Where msgtype = 0 and msgdate < sysdate - 0 Group by to_char(msgdate +1,'yyyy-mm-dd HH24:MI') '''
    #sql = '''delete from MSG_REQUEST_HISTORY'''
    print exec_sql(sql,'aspiremsg/aspiremsg@192.168.253.80:1521/orcl')
    
def get_current_abspath():
    '''
   获取绝对路径
    '''
    return  os.path.abspath(os.curdir).decode('gb2312')
def join_element_by_symbol(firstElement,secondElement,symbol_a="|"):
    newElement = firstElement + symbol_a + secondElement
    return newElement

