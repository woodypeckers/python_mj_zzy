*** Settings ***
Library           OperatingSystem
Library           ../../library/jsonLibrary.py
Resource          ../../resource/HttpLibrary.HTTP.robot
Resource          ../../resource/NNN接口.robot

*** Variables ***

*** Test Cases ***
服务端原值返回自定义头
    ${custom_header}    Set Variable    {"customheader1":"REPLY","customheader2":"REPLY","customheader3":"REPLY"}
    模拟器调用_test_json_customheader接口    13500000000    中文姓名    0    3    0    ${custom_header}
    ${unicode_request_body}=    OperatingSystem.Get File    Template/utf8.json    encoding=utf-8
    ${custom_headers}    Create Dictionary    customheader1=12345    customheader2=22222    customheader3=33333
    custom_post    http://127.0.0.1:10002/test/json/default_utf8    ${unicode_request_body}    encoding=utf-8    custom_headers=${custom_headers}
    ${rsp_header1}    获取返回包头    customheader1
    ${rsp_header2}    获取返回包头    customheader2
    ${rsp_header3}    获取返回包头    customheader3
    Should Be Equal As Strings    ${rsp_header1}    12345
    Should Be Equal As Strings    ${rsp_header2}    22222
    Should Be Equal As Strings    ${rsp_header3}    33333

服务端创建自定义头的值
    [Documentation]    对于某些接口，是请求一个类似于Session的值，如getToken接口，此时http请求不带头，而服务端的返回的Token为随机值
    ${random_token}    创建随机值
    ${custom_header}    Set Variable    {"customheader1":"REPLY","token":"${random_token}"}
    模拟器调用_test_json_customheader接口    13500000000    中文姓名    0    3    0    ${custom_header}
    ${unicode_request_body}=    OperatingSystem.Get File    Template/utf8.json    encoding=utf-8
    ${custom_headers}    Create Dictionary    customheader1=12345
    custom_post    http://127.0.0.1:10002/test/json/default_utf8    ${unicode_request_body}    encoding=utf-8    custom_headers=${custom_headers}
    ${rsp_header1}    获取返回包头    customheader1
    ${token_header}    获取返回包头    token
    Should Be Equal As Strings    ${rsp_header1}    12345
    Should Be Equal As Strings    ${token_header}    ${random_token}

*** Keywords ***
创建随机值
    ${random_token}    Generate Random String    12    [LOWER]
    [Return]    ${random_token}
