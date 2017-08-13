*** Settings ***
Library           XML    uselxml=True
Library           Collections
Library           OperatingSystem
Library           ../../library/XMLAddon.py
Resource          ../../resource/HttpLibrary.HTTP.robot
Resource          ../../resource/NNN接口.robot
Library           random

*** Variables ***

*** Test Cases ***
服务端原值返回3个自定义头
    [Documentation]    Mock的system.xml中，http server如果不配置编码，则缺省按utf-8处理。这样可以兼容以前的Mock V1
    模拟器调用_test_xml_customheader接口    123456789012    愤怒的小鸟    123456    南京市游戏设计有限责任公司    0    0
    ...    3    0    {"customheader1":"REPLY","customheader2":"REPLY","customheader3":"REPLY"}
    ${unicode_request_body}=    OperatingSystem.Get File    Template/utf8.xml    encoding=utf-8
    ${custom_headers}    Create Dictionary    customheader1=12345    customheader2=22222    customheader3=33333
    custom_post    http://127.0.0.1:20002/test/xml/default_utf8    ${unicode_request_body}    encoding=utf-8    custom_headers=${custom_headers}
    ${encoding}    获取response_body编码
    Should Be Equal As Strings    ${encoding}    UTF-8
    ${rsp_header1}    获取返回包头    customheader1
    ${rsp_header2}    获取返回包头    customheader2
    ${rsp_header3}    获取返回包头    customheader3
    Should Be Equal As Strings    ${rsp_header1}    12345
    Should Be Equal As Strings    ${rsp_header2}    22222
    Should Be Equal As Strings    ${rsp_header3}    33333

服务端创建自定义头的值
    [Documentation]    对于某些接口，是请求一个类似于Session的值，如getToken接口，此时http请求不带头，而服务端的返回的Token为随机值
    ${random_token}    创建随机值
    模拟器调用_test_xml_customheader接口    123456789012    愤怒的小鸟    123456    南京市游戏设计有限责任公司    0    0
    ...    3    0    {"customheader1":"REPLY","token":"${random_token}"}
    ${unicode_request_body}=    OperatingSystem.Get File    Template/utf8.xml    encoding=utf-8
    ${custom_headers}    Create Dictionary    customheader1=12345
    custom_post    http://127.0.0.1:20002/test/xml/default_utf8    ${unicode_request_body}    encoding=utf-8    custom_headers=${custom_headers}
    ${encoding}    获取response_body编码
    ${rsp_header1}    获取返回包头    customheader1
    ${rsp_header_token}    获取返回包头    token
    Should Be Equal As Strings    ${rsp_header1}    12345
    Should Be Equal As Strings    ${rsp_header_token}    ${random_token}

*** Keywords ***
创建随机值
    ${random_token}    Generate Random String    12    [LOWER]
    [Return]    ${random_token}
