from requests.api import delete
from ..base import base
from loguru import logger


class collocation(base):
    def __init__(self, token):
        super().__init__(token)

    def list(self, page=1, rows=10):
        api_name = "goods/collocation/list"
        data = {
            "page": page,
            "rows": rows,
        }
        return self.request(api_name, params=data)

    def all(self,):
        page_num = 1
        page_size = 200
        while 1:
            response = self.list(page=page_num, rows=page_size)
            rows = response.get("dataObject").get("list")
            for row in rows:
                yield row
            if len(rows) < page_size:
                break
            page_num += 1
            # break

    def info(self, collocationId):
        api_name = "goods/collocation/info"
        data = {
            "collocationId": collocationId
        }
        return self.request(api_name, params=data)




