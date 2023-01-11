import click
import pandas as pd
from nginx_logs_parser_and_process.DI import DI
from nginx_logs_parser_and_process.application.NginxToDatabase import NginxToDatabase
from nginx_logs_parser_and_process.domain.Server.Server import Server
from nginx_logs_parser_and_process.domain.Tables.tables import Tables
from nginx_logs_parser_and_process.infrastructure.CanadaThreeDatabase import CanadaThreeDatabase
from nginx_logs_parser_and_process.infrastructure.LocalSqliteDatabase import LocalSqliteDatabase


@click.command()
def process_remote_nginx_logs():
    remote_servers: list[Server] = []
    tb_data_to_preserve: list = [{"field": "request", "value": "POST /access/authenticate"}]
    seb_data_to_preserve: list = [
        {"field": "request", "value": "/api/portal-aluno/user/authenticate-sgi-user"},
        {"field": "request", "value": "POST /api/access/authenticate"},
    ]
    tb_tables = Tables(final="logs", temporal="temporal_logs", clean_log="logs2")
    seb_tables = Tables(final="seb_logs", temporal="seb_temporal_logs", clean_log="seb_logs2")
    tb_nginx = Server(
        host="tbnginxasroot",
        source_path="/var/log/nginx/",
        name="TB Nginx Server",
        data_filter=tb_data_to_preserve,
        tables=tb_tables,
        include_files=["portaldoalunobeta*",
                       "portaldoalunodevelop*",
                       "seb.*"
                       ]
    )
    seb_nginx = Server(
        host="tbnginxsebasroot",
        source_path="/var/log/nginx/",
        name="SEB Nginx Server",
        data_filter=seb_data_to_preserve,
        tables=seb_tables,
        include_files=["portaldoalunobeta*",
                       "portaldoalunodevelop*",
                       "seb.*"
                       ]
    )
    remote_servers.append(tb_nginx)
    remote_servers.append(seb_nginx)
    local_server = Server(source_path=DI.logs_path(),
                          name="Local Server",
                          includes="seb.access.log*,seb.portalaluno.ops1.access.log*,seb.ops1.portaldoaluno.access.log*")
    database = CanadaThreeDatabase() # LocalSqliteDatabase()
    database.connect()
    database.truncate_table(remote_servers)
    NginxToDatabase(pd, database=database).process(remote_servers, local_server)


if __name__ == "__main__":
    process_remote_nginx_logs()
