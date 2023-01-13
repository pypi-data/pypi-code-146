#!/usr/bin/env python3
#%% 
from raumo_data_tools.config_handler import ConfigHandler
from influxdb_client import InfluxDBClient
import pandas as pd
import json
from datetime import timedelta
import numpy as np

class QueryInflux():
    def __init__(self, config):
        self.config = config
        self.client = InfluxDBClient(url=self.config.URL, token=self.config.TOKEN, org=self.config.ORG)

    def _concat_list_result(self, result):
        df = pd.DataFrame()

        if type(result) is list:
            for frame in result:
                df = pd.concat([df, frame])
        else:
            df = result

        return df

    def _process_pivot_result(self, df, columns=None):
        if columns == None: 
            columns = "_field"
        df.index = df._time
        df=df.drop(columns= ["result", "table", "_start", "_stop", "_measurement", "_time"])
        df = df.pivot_table(index="_time", columns="_field")
        df = df["_value"]
        df.fillna(0, inplace=True)
        
        return df

    def run_query(self, query):
        query_api = self.client.query_api()
        result = query_api.query_data_frame(query=query)
        df = self._concat_list_result(result)
        df.fillna(0, inplace=True)

        return df

#%%
class GetInfluxData():
    def __init__(self, start, stop, config_path):
        self.start = start
        self.stop = stop
        with open(config_path, 'r') as f:
            self.data_format_dict = json.load(f)

    def _construct_tags_filter(self, tags):
        filter_str = 'r["'
        for key, value in tags.items():
            if key == list(tags)[-1]:
                filter_str += key + '"] == "' + value + '"'
            else:
                filter_str += key + '"] == "' + value + '" or r["'
        return filter_str

    def _apply_time_filter(self, df):
        
        after_interval_first_day = df.index.date>=self.START
        before_last_month_last_day = df.index.date<=END
        between_dates = after_interval_first_day & before_last_month_last_day

        return df[between_dates]

    def _validate_dataset(self, df):
        if (len(pd.unique(df["_field"])) == 1) & (len(pd.unique(df["_measurement"])) == 1):
            return
        else:
            print("There are fields or measurements which are not exclusive.")

    def _replace_zero(self, df):
        """Replacing infinite values in the dataframe by the mean of the value's neighbors

        Args:
            series (pd.Series): series with values to replace

        Returns:
            pd.Series: series with replaced values
        """
        df_mean = df["_value"].mean()
        threshold = df_mean*0.05
        print(threshold)

        if df_mean > 5: #ensures that real zeros are not replaced
            idxs = df[df["_value"] < threshold].index

            if len(idxs) > 0:
                for idx in idxs:
                    idx_before = idx - timedelta(days=7)
                    idx_after = idx + timedelta(days=7)
                
                    try:
                        value = np.mean([df["_value"][idx_before], df["_value"][idx_after]])
                        df["_value"][idx] = value
                        print(f"replaced data at index {idx} with {value}")
                    except KeyError:
                        print("A key error was thrown")

        return df

    def _replace_inf(self, df):
        """Replacing infinite values in the dataframe by the mean of the value's neighbors

        Args:
            series (pd.Series): series with values to replace

        Returns:
            pd.Series: series with replaced values
        """
        idx = np.where(df["_value"] == np.inf)[0]
        if len(idx) > 0:
            value = np.mean([df.iloc[idx-1]["_value"], df.iloc[idx+1]["_value"]])
            df["_value"].iloc[idx] = value
        return df

    def query_fields_df(self, reader, bucket, measurement, field):
        flux_query = '''
        from(bucket:"{}")
            |> range(start: {}, stop: {} )
            |> filter(fn: (r) => r["_measurement"] == "{}")
            |> filter(fn: (r) => r["_field"] == "{}")
            |> drop(columns: ["_start", "_stop"])
        '''.format(bucket, self.start, self.stop, measurement, field)

        df = reader.query_data_frame(flux_query)
        df.index=pd.to_datetime(df["_time"])
        df=df.drop(labels="_time",axis=1)
        return df

    def query_fields_df_custom(self, reader, bucket, measurement, field, custom_filter):
        flux_query = '''
        from(bucket:"{}")
            |> range(start: {}, stop: {} )
            |> filter(fn: (r) => r["_measurement"] == "{}")
            |> filter(fn: (r) => r["_field"] == "{}")
            {}
            |> drop(columns: ["_start", "_stop"])
        '''.format(bucket, self.start, self.stop, measurement, field, custom_filter)

        df = reader.query_data_frame(flux_query)
        df.index=pd.to_datetime(df["_time"])
        df=df.drop(labels="_time",axis=1)
        return df

    def query_fields_tags_df(self, reader, bucket, measurement, field, tags):
        flux_query = '''
        from(bucket:"{}")
            |> range(start: {}, stop: {} )
            |> filter(fn: (r) => r["_measurement"] == "{}")
            |> filter(fn: (r) => r["_field"] == "{}")
            |> filter(fn: (r) => {})
            |> drop(columns: ["_start", "_stop"])
        '''.format(bucket, self.start, self.stop, measurement, field, self._construct_tags_filter(tags))

        df = reader.query_data_frame(flux_query)
        df.index=pd.to_datetime(df["_time"])
        df=df.drop(labels="_time",axis=1)
        return df

    def read_data(self, data_type, dataset_name, agg_interval=None, agg_type="sum"):
        """Read data from the InfluxDB-dataset. The file data_format.json defines where the data is 
        stored in which fields.

        Args:
            data_type (str): first level of data_format.json. "Tracking" or "Logs"
            dataset_name (str): second level of data_format.json. Name of the dataset.
            agg_interval (str, optional): Interval for aggregation. Options: "1d", "1w", "M". Defaults to none.
            agg_type (str, optional): Type for aggregation. Options: "sum" or "mean". Defaults to "sum".

        Returns:
            pd.DataFrame: Data ready for visualization
        """
        info = self.data_format_dict[data_type][dataset_name]
        print(f"Dataset name = {dataset_name}")
        config = ConfigHandler(info["config"])
        influx_client = InfluxDBClient(url=config.URL, token=config.TOKEN, org=config.ORG)
        query_api = influx_client.query_api()
        if "tags" in info:
            df = self.query_fields_tags_df(query_api, info["bucket"], info["measurement"], info["field"], info["tags"])
        else:
            df = self.query_fields_df(query_api, info["bucket"], info["measurement"], info["field"])
        self._validate_dataset(df)

        df = df[["_value"]]

        if agg_interval:
            if agg_type == "sum":
                df = df.groupby(pd.Grouper(freq=agg_interval)).sum()
            elif agg_type == "mean":
                df = df.groupby(pd.Grouper(freq=agg_interval)).mean()
            if agg_interval == '1d':
                df = self._replace_zero(df)

        return df
"""
if __name__ == "__main__":
    TODAY = date.today()
    TODAY.strftime("%Y-%m-%d")
    THIS_MONTH_FIRST_DAY = TODAY.replace(day=1)
    LAST_MONTH_LAST_DAY = THIS_MONTH_FIRST_DAY - timedelta(days=1)
    LAST_MONTH_FIRST_DAY = LAST_MONTH_LAST_DAY.replace(day=1)

    END = LAST_MONTH_LAST_DAY

    config_path = 'configs/data_format.json'

    ir = GetInfluxData(LAST_MONTH_FIRST_DAY, TODAY, config_path=config_path)

    df_tickets = ir.read_data("Tracking", "KVV-Ticket-Buchungen", agg_interval="1d", agg_type="sum")

    df_logs = ir.read_data("Logs", "KVV-Ticket-Buchungen", agg_interval="M")

    df_init = ir.read_data("INIT", "Umsaetze", agg_interval="1d")
    print(df_init.head())
"""

# %%
