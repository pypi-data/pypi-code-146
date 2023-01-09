import pandas as pd
import numpy as np
import datetime as dt
from zeno_etl_libs.helper.google.sheet.sheet import GoogleSheet
from zeno_etl_libs.utils.ipc_pmf.config_ipc_combination import *


def fcst_comb_drug_map(store_id, reset_date, comb_fcst_df, drug_fcst_df,
                       type_list_comb_lvl, schema, db, logger):
    # Round off forecast values
    comb_fcst_df['fcst'] = np.round(comb_fcst_df['fcst'])
    comb_fcst_df = comb_fcst_df.loc[comb_fcst_df['fcst'] > 0]

    # Read assortment from GSheet
    gs = GoogleSheet()
    spreadsheet_id = "1tFHCTr3CHdb0UOFseK_ntjAUJSHQHcjLmysPPCWRM04"
    ast_data = gs.download(data={
        "spreadsheet_id": spreadsheet_id,
        "sheet_name": "Sheet1",
        "listedFields": []})
    df_assortment = pd.DataFrame(ast_data)
    df_assortment.columns = [c.replace('-', '_') for c in df_assortment.columns]
    df_assortment[drug_col] = df_assortment[drug_col].astype(int)
    df_assortment['drug_name'] = df_assortment['drug_name'].astype(str)
    df_assortment['count'] = 1
    df_assortment_comb = df_assortment.loc[df_assortment['type'].isin(type_list_comb_lvl)]

    # Read combinations and corresponding composition
    list_unq_comb = comb_fcst_df[comb_col].tolist()
    if list_unq_comb:
        str_unq_comb = str(list_unq_comb).replace('[', '(').replace(']', ')')
    else:
        str_unq_comb = '(0)'
    q_comb_drug = f"""
            select dsm."drug-id" as drug_id, dsm."group" as comb_id, 
                d."drug-name" as drug_name, d.type, d.composition 
            from "{schema}"."drug-substitution-mapping" dsm
            left join "{schema}".drugs d on dsm."drug-id" = d.id 
            where dsm."group" in {str_unq_comb}
            """
    df_comb_drug = db.get_df(q_comb_drug)

    # Get all mapping cases
    merge_comb_drug = df_comb_drug[[drug_col, comb_col]].merge(
        df_assortment_comb[[drug_col, 'drug_name', 'count']], on=drug_col, how="outer")

    count_comp_drugs = merge_comb_drug.groupby(comb_col, as_index=False).agg({'count': 'sum'})

    list_comb_one_one = count_comp_drugs[count_comp_drugs['count'] == 1][comb_col].tolist()
    list_comb_one_many = count_comp_drugs[count_comp_drugs['count'] > 1][comb_col].tolist()
    list_comb_one_none = count_comp_drugs[count_comp_drugs['count'] == 0][comb_col].tolist()

    # Allocate forecast to drugs
    df_assortment_merge = df_assortment_comb.merge(df_comb_drug, on=drug_col, how='left')
    list_drug_with_comb_fcst = df_assortment_merge.loc[df_assortment_merge[comb_col].notna()][drug_col].tolist()

    df_all_comb = comb_fcst_df.merge(df_assortment_merge, on=comb_col, how='left')
    df_all_comb = df_all_comb[[store_col, comb_col, 'bucket', 'model', drug_col, 'fcst', 'std', 'correction_flags']]
    df_fcst_final = pd.DataFrame()

    # Case 1: One-One, direct assign
    df_temp = df_all_comb.loc[df_all_comb[comb_col].isin(list_comb_one_one)]
    df_temp['fcst_wt'] = 1
    df_temp['map_type'] = 'one-one'
    df_temp['fcst_source'] = 'combination_fcst'
    df_fcst_final = df_fcst_final.append(df_temp)
    df_one_one = df_temp.copy()
    df_one_one = df_one_one.merge(df_assortment_comb, on=drug_col, how='left')
    df_one_one.drop('count', axis=1, inplace=True)

    # Case 2: One-Many, assign based on past month sales contribution
    df_temp = df_all_comb.loc[df_all_comb[comb_col].isin(list_comb_one_many)]
    df_temp = drug_sales_multiplier(df_temp, store_id, reset_date, schema, db)
    df_one_many = df_temp.copy()
    df_temp.drop(['sales_90d', 'comb_sales_90d'], axis=1, inplace=True)
    df_temp['fcst'] = df_temp['fcst'] * df_temp['fcst_wt']
    df_temp['std'] = df_temp['std'] * df_temp['fcst_wt']
    df_temp['map_type'] = 'one-many'
    df_temp['fcst_source'] = 'combination_fcst'
    df_fcst_final = df_fcst_final.append(df_temp)
    df_one_many = df_one_many.merge(df_assortment_comb, on=drug_col, how='left')
    df_one_many.drop('count', axis=1, inplace=True)

    # Case 3: One-None, to send
    df_one_none = df_all_comb.loc[df_all_comb[comb_col].isin(list_comb_one_none)]
    df_one_none.drop(drug_col, axis=1, inplace=True)
    df_one_none = df_one_none.merge(df_comb_drug, on=comb_col, how='left')
    df_one_none = drug_sales_multiplier(df_one_none, store_id, reset_date, schema, db)
    df_one_none = df_one_none.loc[df_one_none['sales_90d'] > 0]
    df_one_none.drop('fcst_wt', axis=1, inplace=True)

    # Case 4: No Comb - Drugs, to map with drug-level-fcst
    df_none_one = df_assortment.loc[~df_assortment[drug_col].isin(list_drug_with_comb_fcst)]
    df_none_one.drop('count', axis=1, inplace=True)

    # get drug-combination groups
    list_drugs = df_none_one[drug_col].tolist()
    if list_drugs:
        str_list_drugs = str(list_drugs).replace('[', '(').replace(']', ')')
    else:
        str_list_drugs = '(0)'
    q_comb_drug = f"""
               select dsm."drug-id" as drug_id, dsm."group" as comb_id, 
                   d."drug-name" as drug_name, d.type, d.composition 
               from "{schema}"."drug-substitution-mapping" dsm
               left join "{schema}".drugs d on dsm."drug-id" = d.id 
               where dsm."drug-id" in {str_list_drugs}
               """
    df_comb_drug = db.get_df(q_comb_drug)

    drug_fcst_df.drop(key_col, axis=1, inplace=True)
    df_fcst_drug_level_merge = drug_fcst_df.merge(df_none_one[[drug_col]],
                                                  on=drug_col, how='inner')

    df_fcst_drug_level_merge = df_fcst_drug_level_merge.merge(
        df_comb_drug, on=drug_col, how='left')
    df_fcst_drug_level_merge['fcst_source'] = 'drug_fcst'
    df_fcst_drug_level_merge['fcst_wt'] = np.nan
    df_fcst_drug_level_merge['map_type'] = np.nan

    df_fcst_final = df_fcst_final.append(df_fcst_drug_level_merge[df_fcst_final.columns])

    # filter only drugs without combination
    drugs_with_comb = df_comb_drug[drug_col].tolist()
    df_none_one = df_none_one.loc[~df_none_one[drug_col].isin(drugs_with_comb)]

    # Append reject cases
    forecasted_drugs = df_fcst_final[drug_col].tolist()
    assortment_drugs = df_assortment[drug_col].tolist()
    reject_drugs = list(set(forecasted_drugs) ^ set(assortment_drugs))
    df_reject_cases = df_assortment.loc[df_assortment[drug_col].isin(reject_drugs)][[drug_col]]
    df_reject_cases[store_col] = store_id
    df_reject_cases['bucket'] = 'NA'
    df_reject_cases['model'] = 'NA'
    df_reject_cases['fcst'] = 0
    df_reject_cases['std'] = 0
    df_reject_cases['fcst_wt'] = np.nan
    df_reject_cases['map_type'] = np.nan
    df_reject_cases['fcst_source'] = np.nan
    df_reject_cases['correction_flags'] = ""
    df_reject_cases = df_reject_cases.merge(df_comb_drug, on=drug_col, how='left')

    df_fcst_final = df_fcst_final.append(df_reject_cases[df_fcst_final.columns])

    # Round off forecast values
    df_fcst_final['fcst'] = df_fcst_final['fcst'].astype(float)
    df_fcst_final['fcst'] = np.round(df_fcst_final['fcst'])

    return df_fcst_final, df_one_one, df_one_many, df_one_none, df_none_one


def drug_sales_multiplier(df, store_id, reset_date, schema, db):
    list_drugs = df[drug_col].tolist()
    if list_drugs:
        str_drugs = str(list_drugs).replace('[', '(').replace(']', ')')
    else:
        str_drugs = '(0)'
    sales_start = (dt.datetime.strptime(reset_date, '%Y-%m-%d').date() -
                   dt.timedelta(days=90)).strftime('%Y-%m-%d')

    q_drug_sales = f"""
        select "drug-id" , sum("net-quantity") as sales_90d
        from "{schema}".sales s 
        where "store-id" = {store_id}
        and date("created-at") >= '{sales_start}'
        and date("created-at") < '{reset_date}'
        and "drug-id" in {str_drugs}
        group by "drug-id" 
        """
    df_drug_sales = db.get_df(q_drug_sales)
    df_drug_sales.columns = [c.replace('-', '_') for c in df_drug_sales.columns]

    df = df.merge(df_drug_sales, on=drug_col, how='left')
    df['sales_90d'] = df['sales_90d'].fillna(0)

    df_comb_sales_sum = df.groupby(comb_col, as_index=False).agg({'sales_90d': 'sum'})
    df_comb_sales_sum.rename({'sales_90d': 'comb_sales_90d'}, axis=1, inplace=True)

    df = df.merge(df_comb_sales_sum, on=comb_col, how='left')
    df['fcst_wt'] = df['sales_90d']/df['comb_sales_90d']
    df['fcst_wt'] = df['fcst_wt'].fillna(0)

    # assign equal split for combination with 0 sales
    zero_sales_comb = df_comb_sales_sum.loc[
        df_comb_sales_sum['comb_sales_90d'] == 0][comb_col].tolist()
    df_comb_equal_split_cases = df.groupby(comb_col, as_index=False).agg({drug_col: 'count'})
    df_comb_equal_split_cases.rename({drug_col: 'count'}, axis=1, inplace=True)
    df_comb_equal_split_cases = df_comb_equal_split_cases.loc[df_comb_equal_split_cases[comb_col].isin(zero_sales_comb)]
    df_comb_equal_split_cases['equal_split_wt'] = 1/df_comb_equal_split_cases['count']

    df = df.merge(df_comb_equal_split_cases, on=comb_col, how='left')
    df['fcst_wt'] = np.where(df['equal_split_wt'].isna(), df['fcst_wt'], df['equal_split_wt'])
    df.drop(['count', 'equal_split_wt'], axis=1, inplace=True)

    return df
