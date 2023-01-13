import hashlib
from pandas import DataFrame


class NormalizeModelData:
    def __init__(self, pd):
        self.pd = pd

    def process(self, dataframe: DataFrame, server_name: str) -> DataFrame:
        if not dataframe.empty:
            dataframe["log_datetime"] = self.pd.to_datetime(
                dataframe["str_datetime"].str.replace("[\[\]]", "", regex=True), format="%d/%b/%Y:%H:%M:%S %z"
            ).dt.tz_convert("America/Sao_Paulo")

            dataframe["log_date"] = dataframe["log_datetime"].dt.strftime("%d/%m/%Y")
            dataframe["log_time"] = dataframe["log_datetime"].dt.strftime("%H:%M:%S %z")
            dataframe["logged"] = dataframe["status"] == 200
            dataframe["data_from_server"] = server_name

            cols = dataframe.columns.values.tolist()
            dataframe['uniqueid'] = dataframe[cols].apply(lambda row: hashlib.md5(str(''.join(row.values.astype(str))).encode()).hexdigest(), axis=1)
        return dataframe
