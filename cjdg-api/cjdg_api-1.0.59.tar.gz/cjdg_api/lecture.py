# 互动社区
from .base import base


class lecture(base):
    def __init__(self, token):
        super().__init__(token)

    def getVideos(self, tagids, pageSize=100, nowPage=1):
        url = "http://client.supshop.cn/allstar/api/" + "lecture/getVideos"
        data = {
            "tagids": tagids,
            "order": 1,
            "pageSize": pageSize,
            "nowPage": nowPage,
        }
        return self.request(url, data)

    def addUserLike(self, evaType, c_id):
        url = "http://client.supshop.cn/allstar/api/" + "lecture/addUserLike"
        data = {}
        data["evaType"] = evaType
        data["id"] = c_id
        return self.request(url, data)

    def addComment(self, tagids, pageSize=100, nowPage=1):
        url = "http://client.supshop.cn/allstar/api/" + "lecture/addComment"
        data = {}
        data["contentId"] = c_id
        data["cont"] = cont
        return self.request(url, data)
