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
runtimelog = logging.FileHandler( "������־_rebuildDb.log" )
runtimelog.setFormatter( formatter )
logger.addHandler( runtimelog )
# д�����ܣ��粻��Ҫ������ע����������
stdoutlog = logging.StreamHandler( sys.stdout )
stdoutlog.setFormatter( formatter )
logger.addHandler( stdoutlog )
logger.setLevel( logging.DEBUG )  # DEBUG, INFO, WARNING, ERROR, CRITICAL ...etc

SSH_flag = 1

def rebuildDb():
    '''ִ�й̶�sql,ԭ�����������ݿ��е����ж����ٰ�˳����SQL'''
    logger.info( '���¹��������ݿ⣬��������ݿ��û��µ����ж���......' )
    os.system( 'sqlplus %s/%s@%s @./tmp/mydbscript/clear_all_objects.sql' % ( Env_oracle['user'], Env_oracle['passwd'], Env_oracle['tnsname'] ) )
    #��һ���������ݿ��е����ж�����ȫ��������ִ��һ������ű�
    os.system( 'sqlplus %s/%s@%s @./tmp/mydbscript/clear_all_objects.sql' % ( Env_oracle['user'], Env_oracle['passwd'], Env_oracle['tnsname'] ) )
    logger.info( '���¹��������ݿ⣬�ٴ�������ݿ��û��µ����ж���......' )
    
    script_dir = os.path.abspath( os.path.curdir )
    rtplt_dbscript_dir = os.path.join( script_dir, './tmp/migu/%s/Release/dbscript/rtplt' % migu_build_str )
    dbscript_dir = os.path.join( script_dir, './tmp/migu/%s/Release/dbscript' % migu_build_str )
    #web_bas2.0���ݿ�ű���·��
    webbas_dbscript_dir = os.path.join( script_dir, './tmp/migu/%s/Release/authmgt/dbscript' % migu_build_str )
    
    #ִ��rtplt�����ݿ�ű�
    logger.info( 'ִ��migu rtplt�����ݿ�ű�' )
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
                   'patch_1.1.0.050_8.sql',          #MIGU1.0.1.0����
                   ]

    for sqlfile in sqlfilelist:
        exec_sql( sqlfile, Env_oracle['user'], Env_oracle['passwd'], Env_oracle['tnsname'] )

    #ִ��migu�����ݿ�ű�
    logger.info( 'ִ��migu dbscript�����ݿ�ű�' )
    print dbscript_dir
    os.chdir( dbscript_dir )
    sqlfilelist = ['migu1.0.0.0/install.sql',
                   'migu1.0.0.001/install.sql',
                   'migu1.0.1.0/install.sql',
                   'migu1.0.2.0/install.sql']
    for sqlfile in sqlfilelist:
        exec_sql( sqlfile, Env_oracle['user'], Env_oracle['passwd'], Env_oracle['tnsname'] )
    os.chdir( script_dir )
	
    #����Ԫ����
    importMiguMetadata()
    
    #ִ��webbas2.0�����ݿ�ű�
    logger.info( 'ִ��webbas2.0�����ݿ�ű�' )
    os.chdir( webbas_dbscript_dir )
    sqlfilelist = ['webbase2.0.0.001_dml.sql']
    for sqlfile in sqlfilelist:
        exec_sql( sqlfile, Env_oracle['user'], Env_oracle['passwd'], Env_oracle['tnsname'] )
    os.chdir( script_dir )
    
    #Ԥ�ó�ʼ������
    mydbscript_sqlfilelist = [ '01migu_init_system_admin.sql'
                               '02migu_init_dbscipt.sql',
                               '03webbas_init_dbscipt.sql']
    for sqlfile in mydbscript_sqlfilelist:
        logger.info( '���Ի�����ʼ�����ݣ�%s�ļ���Ҫ���' % sqlfile )
        os.system( 'sqlplus %s/%s@%s @./tmp/mydbscript/%s > ./tmp/%s.log' % ( Env_oracle['user'], Env_oracle['passwd'], Env_oracle['tnsname'] , sqlfile, sqlfile ) )
        logger.info( '���Ի�����ʼ������%s��ִ����־���£�\n%s' % ( sqlfile, open( './tmp/%s.log' % sqlfile, 'r+' ).read() ) )
    
    #ִ��Ԫ����ִ����ɺ�����ݿ�ű�
    os.chdir( dbscript_dir )
    afterMetadata_sqlfilelist=['migu1.0.0.0/installAfterMetadata.sql',
                               'migu1.0.1.0/installAfterMetadata.sql',
                               'migu1.0.2.0/installAfterMetadata.sql']
    for sqlfile in afterMetadata_sqlfilelist:
        exec_sql( sqlfile, Env_oracle['user'], Env_oracle['passwd'], Env_oracle['tnsname'] )
        print '��Ҫ��Ԫ����ִ����Ϻ�ſ���ִ�е����ݿ�ű�%sִ�����' %sqlfile
		
    os.chdir( script_dir )
    return

def exec_sql( full_sqlfile, dbuser, dbpasswd, tnsname ):
    '''��Щ�ļ��Ǵ�Ŀ¼�ģ�������Ҫ����Ŀ¼����ִ��sql'''
    previous_dir = os.path.abspath( os.path.curdir )
    [path, sqlfile] = os.path.split( full_sqlfile )
    if path != '':
        os.chdir( path )
    logger.info( '%s�ļ���Ҫ���' % full_sqlfile )
    sql_str = open( sqlfile, 'r+' ).read()
    # ����commit�ύSQL
    if sql_str.find( 'commit;' ) == -1:
        open( sqlfile, 'w+' ).write( '%s\n\ncommit;' % sql_str )
    # ����exit����sqlplus�˳�
    if sql_str.find( 'exit;' ) == -1:
        open( sqlfile, 'w+' ).write( '%s\n\nexit;' % sql_str )
    os.system( 'sqlplus %s/%s@%s @%s > %s.log' % ( dbuser, dbpasswd, tnsname , sqlfile, sqlfile ) )
    # logger.info( '%s��ִ����־���£�\n%s' % ( sqlfile, open( '%s.log' % sqlfile, 'r+' ).read() ) )
    log_file = open( '%s.log' % sqlfile, 'r+' ).read ()
    error_line_list = [li for li in open( '%s.log' % sqlfile, 'r+' ).readlines() if li.find( 'ORA-' ) != -1]
    if log_file.find( 'ORA-' ) != -1:
        logger.error( '%s��ִ�б���, ������Ϣ���£�\n%s' % ( sqlfile, '\n'.join( error_line_list ) ) )
    else:
        logger.info( '%sִ�гɹ�' % full_sqlfile )
    logger.info( log_file)
    os.chdir( previous_dir )
    
def importMiguMetadata():
    '''����web_bas1.0��Ԫ����'''
    logger.info( 'web_bas1.0Ԫ���ݵ���,���޸�web_bas1.0��jdbc.properties����ִ��metadata_import_common.cmd' )
    setKeyValue( './tmp/migu/%s/Release/tools/metadata/web_bas/tools/jdbc.properties' % migu_build_str, 'jdbc.url', 'jdbc:oracle:thin:@%s:1521:%s' % ( Env_oracle['ip'], Env_oracle['sid'] ) )
    setKeyValue( './tmp/migu/%s/Release/tools/metadata/web_bas/tools/jdbc.properties' % migu_build_str, 'jdbc.username', Env_oracle['user'] )
    setKeyValue( './tmp/migu/%s/Release/tools/metadata/web_bas/tools/jdbc.properties' % migu_build_str, 'jdbc.password', Env_oracle['passwd'] )
    script_dir = os.path.abspath( os.path.curdir )
    os.chdir( './tmp/migu/%s/Release/tools/metadata/web_bas/tools/' % migu_build_str )
    tmpstr = open( 'metadata_import_common.cmd', 'r+' ).read().replace( 'pause', '' )
    open( 'metadata_import_common.cmd', 'w+' ).write( tmpstr )
    os.system( 'metadata_import_common.cmd' )
    os.chdir( script_dir )
    logger.info( 'web_bas1.0Ԫ���ݵ������' )

    '''����migu��Ԫ����'''
    logger.info( 'miguԪ���ݵ���,���޸��Լ���jdbc.properties����ִ��metadata_import.cmd' )
    setKeyValue( './tmp/migu/%s/Release/tools/metadata/jdbc.properties' % migu_build_str, 'jdbc.url', 'jdbc:oracle:thin:@%s:1521:%s' % ( Env_oracle['ip'], Env_oracle['sid'] ) )
    setKeyValue( './tmp/migu/%s/Release/tools/metadata/jdbc.properties' % migu_build_str, 'jdbc.username', Env_oracle['user'] )
    setKeyValue( './tmp/migu/%s/Release/tools/metadata/jdbc.properties' % migu_build_str, 'jdbc.password', Env_oracle['passwd'] )
    os.chdir( './tmp/migu/%s/Release/tools/metadata' % migu_build_str )
    tmpstr = open( 'metadata_import.cmd', 'r+' ).read().replace( 'pause', '' )
    open( 'metadata_import.cmd', 'w+' ).write( tmpstr )
    os.system( 'metadata_import.cmd' )
    os.chdir( script_dir )
    logger.info( 'miguԪ���ݵ������' )
    
    '''����web_bas2.0��Ԫ����'''
    logger.info( 'web_bas2.0Ԫ���ݵ���,���޸�web_bas2.0��jdbc.properties����ִ��metadata_import_common.cmd' )
    setKeyValue( './tmp/migu/%s/Release/authmgt/metadata/tools/jdbc.properties' % migu_build_str, 'jdbc.url', 'jdbc:oracle:thin:@%s:1521:%s' % ( Env_oracle['ip'], Env_oracle['sid'] ) )
    setKeyValue( './tmp/migu/%s/Release/authmgt/metadata/tools/jdbc.properties' % migu_build_str, 'jdbc.username', Env_oracle['user'] )
    setKeyValue( './tmp/migu/%s/Release/authmgt/metadata/tools/jdbc.properties' % migu_build_str, 'jdbc.password', Env_oracle['passwd'] )
    script_dir = os.path.abspath( os.path.curdir )
    os.chdir( './tmp/migu/%s/Release/authmgt/metadata/tools/' % migu_build_str )
    tmpstr = open( 'metadata_import_common.cmd', 'r+' ).read().replace( 'pause', '' )
    open( 'metadata_import_common.cmd', 'w+' ).write( tmpstr )
    os.system( 'metadata_import_common.cmd' )
    os.chdir( script_dir )
    logger.info( 'web_bas2.0Ԫ���ݵ������' )
    
def setKeyValue( filepath, keyname, newvalue ):
    logger.info( '�޸������ļ�%s  %s = %s' % ( filepath, keyname, newvalue ) )
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
        logger.info( 'stopMigu, ����δ��������shutdown' )
        return
    RemoteCmd( Env_server['ip'], Env_server['user'], Env_server['passwd'], 'cd %s/bin;sh stop.sh' % Env_server['jboss_home'] )
    RemoteCmd( Env_admin['ip'], Env_admin['user'], Env_admin['passwd'], 'cd %s/bin;sh stop.sh' % Env_admin['jboss_home'] )
    RemoteCmd( Env_partner['ip'], Env_partner['user'], Env_partner['passwd'], 'cd %s/bin;sh stop.sh' % Env_partner['jboss_home'] )
    time.sleep( 2 )
    stdstr = RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'], 'ps -ef|grep %s|grep java|grep -v grep' % Env_miguauto['user'], logflag = 0 )
    #ֹ֮ͣ��������ֻ�����migu�û��Ľ��̣�ֱ��kill��
    if stdstr.find( 'java' ) != -1:
        for li in stdstr.split( '\n' ):
            if len( li ) > 4:
                pid = li.split()[1]
                RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'], 'kill %s' % pid , logflag = 0 )

def stopIodd():
    stdstr = RemoteCmd( Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'], 'ps -ef|grep %s|grep java|grep -v grep' % Env_iodd['user'], logflag = 0 )
    if stdstr.find( 'java' ) == -1:
        logger.info( 'stopIodd, ����δ��������shutdown' )
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
    #ֹͣwebbas2.0����
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
    '''����webbas2.0'''
    logger.info( '����webbas2.0' )
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
        logger.debug( 'ִ��Զ��SSH����,����%s:%s:%s,����%s' % ( ip, username, password, command ) )
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
    client.connect( ip, 22, username, password, timeout = 4 )
    command = 'source ~/.bash_profile;' + command
    stdin, stdout, stderr = client.exec_command( command )
    std_info = ''.join( stdout.readlines() )
    error_info_list = stderr.readlines()
    if len( error_info_list ) > 0:
        logger.debug( '����stderror' )
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