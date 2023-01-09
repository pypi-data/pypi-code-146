"""data preparation for drug forecast at store level"""
import pandas as pd
import datetime
import numpy as np

from zeno_etl_libs.utils.ipc_pmf.config_ipc_combination import date_col, store_col, \
    comb_col, target_col, key_col, local_testing


class PreprocessData:

    def add_ts_id(self, df):
        df = df[~df[comb_col].isnull()].reset_index(drop=True)
        df['ts_id'] = (
                df[store_col].astype(int).astype(str)
                + '_'
                + df[comb_col].astype(str)
        )
        return df

    def preprocess_sales(self, df, comb_list):

        df.rename(columns={
            'net_sales_quantity': target_col
        }, inplace=True)

        df.rename(columns={
            'sales_date': date_col
        }, inplace=True)

        set_dtypes = {
            store_col: int,
            comb_col: str,
            date_col: str,
            target_col: float
        }
        df = df.astype(set_dtypes)
        df[target_col] = df[target_col].round()

        df[date_col] = pd.to_datetime(df[date_col])

        df = df.groupby(
            [store_col, comb_col, key_col, date_col]
        )[target_col].sum().reset_index()

        df = df[df[comb_col].isin(comb_list)]

        return df

    def get_formatted_data(self, df):

        df_start = df.groupby([key_col])[date_col].min().reset_index().rename(
            columns={date_col: 'sales_start'})
        df = df[[key_col, date_col, target_col]]
        min_date = df[date_col].dropna().min()
        end_date = df[date_col].dropna().max()
        date_range = []
        date_range = pd.date_range(
            start=min_date,
            end=end_date,
            freq='d'
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
                .rename(columns={0: target_col})
        )

        df = pd.merge(df, df_start, how='left', on=key_col)
        df = df[df[date_col] >= df['sales_start']]
        df[[store_col, comb_col]] = df[key_col].str.split('_', expand=True)
        df[[store_col, comb_col]] = df[[store_col, comb_col]]
        df[store_col] = df[store_col].astype(int)
        df[comb_col] = df[comb_col].astype(str)
        return df

    def preprocess_cfr_pr(self, df):

        set_dtypes = {
            store_col: int,
            comb_col: str,
            'loss_quantity': int
        }
        df = df.astype(set_dtypes)
        df['shortbook_date'] = pd.to_datetime(df['shortbook_date'])
        return df

    def merge_cfr_pr(self, sales, cfr_pr):

        df = sales.merge(cfr_pr,
                         left_on=[store_col, comb_col, date_col],
                         right_on=[store_col, comb_col, 'shortbook_date'],
                         how='left')
        df[date_col] = df[date_col].combine_first(df['shortbook_date'])
        df[target_col].fillna(0, inplace=True)
        df['loss_quantity'].fillna(0, inplace=True)
        df[target_col] += df['loss_quantity']
        df.drop(['shortbook_date', 'loss_quantity'], axis=1, inplace=True)
        return df

    def preprocess_calendar(self, df, last_date):
        df.rename(columns={'date': date_col}, inplace=True)
        df[date_col] = pd.to_datetime(df[date_col])

        cal_sales = df.copy()
        cal_sales['week_begin_dt'] = cal_sales.apply(
            lambda x: x[date_col] - datetime.timedelta(x['day_of_week']),
            axis=1)
        cal_sales['month_begin_dt'] = cal_sales.apply(
            lambda x: x['date'] - datetime.timedelta(x['date'].day - 1), axis=1)
        cal_sales['key'] = 1
        ld = pd.to_datetime(last_date)
        cal_sales = cal_sales[cal_sales[date_col] > ld]
        return df, cal_sales

    def merge_calendar(self, sales, calendar):
        df = sales.merge(calendar,
                         how='left',
                         on=date_col
                         )

        # df_week_days_count = df.groupby([key_col, 'year', 'week_of_year'])[date_col].count().reset_index().rename(columns = {date_col:'week_days_count'})
        # df['week_days_count'] = 1
        df['week_begin_dt'] = df.apply(
            lambda x: x[date_col] - datetime.timedelta(x['day_of_week']),
            axis=1)
        df_week_days_count = df.groupby(['ts_id', 'week_begin_dt'])[
            date_col].count().reset_index().rename(
            columns={date_col: 'week_days_count'})
        # df = df.groupby(['ts_id', store_col, drug_col, ]).resample('W-Mon', on =date_col )[target_col].sum().reset_index()
        df = df.groupby(['ts_id', store_col, comb_col, 'week_begin_dt'])[
            target_col].sum().reset_index()
        df = pd.merge(df, df_week_days_count, how='left',
                      on=[key_col, 'week_begin_dt'])
        df = df[df['week_days_count'] == 7].reset_index(drop=True)
        df.drop(columns=['week_days_count'], inplace=True)
        df.rename(columns={'week_begin_dt': date_col}, inplace=True)
        return df

    def preprocess_bill_date(self, df):
        df.rename(columns={'store-id': store_col}, inplace=True)
        df['bill_date'] = pd.to_datetime(df['bill_date'])
        return df

    def merge_first_bill_date(self, sales, first_bill_date):
        df = pd.merge(sales, first_bill_date, on=[store_col])
        df = df[df[date_col] >= df['bill_date']].reset_index(drop=True)
        df.drop(columns=['bill_date'], inplace=True)
        return df

    def make_future_df(self, df):
        start_date_df = (
            df
                .groupby(key_col)[date_col]
                .min()
                .reset_index()
                .rename(columns={date_col: 'start_date'})
        )

        df = df[[key_col, date_col, target_col]]
        end_date = df[date_col].max() + datetime.timedelta(weeks=5)
        min_date = df[date_col].min()
        date_range = pd.date_range(
            start=min_date,
            end=end_date,
            freq="W-MON"
        )
        date_range = list(set(date_range) - set(df[date_col]))

        df = (
            df
                .groupby([date_col] + [key_col])[target_col]
                .sum()
                .unstack()
        )

        for date in date_range:
            df.loc[date, :] = 0

        df = (
            df
                .fillna(0)
                .stack()
                .reset_index()
                .rename(columns={0: target_col})
        )

        df = df.merge(start_date_df, on=key_col, how='left')

        df = df[
            df[date_col] >= df['start_date']
            ]

        df.drop('start_date', axis=1, inplace=True)

        df[[store_col, comb_col]] = df[key_col].str.split('_', expand=True)
        return df

    def make_future_df_4w_agg(self, df):
        start_date_df = (
            df
                .groupby(key_col)[date_col]
                .min()
                .reset_index()
                .rename(columns={date_col: 'start_date'})
        )

        df = df[[key_col, date_col, target_col]]
        fcst_week_start = df[date_col].max() + datetime.timedelta(weeks=5)
        date_range = [fcst_week_start]

        df = (
            df
                .groupby([date_col] + [key_col])[target_col]
                .sum()
                .unstack()
        )

        for date in date_range:
            df.loc[date, :] = 0

        df = (
            df
                .fillna(0)
                .stack()
                .reset_index()
                .rename(columns={0: target_col})
        )

        df = df.merge(start_date_df, on=key_col, how='left')

        df = df[
            df[date_col] >= df['start_date']
            ]

        df.drop('start_date', axis=1, inplace=True)

        df[[store_col, comb_col]] = df[key_col].str.split('_', expand=True)
        return df

    def sales_pred_vald_df(
            self,
            df
    ):
        vald_max_date = df[date_col].max() - datetime.timedelta(weeks=4)
        df_vald_train = df.loc[df[date_col] <= vald_max_date]
        df_vald_future = df.loc[~(df[date_col] <= vald_max_date)]
        df_vald_future[target_col] = 0
        df_final = df_vald_train.append(df_vald_future)
        train_vald_max_date = df_vald_train[date_col].max()
        return df_final, train_vald_max_date

    def sales_4w_agg(
            self,
            df
    ):
        # =====================================================================
        # Combine 4 weeks into an arbitrary group
        # =====================================================================
        unique_ts_ids = df[key_col].unique().tolist()
        sales_4w_agg = pd.DataFrame()
        for ts_id in unique_ts_ids:
            week_gp_size = 4
            sales_temp = df.loc[df[key_col] == ts_id]
            available_week_count = sales_temp.shape[0]
            if available_week_count >= (3 * week_gp_size):
                allowable_week_count = int(
                    week_gp_size * np.fix(available_week_count / week_gp_size))
                sales_temp = sales_temp.sort_values(by=["date"], ascending=True)
                sales_temp = sales_temp[-allowable_week_count:]
                week_gps_count = int(allowable_week_count / week_gp_size)
                week_gps_list = np.arange(1, week_gps_count + 1, 1)
                week_gps_id_list = np.repeat(week_gps_list, week_gp_size)
                sales_temp["week_gps_id"] = week_gps_id_list
                sales_temp = sales_temp.groupby(
                    [key_col, store_col, comb_col, "week_gps_id"],
                    as_index=False).agg(
                    {"date": "first", "actual_demand": "sum"})
                sales_4w_agg = sales_4w_agg.append(sales_temp)

        sales_4w_agg = sales_4w_agg.drop("week_gps_id", axis=1)
        sales_pred_4w_agg = self.make_future_df_4w_agg(sales_4w_agg.copy())

        return sales_4w_agg, sales_pred_4w_agg


    def comb_sales_12w(
            self,
            df
    ):
        date_12w_back = df[date_col].max() - datetime.timedelta(weeks=12)
        df_12w = df.loc[df[date_col] > date_12w_back]
        df_12w = df_12w.groupby([store_col, comb_col], as_index=False).agg(
            {target_col: 'sum'})

        return df_12w

    def comb_sales_4w_wtd(
            self,
            df
    ):

        date_4w_back = df[date_col].max() - datetime.timedelta(weeks=4)
        df_4w = df.loc[df[date_col] > date_4w_back]

        # sales > 0 and all 4 latest week
        df_4w_1 = df_4w[df_4w[target_col] > 0]

        df_4w_cnt = df_4w_1.groupby([store_col, comb_col], as_index=False).agg(
            {target_col: 'count'})
        df_4w_cnt.rename({target_col: 'week_count'}, axis=1, inplace=True)
        list_4w_combs = df_4w_cnt.loc[df_4w_cnt['week_count'] == 4][comb_col].tolist()

        df_4w_1 = df_4w_1.loc[df_4w_1[comb_col].isin(list_4w_combs)]

        dates_list = list(df_4w_1.date.unique())

        df_4w_1['weights'] = np.where(df_4w_1[date_col] == dates_list[3], 0.4, 0)
        df_4w_1['weights'] = np.where(df_4w_1[date_col] == dates_list[2], 0.3, df_4w_1['weights'])
        df_4w_1['weights'] = np.where(df_4w_1[date_col] == dates_list[1], 0.2, df_4w_1['weights'])
        df_4w_1['weights'] = np.where(df_4w_1[date_col] == dates_list[0], 0.1, df_4w_1['weights'])

        df_4w_1['wtd_demand'] = df_4w_1[target_col] * df_4w_1['weights']

        df_4w_1 = df_4w_1.groupby([store_col, comb_col], as_index=False).agg(
            {'wtd_demand': 'sum'})

        # sales > 0 and only 3 latest week
        df_4w_2 = df_4w[df_4w[target_col] > 0]
        df_4w_cnt = df_4w_2.groupby([store_col, comb_col], as_index=False).agg(
            {target_col: 'count'})
        df_4w_cnt.rename({target_col: 'week_count'}, axis=1, inplace=True)
        list_4w_combs = df_4w_cnt.loc[df_4w_cnt['week_count'] == 3][comb_col].tolist()

        df_4w_2 = df_4w_2.loc[df_4w_2[comb_col].isin(list_4w_combs)]
        df_4w_2['w_count'] = np.tile(np.arange(1, 4), len(df_4w_2))[:len(df_4w_2)]

        df_4w_2['weights'] = np.where(df_4w_2['w_count'] == 3, 0.5, 0)
        df_4w_2['weights'] = np.where(df_4w_2['w_count'] == 2, 0.3, df_4w_2['weights'])
        df_4w_2['weights'] = np.where(df_4w_2['w_count'] == 1, 0.2, df_4w_2['weights'])

        df_4w_2['wtd_demand'] = df_4w_2[target_col] * df_4w_2['weights']

        df_4w_2 = df_4w_2.groupby([store_col, comb_col], as_index=False).agg(
            {'wtd_demand': 'sum'})

        # sales > 0 and only 2 latest week
        df_4w_3 = df_4w[df_4w[target_col] > 0]
        df_4w_cnt = df_4w_3.groupby([store_col, comb_col], as_index=False).agg(
            {target_col: 'count'})
        df_4w_cnt.rename({target_col: 'week_count'}, axis=1, inplace=True)
        list_4w_combs = df_4w_cnt.loc[df_4w_cnt['week_count'] == 2][
            comb_col].tolist()

        df_4w_3 = df_4w_3.loc[df_4w_3[comb_col].isin(list_4w_combs)]
        df_4w_3['w_count'] = np.tile(np.arange(1, 3), len(df_4w_3))[:len(df_4w_3)]

        df_4w_3['weights'] = np.where(df_4w_3['w_count'] == 2, 0.6, 0)
        df_4w_3['weights'] = np.where(df_4w_3['w_count'] == 1, 0.4, df_4w_3['weights'])

        df_4w_3['wtd_demand'] = df_4w_3[target_col] * df_4w_3['weights']

        df_4w_3 = df_4w_3.groupby([store_col, comb_col], as_index=False).agg(
            {'wtd_demand': 'sum'})

        df_4w = pd.concat([df_4w_1, df_4w_2, df_4w_3], axis=0)
        df_4w['wtd_demand'] = np.round(df_4w['wtd_demand'] * 4)

        return df_4w

    def preprocess_all(
            self,
            sales=None,
            cfr_pr=None,
            comb_list=None,
            calendar=None,
            first_bill_date=None,
            last_date=None,
    ):
        sales = self.add_ts_id(sales)
        # filter
        #################################################
        if local_testing == 1:
            tsid_list = \
            sales.sort_values(by=['net_sales_quantity'], ascending=False)[
                key_col].unique().tolist()[:20]
            sales = sales[sales[key_col].isin(tsid_list)]
        #################################################
        sales = self.preprocess_sales(sales, comb_list)
        sales = self.get_formatted_data(sales)
        cfr_pr = self.preprocess_cfr_pr(cfr_pr)
        sales_daily = self.merge_cfr_pr(sales, cfr_pr)
        calendar, cal_sales = self.preprocess_calendar(calendar, last_date)
        sales = self.merge_calendar(sales_daily, calendar)
        first_bill_date = self.preprocess_bill_date(first_bill_date)

        sales = self.merge_first_bill_date(sales, first_bill_date)
        sales_pred = self.make_future_df(sales.copy())

        sales_pred_vald, train_vald_max_date = self.sales_pred_vald_df(sales)

        sales_4w_agg, sales_pred_4w_agg = self.sales_4w_agg(sales)

        sales_pred_4w_agg_vald, train_4w_agg_vald_max_date = self.sales_pred_vald_df(sales_4w_agg)

        comb_sales_latest_12w = self.comb_sales_12w(sales)

        comb_sales_4w_wtd = self.comb_sales_4w_wtd(sales)

        return (
            comb_sales_4w_wtd,
            comb_sales_latest_12w,
            train_4w_agg_vald_max_date,
            sales_pred_4w_agg_vald,
            train_vald_max_date,
            sales_pred_vald,
            sales_4w_agg,
            sales_pred_4w_agg,
            sales,
            sales_pred,
            cal_sales,
            sales_daily
        )
