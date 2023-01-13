from abc import ABC
from nginx_logs_parser_and_process.domain.Server.Server import Server


class Database(ABC):
    def __init__(self):
        pass

    def connect(self):
        raise NotImplementedError

    def get_table_name(self) -> str:
        raise NotImplementedError

    def truncate_table(self, servers: list[Server]):
        raise NotImplementedError

    def pass_temporal_to_final_logs_table(self, server: Server):
        raise NotImplementedError
