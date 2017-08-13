# -*- coding:cp936 -*-
import ftplib
import logging
import os
import paramiko
import shutil
import sys
import telnetlib

############### logger #######################
logger = logging.getLogger( 'MyLog' )
formatter = logging.Formatter( '[%(asctime)s][%(levelname)s] %(message)s' )
# formatter = logging.Formatter( '%(levelname)s:%(message)s' )
runtimelog = logging.FileHandler( "运行日志.log" )
runtimelog.setFormatter( formatter )
logger.addHandler( runtimelog )
# 写屏功能，如不需要，则请注释下面三行
stdoutlog = logging.StreamHandler( sys.stdout )
stdoutlog.setFormatter( formatter )
logger.addHandler( stdoutlog )
logger.setLevel( logging.DEBUG )  # DEBUG, INFO, WARNING, ERROR, CRITICAL ...etc

SSH_flag = 1

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


def TelnetCmd( ip, username, password, command = 'ls -alt', logflag = 1 ):
    if logflag == 1:
        logger.info( '执行远程Telnet命令,环境%s:%s:%s,命令%s' % ( ip, username, password, command ) )
    tn = telnetlib.Telnet( ip )
    tn.read_until( "ogin" )
    tn.write( username + "\n" )
    tn.read_until( "assword " )
    tn.write( password + "\n" )
    tn.write( "%s\n" % command )
    std_info = tn.read_all()
    logger.info( std_info )
    tn.write( "exit\n" )
    return std_info

def RemoteCmd( ip, username, password, command, logflag = 1 ):
    global SSH_flag
    std_info = None
    if SSH_flag == 1:
        std_info = SSHCmd( ip, username, password, command, logflag )
    else:
        std_info = TelnetCmd( ip, username, password, command, logflag )
    return std_info

def test_SSHCmd():
    ip = '192.168.253.10'
    username = 'demodb'
    password = 'demodb'
    std = SSHCmd( ip, username, password, 'ps -ef|grep java' )
    print std

def CleanDir( Dir ):
    if os.path.isdir( Dir ):
        paths = os.listdir( Dir )
        for path in paths:
            filePath = os.path.join( Dir, path )
            if os.path.isfile( filePath ):
                try:
                    os.remove( filePath )
                except os.error:
                    print  "remove %s error." % filePath
            elif os.path.isdir( filePath ):
                if filePath[-4:].lower() == ".svn".lower():
                    continue
                shutil.rmtree( filePath, True )
    return True

def ftpupload( localfile, ip, username, passwd, remotefile, mode = 'bin' ):
    '''将某个文件上传到FTP服务器上，不考虑太多异常'''
    logger.info( 'ftp上传文件  【%s】 %s => ftp://%s:%s@%s %s' % ( mode, localfile, username, passwd, ip, remotefile ) )
    destpath = os.path.split( remotefile )[0]
    filename = os.path.split( remotefile )[1]
    ftpclient = ftplib.FTP( ip )
    ftpclient.set_debuglevel( 0 )
    # ftpclient.connect()
    ftpclient.login( username, passwd )

    ftpclient.cwd( destpath )
    if mode == 'bin':
        ftpclient.storbinary( 'STOR %s' % filename, open( localfile, 'rb' ) )
    else:
        ftpclient.storlines( 'STOR %s' % filename, open( localfile, 'r' ) )
    ftpclient.close()
    ftpclient = None

def ftpdownload( ip, username, passwd, remotefile, localfile, mode = 'bin' ):
    '''将某个文件下载到FTP服务器上，不考虑太多异常'''
    logger.info( 'ftp下载文件  【%s】 ftp://%s:%s@%s %s => %s' % ( mode, username, passwd, ip, remotefile, localfile ) )
    destpath = os.path.split( remotefile )[0]
    filename = os.path.split( remotefile )[1]
    ftpclient = ftplib.FTP( ip )
    ftpclient.set_debuglevel( 0 )
    # ftpclient.connect()
    ftpclient.login( username, passwd )

    ftpclient.cwd( destpath )
    if mode == 'bin':
        ftpclient.retrbinary( 'RETR %s' % filename, open( localfile, 'wb' ).write )
    else:
        ftpclient.retrlines( 'RETR %s' % filename, lambda s, w = open( localfile, 'w' ).write: w( s + "\n" ) )
    ftpclient.close()
    ftpclient = None



def replaceFileStr( filepath, orgstr, newstr ):
    logger.info( '修改配置文件中的字符串%s %s替换成%s' % ( filepath, orgstr, newstr ) )
    filestr = open( filepath, 'r+' ).read()
    newfilestr = filestr.replace( orgstr, newstr )
    open( filepath, 'w' ).write( newfilestr )

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

def sftpupload( localfile, ip, username, passwd, remotefile, mode='ascii' ):
    port = 22
    try:
        t = paramiko.Transport((ip, port))
        t.connect(username=username, password=passwd)

        sftp =paramiko.SFTPClient.from_transport(t)
        sftp.put(localfile, remotefile)
        t.close();
    except Exception, e:
        logger.error('sftp上载%s出错：%s \n%s' % (localfile,e.__class__, e) )
        import traceback
        traceback.print_exc()
        try:
            t.close()
        except:
            pass

def sftpdownload( ip, username, passwd, remotefile, localfile, mode='ascii' ):
    port=22
    try:
        t = paramiko.Transport((ip, port))
        t.connect(username=username, password=passwd)
        sftp =paramiko.SFTPClient.from_transport(t)
        sftp.get(remotefile, localfile)
        t.close();
    except Exception, e:
        logger.error('sftp下载%s出错：%s \n%s' % (remotefile,e.__class__, e) )
        import traceback
        traceback.print_exc()
        try:
            t.close()
        except:
            pass            

def sftpuploadfolder( localdir, ip, user, passwd, remotepdir ):
    '''将本机上的目录打包,sftp放远程服务器上，再解包'''
    script_dir = os.path.abspath( os.path.curdir )
    folder_name = os.path.split( localdir )[-1]
    localdir_parent = os.path.sep.join( os.path.split( localdir )[:-1] )
    os.chdir( localdir_parent )
    os.system( 'zip -r -l %s.zip %s' % ( folder_name, folder_name ) )
    os.chdir( script_dir )
    zipfile_path = os.path.join( localdir_parent, '%s.zip' % folder_name )
    remotefile = remotepdir + '/' + folder_name + '.zip'
    zipfile_name = folder_name + '.zip'
    sftpupload( zipfile_path, ip, user, passwd, remotefile )
    RemoteCmd( ip, user, passwd, 'cd %s;unzip -u -o %s; rm %s' % ( remotepdir, zipfile_name, zipfile_name ) )    


def test():
    RemoteCmd( '10.12.12.157', 'prm', 'prm', 'ls -atl', logflag = 1 )
    global SSH_flag
    # SSH_flag = 0
    # RemoteCmd( '10.1.4.212', 'daf20pf', 'daf20pf', 'ps -ef', logflag = 1 )
    pass


if __name__ == "__main__":
    test()
