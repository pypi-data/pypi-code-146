import datetime

import pandas as pd
from pyrda.dbms.rds import RdClient

from erp2crmsaleout.config import conn1, conn
from sqlalchemy import create_engine


class ERP2CRM():
    def __init__(self):
        # 连接数据库
        new_account = 'mssql+pymssql://{}:{}@{}:{}/{}?charset=utf8'.format(conn1['DB_USER'], conn1['DB_PASS'],
                                                                           conn1['DB_HOST'],
                                                                           conn1['DB_PORT'], conn1['DATABASE'])
        dms_conn = 'mssql+pymssql://{}:{}@{}:{}/{}?charset=utf8'.format(conn['DB_USER'], conn['DB_PASS'],
                                                                        conn['DB_HOST'],
                                                                        conn['DB_PORT'], conn['DATABASE'])
        self.app3 = RdClient(token='9B6F803F-9D37-41A2-BDA0-70A7179AF0F3')
        self.dms_engine = create_engine(dms_conn)
        self.new_engine = create_engine(new_account)
        self.token_china = '9B6F803F-9D37-41A2-BDA0-70A7179AF0F3'
        self.erp_token = "4D181CAB-4CE3-47A3-8F2B-8AB11BB6A227"
        self.app3 = RdClient(token=self.token_china)
        self.app2 = RdClient(token=self.erp_token)

    def get_saleorder(self):
        sql = """
            select FBillNo from RDS_CRM_SRC_saleOrderList where FIsDo = 0
        """
        res = self.app3.select(sql)
        return res

    def ERP2DMS(self):
        """
        将销售出库从ERP写入CRM
        :return:
        """
        res = self.get_saleorder()
        for d in res:
            sql = """
            SELECT DISTINCT
                saleorder.FBILLNO AS salesorder_no,--选择源单
                saleout.FCUSTOMERID,--客户名称
                saleout.FRECCONTACTID,--联系人姓名
                saleout.FCREATEDATE,--创建时间
                saleout.FDELIVERYDEPTID,--发货部门
                st.FNAME AS FSTOCKERGROUPID,--库存组
                saleout.FCARRIAGENO,--运输单号
                saleout.F_SZSP_XSLX AS saletype,--销售类型
                org.FNAME as FSTOCKORGID,--发货组织
                saleout.FDate,--日期
                saleman.FNAME AS FSALESMANID,--负责人
                saleout.FMODIFYDATE,--更新时间
                saleout.FBILLNO,--出库单编号
                saleout.FHEADLOCATIONID,--交货地点
                saleout.FCARRIERID,--承运商
                dep.FNAME AS FSALEORGID,--销售组
                storekeeper.FNAME AS FSTOCKERID,--仓管员
                saleout.FDOCUMENTSTATUS,--审批状态
                soutBaseDetail.FCUSTMATID,--客户物料编号
                materialNo.FNUMBER as FMATERIALID,--物料编号
            -- 	soutdetail.CustMatName,	--客户物料名称
                ut.FNAME AS FUNITID,--库存单位
                soutBaseDetail.FMUSTQTY,--应发数量
                soutBaseDetail.FREALQTY,--实发数量
                soutdetailfree.FISFREE,--是否赠品
                warehouse.FNAME AS FSTOCKID,--仓库
                BillAmount.FBILLALLAMOUNT --价税合计
            FROM
                [dbo].[T_SAL_ORDER] saleorder
                LEFT JOIN T_SAL_DELIVERYNOTICEENTRY detailsInvoice ON saleorder.FBILLNO = detailsInvoice.FSRCBILLNO
                LEFT JOIN T_SAL_DELIVERYNOTICE baseInvoice ON baseInvoice.FID = detailsInvoice.FID
                LEFT JOIN T_SAL_OUTSTOCKENTRY_R soutdetail ON baseInvoice.FBILLNO = soutdetail.FSRCBILLNO
                LEFT JOIN T_SAL_OUTSTOCK saleout ON saleout.FID = soutdetail.FID
                LEFT JOIN T_SAL_OUTSTOCKENTRY soutBaseDetail ON saleout.FID = soutBaseDetail.FID
                LEFT JOIN T_BD_MATERIAL materialNo on materialNo.FMATERIALID = soutBaseDetail.FMATERIALID
                LEFT JOIN T_AR_RECEIVABLEENTRY detailsRec ON detailsRec.FSOURCEBILLNO = saleout.FBILLNO
                LEFT JOIN t_AR_receivable rec ON rec.FID = detailsRec.FID
                LEFT JOIN T_SAL_OUTSTOCKENTRY_F soutdetailfree ON saleout.FID = soutdetailfree.FID
                LEFT JOIN T_SAL_OUTSTOCKFIN BillAmount ON BillAmount.FID = saleout.FID 
                LEFT JOIN rds_vw_organizations org on org.FORGID = saleout.FSTOCKORGID
                left join rds_vw_department dep on dep.FMASTERID = saleout.FSALEDEPTID
                left join crm_vw_stock st on st.FENTRYID = saleout.FSTOCKERGROUPID
                left join rds_vw_storekeeper storekeeper on storekeeper.fmasterid = saleout.FSTOCKERID
                left JOIN rds_vw_unit ut on ut.FUNITID = soutBaseDetail.FUNITID
                LEFT JOIN rds_vw_warehouse warehouse ON warehouse.FMASTERID = soutBaseDetail.FSTOCKID
                LEFT JOIN rds_vw_salesman saleman on saleman.fid = saleout.FSALESMANID
                                where saleorder.FBILLNO = '{}'  and saleout.FBILLNO !='' and saleout.FDOCUMENTSTATUS = 'C'
                     
                """.format(d['FBillNo'])
            # FDOCUMENTSTATUS 单据状态
            data = pd.read_sql(sql, self.new_engine)

            if not data.empty:
                sql = 'select * from RDS_CRM_SRC_saleout where FMODIFYDATE = \'' + str(data['FMODIFYDATE'][0])[
                                                                                   :23] + "'" + "and salesorder_no = '" + \
                      d['FBillNo'] + "'"
                dexist = self.app3.select(sql)
                if not dexist:
                    data.loc[:, 'FIsdo'] = 0
                    data.to_sql('RDS_CRM_SRC_saleout', self.dms_engine, if_exists='append')
                    print(data)
                    sql = "update a set a.FisDo=3 from RDS_CRM_SRC_saleOrderList a where FBillNo = '{}'".format(
                        d['FBillNo'])
                    self.app3.update(sql)
                    self.inser_logging('销售出库', '销售订单为' + f"{d['FBillNo']}",
                                       "该{}销售出库单已保存".format(d['FBillNo']), 1)
                else:
                    self.inser_logging('销售出库', '销售订单为' + f"{d['FBillNo']}",
                                       "该{}销售出库单已经存在与SRC中".format(dexist[0]['FBILLNO']), 2)
                    print("该{}销售出库单已经存在与SRC中".format(dexist[0]['FBILLNO']))
                    sql = "update a set a.FisDo=2 from RDS_CRM_SRC_saleOrderList a where FBillNo = '{}'".format(
                        d['FBillNo'])
                    self.app3.update(sql)
            else:
                self.inser_logging('销售出库', '销售订单为' + f"{d['FBillNo']}",
                                   "{}该销售出库单没有审核或发货通知单没有下推".format(d['FBillNo']), 2)
                print("{}该销售出库单没有审核或发货通知单没有下推".format(d['FBillNo']))
        return {"message": "OK"}

    def inser_logging(self, FProgramName, FNumber, FMessage, FIsdo, FOccurrenceTime=str(datetime.datetime.now())[:19],
                      FCompanyName='CP'):
        app3 = RdClient(token='9B6F803F-9D37-41A2-BDA0-70A7179AF0F3')
        sql = "insert into RDS_CRM_Log(FProgramName,FNumber,FMessage,FOccurrenceTime,FCompanyName,FIsdo) values('" + FProgramName + "','" + FNumber + "','" + FMessage + "','" + FOccurrenceTime + "','" + FCompanyName + "'," + str(
            FIsdo) + ")"
        data = app3.insert(sql)
        return data


if __name__ == '__main__':
    acc = ERP2CRM()
    acc.ERP2DMS()
