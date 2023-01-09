from .base import base


class activity(base):
    def __init__(self, token):
        super().__init__(token)

    def getTopicList(self, activityId, order=1, onlyShowImg=0, page=1, rows=20):
        api_name = "activity/getTopicList"
        data = {}
        data["activityId"] = activityId
        data["onlyShowImg"] = onlyShowImg
        data["order"] = order
        data["page"] = page
        data["rows"] = rows
        return self.request(api_name, params=data)

    def addLike(self, activityId, floor, replyId):
        api_name = "activity/activityLikeOper"
        data = {}
        data["activityId"] = activityId
        data["floor"] = floor
        data["replyId"] = replyId
        return self.request(api_name, method="POST", json=data)
