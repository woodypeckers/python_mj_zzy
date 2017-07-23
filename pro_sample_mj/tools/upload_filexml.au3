
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


#cs ----------------------------------------------------------------------------
; Script Start - Add your code below here
$handle=WinGetHandle("打开 import_test.xml")
WinActivate($handle)

;点击保存文件按钮
;ControlClick("正在打开 buglist.xml","",,,375,570)
;Sleep(3000)
;点击浏览按钮
a=ControlGetFocus("打开 import_test.xml","浏览")
a.send("{SPACE}")


;保存文件路径
$handle1=WinGetHandle("选择下载文件夹:")
WinActivate($handle1)
AutoItSetOption("SendKeyDelay", 40)
send("D:\Github_erqi\python_zhanyong\pro_sample_mj\tools\import_test.xml")
send(2000)
send("{ENTER}")

send(2000)
WinActivate($handle)
send("{ENTER}")
#ce ----------------------------------------------------------------------------

