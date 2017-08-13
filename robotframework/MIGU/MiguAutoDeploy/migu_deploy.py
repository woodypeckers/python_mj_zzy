# -*- coding:cp936 -*-
from migu_biz import *
from migu_utils import *

SSH_flag = 1

# build目录，需要常改，一般从邮件中获取
migu_build_folder = r'\\ASP-BLD-SERV100\release_bldstg\MIGU_PRM\MIGU_PRM1.0.2.0\MIGU_PRM1.0.2.0_SSYT_11__20151216_16.30.54'

# 环境情况，一般只用配一次
Env_oracle = {'name':'db', 'type':'oracle', 'ip':'10.12.3.197', 'port':'1521', 'user':'migu_auto', 'passwd':'migu_prm_auto', 'tnsname':'10.12.3.197', 'sid':'ora11g'}
Env_server = {'name':'miguserver', 'type':'jboss', 'ip':'10.12.12.157', 'port':'48080', 'user':'miguauto', 'passwd':'miguauto', 'jboss_home':'/opt/aspire/product/miguauto/jboss_server'}
Env_iodd = {'name':'miguiodd', 'type':'jboss', 'ip':'10.12.12.157', 'port':'58080', 'user':'miguauto', 'passwd':'miguauto', 'jboss_home':'/opt/aspire/product/miguauto/jboss_iodd', 'sims_inf_url':'http://10.12.12.157:9001'}
Env_admin = {'name':'miguadmin', 'type':'jboss', 'ip':'10.12.12.157', 'port':'38080', 'user':'miguauto', 'passwd':'miguauto', 'jboss_home':'/opt/aspire/product/miguauto/jboss_admin', 'sims_inf_url':'http://10.12.12.157:9001'}
Env_partner = {'name':'migupartner', 'type':'jboss', 'ip':'10.12.12.157', 'port':'61080', 'user':'miguauto', 'passwd':'miguauto', 'jboss_home':'/opt/aspire/product/miguauto/jboss_partner', 'sims_inf_url':'http://10.12.12.157:9001'}
Env_miguauto = {'name':'miguauto', 'ip':'10.12.12.157', 'user':'miguauto', 'passwd':'miguauto', 'jboss_home':'/opt/aspire/product/miguauto'}

migu_build_str = migu_build_folder.split( '\\' )[-1]

def deploy_migu( rebuilddb = 1 ):
    '''部署admin、partner、和server，server对应的war包是prm.war'''
    # 先修改一下war包
    script_dir = os.path.abspath( os.path.curdir )
    os.chdir( './tmp/migu/%s/Release' % migu_build_str )
    modify_jquery_biz_in_war( 'portal/partner.war' )
    modify_jquery_biz_in_war( 'portal/admin.war' )
    modify_jquery_biz_in_war( 'prm/prm.war' )
    os.chdir( script_dir )

    #停止server服务
    RemoteCmd( Env_server['ip'], Env_server['user'], Env_server['passwd'],
           'cd %s/bin;sh stop.sh' % Env_server['jboss_home'] )
    #停止admin服务
    RemoteCmd( Env_admin['ip'], Env_admin['user'], Env_admin['passwd'],
           'cd %s/bin;sh stop.sh' % Env_admin['jboss_home'] )
    #停止partner服务
    RemoteCmd( Env_partner['ip'], Env_partner['user'], Env_partner['passwd'],
           'cd %s/bin;sh stop.sh' % Env_partner['jboss_home'] )   
           
    #删除admin.war、partner.war、prm.war
    RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
           'cd ~/upload;rm admin.war;rm partner.war;rm prm.war' )
    
    #上传admin.war、partner.war、prm.war
    '''
    for li in ['portal/partner.war', 'portal/admin.war', 'prm/prm.war']:
        sftpupload( './tmp/migu/%s/Release/%s' % ( migu_build_str, li ),
                   Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
                   '%s/upload' % ( Env_miguauto['jboss_home']) )
    '''
	
    #上传admin.war
    sftpupload( './tmp/migu/%s/Release/portal/admin.war' % ( migu_build_str, ),
               Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
               '%s/upload/admin.war' % ( Env_miguauto['jboss_home'], ) )
    #上传partner.war
    sftpupload( './tmp/migu/%s/Release/portal/partner.war' % ( migu_build_str, ),
               Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
               '%s/upload/partner.war' % ( Env_miguauto['jboss_home'], ) )
    #上传server.war
    sftpupload( './tmp/migu/%s/Release/prm/prm.war' % ( migu_build_str, ),
               Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
               '%s/upload/prm.war' % ( Env_miguauto['jboss_home'], ) )
    
    #删除admin的配置文件
    RemoteCmd( Env_admin['ip'], Env_admin['user'], Env_admin['passwd'],
           'cd %s/bin;rm -Rf config;rm -Rf deploy_config' % Env_admin['jboss_home'] )
    #删除partner的配置文件
    RemoteCmd( Env_partner['ip'], Env_partner['user'], Env_partner['passwd'],
           'cd %s/bin;rm -Rf config;rm -Rf deploy_config' % Env_partner['jboss_home'] )
    #删除server的配置文件
    RemoteCmd( Env_server['ip'], Env_server['user'], Env_server['passwd'],
           'cd %s/bin;rm -Rf config;rm -Rf deploy_config' % Env_server['jboss_home'] )
    
    #上传admin的配置文件
    sftpuploadfolder( './tmp/migu/%s/Release/portal/config' % migu_build_str,
                    Env_admin['ip'], Env_admin['user'], Env_admin['passwd'],
                    '%s/bin' % Env_admin['jboss_home'] )
    sftpuploadfolder( './tmp/migu/%s/Release/portal/deploy_config' % migu_build_str,
                    Env_admin['ip'], Env_admin['user'], Env_admin['passwd'],
                    '%s/bin' % Env_admin['jboss_home'] )                   
    #上传partner的配置文件
    sftpuploadfolder( './tmp/migu/%s/Release/portal/config' % migu_build_str,
                    Env_partner['ip'], Env_partner['user'], Env_partner['passwd'],
                    '%s/bin' % Env_partner['jboss_home'] )
    sftpuploadfolder( './tmp/migu/%s/Release/portal/deploy_config' % migu_build_str,
                    Env_partner['ip'], Env_partner['user'], Env_partner['passwd'],
                    '%s/bin' % Env_partner['jboss_home'] )
    #上传server的配置文件
    sftpuploadfolder( './tmp/migu/%s/Release/prm/config' % migu_build_str,
                    Env_server['ip'], Env_server['user'], Env_server['passwd'],
                    '%s/bin' % Env_server['jboss_home'] )
    sftpuploadfolder( './tmp/migu/%s/Release/prm/deploy_config' % migu_build_str,
                    Env_server['ip'], Env_server['user'], Env_server['passwd'],
                    '%s/bin' % Env_server['jboss_home'] )
    
    #修改admin、server、partner的配置文件
    modifyRemoteMiguConf()
    
    #重新部署数据库
    if rebuilddb == 1:
        rebuildDb()

    RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
           '. ~/.bash_profile; > ~/build.info; echo build=%s >> ~/build.info' % ( migu_build_str) )


def deploy_iodd():
    '''部署iodd'''
    #停止iodd服务
    RemoteCmd( Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'],
           'cd %s/bin;sh stop.sh' % Env_iodd['jboss_home'] )
    
    #删除iodd.war
    RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
       'cd ~/upload;rm iodd.war' )
    
    #上传iodd.war
    sftpupload( './tmp/migu/%s/Release/iodd/iodd.war' % ( migu_build_str, ),
               Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
               '%s/upload/iodd.war' % ( Env_miguauto['jboss_home'], ) )
    
    #删除iodd的配置文件
    RemoteCmd( Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'],
           'cd %s/bin;rm -Rf config;rm -Rf deploy_config' % Env_iodd['jboss_home'] )
    
    #上传iodd的配置文件
    sftpuploadfolder( './tmp/migu/%s/Release/iodd/config' % migu_build_str,
                    Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'],
                    '%s/bin' % Env_iodd['jboss_home'] )
    sftpuploadfolder( './tmp/migu/%s/Release/iodd/deploy_config' % migu_build_str,
                    Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'],
                    '%s/bin' % Env_iodd['jboss_home'] )
    
    #修改iodd的配置文件
    modifyRemoteIoddConf()

def deploy_webbas():
    '''部署web_bas2.0'''
    #停止webbas2.0服务
    RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
           'cd %s/tomcat-authmgt/bin;./stop.sh' % Env_miguauto['jboss_home'] )
           
    #删除webbas.war
    RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
       'cd ~/tomcat-authmgt/webapps;rm webbas.war' )
    
    #上传webbas.war
    sftpupload( './tmp/migu/%s/Release/authmgt/webbas.war' % ( migu_build_str, ),
               Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
               '%s/tomcat-authmgt/webapps/webbas.war' % ( Env_miguauto['jboss_home'], ) )
    
    #删除webbas2.0的配置文件
    RemoteCmd( Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
           'cd %s/tomcat-authmgt/bin;rm -Rf config' % Env_miguauto['jboss_home'] )
    
    #上传webbas2.0的配置文件
    sftpuploadfolder( './tmp/migu/%s/Release/authmgt/config' % migu_build_str,
                    Env_miguauto['ip'], Env_miguauto['user'], Env_miguauto['passwd'],
                    '%s/tomcat-authmgt/bin' % Env_miguauto['jboss_home'] )
                    
    #修改webbas2.0的配置文件
    modifyWebbasConf()
    
def deploy( rebuilddb = 1 ):
    '''部署的逻辑执行'''
    getLastbuildFile()
    deploy_migu( rebuilddb )
    deploy_iodd()
    deploy_webbas()
    startMigu()
    startIodd()
    startWebbas()



if __name__ == "__main__":
    deploy( rebuilddb = 1 )

