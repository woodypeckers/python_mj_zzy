*** Settings ***
Library           Selenium2Library

*** Variables ***
${base_url}       http://localhost/bugfree/index.php/site/login

*** Keywords ***
打开登录页面
    [Arguments]    ${base_url}
    Open Browser    ${base_url}    ie

输入用户名
    [Arguments]    ${username}
    Input Text    id=LoginForm_username    ${username}

输入密码
    [Arguments]    ${password}
    Input Password    id=LoginForm_password    ${password}

点击登录
    Click Button    id=SubmitLoginBTN

页面包含
    [Arguments]    ${title}
    Page Should Contain    ${title}
