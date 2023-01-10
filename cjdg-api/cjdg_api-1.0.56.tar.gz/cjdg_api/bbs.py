# 互动社区问答
from .base import base


class bbs(base):
    def __init__(self, token):
        super().__init__(token)

    def getTag(self):
        api_name = "bbs/getTagList"
        return self.request(api_name)

    def getQuestList(self):
        api_name = "bbs/getQuestList"
        return self.request(api_name)

    def getQuestuestByNonAnswer(self):
        api_name = "bbs/getQuestList"
        return self.request(api_name)

    def answerQuestion(self):
        api_name = "bbs/getQuestList"
        return self.request(api_name)

    def list(self):
        api_name = "bbs/getActivityList"
        return self.request(api_name)

    def addTopic(self, data):
        api_name = "activity/addTopic"
        return self.request(api_name, data)

    def getBbsForumAndTag(self, interactionType=0, page=1, rows=100, version=1):
        api_name = "v2/bbs/getBbsForumListAndTag"
        data = {}
        data["interactionType"] = interactionType
        data["page"] = page
        data["rows"] = rows
        data["version"] = version
        return self.request(api_name, data)

    def addBbsForumAndTag(self, imgs=None, context=None):
        api_name = "v2/bbs/addBbsForumAndTag"
        data = {}
        data["imgs"] = imgs
        data["context"] = context
        return self.request(api_name, data)

    def addOrDelBbsFavour(self, favourRelId):
        api_name = "bbs/addOrDelBbsFavour"
        data = {}
        data["accessToken"] = self.accessToken
        data["editType"] = 1
        data["favourId"] = 0
        data["favourRelId"] = favourRelId
        data["favourToType"] = 1
        data["favourType"] = 1
        data["relId"] = favourRelId
        return self.request(api_name, data)
