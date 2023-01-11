import os
import glob
from pandas import DataFrame
from urllib.parse import unquote
import hashlib
from nginx_logs_parser_and_process.domain.Server.Server import Server
from nginx_logs_parser_and_process.domain.DataProcessor.PersistIntoDatabase import PersistIntoDatabase
from nginx_logs_parser_and_process.infrastructure.Database import Database


class ReadAllLogsFileIntoMemoryUsingPandas:
    def __init__(self, pd):
        self.pd = pd

    def process(self, server: Server, remote_server: Server, database: Database) -> DataFrame:
        data: DataFrame = DataFrame()
        data_frames: list = []
        for log_file in self.get_files_list(server.source_path, server.includes):
            print(f"Processing file {log_file}")
            file_stats = os.stat(log_file)
            if file_stats.st_size > 0:
                df = self.pd.read_csv(
                    log_file,
                    sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
                    engine="python",
                    usecols=[0, 3, 4, 5, 6, 7, 8],
                    names=["ip", "str_datetime", "request", "status", "size", "referer", "user_agent"],
                    na_values="-",
                    header=None,
                    encoding="utf-8-sig",
                    converters={"request": unquote},
                )

                df = self.normalize_data(df, remote_server.name)
                df = self.eliminate_unnecessary_data(df, remote_server)

                # data_frames.append(df)

                # data = self.pd.concat(data_frames, axis=0, ignore_index=True)
                if not df.empty:
                    print(f"Saving {len(df.index)} rows. {df.shape[0]}")
                    PersistIntoDatabase(database, remote_server).process(df)
        return data

    def get_files_list(self, path: str, files_pattern: str) -> list[str]:
        files_patterns_list = files_pattern.split(",")
        files_list: list = []
        for pattern in files_patterns_list:
            files: list = glob.glob(f"{path}{pattern}")
            files.sort()
            files_list.extend(files)
        return files_list

    def normalize_data(self, dataframe: DataFrame, server_name: str) -> DataFrame:
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

    def eliminate_unnecessary_data(self, dataframe: DataFrame, remote_server: Server) -> DataFrame:
        # dataframe = dataframe.loc[dataframe["referer"] == '"https://seb.ops1.thunderbees.com.br/sgi/"']
        filtered_data: DataFrame = DataFrame(columns=dataframe.columns)
        for filter in remote_server.data_filter:
            clean_dataframe = dataframe.loc[dataframe[filter["field"]].str.contains(filter["value"], regex=True)]
            filtered_data = self.pd.concat([filtered_data, clean_dataframe])
        return filtered_data

        # filtered_data: DataFrame = DataFrame(columns=dataframe.columns)
        # clean_dataframe = filtered_data.loc[~dataframe["request"].str.contains('"POST /sounds/getSounds HTTP/1.1"', regex=True)]
        # filtered_data = self.pd.concat([filtered_data, clean_dataframe])
        # return filtered_data
