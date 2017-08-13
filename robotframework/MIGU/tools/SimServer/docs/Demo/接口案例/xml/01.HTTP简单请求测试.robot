*** Settings ***
Documentation     XML基本上只有POST请求
Library           XML    uselxml=True
Library           OperatingSystem
Library           Collections
Library           ../../library/XMLAddon.py
Resource          ../../resource/HttpLibrary.HTTP.robot
Resource          ../../resource/NNN接口.robot

*** Variables ***

*** Test Cases ***
向URL发起POST 请求
    模拟器调用_test_xml_default_utf8接口    123456789012    愤怒的小鸟    123456    南京市游戏设计有限责任公司    0    0
    ${unicode_request_body}=    OperatingSystem.Get File    Template/utf8.xml    encoding=utf-8
    ${custom_headers}    Create Dictionary    customheader1=12345
    custom_post    http://127.0.0.1:20002/test/xml/default_utf8    ${unicode_request_body}    encoding=utf-8    custom_headers=${custom_headers}
    XML.Element Text Should Be    ${response_body}    0    //resultInfos/returnCode

xpath验证模式
    模拟器调用_XPATH验证模式    123456789012    愤怒的小鸟    123456    南京市游戏设计有限责任公司    0    0
    ${unicode_request_body}=    OperatingSystem.Get File    Template/utf8.xml    encoding=utf-8
    ${custom_headers}    Create Dictionary    customheader1=12345
    custom_post    http://127.0.0.1:20002/test/xml/default_utf8    ${unicode_request_body}    encoding=utf-8    custom_headers=${custom_headers}
    XML.Element Text Should Be    ${response_body}    0    //resultInfos/returnCode
