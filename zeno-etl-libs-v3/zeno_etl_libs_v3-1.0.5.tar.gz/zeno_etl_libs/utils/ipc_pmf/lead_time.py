import numpy as np
import datetime as dt

"""
Steps -
1. Get Auto short total time -> from creation to received at store
2. If marked as lost make it 7 days
3. Max LT capped at 7 days
"""


def lead_time(store_id, reset_date, db, schema, logger=None):
    end_date = str((
        dt.datetime.strptime(reset_date, '%Y-%m-%d') -
        dt.timedelta(7)).date())
    begin_date = str((
        dt.datetime.strptime(reset_date, '%Y-%m-%d') -
        dt.timedelta(97)).date())

    logger.info("Lead Time Calculation Starts")
    logger.info(f"SB Begin Date: {begin_date}, SB End Date: {end_date}")

    lead_time_query = f"""
            select "store-id" , "drug-id" , "type" , status , "created-to-delivery-hour" as "lt-hrs"
            from "{schema}"."as-ms" am 
            where "as-ms" = 'AS'
            and "store-id" = {store_id}
            and date("created-at") <= '{end_date}'
            and date("created-at") >= '{begin_date}'
            and status not in ('failed', 'deleted')
            """
    lead_time = db.get_df(lead_time_query)
    lead_time.columns = [c.replace('-', '_') for c in lead_time.columns]

    # classify all types into generic, ethical & others
    lead_time["type"] = np.where(
        lead_time["type"].isin(['ethical', 'high-value-ethical']), 'ethical',
        lead_time["type"])
    lead_time["type"] = np.where(lead_time["type"].isin(['ethical', 'generic']),
                                 lead_time["type"], 'others')

    lead_time["lt_days"] = lead_time["lt_hrs"] / 24
    lead_time["lt_days"] = lead_time["lt_days"].fillna(7)
    lead_time["lt_days"] = np.where(lead_time["lt_days"] > 7, 7, lead_time["lt_days"])

    lt_store_mean = np.ceil(lead_time.lt_days.mean())
    lt_store_std = round(lead_time.lt_days.std(ddof=0), 2)

    lt_drug = lead_time.groupby('drug_id'). \
        agg({'lt_days': [np.mean, np.std]}).reset_index()
    lt_drug.columns = ['drug_id', 'lead_time_mean', 'lead_time_std']
    lt_drug['lead_time_std'] = np.where(
        lt_drug['lead_time_std'].isin([0, np.nan]),
        lt_store_std, lt_drug['lead_time_std'])

    lt_drug["lead_time_mean"] = np.ceil(lt_drug["lead_time_mean"])
    lt_drug['lead_time_std'] = round(lt_drug['lead_time_std'], 2)

    logger.info("Lead Time Calculation Completed")

    return lt_drug, lt_store_mean, lt_store_std




