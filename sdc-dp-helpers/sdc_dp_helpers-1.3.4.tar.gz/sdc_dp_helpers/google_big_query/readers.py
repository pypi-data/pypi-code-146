# pylint: disable=no-member
import sys

from google.cloud import bigquery
from google.oauth2 import service_account

from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.api_utilities.date_managers import date_range


class CustomGBQReader:
    """
    Custom Google BigQuery Console Reader
    """

    def __init__(self, service_account_secrets_path=None, config_path=None):

        if service_account_secrets_path is not None:
            self.credentials = load_file(service_account_secrets_path, fmt="json")

        if config_path is not None:
            self.config = load_file(config_path, fmt="yml")

    def get_auth(self):
        """
        Get our credentials initialised above and use those to get client

        """
        credentials = service_account.Credentials.from_service_account_info(
            self.credentials
        )
        client = bigquery.Client(
            credentials=credentials,
            project=credentials.project_id,
        )
        return client

    def build_query(self, query, date_run):
        """Build up query """
        # initialization
        query = ""
        project_id: str = self.credentials["project_id"]
        table_id: str = self.credentials["table"]
        query_prefix = f"SELECT *, NULL FROM {project_id}.{table_id}.events_{date_run} "
        query_suffix = " WHERE app_info.firebase_app_id = @firebase_id "
        query = query_prefix + query_suffix
        return query

    def _query_handler(self, client, query, params=None):
        """Query handler for the dataset"""

        result = None
        if params is not None:
            job_config = bigquery.QueryJobConfig()
            job_config.query_parameters = params

            query_job = client.query(query, location="US", job_config=job_config)
        # no parameters justs a simple query
        else:
            query_job = client.query(query)
        try:
            result = query_job.result()
            return result
        except SyntaxError as err:
            if err.code == 400:
                print(f"Syntax error: {err}")
                sys.exit(1)
            else:
                print(f"Got unexpected error:\n {err}")
                sys.exit(1)

    def run_query(self):
        """
        Consumes a config file and loops through the dims
        to return relevant data from Google Big Query.
        """
        _query = None
        client = self.get_auth()

        start_date: str = self.config["start_date"]
        end_date: str = self.config["end_date"]

        print(f"Gathering data between given dates {start_date} and {end_date}. ")
        # split request by date to reduce 504 errors
        # BigQuery tables are named in format (project_id)_name_YYYYMMDD
        for firebase_id in self.config["firebase_ids"]:
            params = [
            bigquery.ScalarQueryParameter("firebase_id", "STRING", firebase_id),
            ]
            business = self.config["firebase_ids"][firebase_id]

            for date in date_range(start_date=start_date, end_date=end_date):
                current_date = date.replace("-", "")
                query = self.build_query(_query, current_date)

                print(f"Querying at date: {current_date}.")
                # run until none is returned or there is no more data in rows
                result = self._query_handler(client, query, params)
                result = [dict(row.items()) for row in result]

                yield {
                    "date": date,
                    "business" : business,
                    "data": result,
                }
