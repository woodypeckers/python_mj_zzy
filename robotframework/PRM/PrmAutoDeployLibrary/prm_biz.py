# -*- coding:cp936 -*-
from Utils import *
import os
import shutil
import zipfile
import time
from prm_deploy import *

def getLastbuildFile():
    '''��ȡ���µ�build��copy����ǰĿ¼�µ�tmpĿ¼'''
    if os.path.exists( 'tmp\\prm\\%s\\' % prm_build_str ) == False:
        logger.info( '��ȡprm�����°汾: %s' % prm_build_str )
        CleanDir( './tmp/prm' )
        os.system( 'xcopy /E /R /Y %s tmp\\prm\\%s\\' % ( prm_build_folder, prm_build_str ) )

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
    rtplt_dbscript_dir = os.path.join( script_dir, './tmp/prm/%s/Release/dbscript/rtplt' % prm_build_str )
    dbscript_dir = os.path.join( script_dir, './tmp/prm/%s/Release/dbscript' % prm_build_str )

    logger.info( 'ִ��Prm rtplt�����ݿ�ű�' )
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
                   ]

    for sqlfile in sqlfilelist:
        exec_sql( sqlfile, Env_oracle['user'], Env_oracle['passwd'], Env_oracle['tnsname'] )

    logger.info( 'ִ��Prm dbscript�����ݿ�ű�' )
    print dbscript_dir
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
                    'prm1.0.2.004/install.sql',
                    'prm1.0.2.005/install.sql',
                    'prm1.0.2.006/install.sql',
                    'prm1.0.2.007/install.sql'
                    ]
    for sqlfile in sqlfilelist:
        exec_sql( sqlfile, Env_oracle['user'], Env_oracle['passwd'], Env_oracle['tnsname'] )
    os.chdir( script_dir )
	
	

    importPrmMetadata()
   #os.chdir( script_dir )

    # ��ʼ������
    mydbscript_sqlfilelist = [ '01_init_system_admin.sql',
                              '02_init_system_sp.sql',
                              '03_init_private.sql',
                              '04_init_dbscipt.sql'
                              ]
    for sqlfile in mydbscript_sqlfilelist:
        logger.info( '���Ի�����ʼ�����ݣ�%s�ļ���Ҫ���' % sqlfile )
        os.system( 'sqlplus %s/%s@%s @./tmp/mydbscript/%s > ./tmp/%s.log' % ( Env_oracle['user'], Env_oracle['passwd'], Env_oracle['tnsname'] , sqlfile, sqlfile ) )
        logger.info( '���Ի�����ʼ������%s��ִ����־���£�\n%s' % ( sqlfile, open( './tmp/%s.log' % sqlfile, 'r+' ).read() ) )
    
	
    #ִ�ж��ں�������Ȩ��,��Ҫ��Ԫ����ִ������Ժ����ִ��
    os.chdir( dbscript_dir )
    afterMetadata_sqlfilelist=['prm1.0.1.0/installAfterMetadata.sql',
                               'prm1.0.2.004/installAfterMetadata.sql']
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

def importPrmMetadata():
    logger.info( 'PrmԪ���ݵ���,���޸�web_bas��jdbc.properties����ִ��metadata_import_common.cmd' )
    setKeyValue( './tmp/prm/%s/Release/tools/metadata/web_bas/tools/jdbc.properties' % prm_build_str, 'jdbc.url', 'jdbc:oracle:thin:@%s:1521:%s' % ( Env_oracle['ip'], Env_oracle['sid'] ) )
    setKeyValue( './tmp/prm/%s/Release/tools/metadata/web_bas/tools/jdbc.properties' % prm_build_str, 'jdbc.username', Env_oracle['user'] )
    setKeyValue( './tmp/prm/%s/Release/tools/metadata/web_bas/tools/jdbc.properties' % prm_build_str, 'jdbc.password', Env_oracle['passwd'] )
    script_dir = os.path.abspath( os.path.curdir )
    os.chdir( './tmp/prm/%s/Release/tools/metadata/web_bas/tools/' % prm_build_str )
    tmpstr = open( 'metadata_import_common.cmd', 'r+' ).read().replace( 'pause', '' )
    open( 'metadata_import_common.cmd', 'w+' ).write( tmpstr )
    os.system( 'metadata_import_common.cmd' )
    os.chdir( script_dir )
    logger.info( 'web_basԪ���ݵ���  ���' )

    logger.info( 'PrmԪ���ݵ���,���޸��Լ���jdbc.properties����ִ��metadata_import.cmd' )
    setKeyValue( './tmp/prm/%s/Release/tools/metadata/jdbc.properties' % prm_build_str, 'jdbc.url', 'jdbc:oracle:thin:@%s:1521:%s' % ( Env_oracle['ip'], Env_oracle['sid'] ) )
    setKeyValue( './tmp/prm/%s/Release/tools/metadata/jdbc.properties' % prm_build_str, 'jdbc.username', Env_oracle['user'] )
    setKeyValue( './tmp/prm/%s/Release/tools/metadata/jdbc.properties' % prm_build_str, 'jdbc.password', Env_oracle['passwd'] )
    os.chdir( './tmp/prm/%s/Release/tools/metadata' % prm_build_str )
    tmpstr = open( 'metadata_import.cmd', 'r+' ).read().replace( 'pause', '' )
    open( 'metadata_import.cmd', 'w+' ).write( tmpstr )
    os.system( 'metadata_import.cmd' )
    os.chdir( script_dir )
    logger.info( 'PrmԪ���ݵ���  ���' )


def stopPrm():
    stdstr = RemoteCmd( Env_prm['ip'], Env_prm['user'], Env_prm['passwd'], 'ps -ef|grep %s|grep java|grep -v grep' % Env_prm['user'], logflag = 0 )
    if stdstr.find( 'java' ) == -1:
        logger.info( 'stopPrm, ����δ��������shutdown' )
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

def startPrm():
    logger.info( 'startPrm' )
    RemoteCmd( Env_prm['ip'], Env_prm['user'], Env_prm['passwd'], 'cd %s/bin;nohup sh start.sh -Djboss.service.binding.set=ports-01 -b 0.0.0.0 > nohup.out &' % Env_prm['jboss_home'] )

def startIodd():
    logger.info( 'startIodd' )
    RemoteCmd( Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'], 'cd %s/bin;nohup sh start.sh -Djboss.service.binding.set=ports-01 -b 0.0.0.0 > nohup.out &' % Env_iodd['jboss_home'] )

def modifyRemotePrmConf():
    # attachment.properties
    sftpdownload( Env_prm['ip'], Env_prm['user'], Env_prm['passwd'],
              '%s/bin/deploy_config/attachment/attachment.properties' % Env_prm['jboss_home'],
              './tmp/attachment.properties',
              mode = 'ascii' )
    setKeyValue( './tmp/attachment.properties', 'SIMS_ID', '2001' )
    setKeyValue( './tmp/attachment.properties', 'FILE_TYPE', 'file' )
    setKeyValue( './tmp/attachment.properties', 'FILE_SERVER_IP', '10.12.12.157' )
    setKeyValue( './tmp/attachment.properties', 'FILE_SERVER_PORT', '21' )
    setKeyValue( './tmp/attachment.properties', 'USERNAME', 'prm' )
    setKeyValue( './tmp/attachment.properties', 'PASSWORD', 'prm' )
    setKeyValue( './tmp/attachment.properties', 'ABSOLUTE_UPLOAD_PATH', '/opt/aspire/product/prm/attachment' )
    setKeyValue( './tmp/attachment.properties', 'ABSOLUTE_SYNC_PATH', '/opt/aspire/product/prm/sync' )
    setKeyValue( './tmp/attachment.properties', 'LOCAL_ABSOLUTE_TEMP_PATH', '/opt/aspire/product/prm/temp' )
    sftpupload( './tmp/attachment.properties',
              Env_prm['ip'], Env_prm['user'], Env_prm['passwd'],
              '%s/bin/deploy_config/attachment/attachment.properties' % Env_prm['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/attachment.properties' )

    # �޸�deploy_config\authproxy\authproxy.xml
    sftpdownload( Env_prm['ip'], Env_prm['user'], Env_prm['passwd'],
              '%s/bin/deploy_config/authproxy/authproxy.xml' % Env_prm['jboss_home'],
              './tmp/authproxy.xml',
              mode = 'ascii' )
    replaceFileStr( './tmp/authproxy.xml', '127.0.0.1', '10.12.12.157' )
    replaceFileStr( './tmp/authproxy.xml', '8080', '18080' )
    replaceFileStr( './tmp/authproxy.xml', '/admin/userAuth.ajax', '/prm_admin/userAuth.ajax' )
    replaceFileStr( './tmp/authproxy.xml', '/admin/portal/login.jsp', '/prm_admin/portal/login.jsp' )
    replaceFileStr( './tmp/authproxy.xml', '/sp/userAuth.ajax', '/prm_sp/userAuth.ajax' )
    replaceFileStr( './tmp/authproxy.xml', '/sp/portal/login.jsp', '/prm_sp/portal/login.jsp' )
    replaceFileStr( './tmp/authproxy.xml', '/server/logout.action', '/server/logout.action' )
    replaceFileStr( './tmp/authproxy.xml', '<admin>admin</admin>', '<admin>prm_admin</admin>' )
    replaceFileStr( './tmp/authproxy.xml', '<sp>sp</sp>', '<sp>prm_sp</sp>' )


    sftpupload( './tmp/authproxy.xml',
              Env_prm['ip'], Env_prm['user'], Env_prm['passwd'],
              '%s/bin/deploy_config/authproxy/authproxy.xml' % Env_prm['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/authproxy.xml' )

    # �޸�deploy_config\portal\portal.xml
    sftpdownload( Env_prm['ip'], Env_prm['user'], Env_prm['passwd'],
              '%s/bin/deploy_config/portal/portal.xml' % Env_prm['jboss_home'],
              './tmp/portal.xml',
              mode = 'ascii' )
    biz_str = '''<biz-context>server</biz-context>
    <prm_admin-domain>
         <name>admin</name>
    </prm_admin-domain>
    <prm_sp-domain>
         <name>sp</name>
    </prm_sp-domain>'''
    replaceFileStr( './tmp/portal.xml', '<biz-context>server</biz-context>', biz_str )
    replaceFileStr( './tmp/portal.xml', '<checkCode>true</checkCode>', '<checkCode>false</checkCode>' )  # ��֤��ȥ��
    sftpupload( './tmp/portal.xml',
              Env_prm['ip'], Env_prm['user'], Env_prm['passwd'],
              '%s/bin/deploy_config/portal/portal.xml' % Env_prm['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/portal.xml' )
    # �޸�deploy_config/email/email.xml
    sftpdownload( Env_prm['ip'], Env_prm['user'], Env_prm['passwd'],
              '%s/bin/deploy_config/email/email.xml' % Env_prm['jboss_home'],
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
              Env_prm['ip'], Env_prm['user'], Env_prm['passwd'],
              '%s/bin/deploy_config/email/email.xml' % Env_prm['jboss_home'],
              mode = 'ascii' )
    os.remove('./tmp/email.xml')

    
    # iodf.properties
    sftpdownload( Env_prm['ip'], Env_prm['user'], Env_prm['passwd'],
              '%s/bin/deploy_config/iodf/iodf.properties' % Env_prm['jboss_home'],
              './tmp/iodf.properties',
              mode = 'ascii' )
    setKeyValue( './tmp/iodf.properties', 'SYNC_NOTIFY_RECIEVE_INTERFACE_URL', 'http://%s:%s/iodd/syncMessageNotifierServlet' % ( Env_iodd['ip'], Env_iodd['port'] ) )
    sftpupload( './tmp/iodf.properties',
              Env_prm['ip'], Env_prm['user'], Env_prm['passwd'],
              '%s/bin/deploy_config/iodf/iodf.properties' % Env_prm['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/iodf.properties' )

    return

def modifyRemoteIoddConf():
    # iodf.properties���޸�SIMS��MM����Ϸ����PRM��Ϣ�ĵ�ַΪģ�����ĵ�ַ
    sftpdownload( Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'],
              '%s/bin/deploy_config/iodf/iodf.properties' % Env_iodd['jboss_home'],
              './tmp/iodf.properties',
              mode = 'ascii' )
              
    setKeyValue( './tmp/iodf.properties', 'SIMS_RECIEVE_INTERFACE_URL', 'http://10.12.12.247:9001')
    setKeyValue( './tmp/iodf.properties', 'MM_RECIEVE_INTERFACE_URL', 'http://10.12.12.247:9004')
    setKeyValue( './tmp/iodf.properties', 'GAME_RECIEVE_INTERFACE_URL', 'http://10.12.12.247:9005')
    setKeyValue( './tmp/iodf.properties', 'GAME_RETRACT_INTERFACE_URL', 'http://10.12.12.247:9005')
    setKeyValue( './tmp/iodf.properties', 'MM_RETRACT_INTERFACE_URL', 'http://10.12.12.247:9004')
    sftpupload( './tmp/iodf.properties',
              Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'],
              '%s/bin/deploy_config/iodf/iodf.properties' % Env_iodd['jboss_home'],
              mode = 'ascii' )
    os.remove( './tmp/iodf.properties' )
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

if __name__ == "__main__":
    test()

