# -*- coding:cp936 -*-
from prm_biz import *
from Utils import *

SSH_flag = 1

# build目录，需要常改，一般从邮件中获取
prm_build_folder = r'\\Asp-bld-serv100\release_bldstg\PRM\PRM1.0.2.007\PRM1.0.2.007_SSYT_4__20151201_16.55.30'

# 环境情况，一般只用配一次
Env_oracle = {'name':'db', 'type':'oracle', 'ip':'10.12.3.197', 'port':'1521', 'user':'prm_auto', 'passwd':'prm_auto_1000', 'tnsname':'10.12.3.197', 'sid':'ora11g'}
Env_prm = {'name':'prm', 'type':'jboss', 'ip':'10.12.12.157', 'port':'18080', 'user':'prm', 'passwd':'prm', 'jboss_home':'/opt/aspire/product/prm/jboss7'}
Env_iodd = {'name':'prmiodd', 'type':'jboss', 'ip':'10.12.12.157', 'port':'28080', 'user':'prm', 'passwd':'prm', 'jboss_home':'/opt/aspire/product/prm/jboss7_iodd', 'sims_inf_url':'http://10.12.12.157:9001'}


prm_build_str = prm_build_folder.split( '\\' )[-1]

def deploy_prm( rebuilddb = 1 ):
    # 先修改一下war包
    script_dir = os.path.abspath( os.path.curdir )
    os.chdir( './tmp/prm/%s/Release' % prm_build_str )
    modify_jquery_biz_in_war( 'prm.war' )
    modify_jquery_biz_in_war( 'prm_admin.war' )
    os.chdir( script_dir )

    RemoteCmd( Env_prm['ip'], Env_prm['user'], Env_prm['passwd'],
           'cd ~/jboss7/standalone/deployments;rm prm_admin.war;rm server.war;rm helpdoc.war;rm prm_sp.war;rm faqdoc.war' )
    RemoteCmd( Env_prm['ip'], Env_prm['user'], Env_prm['passwd'],
           'cd %s/bin;sh stop.sh' % Env_prm['jboss_home'] )
    for li in ['prm.war', 'prm_admin.war', 'prm_server.war', 'helpdoc.war', 'faqdoc.war']:
        sftpupload( './tmp/prm/%s/Release/%s' % ( prm_build_str, li ),
                   Env_prm['ip'], Env_prm['user'], Env_prm['passwd'],
                   '%s/../jboss7/standalone/deployments/%s' % ( Env_prm['jboss_home'], li ) )
	RemoteCmd( Env_prm['ip'], Env_prm['user'], Env_prm['passwd'],
           'cd ~/jboss7/standalone/deployments;mv prm.war prm_sp.war' )
    RemoteCmd( Env_prm['ip'], Env_prm['user'], Env_prm['passwd'],
           'cd ~/jboss7/standalone/deployments;mv prm_server.war server.war' )
    RemoteCmd( Env_prm['ip'], Env_prm['user'], Env_prm['passwd'],
           'cd %s/bin;rm -Rf config;rm -Rf deploy_config' % Env_prm['jboss_home'] )
    sftpuploadfolder( './tmp/prm/%s/Release/config' % prm_build_str,
                    Env_prm['ip'], Env_prm['user'], Env_prm['passwd'],
                    '%s/bin' % Env_prm['jboss_home'] )
    sftpuploadfolder( './tmp/prm/%s/Release/deploy_config' % prm_build_str,
                    Env_prm['ip'], Env_prm['user'], Env_prm['passwd'],
                    '%s/bin' % Env_prm['jboss_home'] )
    modifyRemotePrmConf()


    # 重做数据库
    if rebuilddb == 1:
        rebuildDb()

    RemoteCmd( Env_prm['ip'], Env_prm['user'], Env_prm['passwd'],
           '. ~/.bash_profile; > ~/build.info; echo build=%s >> ~/build.info' % ( prm_build_str, ) )


def deploy_iodd():
    # iodd
    RemoteCmd( Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'],
       'cd ~/jboss7_iodd/standalone/deployments;rm iodd.war' )
    RemoteCmd( Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'],
           'cd %s/bin;sh stop.sh' % Env_iodd['jboss_home'] )
    sftpupload( './tmp/prm/%s/Release/iodd/iodd.war' % ( prm_build_str, ),
               Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'],
               '%s/../jboss7_iodd/standalone/deployments/iodd.war' % ( Env_iodd['jboss_home'], ) )
    sftpuploadfolder( './tmp/prm/%s/Release/iodd/config' % prm_build_str,
                    Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'],
                    '%s/bin' % Env_iodd['jboss_home'] )
    sftpuploadfolder( './tmp/prm/%s/Release/iodd/deploy_config' % prm_build_str,
                    Env_iodd['ip'], Env_iodd['user'], Env_iodd['passwd'],
                    '%s/bin' % Env_iodd['jboss_home'] )
    modifyRemoteIoddConf()

def deploy( rebuilddb = 1 ):
    '''部署的逻辑执行'''
    getLastbuildFile()
    stopIodd()
    stopPrm()
    deploy_prm( rebuilddb )
    deploy_iodd()
    startPrm()
    startIodd()



if __name__ == "__main__":
    deploy( rebuilddb = 1 )

