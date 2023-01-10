from looqbox.database.database_exceptions import TimeOutException, alarm_handler
from looqbox.database.objects.connection_base import BaseConnection
from looqbox.global_calling import GlobalCalling
from multimethod import multimethod
from platform import system
import pandas as pd
import pymongo
import datetime
import signal
import re


class MongoConnection(BaseConnection):
    def __init__(self, connection_name: str,  **additional_args):
        super().__init__()
        self.connection_alias = connection_name
        self.connection_object = pymongo.mongo_client
        self.response_timeout = GlobalCalling.looq.response_timeout if not self.test_mode else 0

        self.database_name_pattern = "(?<=\\w/)\\w+(?=[/\\w+]?)"

    def set_query_script(self, sql_script: dict) -> None:
        self.query = sql_script

    def connect(self):
        connection_credentials = self._get_connection_credentials(self.connection_alias)
        self.connection_object = self._open_mongo_connection(connection_credentials)

    def _open_mongo_connection(self, connection_credential: dict) -> pymongo.mongo_client:
        # Since the original object MongoClient, it's the one that has the close connection method,
        # it must be passed forward, until the very end of sql_execute
        self.database = self._get_database_from_mongo_connString(connection_credential.get("connString"))
        mongo_connection = pymongo.MongoClient(connection_credential.get("connString"))
        return mongo_connection

    def _get_database_from_mongo_connString(self, connection_string: str) -> str:
        database_name = re.findall(self.database_name_pattern, connection_string)[0]
        return database_name

    def set_database_name_pattern(self, pattern: str) -> None:
        self.database_name_pattern = pattern

    def _get_connection_credentials(self, connection: str, parameter_as_json=False) -> dict:
        """
        Get credentials for a list of connections.

        :param connection: String or list of database names
        :param parameter_as_json: Set if the parameters will be in JSON format or not
        :return: A Connection object
        """

        connection_credential = self._get_connection_file()

        try:
            if not parameter_as_json:
                connection_credential = GlobalCalling.looq.connection_config[connection]
            else:
                connection_credential = connection_credential[connection]
        except KeyError:
            raise Exception(
                "Connection " + connection + " not found in the file " + GlobalCalling.looq.connection_file)

        return connection_credential

    def _call_query_executor(self, start_time, query_mode="single"):
        try:
            self._get_query_result()
            total_sql_time = datetime.datetime.now() - start_time
            GlobalCalling.log_query({"connection": self.connection_alias, "query": self.query,
                                     "time": str(total_sql_time), "success": True, "mode": query_mode})
            self._update_response_timeout(total_sql_time)

        except Exception as execution_error:

            total_sql_time = datetime.datetime.now() - start_time
            GlobalCalling.log_query({"connection": self.connection_alias, "query": self.query,
                                     "time": str(total_sql_time), "success": False, "mode": query_mode})
            raise execution_error

    def _get_query_result(self):
        database_connection = self.connection_object[self.database]
        collection = database_connection[(self.query.get("collection"))]
        query_result = collection.find(self.query.get("query"), self.query.get("fields"))

        self.retrieved_data = pd.DataFrame(query_result)
        self.query_metadata = dict(self.retrieved_data.dtypes)

    def _generate_cache_file_name(self) -> str:
        """
        Cache file name is created by encrypt the sql script into a MD5
        string, thus avoiding duplicated names.
        """

        from hashlib import md5
        
        file_name = self.connection_alias + self._convert_query_to_string()
        hashed_file_name = md5(file_name.encode())
        return str(hashed_file_name.hexdigest()) + ".rds"

    def _convert_query_to_string(self) -> str:
        query_as_string = ""
        keys = list(self.query.keys())
        values = list(self.query.values())
        for i in range(len(keys)):
            query_as_string += str(keys[i]) + " " + str(values[i]) + ";"
            query_as_string += " "

        # Removed addition blank space at the end
        query_as_string = query_as_string[:-1]

        # since the character { and } could mess up the md5 conversion between R and Python
        # theses must be removed from the string
        query_as_string = query_as_string.replace("{", "").replace("}", "")
        return query_as_string

    def close_connection(self):
        self.connection_object.close()
