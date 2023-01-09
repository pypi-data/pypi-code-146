import pandas as pd
import numpy as np


def post_processing(store_id, safety_stock_df, seg_df_comb_lvl, seg_df_drug_lvl,
                    schema, db, logger):
    seg_df_comb_lvl[['store_id', 'comb_id']] = seg_df_comb_lvl['ts_id'].str.split('_', expand=True)
    seg_df_drug_lvl[['store_id', 'drug_id']] = seg_df_drug_lvl['ts_id'].str.split('_', expand=True)
    seg_df_drug_lvl['store_id'] = seg_df_drug_lvl['store_id'].astype(int)
    seg_df_drug_lvl['drug_id'] = seg_df_drug_lvl['drug_id'].astype(int)

    list_drugs = safety_stock_df['drug_id'].tolist()
    str_drugs = str(list_drugs).replace('[', '(').replace(']', ')')

    q_drug_info = f"""
            select d.id as drug_id, "drug-name" as drug_name, type, composition
            from "{schema}".drugs d 
            where d.id in {str_drugs}
            """
    df_drug_info = db.get_df(q_drug_info)

    # get store name
    q_store_name = f""" select name from "{schema}".stores where id = {store_id} """
    store_name = db.get_df(q_store_name)['name'][0]

    # get current inventory and avg_ptr info
    q_inv = f"""
                select "drug-id" as drug_id, sum("locked-quantity"+quantity+
                    "locked-for-audit"+"locked-for-transfer"+"locked-for-check"+
                    "locked-for-return") as curr_inventory
                from "{schema}"."inventory-1" i 
                where "store-id" = {store_id}
                and "drug-id" in {str_drugs}
                group by "drug-id" 
                """
    df_inv = db.get_df(q_inv)

    q_avg_ptr_store = f"""
                select "drug-id" as drug_id, avg(ptr) as avg_ptr
                from "{schema}"."inventory-1" i 
                where "store-id" = {store_id}
                and "drug-id" in {str_drugs}
                and DATEDIFF(day, date("created-at"), current_date) < 365
                group by "drug-id" 
                """
    df_avg_ptr_store = db.get_df(q_avg_ptr_store)

    q_avg_ptr_sys = f"""
                select "drug-id" as drug_id, "avg-ptr" as avg_ptr_sys
                from "{schema}"."drug-std-info" dsi 
                """
    df_avg_ptr_sys = db.get_df(q_avg_ptr_sys)

    # add all to ss table
    safety_stock_df['store_id'] = store_id
    safety_stock_df['store_name'] = store_name
    safety_stock_df = safety_stock_df.merge(
        df_drug_info, on='drug_id', how='left')
    safety_stock_df = safety_stock_df.merge(
        df_inv, on='drug_id', how='left')
    safety_stock_df = safety_stock_df.merge(
        df_avg_ptr_store, on='drug_id', how='left')
    safety_stock_df = safety_stock_df.merge(
        df_avg_ptr_sys, on='drug_id', how='left')

    # replace NA in avg_ptr with system-avg_ptr
    safety_stock_df["avg_ptr"] = np.where(safety_stock_df["avg_ptr"].isna(),
                                          safety_stock_df["avg_ptr_sys"],
                                          safety_stock_df["avg_ptr"])
    safety_stock_df.drop("avg_ptr_sys", axis=1, inplace=True)
    safety_stock_df["avg_ptr"] = safety_stock_df["avg_ptr"].astype(float)

    # calculate DOH
    safety_stock_df['fcst'] = safety_stock_df['fcst'].fillna(0)
    safety_stock_df['safety_stock_days'] = np.where(
        (safety_stock_df['fcst'] == 0) | (safety_stock_df['safety_stock'] == 0),
        0, safety_stock_df['safety_stock'] / (safety_stock_df['fcst'] / 28))
    safety_stock_df['reorder_days'] = np.where(
        (safety_stock_df['fcst'] == 0) | (safety_stock_df['reorder_point'] == 0),
        0, safety_stock_df['reorder_point'] / (safety_stock_df['fcst'] / 28))
    safety_stock_df['order_upto_days'] = np.where(
        (safety_stock_df['fcst'] == 0) | (safety_stock_df['order_upto_point'] == 0),
        0, safety_stock_df['order_upto_point'] / (safety_stock_df['fcst'] / 28))

    # calculate max-value, to-order-qty and to-order-val
    safety_stock_df["max_value"] = safety_stock_df['order_upto_point'] * \
                                   safety_stock_df['avg_ptr']

    safety_stock_df['curr_inventory'] = safety_stock_df['curr_inventory'].fillna(0)
    safety_stock_df['to_order_quantity'] = np.where(
        safety_stock_df['curr_inventory'] <= safety_stock_df['reorder_point'],
        safety_stock_df['order_upto_point'] - safety_stock_df['curr_inventory'],
        0)
    safety_stock_df['to_order_value'] = safety_stock_df['to_order_quantity'] * \
                                        safety_stock_df['avg_ptr']

    safety_stock_df = safety_stock_df[[
        'store_id', 'store_name', 'comb_id', 'fcst_source', 'map_type', 'fcst_wt',
        'bucket', 'model', 'drug_id', 'drug_name', 'type', 'composition',
        'fcst', 'std', 'lead_time_mean', 'lead_time_std',
        'safety_stock', 'reorder_point', 'order_upto_point', 'correction_flags',
        'curr_inventory', 'avg_ptr', 'safety_stock_days', 'reorder_days',
        'order_upto_days', 'max_value', 'to_order_quantity', 'to_order_value']]

    # formatting segmentation table
    seg_df_comb_lvl.rename(columns={'std': 'sales_std', 'cov': 'sales_cov',
                           'Mixed': 'bucket', 'Group': 'group',
                           'PLC Status L1': 'plc_status', 'ADI': 'adi',
                           'total_LY_sales': 'total_ly_sales',
                           'start_date': 'sale_start_date'}, inplace=True)
    seg_df_comb_lvl['sale_start_date'] = seg_df_comb_lvl['sale_start_date'].dt.date
    seg_df_comb_lvl['store_name'] = store_name

    seg_df_drug_lvl.rename(columns={'std': 'sales_std', 'cov': 'sales_cov',
                                    'Mixed': 'bucket', 'Group': 'group',
                                    'PLC Status L1': 'plc_status', 'ADI': 'adi',
                                    'total_LY_sales': 'total_ly_sales',
                                    'start_date': 'sale_start_date'},
                           inplace=True)
    seg_df_drug_lvl['sale_start_date'] = seg_df_drug_lvl[
        'sale_start_date'].dt.date
    seg_df_drug_lvl['store_name'] = store_name

    return safety_stock_df, seg_df_comb_lvl, seg_df_drug_lvl
