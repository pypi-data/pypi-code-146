"""
@说明    :动态用户组刷新
@时间    :2019/12/25 下午12:12:24
@作者    :任秋锴
@版本    :1.0
"""

import requests


class cjdgUserGroup:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Host": "bms.chaojidaogou.com",
            "Connection": "keep-alive",
            "Content-Length": "90",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Origin": "http://bms.chaojidaogou.com",
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Referer": "http://bms.chaojidaogou.com/shopguide/book_view.jhtml?topId=140&requestSource=h5",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
            "Cookie": f"JSESSIONID=9AC8A3799D296A8712AE18B059D5B694; Hm_lvt_5e3170920dadcb2f29dfb66f63b9b6aa=1574042672; accessToken={self.token}",
        }

    def get(self, group_id):
        url = "http://bms.chaojidaogou.com/shopguide/groupfindGroupDynamicAttr.jhtml"
        data = {"usergroup.groupId": group_id}
        response = requests.post(url, data=data, headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            return result

    def saveFlush(self, group_id):
        data = self.get(group_id)
        url = "http://bms.chaojidaogou.com/shopguide/groupsaveDynamicGroup.jhtml"
        group = data.get("group")
        orgType = group.get("orgType")
        orgIdTypes = ",".join([f"{k}_{orgType}" for k in group.get("orgMap")])
        data = {
            # "user.orgPath": "null",
            # "user.level1": "NaN",
            # "user.level2": "NaN",
            "user.groupId": group_id,
            "user.userPost": group.get("userPost"),
            "user.ids": group.get("belongOrg"),
            "user.orgIdTypes": orgIdTypes,
            "user.isExeCutive": "1",
            "ge.id": group.get("id"),
            "user.staticGroupId": group.get("staticGroupId"),
            "user.staticGroupName": group.get("staticGroupName"),
            "user.sysUserTagIds": data.get("selecttag"),
            "user.orgType": orgType,
        }
        # print(data)
        response = requests.post(url, data=data, headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            return result


def testcase1():
    group_id = 10917998
    token = "0acae9d8e5e588794b007cd7e7bf8a53_deppon"
    ug = cjdgUserGroup(token)
    print(ug.saveFlush(group_id))
    # print(userGroupFlush(group_id, token))


if __name__ == "__main__":
    testcase1()
    # print(userGroupFlush(group_id, token))
