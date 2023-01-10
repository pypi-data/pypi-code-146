# 互动社区
from .base import base


class bbs(base):
    def __init__(self, token):
        super().__init__(token)

    def getTag(self):
        api_name = "bbs/getTagList"
        return self.request(api_name)

    def list(self):
        api_name = "bbs/getActivityList"
        return self.request(api_name)

    def addTopic(self, data):
        api_name = "activity/addTopic"
        return self.request(api_name, data)

    def addBbsForumAndTag(self, imgs=None, context=None):
        api_name = "v2/bbs/addBbsForumAndTag"
        data = {}
        data["imgs"] = imgs
        data["context"] = context
        return self.request(api_name, data)
