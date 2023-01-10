import requests
from datetime import datetime
from airflow_commons.internal.util.time_utils import get_interval_duration
from airflow_commons.internal.salesforce.auth import Connection
from airflow_commons.internal.salesforce.http_utils import (
    get_headers,
    get_async_operation_url,
    get_async_operation_result_url,
    get_async_operation_status_url,
    get_sync_operation_url,
    get_fetch_operation_url,
)

from airflow_commons.internal.salesforce.defaults import (
    TIMEOUT,
)

from airflow_commons.logger import get_logger


class SalesForceOperator(object):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        account_id: str,
        subdomain: str,
        scope: str = None,
        timeout: int = TIMEOUT,
    ):
        """
        Initializes SalesForceOperator instance with given parameters.
        If no scope is provided, connection starts with every operation available.

        :param client_id: Account client id string
        :param client_secret: Account client secret
        :param account_id: Account id
        :param subdomain: Account specific subdomain
        :param scope: Authorization scope, default value is None
        :param timeout: request timeout duration parameter
        """
        self.logger = get_logger("SalesForceOperator")
        self.connection = Connection(
            client_id=client_id,
            client_secret=client_secret,
            account_id=account_id,
            subdomain=subdomain,
            scope=scope,
        )
        self.session = requests.Session()
        self.timeout = timeout

    def async_upsert(self, key: str, data):
        """
        Starts an async upsert of given data to the data extension provided by key.
        :param key: External customer key of the data extension
        :param data: Data to be uploaded as json array
        :return:
        """
        return self._async_operation(key=key, data=data, method="PUT")

    def async_insert(self, key: str, data):
        """
        Starts an async insert of given data to the data extension provided by key.
        :param key: External customer key of the data extension
        :param data: Data to be uploaded as json array
        :return:
        """
        return self._async_operation(key=key, data=data, method="POST")

    def get_async_operation_result(self, request_id: str):
        """
        Returns result of an ongoing async process.
        :param request_id: ID of async request, can be found in the response of async request itself.
        :return:
        """
        url = get_async_operation_result_url(
            base_url=self.connection.rest_instance_url, request_id=request_id
        )
        request = requests.Request(
            method="GET",
            url=url,
            headers=get_headers(access_token=self.connection.access_token),
        )
        prep = request.prepare()
        return self.session.send(prep, timeout=self.timeout)

    def get_async_operation_status(self, request_id: str):
        """
        Returns current status of an ongoing async process.
        :param request_id: ID of async request, can be found in the response of async request itself.
        :return:
        """
        url = get_async_operation_status_url(
            base_url=self.connection.rest_instance_url, request_id=request_id
        )
        request = requests.Request(
            method="GET",
            url=url,
            headers=get_headers(access_token=self.connection.access_token),
        )
        prep = request.prepare()
        return self.session.send(prep, timeout=self.timeout)

    def _async_operation(self, key: str, data, method: str):
        """
        Internal method of async upsert and insert operations.
        :param key: External customer key of the data extension
        :param data: Data to be uploaded as json array
        :param method: HTTP method
        :return:
        """
        start = datetime.now()
        self.connection.check_and_refresh_token()
        url = get_async_operation_url(
            base_url=self.connection.rest_instance_url, key=key
        )
        request = requests.Request(
            method=method,
            url=url,
            json=data,
            headers=get_headers(access_token=self.connection.access_token),
        )
        prep = request.prepare()
        response = self.session.send(prep, timeout=self.timeout)
        try:
            response.raise_for_status()
            end = datetime.now()
            self.logger.info(
                f"Async operation finished in {get_interval_duration(start, end)} seconds"
            )
        except Exception as e:
            if response:
                self.logger.error(
                    "An error occurred during async operation, "
                    + str(e)
                    + ", response from Salesforce "
                    + response.text
                )
        return response

    def sync_upsert(self, key: str, data):
        """
        Sync upsert of given data to the data extension provided by key.
        :param key: External customer key of the data extension
        :param data: Data to be uploaded as json array
        :return:
        """
        start = datetime.now()
        self.connection.check_and_refresh_token()
        url = get_sync_operation_url(
            base_url=self.connection.rest_instance_url, key=key
        )
        request = requests.Request(
            method="POST",
            url=url,
            json=data,
            headers=get_headers(access_token=self.connection.access_token),
        )
        prep = request.prepare()
        response = self.session.send(prep, timeout=self.timeout)
        try:
            response.raise_for_status()
            end = datetime.now()
            self.logger.info(
                f"Sync operation finished in {get_interval_duration(start, end)} seconds"
            )
        except Exception as e:
            if response:
                self.logger.error(
                    "An error occurred during sync operation, "
                    + str(e)
                    + ", response from Salesforce "
                    + response.text
                )
        return response

    def sync_fetch(self, key: str, filter: str = None):
        """
        Sync upsert of given data to the data extension provided by key.
        :param key: External customer key of the data extension
        :param filter: Filter to apply to data extension search
        :return:
        """
        start = datetime.now()
        self.connection.check_and_refresh_token()
        url = get_fetch_operation_url(
            base_url=self.connection.rest_instance_url, key=key, filter=filter
        )
        request = requests.Request(
            method="GET",
            url=url,
            headers=get_headers(access_token=self.connection.access_token),
        )
        prep = request.prepare()
        response = self.session.send(prep, timeout=self.timeout)
        try:
            response.raise_for_status()
            end = datetime.now()
            self.logger.info(
                f"Sync operation finished in {get_interval_duration(start, end)} seconds"
            )
        except Exception as e:
            if response:
                self.logger.error(
                    "An error occurred during sync operation, "
                    + str(e)
                    + ", response from Salesforce "
                    + response.text
                )
        return response
