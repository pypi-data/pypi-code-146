"""
    CUSTOM FALCON READER CLASSES
"""
# pylint: disable=too-few-public-methods,import-error,unused-import,too-many-locals
import os
from typing import Generator, List
from datetime import datetime, timedelta

import requests

from sdc_dp_helpers.api_utilities.date_managers import date_range_iterator
from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.api_utilities.retry_managers import request_handler, retry_handler


class CustomFalconReader:
    """
    Custom Falcon Reader
    """

    def __init__(self, creds_file: str, config_file=None):
        """creds_file has crecdentials config_file has api pull configs"""
        self._creds: dict = load_file(creds_file, "yml")
        self._config: dict = load_file(config_file, "yml")
        self.request_session: requests.Session = requests.Session()
        self.base_url: str = "https://api.falcon.io/"
        self.steps = 50
        self.start = 0
        self.curr_channel_ids = []

    @retry_handler(exceptions=ConnectionError, total_tries=5)
    def _get_channel_ids(self) -> List[str]:
        """
        Gather all available channel ids.
        """
        print("GET: channel ids.")
        endpoint_url = f"channels?apikey={self._creds['api_key']}"
        url = f"https://api.falcon.io/{endpoint_url}"
        response = self.request_session.get(url=url, params={"limit": "9999"})

        response_data = response.json()
        if response.status_code == 200:
            channel_ids = set()
            for item in response_data.get("items", []):
                channel_ids.add(item["id"])

            return list(channel_ids)

        raise ConnectionError(
            f"Falcon API failed to return channel ids. "
            f"Status code: {response.status_code}, Reason: {response.reason}."
        )

    @request_handler(
        wait=int(os.environ.get("REQUEST_WAIT_TIME", 2)),
        backoff_factor=float(os.environ.get("REQUEST_BACKOFF_FACTOR", 0.01)),
        backoff_method=os.environ.get("REQUEST_BACKOFF_METHOD", 0.01),
    )
    @retry_handler(exceptions=TimeoutError, total_tries=5, initial_wait=900)
    @retry_handler(exceptions=ConnectionError, total_tries=5, initial_wait=900)
    def _content_metrics_by_channel_id(
                        self, start_date: str, end_date: str, channel_ids: list
    ) -> list:
        """Gets the content metrics by channel id
        SEE: https://falconio.docs.apiary.io/ \
        #reference/channel-api/get-facebook-and-instagram-page-insights-metrics\
        # /get-content-metrics-by-channel-ids
        :param: channel_id - integer
        :param: date - string pushed as '2022-07-20'
        :returns: list of dictionaries
        """
        dataset: list = []
        endpoint_url: str = (
            f"measure/api/v1/content/metrics?apikey={self._creds['api_key']}"
        )
        offset: int = 0
        limit = self._config.get("limit", 9999)
        while True:
            print(
                f"INFO: channel id index: {self.start}, channel ids: "
                f"{len(channel_ids)}, date: {start_date}, offset: {offset}."
            )
            end_date = datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=1)
            end_date = datetime.strftime(end_date, "%Y-%m-%d")
            response = self.request_session.post(
                url=f"{self.base_url}{endpoint_url}",
                headers={"Content-Type": "application/json"},
                json={
                    "metrics": self._config.get("metrics", []),
                    "channels": channel_ids,
                    "since": start_date,
                    "until": end_date,
                    "postsSince": start_date,
                    "postsUntil": end_date,
                    "direction": self._config.get("direction", "ASC"),
                    "limit": limit,
                    "offset": offset,
                },
            )
            status_code: int = response.status_code
            reason: str = response.reason
            if status_code == 200:
                results: list = response.json()
                result_count: int = len(results)

                if result_count == 0:
                    break  # we will exit the loop because no data is got back

                if result_count < limit:
                    offset += result_count
                else:
                    offset += limit

                dataset.extend(results)
            elif status_code == 414 and "Request-URI Too Long" in reason:
                self.steps = self.steps - 20
                self.curr_channel_ids = self.curr_channel_ids[self.start : self.steps]
                print(f"len of channel_ids {len(channel_ids)}")
                raise TimeoutError(
                    "Request-URI Too Long. Reducing number of channel_ids by 20"
                )
            elif reason == "Not Found" and status_code == 404:
                print(f"No data for channel ids: {channel_ids}, skipping.\n")
                break
            elif status_code == 429:
                raise TimeoutError("Rolling Window Quota [429] reached.")
            else:
                raise ConnectionError(f"Reason: {reason}, Status: {status_code}.")

        return dataset

    @request_handler(
        wait=int(os.environ.get("REQUEST_WAIT_TIME", 2)),
        backoff_factor=float(os.environ.get("REQUEST_BACKOFF_FACTOR", 0.01)),
        backoff_method=os.environ.get("REQUEST_BACKOFF_METHOD", 0.01),
    )
    @retry_handler(exceptions=TimeoutError, total_tries=5, initial_wait=900)
    @retry_handler(exceptions=ConnectionError, total_tries=5, initial_wait=900)
    def _published_posts_by_channel_id(
                        self, start_date: str, end_date: str, channel_ids: list
    ) -> list:
        """Gets the published posts by channel id
        SEE: https://falconio.docs.apiary.io/
        #reference/content-api/get-content-metrics-by-channel-ids
        :param: channel_id - integer
        :param: date - string '2022-07-20' but converted to isoformat '2022-07-20T00:00:00'
        :returns: list of dictionaries
        """

        dataset: list = []
        endpoint_url: str = f"publish/items?apikey={self._creds['api_key']}"
        limit = self._config.get("limit", 2000)
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        start_date = datetime.strftime(start_date, "%Y-%m-%dT%H:%M:%SZ")
        end_date = datetime.strftime(end_date, "%Y-%m-%dT%H:%M:%SZ")
        while endpoint_url:
            print(
                f"INFO: channel id index: {self.start}, "
                f"channel id: {channel_ids},  date: {start_date}, offset: {len(dataset)}."
            )
            response = self.request_session.get(
                url=f"{self.base_url}{endpoint_url}",
                headers={"Content-Type": "application/json"},
                params={
                    "channels": channel_ids,
                    "since": start_date,
                    "until": end_date,
                    "networks": self._config["networks"],
                    "statuses": self._config.get("statuses", "published"),
                    "limit": limit,
                },
            )
            status_code: int = response.status_code
            reason: str = response.reason
            if response.status_code == 200:
                results: dict = response.json()
                items_data: list = results.get("items", [])
                dataset.extend(items_data)

                endpoint_url = results.get("next", {"href": None}).get("href")

                if len(items_data) == 0 or endpoint_url is None:
                    break

            elif reason == "Not Found" and status_code == 404:
                print(f"No data for channel id: {channel_ids}, skipping.\n")
                break
            elif status_code == 429:
                raise TimeoutError("Rolling Window Quota [429] reached.")
            else:
                raise ConnectionError(f"Reason: {reason}, Status: {status_code}.")

        return dataset

    def _query_handler(self, start_date: str, end_date: str, channel_ids: list) -> list:
        """Interface to decide the api call to make"""
        endpoint_name = self._config.get("endpoint_name", None)
        self.start = 0
        dataset = []
        if not endpoint_name:
            raise KeyError(
                "Please specify endpoint in the configs i.e content_metrics or published_posts"
            )
        if endpoint_name == "content_metrics":
            channel_len = len(channel_ids)
            for _ in range(0, channel_len, self.steps):
                self.curr_channel_ids = channel_ids[
                    self.start : self.start + self.steps
                ]
                results = self._content_metrics_by_channel_id(
                    start_date, end_date, self.curr_channel_ids
                )
                dataset.extend(results)
                self.start += self.steps
        elif endpoint_name == "published_posts":
            for channel_id in channel_ids:
                self.curr_channel_ids = [channel_id]
                results = self._published_posts_by_channel_id(
                    start_date, end_date, [channel_id]
                )
                dataset.extend(results)
                self.start += 1
        else:
            raise ValueError(f"Invalid endpoint_name {endpoint_name}")

        return dataset

    def run_query(self) -> Generator[dict, None, None]:
        """
        Get metrics by channel Id context returns a request session with the ability
        to page with offsets.
        Content (or Post level) contains all metrics about your specific piece of
        content (posts). Here you will find impressions, reach, likes,
        shares and other metrics that show how well your specific post has performed.
        https://falconio.docs.apiary.io/reference/content-api/get-copied-content.
        """
        channel_ids: list = self._get_channel_ids()[:100]
        # channel_ids = ["114215121990330", "58283981268"]
        print(f"Attempting to gather metrics from {len(channel_ids)} channel ids.")
        date_iterator = date_range_iterator(
            start_date=self._config["since"],
            end_date=self._config["until"],
            interval="1_day",
            end_inclusive=False,
            time_format="%Y-%m-%d",
        )
        for start_date, end_date in date_iterator:
            payload: list = []
            payload = self._query_handler(
                start_date=start_date, end_date=end_date, channel_ids=channel_ids
            )
            if len(payload) > 0:
                yield {
                    "networks": self._config["networks"],
                    "date": start_date,
                    "data": payload,
                }
                self.start = 0
            else:
                print(
                    f"No data for endpoint {self._config['endpoint_name']} for date : {start_date}"
                )


class CustomFalconReaderV2:
    """
    Custom Falcon Reader for Content Insights
    """

    def __init__(self, creds_file: str, config_file=None):
        """creds_file has crecdentials config_file has api pull configs"""
        self._creds: dict = load_file(creds_file, "yml")
        self._config: dict = load_file(config_file, "yml")
        self.request_session: requests.Session = requests.Session()
        self.base_url: str = "https://api.falcon.io/"
        self.success = []
        self.start = 0
        self.curr_channels = []

    def is_success(self):
        """Append True to Success List for successfull API pull"""
        self.success.append(True)

    def not_success(self):
        """Append False for failed API pull"""
        self.success.append(False)

    def _get_channel_ids(self) -> dict:
        """
        Gather all available channel ids.
        """
        print("GET: channel ids.")
        endpoint_url = f"channels?apikey={self._creds['api_key']}"
        url = f"{self.base_url}{endpoint_url}"
        response = self.request_session.get(url=url, params={"limit": "9999"})

        response_data = response.json()
        if response.status_code == 200:
            channel_ids = {}
            for item in response_data.get("items", []):
                channel_ids[item["uuid"]] = item["name"]
            return channel_ids

        raise ConnectionError(
            f"Falcon API failed to return channel ids. "
            f"Status code: {response.status_code}, Reason: {response.reason}."
        )

    @retry_handler(exceptions=ConnectionError, total_tries=5, initial_wait=5)
    def _get_content_ids_by_channel_id(
                        self, start_date: str, end_date: str, network: str, channel_ids: List[str]
    ) -> dict:
        """Retrieves all social media published
        SEE: https://falconio.docs.apiary.io/
        #reference/content-api/get-channel-content
        :param: date - string '2022-07-20' but converted to isoformat '2022-07-20T00:00:00Z'
        :returns: list of dictionaries
        """
        print("GET: content ids by channel id.")
        date_filters = f"since={start_date}&until={end_date}"
        endpoint_url = (
            f"publish/items?apikey={self._creds['api_key']}"
            f"&statuses=published"
            f"&networks={network}"
            f"&{date_filters}"
        )
        content_ids_by_channel_id = {}
        while endpoint_url is not None:
            url = f"{self.base_url}{endpoint_url}"
            response = self.request_session.get(url=url, params={"limit": "9999"})
            response_data = response.json()
            if response.status_code != 200:
                raise ConnectionError(
                    f"Falcon API failed to return content ids. "
                    f"Status code: {response.status_code}, Reason: {response.reason}."
                )
            for item in response_data.get("items"):
                content_id = item.get("id")
                channel_id = item.get("channels")
                if channel_id is not None and channel_id[0] in channel_ids:
                    content_ids_by_channel_id.setdefault(channel_id[0], []).append(
                        content_id
                    )
            endpoint_url = response_data.get("next", {"href": None}).get("href")
        return content_ids_by_channel_id

    def _get_insights_request_id(
                        self, start_date: str, end_date: str, content_ids_by_channel_id: dict
    ) -> dict:
        """Get Insights request id
        channels per request : max 15
        time between since and until : max 3 months
        metricids per request : max 20
        contentids per request: max 300
        SEE: https://falconio.docs.apiary.io/
        #reference/measure-api-v2/request-content-insights
        :param: date - string '2022-07-20' but converted to isoformat '2022-07-20T00:00:00'
        :returns: dictionary
        """
        print("GET: insights request id.")
        endpoint_url = f"measure/v2/insights/content?apikey={self._creds['api_key']}"
        url = f"{self.base_url}{endpoint_url}"
        body = {
            "since": start_date,
            "until": end_date,
            "metricIds": self._config["metrics"],
            "channels": [],
        }

        for key, value in content_ids_by_channel_id.items():
            body["channels"].append({"id": key, "contentIds": value})
        response = self.request_session.post(
            url=url, headers={"Content-Type": "application/json"}, json=body
        )
        if response.status_code == 200:
            response_data = response.json()
            insights_request_id = response_data["insightsRequestId"]
            return insights_request_id

        raise ConnectionError(
            f"Falcon API failed to return content ids. "
            f"Status code: {response.status_code}, Reason: {response.reason}."
        )

    @retry_handler(exceptions=ConnectionError, total_tries=5, initial_wait=5)
    def _get_content_insights(self, insights_request_id: str):
        """Get Insights
        It is recommended to wait 3 seconds and then check for the availability
        of the data. If the request is still in progress then check every
        3 seconds.
        SEE: https://falconio.docs.apiary.io/
        #reference/measure-api-v2/request-content-insights
        :param: date - string '2022-07-20' but converted to isoformat '2022-07-20T00:00:00'
        :returns: dictionary
        """
        print("GET: content insights.")
        endpoint_url = (
            f"measure/v2/insights/{insights_request_id}?apikey={self._creds['api_key']}"
        )
        url = f"{self.base_url}{endpoint_url}"
        response = self.request_session.get(url=url)

        response_data = response.json()
        if response.status_code == 200:
            if response_data["status"] == "READY":
                return response_data
            if response_data["status"] == "EXPIRED":
                return None
        raise ConnectionError(
            f"Falcon API failed to return content ids. "
            f"Status code: {response.status_code}, Reason: {response.reason}."
        )

    @staticmethod
    def _normalize_data(dataset: dict, network: str, channel_ids: dict):
        normalized_data = []
        for metric, data_items in dataset.items():
            for data_item in data_items:
                data_item[f"{metric}"] = data_item.pop("value")
                data_item["network"] = network
                data_item["brand"] = channel_ids.get(data_item["channelId"], None)
                normalized_data.append(data_item)
        return normalized_data

    def _query_handler(
                        self, start_date: str, end_date: str, network: str, channel_ids: dict
    ) -> dict:
        endpoint_name = self._config.get("endpoint_name", None)
        if not endpoint_name:
            raise KeyError(
                "Please specify endpoint in the configs i.e content_insights"
            )
        content_ids_by_channel_id = self._get_content_ids_by_channel_id(
            start_date=start_date,
            end_date=end_date,
            network=network,
            channel_ids=channel_ids,
        )
        channels = list(content_ids_by_channel_id.keys())
        channel_id_length = len(channels)
        channel_steps = self._config.get("channel_steps", 10)
        dataset = {}
        data = []
        for _ in range(0, channel_id_length, channel_steps):
            self.curr_channels = channels[self.start : self.start + channel_steps]
            request_content_ids_by_channel_id = {
                key: value
                for key, value in content_ids_by_channel_id.items()
                if key in self.curr_channels
            }

            if len(request_content_ids_by_channel_id) > 0:
                insights_request_id = self._get_insights_request_id(
                    start_date=start_date,
                    end_date=end_date,
                    content_ids_by_channel_id=request_content_ids_by_channel_id,
                )
                results = self._get_content_insights(insights_request_id)
                if results is None:
                    insights_request_id = self._get_insights_request_id(
                        start_date=start_date,
                        end_date=end_date,
                        content_ids_by_channel_id=request_content_ids_by_channel_id,
                    )
                    results = self._get_content_insights(insights_request_id)
                data = results["data"]["insights"]
            dataset.update(data)
            self.start = self.start + channel_steps
        return self._normalize_data(dataset, network, channel_ids)

    def run_query(self):
        """Handles the query results"""
        channel_ids = self._get_channel_ids()
        print(f"Attempting to gather metrics from {len(channel_ids)} channel ids.")
        network = self._config.get("networks")
        date_iterator = date_range_iterator(
            start_date=self._config["since"],
            end_date=self._config["until"],
            interval="1_day",
            end_inclusive=False,
            time_format="%Y-%m-%dT%H:%M:%SZ",
        )
        for start_date, end_date in date_iterator:
            payload: list = []
            payload = self._query_handler(
                start_date=start_date,
                end_date=end_date,
                network=network,
                channel_ids=channel_ids,
            )
            date = start_date[:-10]
            if len(payload) > 0:
                yield {
                    "networks": network,
                    "date": date,
                    "data": payload,
                }
                self.start = 0
                self.is_success()
            else:
                self.not_success()
                print(
                    f"No data for endpoint {self._config['endpoint_name']} for date : {date}"
                )
