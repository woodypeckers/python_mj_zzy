*** Settings ***
Resource          simoper.robot
Library           ../library/detectEncoding.py

*** Keywords ***
模拟器调用_X接口
    [Arguments]    ${validTime}    ${delay}    ${username}    ${payValue}    ${hRet}
    ${request}    Set Variable    {"username":"${username}","payValue":"${payValue}"}
    ${response}    Set Variable    {"hRet":"${hRet}"}
    ${OrderServInfoReq}    模拟器调用请求包构造    /COMP/X/OrderServInfoReq    ${validTime}    ${request}    ${response}    ${delay}
    ${OrderServInfoRsp}    模拟器调用请求    ${OrderServInfoReq}
    [Return]    ${OrderServInfoReq}    ${OrderServInfoRsp}

模拟器调用_test_json_utf8接口
    [Arguments]    ${MobNum}    ${UserID}    ${BusiCode}    ${validTime}=3    ${delay}=0
    ${request}    Set Variable    {"MobNum":"${MobNum}","UserID":"${UserID}"}
    ${response}    Set Variable    {"BusiCode":"${BusiCode}"}
    ${OrderServInfoReq}    模拟器调用请求包构造    /test/json/utf8    ${validTime}    ${request}    ${response}    ${delay}
    ${OrderServInfoRsp}    模拟器调用请求    ${OrderServInfoReq}
    [Return]    ${OrderServInfoReq}    ${OrderServInfoRsp}

模拟器调用_test_json_default_utf8接口
    [Arguments]    ${MobNum}    ${UserID}    ${BusiCode}    ${validTime}=3    ${delay}=0
    ${request}    Set Variable    {"MobNum":"${MobNum}","UserID":"${UserID}"}
    ${response}    Set Variable    {"BusiCode":"${BusiCode}"}
    ${OrderServInfoReq}    模拟器调用请求包构造    /test/json/default_utf8    ${validTime}    ${request}    ${response}    ${delay}
    ${OrderServInfoRsp}    模拟器调用请求    ${OrderServInfoReq}
    [Return]    ${OrderServInfoReq}    ${OrderServInfoRsp}

模拟器调用_test_json_gbk接口
    [Arguments]    ${MobNum}    ${UserID}    ${BusiCode}    ${validTime}=3    ${delay}=0
    ${request}    Set Variable    {"MobNum":"${MobNum}","UserID":"${UserID}"}
    ${response}    Set Variable    {"BusiCode":"${BusiCode}"}
    ${OrderServInfoReq}    模拟器调用请求包构造    /test/json/gbk    ${validTime}    ${request}    ${response}    ${delay}
    ${OrderServInfoRsp}    模拟器调用请求    ${OrderServInfoReq}
    [Return]    ${OrderServInfoReq}    ${OrderServInfoRsp}

模拟器调用_test_json_utf16le接口
    [Arguments]    ${MobNum}    ${UserID}    ${BusiCode}    ${validTime}=3    ${delay}=0
    ${request}    Set Variable    {"MobNum":"${MobNum}","UserID":"${UserID}"}
    ${response}    Set Variable    {"BusiCode":"${BusiCode}"}
    ${OrderServInfoReq}    模拟器调用请求包构造    /test/json/unicode    ${validTime}    ${request}    ${response}    ${delay}
    ${OrderServInfoRsp}    模拟器调用请求    ${OrderServInfoReq}
    [Return]    ${OrderServInfoReq}    ${OrderServInfoRsp}

模拟器调用_test_xml_utf8接口
    [Arguments]    ${contentId}    ${contentName}    ${cpId}    ${cpName}    ${Infos_returnCode}    ${Info_returnCode}
    ...    ${validTime}=3    ${delay}=0
    ${request}    Set Variable    {"contentId":"${contentId}","contentName":"${contentName}","cpId":"${cpId}","cpName":"${cpName}"}
    ${response}    Set Variable    {"Infos_returnCode":"${Infos_returnCode}","Info_returnCode":"${Info_returnCode}"}
    ${OrderServInfoReq}    模拟器调用请求包构造    /test/xml/utf8    ${validTime}    ${request}    ${response}    ${delay}
    ${OrderServInfoRsp}    模拟器调用请求    ${OrderServInfoReq}
    [Return]    ${OrderServInfoReq}    ${OrderServInfoRsp}

模拟器调用_test_xml_default_utf8接口
    [Arguments]    ${contentId}    ${contentName}    ${cpId}    ${cpName}    ${Infos_returnCode}    ${Info_returnCode}
    ...    ${validTime}=3    ${delay}=0
    ${request}    Set Variable    {"contentId":"${contentId}","contentName":"${contentName}","cpId":"${cpId}","cpName":"${cpName}"}
    ${response}    Set Variable    {"Infos_returnCode":"${Infos_returnCode}","Info_returnCode":"${Info_returnCode}"}
    ${OrderServInfoReq}    模拟器调用请求包构造    /test/xml/default_utf8    ${validTime}    ${request}    ${response}    ${delay}
    ${OrderServInfoRsp}    模拟器调用请求    ${OrderServInfoReq}
    [Return]    ${OrderServInfoReq}    ${OrderServInfoRsp}

模拟器调用_test_xml_gbk接口
    [Arguments]    ${contentId}    ${contentName}    ${cpId}    ${cpName}    ${Infos_returnCode}    ${Info_returnCode}
    ...    ${validTime}=3    ${delay}=0
    ${request}    Set Variable    {"contentId":"${contentId}","contentName":"${contentName}","cpId":"${cpId}","cpName":"${cpName}"}
    ${response}    Set Variable    {"Infos_returnCode":"${Infos_returnCode}","Info_returnCode":"${Info_returnCode}"}
    ${OrderServInfoReq}    模拟器调用请求包构造    /test/xml/gbk    ${validTime}    ${request}    ${response}    ${delay}
    ${OrderServInfoRsp}    模拟器调用请求    ${OrderServInfoReq}
    [Return]    ${OrderServInfoReq}    ${OrderServInfoRsp}

模拟器调用_test_xml_utf16le接口
    [Arguments]    ${contentId}    ${contentName}    ${cpId}    ${cpName}    ${Infos_returnCode}    ${Info_returnCode}
    ...    ${validTime}=3    ${delay}=0
    ${request}    Set Variable    {"contentId":"${contentId}","contentName":"${contentName}","cpId":"${cpId}","cpName":"${cpName}"}
    ${response}    Set Variable    {"Infos_returnCode":"${Infos_returnCode}","Info_returnCode":"${Info_returnCode}"}
    ${OrderServInfoReq}    模拟器调用请求包构造    /test/xml/unicode    ${validTime}    ${request}    ${response}    ${delay}
    ${OrderServInfoRsp}    模拟器调用请求    ${OrderServInfoReq}
    [Return]    ${OrderServInfoReq}    ${OrderServInfoRsp}

模拟器调用_test_xml_customheader接口
    [Arguments]    ${contentId}    ${contentName}    ${cpId}    ${cpName}    ${Infos_returnCode}    ${Info_returnCode}
    ...    ${validTime}=3    ${delay}=0    ${custom_header}=${EMPTY}
    ${request}    Set Variable    {"contentId":"${contentId}","contentName":"${contentName}","cpId":"${cpId}","cpName":"${cpName}"}
    ${response}    Set Variable    {"Infos_returnCode":"${Infos_returnCode}","Info_returnCode":"${Info_returnCode}"}
    ${OrderServInfoReq}    模拟器调用请求包构造    /test/xml/default_utf8    ${validTime}    ${request}    ${response}    ${delay}
    ...    ${custom_header}
    ${OrderServInfoRsp}    模拟器调用请求    ${OrderServInfoReq}
    [Return]    ${OrderServInfoReq}    ${OrderServInfoRsp}

模拟器调用_test_json_customheader接口
    [Arguments]    ${MobNum}    ${UserID}    ${BusiCode}    ${validTime}    ${delay}    ${custom_header}
    ${request}    Set Variable    {"MobNum":"${MobNum}","UserID":"${UserID}"}
    ${response}    Set Variable    {"BusiCode":"${BusiCode}"}
    ${OrderServInfoReq}    模拟器调用请求包构造    /test/json/default_utf8    ${validTime}    ${request}    ${response}    ${delay}
    ...    ${custom_header}
    ${OrderServInfoRsp}    模拟器调用请求    ${OrderServInfoReq}
    [Return]    ${OrderServInfoReq}    ${OrderServInfoRsp}

获取response_body编码
    ${encoding}    Detect Encoding
    [Return]    ${encoding}

模拟器调用_XPATH验证模式
    [Arguments]    ${contentId}    ${contentName}    ${cpId}    ${cpName}    ${Infos_returnCode}    ${Info_returnCode}
    ...    ${validTime}=3    ${delay}=0
    ${request}    Set Variable    {"/Request/apkInfo/contentId":"${contentId}","/Request/apkInfo/contentName":"${contentName}","/Request/apkInfo/cpId":"${cpId}","/Request/apkInfo/cpName":"${cpName}"}
    ${response}    Set Variable    {"Infos_returnCode":"${Infos_returnCode}","Info_returnCode":"${Info_returnCode}"}
    ${OrderServInfoReq}    模拟器调用请求包构造    /test/xml/default_utf8    ${validTime}    ${request}    ${response}    ${delay}
    ...    ${EMPTY}    XPATH    XPATH
    ${OrderServInfoRsp}    模拟器调用请求    ${OrderServInfoReq}
    [Return]    ${OrderServInfoReq}    ${OrderServInfoRsp}
