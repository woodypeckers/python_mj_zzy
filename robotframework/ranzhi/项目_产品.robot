*** Settings ***
Library           Selenium2Library
Resource          resources.robot
Resource          Business_key.robot
Library           Screenshot

*** Test Cases ***
登录和退出
    登录业务逻辑
    退出

创建项目
    [Setup]    登录业务逻辑
    [Template]
    #新建一个项目
    Click Link    XPath=.//*[@id='mainNavbar']/div/ul[2]/li[3]/a    #点击项目
    Select Frame    id=iframe-dashboard    #点击创建项目
    #Click Link    #XPath=.//*[@id='createButton']/i    #创建项目    #？？？
    #Click Element    id=createButton    #？？？
    Click Link    id=createButton
    Sleep    3s
    Input Text    name=name    三世因果循环不失    #u"三世因果循环不失"
    Select From List    id=manager    admin    #负责人
    #Input Text    id=manager_chosen    admin    #负责人
    Select From List    id=member    admin    #团队
    Click Element    XPath=.//*[@id='begin']    #点击开始日期
    Click Element    XPath=html/body/div[3]/div[3]/table/tbody/tr[5]/td[4]    #选择开始时间
    Click Element    id=end    #结束日期
    #Click Element    XPath=html/body/div[4]/div[3]/table/tbody/tr[5]/td[5]    #选择七月28号    #OK
    Click Element    XPath=html/body/div[4]/div[3]/table/thead/tr[1]/th[3]/i    #点击右边箭头
    Click Element    XPath=html/body/div[4]/div[3]/table/tbody/tr[5]/td[6]    #选择九月30号
    Select Frame    xpath=.//*[@id='ajaxForm']/table/tbody/tr[6]/td/div/div[2]/iframe    #???输入项目描述为何不行
    Input Text    xpath=/html/body    项目描述
    Unselect Frame
    Select Frame    id=iframe-dashboard
    Select Checkbox    id=whitelist1
    Select Checkbox    id=whitelist2
    submit
    Comment    Click Button    id=submit
    Close Browser
    [Teardown]

删除项目
    [Setup]
    登录业务逻辑
    Click Link    XPath=.//*[@id='mainNavbar']/div/ul[2]/li[3]/a    #点击项目
    Select Frame    id=iframe-dashboard
    Click Element    xpath=html/body/div[1]/div/table/tbody/tr[1]/td[9]/a[5]    #按位置删除
    Comment    Choose Cancel On Next Confirmation    #弹窗--取消
    Set Browser Implicit Wait    3s
    Confirm Action    #弹窗--确定
    Close All Browsers
    [Teardown]

增加产品_海绵宝宝
    #批量添加，如何for循环，产品名称list化
    登录业务逻辑
    Click Element    id=s-menu-1    #电话图标
    等待
    Select Frame    id=iframe-1
    Click link    xpath=.//*[@id='mainNavbar']/div[2]/ul/li[7]/a    #产品
    Click link    xpath=.//*[@id='menuActions']/a    #添加产品
    Input Text    id=name    海绵宝宝
    Input Text    id=code    baobao001
    Select From List    id=line
    Select From List By Index    id=type    0    #实体类
    Select From List By Value    id=status    normal
    submit

删除产品_海绵宝宝
    登录业务逻辑
    Click Element    id=s-menu-1    #电话图标
    Set_Browser_Implicit_Wait    3s    #智能等待
    Select Frame    id=iframe-1
    Click link    xpath=.//*[@id='mainNavbar']/div[2]/ul/li[7]/a    #产品
    Click link    xpath=.//*[@id='productList']/tbody/tr/td[8]/a[2]    #删除
    Confirm Action

维护产品线_增加
    #批量添加，如何for循环，产品名称list化
    登录业务逻辑
    Click Element    id=s-menu-1    #电话图标
    等待
    Select Frame    id=iframe-1
    Click link    xpath=.//*[@id='mainNavbar']/div[2]/ul/li[7]/a    #产品
    Click link    xpath=html/body/div[2]/div[2]/div[1]/div[2]/a    #维护产品线
    等待
    Click Element    xpath=.//*[@id='ajaxForm']/div/table/tbody/tr[2]/td[3]/a/i    #+
    等待
    Click Element    xpath=.//*[@id='ajaxForm']/div/table/tbody/tr[3]/td[3]/a[2]/i    #-
    Input Text    id=values[]    动漫手办
    submit

增加_删除_蟹黄堡
    [Setup]    登录业务逻辑
    #批量添加，如何for循环，产品名称list化
    Click Element    id=s-menu-1    #电话图标
    等待
    Select Frame    id=iframe-1
    Click link    xpath=.//*[@id='mainNavbar']/div[2]/ul/li[7]/a    #产品
    Click link    xpath=.//*[@id='menuActions']/a    #添加产品
    Input Text    id=name    蟹黄堡
    Input Text    id=code    baobao002
    Select From List    id=line
    Select From List By Index    id=type    0    #实体类
    Select From List By Value    id=status    normal
    submit
    [Teardown]    删除

*** Keywords ***
删除
    等待
    Click link    xpath=.//*[@id='productList']/tbody/tr/td[8]/a[2]    #删除
    等待
    Confirm Action
