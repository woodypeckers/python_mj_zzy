# -*- coding:cp936 -*-
import os
import logging
import paramiko
import time
import sys

Env_oracle = {'name':'db', 'type':'oracle', 'ip':'10.12.3.197', 'port':'1521', 'user':'prm_auto', 'passwd':'prm_auto_1000', 'tnsname':'10.12.3.197', 'sid':'ora11g'}
Env_prm = {'name':'prm', 'type':'jboss', 'ip':'10.12.12.157', 'port':'18080', 'user':'prm', 'passwd':'prm', 'jboss_home':'/opt/aspire/product/prm/jboss7'}
Env_iodd = {'name':'prmiodd', 'type':'jboss', 'ip':'10.12.12.157', 'port':'28080', 'user':'prm', 'passwd':'prm', 'jboss_home':'/opt/aspire/product/prm/jboss7_iodd', 'sims_inf_url':'http://10.12.12.157:9001'}

prm_build_folder = r'\\ASP-BLD-SERV100\RELEASE_BLDSTG\PRM\PRM1.0.2.004\PRM1.0.2.004_SSYT_4__20150428_17.59.17'
prm_build_str = prm_build_folder.split( '\\' )[-1]


logger = logging.getLogger( 'MyLog' )
formatter = logging.Formatter( '[%(asctime)s][%(levelname)s] %(message)s' )
# formatter = logging.Formatter( '%(levelname)s:%(message)s' )
runtimelog = logging.FileHandler( "运行日志_rebuildDb.log" )
runtimelog.setFormatter( formatter )
logger.addHandler( runtimelog )
# 写屏功能，如不需要，则请注释下面三行
stdoutlog = logging.StreamHandler( sys.stdout )
stdoutlog.setFormatter( formatter )
logger.addHandler( stdoutlog )
logger.setLevel( logging.DEBUG )  # DEBUG, INFO, WARNING, ERROR, CRITICAL ...etc

SSH_flag = 1

def rebuildDb():
    '''执行固定sql,原则上清理数据库中的所有对象，再按顺序导入SQL'''
    logger.info( '重新构建立数据库，先清除数据库用户下的所有对象......' )
    os.system( 'sqlplus %s/%s@%s @./tmp/mydbscript/clear_all_objects.sql' % ( Env_oracle['user'], Env_oracle['passwd'], Env_oracle['tnsname'] ) )
    #第一次清理数据库中的所有对象不完全，再重新执行一次清除脚本
    os.system( 'sqlplus %s/%s@%s @./tmp/mydbscript/clear_all_objects.sql' % ( Env_oracle['user'], Env_oracle['passwd'], Env_oracle['tnsname'] ) )
    logger.info( '重新构建立数据库，再次清除数据库用户下的所有对象......' )

    script_dir = os.path.abspath( os.path.curdir )
    rtplt_dbscript_dir = os.path.join( script_dir, './tmp/prm/%s/Release/dbscript/rtplt' % prm_build_str )
    dbscript_dir = os.path.join( script_dir, './tmp/prm/%s/Release/dbscript' % prm_build_str )

    logger.info( '执行Prm rtplt的数据库脚本' )
    os.chdir( rtplt_dbscript_dir )
    sqlfilelist = ['install.sql',
                   'install_portal.sql',
                   'patch_1.0.1.0.sql',
                   'patch_1.0.2.0.sql',
                   'patch_1.0.3.0.sql',
                   'patch_1.0.4.0.sql',
                   'patch_1.1.0.050.sql',
                   'patch_1.1.0.050_1.sql',
                   'patch_1.1.0.050_2.sql',
                   'patch_1.1.0.050_3.sql',
                   'patch_1.1.0.050_4.sql',
                   'patch_1.1.0.050_5.sql',
                   'patch_1.1.0.050_6.sql',
                   'patch_1.1.0.050_7.sql',
                   ]

    for sqlfile in sqlfilelist:
        exec_sql( sqlfile, Env_oracle['user'], Env_oracle['passwd'], Env_oracle['tnsname'] )
    
    logger.info( '执行Prm dbscript的数据库脚本' )
    os.chdir( dbscript_dir )
    sqlfilelist = ['prm1.0.0.0/install.sql',
                   #'prm1.0.0.0_dml.sql',
                   #'prm1.0.0.0_dml_announce.sql',
                   'prm1.0.1.0/install.sql',
                   'prm1.0.1.001/install.sql',
				   'prm1.0.1.002/install.sql',
                   'prm1.0.2.0/install.sql',
                   'prm1.0.2.001/install.sql',
                   'prm1.0.2.002/install.sql',
                   'prm1.0.2.003/install.sql',
                   'prm1.0.2.004/install.sql'
                    ]
    for sqlfile in sqlfilelist:
        exec_sql( sqlfile, Env_oracle['user'], Env_oracle['passwd'], Env_oracle['tnsname'] )
    os.chdir( script_dir )

    importPrmMetadata()
    
    #执行二期合作伙伴段权限,需要在元数据执行完成以后才能执行
    logger.info( 'Prm二期合作伙伴端赋权开始' )
    os.chdir( dbscript_dir )
    afterMetadata_sqlfilelist=['prm1.0.1.0/installAfterMetadata.sql',
                               'prm1.0.2.004/installAfterMetadata.sql']
    for sqlfile in afterMetadata_sqlfilelist:
        exec_sql( sqlfile, Env_oracle['user'], Env_oracle['passwd'], Env_oracle['tnsname'] )
        print '%s执行完成' %sqlfile
    os.chdir( script_dir )
    logger.info( 'Prm二期合作伙伴端赋权结束' )

    # 初始化数据
    mydbscript_sqlfilelist = [ '01_init_system_admin',
                              '02_init_system_sp.sql',
                              '03_init_private.sql',
                              '04_init_temp.sql'
                              ]
    for sqlfile in mydbscript_sqlfilelist:
        logger.info( '测试环境初始化数据，%s文件需要入库' % sqlfile )
        os.system( 'sqlplus %s/%s@%s @./tmp/mydbscript/%s > ./tmp/%s.log' % ( Env_oracle['user'], Env_oracle['passwd'], Env_oracle['tnsname'] , sqlfile, sqlfile ) )
        logger.info( '测试环境初始化数据%s的执行日志如下：\n%s' % ( sqlfile, open( './tmp/%s.log' % sqlfile, 'r+' ).read() ) )
    
    return

def exec_sql( full_sqlfile, dbuser, dbpasswd, tnsname ):
    '''有些文件是带目录的，所以需要进到目录中再执行sql'''
    previous_dir = os.path.abspath( os.path.curdir )
    [path, sqlfile] = os.path.split( full_sqlfile )
    if path != '':
        os.chdir( path )
    logger.info( '%s文件需要入库' % full_sqlfile )
    sql_str = open( sqlfile, 'r+' ).read()
    # 总有同学导出sql时把tablespace导入了，所以这里统一替换成测试环境中的tablespace
    testenv_tablespace = 'Data_SIMS20'
    error_tablespace_list = ['DATA_BPM',
                             ]
    for error_tablespace in error_tablespace_list:
        if sql_str.find( error_tablespace ) != -1:
            logger.error( '发现特殊的表空间%s，这里需要改写!' % error_tablespace )
            sql_str.replace( 'tablespace %s' % error_tablespace, 'tablespace %s' % testenv_tablespace )
            open( sqlfile, 'w+' ).write( sql_str )
    # 对于一个文件中全部都是@的情况，打开当前的文件是处理不了的，必须修改所有的@文件
    if sql_str.find( '@' ) != -1 and sql_str.find( '/' ) == -1:
        sub_sqlfile_list = [li.strip( '\n' ).lstrip( '@' ) for li in open( sqlfile, 'r+' ).readlines() if len( li ) >= 10 and li.startswith( '@' )]
        for sub_sql_file in sub_sqlfile_list:
            sub_sql_str = open( sub_sql_file, 'r+' ).read()
            for error_tablespace in error_tablespace_list:
                if sub_sql_str.find( error_tablespace ) != -1:
                    logger.error( '====子SQL文件 %s 发现特殊的表空间%s，这里需要改写!' % ( sub_sql_file, error_tablespace ) )
                    new_sub_sql_str = sub_sql_str.replace( 'tablespace %s' % error_tablespace, 'tablespace %s' % testenv_tablespace )
                    open( sub_sql_file, 'w+' ).write( new_sub_sql_str )
        # 有些开发的兄弟总喜欢直接drop table后再create table:
        for sub_sql_file in sub_sqlfile_list:
            sub_sql_str = open( sub_sql_file, 'r+' ).read()
            if sub_sql_str.find( '\ndrop table' ) != -1:
                new_sub_sql_str = sub_sql_str.replace( '\ndrop table', '\n--drop table' )
                open( sub_sql_file, 'w+' ).write( new_sub_sql_str )
    # 加上exit便于sqlplus退出
    if sql_str.find( 'exit;' ) == -1:
        open( sqlfile, 'w+' ).write( '%s\n\nexit;' % sql_str )
    os.system( 'sqlplus %s/%s@%s @%s > %s.log' % ( dbuser, dbpasswd, tnsname , sqlfile, sqlfile ) )
    # logger.info( '%s的执行日志如下：\n%s' % ( sqlfile, open( '%s.log' % sqlfile, 'r+' ).read() ) )
    log_file = open( '%s.log' % sqlfile, 'r+' ).read ()
    error_line_list = [li for li in open( '%s.log' % sqlfile, 'r+' ).readlines() if li.find( 'ORA-' ) != -1]
    if log_file.find( 'ORA-' ) != -1:
        logger.error( '%s的执行报错, 错误信息如下：\n%s' % ( sqlfile, '\n'.join( error_line_list ) ) )
    else:
        logger.info( '%s执行成功' % full_sqlfile )
    logger.info( log_file)
    os.chdir( previous_dir )
    
def importPrmMetadata():
    logger.info( 'Prm元数据导入,先修改web_bas的jdbc.properties，再执行metadata_import_common.cmd' )
    setKeyValue( './tmp/prm/%s/Release/tools/metadata/web_bas/tools/jdbc.properties' % prm_build_str, 'jdbc.url', 'jdbc:oracle:thin:@%s:1521:%s' % ( Env_oracle['ip'], Env_oracle['sid'] ) )
    setKeyValue( './tmp/prm/%s/Release/tools/metadata/web_bas/tools/jdbc.properties' % prm_build_str, 'jdbc.username', Env_oracle['user'] )
    setKeyValue( './tmp/prm/%s/Release/tools/metadata/web_bas/tools/jdbc.properties' % prm_build_str, 'jdbc.password', Env_oracle['passwd'] )
    script_dir = os.path.abspath( os.path.curdir )
    os.chdir( './tmp/prm/%s/Release/tools/metadata/web_bas/tools/' % prm_build_str )
    tmpstr = open( 'metadata_import_common.cmd', 'r+' ).read().replace( 'pause', '' )
    open( 'metadata_import_common.cmd', 'w+' ).write( tmpstr )
    os.system( 'metadata_import_common.cmd' )
    os.chdir( script_dir )
    logger.info( 'web_bas元数据导入  完成' )

    logger.info( 'Prm元数据导入,再修改自己的jdbc.properties，再执行metadata_import.cmd' )
    setKeyValue( './tmp/prm/%s/Release/tools/metadata/jdbc.properties' % prm_build_str, 'jdbc.url', 'jdbc:oracle:thin:@%s:1521:%s' % ( Env_oracle['ip'], Env_oracle['sid'] ) )
    setKeyValue( './tmp/prm/%s/Release/tools/metadata/jdbc.properties' % prm_build_str, 'jdbc.username', Env_oracle['user'] )
    setKeyValue( './tmp/prm/%s/Release/tools/metadata/jdbc.properties' % prm_build_str, 'jdbc.password', Env_oracle['passwd'] )
    os.chdir( './tmp/prm/%s/Release/tools/metadata' % prm_build_str )
    tmpstr = open( 'metadata_import.cmd', 'r+' ).read().replace( 'pause', '' )
    open( 'metadata_import.cmd', 'w+' ).write( tmpstr )
    os.system( 'metadata_import.cmd' )
    os.chdir( script_dir )
    logger.info( 'Prm元数据导入  完成' )
    
def setKeyValue( filepath, keyname, newvalue ):
    logger.info( '修改配置文件%s  %s = %s' % ( filepath, keyname, newvalue ) )
    linelist = open( filepath ).readlines()
    newlist = []
    for li in linelist:
        if li.lstrip().startswith( keyname ):
            newlist.append( '%s=%s\n' % ( keyname, newvalue ) )
        else:
            newlist.append( li )
    open( filepath, 'w' ).write( ''.join( newlist ) )
    
def stopPrm():
    stdstr = RemoteCmd( Env_prm['ip'], Env_prm['user'], Env_prm['passwd'], 'ps -ef|grep %s|grep java|grep -v grep' % Env_prm['user'], logflag = 0 )
    if stdstr.find( 'java' ) == -1:
        logger.info( 'stopPrm, 进程未启，不用shutdown' )
        return
    RemoteCmd( Env_prm['ip'], Env_prm['user'], Env_prm['passwd'], 'cd %s/bin;sh stop.sh' % Env_prm['jboss_home'] )
    time.sleep( 1 )
    stdstr = RemoteCmd( Env_prm['ip'], Env_prm['user'], Env_prm['passwd'], 'ps -ef|grep %s|grep java|grep -v grep' % Env_prm['user'], logflag = 0 )
    if stdstr.find( 'java' ) != -1:
        for li in stdstr.split( '\n' ):
            if len( li ) > 4:
                pid = li.split()[1]
                RemoteCmd( Env_prm['ip'], Env_prm['user'], Env_prm['passwd'], 'kill %s' % pid , logflag = 0 )

def stopIodd():
    stdstr = RemoteCmd( Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'], 'ps -ef|grep %s|grep java|grep -v grep' % Env_iodd['user'], logflag = 0 )
    if stdstr.find( 'java' ) == -1:
        logger.info( 'stopIodd, 进程未启，不用shutdown' )
        return
    RemoteCmd( Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'], 'cd %s/bin;sh stop.sh' % Env_iodd['jboss_home'] )
    time.sleep( 1 )
    stdstr = RemoteCmd( Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'], 'ps -ef|grep %s|grep java|grep -v grep' % Env_iodd['user'], logflag = 0 )
    if stdstr.find( 'java' ) != -1:
        for li in stdstr.split( '\n' ):
            if len( li ) > 4:
                pid = li.split()[1]
                RemoteCmd( Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'], 'kill %s' % pid , logflag = 0 )

def startPrm():
    logger.info( 'startPrm' )
    RemoteCmd( Env_prm['ip'], Env_prm['user'], Env_prm['passwd'], 'cd %s/bin;nohup sh start.sh -Djboss.service.binding.set=ports-01 -b 0.0.0.0 > nohup.out &' % Env_prm['jboss_home'] )

def startIodd():
    logger.info( 'startIodd' )
    RemoteCmd( Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'], 'cd %s/bin;nohup sh start.sh -Djboss.service.binding.set=ports-01 -b 0.0.0.0 > nohup.out &' % Env_iodd['jboss_home'] )
    
def RemoteCmd( ip, username, password, command, logflag = 1 ):
    global SSH_flag
    std_info = None
    if SSH_flag == 1:
        std_info = SSHCmd( ip, username, password, command, logflag )
    else:
        std_info = TelnetCmd( ip, username, password, command, logflag )
    return std_info

def SSHCmd( ip, username, password, command = 'ls -alt ', logflag = 1 ):
    if logflag == 1:
        logger.debug( '执行远程SSH命令,环境%s:%s:%s,命令%s' % ( ip, username, password, command ) )
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
    client.connect( ip, 22, username, password, timeout = 4 )
    command = 'source ~/.bash_profile;' + command
    stdin, stdout, stderr = client.exec_command( command )
    std_info = ''.join( stdout.readlines() )
    error_info_list = stderr.readlines()
    if len( error_info_list ) > 0:
        logger.debug( '存在stderror' )
        std_error = ''.join( error_info_list )
        std_info = std_info + std_error
    if logflag == 1:
        logger.info( 'SSH Command, Result:\n%s' % std_info )
    client.close()
    client = None
    return std_info

stopIodd()
stopPrm()    
rebuildDb()
startPrm()
startIodd()
