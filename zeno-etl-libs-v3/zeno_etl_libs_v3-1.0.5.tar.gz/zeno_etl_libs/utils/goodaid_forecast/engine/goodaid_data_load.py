import numpy as np
import pandas as pd
import datetime as dt
from zeno_etl_libs.utils.goodaid_forecast.engine.config_goodaid import (
   store_age_limit,
drug_age_limit,
store_col,
drug_col,
key_col,
similar_drug_type
)


class GoodaidloadData:

    def load_file(self, db, query):
        df = db.get_df(query)
        df.columns = [c.replace('-', '_') for c in df.columns]
        return df

    def load_all_input(
            self,
            type_list=None,
            store_id_list=None,
            last_date=None,
            reset_date=None,
            schema=None,
            db=None
    ):
        drug_list = self.load_file(
            query="""
                select id as drug_id from "{schema}".drugs where type in {0}
                 """.format(type_list, schema=schema),
            db=db
        )

        sales_history = self.load_file(
            query="""
                select date("created-at") as "sales-date","store-id", "drug-id" , 
                        sum("net-quantity") as "net-sales-quantity"
                from "{schema}".sales s
                where "store-id" in {store_id_list}
                and s."company-id" = 6984
                -- and s."drug-id" = 487502
                and date("created-at") >= '{last_date}'
                and date("created-at") < '{reset_date}'
                group by "store-id",  "drug-id", "sales-date"
                """.format(
                store_id_list=store_id_list, last_date=last_date,
                reset_date=reset_date, schema=schema),
            db=db
        )

        cfr_pr = self.load_file(
            query=f"""
                select cfr."store-id", cfr."drug-id",cfr."shortbook-date", 
                sum(cfr."loss-quantity") as "loss-quantity"
                from "{schema}"."cfr-patient-request" cfr
                left join "{schema}".drugs d 
				on cfr."drug-id" = d.id               
                where cfr."shortbook-date" >= '{last_date}'
                and d."company-id" = 6984
                -- and d."id" = 487502
                and cfr."shortbook-date" < '{reset_date}'
                and cfr."drug-id" <> -1
                and (cfr."drug-category" = 'chronic' or cfr."repeatability-index" >= 40)
                and cfr."loss-quantity" > 0
                and cfr."drug-type" in {type_list}
                and cfr."store-id" in {store_id_list}
                group by cfr."store-id",cfr."drug-id", cfr."shortbook-date"
                """,
            db=db
        )

        calendar = self.load_file(
            query="""
                select date, year, month, "week-of-year", "day-of-week" 
                from "{schema}".calendar
                where date < '{reset_date}'
                """.format(schema=schema, reset_date=reset_date),
            db=db
        )

        first_bill_date = self.load_file(
            query="""
                select "store-id" , min(date("created-at")) as bill_date from "{schema}".sales
                where "store-id" in {store_id_list}
                group by "store-id" 
                """.format(schema=schema, store_id_list=store_id_list),
            db=db
        )

        first_store_drug_bill_date = self.load_file(
            query="""
                    select
                        s."store-id" ,
                        s."drug-id" ,
                        min(date(s."created-at")) as "first-store-drug-bill"
                    from
                        "{schema}".sales s
                    where
                        s."company-id" = 6984
                        and s."store-id" in  {store_id_list}
                    group by
                        s."store-id" ,
                        s."drug-id"
                """.format(schema=schema, store_id_list=store_id_list),
            db=db
        )

        wh_goodaid_assortment = self.load_file(
            query="""
                select
                    d."id" as "drug-id",
                    case
                        when wssm."add-wh" is not null then wssm."add-wh"
                        else 'No-Entry'
                    end as "wh-assortment"
                from
                    "{schema}".drugs d
                left join "{schema}"."wh-sku-subs-master" wssm
                                on
                    d.id = wssm."drug-id"
                where
                    d."type" not in ('discontinued-products','banned')
                    and d.company = 'GOODAID'
            """.format(schema=schema),
            db=db
        )

        similar_drug_mapping = self.load_file(
            query="""
                    select
                        ducm."drug-id" ,
                        ducm."group",
                        d."type"
                    from
                         "{schema}"."drug-unique-composition-mapping" ducm
                    left join  "{schema}".drugs d 
                    on
                        ducm."drug-id" = d.id
            """.format(schema=schema),
            db=db
        )

        # Exception handling

        date_to_add = (dt.datetime.strptime(reset_date, '%Y-%m-%d') - dt.timedelta(days=8)).strftime('%Y-%m-%d')
        date_to_add2 = (dt.datetime.strptime(reset_date, '%Y-%m-%d') - dt.timedelta(days=15)).strftime('%Y-%m-%d')
        sales_history_add = pd.DataFrame(columns=sales_history.columns)
        first_store_drug_bill_date_add = pd.DataFrame(columns=first_store_drug_bill_date.columns)

        for stores in store_id_list:
            if stores in (0,'(',')'):
                continue

            stores = int(stores)
            drugs_in_ga_assortment = tuple(map(int, wh_goodaid_assortment['drug_id'].unique()))
            drugs_in_sales_history = tuple(map(int, sales_history[sales_history['store_id']==stores]['drug_id'].unique()))
            drugs_in_first_store_drug_bill = tuple(map(int, first_store_drug_bill_date[first_store_drug_bill_date['store_id']==stores]['drug_id'].unique()))
            drugs_in_assortment_but_not_in_sales_history = tuple(
                set(drugs_in_ga_assortment) - set(drugs_in_sales_history))
            drugs_in_sales_history_but_not_in_assortment = tuple(
                set(drugs_in_sales_history) - set(drugs_in_ga_assortment))
            drugs_in_assortment_but_not_in_first_store_drug_bill = tuple(
                set(drugs_in_ga_assortment) - set(drugs_in_first_store_drug_bill))

            dict = {'sales_date': [date_to_add]*len(drugs_in_assortment_but_not_in_sales_history),
                    'store_id': [stores]*len(drugs_in_assortment_but_not_in_sales_history),
                    'drug_id': list(drugs_in_assortment_but_not_in_sales_history),
                    'net_sales_quantity':1
                    }
            sales_history_add_store = pd.DataFrame(dict)

            sales_history_add = pd.concat([sales_history_add_store,sales_history_add],sort = True)

            dict = {'sales_date': [date_to_add2]*len(drugs_in_assortment_but_not_in_sales_history),
                    'store_id': [stores]*len(drugs_in_assortment_but_not_in_sales_history),
                    'drug_id': list(drugs_in_assortment_but_not_in_sales_history),
                    'net_sales_quantity':1
                    }
            sales_history_add_store = pd.DataFrame(dict)
            sales_history_add = pd.concat([sales_history_add_store, sales_history_add], sort=True)

            dict2 = {'store_id':[stores]*len(drugs_in_assortment_but_not_in_first_store_drug_bill),
                     'drug_id':list(drugs_in_assortment_but_not_in_first_store_drug_bill),
                     'first_store_drug_bill':[date_to_add2]*len(drugs_in_assortment_but_not_in_first_store_drug_bill)}

            first_store_drug_bill_date_add_store = pd.DataFrame(dict2)
            first_store_drug_bill_date_add = pd.concat([first_store_drug_bill_date_add_store,first_store_drug_bill_date_add],sort = True)

        sales_history_add[['store_id','drug_id','net_sales_quantity']] = sales_history_add[['store_id','drug_id','net_sales_quantity']].astype(int)

        sales_history = pd.concat([sales_history,sales_history_add],sort=True)

        first_store_drug_bill_date = pd.concat([first_store_drug_bill_date, first_store_drug_bill_date_add], sort=True)
        return (
            drug_list,
            sales_history,
            cfr_pr,
            calendar,
            first_bill_date,
            first_store_drug_bill_date,
            wh_goodaid_assortment,
            similar_drug_mapping,
            sales_history_add
        )

class Goodaid_data_additional_processing:

    def add_ts_id(self, df):
        df = df[~df[drug_col].isnull()].reset_index(drop=True)
        df['ts_id'] = (
                df[store_col].astype(int).astype(str)
                + '_'
                + df[drug_col].astype(int).astype(str)
        )
        return df

    def age_bucket_bifurcation(self, df,reset_date):
        df['reset_date'] = reset_date
        df['reset_date'] = pd.to_datetime(df['reset_date'])
        df['bill_date'] = pd.to_datetime(df['bill_date'])
        df['first_store_drug_bill'] = pd.to_datetime(df['first_store_drug_bill'])
        df['store_age'] = (df['reset_date'] - df['bill_date']).dt.days
        df['drug_store_age'] = (df['reset_date'] - df['first_store_drug_bill']).dt.days

        conditions = [((df['store_age'] >= store_age_limit) & (df['drug_store_age'] >= drug_age_limit)),
                      ((df['store_age'] >= store_age_limit) & (df['drug_store_age'] < drug_age_limit)),
                      ((df['store_age'] < store_age_limit) & (df['drug_store_age'] >= drug_age_limit)),
                      ((df['store_age'] < store_age_limit) & (df['drug_store_age'] < drug_age_limit))]
        choice = ['B1', 'B2', 'B2', 'B2']
        df['age_bucket'] = np.select(conditions, choice)

        df.drop(columns=['bill_date', 'reset_date', 'first_store_drug_bill', 'store_age'],
                inplace=True)

        # df.drop(columns=['bill_date', 'reset_date', 'first_store_drug_bill', 'store_age', 'drug_store_age'],
        #         inplace=True)
        return df

    def merge_first_store_drug_bill_date(self,sales,first_store_drug_bill_date):
        sales = sales.merge(first_store_drug_bill_date, on = [key_col,store_col,drug_col],how = 'left')
        return sales

    def merge_first_bill_date(self,sales,first_bill_date):
        sales = sales.merge(first_bill_date, on='store_id', how='left')
        return sales

    def age_bucketing(self,first_store_drug_bill_date,sales_pred,sales,reset_date,first_bill_date):
        sales = self.merge_first_bill_date(sales,first_bill_date)
        sales_pred = self.merge_first_bill_date(sales_pred,first_bill_date)
        first_store_drug_bill_date = self.add_ts_id(first_store_drug_bill_date)
        sales = self.merge_first_store_drug_bill_date(sales,first_store_drug_bill_date)
        sales = self.age_bucket_bifurcation(sales,reset_date)
        sales_pred = self.merge_first_store_drug_bill_date(sales_pred,first_store_drug_bill_date)
        sales_pred = self.age_bucket_bifurcation(sales_pred,reset_date)
        return sales,sales_pred

    def merge_assortment(self,sales,wh_goodaid_assortment):
        sales = sales.merge(wh_goodaid_assortment,on = drug_col, how = 'left')
        return sales

    def add_wh_current_assortment(self,sales_pred,sales,wh_goodaid_assortment):
        sales = self.merge_assortment(sales,wh_goodaid_assortment)
        sales_pred = self.merge_assortment(sales_pred,wh_goodaid_assortment)
        return sales, sales_pred

    def formatting_column_type_int(self,df,col):
        df[col] = df[col].astype(int)
        return df


    def goodaid_extra_processing_all(self,first_store_drug_bill_date,sales_pred,sales,reset_date,first_bill_date,wh_goodaid_assortment):
        sales = self.formatting_column_type_int(sales,store_col)
        sales = self.formatting_column_type_int(sales,drug_col)
        sales_pred = self.formatting_column_type_int(sales_pred,store_col)
        sales_pred = self.formatting_column_type_int(sales_pred,drug_col)
        first_store_drug_bill_date = self.formatting_column_type_int(first_store_drug_bill_date,store_col)
        first_store_drug_bill_date = self.formatting_column_type_int(first_store_drug_bill_date,drug_col)
        first_bill_date = self.formatting_column_type_int(first_bill_date,store_col)
        sales, sales_pred = self.age_bucketing(first_store_drug_bill_date,sales_pred,sales,reset_date,first_bill_date)
        sales, sales_pred = self.add_wh_current_assortment(sales_pred,sales,wh_goodaid_assortment)
        return sales,sales_pred


class b2_goodaid_load_data:

    def load_file(self, db, query):
        df = db.get_df(query)
        df.columns = [c.replace('-', '_') for c in df.columns]
        return df

    def load_all_input(
            self,
            type_list=None,
            store_id_list=None,
            sales_pred = None,
            similar_drug_mapping = None,
            last_date=None,
            reset_date=None,
            schema=None,
            db=None
    ):
        drug_list = self.load_file(
            query="""
                    select id as drug_id from "{schema}".drugs where type in {0}
                     """.format(type_list, schema=schema),
            db=db
        )

        b2_drugs = tuple(map(int, sales_pred[sales_pred['age_bucket'] == 'B2']['drug_id'].unique()))

        group_info = similar_drug_mapping[similar_drug_mapping["drug_id"].isin(b2_drugs)]
        groups = tuple(map(str,group_info["group"].unique()))

        drug_info = similar_drug_mapping[similar_drug_mapping["group"].isin(groups)]
        drug_info = drug_info[drug_info['type'].isin(similar_drug_type)]
        similar_drugs = tuple(map(int, drug_info['drug_id'].unique()))

        sales_history = self.load_file(
            query="""
                    select date(s."created-at") as "sales-date",s."store-id", d1."drug-id" as "drug-id", 
                            sum(s."net-quantity") as "net-sales-quantity"
                    from "{schema}".sales s
                    left join "{schema}"."drug-unique-composition-mapping" d1
                    on
                    s."drug-id" = d1."drug-id"
                    where "store-id" in {store_id_list}
                    and s."drug-id" in {similar_drugs}
                    and date(s."created-at") >= '{last_date}'
                    and date(s."created-at") < '{reset_date}'
                    group by s."store-id", d1."drug-id", "sales-date"
                    """.format(similar_drugs=similar_drugs + (0,0),groups = groups ,
                store_id_list=store_id_list, last_date=last_date,
                reset_date=reset_date, schema=schema),
            db=db
        )

        cfr_pr = self.load_file(
            query=f"""
                                select cfr."store-id", d1."drug-id" as "drug-id",cfr."shortbook-date",
                                sum(cfr."loss-quantity") as "loss-quantity"
                                from "{schema}"."cfr-patient-request" cfr
                                left join "{schema}".drugs d
                				on cfr."drug-id" = d.id
                				left join "{schema}"."drug-unique-composition-mapping" d1
                                on
                                cfr."drug-id" = d1."drug-id"
                                where cfr."shortbook-date" >= '{last_date}'
                                and cfr."drug-id" in {similar_drugs}
                                and cfr."shortbook-date" < '{reset_date}'
                                and cfr."drug-id" <> -1
                                and (cfr."drug-category" = 'chronic' or cfr."repeatability-index" >= 40)
                                and cfr."loss-quantity" > 0
                                and cfr."drug-type" in {type_list}
                                and cfr."store-id" in {store_id_list}
                                group by cfr."store-id",d1."drug-id", cfr."shortbook-date"
                                """,
            db=db
        )

        calendar = self.load_file(
            query="""
                    select date, year, month, "week-of-year", "day-of-week" 
                    from "{schema}".calendar
                    where date < '{reset_date}'
                    """.format(schema=schema, reset_date=reset_date),
            db=db
        )

        return (
            drug_list,
            sales_history,
            cfr_pr,
            calendar,
            drug_info,
            group_info
        )
