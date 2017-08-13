# -*- coding:cp936 -*-
from migu_utils import *
import os
import shutil
import zipfile
import time
from migu_deploy import *

def getLastbuildFile():
    '''获取最新的build，copy到当前目录下的tmp目录'''
    if os.path.exists( 'tmp\\migu\\%s\\' % migu_build_str ) == False:
        logger.info( '获取migu的最新版本: %s' % migu_build_str )
        CleanDir( './tmp/migu' )
        os.system( 'xcopy /E /R /Y %s tmp\\migu\\%s\\' % ( migu_build_folder, migu_build_str ) )

def sftpuploadfolder( localdir, ip, user, passwd, remotepdir ):
    '''将本机上的目录打包,ftp放远程服务器上，再解包'''
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
    mydbscript_sqlfilelist = [ '01migu_init_system_admin.sql',
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
    '''
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
    '''
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

def modifyRemoteMiguConf():
    #修改server下面的attachment.properties
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
    
    #修改server deploy_config/settlement下面的attachment.properties,MIGU1.0.2.0新增
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
    
    #修改admin下面的attachment.properties
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
    
    #修改partner下面的attachment.properties
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

    #修改server下面的deploy_config\authproxy\authproxy.xml
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

    # 修改admin下面的deploy_config\portal\portal.xml
    sftpdownload( Env_admin['ip'], Env_admin['user'], Env_admin['passwd'],
              '%s/bin/deploy_config/portal/portal.xml' % Env_admin['jboss_home'],
              './tmp/portal.xml',
              mode = 'ascii' )
    replaceFileStr( './tmp/portal.xml', '<biz-context>server</biz-context>', '<biz-context>prm</biz-context>' )
    replaceFileStr( './tmp/portal.xml', '<checkCode>true</checkCode>', '<checkCode>false</checkCode>' )  # 验证码去除
    replaceFileStr( './tmp/portal.xml', '<spUrl>http://10.12.12.184</spUrl>', '<spUrl>http://10.12.12.157</spUrl>' )
    replaceFileStr( './tmp/portal.xml', '<system-name>Portal</system-name>', '<system-name>咪咕合作伙伴接入平台</system-name>' )
    sftpupload( './tmp/portal.xml',
              Env_admin['ip'], Env_admin['user'], Env_admin['passwd'],
              '%s/bin/deploy_config/portal/portal.xml' % Env_admin['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/portal.xml' )
    
    # 修改partner下面的deploy_config\portal\portal.xml
    sftpdownload( Env_partner['ip'], Env_partner['user'], Env_partner['passwd'],
              '%s/bin/deploy_config/portal/portal.xml' % Env_partner['jboss_home'],
              './tmp/portal.xml',
              mode = 'ascii' )
    replaceFileStr( './tmp/portal.xml', '<biz-context>server</biz-context>', '<biz-context>prm</biz-context>' )
    replaceFileStr( './tmp/portal.xml', '<checkCode>true</checkCode>', '<checkCode>false</checkCode>' )  # 验证码去除
    replaceFileStr( './tmp/portal.xml', '<spUrl>http://10.12.12.184</spUrl>', '<spUrl>http://10.12.12.157</spUrl>' )
    replaceFileStr( './tmp/portal.xml', '<system-name>Portal</system-name>', '<system-name>咪咕合作伙伴接入平台</system-name>' )
    sftpupload( './tmp/portal.xml',
              Env_partner['ip'], Env_partner['user'], Env_partner['passwd'],
              '%s/bin/deploy_config/portal/portal.xml' % Env_partner['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/portal.xml' )
     
    # 修改server下面的deploy_config/email/email.xml
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
    
    # 修改admin下面的deploy_config/email/email.xml
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

    # 修改partner下面的deploy_config/email/email.xml
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
    
    # 修改server下面的deploy_config/iodf/iodf.properties
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

    #修改server下面的memcachedclient.properties
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
    
    #修改admin下面的memcachedclient.properties
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
    
    #修改partner下面的memcachedclient.properties
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
    
    #解决通过python脚本上传的配置文件不正确的问题
    #把/opt/aspire/product/miguauto/bak/settlement下面的XmlHttpConfig.xml文件覆盖掉iodd下面的XmlHttpConfig.xml
    RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
           'cp ~/bak/settlement/* ~/jboss_server/bin/config/settlement/excel/export/')
    
    return

def modifyRemoteIoddConf():
    # iodf.properties，修改SIMS接收消息的地址为模拟器的地址
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
    
    #修改iodd下面的deploy_config\iodd\adapter\xmlhttp\XmlHttpConfig.xml
    sftpdownload( Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'],
              '%s/bin/deploy_config/iodd/adapter/xmlhttp/XmlHttpConfig.xml' % Env_iodd['jboss_home'],
              './tmp/XmlHttpConfig.xml',
              mode = 'ascii' )
    text='''<?xml version="1.0"?>
<XmlHttpConfig>
	<nodes>
		<!-- id:网元编号，name：网元名称，messageType:交易代码,serverUrl：服务串，clientSecretKey：作为消息发起方的身份认证密钥key，serverSecretKey：作为消息接收方的身份认证密钥key-->
		<node type="prm" id="2001" messageType="110001" name="同步合作信息" serverUrl="http://10.12.3.24:8280/iodd/miguprmXmlHttp" clientSecretKey="2222" serverSecretKey="2222"/>
		<node type="prm" id="2001" messageType="110002" name="同步合同信息" serverUrl="http://10.12.3.24:8280/iodd/miguprmXmlHttp" clientSecretKey="2222" serverSecretKey="2222"/>
		<node type="prm" id="2001" messageType="220001" name="结果反馈信息" serverUrl="" clientSecretKey="2222" serverSecretKey="2222"/>
		<node type="sims" id="888" messageType="020007" name="申请公司编码" serverUrl="" clientSecretKey="QUERY_COMPANYCODE_SECRETKEY" serverSecretKey="QUERY_COMPANYCODE_SECRETKEY"/>
		<node type="sims" id="888" messageType="020009" name="申请商用时间戳" serverUrl="" clientSecretKey="QUERY_COMPANYCODE_SECRETKEY" serverSecretKey="QUERY_COMPANYCODE_SECRETKEY"/>
		<node type="base" id="999" messageType="010002" name="公司信息同步sims" serverUrl="http://10.1.3.34:7092/iodd/miguMsgReceiveServlet"  clientSecretKey="QUERY_COMPANYCODE_SECRETKEY" serverSecretKey="QUERY_COMPANYCODE_SECRETKEY"/>
		<node type="base" id="02101" messageType="330002" name="子公司确认消息" serverUrl="" clientSecretKey="2222" serverSecretKey="2222"/>
                <node type="base" id="05101" messageType="330002" name="子公司确认消息" serverUrl="" clientSecretKey="2222" serverSecretKey="2222"/>
                <node type="base" id="03801" messageType="330002" name="子公司确认消息" serverUrl="" clientSecretKey="2222" serverSecretKey="2222"/>                         
	        <node type="base" id="04101" messageType="330002" name="子公司确认消息" serverUrl="" clientSecretKey="2222" serverSecretKey="2222"/> 
                <node type="base" id="06101" messageType="330002" name="子公司确认消息" serverUrl="" clientSecretKey="2222" serverSecretKey="2222"/> 
                <node type="base" id="02101" messageType="220001" name="音乐CMS" serverUrl="http://1www.baidu1.com" clientSecretKey="2222" serverSecretKey="2222"/>
                <node type="base" id="02101" messageType="330001" name="音乐CMS" serverUrl="http://1www.baidu2.com" clientSecretKey="2222" serverSecretKey="2222"/>
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
    
    #解决通过python脚本上传的配置文件不正确的问题
    #把/opt/aspire/product/miguauto/bak/iodd下面的XmlHttpConfig.xml文件覆盖掉iodd下面的XmlHttpConfig.xml
    RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
           'cp ~/bak/iodd/XmlHttpConfig.xml ~/jboss_iodd/bin/deploy_config/iodd/adapter/xmlhttp/')
    
    return
    
def modifyWebbasConf():
    '''修改webbas2.0的配置文件'''
    #jdbc.properties，对应实际数据库连接信息
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
    
    #修改portalclient.xml
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
    '''由于引入jquery的Plupload插件用于上传，为了方便使用input[type=file]模式，所以需要修改运行时设置
       当前缺省的配置在war包的jquery/plugin/custom/jquery.biz-1.0.js文件中
       需要把runtimes: 'gears,html5,flash,silverlight,html4' 改为runtimes: 'html5,html4,gears,flash,silverlight'
       '''
    os.system( 'jar xf %s %s' % ( warfile, jquery_biz_file ) )
    file_content = open( jquery_biz_file, 'r+' ).read()
    file_content = file_content.replace( 'gears,html5,flash,silverlight,html4', 'html5,html4,gears,flash,silverlight' )
    open( jquery_biz_file, 'w+' ).write( file_content )
    os.system( 'jar uf %s %s' % ( warfile, jquery_biz_file ) )
   
def test():
    rebuildDb()

