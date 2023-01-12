'''
@Author  :   顾一龙
@Time    :   2022/06/27 12:35:38
@Version :   1.0
@Contact :   小爷怕什么就做什么，就是那么拽！
'''
# Hard to write shit mountain.......

import json
from cjdg_api.base import base, request_accesstoken


class cjdgGoods(base):
    def __init__(self, token, app_secret=None):
        super().__init__(token, app_secret)

    def list(self, accounts, code=None, name=None, barCode=None):
        api_name = "open/fab/goods/list"
        """
        根据条件查询货品资料列表
        accounts	企业账号
        code	货品编码
        name	货品名称
        barCode	货品条码
        """
        data = {
            "code": code,
            "accounts": accounts
        }
        if name:
            data["name"] = name
        if barCode:
            data["barCode"] = barCode
        return self.request(api_name, json=data)

    def get_code(self, accounts, code):
        api_name = "open/fab/goods/getByCode"
        """
        code:商品编码
        根据货品code获取货品资料详情
        """
        data = {
            "accounts": accounts,
            "code": code
        }
        return self.request(api_name, json=data)

    def edit(self, accounts, cateId, name, code, barCode, img, tagPrice, firmAttrId, val):
        api_name = "open/fab/goods/edit"
        """
        cateId	品类id
        name	商品名称
        code	商品编码
        barCode	商品条码
        img	商品图片
        tagPrice	吊牌价（单位：元）
        attrs	商品附加属性（json字符串）
        [{‘firmAttrId’:’val’}]
        编辑货品资料
        """
        data = {
            "accounts": accounts,
            "cateId": cateId,
            "name": name,
            "code": code,
            "barCode": barCode,
            "img": img,
            "tagPrice": tagPrice,
            "attrs": [{
                'firmAttrId': firmAttrId,
                'val': val
            }]

        }
        return self.request(api_name=api_name, json=data, method="POST")

    def delete(self, accounts, code):
        api_name = "open/fab/goods/del"
        """
        删除货品
        code	商品编码
        """
        data = {
            "accounts": accounts,
            "code": code

        }
        return self.request(api_name, json=data)

    def add(self, data):
        api_name = "open/fab/goods/add"
        """
        新增商品
        accounts  企业账号
        cateId	品类id
        name	商品名称
        code	商品编码
        tagPrice	吊牌价（单位：元）
        attrs	商品附加属性（json字符串）
        [{‘firmAttrId’:’val’}]

        """

        return self.request(api_name=api_name, json=data, method="POST")

    def addPics(self, accounts, code, picUrls):
        api_name = "open/fab/goods/img/addPics"
        """
        code	商品编码
        picUrls	商品图片地址集合，逗号分隔  [照片是url的形式]
        上传货品
        """
        data = {
            "accounts": accounts,
            "code": code,
            "picUrls": picUrls
        }
        return self.request(api_name=api_name, json=data, method="POST")

    def addBarCode(self, accounts, code, barCode):
        api_name = "open/fab/goods/barcode/addBarCode"
        """
        code	商品编码
        barCode	商品条码
        添加商品条码
        """
        data = {
            "accounts": accounts,
            "code": code,
            "barCode": barCode
        }
        return self.request(api_name=api_name, json=data, method="POST")

    def config_list(self, data):
        api_name = "open/goods/attr/config/list"
        """
        # 获取配置的商品属性列表
        # accounts  企业管理员
        page	当前页(默认1)
        rows	每页条数（默认15）

        """
        return self.request(api_name, json=data)

    def getCates(self, accounts, cateName, cateType):
        api_name = "open/goods/cate/getCates"
        """
        # 获取分类列表
        # accounts
        cateType	分类类型
        1:大类;2:中类；3:小类
        cateName	分类名称
        page	当前页(默认1)
        rows	每页条数（默认15）
        """
        data = {
            "accounts": accounts,
            "cateType": cateType,
            "cateName": cateName,
        }
        return self.request(api_name, json=data)

    def get_attr_list(self):
        """
        属性配置- all查询
        """
        api_name = "fab/goods/attr/list"
        data = {
            "accessToken": self.token
        }
        return self.request(api_name, json=data)

    def get_attr_attrName_list(self, attrName):
        """
        属性配置- 根据名称查询
        """
        api_name = "fab/goods/attr/list"
        data = {
            "attrName": attrName,
            "accessToken": self.token
        }
        return self.request(api_name, json=data)

    def add_attr(self, attrName=str, attrCode=str) -> str:
        api_name = "fab/goods/attr/save"
        """
        # 新增商品属性配置
        attrName : 配置名
        attrCode : 配置编码
        """
        data = {
            "attrName": attrName,
            "attrCode": attrCode,
            "accessToken": self.token
        }
        return self.request(api_name=api_name, json=data, method="POST")

    def updata_attr(self, attrId, isEnable=int):
        api_name = "fab/goods/attr/update"
        """
        # 禁用和启用
        isEnable   1 是启用
        isEnable   2 是禁用
        attrId 配置 id

        """
        data = {"attrId": attrId, "isEnable": isEnable}
        return self.request(api_name=api_name, json=data, method="POST")

    def save_Goods_FAB(self, goodId):
        api_name = "goods/saveGoodsFAB"
        """
        生成FAb
        goodsIds: 1031682681
        accessToken:
        """
        data = {
            "goodsIds": goodId,
            "accessToken": self.token

        }
        return self.request(api_name=api_name, json=data, method="POST")
    #  商品搭配

    def collocation_list(self, page, rows):
        """
        1. 商品搭配：全部列表

        """
        api_name = "goods/collocation/list"
        data = {
            "page": page,
            "rows": rows,
            "accessToken": self.token
        }

        return self.request(api_name=api_name, json=data)

    def collocation_namecode_list(self, nameCode, page, rows):
        """
        1. 商品搭配：根据名字查询

        """
        api_name = "goods/collocation/list"
        data = {
            "nameCode": nameCode,
            "page": page,
            "rows": rows,
            "accessToken": self.token
        }

        return self.request(api_name=api_name, json=data)

    def collocation_fab_list(self, name, code):
        """
        1. 新增商品搭配的关联商品的FA
        CODE  商品编码
        NAME  商品名称
        两个进行搜索
        """
        api_name = "fab/list"
        data = {
            "accessToken": self.token
        }
        if name:
            data["code"] = code
        if code:
            data["name"] = name
        return self.request(api_name=api_name, json=data)

    def add_collocation(self, name, describle, imgDetail, remarks, fabIds):
        """
        1. 新增：商品搭配：

        """
        api_name = "goods/collocation/add"
        data = {
            "collocationId": "",
            "name": name,
            "describle": describle,
            "imgDetail": imgDetail,
            "remarks": remarks,
            "fabIds": fabIds,
            "accessToken": self.token
        }

        return self.request(api_name=api_name, json=data, method="POST")

    def endit_collocation(self, collocationId, name, describle, imgDetail, remarks, fabIds):
        """
        1. 编辑：商品搭配：

        """
        api_name = "goods/collocation/add"
        data = {
            "collocationId": collocationId,
            "name": name,
            "describle": describle,
            "imgDetail": imgDetail,
            "remarks": remarks,
            "fabIds": fabIds,
            "accessToken": self.token
        }

        return self.request(api_name=api_name, json=data, method="POST")

    def del_collocation(self, collocationIds):
        """
        删除商品搭配
        """
        api_name = "goods/collocation/del"
        data = {
            "collocationIds": collocationIds,
            "accessToken": self.token
        }
        return self.request(api_name=api_name, json=data)


def gyl():
    acc, pwd = "shysuser@shys", "123456"
    asc = "78135e71c6a9caf9702d0061c41bd4ab"
    token = request_accesstoken(acc, pwd)


if __name__ == '__main__':
    gyl()
