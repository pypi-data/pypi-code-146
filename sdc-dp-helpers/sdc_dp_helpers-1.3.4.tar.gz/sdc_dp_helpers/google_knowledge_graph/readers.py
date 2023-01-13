"""
    CUSTOM READER CLASSES
        - Class which manages writer tasks like
        auth, write metadata, write file, create dir structure
"""
# pylint: disable=inconsistent-return-statements
import os
from datetime import datetime
import requests
from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.api_utilities.data_managers import multiple_regex_replace
from sdc_dp_helpers.api_utilities.retry_managers import retry_handler, request_handler


class GoogleKnowledgeGraphReader:
    """Google Knowledge Graph Class"""

    def __init__(self, secrets_filepath: str, config_filepath: str):
        self.secrets: dict = load_file(secrets_filepath)
        self.config: dict = load_file(config_filepath)
        self.request_session: requests.Session = requests.Session()
        self.dataset: list = []
        self.success = []

    def is_success(self):
        """Append True to Success List for successfull API pull"""
        self.success.append(True)

    def not_success(self):
        """Append False for failed API pull"""
        self.success.append(False)

    def query_partition(self, query: str, language: str = None) -> str:
        """Helper to get the query partition string
        :query: "string",
        :language:"string"}
        :returns: query_partition - str
        """
        query = query.strip()
        query_partition = multiple_regex_replace(
            query, {".": "_dot_", " ": "_space_", "+": "_plus_"}
        )
        if language:
            query_partition = f"{query_partition}_lang_{language}"

        return query_partition

    @request_handler(
        wait=int(os.environ.get("REQUEST_WAIT_TIME", 2)),
        backoff_factor=float(os.environ.get("REQUEST_BACKOFF_FACTOR", 0.01)),
        backoff_method=os.environ.get("REQUEST_BACKOFF_METHOD", "0.01"),
    )
    @retry_handler(
        exceptions=ConnectionError,
        total_tries=int(os.environ.get("TOTAL_RETRIES", 5)),
        initial_wait=float(os.environ.get("INITIAL_WAIT", 200)),
    )
    def _query_handler(self, query: str, language: str) -> dict:
        """Does the actual API call"""
        response_json: dict = {}
        if self.secrets.get("api_key") is None:
            raise KeyError("api_key missing in your secrets file")

        base_url = "https://kgsearch.googleapis.com/v1/entities:search"
        try:
            response = self.request_session.get(
                url=base_url,
                params={
                    "query": query,
                    "limit": self.config.get("limit", 1),
                    "indent": self.config.get("indent", True),
                    "key": self.secrets["api_key"],
                    "languages": language,
                },
            )
            status_code = response.status_code
            reason = response.reason
            if status_code in [404, 500, 202]:
                raise ConnectionError(
                    f"Google Knowledge Graph API failed. "
                    f"Status code: {status_code}, Reason: {reason}."
                )
            if status_code == 200:
                response_json = response.json()
            return response_json
        except Exception as err:
            raise Exception(f"Unexpected error: {err}") from err

    def run_query(self):
        """Handles the query results"""
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        results = []
        for query, languages in self.config["queries"].items():
            for language in languages:
                payload: dict = self._query_handler(query, language)
                if payload:
                    # add metadata of date, query and language
                    query_partition: str = self.query_partition(query, language)
                    payload.update(
                        {
                            "date": date,
                            "query": query,
                            "language": language,
                            "query_partition": query_partition,
                        }
                    )
                    results.append(payload)
                    self.is_success()
                    print(
                        f"Got data for query:'{query}' language:'{language}' on '{date}'"
                    )
                if not payload:
                    self.not_success()
                    print(
                        f"No data for query:'{query}' language:'{language}' on '{date}'"
                    )
        # only return if we have daa in the results list
        if results:
            return {"date": date, "data": results}
        self.dataset = results
        return
