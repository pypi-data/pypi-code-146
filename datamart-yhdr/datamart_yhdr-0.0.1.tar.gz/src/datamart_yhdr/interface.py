import requests

from datamart_yhdr.settings import const


class DMInterface:
    def __init__(self, username: str, password: str):
        """
        初始化银河德睿数据平台接口对象
        :param username: 用户名
        :param password: 密码
        """
        self.username = username
        self.password = password
        self.token = self.get_token()

    def get_token(self):
        """
        用于获取数据平台接口授权
        :return: 接口授权
        """
        token_params = {
            "username": self.username,
            "password": self.password,
            "workspace": const.WORKSPACE
        }
        token_url = const.HALO_URL
        token = requests.post(token_url, json=token_params, timeout=5)
        if "success" in token.json():
            if not token.json()["success"]:
                raise ConnectionError("请求失败，请检查用户名与密码。")
            else:
                access_token = token.json()["value"]["accessToken"]
        else:
            raise ConnectionError("请求失败，请检查网络环境。")
        return access_token

    def get_query(self, query: str, **kwargs):
        """
        用于获取数据
        :param query: 查询接口名称
        :param kwargs: 用于自定义其他传参
            args: dict ->接口内部传参，存在部分参输必填的情况
            limit: int ->设置获取条数，sql接口默认返回10条，传参为limit=-1时返回全部
            offset: int ->跳过条数，默认不跳过
        :return: List[dict]
        """
        data = []
        query_params = {"code": query}
        query_params.update(kwargs)
        get_query = requests.post(const.QUERY_URL, headers={'Authorization': self.token}, json=query_params).json()
        if "success" in get_query:
            if not get_query["success"]:
                raise ConnectionError("请求失败，请检查入参，入参设置方式详见数据接口支持列表说明。")
        if "data" in get_query:
            data.extend(get_query["data"])
        if "value" in get_query:
            data.extend(get_query["value"])
        return data


if __name__ == '__main__':
    print(const.QUERY_URL)
