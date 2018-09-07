*** Settings ***
Library           Selenium2Library
Library           String
Library           DateTime
Library           OperatingSystem
Library           Screenshot

*** Variables ***
${base_url}       http://localhost/ranzhi/www/
${user_name}      admin
${password}       123456
${title}          然之协同

*** Keywords ***
等待
    Sleep    2s

打开浏览器
    [Arguments]    ${base_url}
    Open Browser    ${base_url}
    Maximize Browser Window

输入用户名
    [Arguments]    ${user_name}
    Input Text    id=account    ${user_name}

输入密码
    [Arguments]    ${password}
    Input Password    id=password    ${password}

登录后验证
    [Arguments]    ${title}
    Click Button    id=submit
    Page Should Contain    ${title}

等待3秒
    [Arguments]    ${time_sleep}
    sleep    ${time_sleep}    3s

submit
    Click Element    id=submit
