"""""
 Pupose : categorising Excess Inventory
 Author : saurav.maskar@zeno.health
"""""

import os
import sys

sys.path.append('../../../..')

from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.db.db import DB, MySQL
from zeno_etl_libs.config.common import Config
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper import helper
from dateutil.tz import gettz

import json
import datetime

import argparse
import pandas as pd
import numpy as np
import traceback

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stage, prod)")
parser.add_argument('-et', '--email_to', default="saurav.maskar@zeno.health", type=str, required=False)
parser.add_argument('-dl', '--doh_limit', default=45, type=int, required=False,
                    help="Excess Parameter - DOH limit to qualify as excess")
parser.add_argument('-wvl', '--workcell_value_limit', default=100, type=int, required=False,
                    help="Excess Parameter - workcell_value_limit to qualify as excess")
parser.add_argument('-qcei', '--quantity_cap_to_qualify_as_excess_inventory', default=2, type=int, required=False,
                    help = "Excess Parameter - Store must have atleast this much quantity to qualify as excess")
parser.add_argument('-meqc', '--minimum_excess_quantity_cap', default=2, type=int, required=False,
                    help = "Excess Parameter - excess quantity should be >= minimum_excess_quantity_cap ")
parser.add_argument('-mx', '--max_times_x', default=1.2, type=int, required=False,
                    help = "Excess Parameter - Either/or - Cushion over Max to qualify as excess")
parser.add_argument('-mpxd', '--max_plux_x_doh', default=10, type=int, required=False,
                    help = "Excess Parameter - Either/or - Cushion over Max to qualify as excess")
# parser.add_argument('-md', '--minimum_doh', default=30, type=int, required=False,
#                     help = "less Parameter - DOH below which inventory will be qualified as less")
parser.add_argument('-ccof', '--categorise_coco_only_flag', default=1, type=int, required=False,
                    help = "1 = Only COCO store, 0 = All")
parser.add_argument('-msa', '--minimum_store_age', default=180, type=int, required=False,
                    help = "Minimum Store age to categorise excess inventory")
parser.add_argument('-msda', '--minimum_store_drug_age', default=45, type=int, required=False,
                    help = "Minimum Store_drug_age to categorise excess inventory")
parser.add_argument('-nec', '--near_expiry_cap', default=90, type=int, required=False,
                    help = "Inventory above near expiry will only be considered for categorisation")
parser.add_argument('-flsa', '--fofo_launch_store_age', default=90, type=int, required=False,
                    help = "fofo store age for excess type launch_stock>fofo_launch_doh_limit")
parser.add_argument('-fldl', '--fofo_launch_doh_limit', default=180, type=int, required=False,
                    help = "fofo store reove launch_stock where quantity>fofo_launch_doh_limit")
args, unknown = parser.parse_known_args()
env = args.env
email_to = args.email_to
doh_limit = args.doh_limit
workcell_value_limit = args.workcell_value_limit
quantity_cap_to_qualify_as_excess_inventory = args.quantity_cap_to_qualify_as_excess_inventory
minimum_excess_quantity_cap = args.minimum_excess_quantity_cap
max_times_x = args.max_times_x
max_plux_x_doh = args.max_plux_x_doh
# minimum_doh = args.minimum_doh
categorise_coco_only_flag = args.categorise_coco_only_flag
minimum_store_age = args.minimum_store_age
minimum_store_drug_age = args.minimum_store_drug_age
near_expiry_cap = args.near_expiry_cap
fofo_launch_store_age = args.fofo_launch_store_age
fofo_launch_doh_limit = args.fofo_launch_doh_limit

os.environ['env'] = env

logger = get_logger(level='INFO')

logger.info(f"env: {env}")

rs_db = DB()
rs_db.open_connection()

s3 = S3()
start_time = datetime.datetime.now(tz=gettz('Asia/Kolkata'))
logger.info('Script Manager Initialized')
logger.info("")
logger.info("parameters reading")
logger.info(f"env: {env}")
logger.info("email_to - " + email_to)
logger.info("doh_limit - " + str(doh_limit))
logger.info("workcell_value_limit - " + str(workcell_value_limit))
logger.info("quantity_cap_to_qualify_as_excess_inventory  - " + str(quantity_cap_to_qualify_as_excess_inventory))
logger.info("minimum_excess_quantity_cap  - " + str(minimum_excess_quantity_cap))
logger.info("max_times_x - " + str(max_times_x))
logger.info("max_plux_x_doh - " + str(max_plux_x_doh))
# logger.info("minimum_doh - " + str(minimum_doh))
logger.info("categorise_coco_only_flag - " + str(categorise_coco_only_flag))
logger.info("minimum_store_age - " + str(minimum_store_age))
logger.info("minimum_store_drug_age - " + str(minimum_store_drug_age))
logger.info("near_expiry_cap - " + str(near_expiry_cap))
logger.info("fofo_launch_store_age - " + str(fofo_launch_store_age))
logger.info("fofo_launch_doh_limit - " + str(fofo_launch_doh_limit))
logger.info("")

# date parameter
logger.info("code started at {}".format(datetime.datetime.now().strftime(
    '%Y-%m-%d %H:%M:%S')))
logger.info("")

cur_date = datetime.datetime.now(tz=gettz('Asia/Kolkata')).date()

# Fetching Inventory data
inventory_query = f"""
    select
        i."store-id" ,
        i."drug-id",
        sum(i.quantity) as "quantity",
        sum(i.quantity * i."purchase-rate") as "workcell-value"
        from "prod2-generico"."prod2-generico"."inventory-1" i
    where i."quantity" > 0
    and i."franchisee-inventory" = 0
    and i."expiry" > dateadd(day,{near_expiry_cap},getdate())
    group by
        i."store-id" ,
        i."drug-id"
    """
inventory = rs_db.get_df(inventory_query)
logger.info('fetched inventory data')

# Fetching Stores data
stores_query = """
    select
        s.id as "store-id",
        s."name" as "store-name",
        case
            when s."franchisee-id" = 1 then 'COCO'
            else 'FOFO'
        end as "franchise-tag",
        case
            when s."opened-at" is null
            or s."opened-at" = '0101-01-01 00:00:00.000' then 0
            else datediff(day,
            date(s."opened-at"),
            current_date)
        end as "store-age",
        zc."name" as "city-name"
    from
        "prod2-generico"."prod2-generico".stores s
    left join "prod2-generico"."prod2-generico".franchisees f 
            on
        s."franchisee-id" = f.id
    left join "prod2-generico"."prod2-generico"."zeno-city" zc 
            on
        s."city-id" = zc.id
    left join "prod2-generico"."prod2-generico"."zeno-indian-states" zis 
            on
        zc."indian-state-id" = zis.id
    """
stores = rs_db.get_df(stores_query)
inventory = inventory.merge(stores, how = 'left', on = 'store-id')
logger.info('fetched stores data')

# Fetching drugs data
drugs_query = """
    select
        d.id as "drug-id",
        d."drug-name" ,
        d."type" as "drug-type",
        case when d."company-id" = 6984 then 'Goodaid' else 'non-Goodaid' end as "goodaid-flag"
    from
        "prod2-generico"."prod2-generico".drugs d
    """
drugs = rs_db.get_df(drugs_query)
inventory = inventory.merge(drugs, how = 'left', on = 'drug-id')
logger.info('fetched drugs data')

# Fetching store-drug-age
store_drug_age_query = """
    select
        s."store-id" ,
        s."drug-id" ,
        datediff(day,min(s."created-at"),current_date) as "store-drug-age"
    from
        "prod2-generico".sales s
    where
        s."bill-flag" = 'gross'
    group by
        s."store-id" ,
        s."drug-id"
    """
store_drug_age = rs_db.get_df(store_drug_age_query)
inventory = inventory.merge(store_drug_age, how = 'left', on = ['store-id','drug-id'])
inventory['store-drug-age'] = inventory['store-drug-age'].fillna(1)
logger.info('fetched store_drug_age data')

#Fetching sales data
sales_query = """
    select
        s."store-id" ,
        s."drug-id" ,
        sum(s.quantity) as "last-90-days-sales-quantity"
    from
        "prod2-generico"."prod2-generico".sales s
    where
        date(s."created-at") > current_date - 90
    group by
        s."store-id" ,
        s."drug-id"
    """
sales = rs_db.get_df(sales_query)
inventory = inventory.merge(sales, how = 'left', on = ['store-id','drug-id'])
inventory['last-90-days-sales-quantity-orignal'] = inventory['last-90-days-sales-quantity']
logger.info('fetched sales data')

# Fetching store-drug availibility percentage
store_drug_availibility_query = """
    select
        oosdl."store-id" ,
        oosdl."drug-id" ,
    --	sum("oos-count") as "oos-count",
    --	sum("drug-count") as "drug-count",
        1 - (sum("oos-count")/ sum("drug-count")) as "availibility_percentage"
    from
        "prod2-generico"."out-of-shelf-drug-level" oosdl
    where
        "closing-date" >= current_date - 90
        and "max-set" = 'Y'
    group by
        oosdl."store-id" ,
        oosdl."drug-id"
    """
store_drug_availibility = rs_db.get_df(store_drug_availibility_query)
inventory = inventory.merge(store_drug_availibility, how = 'left', on = ['store-id','drug-id'])
inventory['availibility_percentage'] = inventory['availibility_percentage'].fillna(1)
logger.info('fetched store_drug_availibility data')

# Calculating sales based doh
inventory['last-90-days-sales-quantity'] = inventory['last-90-days-sales-quantity'].fillna(0)
inventory['last-90-days-sales-quantity'] = inventory['last-90-days-sales-quantity'] /inventory['availibility_percentage']
inventory['last-90-days-sales-quantity'] = inventory['last-90-days-sales-quantity'].astype(float)
inventory['sales-demand-daily'] = inventory['last-90-days-sales-quantity']*1.0/90.0
inventory['doh-based-on-sales'] = inventory['quantity']/inventory['sales-demand-daily']
inventory['store-drug'] = inventory['store-id'].astype(str) + '-' + inventory['drug-id'].astype(str)
store_drug_list = tuple(map(str,inventory['store-drug'].unique()))
logger.info('calculated sales based doh')

# Fetching IPC forecast data
ipc_forecast_query = f"""
   select
        iss."store-id" ,
        iss."drug-id" ,
        iss.fcst ,
        iss.std 
    from
        "prod2-generico"."ipc2-safety-stock" iss
    inner join (
        select
            "store-id" ,
            max("reset-date") as latest_reset
        from
            "prod2-generico"."ipc2-safety-stock" iss
        group by
            "store-id" 
    ) as sq
    on
        iss."store-id" = sq."store-id"
        and iss."reset-date" = sq.latest_reset
        and concat(iss."store-id", CONCAT('-', iss."drug-id")) in {store_drug_list}
    """
ipc_forecast = rs_db.get_df(ipc_forecast_query)
inventory = inventory.merge(ipc_forecast, how = 'left', on = ['store-id','drug-id'])
logger.info('fetched ipc_forecast data')

# calculating fcst based doh
inventory['fcst'] = inventory['fcst'].fillna(0)
inventory['fcst-demand-daily'] = inventory['fcst']/28
inventory['doh-based-on-fcst'] = inventory['quantity']/inventory['fcst-demand-daily']
logger.info('calculated fcst based doh')

# deciding fcst vs sales based doh
conditions = [inventory['doh-based-on-fcst']<inventory['doh-based-on-sales'],inventory['doh-based-on-fcst']>=inventory['doh-based-on-sales']]
choice = [inventory['doh-based-on-fcst'],inventory['doh-based-on-sales']]
choice2 = [inventory['fcst-demand-daily'],inventory['sales-demand-daily']]
choice3 = ['fcst-based','sales-history-based']
inventory['doh'] = np.select(conditions,choice, default=0)
inventory['demand-daily'] = np.select(conditions,choice2, default=0)
inventory['doh-type'] = np.select(conditions,choice3, default=0)
logger.info('decided fcst vs sales based doh')

# Fetching DOI data
doi_query = f"""
     select
        doi."store-id" ,
        doi."drug-id" ,
        doi.min,
        doi.max ,
        doi."safe-stock" 
    from
        "prod2-generico"."drug-order-info" doi
    where 
        concat(doi."store-id", CONCAT('-', doi."drug-id")) in {store_drug_list}
"""
doi = rs_db.get_df(doi_query)
inventory = inventory.merge(doi,how='left',on = ['store-id','drug-id'])
inventory['max-time-x-original'] = (inventory['max']*max_times_x).apply(np.ceil)
inventory['max-plus-x-doh'] = inventory['max']+ (inventory['fcst-demand-daily']*1).apply(np.ceil)
# Cushion over Max Eiether x% or x DOH which ever is higher
conditions = [inventory['max-time-x-original']>=inventory['max-plus-x-doh'],inventory['max-time-x-original']<inventory['max-plus-x-doh']]
choice = [inventory['max-time-x-original'],inventory['max-plus-x-doh']]
choice2 = ['percentage over max','DOH over max']
inventory['max-cushion-type'] = np.select(conditions,choice2)
inventory['max-time-x'] = np.select(conditions,choice)


logger.info('fetched doi data')

# Fetching NPI data
npi_query = """
    select
        nias."store-id" ,
        nias."drug-id" ,
        '1' as "in-npi"
        from "prod2-generico"."prod2-generico"."npi-inventory-at-store" nias
    where
        nias."inventory-type" = 'Rotate'
    group by
        nias."store-id" ,
        nias."drug-id"
    """
npi = rs_db.get_df(npi_query)
inventory = inventory.merge(npi , how = 'left', on = ['store-id','drug-id'])
logger.info('fetched npi data')

# Categorising inventory based on DOH and MAX
conditions = [(inventory['doh']>=doh_limit) & (inventory['quantity']>inventory['max-time-x']) &(inventory['quantity']>quantity_cap_to_qualify_as_excess_inventory)]

choice = ['excess']

inventory['excess-flag'] = np.select(conditions,choice, default='ok')

# Identifying excess inventory
inventory['excess-def1'] = (inventory['doh']-doh_limit)*inventory['demand-daily']

inventory['excess-def2'] = (inventory['quantity']-inventory['max-time-x'])

inventory['excess-defmin'] = inventory[['excess-def1','excess-def2']].min(axis=1)

# Calculating immediate stock transfer opportunity
# inventory['less-def1'] = (minimum_doh - inventory['doh'])*inventory['demand-daily']
# inventory['less-defmin'] = inventory['less-def1']

# Defining excess quantity and value
conditions = [(inventory['excess-flag']=='excess')]
choice = [inventory['excess-defmin']]
inventory['excess-quantity'] = np.select(conditions,choice, default=0)
inventory['excess-quantity'] = inventory['excess-quantity'].apply(np.floor)
inventory['excess-value'] = (inventory['workcell-value'].astype(float)/inventory['quantity'].astype(float))*inventory['excess-quantity'].astype(float)

# Excess value should be greater than workcell value limit
conditions = [(inventory['excess-flag']=='excess') & (inventory['excess-value']>= workcell_value_limit),
             (inventory['excess-flag']=='excess') & (inventory['excess-value']< workcell_value_limit),
             (inventory['excess-flag']!='excess')]

choice = ['excess','ok',inventory['excess-flag']]
choice1 =[inventory['excess-quantity'],0,inventory['excess-quantity']]
choice2 = [inventory['excess-value'],0,inventory['excess-value']]

inventory['excess-flag'] = np.select(conditions,choice, default='ok')
inventory['excess-quantity'] = np.select(conditions,choice1, default=0)
inventory['excess-value'] = np.select(conditions,choice2, default=0)

# Excess quantity should be greater than minimum_excess_quantity_cap
conditions = [(inventory['excess-flag']=='excess') & (inventory['excess-quantity']>= minimum_excess_quantity_cap),
             (inventory['excess-flag']=='excess') & (inventory['excess-quantity']< minimum_excess_quantity_cap),
             (inventory['excess-flag']!='excess')]

choice = ['excess','ok',inventory['excess-flag']]
choice1 =[inventory['excess-quantity'],0,inventory['excess-quantity']]
choice2 = [inventory['excess-value'],0,inventory['excess-value']]

inventory['excess-flag'] = np.select(conditions,choice, default='ok')
inventory['excess-quantity'] = np.select(conditions,choice1, default=0)
inventory['excess-value'] = np.select(conditions,choice2, default=0)
logger.info('categorised inventory with flags - excess/less/ok')

# Immediate Stock transfer opportunity
# Immediate implies -Void in network stores (Void = (minimum_doh - inventory['doh'])*inventory['demand-daily'])
# df4 = pd.pivot_table(inventory,
#                              values=['excess-quantity','excess-value'],
#                              index=['drug-id'],
#                              columns=['excess-flag'],
#                     aggfunc=np.sum).reset_index()
# df4.columns =  ["-".join(x) for x in df4.columns.ravel()]
#
# df4 = df4.reset_index(drop = True)
# del df4['excess-quantity-ok']
# del df4['excess-value-ok']
#
# df4 = df4[(df4['excess-quantity-excess']>0) | (df4['excess-quantity-less']>0)]
# df4.reset_index(drop = True, inplace = True)
#
# df4.loc[df4['excess-quantity-excess']>=df4['excess-quantity-less'] , 'qty-stock-transfer-opportunity-immediate'] = df4['excess-quantity-less']
# df4.loc[df4['excess-quantity-excess']<df4['excess-quantity-less'] , 'qty-stock-transfer-opportunity-immediate'] = df4['excess-quantity-excess']
#
# df4.loc[df4['excess-quantity-excess']>=df4['excess-quantity-less'] , 'value-stock-transfer-opportunity-immediate'] = df4['excess-value-less']
# df4.loc[df4['excess-quantity-excess']<df4['excess-quantity-less'] , 'value-stock-transfer-opportunity-immediate'] = df4['excess-value-excess']
#
# df4.rename(columns={'drug-id-': 'drug-id'},inplace=True)
# df4.columns
# inventory = inventory.merge(df4[['drug-id','qty-stock-transfer-opportunity-immediate',
#        'value-stock-transfer-opportunity-immediate' ]] , how = 'left', on = ['drug-id'])
#
# logger.info('calculated immediate stock transfer opportunity')
# logger.info("")
# logger.info('whole network level data')
# logger.info(f"Excess Inventory -  {sum(inventory[inventory['excess-flag']=='excess']['excess-value'])}")
# logger.info(f"Excess Inventory with NPI -  {sum(inventory[(inventory['excess-flag']=='excess') & (inventory['in-npi']=='1')]['excess-value'])}")
# logger.info(f"Excess Inventory without NPI -  {sum(inventory[(inventory['excess-flag']=='excess') & (inventory['in-npi']!='1')]['excess-value'])}")
# logger.info(f"stock-transfer-opportunity -  {sum(df4['value-stock-transfer-opportunity-immediate'].fillna(0))}")
# logger.info("")

# Network level sales
network_sales = sales.groupby(['drug-id']).sum().reset_index()[['drug-id','last-90-days-sales-quantity']]
network_sales.rename(columns={'last-90-days-sales-quantity': 'network-level-last-90-days-sales-quantity'},inplace=True)
network_sales[['drug-id','network-level-last-90-days-sales-quantity']] = network_sales[['drug-id','network-level-last-90-days-sales-quantity']].astype(int)

inventory = inventory.merge(network_sales , how = 'left', on = ['drug-id'])
logger.info('added network level sales')

inventory = inventory[inventory['excess-flag'] == 'excess']
inventory = inventory[inventory['store-age']>minimum_store_age]
inventory = inventory[inventory['store-drug-age']>minimum_store_drug_age]
if int(categorise_coco_only_flag) == 1:
    inventory = inventory[inventory['franchise-tag']=='COCO']
inventory = inventory[inventory['in-npi'].isna()]
inventory = inventory[inventory['last-90-days-sales-quantity']!= 0] # Potential NPI, so not adding in excess

# inventory['qty-stock-transfer-opportunity-immediate'] = inventory['qty-stock-transfer-opportunity-immediate'].fillna(0)
# inventory['value-stock-transfer-opportunity-immediate'] = inventory['value-stock-transfer-opportunity-immediate'].fillna(0)

inventory['network-level-last-90-days-sales-quantity'] = inventory['network-level-last-90-days-sales-quantity'].fillna(0)

# conditions = [inventory['qty-stock-transfer-opportunity-immediate']>0]
# choice = [1]
# inventory['immediate-stock-transfer-opportunity-flag'] = np.select(conditions,choice, default=0)

conditions = [inventory['network-level-last-90-days-sales-quantity']>0,inventory['network-level-last-90-days-sales-quantity']<=0]
choice = ['Rotate','Return']
inventory['inventory-type'] = np.select(conditions,choice, default=0)
logger.info('End : COCO Excess categorisation')

# Adding Launch stock DOH > 180 In FOFO
# Fetching fofo Inventory data
logger.info('start : Adding Launch stock DOH > 180 In FOFO')
fofo_launch_inventory_query = f"""
     select
        i."store-id" ,
        i."drug-id",
        sum(i.quantity) as "quantity",
        sum(i.quantity * i."purchase-rate") as "workcell-value"
    from
        "prod2-generico"."inventory-1" i
    left join "prod2-generico".invoices inv on
        i."invoice-id" = inv.id
    left join "prod2-generico"."invoices-1" i2 
            on i."franchisee-invoice-id" = i2.id 
    left join "prod2-generico"."stores" s on
         s."id" = i."store-id"
    where
        i."quantity" > 0
        and s."franchisee-id" != 1 -- fofo
        and i."franchisee-inventory" = 0 -- workcell inventory
        and (inv."invoice-date") < (s."opened-at") -- launch stock
        and i2."franchisee-invoice" = 0 -- workcell invoice
    group by
        i."store-id" ,
        i."drug-id"
    """
fofo_launch_inventory = rs_db.get_df(fofo_launch_inventory_query)
logger.info('fetched fofo_launch_inventory data')

fofo_launch_inventory = fofo_launch_inventory.merge(stores, how = 'left', on = 'store-id')
fofo_launch_inventory = fofo_launch_inventory.merge(drugs, how = 'left', on = 'drug-id')
fofo_launch_inventory = fofo_launch_inventory.merge(store_drug_age, how = 'left', on = ['store-id','drug-id'])
fofo_launch_inventory = fofo_launch_inventory.merge(sales, how = 'left', on = ['store-id','drug-id'])
fofo_launch_inventory['last-90-days-sales-quantity-orignal'] = fofo_launch_inventory['last-90-days-sales-quantity']
fofo_launch_inventory = fofo_launch_inventory.merge(store_drug_availibility, how = 'left', on = ['store-id','drug-id'])
fofo_launch_inventory['availibility_percentage'] = fofo_launch_inventory['availibility_percentage'].fillna(1)
fofo_launch_inventory['last-90-days-sales-quantity'] = fofo_launch_inventory['last-90-days-sales-quantity'].fillna(0)
fofo_launch_inventory['sales-demand-daily'] = fofo_launch_inventory['last-90-days-sales-quantity']*1.0/90.0
fofo_launch_inventory['doh-based-on-sales'] = fofo_launch_inventory['quantity']/fofo_launch_inventory['sales-demand-daily']
fofo_launch_inventory = fofo_launch_inventory.merge(ipc_forecast, how = 'left', on = ['store-id','drug-id'])
fofo_launch_inventory = fofo_launch_inventory.merge(doi,how='left',on = ['store-id','drug-id'])
fofo_launch_inventory['max-time-x'] = (fofo_launch_inventory['max']*max_times_x).apply(np.ceil)
# fofo_launch_inventory['max-plus-x-doh'] = fofo_launch_inventory['max'] + (fofo_launch_inventory['fcst-demand-daily']*1).apply(np.ceil)
# Cushion over Max Eiether x% or x DOH which ever is higher
# conditions = [fofo_launch_inventory['max-time-x-original']>=fofo_launch_inventory['max-plus-x-doh'],fofo_launch_inventory['max-time-x-original']<fofo_launch_inventory['max-plus-x-doh']]
# choice = [fofo_launch_inventory['max-time-x-original'],fofo_launch_inventory['max-plus-x-doh']]
# choice2 = ['percentage over max','DOH over max']
# fofo_launch_inventory['max-cushion-type'] = np.select(conditions,choice2)
# fofo_launch_inventory['max-time-x'] = np.select(conditions,choice)
fofo_launch_inventory = fofo_launch_inventory.merge(npi , how = 'left', on = ['store-id','drug-id'])
fofo_launch_inventory = fofo_launch_inventory.merge(network_sales , how = 'left', on = ['drug-id'])


# Changing doh infinity cases to doh 2000
conditions = [fofo_launch_inventory['doh-based-on-sales']==np.inf,fofo_launch_inventory['doh-based-on-sales']!=np.inf]
choice = [2000,fofo_launch_inventory['doh-based-on-sales']]
fofo_launch_inventory['doh-based-on-sales'] = np.select(conditions,choice)

fofo_launch_inventory['excess-def1'] = (fofo_launch_inventory['doh-based-on-sales']-fofo_launch_doh_limit)*fofo_launch_inventory['sales-demand-daily']
fofo_launch_inventory['excess-def2'] = (fofo_launch_inventory['quantity']-fofo_launch_inventory['max'])
fofo_launch_inventory['excess-defmin'] = fofo_launch_inventory[['excess-def1','excess-def2']].min(axis=1)

fofo_launch_inventory = fofo_launch_inventory[fofo_launch_inventory['store-age']>fofo_launch_store_age]
fofo_launch_inventory = fofo_launch_inventory[fofo_launch_inventory['doh-based-on-sales']>fofo_launch_doh_limit]
fofo_launch_inventory = fofo_launch_inventory[fofo_launch_inventory['in-npi'].isna()]
fofo_launch_inventory = fofo_launch_inventory[fofo_launch_inventory['last-90-days-sales-quantity']!= 0]

fofo_launch_inventory['excess-flag'] = 'fofo_launch_doh'
# Defining excess quantity and value
conditions = [(fofo_launch_inventory['excess-flag']=='fofo_launch_doh')]
choice = [fofo_launch_inventory['excess-defmin']]
fofo_launch_inventory['excess-quantity'] = np.select(conditions,choice, default=0)
fofo_launch_inventory['excess-quantity'] = fofo_launch_inventory['excess-quantity'].apply(np.floor)
fofo_launch_inventory['excess-value'] = (fofo_launch_inventory['workcell-value'].astype(float)/fofo_launch_inventory['quantity'].astype(float))*fofo_launch_inventory['excess-quantity'].astype(float)

fofo_launch_inventory['inventory-type'] = 'Rotate_fofo_launch_doh'

logger.info('end : Adding Launch stock DOH > 180 In FOFO')

inventory['max-with-cushion'] = inventory['max-time-x']
fofo_launch_inventory['max-with-cushion'] = fofo_launch_inventory['max-time-x']
categorisation = pd.concat([inventory,fofo_launch_inventory])
categorisation['created-at'] = cur_date
categorisation['created-by'] = 'data.science@zeno.health'
categorisation['updated-at'] = cur_date
categorisation['updated-by'] = 'data.science@zeno.health'

# =============================================================================
# Snapshot Queries
# =============================================================================

truncate_sns_query = '''
    delete from "prod2-generico"."excess-inventory-categorisation-sns"
    where "snapshot-date" = CURRENT_DATE +1 
  '''
insert_sns_query = ''' 
     insert
        into
        "prod2-generico"."excess-inventory-categorisation-sns"
            select
        CURRENT_DATE + 1 as "snapshot-date",
        "inventory-type",
        "store-id",
        "store-name",
        "drug-type",
        "goodaid-flag" ,
        sum("excess-quantity") as "excess-quantity" ,
        sum("excess-value") as "excess-value"
    from
        "prod2-generico"."excess-inventory-categorisation"
    group by
        "inventory-type",
        "store-id",
        "store-name",
        "drug-type",
        "goodaid-flag"
  '''

# =============================================================================
# Writing table to RS
# =============================================================================
try:
    schema = 'prod2-generico'
    table_name = 'excess-inventory-categorisation'
    table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)

    if isinstance(table_info, type(None)):
        raise Exception(f"table: {table_name} do not exist, create the table first")
    else:
        logger.info(f"Table:{table_name} exists")

        truncate_query = f''' delete
                            from "{schema}"."{table_name}" 
                            '''
        rs_db.execute(truncate_query)
        logger.info(str(table_name) + ' table old data deleted')

        s3.write_df_to_db(df=categorisation[table_info['column_name']], table_name=table_name, db=rs_db,
                          schema=schema)

        logger.info(str(table_name) + ' table uploaded')

        rs_db.execute(truncate_sns_query)
        rs_db.execute(insert_sns_query)
        logger.info(str(table_name) + 'snapshot' + ' table uploaded')

        status = True
except Exception as error:
    status = False
    raise Exception(error)



if status is True:
    mssg = 'Success'
else:
    mssg = 'Failed'

# =============================================================================
# Sending Email
# =============================================================================
end_time = datetime.datetime.now(tz=gettz('Asia/Kolkata'))
difference = end_time - start_time
min_to_complete = round(difference.total_seconds() / 60, 2)
email = Email()

email.send_email_file(subject=f"{env}-{mssg} : {table_name} table updated",
                      mail_body=f"{table_name} table updated, Time for job completion - {min_to_complete} mins ",
                      to_emails=email_to, file_uris=[])

rs_db.close_connection()
