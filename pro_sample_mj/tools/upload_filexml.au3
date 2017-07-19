;获取窗口句柄
$handle = WinGetHandle("打开")
WinActivate($handle)
;获取控件句柄；

;选择要上传的文件
AutoItSetOption("SendKeyDelay", 40)
Send("D:\Github_erqi\python_zhanyong\pro_sample_mj\tools\import_test.xml")
Sleep(2000)

;确认选择
Send("{ENTER}")