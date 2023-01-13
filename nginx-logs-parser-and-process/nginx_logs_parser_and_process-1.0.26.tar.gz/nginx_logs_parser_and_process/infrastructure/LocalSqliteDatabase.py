import os
import sqlite3
from nginx_logs_parser_and_process.DI import DI
from nginx_logs_parser_and_process.domain.Server.Server import Server
from nginx_logs_parser_and_process.infrastructure.Database import Database


class LocalSqliteDatabase(Database):
    def __init__(self):
        self.engine = None
        self.database_file = f"{DI.project_root()}/data/logs.sqlite"
        super().__init__()

    def connect(self):
        if not self.engine:
            self.engine = sqlite3.connect(self.database_file)
        return self.engine

    def get_table_name(self) -> str:
        return "logs"

    def truncate_table(self, servers: list[Server]):
        os.remove(self.database_file)
        self.engine = None
        self.connect()

    def pass_temporal_to_final_logs_table(self, server: Server):
        pass
