1、PC本地运行sim.bat 就可以，端口为7779
相关地址为localhost(本地IP)
http://localhost:7779/migu/app/getData/getBill                       #1. 实时账单接口
http://localhost:7779/migu/app/getData/getPauseInfo             #2. 暂停信息获取接口
http://localhost:7779/migu/app/getData/getBillDetail           #3. 实时账单明细接口
http://localhost:7779/migu/app/getData/getBillDetailHf      #4. 实时账单话费类接口
http://localhost:7779//migu/app/getData/getBillDetailFhf     #5. 实时账单非话费类接口
http://localhost:7779//migu/app/getData/getBillDetailDl   #6. 实时账单代理收入接口
2、服务运行python Sim_JSSP.py

3、结算相关表，目前数据库连接的MIGU测试数据库
select * from bill a ;  ---1. 实时账单
select * from pause_info ; --2. 暂停信息
select * from  bill_detail ; --3. 实时账单明细
select a.*,a.rowid from bill_detail_hf a; --4. 实时账单话费类
select a.*,a.rowid from Bill_Detail_FHf a;--5. 实时账单非话费类
select a.*,a.rowid from Bill_Detail_Dl a; ---6. 实时账单代理收入