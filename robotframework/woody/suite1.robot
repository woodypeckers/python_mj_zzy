*** Settings ***
Library           Selenium2Library
Resource          resources.robot

*** Test Cases ***
test1
    log    1111aaaa
    Open Browser    https://localhost/bugfree    ie

登录成功
    [Tags]    登录成功
    [Template]    登录业务公共关键字
    admin    123456    退出

登录失败_用户名不存在
    [Template]    登录业务公共关键字
    asaas    123456    用户名不存在

登录失败_用户名和密码不匹配
    [Template]    登录业务公共关键字
    admin    1111    用户名和密码不匹配

*** Keywords ***
登录业务公共关键字
    [Arguments]    ${username}    ${password}    ${title}
    Log Many    ${username}    ${password}    ${title}
    打开登录页面    ${base_url}
    输入用户名    ${username}
    输入密码    ${password}
    点击登录
    页面包含    ${title}
    [Teardown]    close browser
