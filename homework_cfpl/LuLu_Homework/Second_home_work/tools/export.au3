#cs ----------------------------------------------------------------------------

 AutoIt Version: 3.3.14.2
 Author:         myName

 Script Function:
	Template AutoIt script.

#ce ----------------------------------------------------------------------------

; Script Start - Add your code below here
$handle=WinGetHandle("正在打开 buglist.xml")
WinActivate($handle)

;点击保存文件按钮
ControlClick("正在打开 buglist.xml","","Button2",,570,375)
Sleep(3000)
;点击浏览按钮
ControlClick("正在打开 buglist.xml","浏览","Button2")



;保存文件路径
$handle1=WinGetHandle("选择下载文件夹:")
WinActivate($handle1)
AutoItSetOption("SendKeyDelay", 40)
send("E:\TEST\pycharmcode\python_wanjl_code\201707170800\tools\buglist.xml")
send(2000)
send("{ENTER}")

send(2000)
WinActivate($handle)
send("{ENTER}")