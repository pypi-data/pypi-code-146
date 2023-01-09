from .base import base


class globalSearch(base):
    def __init__(self, token):
        super().__init__(token)

    def activity(self, keyWord, page=1):
        api_name = "globalSearchActivity"
        data = {}
        data["keyWord"] = keyWord
        data["page"] = page
        data["type"] = "activity"
        return self.request(api_name)

    def article(self, keyWord, page=1):
        api_name = "globalSearchArticle"
        data = {}
        data["keyWord"] = keyWord
        data["page"] = page
        data["type"] = "article"
        return self.request(api_name)
