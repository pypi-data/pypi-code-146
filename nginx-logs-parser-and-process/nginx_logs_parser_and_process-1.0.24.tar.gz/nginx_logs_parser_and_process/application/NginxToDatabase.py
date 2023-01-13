from typing import List
from tabulate import tabulate

from nginx_logs_parser_and_process.domain.DataProcessor.EliminateUnnecessaryData import EliminateUnnecessaryData
from nginx_logs_parser_and_process.domain.DataProcessor.NormalizeModelData import NormalizeModelData
from nginx_logs_parser_and_process.domain.DataProcessor.PersistIntoDatabase import PersistIntoDatabase
from nginx_logs_parser_and_process.domain.Logs.ReadAllLogsFileIntoMemoryUsingPandas import ReadAllLogsFileIntoMemoryUsingPandas
from nginx_logs_parser_and_process.domain.Server.Server import Server
from nginx_logs_parser_and_process.domain.Server.SynchronizeRemoteNginxLogsWithLocalRepository import \
    SynchronizeRemoteNginxLogsWithLocalRepository


class NginxToDatabase:
    def __init__(self, data_processor, database):
        self.data_processor = data_processor
        self.database = database

    def process(self, origin_servers: List[Server], destination_server: Server):
        try:
            for remote_server in origin_servers:
                SynchronizeRemoteNginxLogsWithLocalRepository().process(remote_server, destination_server)
                raw_data = ReadAllLogsFileIntoMemoryUsingPandas(self.data_processor)\
                    .process(destination_server, remote_server, self.database)
                # normalized_data = NormalizeModelData(self.data_processor).process(raw_data, remote_server.name)
                # clean_data = EliminateUnnecessaryData(self.data_processor, remote_server).process(normalized_data)
                # clean_data = normalized_data
                # PersistIntoDatabase(self.database, remote_server).process(clean_data)

                # InformProcessExecutionStatus(SucessMessage())
                # print(clean_data.info())
                # print(clean_data[["str_datetime", "log_datetime", "log_date"]])
                # print(tabulate(clean_data.tail(10), showindex=False, headers="keys"))
                # print(tabulate(raw_data.tail(100)[["UserLogin", "request"]], showindex=False, headers="keys"))
        except Exception as error:
            print(error)
            #     InformProcessExecutionStatus(FailedMessage())
