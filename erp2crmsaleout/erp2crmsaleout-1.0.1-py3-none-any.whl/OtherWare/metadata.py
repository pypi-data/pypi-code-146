import json

from OtherWare.utility import CommUtility


class Save2ERP(CommUtility):
    def __init__(self):
        super(Save2ERP, self).__init__()

    def erp_save(self, app2, api_sdk, option, data, app3):

        api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                           option['app_sec'], option['server_url'])

        for i in data:

            if self.exist_order(api_sdk, i[0]['FGODOWNNO']) != True:

                model = {
                    "Model": {
                        "FID": 0,
                        "FBillNo": str(i[0]['FGODOWNNO']),
                        "FBillTypeID": {
                            "FNUMBER": "QTRKD01_SYS"
                        },
                        "FStockOrgId": {
                            "FNumber": "104"
                        },
                        "FStockDirect": "GENERAL",
                        "FDate": str(i[0]['FBUSINESSDATE']),
                        "FSUPPLIERID": {
                            "FNumber": self.code_conversion(app2, "rds_vw_supplier", "FNAME", i[0]['FSUPPLIERNAME'])
                        },
                        "FDEPTID": {
                            "FNumber": "BM000040"
                        },
                        "FSTOCKERID": {
                            "FNumber": "BSP00040"
                        },
                        "FSTOCKERGROUPID": {
                            "FNumber": "SKCKZ01"
                        },
                        "FOwnerTypeIdHead": "BD_OwnerOrg",
                        "FOwnerIdHead": {
                            "FNumber": "104"
                        },
                        "FNOTE": str(i[0]['FBILLNO']),
                        "FBaseCurrId": {
                            "FNumber": "PRE001"
                        },
                        "FEntity": self.data_splicing(app2, i)
                    }
                }

                save_res = json.loads(api_sdk.Save("STK_MISCELLANEOUS", model))

                if save_res['Result']['ResponseStatus']['IsSuccess']:

                    submit_result = self.ERP_submit(api_sdk, str(i[0]['FGODOWNNO']))

                    if submit_result:

                        audit_result = self.ERP_Audit(api_sdk, str(i[0]['FGODOWNNO']))

                        if audit_result:

                            self.changeStatus(app3, str(i[0]['FGODOWNNO']), "1")

                        else:
                            self.changeStatus(app3, str(i[0]['FGODOWNNO']), "2")
                    else:
                        self.changeStatus(app3, str(i[0]['FGODOWNNO']), "2")
                else:

                    changeStatus(app3, str(i[0]['FGODOWNNO']), "2")

                    print(str(i[0]['FBILLNO']))

                    print(save_res)
