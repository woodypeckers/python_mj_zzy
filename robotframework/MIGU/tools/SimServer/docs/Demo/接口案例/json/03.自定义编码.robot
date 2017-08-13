*** Settings ***
Documentation     1）编码的配置，在Mock端是在system.xml的http server节点的encoding进行设置的
...               2）为图简单，文件均采用template中装载，装到RF之后成为unicode，再转换为相应的编码post出去
Library           OperatingSystem
Library           ../../library/jsonLibrary.py
Library           String
Resource          ../../resource/HttpLibrary.HTTP.robot
Resource          ../../resource/NNN接口.robot

*** Test Cases ***
服务端设置编码为utf8(缺省)
    [Documentation]    编码的配置，在Mock端是在system.xml的http server节点的encoding进行设置的
    模拟器调用_test_json_utf8接口    13500000000    中文姓名    0
    ${unicode_request_body}=    OperatingSystem.Get File    Template/utf8.json    encoding=utf-8
    ${custom_headers}=    Create Dictionary    customheader1=12345    customheader2=22345
    custom_post    http://127.0.0.1:10001/test/json/utf8    ${unicode_request_body}    encoding=utf-8    custom_headers=${custom_headers}
    ${encoding}    获取response_body编码
    Should Be Equal As Strings    ${encoding}    UTF-8

服务端未设置编码_兼容utf8
    [Documentation]    Mock的system.xml中，http server如果不配置编码，则缺省按utf-8处理。这样可以兼容以前的Mock V1
    模拟器调用_test_json_default_utf8接口    13500000000    中文姓名    0
    ${unicode_request_body}=    OperatingSystem.Get File    Template/utf8.json    encoding=utf-8
    ${custom_headers}    Create Dictionary    customheader1=12345
    custom_post    http://127.0.0.1:10002/test/json/default_utf8    ${unicode_request_body}    encoding=utf-8    custom_headers=${custom_headers}
    ${encoding}    获取response_body编码
    Should Be Equal As Strings    ${encoding}    UTF-8

服务端设置编码为gbk_包头和包体编码一致
    [Documentation]    目前Mock不对http包头判断，只判断包体的encoding
    模拟器调用_test_json_gbk接口    13500000000    中文姓名    0
    ${unicode_request_body}    OperatingSystem.Get File    Template/gbk.json    encoding=GBK
    ${custom_headers}    Create Dictionary    customheader1=12345    Content-Type=json/text;charset=gbk
    custom_post    http://127.0.0.1:10003/test/json/gbk    ${unicode_request_body}    encoding=gbk    custom_headers=${custom_headers}
    ${encoding}    获取response_body编码
    Should Be Equal As Strings    ${encoding}    GB2312

服务端设置编码为gbk_未指定包头编码
    [Documentation]    目前Mock不对http包头判断，只判断包体的encoding
    模拟器调用_test_json_gbk接口    13500000000    中文姓名    0
    ${unicode_request_body}    OperatingSystem.Get File    Template/gbk.json    encoding=GBK
    ${custom_headers}    Create Dictionary    customheader1=12345    Content-Type=json/text
    custom_post    http://127.0.0.1:10003/test/json/gbk    ${unicode_request_body}    encoding=gbk    custom_headers=${custom_headers}
    ${encoding}    获取response_body编码
    Should Be Equal As Strings    ${encoding}    GB2312

服务端设置编码为UTF-16LE
    [Documentation]    试验用，用charset来指定实际发出的包的编码,可以看出，还是可以指定以UTF-16LE发出的，但是需要在接收端做转码，参见下面：
    ...    datas \ = datas.decode('UTF-16LE').encode('UTF-8'),这样就转成了带BOM的UTF-8格式，可以存盘
    模拟器调用_test_json_utf16le接口    13500000000    中文姓名    0
    ${unicode_request_body}    OperatingSystem.Get File    Template/unicode.json    encoding=UTF-16LE
    ${custom_headers}    Create Dictionary    customheader1=12345    Content-Type= application/json;charset=UTF-16LE
    custom_post    http://127.0.0.1:10004/test/json/unicode    ${unicode_request_body}    encoding=UTF-16LE    custom_headers=${custom_headers}
    ${encoding}    获取response_body编码
    Should Be Equal As Strings    ${encoding}    UTF-16LE

*** Keywords ***
