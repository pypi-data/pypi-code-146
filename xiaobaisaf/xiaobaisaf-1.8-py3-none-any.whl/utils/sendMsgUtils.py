#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/28 23:23
@File  : sendMsgUtils.py
'''
from saf.data.config import *
from saf import Union, request, search

def sendMessage(
        url: str = None,
        msg: dict = None,
        assert_path: str = None,
        assert_value: Union[str, int] = None
):
    '''
    发送消息函数
    :param url:             WebHook的URL地址
    :param msg:             WebHook发送的信息
    :param assert_path:     判断内容的路径
    :param assert_value:    判断内容的值
    :return:
    '''
    if not url and not msg:
        raise ('url或者msg信息不能为空，必填内容！')
    else:
        response = request(
                        method='POST',
                        url=url,
                        headers={'Content-Type': 'application/json'},
                        json=msg
                    )
    if assert_path and assert_value:
        try:
            assert assert_value == search(assert_path, response.json())
        except AssertionError as e:
            raise ('信息发送失败！')

def feishuWebhookSendMessage(msg:str = '本次测试结束'):
    '''
    使用飞书的webhook发送机器人消息
    :param msg:     需要发送的信息内容，
    :return:

    调用飞书机器人发送飞书群消息
    @feishu_help_document = https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN
    '''
    sendMessage(url=feishu.webhook(),
                 msg={
                     'msg_type': 'text',
                     'content': {
                         'text': msg
                     }
                 },
                 assert_path='StatusCode',
                 assert_value=0
    )

def dingdingWebhookSendMessage(msg:str = '本次测试结束'):
    '''
    使用钉钉的webhook发送机器人消息
    :param msg:     需要发送的信息内容，
    :return:

    调用钉钉机器人发送钉钉群消息
    @dingding_help_document = https://open.dingtalk.com/document/group/custom-robot-access
    '''
    sendMessage(url=dingding.webhook(),
                 msg={'msgtype': 'text',
                        'text': {
                         'content': msg
                        }
                 },
                 assert_path='errcode',
                 assert_value=0
    )

def robotSendMessage(robot_name: str= 'feishu', msg: str = '本次测试结束'):
    ''' 统一调用机器人发送消息 '''
    if 'feishu' in robot_name:
        feishuWebhookSendMessage(msg)
    if 'dingding' in robot_name:
        dingdingWebhookSendMessage(msg)