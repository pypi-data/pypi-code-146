# 互动社区
from .base import base


class dollyin(base):
    def __init__(self, token):
        super().__init__(token)
        self.lecturer_id = self.get_user_id()

    def get_user_info(self):
        url = "http://sub.chaojidaogou.com/dollyin/api/lecture/getOwnInfo"
        return self.request(url=url)

    def get_user_id(self):
        response = self.get_user_info()
        code = response.get("code")
        if code == 102:
            data = response.get("dataObject")
            lecturer_id = data.get("lecturerId")
            return lecturer_id

    def update_user_info(self, data):
        url = "http://sub.supshop.cn/dollyin/api/lecture/updateLecturer"
        return self.request(url=url, json=data, method="POST")

    def update_user_des(self, lecturer_des):
        # 修改用户简介
        data = {
            "lecturerId": self.lecturer_id,
            "lecturerDes": lecturer_des,
        }
        print(data)
        return self.update_user_info(data)
