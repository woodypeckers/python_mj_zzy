@echo off
echo "这个脚本自动启mockserver,然后运行pybot报告测试，最后打开RF的测试报告"


cd ..\..
start python.exe simServer.py
sleep 5
cd docs\Demo
start pybot --LogLevel Trace:Info -d report 接口案例
sleep 10&&start report\log.html&&taskkill /IM python.exe&&taskkill /IM cmd.exe
