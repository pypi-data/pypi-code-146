#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/20 22:29
@File  : config.py
'''
import hashlib
import time

class feishu(object):
    @staticmethod
    def webhook():
        ''' 飞书webhook的地址 '''
        return 'https://open.feishu.cn/open-apis/bot/v2/hook/xxxx'

class dingding(object):
    @staticmethod
    def webhook():
        ''' 钉钉webhook的地址 '''
        return 'https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxx'

class email(object):
    @staticmethod
    def smtpServer():
        ''' smtp服务器IP或者域名
        163邮箱：http://help.163.com/09/1223/14/5R7P3QI100753VB8.html
        QQ邮箱：https://service.mail.qq.com/cgi-bin/help?subtype=1&id=28&no=369
        '''
        return 'smtp.163.com'

    @staticmethod
    def smtpPort():
        ''' smtp端口： '''
        return 25

    @staticmethod
    def username():
        ''' 邮箱登录账户 '''
        return 'username'

    @staticmethod
    def password():
        ''' 授权码，163和QQ的不是登录密码 '''
        return 'password'

    @staticmethod
    def isSSL():
        ''' 是否使用安全隧道 '''
        return False

class zenTao(object):
    '''
    参考禅道接口文档：
    https://www.zentao.net/book/zentaopmshelp/integration-287.html
    '''
    @staticmethod
    def baseURL():
        ''' 禅道的根路径 '''
        return 'http://192.168.254.133/zentao'

    @staticmethod
    def account():
        ''' 后台-》二次开发-》应用-》免密登录的账户名 '''
        return 'admin'

    @staticmethod
    def getCode():
        ''' 后台-》二次开发-》应用-》创建-》代号 '''
        return 'xbkj'

    @staticmethod
    def getKey():
        ''' 后台-》二次开发-》应用-》创建-》密钥 '''
        return ''

    @staticmethod
    def getTime():
        ''' 获取时间戳 '''
        return int(time.time())

    @staticmethod
    def getToken():
        ''' 获取token： md5($code + $key + $time) '''
        _md5 = hashlib.md5(f'{zenTao.getCode()}{zenTao.getKey()}{zenTao.getTime()}'.encode('utf-8'))
        return _md5.hexdigest()

class Jira(object):
    @staticmethod
    def server_url():
        return ''

    @staticmethod
    def username():
        return ''

    @staticmethod
    def password():
        return ''

class browser(object):
    @staticmethod
    def name():
        ''' 浏览器名称： chrome 或 firefox 或 ie '''
        return 'chrome'

class log(object):
    @staticmethod
    def path():
        ''' 日志存储的路径 '''
        return '.'

    @staticmethod
    def name():
        ''' 日志文件名 '''
        return 'auto_info_{time}.log'

    @staticmethod
    def rotation():
        ''' 日志存储规则：50 MB 或者 1 days '''
        return '1 days'