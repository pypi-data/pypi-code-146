import requests
from loguru import logger


class cjdgLearnPath:
    def __init__(self, token):
        self.token = token

    def request(self, api_name, method="GET", **kwargs):
        host_name = "https://sub.chaojidaogou.com/learn_path/api/"
        url = f"{host_name}{api_name}"
        params = kwargs.get("params", {})
        params["accessToken"] = self.token
        response = requests.request(method=method, url=url, **kwargs)
        if response.status_code == 200:
            return self.response(response.json())
        else:
            logger.error(
                {
                    "msg": "status code 不正确。",
                    "status_code": response.status_code,
                }
            )

    def response(self, response_raw):
        return response_raw

    def learningPath(
        self, pathStatus="published", checkAuth=False, pageSize=10, nowPage=1
    ):
        api_name = "learningPath"
        data = {
            "pathStatus": pathStatus,
            "checkAuth": checkAuth,
            "pageSize": pageSize,
            "nowPage": nowPage,
        }
        kwargs = {}
        kwargs["params"] = data
        return self.request(api_name=api_name, method="GET", **kwargs)

    def LearningPathClass(
        self, pathStatus="published", checkAuth=False, pageSize=10, nowPage=1
    ):
        api_name = "LearningPathClass"
        data = {
            "pathStatus": pathStatus,
            "checkAuth": checkAuth,
            "pageSize": pageSize,
            "nowPage": nowPage,
        }
        kwargs = {}
        kwargs["params"] = data
        return self.request(api_name=api_name, method="GET", **kwargs)


class cjdgLearningPathOverview(cjdgLearnPath):
    def __init__(self, token):
        super().__init__(token)

    def learningProgress(self, pathId, pageSize=10, nowPage=1,learnStatus=None):
        api_name = "learningPathOverview/learningProgress"
        data = {
            "pathId": pathId,
            "pageSize": pageSize,
            "nowPage": nowPage,
        }
        if learnStatus:
            data["learnStatus"] = learnStatus
        kwargs = {}
        kwargs["params"] = data
        return self.request(api_name=api_name, method="GET", **kwargs)