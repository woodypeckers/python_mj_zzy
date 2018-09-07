*** Settings ***
Library           Selenium2Library
Resource          resources.robot

*** Keywords ***
登录业务逻辑
    打开浏览器    ${base_url}
    输入用户名    ${user_name}
    输入密码    ${password}
    登录后验证    ${title}
    等待
    ${file1}=    Capture Page Screenshot
    File Should Exist    ${OUTPUTDIR}${/}selenium-screenshot-1.png
    Set Browser Implicit Wait    10s    #智能等待

退出
    Sleep    2s
    Click Button    id=start
    Sleep    2s
    Click Link    xpath=.//*[@id='startMenu']/li[10]/a
    Comment    Click Link    xpath=.//*[@id='startMenu']/li[10]/a    #也可以
    Sleep    2s
    Close All Browsers

进入客户列表页面
    Click Element    id=s-menu-1    #电话图标
    Sleep    3s
    Select Frame    id=iframe-1
    Click link    xpath=.//*[@id='mainNavbar']/div[2]/ul/li[4]/a    #客户

进入合同列表页面
    Click Element    id=s-menu-1    #电话图标
    Sleep    3s
    Select Frame    id=iframe-1
    Click link    xpath=.//*[@id='mainNavbar']/div[2]/ul/li[3]/a    #合同

进入订单列表页面
    Click Element    id=s-menu-1    #电话图标
    Sleep    3s
    Select Frame    id=iframe-1
    Click link    xpath=.//*[@id='mainNavbar']/div[2]/ul/li[2]/a    #订单
