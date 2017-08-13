#-*- coding: utf-8 -*-
'''这是一个基本的sqlalchemy模式的ORM，对数据库中的表进行对象封装,
方便在模拟器中调用数据库模型
'''
from sqlalchemy import Column, String, Integer, Float, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy import func
import datetime

Base = declarative_base()

class Bill(Base):
    __tablename__ = 'bill'

    id = Column(Integer, autoincrement=True, primary_key=True)
    sett_id = Column(String(20),)                       
    sett_type = Column(String(2), default='cp')             #结算类型(cp、ch)
    sett_name = Column(String(20),)
    sett_flag = Column(String(1), default='0')              #是否可结算(0 不可结算   1 可结算)
    sett_month = Column(String(6),)                         # "201606"
    jssp_flag = Column(String(20),default=u'未付款')
    fee_invat = Column(Float(6,2),default=5450.35)                         #结算额
    tax_rate = Column(Float(0,2), default=0.06)             #税率（不带%的小数）
    comments = Column(String(200), default=u"备注1")         #  备注,"备注1"
    update_time = Column(String(8),)                         #最近更新时间,"20160329"
    
class Pause_Info(Base):
    __tablename__ = 'pause_info'

    id = Column(Integer, autoincrement=True, primary_key=True)
    sett_id = Column(String(20),)
    sett_month = Column(String(6),)                             #"201606"
    pause_type  = Column(String(1), default="4")                #暂停类型：服务1  合同2   人工3  欠费4
    recovery_month = Column(String(6),)
    comments = Column(String(200), default=u"欠费")
    
class Bill_Detail(Base):
    __tablename__ = 'bill_detail'

    id = Column(Integer, autoincrement=True, primary_key=True)
    sett_id = Column(String(20),)
    sett_month = Column(String(6),)                 # "201606"
    sett_name = Column(String(200),)
    fee_hf = Column(String(10),)                      #话费类收入
    fee_fhf = Column(String(10),)                     #非话费收入
    fee_dl = Column(String(10),)                      #代理收入
    fee_vgop = Column(String(10),)                    #VGOP稽核
    fee_kh = Column(String(10),)                      #违约金考核
    fee_tz = Column(String(10),)                      #调账金额
    fee_sett = Column(String(10),)                    #实结信息费
    vatrate = Column(String(10),)                     #税率
    fee_exvat = Column(String(10),)                   #实结信息费(不含税)
    fee_vat = Column(String(10),)                     #实结信息费(进项税额)
    fee_invat = Column(String(10),)                   #开票信息费(含税)
    payable_vat = Column(String(10),)                 #咪咕纳税额(销项-进项)
    
class Bill_Detail_Hf(Base):
    __tablename__ = 'bill_detail_hf'
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    sett_month = Column(String(6),)
    sett_id = Column(String(20),)
    sett_type = Column(String(2),)
    sett_name = Column(String(20),)
    content_id = Column(String(20),)
    content_name = Column(String(20),)
    sub_ch_code = Column(String(20),)
    sub_ch_name = Column(String(20),)
    dis_info_fees = Column(String(20),)
    audit_fee = Column(String(20),)
    js_ratio = Column(String(20),)
    js_yj_settfee = Column(String(20),)

class Bill_Detail_FHf(Base):
    __tablename__ = 'bill_detail_fhf'
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    sett_month = Column(String(6),)
    sett_id = Column(String(20),)
    sett_type = Column(String(2),)
    sett_name = Column(String(20),)
    content_id = Column(String(20),)
    content_name = Column(String(20),)
    sub_ch_code = Column(String(20),)
    sub_ch_name = Column(String(20),)
    dis_info_fees = Column(String(20),)
    audit_fee = Column(String(20),)
    js_ratio = Column(String(20),)
    js_yj_settfee = Column(String(20),)

class Bill_Detail_Dl(Base):
    __tablename__ = 'bill_detail_dl'
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    sett_month = Column(String(6),)
    dl_comp = Column(String(20),)
    month_id = Column(String(6),)
    cp_code = Column(String(20),)
    cp_name = Column(String(20),)
    oper_code = Column(String(20),)
    oper_name = Column(String(20),)
    info_fee = Column(String(20),)

engine = create_engine(
                #'mysql://demo:demo@192.168.253.1:3306/Demo?charset=utf8')
                #'sqlite:///./database.sqlite',encoding='utf8'
                'oracle://migu:migu_prm@10.12.3.197:1521/ora11g')
DBSession = sessionmaker(bind=engine)
session = DBSession()

def init_db():
    Base.metadata.create_all(engine)
    
def drop_db():
    Base.metadata.drop_all(engine)

    
### 下面是业务功能，主要方便handler调用时方便查询内容
def query_bill_list(sett_id,sett_type,sett_name,page_current,page_size,start_month,stop_month,):
    '''查询出满足条件的bill列表,　这里加上了分页'''
    bill_list = session.query(Bill).order_by(Bill.sett_id,Bill.sett_month)\
                                            .filter(Bill.sett_id.like("%"+sett_id+"%")).filter(Bill.sett_month>=start_month)\
                                            .filter(Bill.sett_month<=stop_month)\
                                            .filter(Bill.sett_type.like("%"+sett_type+"%"))\
                                            .filter(Bill.sett_name.like("%"+sett_name+"%"))\
                                            .offset((int(page_current)-1)*int(page_size))\
                                            .limit(page_size)
    query_count = session.query(func.count('*')).order_by(Bill.sett_id,Bill.sett_month)\
                                            .filter(Bill.sett_id.like("%"+sett_id+"%")).filter(Bill.sett_month>=start_month)\
                                            .filter(Bill.sett_month<=stop_month)\
                                            .filter(Bill.sett_type.like("%"+sett_type+"%"))\
                                            .filter(Bill.sett_name.like("%"+sett_name+"%")).first()[0]
    #print bill_list
    #print query_count
    return (query_count,bill_list)

def query_pause_info(sett_month,sett_id):
    '''查询出pause_info表中的对象,返回为单一对象'''
    pause_info_obj=session.query(Pause_Info).filter(Pause_Info.sett_month==sett_month 
                                            and Pause_Info.sett_id==sett_id).first()
    return pause_info_obj

def query_bill_detail(sett_month,sett_id):
    '''查询出bill_detail表中的对象,返回为单一对象'''
    bill_detail_obj=session.query(Bill_Detail).filter(Bill_Detail.sett_month==sett_month
                                            and Bill_Detail.sett_id==sett_id).first()
    return bill_detail_obj

###查询出符合条件的话单类数据
def query_bill_DetailHf(sett_id,sett_month,sett_type,page_current,page_size):
    '''查询出满足条件的bill列表,　这里加上了分页'''
    bill_list = session.query(Bill_Detail_Hf).order_by(Bill_Detail_Hf.sett_id,Bill_Detail_Hf.sett_month)\
                                            .filter(Bill_Detail_Hf.sett_id==sett_id).filter(Bill_Detail_Hf.sett_month==sett_month)\
                                            .filter(Bill_Detail_Hf.sett_type==sett_type)\
                                            .offset((int(page_current)-1)*int(page_size))\
                                            .limit(page_size)
    query_count = session.query(func.count('*')).order_by(Bill_Detail_Hf.sett_id,Bill_Detail_Hf.sett_month)\
                                            .filter(Bill_Detail_Hf.sett_id==sett_id).filter(Bill_Detail_Hf.sett_month==sett_month)\
                                            .filter(Bill_Detail_Hf.sett_type==sett_type).first()[0]
    #print bill_list
    #print query_count
    return (query_count,bill_list)
######查询出符合条件的非话单类数据
def query_bill_DetailFHf(sett_id,sett_month,sett_type,page_current,page_size):
    '''查询出满足条件的bill列表,　这里加上了分页'''
    bill_list = session.query(Bill_Detail_FHf).order_by(Bill_Detail_FHf.sett_id,Bill_Detail_FHf.sett_month)\
                                            .filter(Bill_Detail_FHf.sett_id==sett_id).filter(Bill_Detail_FHf.sett_month==sett_month)\
                                            .filter(Bill_Detail_FHf.sett_type==sett_type)\
                                            .offset((int(page_current)-1)*int(page_size))\
                                            .limit(page_size)
    query_count = session.query(func.count('*')).order_by(Bill_Detail_FHf.sett_id,Bill_Detail_FHf.sett_month)\
                                            .filter(Bill_Detail_FHf.sett_id==sett_id).filter(Bill_Detail_FHf.sett_month==sett_month)\
                                            .filter(Bill_Detail_FHf.sett_type==sett_type).first()[0]
    #print bill_list
    #print query_count
    return (query_count,bill_list)

####查询出符合条件的实时账单代理收入
def query_bill_DetailDl(sett_id,sett_month,page_current,page_size):
    '''查询出满足条件的bill列表,　这里加上了分页'''
    bill_list = session.query(Bill_Detail_Dl).order_by(Bill_Detail_Dl.cp_code,Bill_Detail_Dl.sett_month)\
                                            .filter(Bill_Detail_Dl.cp_code==sett_id).filter(Bill_Detail_Dl.sett_month==sett_month)\
                                            .offset((int(page_current)-1)*int(page_size))\
                                            .limit(page_size)
    query_count = session.query(func.count('*')).order_by(Bill_Detail_Dl.cp_code,Bill_Detail_Dl.sett_month)\
                                            .filter(Bill_Detail_Dl.cp_code==sett_id).filter(Bill_Detail_Dl.sett_month==sett_month)\
                                            .first()[0]
    #print bill_list
    #print query_count
    return (query_count,bill_list)

if __name__ == '__main__':
    drop_db()
    init_db()
    # for li in range(1,1001):
        # b1=Bill(sett_id='10007', sett_type='cp',jssp_flag=u'未付款',sett_flag='1',sett_month='201505',update_time='20150503')
        # session.add(b1)
    # session.commit()
    # session.close()
    count,obj_list = query_bill_list(sett_id='10006',sett_type='cp',page_current="1", page_size="10",sett_name=u'斯蒂芬打分',start_month='201001',stop_month='209910')
    #print count
    for li in obj_list:
        print li.id,li.sett_id,type(li.sett_month),li.sett_month,type(li.comments),li.comments,li.sett_name
