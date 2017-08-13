*** Settings ***
Library           RequestsLibrary
Library           HttpLibrary.HTTP
Library           Collections

*** Keywords ***
建立连接
    [Arguments]    ${url}
    Create Session	    http_session    ${url}

发送POST请求
    [Arguments]    ${uri}    ${body}    ${headers}=None
    ${responsebody}=    Post Request    alias1    uri    data=${body}    headers=${headers}
    [Return]    ${responsebody}

test1
    [Arguments]
    Po