import json


class CommUtility():
    def ERP_Audit(self, api_sdk, FNumber):
        '''
        将订单审核
        :param api_sdk: API接口对象
        :param FNumber: 订单编码
        :return:
        '''

        model = {
            "CreateOrgId": 0,
            "Numbers": [FNumber],
            "Ids": "",
            "InterationFlags": "",
            "NetworkCtrl": "",
            "IsVerifyProcInst": "",
            "IgnoreInterationFlag": "",
        }

        res = json.loads(api_sdk.Audit("STK_AssembledApp", model))

        return res['Result']['ResponseStatus']['IsSuccess']

    def getSubEntityCode(self, app2, FNumber):
        '''
        获得子件信息
        :return:
        '''

        sql = f"select * from RDS_ECS_ODS_ASS_STORAGEACCT where FBillNo='{FNumber}'"

        res = app2.select(sql)

        return res

    def data_splicing(self, app3, FNumber):
        '''
        将订单内的物料进行遍历组成一个列表，然后将结果返回给 FSaleOrderEntry
        :param data:
        :return:
        '''

        d_lis = []
        data = self.getSubEntityCode(app3, FNumber)
        for i in data:
            d_lis.append(self)

        return list

    def json_model(self, app2, i):
        '''
        子件数据模型
        :param app2:
        :param i:
        :return:
        '''
        model = {
            "FMaterialIDSETY": {
                "FNumber": self.code_conversion(app2, "rds_vw_material", "F_SZSP_SKUNUMBER", i['FItemNumber'])
            },
            # "FUnitIDSETY": {
            #     "FNumber": "01"
            # },
            "FQtySETY": str(i['Fqty']),
            "FStockIDSETY": {
                "FNumber": "SK01"
            },
            "FStockLocIdSETY": {
                "FSTOCKLOCIDSETY__FF100002": {
                    "FNumber": "SK01"
                }
            },
            "FStockStatusIDSETY": {
                "FNumber": "KCZT01_SYS"
            },
            "FLOTSETY": {
                "FNumber": str(i['Flot'])
            },
            # "FBaseUnitIDSETY": {
            #     "FNumber": "01"
            # },
            "FKeeperTypeIDSETY": "BD_KeeperOrg",
            "FKeeperIDSETY": {
                "FNumber": "104"
            },
            "FOwnerTypeIDSETY": "BD_OwnerOrg",
            "FOwnerIDSETY": {
                "FNumber": "104"
            },
            "FProduceDateSETY": str(i['FPRODUCEDATE']) if self.iskfperiod(app2, i['FItemNumber']) == '1' else "",
            "FEXPIRYDATESETY": str(i['FEFFECTIVEDATE']) if self.iskfperiod(app2, i['FItemNumber']) == '1' else "",
        }

        return model

    def changeStatus(self, app3, fnumber, status):
        '''
        将没有写入的数据状态改为2
        :param app2: 执行sql语句对象
        :param fnumber: 订单编码
        :param status: 数据状态
        :return:
        '''

        sql = f"update a set a.FIsdo={status} from RDS_ECS_ODS_DISASS_DELIVERY a where FBillNo='{fnumber}'"

        app3.update(sql)

    def code_conversion(self, app2, tableName, param, param2):
        '''
        通过ECS物料编码来查询系统内的编码
        :param app2: 数据库操作对象
        :param tableName: 表名
        :param param:  参数1
        :param param2: 参数2
        :return:
        '''

        sql = f"select FNumber from {tableName} where {param}='{param2}'"

        res = app2.select(sql)

        if res == []:

            return ""

        else:

            return res[0]['FNumber']

    def iskfperiod(self, app2, FNumber):
        '''
        查看物料是否启用保质期
        :param app2:
        :param FNumber:
        :return:
        '''

        sql = f"select FISKFPERIOD from rds_vw_fiskfperiod where F_SZSP_SKUNUMBER='{FNumber}'"

        res = app2.select(sql)

        if res == []:

            return ""

        else:

            return res[0]['FISKFPERIOD']

    def check_order_exists(self, api_sdk, FNumber):
        '''
        查看订单是否在ERP系统存在
        :param api: API接口对象
        :param FNumber: 订单编码
        :return:
        '''

        model = {
            "CreateOrgId": 0,
            "Number": FNumber,
            "Id": "",
            "IsSortBySeq": "false"
        }

        res = json.loads(api_sdk.View("STK_AssembledApp", model))

        return res['Result']['ResponseStatus']['IsSuccess']

    def ERP_submit(self, api_sdk, FNumber):
        model = {
            "CreateOrgId": 0,
            "Numbers": [FNumber],
            "Ids": "",
            "SelectedPostId": 0,
            "NetworkCtrl": "",
            "IgnoreInterationFlag": ""
        }

        res = json.loads(api_sdk.Submit("STK_AssembledApp", model))

        return res['Result']['ResponseStatus']['IsSuccess']

    def getCode(self,app3):
        '''
        查询出表中的编码
        :param app2:
        :return:
        '''

        sql = "select FBillNo,Fseq,Fdate,FDeptName,FItemNumber,FItemName,FItemModel,FUnitName,Fqty,FStockName,Flot,Fnote,FPRODUCEDATE,FEFFECTIVEDATE,FSUMSUPPLIERLOT,FAFFAIRTYPE,FIsdo from RDS_ECS_ODS_DISASS_DELIVERY where FIsdo=0"

        res = app3.select(sql)

        return res

    def exist_order(self,api_sdk, FNumber):
        '''
        查看订单是否存在
        :param api_sdk:
        :param FNumber:
        :return:
        '''
        model = {
            "CreateOrgId": 0,
            "Number": FNumber,
            "Id": "",
            "IsSortBySeq": "false"
        }

        res = json.loads(api_sdk.View("STK_MISCELLANEOUS", model))

        return res['Result']['ResponseStatus']['IsSuccess']