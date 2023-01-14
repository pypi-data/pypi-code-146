import datetime
from urllib import parse

import pandas as pd
import pymysql
from k3cloud_webapi_sdk.main import K3CloudApiSdk
from pyrda.dbms.rds import RdClient
from sqlalchemy import create_engine

bad_password1 = 'rds@2022'
conn2 = {'DB_USER': 'dms',
         'DB_PASS': parse.quote_plus(bad_password1),
         'DB_HOST': '58.211.213.34',
         'DB_PORT': 1433,
         'DATABASE': 'AIS20220926102634',
         }
bad_password2 = 'rds@2022'
conn3 = {'DB_USER': 'sa',
         'DB_PASS': parse.quote_plus(bad_password2),
         'DB_HOST': '139.224.232.93',
         'DATABASE': 'cprds',
         }
option = {
    "acct_id": '63310e555e38b1',
    "user_name": '杨斌',
    "app_id": '240072_1e2qRzvGzulUR+1vQ6XK29Tr2q28WLov',
    # "app_sec": 'd019b038bc3c4b02b962e1756f49e179',
    "app_sec": '224f05e7023743d9a0ab51d3bf803741',
    "server_url": 'http://cellprobio.gnway.cc/k3cloud',
}


class ERPTOCrm():
    def __init__(self):
        # 连接数据库
        erp_conn = 'mssql+pymssql://{}:{}@{}:{}/{}?charset=utf8'.format(conn2['DB_USER'], conn2['DB_PASS'],
                                                                        conn2['DB_HOST'],
                                                                        conn2['DB_PORT'], conn2['DATABASE'])
        test_conn = 'mssql+pymssql://{}:{}@{}:{}/{}?charset=utf8'.format(conn3['DB_USER'], conn3['DB_PASS'],
                                                                         conn3['DB_HOST'],
                                                                         1433, conn3['DATABASE'])
        self.crm_con = pymysql.connect(host='123.207.201.140', database='ldcrm', user='lingdang', port=33306,
                                       password='lingdangcrm123!@#')
        self.new_cursor = self.crm_con.cursor(cursor=pymysql.cursors.DictCursor)
        self.dms_engine = create_engine(erp_conn)
        self.test_engine = create_engine(test_conn)

    def get_products(self, FDate):
        sql = f"""
        select *
        from rds_crm_material where FVarDateTime > '{FDate}'
        """
        df = pd.read_sql(sql, self.dms_engine)
        return df

    def getFinterId(self, app3, tableName):
        '''
        在两张表中找到最后一列数据的索引值
        :param app2: sql语句执行对象
        :param tableName: 要查询数据对应的表名表名
        :return:
        '''

        sql = "select isnull(max(FInterId),0) as FMaxId from " + tableName
        res = app3.select(sql)

        return res[0]['FMaxId']

    def proto_crm(self, app3, FData):
        df_pro = self.get_products(FData)
        mater_lis = app3.select('select FNumber from RDS_CRM_SRC_MaterialDetail')
        material_lis = []
        for i in mater_lis:
            material_lis.append(i['FNumber'])
        if not df_pro.empty:
            for i, r in df_pro.iterrows():
                if r['FNumber'] not in material_lis:
                    if r['FDOCUMENTSTATUS'] == 'C':
                        find_sql = "select * from RDS_CRM_SRC_MaterialDetail where FNumber = '{}'".format(r['FNumber'])
                        dexist = app3.select(find_sql)
                        if not dexist:
                            try:
                                df_pro['FIsdo'] = 0
                                lis_m = list(r)
                                lis_m.append(0)
                                res = pd.DataFrame(lis_m, index=df_pro.columns).T
                                res.to_sql('RDS_CRM_SRC_MaterialDetail', self.test_engine, if_exists='append',
                                           index=False)
                                print(r['FNAME'] + "该物料保存成功")
                            except:
                                self.inser_logging(app3, '基础物料ERP保存到CRM', f"{r['FNumber']}",
                                                   f"{r['FNumber']}该基础物料数据异常,清检查该条数据")
                                print(f"{r['FNumber']}该基础物料数据异常,清检查该条数据")
                        else:
                            self.inser_logging(app3, '基础物料ERP保存到CRM', f"{r['FNumber']}", f"{r['FNumber']}该基础物料数据已存在")
                            print("{}该基础物料数据已存在".format(r['FNumber']))

                    else:
                        self.inser_logging(app3, '基础物料ERP保存到CRM', f"{r['FNumber']}", f"{r['FNumber']}该基础物料数据未批准")
                        print("{}该基础物料数据未批准".format(r['FNumber']))
                else:
                    if r["FNumber"] != None:
                        sub_sql = f"""select FNumber from RDS_CRM_SRC_MaterialDetail where FNumber = '{r['FNumber']}' and FVarDateTime = '{r['FVarDateTime']}' and FIsDo !=1
                                       """
                        try:
                            dexist = app3.select(sub_sql)
                            if not dexist:
                                del_sql = "delete from RDS_CRM_SRC_MaterialDetail where FNumber = '" + str(
                                    r['FNumber']) + "'"
                                app3.delete(del_sql)
                                sql1 = f"""insert into RDS_CRM_SRC_MaterialDetail(FInterId,FDeptId,FUserId,FApplyOrgName,FVarDateTime,FNumber,FName,FSpecification,FDescription,FTaxRateId,FGROSSWEIGHT,FNETWEIGHT,FLENGTH,FWIDTH,FVOLUME,FHEIGHT,FSafeStock,FMinPackCount,FPlanningStrategy,FOrderPolicy,FFixLeadTime,FVarLeadTime,FOrderIntervalTimeType,FOrderIntervalTime,FMaxPOQty,FMinPOQty,FIncreaseQty,FEOQ,FVarLeadTimeLotSize,FFinishReceiptOverRate,FFinishReceiptShortRate,FMinIssueQty,FISMinIssueQty,FIsBatchManage,FOverControlMode,FIsKFPeriod,FMaterialGroup,FTaxCategoryCodeId,FWEIGHTUNITID,FBaseUnitId,FVOLUMEUNITID,F_SZSP_Assistant,Fisdo,FOldNumber,FIsPurchase,FExpUnit,FExpPeriod,FMinStock,FMaxStock) values
                                                               ({self.getFinterId(app3, 'RDS_CRM_SRC_MaterialDetail') + 1},'{r['FDeptID']}','{r['FUserId']}','{r['FApplyOrgName']}','{str(r['FVarDateTime'])}','{r['FNumber']}','{r['FNAME']}','{r['FSPECIFICATION']}','{r['FDescription']}','{r['FTaxRateId']}','{r['FGROSSWEIGHT']}','{r['FNETWEIGHT']}','{r['FLENGTH']}','{r['FWIDTH']}','{r['FVOLUME']}','{r['FHEIGHT']}','{r['FSafeStock']}','{r['FMinPackCount']}','{r['FPlanningStrategy']}','{r['FOrderPolicy']}','{r['FFixLeadTime']}','{r['FVarLeadTime']}','{r['FOrderIntervalTimeType']}','{r['FOrderIntervalTime']}','{r['FMaxPOQty']}','{r['FMinPOQty']}','{r['FIncreaseQty']}','{r['FEOQ']}','{r['FVarLeadTimeLotSize']}','{r['FFinishReceiptOverRate']}','{r['FFinishReceiptShortRate']}','{r['FMINISSUEQTY']}','{r['FISMINISSUEQTY']}','{r['FISBATCHMANAGE']}','{r['FOVERCONTROLMODE']}','{r['FISKFPERIOD']}','{r['FMATERIALGROUP']}','{r['FTAXCATEGORYCODEID']}','{r['FWEIGHTUNITID']}','{r['FBASEUNITID']}','{r['FVOLUMEUNITID']}','{r['F_SZSP_ASSISTANT']}',0,'{r['FOldNumber']}',{r['FISPURCHASE']},'{r['FEXPUNIT']}',{r['FEXPPERIOD']},{r['FMINSTOCK']},{r['FMAXSTOCK']})"""
                                app3.insert(sql1)
                                print("{}该客户数据已更新".format(r['FNumber']))

                        except:
                            self.inser_logging(app3, '基础物料ERP保存到CRM', r["FNumber"], r["FNumber"] + '该物料数据异常')
                            print(f"{r['FNumber']}此该物料数据异常,无法存入SRC,请检查数据")
        else:
            self.inser_logging(app3, '基础物料ERP保存到CRM', "", f"没有查询到物料")
            print("没有查询到物料")

    def inser_logging(self, app3, FProgramName, FNumber, FMessage, FOccurrenceTime=str(datetime.datetime.now())[:19],
                      FCompanyName='CP'):
        lis = []
        lis.append([FProgramName, FNumber, FMessage,FOccurrenceTime,FCompanyName])
        df = pd.DataFrame(lis,columns=['FProgramName','FNumber','FMessage','FOccurrenceTime','FCompanyName'])
        df.to_sql('RDS_CRM_Log',self.test_engine,index=False,if_exists='append')
        # sql = "insert into RDS_CRM_Log(FProgramName,FNumber,FMessage,FOccurrenceTime,FCompanyName) values('" + FProgramName + "','" + FNumber + "','" + FMessage + "','" + FOccurrenceTime + "','" + FCompanyName + "')"
        # data = app3.insert(sql)
        return df



