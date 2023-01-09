"""
Author : shubham.gupta@zeno.health
Purpose : Store Intelligence and Daily recommendation
"""

# Essential Libraries

# Warnings
from warnings import filterwarnings as fw

import pandas as pd

fw('ignore')

import argparse
import os
import sys

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper.email.email import Email

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
parser.add_argument('-et', '--email_to', default="shubham.gupta@zeno.health", type=str, required=False)
parser.add_argument('-scm', '--email_to_sc', default="soumya.pattnaik@zeno.health", type=str, required=False)
parser.add_argument('-odc', '--oos_day_count', default=5, type=str, required=False)
parser.add_argument('-iud', '--inv_update_day', default=2, type=str, required=False)
parser.add_argument('-debug', '--debug_mode', default='N', type=str, required=False)
parser.add_argument('-as', '--active_stores', default="all", type=str, required=False)

args, unknown = parser.parse_known_args()
env = args.env
os.environ['env'] = env

# parameters
email_to = args.email_to
email_to = email_to.split(',')
email_to_sc = args.email_to_sc
odc = args.oos_day_count
iud = args.inv_update_day
debug = args.debug_mode
active_stores = args.active_stores

logger = get_logger()
logger.info(f"env: {env}")

rs_db = DB()
rs_db.open_connection()

s3 = S3()
read_schema = "prod2-generico"
email = Email()

if active_stores == 'all':
    stores_q = """select
                    id
                from
                    "prod2-generico".stores s
                where
                    "is-active" = 1
                    and category = 'retail';"""

    all_stores = rs_db.get_df(stores_q)
    active_stores = all_stores['id'].unique()
    active_stores = tuple(map(int, active_stores))
else:
    active_stores = active_stores.split(',') + ['0']
    active_stores = tuple(map(int, active_stores))


################################################################
###################### Helper Functions ########################
################################################################

def store_info_func(store_id):
    """
    This basic function return store name and emails
    """
    rs_db_h = DB(read_only=True)
    rs_db_h.open_connection()

    store_q = f"""select
                    sm.id,
                    sm.store as "store-name",
                    sm."store-email",
                    sm."line-manager",
                    sm."line-manager-email",
                    sm.abo,
                    sm."abo-email",
                    sm."store-manager",
                    sm."store-manager-email",
                    s."franchisee-email" 
                from
                    "{read_schema}"."stores-master" sm 
                left join "{read_schema}".stores s on sm.id = s.id 
                where sm.id = {store_id};
            """
    store_info = rs_db.get_df(store_q)
    try:
        store_info = store_info.iloc[0]
        store_name = store_info["store-name"]
        store_mails = []
        for col in ["store-email", "line-manager-email", "abo-email", "store-manager-email", "franchisee-email"]:
            if '@' in str(store_info[col]):
                store_mails.append(store_info[col])
    except:
        store_name = "store not exist"
        store_mails = ["shubham.gupta@zeno.health"]
    return store_name, store_mails


logger.info(f"script running for stores_ids : {active_stores}")
for store_id in active_stores:
    logger.info(f"store name : {store_info_func(store_id)[0]}")
    logger.info(f"store emails : {store_info_func(store_id)[1]}")

#################################################################
###################### OOS and Inventory ########################
#################################################################
logger.info("OOS and Inventory Issue Started")
oos_q = f"""
        select
            t_final.*,
            d."drug-name" as "drug-name"
        from
            (
            select
                t."store-id",
                t."drug-id",
                min(t."closing-date") "from-date",
                max(t."closing-date") "to-date",
                datediff('days', min(t."closing-date"), max(t."closing-date")) + 1 as "days-count"
            from
                (
                select
                    * ,
                    row_number() over (partition by "store-id",
                    "drug-id"
                order by
                    "closing-date" desc) as "rn",
                    dateadd('days',
                    "rn",
                    "closing-date") "plus-date"
                from
                    "{read_schema}"."out-of-shelf-drug-level" oosdl
                where
                    "oos-count" = 1
                    and "max-set" = 'Y'
                    and "mature-flag" = 'Y') t
            where
                date("plus-date") = current_date
                and t."store-id" in {active_stores}
            group by
                t."store-id",
                t."drug-id"
            having
                "days-count" > {odc}) t_final
        left join 
            "{read_schema}".stores s on
            t_final."store-id" = s.id
        left join 
            "{read_schema}".drugs d on
            t_final."drug-id" = d.id
        left join "{read_schema}"."drug-substitution-mapping" dsm1 on
            t_final."drug-id" = dsm1."drug-id"
        left join (
            select
                i."store-id",
                dsm2."group",
                sum(quantity) "total-quantity"
            from
                "{read_schema}"."inventory-1" i
            left join "{read_schema}"."drug-substitution-mapping" dsm2 on
                i."drug-id" = dsm2."drug-id"
            group by
                i."store-id",
                dsm2."group") t_dsm on
            t_dsm."group" = dsm1."group" and t_final."store-id" = t_dsm."store-id"
        where
            t_dsm."total-quantity" = 0;
        """

sales_loss_q = f"""
                select 	
                    tw."store-id",
                    tw."drug-id",
                    min(tw."closing-date") "from-date",
                    max(tw."closing-date") "to-date",
                    datediff('days', min(tw."closing-date"), max(tw."closing-date")) + 1 as "days-count",
                    sum(s."revenue-value") as "total-sales"
                from
                    (
                    select
                        *,
                        rank() over (partition by "store-id",
                        "drug-id"
                    order by
                        "plus-date" desc) as "latest-rank"
                    from
                        (
                        select
                            * ,
                            row_number() over (partition by "store-id",
                            "drug-id"
                        order by
                            "closing-date" desc) as "rn",
                            dateadd('days',
                            "rn",
                            "closing-date") "plus-date"
                        from
                             "{read_schema}"."out-of-shelf-drug-level" oosdl
                        where
                            "oos-count" = 0) t ) tw
                left join  "{read_schema}".sales s on
                    date(s."created-at") = tw."closing-date"
                    and s."drug-id" = tw."drug-id"
                    and s."store-id" = tw."store-id"
                where 
                    "latest-rank" = 1
                    and "plus-date" != current_date
                group by 
                    tw."store-id",
                    tw."drug-id";
                """

oos = rs_db.get_df(oos_q)
sales_loss = rs_db.get_df(sales_loss_q)

sales_loss['avg-per-day-sales'] = sales_loss['total-sales'] / sales_loss['days-count']
sales_loss = sales_loss[['store-id', 'drug-id', 'avg-per-day-sales']]
oos = pd.merge(oos, sales_loss, how='left', on=['store-id', 'drug-id'])
oos = oos.dropna(subset=['avg-per-day-sales'])
oos['avg-per-day-sales'] = oos['avg-per-day-sales'].astype(float).round(2)
oos['sales-loss'] = oos['avg-per-day-sales'] * oos['days-count']

# Let's solve issues for top 20 only for a day

oos = oos.sort_values('sales-loss', ascending=False).head(20)
store_ids = oos['store-id'].unique()

oos_mail_body = """
Hey {store_name},
There are some drugs which are out of stock on your store for very long time
Plus these are the drugs which don't have any alternative available on store

Possible issues are as listed :

1. Auto Short not triggered
2. Short in market 
3. Quantity in locked state (Store inventory)

Because of these specific drugs OOS of your store is high
Your daily task for today is resolve these issues :

Step 1. Copy-Paste drug name from the sheet into compare tab
Step 2. Check its best alternative - 1 Generic, 1 Ethical
Step 3a). Create a manual short of the best alternative in 1 quantity ( 1 Ethical, 1 Generic)
Step 3b) If an Alternate is not available just raise MS for the same drug which is mentioned.

"""

logger.info(f"OOS mail sending to following stores {store_ids}")
if debug == 'N':
    for store_id in store_ids:
        store_name, store_emails = store_info_func(store_id)
        for other_email in email_to:
            store_emails.append(other_email)
        if store_name != "store not exist":
            store_emails.append(email_to_sc)
        file_name = 'OOS_Drugs.xlsx'
        file_path = s3.write_df_to_excel(data={'Drugs': oos[oos['store-id'] == store_id]}, file_name=file_name)
        email.send_email_file(subject="Store Daily Insight 1 : Unavailability Issue",
                              mail_body=oos_mail_body.format(store_name=store_name),
                              to_emails=store_emails,
                              file_uris=[],
                              file_paths=[file_path])
        logger.info(f"OOS issue mail sent to {store_name} store on following emails : {store_emails}")
if debug == 'Y':
    store_name, store_emails = 'Debugger', ['shubham.gupta@zeno.health']
    file_name = 'OOS_Drugs.xlsx'
    file_path = s3.write_df_to_excel(data={'Drugs': oos}, file_name=file_name)
    email.send_email_file(subject="Store Daily Insight 1 : Unavailability Issue",
                          mail_body=oos_mail_body.format(store_name=store_name),
                          to_emails=store_emails,
                          file_uris=[],
                          file_paths=[file_path])

inv_q = f"""
            select
                i."store-id",
                s."name" as "store-name", 
                i."drug-id",
                d."drug-name", 
                sum(i.quantity) as "quantity",
                sum(i."locked-quantity") as "locked-quantity",
                sum(i."locked-for-check") as "locked-for-check",
                sum(i."locked-for-audit") as "locked-for-audit",
                sum(i."locked-for-return") as "locked-for-return",
                sum(i."locked-for-transfer") as "locked-for-transfer",
                sum(i."extra-quantity") as "extra-quantity",
                max(i."updated-at") as "updated-at"
            from
                "{read_schema}"."inventory-1" i
            left join "{read_schema}".stores s on
                s.id = i."store-id"
            left join "{read_schema}".drugs d on
                d.id = i."drug-id"
            where i."store-id" in {active_stores}
            group by
                i."store-id",
                s."name", 
                i."drug-id",
                d."drug-name" 
            having
                sum(i."quantity") = 0
                and sum(i."locked-quantity" + i."locked-for-check" + i."locked-for-audit" + i."locked-for-return" + i."locked-for-transfer" + i."extra-quantity") > 0
                and max(i."updated-at") <= current_date - {iud}
            order by
                "updated-at" 
            limit 20;
        """
inv = rs_db.get_df(inv_q)

# Taking out all stores
store_ids = inv['store-id'].unique()

inv_mail_body = """
Hey {store_name},

There are some drugs in your store where system available quantity is shown as 0, 
so not available for sale, but their quantity is stuck in locked state
since long time which cause trouble in triggering Auto Short

Your daily task for today is resolve these issues : Please reach out to ABO or tech-support for any doubts.

> Unlock mentioned drugs

"""
logger.info(f"Inventory mail sending to following stores {store_ids}")
if debug == 'N':
    for store_id in store_ids:
        store_name, store_emails = store_info_func(store_id)
        for other_email in email_to:
            store_emails.append(other_email)
        file_name = 'Locked State Drugs.xlsx'
        file_path = s3.write_df_to_excel(data={'Drugs': inv[inv['store-id'] == store_id]}, file_name=file_name)
        email.send_email_file(subject="Store Daily Insight 2 : Inventory locked Issue",
                              mail_body=inv_mail_body.format(store_name=store_name),
                              to_emails=store_emails,
                              file_uris=[],
                              file_paths=[file_path])
        logger.info(f"Inventory issue mail sent to {store_name} store on following emails : {store_emails}")
if debug == 'Y':
    store_name, store_emails = 'Debugger', ['shubham.gupta@zeno.health']
    file_name = 'Locked State Drugs.xlsx'
    file_path = s3.write_df_to_excel(data={'Drugs': inv}, file_name=file_name)
    email.send_email_file(subject="Store Daily Insight 2 : Inventory locked Issue",
                          mail_body=inv_mail_body.format(store_name=store_name),
                          to_emails=store_emails,
                          file_uris=[],
                          file_paths=[file_path])
logger.info("OOS and Inventory Issue Finished")
#################################################################
###################### Substitution  ############################
#################################################################
logger.info("Generic Issue Started")
gen_shift_q = """
                select
                    "primary-store-id" as "store-id",
                    (case
                        when "post-generic-quantity" > 0 then 'generic-shift'
                        when "post-generic-quantity" = 0
                        and "post-ethical-quantity" > 0 then 'still-ethical'
                        else 'bought others'
                    end
                    ) "behaviour-shift",
                    count(distinct t1."patient-id") "patient-count"
                from
                    (
                    select
                        "patient-id",
                        sum("quantity-ethical") "pre-ethical-quantity",
                        sum("quantity-generic") "pre-generic-quantity"
                    from
                        "prod2-generico"."retention-master" rm
                    where
                        "created-at" < date_trunc('month', current_date)
                        and "created-at" >= dateadd('month',
                        -3,
                        date_trunc('month', current_date))
                    group by
                        "patient-id"
                    having
                        "pre-ethical-quantity" > 0
                        and "pre-generic-quantity" = 0 ) t1
                inner join
                (
                    select
                        "patient-id",
                        "primary-store-id",
                        sum("quantity-ethical") "post-ethical-quantity",
                        sum("quantity-generic") "post-generic-quantity"
                    from
                        "prod2-generico"."retention-master" rm
                    where
                        "created-at" >= date_trunc('month', current_date)
                    group by
                        "primary-store-id",
                        "patient-id") t2
                on
                    t1."patient-id" = t2."patient-id"
                group by
                    "primary-store-id",
                    "behaviour-shift"
                    """

gen_shift = rs_db.get_df(gen_shift_q)

gen_shift_dist = pd.crosstab(index=gen_shift['store-id'],
                             columns=gen_shift['behaviour-shift'],
                             values=gen_shift['patient-count'],
                             aggfunc='sum', normalize='index')

# i = issue
gen_shift_dist_i = gen_shift_dist[gen_shift_dist['generic-shift'] < gen_shift_dist['generic-shift'].quantile(0.05)]

store_ids = gen_shift_dist_i.index

store_ids = list(set.intersection(set(store_ids), set(active_stores)))
logger.info(f"Active generic subs mail sending to following stores {store_ids}")
for store_id in store_ids:
    store_name, store_emails = store_info_func(store_id)
    if debug == 'Y':
        store_emails = ['shubham.gupta@zeno.health']
    else:
        for other_email in email_to:
            store_emails.append(other_email)
    gen_mail_body = f"""
    Hey {store_name} Store,
    Your store is in Top stores where generic substitution is lower for active consumer
    System average for active customer generic shift is  :  {gen_shift_dist['generic-shift'].quantile(0.5).round(4) * 100} %
    Your store performance : {gen_shift_dist_i.loc[store_id]['generic-shift'].round(4) * 100} %
    
    Your Daily task to resolve this issues :
    
    > Focus on substitution for active customers 
    > Pitch Generic to customer whose generic affinity is lower (Visible on billing panel)
    """

    file_name = 'Substitution active consumer.xlsx'
    file_path = s3.write_df_to_excel(data={'Drugs': gen_shift_dist_i.loc[store_id]}, file_name=file_name)
    email.send_email_file(subject="Store Daily Insight 3 : Active Consumer substitution Issue",
                          mail_body=gen_mail_body,
                          to_emails=store_emails,
                          file_uris=[],
                          file_paths=[file_path])
    logger.info(f"Active generic subs issue mail sent to {store_name} store on following emails : {store_emails}")
logger.info("Generic Issue Finished")
#################################################################
############################ Sales  #############################
#################################################################
logger.info("Sales De-growth Issue Started")
sale_tq = """select
                s."store-id",
                sum(case 
                    when s."created-at" >= date_trunc('month', current_date)
                    and s."created-at" <= current_date then s."revenue-value" else 0 end) "MTD-Sales",
                sum(case when s."created-at" >= dateadd('month', -1, date_trunc('month', current_date))
                    and s."created-at" <= dateadd('month', -1, current_date) then s."revenue-value" else 0 end) "LMTD-Sales",
                "MTD-Sales" - "LMTD-Sales" as "sales-diff",
                ("MTD-Sales" - "LMTD-Sales") / "LMTD-Sales" as "perc diff"
            from
                "prod2-generico".sales s
            left join "prod2-generico".stores s2 on
                s."store-id" = s2.id
            where
                s2."is-active" = 1
                and s2."franchisee-id" = 1
            group by
                s."store-id"
            having
                "sales-diff" < 0
                and "LMTD-Sales" != 0
                and min(s."created-at") < dateadd('month', -1, date_trunc('month', current_date))
            order by
                5
            limit 10"""

sale_t = rs_db.get_df(sale_tq)

store_ids = sale_t["store-id"].unique()
store_ids = list(set.intersection(set(store_ids), set(active_stores)))

for store_id in store_ids:
    store_name, store_emails = store_info_func(store_id)
    if debug == 'Y':
        store_emails = ['shubham.gupta@zeno.health']
    else:
        for other_email in email_to:
            store_emails.append(other_email)
    target = sale_t[sale_t["store-id"] == store_id]["sales-diff"].values[0]
    sales_mail_body = f"""
    Hey {store_name} Store,
    Your store is in Top stores in terms of sales de-growth 

    To exit from this phase you need to complete this sales target for today : {abs(target)}
    """

    email.send_email_file(subject="Store Daily Insight 4 : Sales target for de-growing stores",
                          mail_body=sales_mail_body,
                          to_emails=store_emails,
                          file_uris=[],
                          file_paths=[])
logger.info("Sales De-growth Issue Finished")
#################################################################
############################ Substitution  ######################
#################################################################
logger.info("Substitution Issue Started")
sub_q = """
        select
            "store-id",
            "store-name",
            composition, 
            sum(case when "substitution-status" = 'substituted' then 1.0 * quantity end)/ sum(case when "substitution-status" in ('substituted', 'not-substituted') then quantity end) as "substitution"
        from
            "prod2-generico".sales s
        where
            date("created-at") between current_date - 90 and current_date
        group by
            "store-id",
            "store-name",
            composition
        having
            "substitution" is not null;
        """

sub = rs_db.get_df(sub_q)

sub['substitution'] = sub['substitution'].astype(float)
sub05 = sub.groupby('composition', as_index=False).agg({'substitution': lambda x: x.quantile(0.05)})
sub05.rename(columns={'substitution': 'sub_05'}, inplace=True)
sub_system = sub.groupby('composition', as_index=False).agg({'substitution': lambda x: x.quantile(0.5)})
sub_system.rename(columns={'substitution': 'System Average'}, inplace=True)

sub = pd.merge(sub, sub05, on=['composition'], how='inner')
sub = pd.merge(sub, sub_system, on=['composition'], how='inner')

sub = sub[sub['substitution'] < sub['sub_05']]

sub.drop(columns=['sub_05'], inplace=True)
sub = sub.sort_values('substitution', ascending=True).head(50)
sub['substitution'] = sub['substitution'].apply(lambda x: str(x * 100) + '%')
sub['System Average'] = sub['System Average'].apply(lambda x: str(x * 100) + '%')
store_ids = sub['store-id'].unique()
store_ids = list(set.intersection(set(store_ids), set(active_stores)))
for store_id in store_ids:
    store_name, store_emails = store_info_func(store_id)
    if debug == 'Y':
        store_emails = ['shubham.gupta@zeno.health']
    else:
        for other_email in email_to:
            store_emails.append(other_email)

    sub_mail_body = f"""
    Hey {store_name} Store,
    There are some composition where your store is not performing well in terms of substitution,
    compare to other stores
    Please download the list and try to do active substitution for mentioned composition 

    """
    file_name = 'Substitution Composition.xlsx'
    file_path = s3.write_df_to_excel(data={'Drugs': sub[sub['store-id'] == store_id]}, file_name=file_name)

    email.send_email_file(subject="Store Daily Insight 5 : Composition substitution",
                          mail_body=sub_mail_body,
                          to_emails=store_emails,
                          file_uris=[],
                          file_paths=[file_path])
logger.info("Substitution Issue Finished")

#################################################################
######################### SKUs short in Market ##################
#################################################################
## Adding query for now - Create module after feedback from Soumya and Saniya
# select
# 	sm.store,
# 	t1.*,
# 	d.id as "best-substitute-drug-id",
# 	d."drug-name" as "best-substitute-drug-name"
# from
# 	(
# 	select
# 		sbx."store-id",
# 		sbx."drug-id",
# 		sbx."drug-name",
# 		max(sbx."created-at") "last-failed"
# 	from
# 		(
# 		select
# 			*,
# 			(case
# 				when status in ('lost', 'failed', 'declined') then 1.0
# 				else 0.0
# 			end) "status-code",
# 			rank() over( partition by "store-id",
# 			"drug-id"
# 		order by
# 			"created-at" desc) as "ORank"
# 		from
# 			"short-book-1" sb
# 		where
# 			date("created-at") between current_date-30 and current_date
# 			) sbx
# 	where
# 		sbx."orank" <= 3
# 		and sbx."drug-id" is not null
# 	group by
# 		sbx."store-id",
# 		sbx."drug-id",
# 		sbx."drug-name"
# 	having
# 		avg(sbx."status-code")= 1
# 		and max(sbx."orank") >= 3
# 		) t1
# left join "drug-substitution-mapping" dsm1 on
# 	t1."drug-id" = dsm1."drug-id"
# left join (
# 	select
# 		i."store-id",
# 		dsm2."group",
# 		dsm2."drug-id",
# 		sum(i.quantity) as "total-quantity",
# 		dense_rank() over( partition by i."store-id",
# 		dsm2."group"
# 	order by
# 		"total-quantity" desc) as "gRank"
# 	from
# 		"drug-substitution-mapping" dsm2
# 	left join "inventory-1" i on
# 		dsm2."drug-id" = i."drug-id"
# 	group by
# 		i."store-id",
# 		dsm2."group",
# 		dsm2."drug-id"
# 	having
# 		sum(i.quantity) > 0) t2 on
# 	t2."group" = dsm1."group"
# 	and t2."store-id" = t1."store-id"
# left join drugs d on
# 	t2."drug-id" = d.id
# left join "drug-order-info" doi on
# 	t1."drug-id" = doi."drug-id"
# 	and t1."store-id" = doi."store-id"
# left join "stores-master" sm on
# 	sm.id = t1."store-id"
# where
# 	t2."gRank" = 1
# 	and t1."drug-id" != t2."drug-id"
# 	and doi."as-active" = 1
# 	and doi."max" > 0
# order by
# 	5 desc
# limit 20;
