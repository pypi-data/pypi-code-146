# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 21:45:59 2022

@author: akshay.bhutada@zeno.health

@Purpose: To populate table wh-inventory-ss that takes daily snapshot of warehouse inventory
"""

import os
import sys
import argparse
import datetime
import pandas as pd

sys.path.append('../../../..')

from dateutil.tz import gettz
from zeno_etl_libs.db.db import DB, MSSql
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.helper import helper

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description
        ="Populates table wh-inventory-ss that takes daily snapshot of warehouse inventory.")
    parser.add_argument('-e', '--env',
                        default="dev", type=str, required=False)
    parser.add_argument('-et', '--email_to',
                        default="vivek.sidagam@zeno.health,akshay.bhutada@zeno.health",
                        type=str, required=False)
    args, unknown = parser.parse_known_args()
    env = args.env
    os.environ['env'] = env
    email_to = args.email_to

    err_msg = ''

    logger = get_logger()
    logger.info("Script begins")

    cur_date = datetime.datetime.now(tz=gettz('Asia/Kolkata'))
    status = False

    try:
        # MSSql connection
        mssql = MSSql(connect_via_tunnel=False)
        mssql_connection = mssql.open_connection()
        # RS Connection
        rs_db = DB()
        rs_db.open_connection()
        q1 = """
        Select * FROM (select
            199 as wh_id,
            b.code as wms_drug_code,
            b.Barcode as drug_id,
            a2.Altercode as distributor_id,
            a2.Name as distributor_name,
            a.Acno as wms_distributor_code,
            a.Vdt as purchase_date,
            b.name as drug_name,
            a.Srate as srate,
            coalesce(a.TQty, 0) as total_quantity,
            case
                when a.Vno < 0 then 0
                else coalesce(a.bqty, 0)
            end as balance_quantity,
            case
                when a.Vno > 0 then 0
                else coalesce(a.tqty, 0)
            end as locked_quantity,
            coalesce(a.TQty * a.cost, 0) as total_value,
            case
                when a.Vno < 0 then 0
                else coalesce(a.bqty * a.cost, 0)
            end as balance_value,
            case
                when a.Vno > 0 then 0
                else coalesce(a.tqty * a.cost, 0)
            end as locked_value,
            a.Evdt as expiry,
            b.Compname as company_name,
            b.Compcode as company_code,
            b.Pack as pack,
            a.Cost as purchase_rate,
            a.Pbillno as purchase_bill_no,
            a.Psrlno as purchase_serial_no,
            a.Batch as batch_number,
            a.mrp as mrp,
            b.Prate as prate,
            m.name as "drug_type",
            s.name as "composition",
            a.Gdn2 as godown_qty,
            a.BQty - a.Gdn2 as store_qty,
            sp.NetAmt invoice_net_amt,
            sp.Taxamt invoice_tax_amt,
            sp.Disamt invoice_dis_amt,
            sp.qty as invoice_qty,
            sp.cgst,
            sp.sgst,
            sp.igst,
            a.vno,
            b.MinQty as shelf_min,
            b.MaxQty as shelf_max
        from
            fifo a with (nolock)
        right join item b with (nolock) on
            a.itemc = b.code
        left join Acm a2 with (nolock) on
            a2.code = a.Acno
            and a2.Slcd in ('SL', 'GL')
        left join Master m with (nolock) on
            b.ItemCat = m.code
        left join Salt s with (nolock) on
            b.Saltcode = s.Code
        left join SalePurchase2 sp with (nolock) on
            a.Pbillno = sp.Pbillno
            and a.Psrlno = sp.Psrlno
            and a.Itemc = sp.Itemc
            and sp.Vdt = a.Vdt
        where
            b.code > 0
            and
             (a.Psrlno in (
	            select
		        Psrlno
	                from
		        Esdata.dbo.salepurchase2 s2)
		or a.Psrlno IN (SELECT sp2.Psrlno from   Esdata2122.dbo.SalePurchase2 sp2 
		))  and b.Barcode not like '%[^0-9]%') a
		Where a."vno"!=0 and (a."balance_quantity"+a."locked_quantity")>0
        """
        logger.info("getting data from esdata1 tables")
        bhw = pd.read_sql(q1, mssql_connection)
        logger.info("Data pulled from esdata1 tables")

        # MSSql2 connection
        mssql2 = MSSql(connect_via_tunnel=False, db='Esdata_WS_2')
        mssql2_connection = mssql2.open_connection()
        q2 = """
        Select * FROM (select
            343 as wh_id,
            b.code as wms_drug_code,
            b.Barcode as drug_id,
            a2.Altercode as distributor_id,
            a2.Name as distributor_name,
            a.Acno as wms_distributor_code,
            a.Vdt as purchase_date,
            b.name as drug_name,
            a.Srate as srate,
            coalesce(a.TQty, 0) as total_quantity,
            case
                when a.Vno < 0 then 0
                else coalesce(a.bqty, 0)
            end as balance_quantity,
            case
                when a.Vno > 0 then 0
                else coalesce(a.tqty, 0)
            end as locked_quantity,
            coalesce(a.TQty * a.cost, 0) as total_value,
            case
                when a.Vno < 0 then 0
                else coalesce(a.bqty * a.cost, 0)
            end as balance_value,
            case
                when a.Vno > 0 then 0
                else coalesce(a.tqty * a.cost, 0)
            end as locked_value,
            a.Evdt as expiry,
            b.Compname as company_name,
            b.Compcode as company_code,
            b.Pack as pack,
            a.Cost as purchase_rate,
            a.Pbillno as purchase_bill_no,
            a.Psrlno as purchase_serial_no,
            a.Batch as batch_number,
            a.mrp as mrp,
            b.Prate as prate,
            m.name as "drug_type",
            s.name as "composition",
            a.Gdn2 as godown_qty,
            a.BQty - a.Gdn2 as store_qty,
            sp.NetAmt invoice_net_amt,
            sp.Taxamt invoice_tax_amt,
            sp.Disamt invoice_dis_amt,
            sp.qty as invoice_qty,
            sp.cgst,
            sp.sgst,
            sp.igst,
            a.vno,
            b.MinQty as shelf_min,
            b.MaxQty as shelf_max
        from
            fifo a with (nolock)
        right join item b with (nolock) on
            a.itemc = b.code
        left join Acm a2 with (nolock) on
            a2.code = a.Acno
            and a2.Slcd in ('SL', 'GL')
        left join Master m with (nolock) on
            b.ItemCat = m.code
        left join Salt s with (nolock) on
            b.Saltcode = s.Code
        left join SalePurchase2 sp with (nolock) on
            a.Pbillno = sp.Pbillno
            and a.Psrlno = sp.Psrlno
            and a.Itemc = sp.Itemc
            and sp.Vdt = a.Vdt
        where
            b.code > 0
            and a.Psrlno in (
            select
                Psrlno
            from
                SalePurchase2)
            and b.Barcode not like '%[^0-9]%') b 
            Where b."vno"!=0 and (b."balance_quantity"+b."locked_quantity")>0
        """
        logger.info("getting data from esdata2 tables")
        gaw = pd.read_sql(q2, mssql2_connection)
        logger.info("Data pulled from esdata2 tables")


        # MSSql3 connection
        mssql3 = MSSql(connect_via_tunnel=False, db='Esdata_TEPL')
        mssql3_connection = mssql3.open_connection()
        q3 = """
             Select * FROM ( select
                  342 as wh_id,
                  b.code as wms_drug_code,
                  b.Barcode as drug_id,
                  a2.Altercode as distributor_id,
                  a2.Name as distributor_name,
                  a.Acno as wms_distributor_code,
                  a.Vdt as purchase_date,
                  b.name as drug_name,
                  a.Srate as srate,
                  coalesce(a.TQty, 0) as total_quantity,
                  case
                      when a.Vno < 0 then 0
                      else coalesce(a.bqty, 0)
                  end as balance_quantity,
                  case
                      when a.Vno > 0 then 0
                      else coalesce(a.tqty, 0)
                  end as locked_quantity,
                  coalesce(a.TQty * a.cost, 0) as total_value,
                  case
                      when a.Vno < 0 then 0
                      else coalesce(a.bqty * a.cost, 0)
                  end as balance_value,
                  case
                      when a.Vno > 0 then 0
                      else coalesce(a.tqty * a.cost, 0)
                  end as locked_value,
                  a.Evdt as expiry,
                  b.Compname as company_name,
                  b.Compcode as company_code,
                  b.Pack as pack,
                  a.Cost as purchase_rate,
                  a.Pbillno as purchase_bill_no,
                  a.Psrlno as purchase_serial_no,
                  a.Batch as batch_number,
                  a.mrp as mrp,
                  b.Prate as prate,
                  m.name as "drug_type",
                  s.name as "composition",
                  a.Gdn2 as godown_qty,
                  a.BQty - a.Gdn2 as store_qty,
                  sp.NetAmt invoice_net_amt,
                  sp.Taxamt invoice_tax_amt,
                  sp.Disamt invoice_dis_amt,
                  sp.qty as invoice_qty,
                  sp.cgst,
                  sp.sgst,
                  sp.igst,
                  a.vno,
                  b.MinQty as shelf_min,
                  b.MaxQty as shelf_max
              from
                  fifo a with (nolock)
              right join item b with (nolock) on
                  a.itemc = b.code
              left join Acm a2 with (nolock) on
                  a2.code = a.Acno
                  and a2.Slcd in ('SL', 'GL')
              left join Master m with (nolock) on
                  b.ItemCat = m.code
              left join Salt s with (nolock) on
                  b.Saltcode = s.Code
              left join SalePurchase2 sp with (nolock) on
                  a.Pbillno = sp.Pbillno
                  and a.Psrlno = sp.Psrlno
                  and a.Itemc = sp.Itemc
                  and sp.Vdt = a.Vdt
              where
                  b.code > 0
                  and a.Psrlno in (
                  select
                      Psrlno
                  from
                      SalePurchase2)
                  and b.Barcode not like '%[^0-9]%') c
                Where c."vno"!=0 and (c."balance_quantity"+c."locked_quantity")>0
              """
        logger.info("getting data from esdata3 tables")
        tepl = pd.read_sql(q3, mssql3_connection)
        logger.info("Data pulled from esdata3 tables")



        df1 = pd.concat([bhw, gaw,tepl])

        # getting safety stock data
        doi_query = """
        select
            doi."store-id" as "wh_id",
            doi."drug-id" as "drug_id",
            doi."safe-stock" as "reorder_point",
            doi.min as "safety_stock",
            doi.max as "order_upto_point",
            'NA' as bucket,
            'NA' as history_bucket,
            'NA' as category
        from
            "prod2-generico"."prod2-generico"."drug-order-info" doi
        left join "prod2-generico"."prod2-generico".drugs d on
            doi."drug-id" = d.id
        where
            "store-id" in (199, 343, 342)
            and d."company-id" != 6984
        union 
        select
            doid."store-id" as "wh_id",
            doid."drug-id" as "drug_id",
            doid."safe-stock" as "reorder_point",
            doid.min as "safety_stock",
            doid.max as "order_upto_point",
            'NA' as bucket,
            'NA' as history_bucket,
            'NA' as category
        from
            "prod2-generico"."prod2-generico"."drug-order-info-data" doid
        left join "prod2-generico"."prod2-generico".drugs d on
            doid."drug-id" = d.id
        where
            doid."store-id" in (199, 343, 342)
            and d."company-id" = 6984 
        """
        logger.info("Getting data from RS")
        doi_data = rs_db.get_df(doi_query)
        logger.info("Data pulled from RS")
        # doi_data.columns = doi_data.columns.str.decode("utf-8")
        doi_data.columns = [c.replace('-', '_') for c in doi_data.columns]

        wh_portfolio_query = """
            select
                "drug-id"
            from
                "prod2-generico"."wh-sku-subs-master" wssm
            left join "prod2-generico".drugs d on
                wssm."drug-id" = d.id
            where
                wssm."add-wh" = 'Yes'
                and d."type" not in ('discontinued-products', 'banned')
        """
        wh_portfolio = rs_db.get_df(wh_portfolio_query)
        wh_portfolio.columns = [c.replace('-', '_') for c in wh_portfolio.columns]
        wh_portfolio["in_wh_portfolio"] = 1

        wh_portfolio['drug_id'] = wh_portfolio['drug_id'].astype(str)

        wh_inventory = df1.merge(wh_portfolio, on="drug_id", how='outer')

        wh_inventory['in_wh_portfolio'] = wh_inventory['in_wh_portfolio'].fillna(0).astype(int)

        wh_inventory['wh_id']=wh_inventory['wh_id'].fillna(199)

        wh_inventory[['wms_drug_code','distributor_id','wms_distributor_code','company_code','vno']]=\
            wh_inventory[['wms_drug_code','distributor_id','wms_distributor_code','company_code','vno']].fillna(-1)

        # merging two data sets
        doi_data['drug_id'] = doi_data['drug_id'].astype(str)
        wh_inventory = wh_inventory.merge(doi_data, on=['drug_id', 'wh_id'], how='left')

        wh_inventory[['bucket','history_bucket','category']].fillna('NA', inplace=True)

        wh_inventory.dtypes

        wh_inventory[['safety_stock','reorder_point','order_upto_point','shelf_min',
                      'shelf_max','invoice_qty'
                      ]].fillna(0, inplace=True)
        wh_inventory['snapshot_date'] = cur_date.strftime("%Y-%m-%d %H:%M:%S")
        wh_inventory['created-at'] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime(
            "%Y-%m-%d %H:%M:%S")
        wh_inventory['created-by'] = 'etl-automation'
        wh_inventory['updated-by'] = 'etl-automation'
        wh_inventory['updated-at'] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime(
            "%Y-%m-%d %H:%M:%S")

        wh_inventory[['total_quantity', 'balance_quantity', 'locked_quantity', 'total_value',
                      'balance_value', 'locked_value','safety_stock', 'reorder_point', 'order_upto_point', 'shelf_min',
                      'shelf_max', 'invoice_qty','godown_qty','store_qty','srate','purchase_serial_no'
                      ]]=wh_inventory[['total_quantity', 'balance_quantity', 'locked_quantity', 'total_value',
                      'balance_value', 'locked_value','safety_stock', 'reorder_point', 'order_upto_point', 'shelf_min',
                      'shelf_max', 'invoice_qty','godown_qty','store_qty','srate','purchase_serial_no'
                      ]].fillna(0)

        wh_inventory.dtypes


        # Writing data
        wh_inventory[['wh_id', 'wms_drug_code','drug_id','wms_distributor_code',
                      'company_code','purchase_serial_no',
                      'safety_stock','reorder_point',
                      'order_upto_point',
                      'total_quantity','balance_quantity',
                      'locked_quantity',
                      'godown_qty',
                      'store_qty','invoice_qty','shelf_min','shelf_max','vno' ]] = \
        wh_inventory[['wh_id', 'wms_drug_code','drug_id','wms_distributor_code',
                      'company_code','purchase_serial_no','safety_stock','reorder_point',
                      'order_upto_point',
                      'total_quantity','balance_quantity',
                      'locked_quantity',
                      'godown_qty',
                      'store_qty','invoice_qty','shelf_min','shelf_max','vno' ]].astype(int)

        wh_inventory.columns = [c.replace('_', '-') for c in wh_inventory.columns]
        wh_inventory = wh_inventory[
            ['wms-drug-code', 'drug-id', 'distributor-id', 'distributor-name',
             'wms-distributor-code', 'purchase-date', 'drug-name', 'srate',
             'total-quantity', 'balance-quantity', 'locked-quantity', 'total-value',
             'balance-value', 'locked-value', 'expiry', 'company-name',
             'company-code', 'pack', 'purchase-rate', 'purchase-bill-no',
             'purchase-serial-no', 'batch-number', 'mrp', 'prate', 'drug-type',
             'composition', 'bucket', 'history-bucket', 'category', 'safety-stock',
             'reorder-point', 'order-upto-point', 'shelf-min', 'shelf-max',
             'snapshot-date', 'godown-qty', 'store-qty', 'invoice-net-amt',
             'invoice-tax-amt', 'invoice-dis-amt', 'invoice-qty', 'cgst', 'sgst',
             'igst', 'vno', 'created-at',
             'created-by', 'updated-at', 'updated-by', 'in-wh-portfolio', 'wh-id']]


        s3 = S3()
        logger.info("Writing data to wh-inventory-ss")
        schema = "prod2-generico"
        table_name = "wh-inventory-ss"
        table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)


        s3.write_df_to_db(df=wh_inventory[table_info['column_name']], table_name=table_name,
                          db=rs_db, schema='prod2-generico')

        logger.info("wh-inventory-ss table updated")
        status = True

    except Exception as e:
        err_msg = str(e)
        logger.info('wms_inventory job failed')
        logger.exception(e)

    finally:
        rs_db.close_connection()
        mssql.close_connection()
        mssql2.close_connection()
        mssql3.close_connection()
        # Sending email
        email = Email()
        if status:
            result = 'Success'
            email.send_email_file(subject=f"wms_inventory ({env}): {result}",
                                  mail_body=f"Run time: {cur_date}",
                                  to_emails=email_to, file_uris=[])
        else:
            result = 'Failed'
            email.send_email_file(subject=f"wms_inventory ({env}): {result}",
                                  mail_body=f"Run time: {cur_date}  {err_msg}",
                                  to_emails=email_to, file_uris=[])

        logger.info("Script ended")
