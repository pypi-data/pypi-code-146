'''
@说明    :用于超级导购的PUSH消息管理
@时间    :2019/12/23 下午8:51:02
@作者    :任秋锴
@版本    :1.0
'''
import requests
from .base import base


class cjdgPushSms(base):
    '''
    流程：1，添加消息。2，添加用户。3，发送。
    example 向用户发送：
    >>> sms = cjdgPushSms("00a405fd489d85d36096cff8f1a63dd3_gltjd")
    >>> infoId = sms.addPushInfo(content, pushInfoId, title, info_type=4)
    >>> sms.addUser(infoId, user_id)
    >>> sms.sendOutInfo(infoId)

    example 向用户组发送：
    >>> sms = cjdgPushSms("00a405fd489d85d36096cff8f1a63dd3_gltjd")
    >>> infoId = sms.addPushInfo(content, pushInfoId, title, info_type=4)
    >>> sms.addGroup(infoId, group_id)
    >>> sms.sendOutInfo(infoId)
    '''

    def __init__(self, token, app_secret=None):
        super().__init__(token, app_secret)

    def addPushInfo(self, content, pushInfoId, title, info_type=4):
        # 添加消息信息
        # info_type:0:文本，1：文章，2：课程，4：外部素材
        api_name = "push/addPushInfo"
        data = {
            "type": info_type,
            "title": title,
            "pushInfoId": pushInfoId,
            "content": content,
            "isTimed": "0",
        }
        result = self.request(api_name, data)
        code = result.get("code")
        if code == 102:
            infoId = result.get("dataObject")
            return infoId

    def addUser(self, infoId, objRelIds):
        # 添加用户ID
        api_name = "push/addUser"
        data = {
            "infoId": infoId,
            "objRelIds": objRelIds,
        }
        return (self.request(api_name, data))

    def addGroup(self, infoId, objRelIds):
        # 添加用户组ID
        api_name = "push/addGroup"
        data = {
            "infoId": infoId,
            "objRelIds": objRelIds,
        }
        return self.request(api_name, data)

    def sendOutInfo(self, infoId):
        api_name = "push/sendOutInfo"
        data = {
            "infoId": infoId,
        }
        return (self.request(api_name, data))

