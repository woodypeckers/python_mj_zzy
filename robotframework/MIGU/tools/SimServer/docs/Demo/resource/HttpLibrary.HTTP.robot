*** Settings ***
Documentation     HTTPLibrary库实际是RF对httplib的对象封装，好处是自动加了一堆的log,设置了上下文Context（未来可能用得着）；坏处是需要修改一下py文件，readme中的说法：
...
...               该库缺省时会自己把包体encode(utf-8)
...               需要修改robotframework_httplibrary-0.x.x-py2.7.egg\HttpLibrary\__init__.py中463行
...               def set_request_body(self, body):
...               看一下就知道怎么改了！
...
...               这个Library需要pip install robotframework-httplibrary, \ 中间的封装大部分来源于卓信通项目的封装
Library           HttpLibrary.HTTP
Library           ../library/httpLibrary.py
Library           Collections
Library           String
Library           ../library/robotPatch.py

*** Variables ***
&{http_custom_headers_obj}

*** Keywords ***
创建连接
    [Arguments]    ${host}    ${scheme}=http
    Create Http Context    ${host}    ${scheme}

设置请求包
    [Arguments]    ${body}    ${encoding}=utf-8
    [Documentation]    body采用unicode， encoding是指请求包需要采用的编码方式（缺省utf-8)
    robotPatch.Set Httplibrary Request Encoding    ${encoding}
    Set Request Body    ${body}

设置请求头
    [Arguments]    ${header_name}    ${header_value}
    Set Request Header    ${header_name}    ${header_value}

提交GET请求
    [Arguments]    ${url}
    HttpLibrary.HTTP.GET    ${url}

提交POST请求
    [Arguments]    ${url}
    HttpLibrary.HTTP.POST    ${url}

获取返回包
    ${Response_body}    Get Response Body
    [Return]    ${Response_body}

获取返回包头
    [Arguments]    ${header_name}
    ${Response_header_value}    Get Response Header    ${header_name}
    Run Keyword If    "type(${Response_header_value})"=="type([])"    Return From Keyword
    ${Response_header_value}    Collections.Get From List    ${Response_header_value}    0
    [Return]    ${Response_header_value}

获取响应状态码
    ${Status}    Get Response Status
    [Return]    ${Status}

解析Json串
    [Arguments]    ${json_string}
    log    Parses the JSON document `json_string` and returns a data structure.
    ${result}=    parse Json    ${json_string}
    [Return]    ${result}

获取Json变量值
    [Arguments]    ${json_string}    ${json_pointer}
    log    Get the target node of the JSON document `json_string` specified by `json_pointer`.
    ${value}=    Get Json Value    ${json_string}    ${json_pointer}    #返回为String类型
    [Return]    ${value}

JSON方式解析串
    [Arguments]    ${json_string}
    log    Attempts to parse `json_string` as JSON.
    Should Be Valid Json    ${json_string}

custom_post
    [Arguments]    ${url}    ${request_body}    ${encoding}=utf-8    ${custom_headers}=${EMPTY}
    [Documentation]    对httplibrary.HTTP做一个一元的post的封装
    ...    输入：${url}, &{headers},body, encoding=utf-8
    ...    输出: 直接设置test变量 &{response_headers}, ${response_body}
    ${host}    Get Host By Url    ${url}
    ${uri}    Get Uri By Url    ${url}
    创建连接    ${host}
    ${customs_headers_dict}    Collections.Convert To Dictionary    ${custom_headers}
    @{key_list}    Get Dictionary Keys    ${customs_headers_dict}
    : FOR    ${key}    IN    @{key_list}
    \    ${value}    Get From Dictionary    ${custom_headers}    ${key}
    \    设置请求头    ${key}    ${value}
    设置请求包    ${request_body}    ${encoding}
    提交POST请求    ${uri}
    ${response_body}    获取返回包
    Set Test Variable    ${response_body}
    Set Test Variable    ${custom_headers}
    [Return]    ${response_body}
