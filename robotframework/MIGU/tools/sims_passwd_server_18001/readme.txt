工具用途：
	模拟rtplt生成passwd加密串，采用了RemoteServer的方式向RFS提供服务。

使用方式：
	部署在linux机器上，使用jython，并nohup运行。

	RFS的用法详见Common/公用.txt中
	Library           Remote    http://10.12.12.157:18001    WITH NAME    rtplt


备注：
	当前已经由彭亨康部署在http://10.12.12.157:18001
	如果工具已启动，则RFS中可以通过rtplt后加点查看到具备的方法； 如果工具未启动，则引用Library的那句话会变红色，另外，rtplt.Encryptpasswd会成为不可识别的关键字（由蓝色变成黑色）

