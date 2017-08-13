# -*- coding:cp936 -*-
from migu_utils import *
import os
import shutil
import zipfile
import time
from migu_deploy import *

def getLastbuildFile():
    '''��ȡ���µ�build��copy����ǰĿ¼�µ�tmpĿ¼'''
    if os.path.exists( 'tmp\\migu\\%s\\' % migu_build_str ) == False:
        logger.info( '��ȡmigu�����°汾: %s' % migu_build_str )
        CleanDir( './tmp/migu' )
        os.system( 'xcopy /E /R /Y %s tmp\\migu\\%s\\' % ( migu_build_folder, migu_build_str ) )

def sftpuploadfolder( localdir, ip, user, passwd, remotepdir ):
    '''�������ϵ�Ŀ¼���,ftp��Զ�̷������ϣ��ٽ��'''
    script_dir = os.path.abspath( os.path.curdir )
    folder_name = os.path.split( localdir )[-1]
    localdir_parent = os.path.sep.join( os.path.split( localdir )[:-1] )
    os.chdir( localdir_parent )
    os.system( 'zip -r -l %s.zip %s' % ( folder_name, folder_name ) )
    os.chdir( script_dir )
    zipfile_path = os.path.join( localdir_parent, '%s.zip' % folder_name )
    remotefile = remotepdir + '/' + folder_name + '.zip'
    zipfile_name = folder_name + '.zip'
    sftpupload( zipfile_path, ip, user, passwd, remotefile, mode = 'bin' )
    RemoteCmd( ip, user, passwd, 'cd %s;unzip -u -o %s; rm %s' % ( remotepdir, zipfile_name, zipfile_name ) )

    pass

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
    mydbscript_sqlfilelist = [ '01migu_init_system_admin.sql',
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
    '''
    # ����ͬѧ����sqlʱ��tablespace�����ˣ���������ͳһ�滻�ɲ��Ի����е�tablespace
    testenv_tablespace = 'Data_SIMS20'
    error_tablespace_list = ['DATA_BPM',
                             ]
    for error_tablespace in error_tablespace_list:
        if sql_str.find( error_tablespace ) != -1:
            logger.error( '��������ı�ռ�%s��������Ҫ��д!' % error_tablespace )
            sql_str.replace( 'tablespace %s' % error_tablespace, 'tablespace %s' % testenv_tablespace )
            open( sqlfile, 'w+' ).write( sql_str )
    # ����һ���ļ���ȫ������@��������򿪵�ǰ���ļ��Ǵ����˵ģ������޸����е�@�ļ�
    if sql_str.find( '@' ) != -1 and sql_str.find( '/' ) == -1:
        sub_sqlfile_list = [li.strip( '\n' ).lstrip( '@' ) for li in open( sqlfile, 'r+' ).readlines() if len( li ) >= 10 and li.startswith( '@' )]
        for sub_sql_file in sub_sqlfile_list:
            sub_sql_str = open( sub_sql_file, 'r+' ).read()
            for error_tablespace in error_tablespace_list:
                if sub_sql_str.find( error_tablespace ) != -1:
                    logger.error( '====��SQL�ļ� %s ��������ı�ռ�%s��������Ҫ��д!' % ( sub_sql_file, error_tablespace ) )
                    new_sub_sql_str = sub_sql_str.replace( 'tablespace %s' % error_tablespace, 'tablespace %s' % testenv_tablespace )
                    open( sub_sql_file, 'w+' ).write( new_sub_sql_str )
        
        # ��Щ�������ֵ���ϲ��ֱ��drop table����create table:
        for sub_sql_file in sub_sqlfile_list:
            sub_sql_str = open( sub_sql_file, 'r+' ).read()
            if sub_sql_str.find( '\ndrop table' ) != -1:
                new_sub_sql_str = sub_sql_str.replace( '\ndrop table', '\n--drop table' )
                open( sub_sql_file, 'w+' ).write( new_sub_sql_str )
    '''
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

def modifyRemoteMiguConf():
    #�޸�server�����attachment.properties
    sftpdownload( Env_server['ip'], Env_server['user'], Env_server['passwd'],
              '%s/bin/deploy_config/attachment/attachment.properties' % Env_server['jboss_home'],
              './tmp/attachment.properties',
              mode = 'ascii' )
    setKeyValue( './tmp/attachment.properties', 'SIMS_ID', '888' )
    setKeyValue( './tmp/attachment.properties', 'FILE_TYPE', 'sftp' )
    setKeyValue( './tmp/attachment.properties', 'FILE_SERVER_IP', '10.12.12.157' )
    setKeyValue( './tmp/attachment.properties', 'FILE_SERVER_PORT', '22' )
    setKeyValue( './tmp/attachment.properties', 'USERNAME', 'miguauto' )
    setKeyValue( './tmp/attachment.properties', 'PASSWORD', 'miguauto' )
    setKeyValue( './tmp/attachment.properties', 'ABSOLUTE_UPLOAD_PATH', '/opt/aspire/product/miguauto/attachment' )
    setKeyValue( './tmp/attachment.properties', 'ABSOLUTE_SYNC_PATH', '/opt/aspire/product/miguauto/sync' )
    setKeyValue( './tmp/attachment.properties', 'LOCAL_ABSOLUTE_TEMP_PATH', '/opt/aspire/product/miguauto/temp' )
    sftpupload( './tmp/attachment.properties',
              Env_server['ip'], Env_server['user'], Env_server['passwd'],
              '%s/bin/deploy_config/attachment/attachment.properties' % Env_server['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/attachment.properties' )
    
    #�޸�server deploy_config/settlement�����attachment.properties,MIGU1.0.2.0����
    sftpdownload( Env_server['ip'], Env_server['user'], Env_server['passwd'],
              '%s/bin/deploy_config/settlement/attachment.properties' % Env_server['jboss_home'],
              './tmp/attachment.properties',
              mode = 'ascii' )
    setKeyValue( './tmp/attachment.properties', 'SIMS_ID', '888' )
    setKeyValue( './tmp/attachment.properties', 'FILE_TYPE', 'sftp' )
    setKeyValue( './tmp/attachment.properties', 'FILE_SERVER_IP', '10.12.12.157' )
    setKeyValue( './tmp/attachment.properties', 'FILE_SERVER_PORT', '22' )
    setKeyValue( './tmp/attachment.properties', 'USERNAME', 'miguauto' )
    setKeyValue( './tmp/attachment.properties', 'PASSWORD', 'miguauto' )
    setKeyValue( './tmp/attachment.properties', 'ABSOLUTE_UPLOAD_PATH', '/opt/aspire/product/miguauto/settlement_copy' )
    sftpupload( './tmp/attachment.properties',
              Env_server['ip'], Env_server['user'], Env_server['passwd'],
              '%s/bin/deploy_config/settlement/attachment.properties' % Env_server['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/attachment.properties' )
    
    #�޸�admin�����attachment.properties
    sftpdownload( Env_admin['ip'], Env_admin['user'], Env_admin['passwd'],
              '%s/bin/deploy_config/attachment/attachment.properties' % Env_admin['jboss_home'],
              './tmp/attachment.properties',
              mode = 'ascii' )
    setKeyValue( './tmp/attachment.properties', 'SIMS_ID', '888' )
    setKeyValue( './tmp/attachment.properties', 'FILE_TYPE', 'sftp' )
    setKeyValue( './tmp/attachment.properties', 'FILE_SERVER_IP', '10.12.12.157' )
    setKeyValue( './tmp/attachment.properties', 'FILE_SERVER_PORT', '22' )
    setKeyValue( './tmp/attachment.properties', 'USERNAME', 'miguauto' )
    setKeyValue( './tmp/attachment.properties', 'PASSWORD', 'miguauto' )
    setKeyValue( './tmp/attachment.properties', 'ABSOLUTE_UPLOAD_PATH', '/opt/aspire/product/miguauto/attachment' )
    setKeyValue( './tmp/attachment.properties', 'ABSOLUTE_SYNC_PATH', '/opt/aspire/product/miguauto/sync' )
    setKeyValue( './tmp/attachment.properties', 'LOCAL_ABSOLUTE_TEMP_PATH', '/opt/aspire/product/miguauto/temp' )
    sftpupload( './tmp/attachment.properties',
              Env_admin['ip'], Env_admin['user'], Env_admin['passwd'],
              '%s/bin/deploy_config/attachment/attachment.properties' % Env_admin['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/attachment.properties' )
    
    #�޸�partner�����attachment.properties
    sftpdownload( Env_partner['ip'], Env_partner['user'], Env_partner['passwd'],
              '%s/bin/deploy_config/attachment/attachment.properties' % Env_partner['jboss_home'],
              './tmp/attachment.properties',
              mode = 'ascii' )
    setKeyValue( './tmp/attachment.properties', 'SIMS_ID', '888' )
    setKeyValue( './tmp/attachment.properties', 'FILE_TYPE', 'sftp' )
    setKeyValue( './tmp/attachment.properties', 'FILE_SERVER_IP', '10.12.12.157' )
    setKeyValue( './tmp/attachment.properties', 'FILE_SERVER_PORT', '22' )
    setKeyValue( './tmp/attachment.properties', 'USERNAME', 'miguauto' )
    setKeyValue( './tmp/attachment.properties', 'PASSWORD', 'miguauto' )
    setKeyValue( './tmp/attachment.properties', 'ABSOLUTE_UPLOAD_PATH', '/opt/aspire/product/miguauto/attachment' )
    setKeyValue( './tmp/attachment.properties', 'ABSOLUTE_SYNC_PATH', '/opt/aspire/product/miguauto/sync' )
    setKeyValue( './tmp/attachment.properties', 'LOCAL_ABSOLUTE_TEMP_PATH', '/opt/aspire/product/miguauto/temp' )
    sftpupload( './tmp/attachment.properties',
              Env_partner['ip'], Env_partner['user'], Env_partner['passwd'],
              '%s/bin/deploy_config/attachment/attachment.properties' % Env_partner['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/attachment.properties' )

    #�޸�server�����deploy_config\authproxy\authproxy.xml
    sftpdownload( Env_server['ip'], Env_server['user'], Env_server['passwd'],
              '%s/bin/deploy_config/authproxy/authproxy.xml' % Env_server['jboss_home'],
              './tmp/authproxy.xml',
              mode = 'ascii' )
    text='''<?xml version="1.0" encoding="gb2312"?>
<authproxy>
	<subsystem>
		<logout-url>http://10.12.12.157:48080/prm/logout.action</logout-url>
	</subsystem>
	
	<contextPath>
		<admin>admin</admin>
		<sp>partner</sp>
	</contextPath>
	
	<portal>
		<admin>
			<host>10.12.12.157</host>
			<port>38080</port>
			<url>/admin/userAuth.ajax</url>
			<out-host>10.0.0.1</out-host>
			<out-port>80</out-port>
			<index-url>/admin/portal/login.jsp</index-url>
		</admin>
		<sp>
			<host>10.12.12.157</host>
			<port>61080</port>
			<url>/partner/userAuth.ajax</url>
			<out-host>10.0.0.2</out-host>
			<out-port>81</out-port>
			<index-url>/partner/portal/login.jsp</index-url>
		</sp>		
	</portal>
	
	<sessionCallbackClass></sessionCallbackClass>
</authproxy>
    '''
    replaceFileText('./tmp/authproxy.xml', text)
    sftpupload( './tmp/authproxy.xml',
              Env_server['ip'], Env_server['user'], Env_server['passwd'],
              '%s/bin/deploy_config/authproxy/authproxy.xml' % Env_server['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/authproxy.xml' )

    # �޸�admin�����deploy_config\portal\portal.xml
    sftpdownload( Env_admin['ip'], Env_admin['user'], Env_admin['passwd'],
              '%s/bin/deploy_config/portal/portal.xml' % Env_admin['jboss_home'],
              './tmp/portal.xml',
              mode = 'ascii' )
    replaceFileStr( './tmp/portal.xml', '<biz-context>server</biz-context>', '<biz-context>prm</biz-context>' )
    replaceFileStr( './tmp/portal.xml', '<checkCode>true</checkCode>', '<checkCode>false</checkCode>' )  # ��֤��ȥ��
    replaceFileStr( './tmp/portal.xml', '<spUrl>http://10.12.12.184</spUrl>', '<spUrl>http://10.12.12.157</spUrl>' )
    replaceFileStr( './tmp/portal.xml', '<system-name>Portal</system-name>', '<system-name>�乾����������ƽ̨</system-name>' )
    sftpupload( './tmp/portal.xml',
              Env_admin['ip'], Env_admin['user'], Env_admin['passwd'],
              '%s/bin/deploy_config/portal/portal.xml' % Env_admin['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/portal.xml' )
    
    # �޸�partner�����deploy_config\portal\portal.xml
    sftpdownload( Env_partner['ip'], Env_partner['user'], Env_partner['passwd'],
              '%s/bin/deploy_config/portal/portal.xml' % Env_partner['jboss_home'],
              './tmp/portal.xml',
              mode = 'ascii' )
    replaceFileStr( './tmp/portal.xml', '<biz-context>server</biz-context>', '<biz-context>prm</biz-context>' )
    replaceFileStr( './tmp/portal.xml', '<checkCode>true</checkCode>', '<checkCode>false</checkCode>' )  # ��֤��ȥ��
    replaceFileStr( './tmp/portal.xml', '<spUrl>http://10.12.12.184</spUrl>', '<spUrl>http://10.12.12.157</spUrl>' )
    replaceFileStr( './tmp/portal.xml', '<system-name>Portal</system-name>', '<system-name>�乾����������ƽ̨</system-name>' )
    sftpupload( './tmp/portal.xml',
              Env_partner['ip'], Env_partner['user'], Env_partner['passwd'],
              '%s/bin/deploy_config/portal/portal.xml' % Env_partner['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/portal.xml' )
     
    # �޸�server�����deploy_config/email/email.xml
    sftpdownload( Env_server['ip'], Env_server['user'], Env_server['passwd'],
              '%s/bin/deploy_config/email/email.xml' % Env_server['jboss_home'],
              './tmp/email.xml',
              mode = 'ascii' )
    replaceFileStr( './tmp/email.xml', '<default-from>simstestmail@aspire-tech.com</default-from>', '<default-from>sims_test@gc0077.aspire.aspire-tech.com</default-from>')
    replaceFileStr( './tmp/email.xml', '<host-name>mail.aspire-tech.com</host-name>', '<host-name>10.12.7.131</host-name>')
    replaceFileStr( './tmp/email.xml', '<user-name>userName</user-name>', '<user-name>sims_test</user-name>')
    replaceFileStr( './tmp/email.xml', '<password>password</password>', '<password>sims_test</password>')
    replaceFileStr( './tmp/email.xml', '<mode>dev</mode>', '<mode>product</mode>')
    replaceFileStr( './tmp/email.xml', '<email>simstestmail@aspire-tech.com</email>', '<email>2605661371@qq.com</email>')
    replaceFileStr( './tmp/email.xml', '<email>simstestmail2@aspire-tech.com</email>', '<email>penghengkang@10.12.7.131</email>')
    sftpupload( './tmp/email.xml',
              Env_server['ip'], Env_server['user'], Env_server['passwd'],
              '%s/bin/deploy_config/email/email.xml' % Env_server['jboss_home'],
              mode = 'ascii' )
    os.remove('./tmp/email.xml')
    
    # �޸�admin�����deploy_config/email/email.xml
    sftpdownload( Env_admin['ip'], Env_admin['user'], Env_admin['passwd'],
              '%s/bin/deploy_config/email/email.xml' % Env_admin['jboss_home'],
              './tmp/email.xml',
              mode = 'ascii' )
    replaceFileStr( './tmp/email.xml', '<default-from>simstestmail@aspire-tech.com</default-from>', '<default-from>sims_test@gc0077.aspire.aspire-tech.com</default-from>')
    replaceFileStr( './tmp/email.xml', '<host-name>mail.aspire-tech.com</host-name>', '<host-name>10.12.7.131</host-name>')
    replaceFileStr( './tmp/email.xml', '<user-name>userName</user-name>', '<user-name>sims_test</user-name>')
    replaceFileStr( './tmp/email.xml', '<password>password</password>', '<password>sims_test</password>')
    replaceFileStr( './tmp/email.xml', '<mode>dev</mode>', '<mode>product</mode>')
    replaceFileStr( './tmp/email.xml', '<email>simstestmail@aspire-tech.com</email>', '<email>2605661371@qq.com</email>')
    replaceFileStr( './tmp/email.xml', '<email>simstestmail2@aspire-tech.com</email>', '<email>penghengkang@10.12.7.131</email>')
    sftpupload( './tmp/email.xml',
              Env_admin['ip'], Env_admin['user'], Env_admin['passwd'],
              '%s/bin/deploy_config/email/email.xml' % Env_admin['jboss_home'],
              mode = 'ascii' )
    os.remove('./tmp/email.xml')

    # �޸�partner�����deploy_config/email/email.xml
    sftpdownload( Env_partner['ip'], Env_partner['user'], Env_partner['passwd'],
              '%s/bin/deploy_config/email/email.xml' % Env_partner['jboss_home'],
              './tmp/email.xml',
              mode = 'ascii' )
    replaceFileStr( './tmp/email.xml', '<default-from>simstestmail@aspire-tech.com</default-from>', '<default-from>sims_test@gc0077.aspire.aspire-tech.com</default-from>')
    replaceFileStr( './tmp/email.xml', '<host-name>mail.aspire-tech.com</host-name>', '<host-name>10.12.7.131</host-name>')
    replaceFileStr( './tmp/email.xml', '<user-name>userName</user-name>', '<user-name>sims_test</user-name>')
    replaceFileStr( './tmp/email.xml', '<password>password</password>', '<password>sims_test</password>')
    replaceFileStr( './tmp/email.xml', '<mode>dev</mode>', '<mode>product</mode>')
    replaceFileStr( './tmp/email.xml', '<email>simstestmail@aspire-tech.com</email>', '<email>2605661371@qq.com</email>')
    replaceFileStr( './tmp/email.xml', '<email>simstestmail2@aspire-tech.com</email>', '<email>penghengkang@10.12.7.131</email>')
    sftpupload( './tmp/email.xml',
              Env_partner['ip'], Env_partner['user'], Env_partner['passwd'],
              '%s/bin/deploy_config/email/email.xml' % Env_partner['jboss_home'],
              mode = 'ascii' )
    os.remove('./tmp/email.xml')
    
    # �޸�server�����deploy_config/iodf/iodf.properties
    sftpdownload( Env_server['ip'], Env_server['user'], Env_server['passwd'],
              '%s/bin/deploy_config/iodf/iodf.properties' % Env_server['jboss_home'],
              './tmp/iodf.properties',
              mode = 'ascii' )
    setKeyValue( './tmp/iodf.properties', 'SYNC_NOTIFY_RECIEVE_INTERFACE_URL', 'http://%s:%s/iodd/syncMessageNotifierServlet' % ( Env_iodd['ip'], Env_iodd['port'] ) )
    sftpupload( './tmp/iodf.properties',
              Env_server['ip'], Env_server['user'], Env_server['passwd'],
              '%s/bin/deploy_config/iodf/iodf.properties' % Env_server['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/iodf.properties' )

    #�޸�server�����memcachedclient.properties
    sftpdownload( Env_server['ip'], Env_server['user'], Env_server['passwd'],
              '%s/bin/deploy_config/memcachedclient/memcachedclient.properties' % Env_server['jboss_home'],
              './tmp/memcachedclient.properties',
              mode = 'ascii' )
    setKeyValue( './tmp/memcachedclient.properties', 'schooner.memcached.servers', '10.12.12.157\:12000' )
    setKeyValue( './tmp/memcachedclient.properties', 'x.memcached.servers', '10.12.12.157\:11211' )
    sftpupload( './tmp/memcachedclient.properties',
              Env_server['ip'], Env_server['user'], Env_server['passwd'],
              '%s/bin/deploy_config/memcachedclient/memcachedclient.properties' % Env_server['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/memcachedclient.properties' )
    
    #�޸�admin�����memcachedclient.properties
    sftpdownload( Env_admin['ip'], Env_admin['user'], Env_admin['passwd'],
              '%s/bin/deploy_config/memcachedclient/memcachedclient.properties' % Env_admin['jboss_home'],
              './tmp/memcachedclient.properties',
              mode = 'ascii' )
    setKeyValue( './tmp/memcachedclient.properties', 'schooner.memcached.servers', '10.12.12.157\:12000' )
    setKeyValue( './tmp/memcachedclient.properties', 'x.memcached.servers', '10.12.12.157\:11211' )
    sftpupload( './tmp/memcachedclient.properties',
              Env_admin['ip'], Env_admin['user'], Env_admin['passwd'],
              '%s/bin/deploy_config/memcachedclient/memcachedclient.properties' % Env_admin['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/memcachedclient.properties' )
    
    #�޸�partner�����memcachedclient.properties
    sftpdownload( Env_partner['ip'], Env_partner['user'], Env_partner['passwd'],
              '%s/bin/deploy_config/memcachedclient/memcachedclient.properties' % Env_partner['jboss_home'],
              './tmp/memcachedclient.properties',
              mode = 'ascii' )
    setKeyValue( './tmp/memcachedclient.properties', 'schooner.memcached.servers', '10.12.12.157\:12000' )
    setKeyValue( './tmp/memcachedclient.properties', 'x.memcached.servers', '10.12.12.157\:11211' )
    sftpupload( './tmp/memcachedclient.properties',
              Env_partner['ip'], Env_partner['user'], Env_partner['passwd'],
              '%s/bin/deploy_config/memcachedclient/memcachedclient.properties' % Env_partner['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/memcachedclient.properties' )
    
    #���ͨ��python�ű��ϴ��������ļ�����ȷ������
    #��/opt/aspire/product/miguauto/bak/settlement�����XmlHttpConfig.xml�ļ����ǵ�iodd�����XmlHttpConfig.xml
    RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
           'cp ~/bak/settlement/* ~/jboss_server/bin/config/settlement/excel/export/')
    
    return

def modifyRemoteIoddConf():
    # iodf.properties���޸�SIMS������Ϣ�ĵ�ַΪģ�����ĵ�ַ
    sftpdownload( Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'],
              '%s/bin/deploy_config/iodf/iodf.properties' % Env_iodd['jboss_home'],
              './tmp/iodf.properties',
              mode = 'ascii' )
              
    setKeyValue( './tmp/iodf.properties', 'SIMS_RECIEVE_INTERFACE_URL', 'http://10.12.12.247:9051')
    sftpupload( './tmp/iodf.properties',
              Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'],
              '%s/bin/deploy_config/iodf/iodf.properties' % Env_iodd['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/iodf.properties' )
    
    #�޸�iodd�����deploy_config\iodd\adapter\xmlhttp\XmlHttpConfig.xml
    sftpdownload( Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'],
              '%s/bin/deploy_config/iodd/adapter/xmlhttp/XmlHttpConfig.xml' % Env_iodd['jboss_home'],
              './tmp/XmlHttpConfig.xml',
              mode = 'ascii' )
    text='''<?xml version="1.0"?>
<XmlHttpConfig>
	<nodes>
		<!-- id:��Ԫ��ţ�name����Ԫ���ƣ�messageType:���״���,serverUrl�����񴮣�clientSecretKey����Ϊ��Ϣ���𷽵������֤��Կkey��serverSecretKey����Ϊ��Ϣ���շ��������֤��Կkey-->
		<node type="prm" id="2001" messageType="110001" name="ͬ��������Ϣ" serverUrl="http://10.12.3.24:8280/iodd/miguprmXmlHttp" clientSecretKey="2222" serverSecretKey="2222"/>
		<node type="prm" id="2001" messageType="110002" name="ͬ����ͬ��Ϣ" serverUrl="http://10.12.3.24:8280/iodd/miguprmXmlHttp" clientSecretKey="2222" serverSecretKey="2222"/>
		<node type="prm" id="2001" messageType="220001" name="���������Ϣ" serverUrl="" clientSecretKey="2222" serverSecretKey="2222"/>
		<node type="sims" id="888" messageType="020007" name="���빫˾����" serverUrl="" clientSecretKey="QUERY_COMPANYCODE_SECRETKEY" serverSecretKey="QUERY_COMPANYCODE_SECRETKEY"/>
		<node type="sims" id="888" messageType="020009" name="��������ʱ���" serverUrl="" clientSecretKey="QUERY_COMPANYCODE_SECRETKEY" serverSecretKey="QUERY_COMPANYCODE_SECRETKEY"/>
		<node type="base" id="999" messageType="010002" name="��˾��Ϣͬ��sims" serverUrl="http://10.1.3.34:7092/iodd/miguMsgReceiveServlet"  clientSecretKey="QUERY_COMPANYCODE_SECRETKEY" serverSecretKey="QUERY_COMPANYCODE_SECRETKEY"/>
		<node type="base" id="02101" messageType="330002" name="�ӹ�˾ȷ����Ϣ" serverUrl="" clientSecretKey="2222" serverSecretKey="2222"/>
                <node type="base" id="05101" messageType="330002" name="�ӹ�˾ȷ����Ϣ" serverUrl="" clientSecretKey="2222" serverSecretKey="2222"/>
                <node type="base" id="03801" messageType="330002" name="�ӹ�˾ȷ����Ϣ" serverUrl="" clientSecretKey="2222" serverSecretKey="2222"/>                         
	        <node type="base" id="04101" messageType="330002" name="�ӹ�˾ȷ����Ϣ" serverUrl="" clientSecretKey="2222" serverSecretKey="2222"/> 
                <node type="base" id="06101" messageType="330002" name="�ӹ�˾ȷ����Ϣ" serverUrl="" clientSecretKey="2222" serverSecretKey="2222"/> 
                <node type="base" id="02101" messageType="220001" name="����CMS" serverUrl="http://1www.baidu1.com" clientSecretKey="2222" serverSecretKey="2222"/>
                <node type="base" id="02101" messageType="330001" name="����CMS" serverUrl="http://1www.baidu2.com" clientSecretKey="2222" serverSecretKey="2222"/>
                <node type="base" id="06101" messageType="220001" name="video cp" serverUrl="http://1www.baidu3.com" clientSecretKey="2222" serverSecretKey="2222"/>
                <node type="base" id="06101" messageType="330001" name="video cp" serverUrl="http://1www.baidu4.com" clientSecretKey="2222" serverSecretKey="2222"/>

	</nodes>
</XmlHttpConfig>
    '''
    replaceFileText('./tmp/XmlHttpConfig.xml', text)
    sftpupload( './tmp/XmlHttpConfig.xml',
              Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'],
              '%s/bin/deploy_config/iodd/adapter/xmlhttp/XmlHttpConfig.xml' % Env_iodd['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/XmlHttpConfig.xml' )
    
    #���ͨ��python�ű��ϴ��������ļ�����ȷ������
    #��/opt/aspire/product/miguauto/bak/iodd�����XmlHttpConfig.xml�ļ����ǵ�iodd�����XmlHttpConfig.xml
    RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
           'cp ~/bak/iodd/XmlHttpConfig.xml ~/jboss_iodd/bin/deploy_config/iodd/adapter/xmlhttp/')
    
    return
    
def modifyWebbasConf():
    '''�޸�webbas2.0�������ļ�'''
    #jdbc.properties����Ӧʵ�����ݿ�������Ϣ
    sftpdownload( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
              '%s/tomcat-authmgt/bin/config/jdbc.properties' % Env_miguauto['jboss_home'],
              './tmp/jdbc.properties',
              mode = 'ascii' )        
    setKeyValue( './tmp/jdbc.properties', 'jdbc.url', 'jdbc:oracle:thin:@%s:1521:%s' % ( Env_oracle['ip'], Env_oracle['sid'] ))
    setKeyValue( './tmp/jdbc.properties', 'jdbc.username', 'migu_auto')
    setKeyValue( './tmp/jdbc.properties', 'jdbc.password', 'migu_prm_auto')
    replaceFileStr( './tmp/jdbc.properties', '^M', '' )
    sftpupload( './tmp/jdbc.properties',
              Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
              '%s/tomcat-authmgt/bin/config/jdbc.properties' % Env_miguauto['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/jdbc.properties' )
    
    #�޸�portalclient.xml
    sftpdownload( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
              '%s/tomcat-authmgt/bin/config/portalclient.xml' % Env_miguauto['jboss_home'],
              './tmp/portalclient.xml',
              mode = 'ascii' )        
    replaceFileStr( './tmp/portalclient.xml', '<logout-url>http://localhost:8080/webbas/logout.biz</logout-url>', '<logout-url>http://10.12.12.157:38181/webbas/logout.biz</logout-url>' )
    replaceFileStr( './tmp/portalclient.xml', '<domain>http://localhost:8080/admin</domain>', '<domain>http://10.12.12.157:18092/admin</domain>' )
    replaceFileStr( './tmp/portalclient.xml', '<out-domain>http://localhost:8080/admin</out-domain>', '<out-domain>http://10.12.12.157:18092/admin</out-domain>' )
    replaceFileStr( './tmp/portalclient.xml', '^M', '' )
    sftpupload( './tmp/portalclient.xml',
              Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
              '%s/tomcat-authmgt/bin/config/portalclient.xml' % Env_miguauto['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/portalclient.xml' )
    
    return

def modify_jquery_biz_in_war( warfile, jquery_biz_file = 'jquery/plugin/custom/jquery.biz-1.0.js' ):
    '''��������jquery��Plupload��������ϴ���Ϊ�˷���ʹ��input[type=file]ģʽ��������Ҫ�޸�����ʱ����
       ��ǰȱʡ��������war����jquery/plugin/custom/jquery.biz-1.0.js�ļ���
       ��Ҫ��runtimes: 'gears,html5,flash,silverlight,html4' ��Ϊruntimes: 'html5,html4,gears,flash,silverlight'
       '''
    os.system( 'jar xf %s %s' % ( warfile, jquery_biz_file ) )
    file_content = open( jquery_biz_file, 'r+' ).read()
    file_content = file_content.replace( 'gears,html5,flash,silverlight,html4', 'html5,html4,gears,flash,silverlight' )
    open( jquery_biz_file, 'w+' ).write( file_content )
    os.system( 'jar uf %s %s' % ( warfile, jquery_biz_file ) )
   
def test():
    rebuildDb()

