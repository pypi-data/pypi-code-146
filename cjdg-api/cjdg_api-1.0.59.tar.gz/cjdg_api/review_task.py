'''
@Author  :   顾一龙 
@Time    :   2022/12/14 22:37:13
@Version :   1.0
@Contact :   世界那么大，你不想走走吗
'''
# Hard to write shit mountain.......
#  检核任务
from cjdg_open_api.base import baseApi


class reviewTask(baseApi):
    def __init__(self, token, app_secret=None):
        super().__init__(token, app_secret)

    def list(self):
        api_name = f"enter/superguide/inspection/task/list"
        data = {"pageNum": 1, "pageSize": 10, "queryParameter": {"name": ""}}
        return self.request(api_name, data)

    # 根据name查询任务
    def list_name(self, name):
        api_name = f"enter/superguide/inspection/task/list"
        data = {"pageNum": 1, "pageSize": 10, "queryParameter": {"name": name}}
        return self.request(api_name, data)
#  失效任务

    def inspection(self, id):
        api_name = "enter/superguide/inspection/task/invalid"
        data = {"data": id}
        return self.request(api_name, data)

# 删除任务
    def delete(self, id):
        api_name = "enter/superguide/inspection/task/delete"
        data = {"data": [id]}
        return self.request(api_name, data)

# 查看任务
    def findBizCount(self, id):
        api_name = "enter/userCenter/extension/openBizSelect/findBizCount"
        data = {"bizType": "INSPECTION", "bizId": id,
                "bizSubType": "INSPECTED_USER", "temporaryId": ""}
        return self.request(api_name, data)

# 数据查看
    def findBizCount(self, taskId):
        api_name = "enter/superguide/inspection/feedback/details"
        data = {"pageNum": 1, "pageSize": 10,
                "queryParameter": {"taskId": taskId}}
        return self.request(api_name, data)


# 检核任务新增好麻烦啊。

    def add(self, taskId):
        api_name = "enter/superguide/inspection/feedback/details"
        data = {"pageNum": 1, "pageSize": 10,
                "queryParameter": {"taskId": taskId}}
        return self.request(api_name, data)
