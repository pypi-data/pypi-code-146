import logging
from rebel import Database, PgsqlDriver
from hashids import Hashids
import base64


class Sabi_Postgresql:
    session = None
    logger = None
    db = None
    schema = None
    private_key = None
    server = None
    lambda_client = None
    generic_hashid = None

    def __init__(self, hashid_salt, host, user, password, database, schema=None, port=5432, timezone=""):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.schema = schema
        self.generic_hashid = Hashids(salt=hashid_salt, min_length=16)

        driver = PgsqlDriver(host=host, port=int(port), database=database, user=user, password=password)
        self.db = Database(driver)
        if schema != None:
            self.db.execute(f"SET search_path TO :schema", schema=self.schema)
            self.generic_hashid = Hashids(salt=hashid_salt, min_length=16)

        if timezone != "":
            self.db.execute(f"SET TIMEZONE=:timezone; ", timezone=timezone)

    def encode(self, string):
        if string is None:
            return_value = None
        else:
            return_value = self.generic_hashid.encode(string)

        return return_value

    def decode(self, string):
        if string is None:
            return_value = None
        else:
            return_value = self.generic_hashid.decode(string)
            if len(return_value) > 0:
                return_value = return_value[0]
        return return_value

    def encode_to_base64(self, string):
        return base64.b64encode(bytes(string, "utf-8")).decode("utf-8")

    def decode_from_base64(self, string):
        base64_bytes = string.encode("ascii")
        message_bytes = base64.b64decode(base64_bytes)
        decoded = message_bytes.decode("ascii")
        return decoded

    def query(self, sql, params={}):
        rows = self.db.query(sql, **params)
        return rows

    def refresh_materialized_view(self, logger, schema_name, view_name):
        sql = self.db.sql(
            f"""
            SELECT pid FROM pg_stat_activity WHERE state='active' AND query LIKE 'REFRESH MATERIALIZED VIEW CONCURRENTLY "{schema_name}"."{view_name}"'
            """
        )
        current_processes = sql.query()

        # Cancel an existing run if there is one
        if len(current_processes) > 0:
            logger.info(f"Cancelling existing refresh run for {schema_name} - {view_name}")
            self.db.query("SELECT pg_cancel_backend(:pid);", pid=current_processes[0]["pid"])
        logger.info(f"Starting refresh run for {schema_name} - {view_name}")
        sql = self.db.sql(f'REFRESH MATERIALIZED VIEW CONCURRENTLY "{schema_name}"."{view_name}"')
        sql.execute()

    def check_view_refresh_run(self, logger, schema_name, view_name):
        current_processes = self.db.query(
            f"""SELECT pid FROM pg_stat_activity WHERE state='active' AND query LIKE 'REFRESH MATERIALIZED VIEW CONCURRENTLY "{schema_name}"."{view_name}"';""",
            schema=schema_name,
            view_name=view_name,
        )
        return_value = False

        if len(current_processes) > 0:
            logger.info(f"Confirmed that {schema_name} - {view_name} is running")
            return_value = True
        else:
            logger.info(f"{schema_name} - {view_name} is not running")
        return return_value

    def get_sql_as_string(self, sql):
        full_sql = ""
        for part in sql.parts:
            args = []
            for arg in part["args"]:
                if type(arg) is tuple:
                    append_string = arg[0]
                else:
                    append_string = arg

                if isinstance(append_string, str):
                    args.append("'" + append_string + "'")
                else:
                    args.append(append_string)

            full_sql += part["sql"].replace("?", "{}").format(*args)
        full_sql = full_sql.replace("None", "NULL")
        return full_sql
