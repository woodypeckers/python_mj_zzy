*** Settings ***
Resource          resources.robot
Library           Selenium2Library
Resource          Business_key.robot

*** Test Cases ***
用于问题记录
    [Template]
    #截图如何格式化
    #指定系统关键字，封装成逻辑步骤，然后封装成一个业务关键字，调用这个业务关键字模板，即调用指定步骤    #已解决
    #批量添加，如何for循环，产品名称list化

登录逻辑
    打开浏览器    ${base_url}
    输入用户名    ${user_name}
    输入密码    ${password}
    登录后验证    ${title}
    Sleep    3s
    ${file1}=    Capture Page Screenshot
    File Should Exist    ${OUTPUTDIR}${/}selenium-screenshot-1.png

selenium截图
    Open Browser    https://www.baidu.com
    ${file1} =    Capture Page Screenshot
    File Should Exist    ${OUTPUTDIR}${/}selenium-screenshot-1.png
    Sleep    3s
    ${file2}    Capture Page Screenshot
    File Should Exist    ${OUTPUTDIR}${/}selenium-screenshot-2.png
    close Browser

标准截图
    Screenshot.Set Screenshot Directory    c:\Intel
    sleep    2s
    Take Screenshot    mypic
    Take Screenshot    mypic
