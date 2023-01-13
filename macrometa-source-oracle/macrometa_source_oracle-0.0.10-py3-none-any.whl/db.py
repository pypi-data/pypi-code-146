import singer
from singer import metadata, utils
import macrometa_source_oracle.sync_strategies.common as common
import cx_Oracle

LOGGER = singer.get_logger()

def fully_qualified_column_name(schema, table, column):
    return '"{}"."{}"."{}"'.format(schema, table, column)

def make_dsn(config):
   return cx_Oracle.makedsn(config["host"], config["port"], service_name=config["service_name"])

def open_connection(config):
    LOGGER.info("dsn: %s", make_dsn(config))
    conn = cx_Oracle.connect(config["user"], config["password"], make_dsn(config))
    return conn

def fetch_samples(conn_config: dict, stream):
    md_map = metadata.to_map(stream.metadata)
    conn_config['dbname'] = md_map.get(()).get('database-name')
    desired_columns = [c for c in stream.schema.properties.keys() if common.should_sync_column(md_map, c)]
    desired_columns.sort()

    if len(desired_columns) == 0:
        LOGGER.warning('There are no columns selected for stream %s, skipping it', stream.tap_stream_id)
        return []

    if md_map.get((), {}).get('is-view'):
        state = fetch_view(conn_config, stream, desired_columns)
    else:
        state = fetch_table(conn_config, stream, desired_columns)
    return state


def fetch_table(conn_config, stream, desired_columns):
    samples = []
    with open_connection(conn_config) as connection:
        connection.outputtypehandler = common.OutputTypeHandler
        with connection.cursor() as cur:
            cur.execute("ALTER SESSION SET TIME_ZONE = '00:00'")
            if conn_config['multitenant']:
                cur.execute(f"ALTER SESSION SET CONTAINER = {conn_config['pdb_name']}") #Switch to expected PDB
            cur.execute("""ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD"T"HH24:MI:SS."00+00:00"'""")
            cur.execute("""ALTER SESSION SET NLS_TIMESTAMP_FORMAT='YYYY-MM-DD"T"HH24:MI:SSXFF"+00:00"'""")
            cur.execute("""ALTER SESSION SET NLS_TIMESTAMP_TZ_FORMAT  = 'YYYY-MM-DD"T"HH24:MI:SS.FFTZH:TZM'""")
            time_extracted = utils.now()

            md = metadata.to_map(stream.metadata)
            schema_name = md.get(()).get('schema-name')
            escaped_columns = map(lambda c: common.prepare_columns_sql(stream, c), desired_columns)
            escaped_schema  = schema_name
            escaped_table   = stream.table
            select_sql      = """SELECT {} FROM {}.{}
                            ORDER BY ORA_ROWSCN ASC
                            FETCH FIRST 5 ROWS ONLY""".format(','.join(escaped_columns), escaped_schema, escaped_table)

            LOGGER.info("select %s", select_sql)
            for row in cur.execute(select_sql):
                row = row[:-1]
                record_message = common.row_to_singer_message(stream, row, None, desired_columns, time_extracted)
                samples.append(record_message.record)
    return samples


def fetch_view(conn_config, stream, desired_columns):
    samples = []
    with open_connection(conn_config) as connection:
        connection.outputtypehandler = common.OutputTypeHandler
        with connection.cursor() as cur:
            cur.execute("ALTER SESSION SET TIME_ZONE = '00:00'")
            if conn_config['multitenant']:
                cur.execute(f"ALTER SESSION SET CONTAINER = {conn_config['pdb_name']}") #Switch to expected PDB
            cur.execute("""ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD"T"HH24:MI:SS."00+00:00"'""")
            cur.execute("""ALTER SESSION SET NLS_TIMESTAMP_FORMAT='YYYY-MM-DD"T"HH24:MI:SSXFF"+00:00"'""")
            cur.execute("""ALTER SESSION SET NLS_TIMESTAMP_TZ_FORMAT  = 'YYYY-MM-DD"T"HH24:MI:SS.FFTZH:TZM'""")
            time_extracted = utils.now()

            md = metadata.to_map(stream.metadata)
            schema_name = md.get(()).get('schema-name')
            escaped_columns = map(lambda c: common.prepare_columns_sql(stream, c), desired_columns)
            escaped_schema  = schema_name
            escaped_table   = stream.table
            select_sql      = 'SELECT {} FROM {}.{}'.format(','.join(escaped_columns), escaped_schema, escaped_table)

            LOGGER.info("select %s", select_sql)
            for row in cur.execute(select_sql):
                record_message = common.row_to_singer_message(stream, row, None, desired_columns, time_extracted)
                samples.append(record_message.record)
    return samples
