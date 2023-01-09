#!/usr/bin/env python
# coding: utf-8
import os
import sys

sys.path.append('../../../..')
import numpy as np
import pandas as pd
import datetime as dt
import argparse

from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.logger import get_logger
from dateutil.tz import gettz
from zeno_etl_libs.helper import helper

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
args, unknown = parser.parse_known_args()
env = args.env
os.environ['env'] = env

logger = get_logger()

logger.info(f"env: {env}")

rs_db = DB()
rs_db.open_connection()

s3 = S3()

# def main(rs_db, s3):
schema = 'prod2-generico'

# composition wise data for the last 30 days
query = '''
        select 
            x1.composition, 
            x1."overall_qty",
            round((x1."gen_quantity"/(x1."gen_quantity"+x1."eth_quantity"))*100,2) as "gen_share",
            round((x1."stores_comp_sold"/x1."live_stores")*100,2) as "stores_share_comp_sold",
            round((x1."gen_stores"/x1."stores_comp_sold")*100,2) as "%_stores_gen_sold" ,
            round((x1."sub_qty"/x1."sub_base")*100,2) as "substitution_percentage",
        --	round((x1."not_inv_base"/x1."overall_qty")*100,2) as "not_in_inv_%",
            round(((x1."gen_mrp"-x1."gen_sp")/x1."gen_mrp")*100,2) as "%_gen_discount",
            round(((x1."eth_mrp"-x1."eth_sp")/x1."eth_mrp")*100,2) as "%_eth_discount",
            x1."gen_mrp",
            x1."eth_mrp",
            x1."gen_sp",
            x1."eth_sp",
            x1."no_gen_drug",
            x1."no_eth_drug", 
            x1."GA_flag"
            from
        (select
            s.composition , 
            sum(s."net-quantity") as "overall_qty",
            sum(case when s."type" = 'generic' then convert(float,s."net-quantity") end) as "gen_quantity",
            sum(case when s."type" = 'ethical' then convert(float,s."net-quantity") end) as "eth_quantity",
            convert(float, count(distinct "store-id")) as "stores_comp_sold",
            convert(float, count(distinct(case when s."type" = 'generic' then s."store-id" end))) as "gen_stores",
            convert(float, count(distinct(case when s."type" = 'ethical' then s."store-id" end))) as "eth_stores",
            convert(float, count(distinct(case when s."substitution-status"= 'not-in-inventory' then s."store-id" end))) as "not_inv_stores",
            convert(float, (select count(distinct "store-id") from "prod2-generico"."prod2-generico".sales s where "created-date" >= dateadd(day, -30, current_date))) as "live_stores",
            sum(case when s."substitution-status" in ('substituted', 'not-substituted') then convert(float,"net-quantity") end) as "sub_base",
            sum(case when s."substitution-status" in ('substituted') then convert(float,"net-quantity") end) as "sub_qty",
            sum(case when s."substitution-status" in ('not-in-inventory', 'generic-unavailable') then convert(float,"net-quantity")  end) as "not_inv_base",
            avg(case when s."type" = 'generic' then mrp end) as "gen_mrp",
            avg(case when s."type" = 'ethical' then mrp end) as "eth_mrp",
            avg(case when s."type" = 'ethical' then "net-rate" end) as "eth_sp",
            avg(case when s."type" = 'generic' then "net-rate" end) as "gen_sp",
            count(distinct (case when s."type" = 'generic' then s."drug-id" end)) as "no_gen_drug",
            count(distinct (case when s."type" = 'ethical' then s."drug-id" end)) as "no_eth_drug",
            max(case when s."company-id"=6984 then 1 else 0 end) as "GA_flag"
        from
            "prod2-generico"."prod2-generico".sales s
        where 
            s."created-date" >= dateadd(day, -30, current_date)
            and s.composition in (select composition from "prod2-generico"."prod2-generico".drugs d where d."type"= 'generic')
            and s."net-quantity">0
        group by 1)x1  '''
comp_wise_data = rs_db.get_df(query)
comp_wise_data.fillna(0, inplace=True)

# Not in inv data store store store wise
query = '''
        select 
            x1.composition, 
            (sum(case when x1."gen_flag" =0 then convert(float,x1."not_inv_tot_qty") end)/sum(case when x1."gen_flag" =0 then convert(float, x1."tot_qty") end))*100  as "not_inv_per_gen_not_sold", 
            (sum(case when x1."gen_flag" =1 then convert(float,x1."not_inv_tot_qty") end)/sum(case when x1."gen_flag" =1 then convert(float, x1."tot_qty") end))*100  as "not_inv_per_gen_sold",
            (sum(case when x1."gen_flag" =1 then convert(float,x1."sub_qty") end)/sum(case when x1."gen_flag" =1 then convert(float, x1."sub_qty_base") end))*100 as "sub_per_str_whr_gen_sold",
            avg(case when x1."gen_flag" = 1 then "opportunity" end)*100 as "opp_gen_sold"
            from 
        (select
            s."store-id" , 
            s.composition ,
            nvl(sum(case when s."substitution-status" in ('substituted') then convert(float,s."net-quantity") end ),0) as "sub_qty",
            nvl(sum(case when s."substitution-status" in ('not-substituted') then s."net-quantity" end ),0) as "not_sub_qty",
            nvl(sum(case when s."substitution-status" in ('not-in-inventory') then s."net-quantity" end ),0) as "not_inv_qty",
            nvl(sum(case when s."substitution-status" in ('not-in-inventory','generic-unavailable') then s."net-quantity" end ),0) as "not_inv_tot_qty",
            nvl(sum(case when s."substitution-status" in ('substituted','not-substituted') then s."net-quantity" end ),0) as "sub_qty_base",
            nvl(sum(case when s."substitution-status" in ('substituted','not-substituted','not-in-inventory','generic-unavailable') then s."net-quantity" end),0) as "tot_qty",
            (case when "sub_qty">0 then 1 else 0 end) as "gen_flag",
            nvl(round(convert(float,"sub_qty")/nullif(convert(float,"sub_qty_base"),0),2),0) as "sub_%",
            ceil ((convert(float,"not_inv_qty")*"sub_%")+convert(float,"sub_qty")) as "sub_sim",
            ceil ((convert(float,"not_inv_qty")*"sub_%")+convert(float,"not_sub_qty")) as "not_sub_sim",
            nvl(round(convert(float, "sub_sim")/nullif(convert(float, "tot_qty"),0),2),0) as "opportunity"
        from
            "prod2-generico"."prod2-generico".sales s left join 
            "prod2-generico"."prod2-generico".drugs d2 on s."drug-id"= d2.id 
        where
            s.composition in (select composition from "prod2-generico"."prod2-generico".drugs d	where d."type" = 'generic')
            and s."created-date" >= dateadd(day, -30, current_date)
        group by s."store-id",s.composition )x1
        where x1."tot_qty">0
        group by x1.composition'''
not_inv_data = rs_db.get_df(query)
not_inv_data.fillna(0, inplace=True)

comp_wise_data = pd.merge(left=comp_wise_data, right=not_inv_data, how='left', on='composition')

# gen comp max set
query = '''
        select
            d.composition ,
            case when sum(doi.max) >0 then 'Yes' else 'No' end as "max_set"
        from
            "prod2-generico"."prod2-generico"."drug-order-info" doi
        left join "prod2-generico"."prod2-generico".drugs d on
            doi."drug-id" = d.id
        where
            d."type" = 'generic'
        group by d.composition '''
gen_max_set = rs_db.get_df(query)
comp_wise_data = pd.merge(left = comp_wise_data, right = gen_max_set, how = 'left', on = 'composition')

# gettin the comp from the above table
comp = comp_wise_data.composition.unique()
comp = tuple(comp)

# getting rank 1 drug ids of both ethical and generic of the above compositions
query = f'''
        select
            "drug-id" as "drug_id", egr.composition,  "type", egr.company 
        from
            "prod2-generico"."prod2-generico"."ethical-generic-rank" egr
        where
            composition in {comp}
            and "rank" = 1 
            and "type" in ('generic', 'ethical') '''
drug_rank = rs_db.get_df(query)

# top 20 companies check
query = f'''
        select * from
        (
        select 
            s.company ,
            rank() over(order by sum(s."net-quantity") desc) as "row"
        from
            "prod2-generico"."prod2-generico".sales s
        where s."year-created-at" > extract(year from current_date)-4
            and s."type"= 'generic'
        group by 1)x1 
        where "row"<= 20'''
top_20 = rs_db.get_df(query)

condition = [drug_rank['company'].isin(top_20['company'].unique()),
             ~drug_rank['company'].isin(top_20['company'].unique())]
choice = [1, 0]
drug_rank['in-top-20'] = np.select(condition, choice, default=0)

top_20_company = drug_rank[drug_rank['type'] == 'generic']
comp_wise_data = comp_wise_data.merge(top_20_company[['composition', 'in-top-20']])

id_list = drug_rank.drug_id.unique()
id_list = tuple(id_list)

# best selling generic drug of the above and ethical drug Margin, mrp, and selling price.
query = f'''
        select
            x1.composition,
            round((x1."eth1_mrp"-x1."eth1_sp")/(x1."eth1_mrp")*100,2) as "%_eth1_discount",
            round((x1."gen1_mrp"-x1."gen1_sp")/(x1."gen1_mrp")*100,2) as "%_gen1_discount",
            round((x1."gen1_sp"-x1."gen1_pur")/(x1."gen1_sp")*100,2) as "%_gen1_margin",
            round((x1."eth1_sp"-x1."eth1_pur")/(x1."eth1_sp")*100,2) as "%_eth1_margin",
            x1.gen1_sp,
            x1.eth1_sp
        from
        (select 
            composition ,
            round(avg(case when "type" = 'generic' then mrp end),2) as "gen1_mrp",
            round(avg(case when "type" = 'generic' then "net-rate" end),2) as "gen1_sp",
            round(avg(case when "type" = 'generic' then "purchase-rate" end),2) as "gen1_pur",
            round(avg(case when "type" = 'ethical' then mrp end), 2) as "eth1_mrp",
            round(avg(case when "type" = 'ethical' then "net-rate" end),2) as "eth1_sp",
            round(avg(case when "type" = 'ethical' then "purchase-rate" end),2) as "eth1_pur"
        from "prod2-generico"."prod2-generico".sales s 
        where "drug-id" in {id_list}
        group by 1
        having "gen1_sp"> 0 and "eth1_sp">0)x1 '''
comp1_price = rs_db.get_df(query)

merged_df = pd.merge(left=comp_wise_data, right=comp1_price, on='composition')

# Drug exists in WH
query = ''' 
        select
            d.composition , w."add-wh" 
        from
            "prod2-generico"."prod2-generico"."wh-sku-subs-master" w
        inner join "prod2-generico"."prod2-generico".drugs d on w."drug-id" = d.id 
        where 
            w."add-wh" = 'Yes'
            and d."type"= 'generic'
        group by d.composition, w."add-wh" '''
avail_at_wh = rs_db.get_df(query)
condition = [merged_df['composition'].isin(avail_at_wh['composition'].unique()),
             ~merged_df['composition'].isin(avail_at_wh['composition'].unique())]
choice = ['Yes', 'No']
merged_df['add-wh'] = np.select(condition, choice, default=0)

# Schedule H1 drug or not
query = '''
        select
            b."composition"
        from
            "prod2-generico"."composition-master-molecules-master-mapping" a
        inner join "prod2-generico"."composition-master" b
        on
            a."composition-master-id" = b."id"
        inner join "prod2-generico"."molecule-master" c
        on
            a."molecule-master-id" = c."id"
        where
            c."schedule" = 'h1'
        group by
            b."composition" '''
schedule = rs_db.get_df(query)
condition = [merged_df['composition'].isin(schedule['composition'].unique()),
             ~merged_df['composition'].isin(schedule['composition'].unique())]
choice = ['Yes', 'No']
merged_df['schedule-h1'] = np.select(condition, choice, default=0)

merged_df.columns = [c.replace('_', '-') for c in merged_df.columns]

merged_df['created-at'] = dt.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
merged_df['created-by'] = 'etl-automation'
merged_df['updated-at'] = dt.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
merged_df['updated-by'] = 'etl-automation'

# writing the table
table_name = 'actionable-compositions'
table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)
# =========================================================================
# Writing table in Redshift
# =========================================================================
if isinstance(table_info, type(None)):
    raise Exception(f"table: {table_name} do not exist, create the table first")
else:
    print(f"Table:{table_name} exists")
truncate_query = f''' DELETE FROM "{schema}"."{table_name}" '''
rs_db.execute(truncate_query)
logger.info(f"Table:{table_name} table truncated")
s3.write_df_to_db(df=merged_df[table_info['column_name']], table_name=table_name, db=rs_db,
                  schema=schema)
logger.info(f"Table:{table_name} table uploaded")

# finding how many days the gen 1 compositions was oos and at how many stores,
gen1_id = drug_rank[drug_rank['type'] == 'generic']
gen1_id_list = gen1_id.drug_id.unique()
gen1_id_list = tuple(gen1_id_list)

# finding OOS for the above drgu-ids
query = f'''
        select
            o."store-id" as "store_id",
            o."store-name",
            o."drug-id" as "drug_id",
            d."drug-name" as "drug_name",
            d.composition ,
            sum(o."oos-count") as "oos_days",
            o."as-active" as "as_active",
            o."max-set" 
        from
            "prod2-generico"."prod2-generico"."out-of-shelf-drug-level" o
        left join "prod2-generico"."prod2-generico".drugs d on o."drug-id" = d.id 
        where
            o."drug-id" in {gen1_id_list}
            and "max-set" = 'Y'
            and date(o."closing-date") >= dateadd(day, -30, current_date)
        group by 1,2,3,4,5,7,8; '''
oos_data = rs_db.get_df(query)
oos_data.columns = [c.replace('_', '-') for c in oos_data.columns]

df = merged_df[['composition', 'gen-share']]
oos_data = oos_data.merge(df[['composition', 'gen-share']])

oos_data['created-at'] = dt.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
oos_data['created-by'] = 'etl-automation'
oos_data['updated-at'] = dt.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
oos_data['updated-by'] = 'etl-automation'

# writing the table
table_name = 'actionable-gen1-oos'
table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)
# =========================================================================
# Writing table in Redshift
# =========================================================================
if isinstance(table_info, type(None)):
    raise Exception(f"table: {table_name} do not exist, create the table first")
else:
    print(f"Table:{table_name} exists")
truncate_query = f''' DELETE FROM "{schema}"."{table_name}" '''
rs_db.execute(truncate_query)
logger.info(f"Table:{table_name} table truncated")
s3.write_df_to_db(df=oos_data[table_info['column_name']], table_name=table_name, db=rs_db,
                  schema=schema)
logger.info(f"Table:{table_name} table uploaded")

# store wise substitution
query = f'''
        select 
            x1."store-id", 
            x1."store-name",
            x1.composition, 
            x1."created-by",
            x1."overall_qty",
            round((x1."gen_quantity"/(x1."gen_quantity"+x1."eth_quantity"))*100,2) as "gen_share",
            round((x1."sub_qty"/x1."sub_base")*100,2) as "substitution_percentage",
            round((x1."not_inv_base"/x1."tot_qty")*100,2) as "not_inv_percentage"
        from 
        (select
            "store-id" ,
            "store-name" ,
            composition ,
            s."created-by" ,
            sum(s."net-quantity") as "overall_qty",
            sum(case when s."type" = 'generic' then convert(float,s."net-quantity") end) as "gen_quantity",
            sum(case when s."type" = 'ethical' then convert(float,s."net-quantity") end) as "eth_quantity",
            sum(case when s."substitution-status" in ('substituted') then convert(float,"net-quantity") end) as "sub_qty",
            sum(case when s."substitution-status" in ('substituted', 'not-substituted') then convert(float,"net-quantity") end) as "sub_base",
            sum(case when s."substitution-status" in ('substituted','not-substituted','not-in-inventory', 'generic-not-available') then convert(float,"net-quantity") end) as "tot_qty",
            sum(case when s."substitution-status" in ('not-in-inventory', 'generic-not-available') then convert(float,"net-quantity") end) as "not_inv_base"
        from
            "prod2-generico"."prod2-generico".sales s
        where 
            s.composition in (select composition from "prod2-generico"."prod2-generico".drugs d where d."type"= 'generic')
            and s."created-date" >= dateadd(day, -30, current_date)
        group by 1,2,3,4
        having "gen_quantity">0 and "eth_quantity" >0 )x1 '''
store_wise_sub = rs_db.get_df(query)
store_wise_sub.columns = [c.replace('_', '-') for c in store_wise_sub.columns]

store_wise_sub['created-at'] = dt.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
store_wise_sub['updated-at'] = dt.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
store_wise_sub['updated-by'] = 'etl-automation'

# writing table
table_name = 'actionable-store-sub'
table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)
# =========================================================================
# Writing table in Redshift
# =========================================================================
if isinstance(table_info, type(None)):
    raise Exception(f"table: {table_name} do not exist, create the table first")
else:
    print(f"Table:{table_name} exists")
truncate_query = f''' DELETE FROM "{schema}"."{table_name}" '''
rs_db.execute(truncate_query)
logger.info(f"Table:{table_name} table truncated")
s3.write_df_to_db(df=store_wise_sub[table_info['column_name']], table_name=table_name, db=rs_db,
                  schema=schema)
logger.info(f"Table:{table_name} table uploaded")

# Closing the DB Connection
rs_db.close_connection()
