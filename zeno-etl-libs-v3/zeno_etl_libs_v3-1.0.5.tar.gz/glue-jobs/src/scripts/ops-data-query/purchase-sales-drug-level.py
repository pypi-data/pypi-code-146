''' Script for Purchase Sales at drug level  '''

#@owner: akshay.bhutada@zeno.health

#@Purpose: To find purchase sales ration at drug level and purchase margin.


import os
import sys
import datetime
import argparse
import pandas as pd
import numpy as np
from dateutil.tz import gettz

sys.path.append('../../../..')

from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.db.db import MSSql
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper import helper


parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
parser.add_argument('-et', '--email_to',
                    default="akshay.bhutada@zeno.health",
                    type=str, required=False)
parser.add_argument('-sd', '--start_date', default='NA', type=str, required=False)
parser.add_argument('-ed', '--end_date', default='NA', type=str, required=False)
args, unknown = parser.parse_known_args()
env = args.env
email_to = args.email_to
start_date = args.start_date
end_date = args.end_date

os.environ['env'] = env

cur_date = datetime.datetime.now(tz=gettz('Asia/Kolkata')).date()

d = datetime.timedelta(days = 5)

start_dt=cur_date-d

end_dt = cur_date - datetime.timedelta(1)


if start_date == 'NA' and end_date == 'NA':
    start_date = start_dt
    end_date = end_dt

s3=S3()

logger = get_logger(level='INFO')

rs_db = DB()
rs_db.open_connection()

# Net Sales

q_1='''
select
    '' as "wh-name",
	'SB' as "sub-type-1",
	'store' as "sub-type-2",
	'' as "sub-type-3",
	s."drug-id" ,
	s."drug-name" ,
	s."type" as "drug-type",
	s.category as "drug-category",
	(case when s."company-id"=6984 then 'true'
	else 'false' end) as "goodaid-flag",
	(case when s."invoice-item-reference" is null then 76
		else s."distributor-id" end ) as "distributor-id",
	(case when s."invoice-item-reference"  is null then 'Local Purchase'
		else s."distributor-name" end )  as "distributor-name",
	(case when sb."patient-id"=4480 and sb."auto-short"=1 then 'AS'
	When sb."auto-short"=0 and sb."auto-generated"=0 and sb."patient-id"!=4480 then 'PR'
	when sb."auto-short" =1 and sb."patient-id" !=4480  then 'MS'
	else 'distributor-dump' end ) as "as-ms-pr",
	date(s."created-at") as "approved-date",
	SUM(s."net-quantity") as "net-quantity",
	SUM(s."net-quantity"*s.rate) as "net-value",
	SUM(s."net-quantity"*s.mrp) as "mrp-value",
	SUM(s."net-quantity"*s."purchase-rate") as "wc-value"
from
	"prod2-generico".sales s 
left join (select * from (select
	"invoice-item-id",
	"short-book-id",
	row_number() over(partition by "invoice-item-id" 
order by
	"short-book-id" desc) as count_new
from
	"prod2-generico"."prod2-generico"."short-book-invoice-items" sbii  ) a
where a.count_new=1 ) g on
		s."invoice-item-reference" = g."invoice-item-id"
left join "prod2-generico"."prod2-generico"."short-book-1" sb on
		g."short-book-id" = sb.id
where date(s."created-at")>='{}' and date(s."created-at")<='{}' and  s."franchisee-id" =1
and  s."store-b2b" ='Store'
	group by 
	 "sub-type-1",
	 "sub-type-2",
	 "sub-type-3",
	 s."drug-id" ,
	s."drug-name",
	s."type" ,
	s.category ,
	(case when s."company-id"=6984 then 'true'
	else 'false' end) ,
	(case when s."invoice-item-reference" is null then 76
		else s."distributor-id" end ) ,
	(case when s."invoice-item-reference"  is null then 'Local Purchase'
		else s."distributor-name" end ) ,
	(case when sb."patient-id"=4480 and sb."auto-short"=1 then 'AS'
	When sb."auto-short"=0 and sb."auto-generated"=0 and sb."patient-id"!=4480 then 'PR'
	when sb."auto-short" =1 and sb."patient-id" !=4480  then 'MS'
	else 'distributor-dump' end ),
	date(s."created-at")
'''.format(start_date, end_date)


store_sales=rs_db.get_df(query=q_1)

# DC

q_4='''
select
    '' as "wh-name",
	'PB' as "sub-type-1",
	'DC' as "sub-type-2",
	'' as "sub-type-3",
	d.id  as "drug-id",
	d."drug-name" ,
	d."type" as "drug-type",
	d.category as "drug-category",
	(case
		when d."company-id" = 6984 then 'true'
		else 'false'
	end) as "goodaid-flag",
	i."distributor-id" ,
	d2."name" as "distributor-name",
	(case when sb."patient-id"=4480 and sb."auto-short"=1 then 'AS'
	When sb."auto-short"=0 and sb."auto-generated"=0 and sb."patient-id"!=4480 then 'PR'
	when sb."auto-short" =1 and sb."patient-id" !=4480  then 'MS'
	else 'distributor-dump' end ) as "as-ms-pr",
	date(i."approved-at") as "approved-date",
	SUM(ii."actual-quantity") as "net-quantity",
	SUM(ii."net-value") as "net-value",
	SUM(ii.mrp*ii."actual-quantity") as "mrp-value",
	SUM(ii."net-value") as "wc-value"
from
	"prod2-generico"."prod2-generico"."invoice-items" ii
left join "prod2-generico"."prod2-generico".invoices i on
	ii."invoice-id" = i.id
left join "prod2-generico"."prod2-generico".stores s on
	i."dc-id" =s.id 
left join "prod2-generico"."prod2-generico".stores s2 on
i."store-id" =s2.id
left join "prod2-generico"."prod2-generico".drugs d on
	ii."drug-id" = d.id
left join "prod2-generico"."prod2-generico".distributors d2 on
i."distributor-id" =d2.id 
left join (select * from (select
	"invoice-item-id",
	"short-book-id",
	row_number() over(partition by "invoice-item-id" 
order by
	"short-book-id" desc) as count_new
from
	"prod2-generico"."prod2-generico"."short-book-invoice-items" sbii  ) a
where a.count_new=1 ) g on
		ii.id = g."invoice-item-id"
	left join "prod2-generico"."prod2-generico"."short-book-1" sb on
		g."short-book-id" = sb.id
where
	  date(i."approved-at") >='{}' and date(i."approved-at") <='{}'
	and s2."franchisee-id" =1 and i."distributor-id" !=8105
group by 
	"sub-type-1",
	"sub-type-2",
	"sub-type-3",
	d.id ,
	d."drug-name" ,
	d."type" ,
	d.category ,
	(case
		when d."company-id" = 6984 then 'true'
		else 'false'
	end),
	i."distributor-id" ,
	d2."name" ,
	(case when sb."patient-id"=4480 and sb."auto-short"=1 then 'AS'
	When sb."auto-short"=0 and sb."auto-generated"=0 and sb."patient-id"!=4480 then 'PR'
	when sb."auto-short" =1 and sb."patient-id" !=4480  then 'MS'
	else 'distributor-dump' end ),
	date(i."approved-at")
'''.format(start_date, end_date)

network_dc_purchase=rs_db.get_df(query=q_4)

# Lp

q_5='''
select
      '' as "wh-name",
	'PB' as "sub-type-1",
	'LP' as "sub-type-2",
	'' as "sub-type-3",
	d.id as "drug-id" ,
	d."drug-name" ,
	d."type" as "drug-type",
	d.category as "drug-category",
	(case
		when d."company-id" = 6984 then 'true'
		else 'false'
	end) as "goodaid-flag",
	i."distributor-id" ,
	d2."name" as "distributor-name",
	'' as "as-ms-pr",
	date(i."approved-at") as "approved-date",
	SUM(ii."actual-quantity") as "net-quantity",
	SUM(ii."net-value") as "net-value",
	SUM(ii.mrp*ii."actual-quantity") as "mrp-value",
	SUM(ii."net-value") as "wc-value"
from
	"prod2-generico"."prod2-generico"."invoice-items-1" ii
left join "prod2-generico"."prod2-generico"."invoices-1" i on ii."franchisee-invoice-id" =i.id 
left join "prod2-generico"."prod2-generico".stores s on
	s.id = i."store-id"
left join "prod2-generico"."prod2-generico".drugs d on
	ii."drug-id" = d.id
left join "prod2-generico"."prod2-generico".distributors d2 on
i."distributor-id" =d2.id 
where
	ii."invoice-item-reference" is null and s."franchisee-id" =1 and 
	 date(i."approved-at") >='{}' and date(i."approved-at") <='{}'
group by
	"sub-type-1",
	"sub-type-2",
	"sub-type-3",
	d.id ,
	d."drug-name",
	d."type" ,
	d.category ,
	(case
		when d."company-id" = 6984 then 'true'
		else 'false'
	end),
	i."distributor-id" ,
	d2."name" ,
	date(i."approved-at")
'''.format(start_date, end_date)

network_lp_purchase=rs_db.get_df(query=q_5)

# Sale to Franchise

q_6='''	
select
      '' as "wh-name",
	'SB' as "sub-type-1",
	'Franchisee' as "sub-type-2",
	(case
		when i."distributor-id" = 8105 then 'WH'
		else 'DC' end) as "sub-type-3",
		d.id  as "drug-id",
		d."drug-name" ,
	d."type" as "drug-type",
	d.category as "drug-category",
	(case
		when d."company-id" = 6984 then 'true'
		else 'false'
	end) as "goodaid-flag",
	i."distributor-id" ,
	d2."name" as "distributor-name",
	'' as "as-ms-pr",
	date(i1."approved-at") as "approved-date",
	SUM(ii."actual-quantity") as "net-quantity",
	SUM(ii."net-value") as "net-value",
	SUM(ii.mrp*ii."actual-quantity") as "mrp-value",
	SUM(ii2."net-value") as "wc-value"
from
"prod2-generico"."prod2-generico"."invoice-items-1" ii 
left join "prod2-generico"."prod2-generico"."invoice-items" ii2 on ii."invoice-item-reference" =ii2.id 
left join "prod2-generico"."prod2-generico"."invoices-1" i1 on ii."franchisee-invoice-id" =i1.id 
left join "prod2-generico"."prod2-generico".invoices i on
	ii."invoice-id" =i.id 
left join "prod2-generico"."prod2-generico".stores s on
	i1."store-id" =s.id 
left join "prod2-generico"."prod2-generico".franchisees f 
on s."franchisee-id" =f.id 
left join "prod2-generico"."prod2-generico".drugs d on
	ii."drug-id" = d.id
left join "prod2-generico"."prod2-generico".distributors d2 on
i."distributor-id" =d2.id 
where
	  date(i1."approved-at") >='{}' and date(i1."approved-at") <='{}'
	and s."franchisee-id" !=1 and i1."franchisee-invoice" =0
group by 
	"sub-type-1",
	"sub-type-2",
	(case
		when i."distributor-id" = 8105 then 'WH'
		else 'DC' end),
	d.id ,
	d."drug-name", 
	d."type" ,
	d.category ,
	(case
		when d."company-id" = 6984 then 'true'
		else 'false'
	end),
	i."distributor-id" ,
	d2."name" ,
	date(i1."approved-at");
'''.format(start_date, end_date)


network_franchisee_sale=rs_db.get_df(query=q_6)


drug_info = '''

select
	d.id as "drug-id",
	d."drug-name",
	d."type" as "drug-type" ,
	d."category" as "drug-category",
	(case when d."company-id" =6984 then 'true'
	else 'false'  end) as "goodaid-flag"
from
	"prod2-generico".drugs d 
'''

drug_info = rs_db.get_df(query=drug_info)


mssql = MSSql(connect_via_tunnel=False)

cnxn = mssql.open_connection()

cursor = cnxn.cursor()

#Warehouse purchase
q_7='''
select
    'bhiwnadi-warehouse' as "wh-name",
	'PB' as "sub-type-1",
	'WH' as "sub-type-2",
	(CASE
		when sp.vno>0 then 'barcoded'
		else 'non-barcoded'
	end) as "sub-type-3",
	CONVERT(int, i.Barcode) as "drug-id",
	sp.acno as "distributor-id",
	a."name" as "distributor-name",
	(CASE when f.Uid is null then 'Auto'
	else 'manual' end ) as "as-ms-pr",
	CONVERT(date ,
	sp.Vdt) as "approved-date",
	SUM(sp.qty) as "net-quantity",
	SUM(sp.netamt + sp.taxamt) as "net-value",
	SUM(f1.mrp*sp.Qty) as "mrp-value",
	SUM(sp.NetAmt+sp.Taxamt) as "wc-value"
from
	salepurchase2 sp
left join item i on
	sp.itemc = i.code
left join FIFO f1 on 
            (f1.Pbillno = sp.Pbillno
            and f1.Psrlno = sp.Psrlno
            and f1.Itemc = sp.Itemc
            and f1.Vdt = sp.Vdt)
left join acm a on
	sp.acno = a.code
left join (Select Uid,Vtyp,Vdt,Acno,Vno FROM Salepurchase1 sp1 where sp1.Vtyp ='PO' and sp1.Slcd ='SL') f 
on (f.Vno=sp.RefVno and convert(date,sp.RefVdt) =convert(date,f.Vdt) and sp.Acno =f.acno)
where
	sp.vtype = 'PB'
	and sp.vdt >= '{}'
	and sp.vdt <= '{}'
	and sp.qty >0
	and 
	isnumeric(i.Barcode) = 1
	and i.barcode not like '%[^0-9]%' and sp.Acno not IN (59489)
group by
	(CASE
		when sp.vno>0 then 'barcoded'
		else 'non-barcoded'
	end),
	i.Barcode ,
	sp.acno ,
	a."name" ,
		(CASE when f.Uid is null then 'Auto'
	else 'manual' end ),
	sp.Vdt
'''.format(start_date, end_date)

network_wh_purchase_bhiwandi= pd.read_sql(q_7,cnxn)


mssql_ga = MSSql(connect_via_tunnel=False,db='Esdata_WS_2')

cnxn = mssql_ga.open_connection()

cursor = cnxn.cursor()

q_8='''select
    'goodaid-warehouse' as "wh-name",
	'PB' as "sub-type-1",
	'WH' as "sub-type-2",
	(CASE
		when sp.vno>0 then 'barcoded'
		else 'non-barcoded'
	end) as "sub-type-3",
	CONVERT(int, i.Barcode) as "drug-id",
	sp.acno as "distributor-id",
	a."name" as "distributor-name",
	(CASE when f.Uid is null then 'Auto'
	else 'manual' end ) as "as-ms-pr",
	CONVERT(date ,
	sp.Vdt) as "approved-date",
	SUM(sp.qty) as "net-quantity",
	SUM(sp.netamt + sp.taxamt) as "net-value",
	SUM(f1.mrp*sp.Qty) as "mrp-value",
	SUM(sp.NetAmt+sp.Taxamt) as "wc-value"
from
	salepurchase2 sp
left join item i on
	sp.itemc = i.code
left join FIFO f1 on 
            (f1.Pbillno = sp.Pbillno
            and f1.Psrlno = sp.Psrlno
            and f1.Itemc = sp.Itemc
            and f1.Vdt = sp.Vdt)
left join acm a on
	sp.acno = a.code
left join (Select Uid,Vtyp,Vdt,Acno,Vno FROM Salepurchase1 sp1 where sp1.Vtyp ='PO' and sp1.Slcd ='SL') f 
on (f.Vno=sp.RefVno and convert(date,sp.RefVdt) =convert(date,f.Vdt) and sp.Acno =f.acno)
where
	sp.vtype = 'PB'
	and sp.vdt >= '{}'
	and sp.vdt <= '{}'
	and sp.qty >0
	and 
	isnumeric(i.Barcode) = 1
	and i.barcode not like '%[^0-9]%'
group by
	(CASE
		when sp.vno>0 then 'barcoded'
		else 'non-barcoded'
	end),
	i.Barcode ,
	sp.acno ,
	a."name" ,
		(CASE when f.Uid is null then 'Auto'
	else 'manual' end ),
	sp.Vdt
'''.format(start_date, end_date)

network_wh_purchase_goodaid= pd.read_sql(q_8,cnxn)


mssql_tepl = MSSql(connect_via_tunnel=False,db='Esdata_TEPL')

cnxn = mssql_tepl.open_connection()

cursor = cnxn.cursor()

q_9='''select
    'tepl-warehouse' as "wh-name",
	'PB' as "sub-type-1",
	'WH' as "sub-type-2",
	(CASE
		when sp.vno>0 then 'barcoded'
		else 'non-barcoded'
	end) as "sub-type-3",
	CONVERT(int, i.Barcode) as "drug-id",
	sp.acno as "distributor-id",
	a."name" as "distributor-name",
	(CASE when f.Uid is null then 'Auto'
	else 'manual' end ) as "as-ms-pr",
	CONVERT(date ,
	sp.Vdt) as "approved-date",
	SUM(sp.qty) as "net-quantity",
	SUM(sp.netamt + sp.taxamt) as "net-value",
	SUM(f1.mrp*sp.Qty) as "mrp-value",
	SUM(sp.NetAmt+sp.Taxamt) as "wc-value"
from
	salepurchase2 sp
left join item i on
	sp.itemc = i.code
left join FIFO f1 on 
            (f1.Pbillno = sp.Pbillno
            and f1.Psrlno = sp.Psrlno
            and f1.Itemc = sp.Itemc
            and f1.Vdt = sp.Vdt)
left join acm a on
	sp.acno = a.code
left join (Select Uid,Vtyp,Vdt,Acno,Vno FROM Salepurchase1 sp1 where sp1.Vtyp ='PO' and sp1.Slcd ='SL') f 
on (f.Vno=sp.RefVno and convert(date,sp.RefVdt) =convert(date,f.Vdt) and sp.Acno =f.acno)
where
	sp.vtype = 'PB'
	and sp.vdt >= '{}'
	and sp.vdt <= '{}'
	and sp.qty >0
	and 
	isnumeric(i.Barcode) = 1
	and i.barcode not like '%[^0-9]%'
group by
	(CASE
		when sp.vno>0 then 'barcoded'
		else 'non-barcoded'
	end),
	i.Barcode ,
	sp.acno ,
	a."name" ,
		(CASE when f.Uid is null then 'Auto'
	else 'manual' end ),
	sp.Vdt
'''.format(start_date, end_date)

network_wh_purchase_tepl= pd.read_sql(q_9,cnxn)


network_wh_purchase=pd.concat([network_wh_purchase_bhiwandi,
                               network_wh_purchase_goodaid,network_wh_purchase_tepl],
                              sort=False,ignore_index=False)


network_wh_purchase[['drug-id']]= \
    network_wh_purchase[['drug-id']].\
        apply(pd.to_numeric, errors='ignore').astype('Int64')


network_wh_purchase=pd.merge(network_wh_purchase,drug_info,how='left',on='drug-id')



network_wh_purchase[['drug-type','drug-category', 'goodaid-flag']]=\
    network_wh_purchase[['drug-type','drug-category', 'goodaid-flag']].\
        fillna('NA')

network_wh_purchase[['net-quantity']]=\
    network_wh_purchase[['net-quantity']].astype(np.int64)


network_wh_purchase=network_wh_purchase[['wh-name','sub-type-1',
                                    'sub-type-2','sub-type-3',
                                    'drug-id','drug-name','drug-type','drug-category',
                                    'goodaid-flag','distributor-id',
                                    'distributor-name','as-ms-pr','approved-date','net-quantity',
                                         'net-value','mrp-value','wc-value']]


sale_purchase_all=pd.concat([store_sales,
                 network_dc_purchase,
                network_lp_purchase,
                network_wh_purchase,network_franchisee_sale],
                 sort=False,ignore_index=False)



sale_purchase_all[['drug-id', 'distributor-id']]= \
    sale_purchase_all[['drug-id','distributor-id']].\
        apply(pd.to_numeric, errors='ignore').astype('Int64')

sale_purchase_all[['net-quantity']]=sale_purchase_all[['net-quantity']].astype(np.int64)

sale_purchase_all[['net-value','mrp-value','wc-value']]=\
    sale_purchase_all[['net-value','mrp-value','wc-value']].\
        astype(np.float64)


created_at = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
sale_purchase_all['created-at']=datetime.datetime.strptime(created_at,"%Y-%m-%d %H:%M:%S")
updated_at = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
sale_purchase_all['updated-at']=datetime.datetime.strptime(updated_at,"%Y-%m-%d %H:%M:%S")
sale_purchase_all['created-by'] = 'etl-automation'
sale_purchase_all['updated-by'] = 'etl-automation'



sale_purchase_all.columns = [c.replace('_', '-') for c in sale_purchase_all.columns]


schema = "prod2-generico"
table_name = "purchase-sales-meta-drug-level"
table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)


#truncating the last 5 days data

delete_q = """
        delete
from
	"prod2-generico"."purchase-sales-meta-drug-level"
where
	date("approved-date") >= '{start_date_n}'
	and date("approved-date") <= '{end_date_n}'
	and "sub-type-1" in ('inventory', 'SB', 'PB')
    """.format(start_date_n=start_date, end_date_n=end_date)

rs_db.execute(delete_q)

#Keep only Last one year data

delete_one_year='''
delete from "prod2-generico"."purchase-sales-meta-drug-level" 
where date("approved-date")<=current_date -interval '12 months'
'''
rs_db.execute(delete_one_year)


s3.write_df_to_db(df=sale_purchase_all[table_info['column_name']], table_name=table_name, db=rs_db,
                  schema=schema)

status=True

if status==True:
    script_status="Success"
else:
    script_status="Failed"


email = Email()

#email.send_email_file(
# subject=f"purchase_sales
# start date: {start_date} end date: {end_date} {script_status}",
             #mail_body=f"purchase_sales status: {script_status} ",
                      #to_emails=email_to)

email.send_email_file(subject=f"sale purchase report drug level  for date {end_date}",
                      mail_body=f"PFA sale purchase data drug level for date   {end_date} ",
                      to_emails=email_to)


rs_db.close_connection()
mssql.close_connection()
mssql_ga.close_connection()
mssql_tepl.close_connection()
