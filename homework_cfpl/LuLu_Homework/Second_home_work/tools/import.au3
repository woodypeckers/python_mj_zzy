#cs ----------------------------------------------------------------------------

 AutoIt Version: 3.3.14.2
 Author:         myName

 Script Function:
	Template AutoIt script.

#ce ----------------------------------------------------------------------------

; Script Start - Add your code below here


$handle=WinGetHandle("文件上传")
WinActivate($handle)

AutoItSetOption("SendKeyDelay",40)
send("E:\TEST\pycharmcode\python_wanjl_code\201707170800\config\test.xml")
Sleep(3000)

send("{ENTER}")