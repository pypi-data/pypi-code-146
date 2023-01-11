import numpy as np
import pandas as pd

from txp.ml.common.tasks.encoder import Encoder


class VibrationEncoder(Encoder):

    def __init__(self, schema):
        super().__init__(schema)

    def transform_input_signals(self, signals_completed) -> pd.DataFrame:
        dataframe_row = {}
        for edge_logical_id in signals_completed:
            for perception_name in signals_completed[edge_logical_id]:
                for table_id in signals_completed[edge_logical_id][perception_name]:
                    rows = signals_completed[edge_logical_id][perception_name][table_id]
                    if table_id in ["time_metrics", "fft_metrics", "psd_metrics"]:
                        for row in rows:
                            for metric in self.schema[edge_logical_id][perception_name][table_id]:
                                dataframe_row[
                                    f'{metric}_{table_id}_{perception_name}_{edge_logical_id}_{row["dimension"]}'] \
                                    = row[metric]
                    else:
                        row = rows[0]
                        if table_id == "fft":
                            row["fft"] = [[np.complex128(complex(z["real"], z["imag"]))
                                           for z in dimension["values"]] for dimension in row["fft"]]
                        else:
                            row["psd"] = [dimension["psd"] for dimension in row["data"]]
                        for dimension in range(len(row[table_id])):
                            for i in range(len(row[table_id][dimension])):
                                dataframe_row[f"{table_id}_{perception_name}_{edge_logical_id}_{dimension}_{i}"] = \
                                    row[table_id][dimension][i].real

        dataset = pd.DataFrame()
        dataset = dataset.append(dataframe_row, ignore_index=True)
        columns = list(self.dataset.columns)
        columns.remove(self.target)

        return dataset[columns]

    def build_training_dataset(self, target, **kwargs):
        tables = kwargs['tables']
        self.target = target
        groups_time_df = tables['time_df'].groupby("observation_timestamp")
        groups_fft_df = tables['fft_df'].groupby(["observation_timestamp", "edge_logical_id", "perception_name"])
        groups_psd_df = tables['psd_df'].groupby(["observation_timestamp", "edge_logical_id", "perception_name"])
        groups_time_metrics_df = tables['time_metrics_df'].groupby(
            ["observation_timestamp", "edge_logical_id", "perception_name"])
        groups_fft_metrics_df = tables['fft_metrics_df'].groupby(["observation_timestamp", "edge_logical_id",
                                                                  "perception_name"])
        groups_psd_metrics_df = tables['psd_metrics_df'].groupby(["observation_timestamp", "edge_logical_id",
                                                                  "perception_name"])
        dataset = pd.DataFrame()

        for observation_timestamp, group_time_df in groups_time_df:
            row = self.__get_row(groups_time_metrics_df, groups_psd_metrics_df, groups_fft_metrics_df,
                                 observation_timestamp, groups_fft_df, groups_psd_df)
            if row:
                row[target] = group_time_df.iloc[0][target]
                dataset = dataset.append(row, ignore_index=True)

        self.dataset = dataset.replace(np.nan, 0)

        return self.dataset

    @staticmethod
    def __get_metrics(observation_timestamp, perception, group_dataframe, name, df_metrics, edge_logical_id):

        if (observation_timestamp, edge_logical_id, perception) not in group_dataframe.groups:
            return {}
        window_df = group_dataframe.get_group((observation_timestamp, edge_logical_id, perception))
        if len(window_df) < 3:
            return {}
        res = {}
        for _, signal in window_df.iterrows():
            for metric in df_metrics:
                res[f'{metric}_{name}_{perception}_{edge_logical_id}_{signal["dimension"]}'] = signal[metric]
        return res

    @staticmethod
    def __get_vector_magnitude(observation_timestamp, perception, group_dataframe, name, edge_logical_id):
        if (observation_timestamp, edge_logical_id, perception) not in group_dataframe.groups:
            return {}
        window_df = group_dataframe.get_group((observation_timestamp, edge_logical_id, perception))
        if len(window_df) != 1:
            return {}
        res = {}
        signal = window_df.iloc[0]
        for dimension in range(len(signal[name])):
            for i in range(len(signal[name][dimension])):
                res[f"{name}_{perception}_{edge_logical_id}_{dimension}_{i}"] = signal[name][dimension][i].real
        return res

    def __get_row(self, groups_time_metrics_df, groups_psd_metrics_df, groups_fft_metrics_df, observation_timestamp,
                  groups_fft_df, groups_psd_df):
        row = {}
        for edge_logical_id in self.schema:
            for perception in self.schema[edge_logical_id]:

                if "time_metrics" in self.schema[edge_logical_id][perception]:
                    row_metrics = self.__get_metrics(observation_timestamp, perception, groups_time_metrics_df,
                                                     "time_metrics",
                                                     self.schema[edge_logical_id][perception]["time_metrics"],
                                                     edge_logical_id)
                    if not row_metrics:
                        return {}
                    row = {**row, **row_metrics}

                if "psd_metrics" in self.schema[edge_logical_id][perception]:
                    row_metrics = self.__get_metrics(observation_timestamp, perception, groups_psd_metrics_df,
                                                     "psd_metrics",
                                                     self.schema[edge_logical_id][perception]["psd_metrics"],
                                                     edge_logical_id)
                    if not row_metrics:
                        return {}
                    row = {**row, **row_metrics}

                if "fft_metrics" in self.schema[edge_logical_id][perception]:
                    row_metrics = self.__get_metrics(observation_timestamp, perception, groups_fft_metrics_df,
                                                     "fft_metrics",
                                                     self.schema[edge_logical_id][perception]["fft_metrics"],
                                                     edge_logical_id)
                    if not row_metrics:
                        return {}
                    row = {**row, **row_metrics}

                if "fft" in self.schema[edge_logical_id][perception] and \
                        self.schema[edge_logical_id][perception]["fft"]:
                    vector_magnitude = self.__get_vector_magnitude(observation_timestamp, perception, groups_fft_df,
                                                                   "fft", edge_logical_id)
                    if not vector_magnitude:
                        return {}
                    row = {**row, **vector_magnitude}

                if "psd" in self.schema[edge_logical_id][perception] and \
                        self.schema[edge_logical_id][perception]["psd"]:
                    vector_magnitude = self.__get_vector_magnitude(observation_timestamp, perception, groups_psd_df,
                                                                   "psd", edge_logical_id)
                    if not vector_magnitude:
                        return {}
                    row = {**row, **vector_magnitude}

        return row