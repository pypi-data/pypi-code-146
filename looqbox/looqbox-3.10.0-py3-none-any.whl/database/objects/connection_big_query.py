from looqbox.database.database_exceptions import TimeOutException, alarm_handler
from looqbox.database.objects.connection_base import BaseConnection
from looqbox.global_calling import GlobalCalling
from google.oauth2 import service_account
from google.cloud import bigquery
from platform import system
from multimethod import multimethod
import pandas as pd
import json
import datetime
import signal
import os


class BigQueryConnection(BaseConnection):
    def __init__(self, connection_name: str, **additional_args):
        super().__init__()
        self.connection_alias = connection_name
        self.connection_object = dict()
        self.response_timeout = GlobalCalling.looq.response_timeout if not self.test_mode else 0
        self.eval_limit = 10

    def set_query_script(self, sql_script: str) -> None:
        self.query = sql_script

    def connect(self):
        self.connection_object = self._get_connection_credentials(self.connection_alias)

    def _get_connection_credentials(self, connection: str, parameter_as_json=False) -> dict:
        """
        Get credentials for a list of connections.

        :param connection: String of database names
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

    def _execute_query(self, bq_client):
        bq_response = bq_client._connection.api_request(
            "POST",
            f"/projects/{bq_client.project}/queries",
            data={"query": self.query, "useLegacySql": False}
        )

        job_complete = bq_response.get("jobComplete", False)
        job_id = bq_response.get("jobReference", {}).get("jobId")
        page_token = bq_response.get("pageToken")
        if not job_complete:
            bq_response = self._wait_for_job_to_complete(bq_client, job_id)

        while page_token is not None:
            rows = bq_response.get("rows", [])

            page_response = self._get_response_by_job_id(bq_client, job_id, {"pageToken": page_token})
            page_rows = page_response.get("rows", [])
            rows.extend(page_rows)
            bq_response["rows"] = rows

            page_token = page_response.get("pageToken")

        return bq_response

    def _wait_for_job_to_complete(self, bq_client, job_id):
        bq_response = self._get_response_by_job_id(bq_client, job_id)
        job_complete = bq_response.get("jobComplete", False)
        eval_ = 0
        while not job_complete and eval_ <= self.eval_limit:
            bq_response = self._get_response_by_job_id(bq_client, job_id)
            job_complete = bq_response.get("jobComplete", False)
            eval_ += 1

        if not job_complete:
            raise Exception("Job did not complete in time")

        return bq_response

    @staticmethod
    def _get_response_by_job_id(bq_client, job_id, query_params=None):
        bq_response = bq_client._connection.api_request(
            "GET",
            f"/projects/{bq_client.project}/queries/{job_id}",
            query_params=query_params
        )
        return bq_response

    def _build_dataframe_from_response(self, response):
        fields = response.get("schema").get("fields")
        rows = response.get("rows") or []
        column_names = [field.get("name") for field in fields]
        column_types = [field.get("type") for field in fields]
        type_dict = dict(zip(column_names, column_types))
        row_list = [row.get("f") for row in rows]
        raw_data_frame = pd.DataFrame(data=row_list, columns=column_names)
        data_frame = raw_data_frame.applymap(lambda cell: cell.get("v"))
        self._convert_columns_type(data_frame, type_dict)
        return data_frame

    def _get_query_result(self):
        big_query_key = json.loads(self.connection_object.get("apiKey"))
        bq_client = self._connect_to_client(big_query_key)
        bq_response = self._execute_query(bq_client)

        self.retrieved_data = self._build_dataframe_from_response(bq_response)
        self.query_metadata = self.get_table_metadata_from_request(bq_response)

    @staticmethod
    def _connect_to_client(big_query_key):
        credentials = service_account.Credentials.from_service_account_info(big_query_key)
        client = bigquery.Client(
            credentials=credentials,
            project=credentials.project_id
        )
        return client

    @staticmethod
    def _convert_columns_type(data_frame, types):
        type_function_map = {
            "NUMERIC": "float",
            "BIGNUMERIC": "float",
            "FLOAT": "float",
            "INTEGER": "int"
        }
        for column, data_type in types.items():
            if type_function_map.get(data_type):
                astype_type = type_function_map[data_type]
                if astype_type == "int":
                    data_frame[column] = data_frame[column].astype("int", errors="ignore")
                    if data_frame[column].dtype != astype_type:
                        data_frame[column] = data_frame[column].astype("float")
                data_frame[column] = data_frame[column].astype(astype_type, errors="ignore")

    @staticmethod
    def get_table_metadata_from_request( request: dict) -> dict:
        metadata = dict()
        for column in request.get("schema").get("fields"):
            column_type = column.get("type")
            metadata[column.get("name")] = {
                "type": column_type
            }

        return metadata

    def _generate_cache_file_name(self) -> str:
        """
        Cache file name is created by encrypt the sql script into a MD5
        string, thus avoiding duplicated names.
        """
        from hashlib import md5

        file_name = self.connection_alias + self.query
        hashed_file_name = md5(file_name.encode())
        return str(hashed_file_name.hexdigest()) + ".rds"

    def close_connection(self):
        # Since Big Query uses API to get data, no close_connection method is needed
        pass
