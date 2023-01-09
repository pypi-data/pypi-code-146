# 排行榜PK

from .base import base


class pk(base):
    def __init__(self, token):
        super().__init__(token)


    # 排行榜PK列表
    def query(self):
        api_name = 'om-web/storemanagement/pk/pk/query'
        return self.request(api_name)


    # 排行榜新增/编辑
    # 配置必填项和主指标
    def save(self):
        api_name = 'om-web/stoermanagement/pk/v2/pk/save'
        return self.request(api_name)


    # 配置其他副指标，非必填项
    def pkIndex(self):
        api_name = 'om-web/storemanagement/pk/pk/saveOrUpdatePkIndex'
        return self.request(api_name)


    # 选择组织/战队
    def player(self):
        api_name = 'om-web/storemanagement/pk/v2/pk/savePlayer'
        return self.request(api_name)



    # 发布
    def public(self):
        api_name = 'om-web/storemanagement/pk/v2/pk/public'
        return self.request(api_name)



    # 查看PK基础信息
    def queryDetail(self):
        api_name = 'om-web/storemanagement/pk/pk/querydetailselectmenber'
        return self.request(api_name)


    # 查看上报明细
    def submitDetail(self):
        api_name = 'om-web/storemanagement/pk/pk/querySubmitDetailList4Backend'
        return self.request(api_name)


    # 删除PK
    def pkdel(self):
        api_name = 'om-web/storemanagement/pk/pk/delete'
        return self.request(api_name)


def main():
    pass

if __name__ == '__main__':
    main()
