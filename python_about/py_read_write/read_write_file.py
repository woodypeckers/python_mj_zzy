# -*- coding: utf-8 -*-

def read_file():
    h_config = open("config.ini",'r')#读入文件
    for i in h_config.readlines():
        print i.strip()
    h_config.close()

def write_file():
    """
    数据的持久化、写入文件、写入数据库、写入配置文件
    在程序里全部用uicode编码，支持比较好
    第一种方法好：
    1.读写数据会导致磁盘读写，磁盘慢
    2.块读取，根本原因：cpu,内存,硬盘，网络速度不一致
    """
    name_list = [u'张',u'李三',u'王绍']
    h_file = open('write_name.txt','w')
    #h_file.write('\n'.join(name_list).encode('utf-8'))#第一种方法
    #h_file.close()
    for i in name_list:
        h_file.write(i.encode('utf-8') + '\n' ) #第2种方法
    h_file.close()




if __name__ == "__main__":
    read_file()
    #write_file()