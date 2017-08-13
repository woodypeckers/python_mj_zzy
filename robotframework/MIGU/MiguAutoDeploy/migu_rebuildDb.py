# -*- coding:cp936 -*-
import os
import logging
import paramiko
import time
import sys

Env_oracle = {'name':'db', 'type':'oracle', 'ip':'10.12.3.197', 'port':'1521', 'user':'migu_auto', 'passwd':'migu_prm_auto', 'tnsname':'10.12.3.197', 'sid':'ora11g'}
Env_server = {'name':'miguserver', 'type':'jboss', 'ip':'10.12.12.157', 'port':'48080', 'user':'miguauto', 'passwd':'miguauto', 'jboss_home':'/opt/aspire/product/miguauto/jboss_server'}
Env_iodd = {'name':'miguiodd', 'type':'jboss', 'ip':'10.12.12.157', 'port':'58080', 'user':'miguauto', 'passwd':'miguauto', 'jboss_home':'/opt/aspire/product/miguauto/jboss_iodd', 'sims_inf_url':'http://10.12.12.157:9001'}
Env_admin = {'name':'miguadmin', 'type':'jboss', 'ip':'10.12.12.157', 'port':'38080', 'user':'miguauto', 'passwd':'miguauto', 'jboss_home':'/opt/aspire/product/miguauto/jboss_admin', 'sims_inf_url':'http://10.12.12.157:9001'}
Env_partner = {'name':'migupartner', 'type':'jboss', 'ip':'10.12.12.157', 'port':'61080', 'user':'miguauto', 'passwd':'miguauto', 'jboss_home':'/opt/aspire/product/miguauto/jboss_partner', 'sims_inf_url':'http://10.12.12.157:9001'}
Env_miguauto = {'name':'miguauto', 'ip':'10.12.12.157', 'user':'miguauto', 'passwd':'miguauto', 'jboss_home':'/opt/aspire/product/miguauto'}

migu_build_folder = r'\\ASP-BLD-SERV100\release_bldstg\MIGU_PRM\MIGU_PRM1.0.2.0\MIGU_PRM1.0.2.0_SSYT_11__20151216_16.30.54'
migu_build_str = migu_build_folder.split( '\\' )[-1]


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
    rtplt_dbscript_dir = os.path.join( script_dir, './tmp/migu/%s/Release/dbscript/rtplt' % migu_build_str )
    dbscript_dir = os.path.join( script_dir, './tmp/migu/%s/Release/dbscript' % migu_build_str )
    #web_bas2.0数据库脚本的路径
    webbas_dbscript_dir = os.path.join( script_dir, './tmp/migu/%s/Release/authmgt/dbscript' % migu_build_str )
    
    #执行rtplt的数据库脚本
    logger.info( '执行migu rtplt的数据库脚本' )
    os.chdir( rtplt_dbscript_dir )
    print rtplt_dbscript_dir
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
                   'patch_1.1.0.050_8.sql',          #MIGU1.0.1.0新增
                   ]

    for sqlfile in sqlfilelist:
        exec_sql( sqlfile, Env_oracle['user'], Env_oracle['passwd'], Env_oracle['tnsname'] )

    #执行migu的数据库脚本
    logger.info( '执行migu dbscript的数据库脚本' )
    print dbscript_dir
    os.chdir( dbscript_dir )
    sqlfilelist = ['migu1.0.0.0/install.sql',
                   'migu1.0.0.001/install.sql',
                   'migu1.0.1.0/install.sql',
                   'migu1.0.2.0/install.sql']
    for sqlfile in sqlfilelist:
        exec_sql( sqlfile, Env_oracle['user'], Env_oracle['passwd'], Env_oracle['tnsname'] )
    os.chdir( script_dir )
	
    #导入元数据
    importMiguMetadata()
    
    #执行webbas2.0的数据库脚本
    logger.info( '执行webbas2.0的数据库脚本' )
    os.chdir( webbas_dbscript_dir )
    sqlfilelist = ['webbase2.0.0.001_dml.sql']
    for sqlfile in sqlfilelist:
        exec_sql( sqlfile, Env_oracle['user'], Env_oracle['passwd'], Env_oracle['tnsname'] )
    os.chdir( script_dir )
    
    #预置初始化数据
    mydbscript_sqlfilelist = [ '01migu_init_system_admin.sql'
                               '02migu_init_dbscipt.sql',
                               '03webbas_init_dbscipt.sql']
    for sqlfile in mydbscript_sqlfilelist:
        logger.info( '测试环境初始化数据，%s文件需要入库' % sqlfile )
        os.system( 'sqlplus %s/%s@%s @./tmp/mydbscript/%s > ./tmp/%s.log' % ( Env_oracle['user'], Env_oracle['passwd'], Env_oracle['tnsname'] , sqlfile, sqlfile ) )
        logger.info( '测试环境初始化数据%s的执行日志如下：\n%s' % ( sqlfile, open( './tmp/%s.log' % sqlfile, 'r+' ).read() ) )
    
    #执行元数据执行完成后的数据库脚本
    os.chdir( dbscript_dir )
    afterMetadata_sqlfilelist=['migu1.0.0.0/installAfterMetadata.sql',
                               'migu1.0.1.0/installAfterMetadata.sql',
                               'migu1.0.2.0/installAfterMetadata.sql']
    for sqlfile in afterMetadata_sqlfilelist:
        exec_sql( sqlfile, Env_oracle['user'], Env_oracle['passwd'], Env_oracle['tnsname'] )
        print '需要在元数据执行完毕后才可以执行的数据库脚本%s执行完毕' %sqlfile
		
    os.chdir( script_dir )
    return

def exec_sql( full_sqlfile, dbuser, dbpasswd, tnsname ):
    '''有些文件是带目录的，所以需要进到目录中再执行sql'''
    previous_dir = os.path.abspath( os.path.curdir )
    [path, sqlfile] = os.path.split( full_sqlfile )
    if path != '':
        os.chdir( path )
    logger.info( '%s文件需要入库' % full_sqlfile )
    sql_str = open( sqlfile, 'r+' ).read()
    # 加上commit提交SQL
    if sql_str.find( 'commit;' ) == -1:
        open( sqlfile, 'w+' ).write( '%s\n\ncommit;' % sql_str )
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
    
def importMiguMetadata():
    '''导入web_bas1.0的元数据'''
    logger.info( 'web_bas1.0元数据导入,先修改web_bas1.0的jdbc.properties，再执行metadata_import_common.cmd' )
    setKeyValue( './tmp/migu/%s/Release/tools/metadata/web_bas/tools/jdbc.properties' % migu_build_str, 'jdbc.url', 'jdbc:oracle:thin:@%s:1521:%s' % ( Env_oracle['ip'], Env_oracle['sid'] ) )
    setKeyValue( './tmp/migu/%s/Release/tools/metadata/web_bas/tools/jdbc.properties' % migu_build_str, 'jdbc.username', Env_oracle['user'] )
    setKeyValue( './tmp/migu/%s/Release/tools/metadata/web_bas/tools/jdbc.properties' % migu_build_str, 'jdbc.password', Env_oracle['passwd'] )
    script_dir = os.path.abspath( os.path.curdir )
    os.chdir( './tmp/migu/%s/Release/tools/metadata/web_bas/tools/' % migu_build_str )
    tmpstr = open( 'metadata_import_common.cmd', 'r+' ).read().replace( 'pause', '' )
    open( 'metadata_import_common.cmd', 'w+' ).write( tmpstr )
    os.system( 'metadata_import_common.cmd' )
    os.chdir( script_dir )
    logger.info( 'web_bas1.0元数据导入完成' )

    '''导入migu的元数据'''
    logger.info( 'migu元数据导入,再修改自己的jdbc.properties，再执行metadata_import.cmd' )
    setKeyValue( './tmp/migu/%s/Release/tools/metadata/jdbc.properties' % migu_build_str, 'jdbc.url', 'jdbc:oracle:thin:@%s:1521:%s' % ( Env_oracle['ip'], Env_oracle['sid'] ) )
    setKeyValue( './tmp/migu/%s/Release/tools/metadata/jdbc.properties' % migu_build_str, 'jdbc.username', Env_oracle['user'] )
    setKeyValue( './tmp/migu/%s/Release/tools/metadata/jdbc.properties' % migu_build_str, 'jdbc.password', Env_oracle['passwd'] )
    os.chdir( './tmp/migu/%s/Release/tools/metadata' % migu_build_str )
    tmpstr = open( 'metadata_import.cmd', 'r+' ).read().replace( 'pause', '' )
    open( 'metadata_import.cmd', 'w+' ).write( tmpstr )
    os.system( 'metadata_import.cmd' )
    os.chdir( script_dir )
    logger.info( 'migu元数据导入完成' )
    
    '''导入web_bas2.0的元数据'''
    logger.info( 'web_bas2.0元数据导入,先修改web_bas2.0的jdbc.properties，再执行metadata_import_common.cmd' )
    setKeyValue( './tmp/migu/%s/Release/authmgt/metadata/tools/jdbc.properties' % migu_build_str, 'jdbc.url', 'jdbc:oracle:thin:@%s:1521:%s' % ( Env_oracle['ip'], Env_oracle['sid'] ) )
    setKeyValue( './tmp/migu/%s/Release/authmgt/metadata/tools/jdbc.properties' % migu_build_str, 'jdbc.username', Env_oracle['user'] )
    setKeyValue( './tmp/migu/%s/Release/authmgt/metadata/tools/jdbc.properties' % migu_build_str, 'jdbc.password', Env_oracle['passwd'] )
    script_dir = os.path.abspath( os.path.curdir )
    os.chdir( './tmp/migu/%s/Release/authmgt/metadata/tools/' % migu_build_str )
    tmpstr = open( 'metadata_import_common.cmd', 'r+' ).read().replace( 'pause', '' )
    open( 'metadata_import_common.cmd', 'w+' ).write( tmpstr )
    os.system( 'metadata_import_common.cmd' )
    os.chdir( script_dir )
    logger.info( 'web_bas2.0元数据导入完成' )
    
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
    
def stopMigu():
    stdstr = RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'], 'ps -ef|grep %s|grep java|grep -v grep' % Env_miguauto['user'], logflag = 0 )
    if stdstr.find( 'java' ) == -1:
        logger.info( 'stopMigu, 进程未启，不用shutdown' )
        return
    RemoteCmd( Env_server['ip'], Env_server['user'], Env_server['passwd'], 'cd %s/bin;sh stop.sh' % Env_server['jboss_home'] )
    RemoteCmd( Env_admin['ip'], Env_admin['user'], Env_admin['passwd'], 'cd %s/bin;sh stop.sh' % Env_admin['jboss_home'] )
    RemoteCmd( Env_partner['ip'], Env_partner['user'], Env_partner['passwd'], 'cd %s/bin;sh stop.sh' % Env_partner['jboss_home'] )
    time.sleep( 2 )
    stdstr = RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'], 'ps -ef|grep %s|grep java|grep -v grep' % Env_miguauto['user'], logflag = 0 )
    #停止之后，如果发现还存在migu用户的进程，直接kill掉
    if stdstr.find( 'java' ) != -1:
        for li in stdstr.split( '\n' ):
            if len( li ) > 4:
                pid = li.split()[1]
                RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'], 'kill %s' % pid , logflag = 0 )

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

def stopWebbas():
    #停止webbas2.0服务
    RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
           'cd %s/tomcat-authmgt/bin;./stop.sh' % Env_miguauto['jboss_home'] )
                
def startMigu():
    logger.info( 'startMigu' )
    RemoteCmd( Env_server['ip'], Env_server['user'], Env_server['passwd'], 'cd %s/bin;nohup sh start.sh -Djboss.service.binding.set=ports-01 -b 0.0.0.0 > nohup.out &' % Env_server['jboss_home'] )
    RemoteCmd( Env_admin['ip'], Env_admin['user'], Env_admin['passwd'], 'cd %s/bin;nohup sh start.sh -Djboss.service.binding.set=ports-01 -b 0.0.0.0 > nohup.out &' % Env_admin['jboss_home'] )
    RemoteCmd( Env_partner['ip'], Env_partner['user'], Env_partner['passwd'], 'cd %s/bin;nohup sh start.sh -Djboss.service.binding.set=ports-01 -b 0.0.0.0 > nohup.out &' % Env_partner['jboss_home'] )

def startIodd():
    logger.info( 'startIodd' )
    RemoteCmd( Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'], 'cd %s/bin;nohup sh start.sh -Djboss.service.binding.set=ports-01 -b 0.0.0.0 > nohup.out &' % Env_iodd['jboss_home'] )

def startWebbas():
    '''启动webbas2.0'''
    logger.info( '启动webbas2.0' )
    RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'], 'cd %s/tomcat-authmgt/bin;./s start' % Env_miguauto['jboss_home'] )

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

if __name__ == "__main__":
    stopMigu()
    stopIodd()
    stopWebbas()
    rebuildDb()
    startMigu()
    startIodd()
    startWebbas()