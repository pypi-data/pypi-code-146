import json
from .decorator import ensure_table_exists, ensure_connection, handle_transactions, sql_injection_safe, enforce_resource_limits
import pyexasol
import dask.dataframe as dd
import pandas as pd
import requests
import csv
import xlwt
import math


class Features(pyexasol.ExaConnection):
    PROTOCOL_V1 = 1
    PROTOCOL_V2 = 2
    PROTOCOL_V3 = 3

    DEFAULT_PORT = 8563
    DEFAULT_AUTOCOMMIT = True

    DEFAULT_CONNECTION_TIMEOUT = 10
    DEFAULT_SOCKET_TIMEOUT = 30
    DEFAULT_QUERY_TIMEOUT = 0

    DEFAULT_FETCHMANY_SIZE = 10000
    DEFAULT_FETCH_SIZE_BYTES = 5 * 1024 * 1024

    DRIVER_NAME = 'PyEXASOL'

    LOGGER_FILENAME_TIMESTAMP_FORMAT = '%Y%m%d_%H%M%S_%f'
    LOGGER_MAX_JSON_LENGTH = 20000

    EXCEPTION_QUERY_TEXT_MAX_LENGTH = 20000

    DATATYPE_MAPPING = {
        'int8': 'TINYINT',
        'int16': 'SMALLINT',
        'int32': 'INTEGER',
        'int64': 'BIGINT',
        'uint8': 'TINYINT',
        'uint16': 'SMALLINT',
        'uint32': 'INTEGER',
        'uint64': 'BIGINT',
        'float16': 'FLOAT',
        'float32': 'FLOAT',
        'float64': 'DOUBLE',
        'bool': 'BOOLEAN',
        'object': 'VARCHAR',
        'category': 'VARCHAR',
        'datetime64': 'TIMESTAMP',
        'timedelta[ns]': 'INTERVAL'
    }

    def __init__(self, dsn, user, password, schema=None, *args, **kwargs):
        super().__init__(dsn, user, password, schema)
        self.conn = pyexasol.ExaConnection(dsn, user, password, schema=schema)

        self.options = {}
        self.options['autocommit'] = self.DEFAULT_AUTOCOMMIT
        self.options['snapshot_transactions'] = None
        self.options['connection_timeout'] = self.DEFAULT_CONNECTION_TIMEOUT
        self.options['socket_timeout'] = self.DEFAULT_SOCKET_TIMEOUT
        self.options['query_timeout'] = self.DEFAULT_QUERY_TIMEOUT
        self.options['compression'] = False
        self.options['encryption'] = True
        self.options['fetch_size_bytes'] = self.DEFAULT_FETCH_SIZE_BYTES
        self.options['quote_ident'] = False
        self.options['json_lib'] = 'json'
        self.options['verbose_error'] = True
        self.options['debug'] = False
        self.options['debug_logdir'] = None
        self.options['udf_output_bind_address'] = None
        self.options['udf_output_connect_address'] = None
        self.options['udf_output_dir'] = None
        self.options['http_proxy'] = None
        self.options['client_name'] = None
        self.options['client_version'] = None
        self.options['client_os_username'] = None
        self.options['protocol_version'] = self.PROTOCOL_V3
        self.options['dsn'] = None
        self.options['user'] = None
        self.options['password'] = None
        self.options['schema'] = ''
        self.options['fetch_dict'] = False
        self.options['fetch_mapper'] = None
        self.options['lower_ident'] = False
        self.options['websocket_sslopt'] = None
        self.options['access_token'] = None
        self.options['refresh_token'] = None

    def connect(self, connection_params):
        self.conn = pyexasol.connect(connection_params)

    def close(self):
        self.conn.close()
        self.conn = None

    @ensure_connection
    def execute(self, sql, **kwargs):
        return self.conn.execute(sql, **kwargs)

    def fetchall(self, **kwargs):
        return self.execute.fetchall(**kwargs)

    def fetchone(self, **kwargs):
        return self.execute.fetchone(**kwargs)

    def fetchmany(self, size=None, **kwargs):
        return self.execute.fetchmany(size=size, **kwargs)

    @ensure_connection
    def commit(self):
        return self.conn.commit()

    @ensure_connection
    def rollback(self):
        return self.conn.rollback()

    def get_column_names(self, source):
        """Get the column names for a table, query, or CTE in Exasol."""
        if isinstance(source, pd.DataFrame):
            # Create the table from the DataFrame
            return source.columns.tolist()
        elif isinstance(source, dd.DataFrame):
            return source.compute().columns.tolist()
        else:
            return self.export_to_dask(f"SELECT * FROM {source} LIMIT 0").columns.tolist()

    def table_exists(self, table_name):
        # Check if the table exists by querying the EXA_ALL_TABLES system view
        result = self.conn.execute(f"SELECT 1 FROM EXA_ALL_TABLES WHERE TABLE_NAME = '{table_name}'")
        return bool(result.fetchone())

    def get_column_data_type_from_df(self, source, column):
        exa_data_type = self.DATATYPE_MAPPING[str(source[column].dtype)]
        if isinstance(source, dd.DataFrame):
            source = source.compute()
        if exa_data_type == 'VARCHAR':
            col_len = source[column].str.len().max()
            potenz = 10 ** (len(str(col_len)) - 1 if len(str(col_len)) > 1 else 1)
            col_max = math.ceil((col_len / potenz) + 0.5) * potenz
            exa_data_type = f'VARCHAR({col_max})'
        return exa_data_type

    def create_table_from_df(self, table_name, df):
        import math
        # Create a list of column definitions
        column_defs = []
        for col, dtype in zip(df.columns, df.dtypes):
            # Get the Exasol data type for the column
            exa_data_type = self.get_column_data_type_from_df(df, col)
            # Add the column definition to the list
            column_defs.append(f"{col} {exa_data_type}")
        # Join the column definitions with a comma separator
        column_defs_str = ",\n".join(column_defs)
        # Build the CREATE TABLE statement
        create_stmt = f"""
            CREATE TABLE {table_name} (
            {column_defs_str}
            )
        """
        # Execute the CREATE TABLE statement
        self.conn.execute(create_stmt)

    def create_table_from_table(self, target_table, source_table):
        # Build the CREATE TABLE AS SELECT statement
        create_stmt = f"CREATE TABLE {target_table} AS SELECT * FROM {source_table}"
        # Execute the CREATE TABLE AS SELECT statement
        self.conn.execute(create_stmt)

    def add_columns(self, table_name, column_names):
        # Iterate over the column names
        for column_name in column_names:
            # Build the ALTER TABLE ADD COLUMN statement
            alter_stmt = f"ALTER TABLE {table_name} ADD COLUMN {column_name[0]} {column_name[1]}"
            # Execute the ALTER TABLE ADD COLUMN statement
            self.conn.execute(alter_stmt)

    def get_column_data_type(self, table_name, column_name):
        # Query the EXA_ALL_COLUMNS system view to get the data type for the column
        result = self.conn.execute(f"SELECT COLUMN_TYPE FROM EXA_ALL_COLUMNS WHERE COLUMN_TABLE = '{table_name}' AND COLUMN_NAME = '{column_name}'")
        # Return the data type from the result
        return result.fetchone()[0]

    def export_to_dask(self, sql, chunksize=10000):
        return dd.from_pandas(self.conn.export_to_pandas(query_or_table=sql), chunksize=chunksize)

    @ensure_connection
    @ensure_table_exists
    def import_from_dask(self, source, target_table):
        source = source.compute()
        self.conn.import_from_pandas(source, target_table)

    @staticmethod
    def to_pandas(df):
        """Convert a Dask DataFrame to a Pandas DataFrame."""
        return df.compute()

    @staticmethod
    def to_json(self, df, path):
        """Convert a Dask DataFrame to a JSON file."""
        df.to_csv(path, index=False)

    @staticmethod
    def to_csv(self, df, path):
        """Convert a Dask DataFrame to a CSV file."""
        df.to_csv(path, index=False)

    def to_xml(self, df, path):
        """Convert a Dask DataFrame to an XML file."""
        # Open a file handle to the destination XML file
        with open(f'{path}.xml', 'w') as xml_file:
            # Use the Dask 'to_csv' method to write the DataFrame to a CSV stream
            df.to_csv(xml_file, index=False)

            # Seek back to the beginning of the stream
            xml_file.seek(0)

            # Write the XML header
            xml_file.write(f'<?xml version="1.0" encoding="UTF-8"?>\n')
            xml_file.write('<root>\n')

            # Create a CSV reader and iterate through the rows of the CSV stream
            reader = csv.reader(xml_file)
            for row in reader:
                # Write an XML element for each row, with each column as an attribute
                xml_file.write('  <row')
                for i, col in enumerate(row):
                    xml_file.write(f' col{i}="{col}"')
                xml_file.write('/>\n')

            # Write the XML footer
            xml_file.write('</root>\n')

    def to_excel(self, dd, path):
        """Convert a Dask DataFrame to an Excel file."""
        df = dd.compute()
        return df.to_excel(path, index=False)

    def to_sql_select(self, source, target_table='tmp_tbl'):
        # Prüfe, ob der source ein dask.DataFrame oder ein pandas.DataFrame ist
        if isinstance(source, dd.DataFrame):
            df = source.compute()
        elif isinstance(source, pd.DataFrame):
            df = source

        # Erstelle eine Liste von Spaltennamen und ihren Datentypen
        columns = [col.replace('-', '_').replace(' ', '_').replace('.', '_').replace('__', '_').upper() for col in df.columns.tolist()]
        name_type = []
        for col, name in zip(df.columns.tolist(), columns):
            ent = {}
            ent['df_col_name'] = col
            ent['tbl_col_name'] = name
            ent['is_number'] = all(isinstance(value, int) for value in df[col])
            name_type.append(ent)

        # Erstelle eine Liste von SELECT-Statements für jede Zeile im DataFrame
        selects = []
        for row in df.values:
            select = 'SELECT '
            for i, col in enumerate(name_type):
                select += "{val} AS {col}, ".format(**{"val": str(row[i]) if col['is_number'] else "'" + str(row[i]) + "'", "col": col['tbl_col_name']})
            selects.append(select)

        select_stmt = f"SELECT * FROM\n(\n"
        select_stmt += "\nUNION ALL\n".join([select.rstrip(', ') for select in selects])
        select_stmt += f'\n) AS {target_table}'
        return select_stmt

    @ensure_connection
    @ensure_table_exists
    def merge_tables(self, source, source_type, target_table, primary_columns=['@@@@@@@'], exclude_columns=[]):
        """Merge a table or query with an Exasol table, updating common columns and inserting new ones."""
        try:
            # Get the column names for the target table
            target_columns = self.get_column_names(target_table)

            # Determine the common columns between the source and target tables
            if source_type == "table":
                # Get the column names for the source table
                source_columns = self.get_column_names(source)
                common_columns = list(set(source_columns) & set(target_columns))
            elif source_type == "query":
                # Get the column names for the source query
                source = f'({source})'
                source_columns = [d[0] for d in self.get_column_names(source)]
                common_columns = list(set(source_columns) & set(target_columns))

            # Remove the excluded columns from the list of common columns
            all_common_columns = [col for col in common_columns if col not in exclude_columns]

            # Remove the primary columns from the list of common columns
            common_columns = [col for col in common_columns if col not in primary_columns]

            # Build the ON clause for the MERGE INTO statement
            on_clause = " AND ".join([f"TGT.{col} = SRC.{col}" for col in primary_columns])

            # Build the UPDATE SET clause for the MERGE INTO statement
            update_clause = ", ".join([f"TGT.{col} = SRC.{col}" for col in common_columns])

            # Build the INSERT clause for the MERGE INTO statement
            insert_clause = ", ".join(all_common_columns)

            # Build the full MERGE INTO statement
            merge_stmt = f"""
                MERGE INTO {target_table} TGT
                USING {source} SRC
                ON {on_clause}
                WHEN MATCHED THEN
                    UPDATE SET {update_clause}
                WHEN NOT MATCHED THEN
                    INSERT ({insert_clause})
                    VALUES ({insert_clause})
            """

            # Execute the MERGE INTO statement
            result = self.conn.execute(merge_stmt)
        except Exception as e:
            # Print the error message and raise the exception
            print(f"Error: {e}")
            raise e
        else:
            # Print the number of rows affected by the MERGE INTO statement
            print(f"{result.rowcount} rows affected")

    @ensure_connection
    @ensure_table_exists
    def merge_from_external(self, target_table, source, primary_columns=['@@@@@@@'], chunksize=10000):
        try:
            # Convert the source to a Dask DataFrame
            if isinstance(source, pd.DataFrame):
                source_df = dd.from_pandas(source, chunksize=chunksize)
            elif isinstance(source, dd.DataFrame):
                source_df = source
            elif isinstance(source, str):
                if source.endswith('.csv'):
                    source_df = dd.read_csv(source)
                elif source.endswith('.json'):
                    source_df = dd.read_json(source)
                elif source.endswith('.xml'):
                    source_df = dd.read_html(source)
                elif source.endswith('.xls') or source.endswith('.xlsx'):
                    source_df = dd.read_excel(source)
                else:
                    try:
                        json_str = json.loads(source)
                        source_df = dd.read_json(json_str)
                    except json.JSONDecodeError:
                        raise ValueError(
                            'Unable to determine source type. Please provide a valid file path or a valid DataFrame.')
            else:
                raise ValueError(
                    'Unable to determine source type. Please provide a valid file path or a valid DataFrame.')

            # Build the ON clause
            on_clause = " AND ".join([f"TGT.{col} = SRC.{col}" for col in primary_columns])

            # Get the column names for the target and source tables
            target_columns = self.get_column_names(target_table)
            source_columns = source_df.columns.tolist()

            # Get the common columns between the target and source tables
            common_columns = list(set(target_columns) & set(source_columns))

            # Build the UPDATE clause
            update_clause = ", ".join(
                [f"TGT.{col} = SRC.{col}" for col in common_columns if col not in primary_columns])

            # Build the INSERT clause
            insert_clause = ", ".join(common_columns)

            # Build the full MERGE INTO statement
            merge_stmt = f"""
                MERGE INTO {target_table} TGT
                USING {self.to_sql_select(source_df, 'test')} SRC
                ON {on_clause}
                WHEN MATCHED THEN
                    UPDATE SET {update_clause}
                WHEN NOT MATCHED THEN
                    INSERT ({insert_clause})
                    VALUES ({insert_clause})
            """

            # Execute the MERGE INTO statement
            result = self.conn.execute(merge_stmt)
        except Exception as e:
            # Print the error message and raise the exception
            print(f"Error: {e}")
            raise e
        else:
            # Print the number of rows affected by the MERGE INTO statement
            print(f"{result.rowcount} rows affected")

