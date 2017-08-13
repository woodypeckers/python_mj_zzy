#-*- coding:utf-8 -*-
import rtpltlib
from robotremoteserver import RobotRemoteServer
	
if __name__ == '__main__':
	print "RobotRemoteServer Listening on port 18001..."
	server = RobotRemoteServer(rtpltlib,"0.0.0.0",18001)
	
