"""
# 模块管理
## 模块分类管理
## 模块管理
"""
import requests
from loguru import logger
from .base import base


class appMod(base):
    """
    app模块管理
    """

    def __init__(self, token) -> None:
        super().__init__(token)

    def request(self, **kwarg):
        api_prefix = ""
        headers = {
            "Cookie": f"accessToken={self.token}"
        }
        return super().request(api_prefix=api_prefix,
                               headers=headers,
                               ** kwarg)

    def list(self, mod_code=None, mod_name=None, cate_name=None, mod_type_id=None):
        data = dict(
            page=1,
            rows=100
        )
        if mod_code:
            data["param.modCode"] = mod_code
        if mod_name:
            data["param.modName"] = mod_name
        if cate_name:
            data["param.cateName"] = cate_name
        if mod_type_id:
            data["param.modType"] = mod_type_id
        response = self.request(api_name="appModlist.jhtml",
                                data=data,
                                method="POST")
        rows = response.get("rows")
        if rows:
            return rows

    def get_last_one(self):
        rows = self.list()
        if rows:
            return rows[0]

    def get_last_one_mod_id(self):
        return self.get_last_one().get("appModuleId")

    def create(self, module_name, module_code, cate_id, img_url, disp_order):
        """
        增加模块
        """
        data = {
            "appModules.moduleName": module_name,
            "appModules.moduleCode": module_code,
            "appModules.type": 20,
            "appModules.cate": cate_id,
            "appModules.img": img_url,
            "appModules.moduleFlag": 1,
            "appModules.isShowNew": 1,
            "appModules.dispOrder": disp_order,
        }
        response = self.request(api_name="appModadd.jhtml",
                                data=data,
                                method="POST"
                                )
        return self.get_last_one_mod_id()

    def delete(self, module_id):
        data = {
            "moduleId": module_id,
        }
        response = self.request(api_name="appModdel.jhtml",
                                data=data,
                                method="POST"
                                )
        data["response"] = response
        logger.debug(data)

    def delete_all(self):
        rows = self.list()
        for row in rows:
            module_id = row.get("appModuleId")
            self.delete(module_id=module_id)

    def get_mod_type(self):
        data = {}
        response = self.request(api_name="appModgetAppModType.jhtml",
                                data=data,
                                method="POST"
                                )
        return response

    def get_mod_type_id(self, type_name):
        """
        通过模块类型名称查找类型ID
        """
        for row in self.get_mod_type():
            if type_name == row.get("mTypeName"):
                type_id = row.get("mTypeId")
                return type_id
        logger.error({
            "msg": "找不到模块类型",
            "type_name": type_name,
        })


class appModCat(base):
    """
    模块分类管理
    """

    def __init__(self, token) -> None:
        super().__init__(token)

    def request(self, **kwarg):
        api_prefix = ""
        headers = {
            "Cookie": f"accessToken={self.token}"
        }
        return super().request(api_prefix=api_prefix,
                               headers=headers,
                               ** kwarg)

    def list(self, cate_name=None):
        data = dict(
            page=1,
            rows=100
        )
        response = self.request(api_name="appModmoduleCateList.jhtml",
                                data=data,
                                method="POST")
        rows = response.get("rows")
        if rows:
            if not cate_name:
                return rows
            for row in rows:
                if cate_name == row.get("cate"):
                    return row
        logger.error({
            "msg": "查找不到模块分类",
            "cate_name": cate_name,
        })

    def get_last_one(self):
        rows = self.list()
        if rows:
            return rows[-1]

    def get_last_one_mod_id(self):
        return self.get_last_one().get("id")

    def create(self, cate_name, cate_order):
        """
        增加模块分类

        """
        data = {
            "cateName": cate_name,
            "cateOrder": cate_order,
        }
        response = self.request(api_name="appModmodfiModuleCate.jhtml",
                                data=data,
                                method="POST"
                                )
        info = response.get("info")
        if info == "ok":
            return self.get_last_one_mod_id()
        else:
            data["msg"] = "添加失败"
            data["response"] = response
            logger.error(data)
