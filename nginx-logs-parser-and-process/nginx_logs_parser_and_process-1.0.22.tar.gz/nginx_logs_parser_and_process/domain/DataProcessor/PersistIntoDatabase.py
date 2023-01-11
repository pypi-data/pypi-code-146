from pandas import DataFrame

from nginx_logs_parser_and_process.domain.Server.Server import Server
from nginx_logs_parser_and_process.infrastructure.Database import Database


class PersistIntoDatabase:
    def __init__(self, database: Database, server: Server):
        self.database = database
        self.database_conn = self.database.connect()
        self.server = server

    def process(self, dataframe: DataFrame):
        if self.database_conn:
            dataframe.to_sql(self.server.tables.temporal, self.database_conn, if_exists="append")
            self.database.pass_temporal_to_final_logs_table(self.server)
