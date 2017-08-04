*** Settings ***
Library           Selenium2Library
Resource          resources.robot
Resource          Business_key.robot
Library           Screenshot

*** Test Cases ***
添加客户
    [Template]
    [Timeout]    2 minutes
    登录业务逻辑
    Click Element    id=s-menu-1    #电话图标
    Sleep    3s
    Select Frame    id=iframe-1
    Click link    xpath=.//*[@id='mainNavbar']/div[2]/ul/li[4]/a    #客户
    Page Should Contain    ${title}    然之协同
    Sleep    3s
    Select Frame    id=iframe-1
    Click Element    xpath=.//*[@id='menuActions']/a    #添加客户
    等待
    Comment    Select Frame    id=iframe-1
    等待
    Input Text    id=name    南国遗梦
    Input Text    id=contact    渴渴
    Input Text    id=phone    13000000000
    Input Text    id=email    123456@qq.com
    #用SELECT选择--企业股份
    Comment    Select From List    xpath=.//*[@id='type']    股份企业
    Select From List By Label    xpath=.//*[@id='type']    股份企业    #股份企业corporate
    Select From List    xpath=.//*[@id='size']    大型(100人以上)
    #用SELECT选择--意向
    Comment    Select From List    xpath=.//*[@id='status']    意向
    Select From List By Index    id=status    1    #从0开始，意向
    Select From List By Value    xpath=.//*[@id='level']    A    #value=A
    Comment    Select From List    xpath=.//*[@id='level']    A(有明显的业务需求，预计一个月内成交)
    Input Text    xpath=.//*[@id='intension']    购买购买购买
    submit
    Comment    Click Button    id=submit
    等待
    Click Button    id=continueSubmit    #或者下面的confirm action
    Comment    Confirm Action    #已经存在，继续保存

删除客户
    登录业务逻辑
    进入客户列表页面
    Click Link    xpath=.//*[@id='ajaxForm']/table/tbody/tr/td[11]/div/a
    Click Link    xpath=.//*[@id='ajaxForm']/table/tbody/tr/td[11]/div/ul/li[4]/a
    Confirm Action
    等待
    Close All Browsers

添加订单_新建
    登录业务逻辑
    进入订单列表页面
    Click Element    xpath=.//*[@id='menuActions']/a
    Select Checkbox    id=createCustomer
    等待
    Input Text    id=name    新建联系人
    Input Text    id=contact    不困
    Input Text    id=phone    15012345678
    Input Text    id=email    2@2.com
    Input Text    id=qq    10000
    Comment    Click Element    xpath=.//*[@id='product_chosen']/ul    #产品框
    Comment    Click Element    xpath=.//*[@id='product_chosen']/div/ul/li    #选择已有产品
    Select Checkbox    id=createProduct    #产品新建框
    Input Text    id=productName    娃娃
    Input Text    id=code    xin001
    Select From List By Value    id=currency    usd
    Input Text    name=plan    77777
    submit

添加订单_选择已有
    登录业务逻辑
    进入订单列表页面
    Click Element    xpath=.//*[@id='menuActions']/a
    Select Checkbox    id=createCustomer
    等待
    Unselect Checkbox    id=createCustomer
    Comment    Select From List    xpath=.//*[@id='customer_chosen']/a
    Click Element    xpath=//*[@id="customer_chosen"]/a    #客户框
    Click Element    xpath=.//*[@id="customer_chosen"]/div/ul/li    #需要先选择下拉框，然后定位元素
    等待
    Click Element    xpath=.//*[@id='product_chosen']/ul    #产品框
    Click Element    xpath=.//*[@id='product_chosen']/div/ul/li    #选择产品    #通过层级自己去找，手写，选择
    Select From List By Label    name=currency    美元
    Input Text    id=plan    8888
    submit

删除订单
    登录业务逻辑
    Click Element    id=s-menu-1    #电话图标
    Sleep    3s
    Select Frame    id=iframe-1
    Click Element    xpath=.//*[@id='mainNavbar']/div[2]/ul/li[2]/a
    Click Element    xpath=html/body/div[2]/div[2]/table/tbody/tr[1]/td[11]/div/a
    Click Element    xpath=html/body/div[2]/div[2]/table/tbody/tr[1]/td[11]/div/ul/li[4]/a
    Choose Ok On Next Confirmation
    Confirm Action

添加合同
    登录业务逻辑
    进入合同列表页面
    Click Element    xpath=.//*[@id='menuActions']/a
    Click Element    xpath=.//*[@id='customer_chosen']/a    #先选择下拉框
    Click Element    xpath=//*[@id='customer_chosen']/div/ul/li[2]    #再选
    等待
    Select From List By Index    xpath=.//*[@id='orderTD']/div/span[1]/select    1
    Input Text    id=code    hetong001
    Click Element    id=contact
    Select From List By Value    id=contact    5
    Click Element    xpath=.//*[@id='signedBy_chosen']/a
    Click Element    xpath=.//*[@id='signedBy_chosen']/div/ul/li
    Input Text    id=signedDate    2017-08-02
    Input Text    id=begin    2017-08-03
    Input Text    id=end    2018-08-06
    Click Element    xpath=//*[@id="handlers_chosen"]/ul
    Click Element    xpath=//*[@id="handlers_chosen"]/div/ul/li
    Input Text    xpath=/html/body    主要条款
    Comment    \    name=files[]    \    #上传附件,windows控件
    submit

*** Keywords ***
登录业务逻辑放template
    打开浏览器    ${base_url}
    输入用户名    ${user_name}
    输入密码    ${password}
    登录后验证    ${title}
    等待
    ${file1}=    Capture Page Screenshot
    File Should Exist    ${OUTPUTDIR}${/}selenium-screenshot-1.png
