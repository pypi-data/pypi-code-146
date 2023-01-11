from pydantic import BaseModel
from nginx_logs_parser_and_process.domain.Tables.tables import Tables


class Server(BaseModel):
    name: str
    source_path: str
    host: str = None
    port: int = 22
    includes: str = ""
    data_filter: list = []
    tables: Tables = None
    include_files: list =[]
