@echo off
echo "����ű��Զ���mockserver,Ȼ������pybot������ԣ�����RF�Ĳ��Ա���"


cd ..\..
start python.exe simServer.py
sleep 5
cd docs\Demo
start pybot --LogLevel Trace:Info -d report �ӿڰ���
sleep 10&&start report\log.html&&taskkill /IM python.exe&&taskkill /IM cmd.exe
