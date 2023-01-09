from .base import base


class articles(base):
    def __init__(self, token):
        super().__init__(token)

    def getById(self, articleId):
        api_name = "contmgn/getArticleById"
        data = {}
        data["articleId"] = articleId
        return self.request(api_name)

    def addComment(self, articleId, content, stren=0):
        api_name = "contmgn/addComment"
        data = {}
        data["articleId"] = articleId
        data["content"] = content
        data["stren"] = stren
        return self.request(api_name, data)

    def getCommentListByArticleId(self, articleId,  page=1, row=20):
        api_name = "contmgn/getCommentListByArticleId"
        data = {}
        data["articleId"] = articleId
        data["page"] = page
        data["rows"] = rows
        return self.request(api_name, data)

    def addPraiseNum(self, articleId):
        api_name = "contmgn/addPraiseNum"
        data = {}
        data["articleId"] = articleId
        return self.request(api_name, data)

    def addReplyPraise(self, targetId, articleId):
        api_name = "contmgn/addReplyPraise"
        data = {}
        data["favourToType"] = 3
        data["favourType"] = 2
        data["targetId"] = targetId
        data["targetParentId"] = articleId
        return self.request(api_name, data)
