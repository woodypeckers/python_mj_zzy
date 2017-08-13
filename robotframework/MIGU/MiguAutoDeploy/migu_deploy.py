# -*- coding:cp936 -*-
from migu_biz import *
from migu_utils import *

SSH_flag = 1

# buildĿ¼����Ҫ���ģ�һ����ʼ��л�ȡ
migu_build_folder = r'\\ASP-BLD-SERV100\release_bldstg\MIGU_PRM\MIGU_PRM1.0.2.0\MIGU_PRM1.0.2.0_SSYT_11__20151216_16.30.54'

# ���������һ��ֻ����һ��
Env_oracle = {'name':'db', 'type':'oracle', 'ip':'10.12.3.197', 'port':'1521', 'user':'migu_auto', 'passwd':'migu_prm_auto', 'tnsname':'10.12.3.197', 'sid':'ora11g'}
Env_server = {'name':'miguserver', 'type':'jboss', 'ip':'10.12.12.157', 'port':'48080', 'user':'miguauto', 'passwd':'miguauto', 'jboss_home':'/opt/aspire/product/miguauto/jboss_server'}
Env_iodd = {'name':'miguiodd', 'type':'jboss', 'ip':'10.12.12.157', 'port':'58080', 'user':'miguauto', 'passwd':'miguauto', 'jboss_home':'/opt/aspire/product/miguauto/jboss_iodd', 'sims_inf_url':'http://10.12.12.157:9001'}
Env_admin = {'name':'miguadmin', 'type':'jboss', 'ip':'10.12.12.157', 'port':'38080', 'user':'miguauto', 'passwd':'miguauto', 'jboss_home':'/opt/aspire/product/miguauto/jboss_admin', 'sims_inf_url':'http://10.12.12.157:9001'}
Env_partner = {'name':'migupartner', 'type':'jboss', 'ip':'10.12.12.157', 'port':'61080', 'user':'miguauto', 'passwd':'miguauto', 'jboss_home':'/opt/aspire/product/miguauto/jboss_partner', 'sims_inf_url':'http://10.12.12.157:9001'}
Env_miguauto = {'name':'miguauto', 'ip':'10.12.12.157', 'user':'miguauto', 'passwd':'miguauto', 'jboss_home':'/opt/aspire/product/miguauto'}

migu_build_str = migu_build_folder.split( '\\' )[-1]

def deploy_migu( rebuilddb = 1 ):
    '''����admin��partner����server��server��Ӧ��war����prm.war'''
    # ���޸�һ��war��
    script_dir = os.path.abspath( os.path.curdir )
    os.chdir( './tmp/migu/%s/Release' % migu_build_str )
    modify_jquery_biz_in_war( 'portal/partner.war' )
    modify_jquery_biz_in_war( 'portal/admin.war' )
    modify_jquery_biz_in_war( 'prm/prm.war' )
    os.chdir( script_dir )

    #ֹͣserver����
    RemoteCmd( Env_server['ip'], Env_server['user'], Env_server['passwd'],
           'cd %s/bin;sh stop.sh' % Env_server['jboss_home'] )
    #ֹͣadmin����
    RemoteCmd( Env_admin['ip'], Env_admin['user'], Env_admin['passwd'],
           'cd %s/bin;sh stop.sh' % Env_admin['jboss_home'] )
    #ֹͣpartner����
    RemoteCmd( Env_partner['ip'], Env_partner['user'], Env_partner['passwd'],
           'cd %s/bin;sh stop.sh' % Env_partner['jboss_home'] )   
           
    #ɾ��admin.war��partner.war��prm.war
    RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
           'cd ~/upload;rm admin.war;rm partner.war;rm prm.war' )
    
    #�ϴ�admin.war��partner.war��prm.war
    '''
    for li in ['portal/partner.war', 'portal/admin.war', 'prm/prm.war']:
        sftpupload( './tmp/migu/%s/Release/%s' % ( migu_build_str, li ),
                   Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
                   '%s/upload' % ( Env_miguauto['jboss_home']) )
    '''
	
    #�ϴ�admin.war
    sftpupload( './tmp/migu/%s/Release/portal/admin.war' % ( migu_build_str, ),
               Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
               '%s/upload/admin.war' % ( Env_miguauto['jboss_home'], ) )
    #�ϴ�partner.war
    sftpupload( './tmp/migu/%s/Release/portal/partner.war' % ( migu_build_str, ),
               Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
               '%s/upload/partner.war' % ( Env_miguauto['jboss_home'], ) )
    #�ϴ�server.war
    sftpupload( './tmp/migu/%s/Release/prm/prm.war' % ( migu_build_str, ),
               Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
               '%s/upload/prm.war' % ( Env_miguauto['jboss_home'], ) )
    
    #ɾ��admin�������ļ�
    RemoteCmd( Env_admin['ip'], Env_admin['user'], Env_admin['passwd'],
           'cd %s/bin;rm -Rf config;rm -Rf deploy_config' % Env_admin['jboss_home'] )
    #ɾ��partner�������ļ�
    RemoteCmd( Env_partner['ip'], Env_partner['user'], Env_partner['passwd'],
           'cd %s/bin;rm -Rf config;rm -Rf deploy_config' % Env_partner['jboss_home'] )
    #ɾ��server�������ļ�
    RemoteCmd( Env_server['ip'], Env_server['user'], Env_server['passwd'],
           'cd %s/bin;rm -Rf config;rm -Rf deploy_config' % Env_server['jboss_home'] )
    
    #�ϴ�admin�������ļ�
    sftpuploadfolder( './tmp/migu/%s/Release/portal/config' % migu_build_str,
                    Env_admin['ip'], Env_admin['user'], Env_admin['passwd'],
                    '%s/bin' % Env_admin['jboss_home'] )
    sftpuploadfolder( './tmp/migu/%s/Release/portal/deploy_config' % migu_build_str,
                    Env_admin['ip'], Env_admin['user'], Env_admin['passwd'],
                    '%s/bin' % Env_admin['jboss_home'] )                   
    #�ϴ�partner�������ļ�
    sftpuploadfolder( './tmp/migu/%s/Release/portal/config' % migu_build_str,
                    Env_partner['ip'], Env_partner['user'], Env_partner['passwd'],
                    '%s/bin' % Env_partner['jboss_home'] )
    sftpuploadfolder( './tmp/migu/%s/Release/portal/deploy_config' % migu_build_str,
                    Env_partner['ip'], Env_partner['user'], Env_partner['passwd'],
                    '%s/bin' % Env_partner['jboss_home'] )
    #�ϴ�server�������ļ�
    sftpuploadfolder( './tmp/migu/%s/Release/prm/config' % migu_build_str,
                    Env_server['ip'], Env_server['user'], Env_server['passwd'],
                    '%s/bin' % Env_server['jboss_home'] )
    sftpuploadfolder( './tmp/migu/%s/Release/prm/deploy_config' % migu_build_str,
                    Env_server['ip'], Env_server['user'], Env_server['passwd'],
                    '%s/bin' % Env_server['jboss_home'] )
    
    #�޸�admin��server��partner�������ļ�
    modifyRemoteMiguConf()
    
    #���²������ݿ�
    if rebuilddb == 1:
        rebuildDb()

    RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
           '. ~/.bash_profile; > ~/build.info; echo build=%s >> ~/build.info' % ( migu_build_str) )


def deploy_iodd():
    '''����iodd'''
    #ֹͣiodd����
    RemoteCmd( Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'],
           'cd %s/bin;sh stop.sh' % Env_iodd['jboss_home'] )
    
    #ɾ��iodd.war
    RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
       'cd ~/upload;rm iodd.war' )
    
    #�ϴ�iodd.war
    sftpupload( './tmp/migu/%s/Release/iodd/iodd.war' % ( migu_build_str, ),
               Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
               '%s/upload/iodd.war' % ( Env_miguauto['jboss_home'], ) )
    
    #ɾ��iodd�������ļ�
    RemoteCmd( Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'],
           'cd %s/bin;rm -Rf config;rm -Rf deploy_config' % Env_iodd['jboss_home'] )
    
    #�ϴ�iodd�������ļ�
    sftpuploadfolder( './tmp/migu/%s/Release/iodd/config' % migu_build_str,
                    Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'],
                    '%s/bin' % Env_iodd['jboss_home'] )
    sftpuploadfolder( './tmp/migu/%s/Release/iodd/deploy_config' % migu_build_str,
                    Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'],
                    '%s/bin' % Env_iodd['jboss_home'] )
    
    #�޸�iodd�������ļ�
    modifyRemoteIoddConf()

def deploy_webbas():
    '''����web_bas2.0'''
    #ֹͣwebbas2.0����
    RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
           'cd %s/tomcat-authmgt/bin;./stop.sh' % Env_miguauto['jboss_home'] )
           
    #ɾ��webbas.war
    RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
       'cd ~/tomcat-authmgt/webapps;rm webbas.war' )
    
    #�ϴ�webbas.war
    sftpupload( './tmp/migu/%s/Release/authmgt/webbas.war' % ( migu_build_str, ),
               Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
               '%s/tomcat-authmgt/webapps/webbas.war' % ( Env_miguauto['jboss_home'], ) )
    
    #ɾ��webbas2.0�������ļ�
    RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
           'cd %s/tomcat-authmgt/bin;rm -Rf config' % Env_miguauto['jboss_home'] )
    
    #�ϴ�webbas2.0�������ļ�
    sftpuploadfolder( './tmp/migu/%s/Release/authmgt/config' % migu_build_str,
                    Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
                    '%s/tomcat-authmgt/bin' % Env_miguauto['jboss_home'] )
                    
    #�޸�webbas2.0�������ļ�
    modifyWebbasConf()
    
def deploy( rebuilddb = 1 ):
    '''������߼�ִ��'''
    getLastbuildFile()
    deploy_migu( rebuilddb )
    deploy_iodd()
    deploy_webbas()
    startMigu()
    startIodd()
    startWebbas()



if __name__ == "__main__":
    deploy( rebuilddb = 1 )

