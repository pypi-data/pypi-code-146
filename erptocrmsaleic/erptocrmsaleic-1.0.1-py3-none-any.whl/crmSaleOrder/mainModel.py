import datetime

from pyrda.dbms.rds import RdClient
from k3cloud_webapi_sdk.main import K3CloudApiSdk
from crmSaleOrder import utility as ut
from crmSaleOrder import metadata as mt
from crmSaleOrder import operation as db
from crmSaleOrder.src_crm_saleorder import CrmToDms


def salesOrder():
    '''
    函数入口
    :param startDate:
    :param endDate:
    :return:
    '''

    app2 = RdClient(token='4D181CAB-4CE3-47A3-8F2B-8AB11BB6A227')
    app3 = RdClient(token='9B6F803F-9D37-41A2-BDA0-70A7179AF0F3')

    data = db.getCode(app3)

    if data:
        res = ut.classification_process(app3, data)

        api_sdk = K3CloudApiSdk()

        # 测试账套
        option1 = {
            "acct_id": '63310e555e38b1',
            "user_name": '杨斌',
            "app_id": '240072_1e2qRzvGzulUR+1vQ6XK29Tr2q28WLov',
            # "app_sec": 'd019b038bc3c4b02b962e1756f49e179',
            "app_sec": '224f05e7023743d9a0ab51d3bf803741',
            "server_url": 'http://cellprobio.gnway.cc/k3cloud',
        }

        # # 新账套
        #
        # option1 = {
        #     "acct_id": '62777efb5510ce',
        #     "user_name": 'DMS',
        #     "app_id": '235685_4e6vScvJUlAf4eyGRd3P078v7h0ZQCPH',
        #     # "app_sec": 'd019b038bc3c4b02b962e1756f49e179',
        #     "app_sec": 'b105890b343b40ba908ed51453940935',
        #     "server_url": 'http://cellprobio.gnway.cc/k3cloud',
        # }

        result = mt.ERP_Save(api_sdk=api_sdk, data=res, option=option1, app2=app2, app3=app3)
        return result
    else:
        ret_dict = {
            "code": "0",
            "message": "没有销售订单数据",
        }
        return ret_dict


def run():
    token_erp = '9B6F803F-9D37-41A2-BDA0-70A7179AF0F3'
    app3 = RdClient(token=token_erp)
    c = CrmToDms()
    FDate = str(datetime.datetime.now())[:10]
    c.sale_order_to_dms(app3, FDate)
    c.get_saleorder()
    res = salesOrder()
    return res
run()