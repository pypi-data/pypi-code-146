"""
@说明    :用户岗位
@时间    :2019/12/25 下午12:12:24
@作者    :任秋锴
@版本    :1.0
"""

import requests


class cjdgUserPosition:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Cookie": f"accessToken={self.token}",
        }

    def list(self, page=1, rows=20):
        url = "http://bms.microc.cn/shopguide/positionlist.jhtml"
        params = {
            "page": page,
            "rows": rows,
        }
        response = requests.get(url, params=params, headers=self.headers)
        if response.status_code == 200:
            return response.json()

    def get_all(self,):
        result = []
        page = 1
        page_rows = 100
        while 1:
            response = self.list(page, page_rows)
            rows = response.get("rows")
            result.extend(rows)
            print(f"loading {page:03d}...")
            if len(rows) < page_rows:
                break
            page += 1
        return result


def testcase1():
    token = "8d99dc283797a8e04178f50f642a4ef4_deppon"
    ug = cjdgUserPosition(token)
    for row in ug.get_all():
        print(row)


if __name__ == "__main__":
    testcase1()
