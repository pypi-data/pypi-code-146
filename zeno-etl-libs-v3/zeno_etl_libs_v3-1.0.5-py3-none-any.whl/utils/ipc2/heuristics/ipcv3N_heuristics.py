import pandas as pd
import numpy as np
import datetime as datetime
from datetime import timedelta
from zeno_etl_libs.utils.ipc2.config_ipc import key_col, date_col, store_col, drug_col, target_col

def load_data(store_id,start_d, end_d,db,schema):

    mos = f''' select * from "{schema}".sales
            where date("created-at") >= '{start_d}' and date("created-at") < '{end_d}'  and "store-id" in ({store_id}) '''

    cfr = f'''select cpr."store-id" , cpr."drug-id" , cpr."shortbook-date", sum("loss-quantity") as "loss-quantity"  from 
    "{schema}"."cfr-patient-request" cpr 
    where "shortbook-date" >= '{start_d}' and "shortbook-date" < '{end_d}'
    and cpr."drug-id" <> -1 
    and ("drug-category" = 'chronic' or "repeatability-index" >= 40)
    and "loss-quantity" > 0 
    and "drug-type" in ('ethical', 'ayurvedic', 'generic', 'discontinued-products', 'banned', 'general', 'high-value-ethical', 'baby-product', 'surgical', 'otc', 'glucose-test-kit', 'category-2', 'category-1', 'category-4', 'baby-food', '', 'category-3')
    and "store-id" in ({store_id})
    group by cpr."store-id" , cpr."drug-id" , "shortbook-date" '''

    df_mos = db.get_df(mos)
    df_cfr = db.get_df(cfr)
    df_mos.columns = [c.replace('-', '_') for c in df_mos.columns]
    df_cfr.columns = [c.replace('-', '_') for c in df_cfr.columns]

    return df_mos,df_cfr

def pre_process_data(df_mos,df_cfr):

    set_dtypes = {
    store_col: int,
    drug_col: int,
    'loss_quantity': int
    }
    df_cfr = df_cfr.astype(set_dtypes)
    df_cfr['shortbook_date'] = pd.to_datetime(df_cfr['shortbook_date'])
    df_mos['created_at'] = pd.to_datetime(df_mos['created_at'])
    df_mos['sales_date'] = pd.to_datetime(df_mos['created_at'].dt.date)
    df_mos['drug_id'].fillna(0,inplace=True)
    df_mos['ts_id'] = df_mos['store_id'].astype(int).astype(str) + "_" + df_mos['drug_id'].astype(int).astype(str)
    df_mos = df_mos.groupby(['ts_id', 'sales_date', 'store_id', 'drug_id' ])['net_quantity'].sum().reset_index()
    df_mos.rename(columns={'sales_date':date_col},inplace=True)
    df_mos.rename(columns={'net_quantity':target_col},inplace=True)

    return df_mos, df_cfr

def get_formatted_data(df, key_col, date_col, store_col, drug_col, target_col):

    df = df[[key_col, date_col, target_col]]
    min_date = df[date_col].dropna().min()
    end_date = df[date_col].dropna().max()
    date_range = []
    date_range = pd.date_range(
        start= min_date,
        end= end_date,
        freq= 'd'
    )
    date_range = list(set(date_range) - set(df[date_col]))

    df = (
        df
        .groupby([date_col] + [key_col])[target_col]
        .sum()
        .unstack()
    )

    for date in date_range:
        df.loc[date, :] = np.nan

    df = (
        df
        .fillna(0)
        .stack()
        .reset_index()
        .rename(columns = {0: target_col})
    )

    df[[store_col, drug_col]] = df[key_col].str.split('_', expand = True)
    df[[store_col, drug_col]] = df[[store_col, drug_col]].astype(float).astype(int)
    return df

def aggreagte_data(df_sales, df_cfr):

    df = df_sales.merge(df_cfr,
                    left_on=[store_col, drug_col, date_col],
                    right_on=[store_col, drug_col, 'shortbook_date'],
                    how='left')
    df[date_col] = df[date_col].combine_first(df['shortbook_date'])
    df[target_col].fillna(0, inplace=True)
    df['loss_quantity'].fillna(0, inplace=True)
    df[target_col] += df['loss_quantity']
    df.drop(['shortbook_date', 'loss_quantity'], axis=1, inplace=True)
    df_l3m_sales = df.groupby([store_col,drug_col])[target_col].sum().reset_index()
    df_l3m_sales.rename(columns={target_col:'l3m_sales_qty'},inplace=True)

    return df_l3m_sales


def implement_corrections(final_ss_df,df_l3m_sales):
    cols = final_ss_df.columns
    df = pd.merge(final_ss_df,df_l3m_sales,how='left', on=[store_col,drug_col] )
    df['fcst_zero_w_sales'] = np.where(((df['fcst']==0)&(df['l3m_sales_qty']>0)&(df['order_upto_point']==0)),1, 0)
    df['order_upto_point'] = np.where(df['fcst_zero_w_sales']==1,np.round((df['l3m_sales_qty']/3)*(18/30)), df['order_upto_point'])
    df['order_upto_point'] = np.where(((df['fcst_zero_w_sales']==1)&(df['l3m_sales_qty']==2)&(df['order_upto_point']==0)),1, df['order_upto_point'])
    df['reorder_point'] = np.where(df['fcst_zero_w_sales']==1,np.floor((df['l3m_sales_qty']/3)*(13/30)), df['reorder_point'])
    df['reorder_point'] = np.where((df['fcst_zero_w_sales']==1)&(df['reorder_point']==df['order_upto_point'])&(df['reorder_point']>0),df['order_upto_point']-1, df['reorder_point'])
    df['safety_stock'] = np.where(df['fcst_zero_w_sales']==1,np.floor((df['l3m_sales_qty']/3)*(7/30)), df['safety_stock'])
    df = df[cols]
    return df

def v3N_corrections(final_ss_df, store_id, reset_date, schema, db, logger):

    end_d = pd.to_datetime(reset_date)
    start_d = end_d - timedelta(days= 90)
    start_d = str(start_d.date())
    end_d = str(end_d.date())

    df_mos,df_cfr = load_data(store_id=store_id,start_d=start_d, end_d=end_d,db=db,schema=schema)
    df_mos, df_cfr = pre_process_data(df_mos=df_mos, df_cfr=df_cfr)
    df_sales = get_formatted_data(df=df_mos, key_col=key_col, date_col = date_col, target_col=target_col, store_col=store_col, drug_col=drug_col)
    df_l3m_sales = aggreagte_data(df_sales=df_sales, df_cfr = df_cfr)
    final_ss_df = implement_corrections(final_ss_df=final_ss_df, df_l3m_sales=df_l3m_sales)
    
    return final_ss_df