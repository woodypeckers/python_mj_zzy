1��PC��������sim.bat �Ϳ��ԣ��˿�Ϊ7779
��ص�ַΪlocalhost(����IP)
http://localhost:7779/migu/app/getData/getBill                       #1. ʵʱ�˵��ӿ�
http://localhost:7779/migu/app/getData/getPauseInfo             #2. ��ͣ��Ϣ��ȡ�ӿ�
http://localhost:7779/migu/app/getData/getBillDetail           #3. ʵʱ�˵���ϸ�ӿ�
http://localhost:7779/migu/app/getData/getBillDetailHf      #4. ʵʱ�˵�������ӿ�
http://localhost:7779//migu/app/getData/getBillDetailFhf     #5. ʵʱ�˵��ǻ�����ӿ�
http://localhost:7779//migu/app/getData/getBillDetailDl   #6. ʵʱ�˵���������ӿ�
2����������python Sim_JSSP.py

3��������ر�Ŀǰ���ݿ����ӵ�MIGU�������ݿ�
select * from bill a ;  ---1. ʵʱ�˵�
select * from pause_info ; --2. ��ͣ��Ϣ
select * from  bill_detail ; --3. ʵʱ�˵���ϸ
select a.*,a.rowid from bill_detail_hf a; --4. ʵʱ�˵�������
select a.*,a.rowid from Bill_Detail_FHf a;--5. ʵʱ�˵��ǻ�����
select a.*,a.rowid from Bill_Detail_Dl a; ---6. ʵʱ�˵���������