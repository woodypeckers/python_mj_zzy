*** Settings ***
Library           OperatingSystem
Library           ../../library/jsonLibrary.py
Resource          ../../resource/HttpLibrary.HTTP.robot
Resource          ../../resource/NNN接口.robot

*** Variables ***

*** Test Cases ***
向URL发起POST请求
    模拟器调用_test_json_utf8接口    13500000000    中文姓名    0
    ${unicode_request_body}=    OperatingSystem.Get File    Template/utf8.json    encoding=utf-8
    custom_post    http://127.0.0.1:10001/test/json/utf8    ${unicode_request_body}    encoding=utf-8
