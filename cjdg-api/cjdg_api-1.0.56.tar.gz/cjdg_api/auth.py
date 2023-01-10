'''
@说明    :超导角色组相关功能
@时间    :2019/12/25 下午1:02:11
@作者    :任秋锴
@版本    :1.0
'''


'''
@说明    :动态用户组刷新
@时间    :2019/12/25 下午12:12:24
@作者    :任秋锴
@版本    :1.0
'''




import requests
class cjdgAuthRole:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Length": "0",
            "Cookie": f"JSESSIONID=CA5A375A7AD6885FEDAF4F32B3D8837E; Hm_lvt_5e3170920dadcb2f29dfb66f63b9b6aa=1574042672; accessToken={self.token}",
            "Host": "bms.chaojidaogou.com",
            "Origin": "http://bms.chaojidaogou.com",
            "Pragma": "no-cache",
            "Referer": "http://bms.chaojidaogou.com/shopguide/authrole_roleView.jhtml?topId=511&requestSource=h5",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }

    def get(self, group_id):
        url = "http://bms.chaojidaogou.com/shopguide/groupfindGroupDynamicAttr.jhtml"
        data = {
            "usergroup.groupId": group_id
        }
        response = requests.post(url, data=data, headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            return (result)

    def publish(self, auth_role_id):
        url = f"http://bms.chaojidaogou.com/shopguide/assignmentpublishAuthFactByRoleId.jhtml?roleIdStr={auth_role_id}"
        response = requests.get(url, data=None, headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            return (result)


def testcase1():
    # 测试流程是否正常
    auth_role_id = 7830179
    token = "6c24d991339096fe99f4e011d19626e9_deppon"
    ar = cjdgAuthRole(token)
    print(ar.publish(auth_role_id))


if __name__ == "__main__":
    testcase1()
