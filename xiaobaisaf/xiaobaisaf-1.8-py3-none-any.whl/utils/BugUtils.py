#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/28 23:25
@File  : zenTao.py
'''
from saf.data.config import *
from saf import Session, Union
import datetime
from jira import JIRA

session = Session()

def loginZenTao():
    ''' 禅道的免密登录，使用session模式登录 '''
    global session
    # 创建应用免密模式
    url = f'{zenTao.baseURL()}/api.php?m=user&f=apilogin&account={zenTao.account()}&code={zenTao.getCode()}&time={zenTao.getTime()}&token={zenTao.getToken()}'
    session.get(url)

def loginJira():
    return JIRA(server=Jira.server_url(), basic_auth=(Jira.username(), Jira.password()))

def addJiraBug(project_key, summary, description, project_id, assignee_name):
    jira_user = loginJira()
    jira_user.create_issue({
        'project': {'key': project_key},
        'summary': summary,  # 'BUG的标题',
        'description': description,  # 'BUG的备注信息',
        'issuetype': {'id': project_id},   # 'issuetype': {'name': 'Bug'}  BUG的类型
        'assignee': {'name': assignee_name},  # 指派人的账户
        'customfield_11100': {'value': project_id}
    })

def addZenTaoBUG(product: int = 1,
                branch: int = '',
                module: int = '',
                title: str = f'BUG标题-{int(time.time())}',
                openedBuild: Union[int, str] = 'trunk',
                execution: int = 0,
                assignedTo: str = '',
                deadline: datetime.date = datetime.date.today() + datetime.timedelta(3),  # 为期3天
                feedbackBy: str = '',
                type: str = '',
                os_name: str = '',
                browser: str = '',
                color: str = '',
                serverity: int = 3,
                pri: int = 3,
                steps: str = '',
                story: int = '',
                task: int = '',
                mailto: str = '',
                keywords: str = ''
                ):
    '''
    禅道提BUG单
    :param product          : 所属产品ID *必填
    :param branch           : 分支/平台
    :param module           : 所属模块
    :param title            : Bug标题 *必填
    :param openedBuild      : 影响版本 *必填
    :param execution        : 所属执行 为0
    :param assignedTo       : 指派给
    :param deadline         : 截止日期 日期格式：YY-mm-dd，如：2022-08-28
    :param type             : Bug类型 取值范围： | codeerror | config | install | security | performance | standard | automation | designdefect | others
    :param os_name          : 操作系统 取值范围： | all | windows | win10 | win8 | win7 | vista | winxp | win2012 | win2008 | win2003 | win2000 | android | ios | wp8 | wp7 | symbian | linux | freebsd | osx | unix | others
    :param browser          : 浏览器 取值范围： | all | ie | ie11 | ie10 | ie9 | ie8 | ie7 | ie6 | chrome | firefox | firefox4 | firefox3 | firefox2 | opera | oprea11 | oprea10 | opera9 | safari | maxthon | uc | other
    :param color            : 标题颜色 颜色格式：#RGB，如：#3da7f5
    :param serverity        : 严重程度 取值范围：1 | 2 | 3 | 4
    :param pri              : 优先级 取值范围：0 | 1 | 2 | 3 | 4
    :param steps            : 重现步骤
    :param story            : 需求ID
    :param task             : 任务ID
    :param mailto           : 抄送给 填写帐号，多个账号用','分隔。
    :param keywords         : 关键词
    :return:

    帮助文档：https://www.zentao.net/book/zentaopmshelp/integration-287.html
    '''
    loginZenTao()
    add_bug_url = f'{zenTao.baseURL()}/bug-create-{product}-{branch}-moduleID={module}.json?tid=h96emyim'
    payload = f"------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"product\"\r\n\r\n{product}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"module\"\r\n\r\n{module}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"project\"\r\n\r\n1\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"execution\"\r\n\r\n{execution}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"openedBuild[]\"\r\n\r\n{openedBuild}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"assignedTo\"\r\n\r\n{assignedTo}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"deadline\"\r\n\r\n{str(deadline)}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"feedbackBy\"\r\n\r\n{feedbackBy}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"notifyEmail\"\r\n\r\n\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"type\"\r\n\r\n{type}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"os\"\r\n\r\n{os_name}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"browser\"\r\n\r\n{browser}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"title\"\r\n\r\n{title}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"color\"\r\n\r\n{color}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"severity\"\r\n\r\n{serverity}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"pri\"\r\n\r\n{pri}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"steps\"\r\n\r\n{steps}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"story\"\r\n\r\n{story}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"task\"\r\n\r\n{task}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"oldTaskID\"\r\n\r\n0\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"mailto[]\"\r\n\r\n{mailto}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"keywords\"\r\n\r\n{keywords}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"status\"\r\n\r\nactive\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"issueKey\"\r\n\r\n\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"labels[]\"\r\n\r\n\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"files[]\"\r\n\r\n\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"uid\"\r\n\r\n\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"case\"\r\n\r\n0\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"caseVersion\"\r\n\r\n0\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"result\"\r\n\r\n0\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"testtask\"\r\n\r\n0\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs--".encode(
        'UTF-8')
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryRWJBJ0CsyWBBWFKs',
        'Referer': f'{zenTao.baseURL()}/bug-create-{product}-{branch}-moduleID={module}.json?tid=h96emyim',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63',
        'X-Requested-With': 'XMLHttpRequest'
    }
    session.post(url=add_bug_url, headers=headers, data=payload)


def view_bug(id: int = 1):
    loginZenTao()
    view_bug_url = f'{zenTao.baseURL()}/bug-view-{id}.json?tid=gz3p07qa'
    session.get(url=view_bug_url)