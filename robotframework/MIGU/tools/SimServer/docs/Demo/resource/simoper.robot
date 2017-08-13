*** Settings ***
Documentation     这个来源于mock server中的例子，原则上，其他的模拟器调用均可以参考这个例子
Library           ../library/httpLibrary.py
Library           ../library/simClient.py

*** Variables ***
${sim_set_url}    http://127.0.0.1:8000/simSet    #http://10.1.25.61:8000/simSet wangmianjie
${sim_query_url}    http://127.0.0.1:8000/simQuery    #http://10.1.25.61:8000/simQuery
${被测系统ip}         127.0.0.1

*** Keywords ***
模拟器调用请求
    [Arguments]    ${req_data}    # http请求数据
    ${rspStr}=    http post    ${sim_set_url}    ${req_data}
    [Return]    ${rspStr}

模拟器调用请求包构造
    [Arguments]    ${msgType}    ${timeOut}    ${request}    ${response}    ${delay}    ${custom_header}=${EMPTY}
    ...    ${verifyMode}=NORMAL    ${respMode}=NORMAL    #消息URL|超时时间|请求参数|应答参数|模拟器返回延迟时间|自定义头|校验模式|应答模式
    ${simPkg}=    simReqPkg    ${被测系统ip}    ${timeOut}    ${msgType}    ${request}    ${response}
    ...    ${delay}    ${custom_header}    ${verifyMode}    ${respMode}
    log    ${simPkg}
    [Return]    ${simPkg}

模拟器结果查询
    [Arguments]    ${req_data}    ${result_strint}=success    ${ip}=${sim_query_url}    # http请求数据
    ${rspStr}=    http post    ${ip}    ${req_data}
    Should Be Equal As Strings    ${rspStr}    ${result_strint}
    log    模拟器调用成功
    [Return]    ${rspStr}
