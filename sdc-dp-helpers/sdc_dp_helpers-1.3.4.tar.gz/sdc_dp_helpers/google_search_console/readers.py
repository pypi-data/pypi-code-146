"""
    CUSTOM READERS MODULE FOR GOOGLE SEARCH CONSOLE
"""
# pylint: disable=no-member,too-many-locals,broad-except,too-few-public-methods,arguments-differ
from typing import Any, List, Dict, Union
from googleapiclient import discovery
from google.oauth2 import service_account

from sdc_dp_helpers.base_readers import BaseReader

from sdc_dp_helpers.api_utilities.date_managers import date_range_iterator
from sdc_dp_helpers.api_utilities.file_managers import load_file


class GoogleSearchConsoleReader(BaseReader):
    """
    Google Search Console Reader v1
    """

    def __init__(self, creds_filepath: str, config_filepath: str):
        self.secrets: Dict[Any, Any] = load_file(creds_filepath)
        self.config: Dict[Any, Any] = load_file(config_filepath)
        self.service = self._get_auth()

    def _get_auth(self):
        """
        Get our credentials initialised above and use those to get client

        """
        credentials = service_account.Credentials.from_service_account_info(
            info=self.secrets,
            scopes=["https://www.googleapis.com/auth/webmasters.readonly"],
        )
        service = discovery.build(
            serviceName="searchconsole", version="v1", credentials=credentials
        )
        return service

    def _normalize(
        self, response: Dict[Any, Any], query_dim_list: List[str]
    ) -> List[Dict[str, Any]]:
        """Method to normalize data into a flat structure and add metadata

        Args:
            response (Dict[Any, Any]): api response in dictionary format
            query_dim_list (List[str]): Zero or more dimensions to group results.

        Returns:
            Dict[str, Any]: flattened data dictionary
        """

        # added additional data that the api does not provide
        dataset_list: List[Dict[str, Any]] = []
        for _, row in enumerate(response["rows"]):
            row_dataset: Dict[str, Any] = {}
            row_dataset = {
                "site_url": self.config.get("site_url"),
                # keeping original search_type name for reporting
                "search_type": self.config.get("search_type"),
            }

            # get dimension data keys and values
            row_dataset.update(
                dict(
                    zip(
                        query_dim_list,
                        row.get("keys", []),
                    )
                )
            )

            # get metrics data
            for metric in self.config.get("metrics", []):
                row_dataset[metric] = row.get(metric)

            dataset_list.append(row_dataset)

        return dataset_list

    def _query_handler(
        self, start_date: str, end_date: str, start_row: int, query_dim_list: List[str]
    ) -> Union[Dict[Any, Any], None]:
        """Function to make api call

        Args:
            start_date (str): start of range inclusive 'YYYY-MM-DD'
            end_date (str): end of range inclusive 'YYYY-mm-dd'
            query_dim_list (List[str]): Zero or more dimensions to group results.

        Returns:
            Dict[Any, Any]: dictionary of response
        """
        response: Union[Dict[Any, Any], None] = None
        try:
            request = {
                "startDate": start_date,
                "endDate": end_date,
                "dimensions": query_dim_list,
                "metrics": self.config.get("metrics"),
                "searchType": self.config.get("search_type"),
                "rowLimit": self.config.get("row_limit", 25000),
                "startRow": start_row * self.config.get("row_limit", 25000),
                "aggregationType": self.config.get("aggregation_type", "auto"),
                "dimensionFilterGroups": self.config.get("dimension_filter_groups", []),
                "dataState": self.config.get("data_state", "final"),
            }
            response = (
                self.service.searchanalytics()
                .query(siteUrl=self.config.get("site_url"), body=request)
                .execute()
            )

        except Exception as err:
            # print(err)
            raise err

        return response

    def run_query(self):
        """Main Class Method"""
        # site_list = self.service.sites().list().execute()
        # print(site_list)

        for dimension in self.config["dimensions"]:
            for start_date, end_date in date_range_iterator(
                start_date=self.config["start_date"],
                end_date=self.config["end_date"],
                interval=self.config.get("interval", "day"),
                end_inclusive=True,
                time_format="%Y-%m-%d",
            ):
                dataset: List[Dict[str, Any]] = []
                query_dim_list: List[str] = list(dict.fromkeys(["date", dimension]))
                start_row: int = 0
                while True:
                    response = self._query_handler(
                        start_date=start_date,
                        end_date=end_date,
                        start_row=start_row,
                        query_dim_list=query_dim_list,
                    )

                    if response is None:
                        self.not_success()
                        print(
                            f"response is 'None' for date dimension row: "
                            f"'{start_date}' '{dimension}' '{start_row}'"
                        )
                        break
                    if "rows" not in response:
                        self.not_success()
                        print(
                            f"No more data for date dimension row: "
                            f"'{start_date}' '{dimension}' '{start_row}'"
                        )
                        break

                    self.is_success()
                    normalised_dataset = self._normalize(response, query_dim_list)
                    dataset.extend(normalised_dataset)
                    start_row += 1

                yield {
                    "date": start_date.replace("-", ""),
                    "dimension": dimension,
                    "data": dataset,
                }
