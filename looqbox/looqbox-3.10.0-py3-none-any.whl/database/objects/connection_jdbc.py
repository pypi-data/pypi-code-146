from looqbox.database.database_exceptions import TimeOutException, alarm_handler
from looqbox.database.objects.connection_base import BaseConnection
from looqbox.global_calling import GlobalCalling
from looqbox.utils.utils import base64_decode
from jaydebeapi import connect, Connection, DatabaseError
from platform import system
from multimethod import multimethod
import pandas as pd
import datetime
import signal
import jaydebeapi


class JDBCConnection(BaseConnection):

    def __init__(self, connection_name: str, parameter_as_json=False, use_all_jars=True):
        super().__init__()
        self.connection_alias = connection_name
        self.connection_object = Connection

        self.parameter_as_json = parameter_as_json
        self.import_all_jars_files = use_all_jars

    def set_query_script(self, sql_script: str) -> None:
        self.query = sql_script

    def connect(self) -> None:
        credential = self._get_connection_credentials(self.connection_alias)
        self._open_jdbc_connection(credential)

    def _open_jdbc_connection(self, connection_credential) -> None:
        # build driver_args to enable connections that rather use or not user and password
        if self._is_user_and_password_empty(connection_credential):
            driver_args = {}
        else:
            driver_args = {
                'user': connection_credential['user'],
                'password': base64_decode(connection_credential['pass'])
            }

        # Since jaydebeapi instantiate a JVM to perform the db connection, any kind of alteration (jar/drive
        # insertion or removing) are impossible, thus being essential to shut down the current JVM (create an error
        # in Looqbox Kernel) in this regard, all jars are imported into the JVM by default
        jars_path = self._get_all_jar_files() if self.import_all_jars_files else connection_credential["jar"]
        self.connection_object = connect(
                                          connection_credential['driver'],
                                          connection_credential['connString'],
                                          driver_args,
                                          jars=jars_path,
                                         )

    def _is_user_and_password_empty(self, connection_credential: dict) -> bool:
        return connection_credential['user'] == '' and connection_credential['pass'] == ''

    def _get_all_jar_files(self) -> list:
        """
        Get and append all jar files required for each entry in connection.json
        """

        jar_list = list()
        file_connections = self._get_connection_file()

        # get the jar files for each connection
        for connections in file_connections:

            # Avoid errors due some wrong connection register
            try:
                connection_jar = self._get_connection_credentials(connections)["jar"]
            except:
                connection_jar = []

            jar_list.extend(connection_jar)
        return jar_list

    def _get_connection_credentials(self, connection: str) -> dict:
        """
        Get credentials for a list of connections.

        :param connection: String or list of database names
        :return: A Connection object
        """
        driver_path = []
        connection_credential = self._get_connection_file()

        try:
            if not self.parameter_as_json:
                connection_credential = GlobalCalling.looq.connection_config[connection]
            else:
                connection_credential = connection_credential[connection]
        except KeyError:
            raise Exception(
                "Connection " + connection + " not found in the file " + GlobalCalling.looq.connection_file)

        if self._connection_have_driver(connection_credential):
            driver_path = self._get_drivers_path(connection_credential, driver_path)
        connection_credential["jar"] = driver_path
        return connection_credential

    def _connection_have_driver(self, connection) -> bool:
        return connection.get('driverFile') is not None

    def _get_drivers_path(self, connection_credential, driver_path) -> str:
        import os

        conn_file_name, conn_file_extension = os.path.splitext(connection_credential['driverFile'])
        old_driver_folder_path = os.path.join(GlobalCalling.looq.jdbc_path + '/' + conn_file_name + conn_file_extension)
        new_driver_folder_path = os.path.join(GlobalCalling.looq.jdbc_path + '/' + conn_file_name)
        if new_driver_folder_path:
            for file in os.listdir(new_driver_folder_path):
                if self._is_jar(file):
                    driver_path.append(new_driver_folder_path + '/' + file)

        elif old_driver_folder_path:
            driver_path = old_driver_folder_path
        return driver_path

    def _is_jar(self, file: str) -> bool:
        return not file.startswith('.') and '.jar' in file

    def _call_query_executor(self, start_time, query_mode="single"):
        try:
            self._get_query_result()
            total_sql_time = datetime.datetime.now() - start_time
            GlobalCalling.log_query({"connection": self.connection_alias, "query": self.query,
                                     "time": str(total_sql_time), "success": True, "mode": query_mode})

            self._update_response_timeout(total_sql_time)

        except DatabaseError as error:
            self.close_connection()
            total_sql_time = datetime.datetime.now() - start_time

            GlobalCalling.log_query({"connection": self.connection_alias, "query": self.query,
                                     "time": str(total_sql_time), "success": False, "mode": query_mode})

            raise error

    def _get_query_result(self) -> None:
        """
        Function to get the table resulting from the query
        """

        conn_curs = self.connection_object.cursor()

        conn_curs.execute(self.query)
        col_names = [i[0] for i in conn_curs.description]
        fetch_tuple = conn_curs.fetchall()

        metadata = self._get_column_types(conn_curs)

        # Fix error when fetch brings one None row
        query_df = pd.DataFrame()
        if fetch_tuple or len(fetch_tuple) > 0:
            if len(fetch_tuple[0]) == 1:
                if fetch_tuple[0][0] is not None:
                    query_df = pd.DataFrame(fetch_tuple, columns=col_names)
            else:
                query_df = pd.DataFrame(fetch_tuple, columns=col_names)

        self.retrieved_data = query_df
        self.query_metadata = metadata

    def _generate_cache_file_name(self) -> str:
        """
        Cache file name is created by encrypt the sql script into a MD5
        string, thus avoiding duplicated names.
        """
        from hashlib import md5

        file_name = self.connection_alias + self.query
        hashed_file_name = md5(file_name.encode())
        return str(hashed_file_name.hexdigest()) + ".rds"

    def _get_column_types(self, cursor: jaydebeapi.Cursor) -> dict:
        metadata = dict()
        for column in cursor.description:
            column_name = column[0]
            column_type = self._filter_types(column[1].values)
            metadata[column_name] = {
                "type": column_type
            }
        return metadata

    def _filter_types(self, type_list: list) -> str:
        type_dict = {
            'CHAR': ('CHAR', 'NCHAR', 'NVARCHAR', 'VARCHAR', 'OTHER'),
            'LONGVARCHAR': ('CLOB', 'LONGVARCHAR', 'LONGNVARCHAR', 'NCLOB', 'SQLXML'),
            'BINARY': ('BINARY', 'BLOB', 'LONGVARBINARY', 'VARBINARY'),
            'INTEGER': ('BOOLEAN', 'BIGINT', 'BIT', 'INTEGER', 'SMALLINT', 'TINYINT'),
            'FLOAT': ('FLOAT', 'REAL', 'DOUBLE'),
            'NUMERIC': ('DECIMAL', 'NUMERIC'),
            'DATE': ('DATE',),
            'TIME': ('TIME',),
            'TIMESTAMP': ('TIMESTAMP',),
            'ROWID': ('ROWID',)
        }
        column_type = None
        for db_type, aliases in type_dict.items():
            if type_list == aliases:
                column_type = db_type
        return column_type

    def close_connection(self) -> None:
        self.connection_object.close()
