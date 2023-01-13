import random
from http import HTTPStatus
from io import IOBase, BytesIO
from time import sleep
from bson_extra import bson_extra

from pyqalx.core.encryption import QalxEncrypt

try:
    from json.decoder import JSONDecodeError
except ImportError:
    # JSONDecodeError is for Python3 only
    JSONDecodeError = ValueError

import requests


class PyQalxAPIException(Exception):
    """
    A generic error for PyQalxAPI
    """


class BasePyQalxAPI(object):
    """
    Core functionality for the transport layer.  Handles the building of the
    request and the response
    """

    def __init__(self, session):
        self.session = session
        self.config = self.session.config
        self.base_url = self.config.get("BASE_URL", "https://api.qalx.net/")
        self.__token = None
        self.token = self.config["TOKEN"]
        self._last_response = None
        self._host_ip = None

        # The maximum amount of retries for specific response status codes
        self._max_retries = {
            HTTPStatus.TOO_MANY_REQUESTS.value: {"retries": 0},
            HTTPStatus.INTERNAL_SERVER_ERROR.value: {
                "retries": 0,
                "max": self.config["MAX_RETRY_500"],
            },
        }

    def _should_retry(self, status_code):
        """
        Determines whether this request should be retried based on the
        status code and the number of times this request has already been tried
        :param status_code:The status code of the response
        :type status_code:int
        :return:bool of whether or not the request should be retried.
        """
        _too_many_requests = HTTPStatus.TOO_MANY_REQUESTS.value
        _internal_server_error = HTTPStatus.INTERNAL_SERVER_ERROR.value
        should_retry = False

        if status_code == _too_many_requests:
            # Throttled.  Always retry using a random expanding time window,
            # log a warning
            should_retry = True
            too_many_requests = self._max_retries[_too_many_requests]

            too_many_requests["retries"] += 1
            # Sleep for a random increasing window to allow the throttle to
            # expire
            sleep_for = too_many_requests["retries"] * random.randint(1, 5)

            self.session.log.warning(
                f"Got `{status_code}` response from API. Sleeping for "
                f"`{sleep_for}` seconds before trying again."
            )
            sleep(sleep_for)
        elif status_code >= _internal_server_error:
            # Error from API or requests exception.  Only try
            # up to the amount specified in the config
            internal_server_error = self._max_retries[_internal_server_error]
            if internal_server_error["retries"] < internal_server_error["max"]:
                should_retry = True
                internal_server_error["retries"] += 1
        return should_retry

    @property
    def token(self):
        """
        Returns the current API Token that is in use for this session

        :return: str
        """
        return self.__token

    @token.setter
    def token(self, token):
        """
        Setter for the token attribute.  Whenever a token is set the
        requests.Session object should be reinitialised to ensure that it
        has the correct token cached

        :param token: The token to use for authing all requests
        """
        self.__token = token
        self._initialise_session()

    def _initialise_session(self):
        """
        Initialises a new instance of `requests.Session` and sets the
        authentication headers.  This needs to happen post fork for Workers,
        due to multiprocessing issues - https://github.com/psf/requests/issues/4323
        """
        self._session = requests.Session()
        self._session.headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
        }

    def _build_request(self, url, method, include_auth_headers=True, **kwargs):
        """
        Handles making the request
        :param url: The url to make the request to
        :param include_auth_headers: Should we include the auth headers
        :param kwargs: kwargs to pass through to the request
        :return: response
        """
        headers = kwargs.pop("headers", {})
        if include_auth_headers is False:
            # We might not include the Authorization header if we are PUTing to S3
            headers.update({"Authorization": None})

        for k in self._max_retries.keys():
            # Reset all retries.
            self._max_retries[k]["retries"] = 0

        should_retry = True

        while should_retry:
            # There may be instances where the API returns a 500 error.  This
            # could be due to many things (network issues, cold starts etc).
            # To avoid terminating workers we retry up to `MAX_RETRIES` times
            # to make our best attempt at completing the request successfully.
            try:
                resp = self._session.request(
                    url=url, method=method, headers=headers, **kwargs
                )
                self._last_response = resp
                status_code = resp.status_code
            except requests.exceptions.RequestException as exc:
                # RequestException: The base exception that `requests` can
                #                   raise. Catch everything and return to the
                #                   client
                resp = exc
                status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
            # Check whether this request should be retried
            should_retry = self._should_retry(status_code)
        return self._build_response(resp)

    def _build_non_safe_request(self, method, endpoint, **kwargs):
        """
        Helper method for performing non safe requests (POST, PUT, PATCH etc).
        Handles the possibility of a user trying to create or update an item
        that also has a file
        :param method: The HTTP method
        :param endpoint: The endpoint you want to query: 'item`
        :param kwargs: Any data you want to pass to the request.
                      Use `json` key for data you want to post. Anything else
                      will be passed to `requests` as kwargs
                      json={'data': {'some': 'data'}, 'meta': {'some': 'meta'}}
        :return: response
        """
        url = self._get_url(endpoint)
        data = kwargs.get("data", None)

        if data:
            # data is dumped to json in a way that enables type to be preserved.
            # This means that we cannot use the `json` keyword argument so
            # have to pass the data using `data` and set the Content-Type of
            # the request to `application/json`
            data = bson_extra.dumps(data)
            if not isinstance(data, bytes):
                data = data.encode("utf-8")
            kwargs["data"] = data
        resp_ok, data = self._build_request(url=url, method=method, **kwargs)
        return resp_ok, data

    def _build_external_request(self, url, method, **kwargs):
        """
        Helper for building a request that is to an external source
        :param url: The URL to request
        :param method: The method to call
        :return: The response from `self._build_request`
        """
        return self._build_request(
            url=url, method=method, include_auth_headers=False, **kwargs
        )

    @staticmethod
    def _build_response(resp):
        """
        Builds the response that gets sent back to the client
        :param resp: The response from `requests` or an instance
                     of `RequestException`
        :return: tuple of `(response_ok:bool, response data:dict)`
        """
        # If it doesn't have `ok` then a `requests` exception was raised
        is_ok = getattr(resp, "ok", False)
        try:
            # Ensure that we load data to the correct type
            data = resp.json(**bson_extra._bson_loads_kwargs())
        except (AttributeError, JSONDecodeError):
            # AttributeError: `resp` is an instance of RequestException
            # JSONDecodeError: `resp` is a normal response but has no data.
            #                   i.e. a 500 or a `delete` response
            data = []
        if is_ok is False:
            # If either of these are missing then a `requests` exception was
            # raised
            status_code = getattr(resp, "status_code", "")
            reason = getattr(resp, "reason", resp)
            data = {
                "status_code": status_code,
                "reason": reason,
                "errors": data,
            }
        return is_ok, data

    def _get_url(self, endpoint):
        """
        Builds the URL for the request from the base_url and the endpoint
        :param endpoint: The endpoint you want to query: 'item/<item_guid>'
        :return: url
        """
        url = "{base_url}{endpoint}".format(
            base_url=self.base_url, endpoint=endpoint.rstrip("/").lstrip("/")
        )
        return url

    def _upload_to_s3(self, data, source, file_key):
        """
        Given a response object with a file url in will attempt to
        PUT the file onto S3

        :param data:        The data from the api
        :param source:  The path to the file to upload or the file itself
        :param file_key:    The file key in the data dictionary
        :return: response
        """
        url = data[file_key]["put_url"]

        if self.is_filestream(source):
            # seek(0) because the file could be at the end if it has already
            # been uploaded (i.e. if add_many uses the same file for
            # multiple entities)
            source.seek(0)
            file_data = source.read()
        else:
            file_data = open(source, "rb").read()
        # Check if we need to encrypt the file data
        if data[file_key].get("keyfile") is not None:
            key_file = self.config["KEYFILE"]
            qalx_encrypt = QalxEncrypt(key_file)
            token = qalx_encrypt.encrypt(bytes(file_data))
            file_data = BytesIO(token)
        return self._build_external_request(
            url=url, method="PUT", data=file_data
        )

    def _get_external_ip(self):
        """
        Gets the IP external address
        """
        if self._host_ip is None:
            # Get the external IP and cache it on the session
            success, ip = self._build_external_request(
                url="https://api.myip.com/", method="GET"
            )
            if success:
                self._host_ip = ip["ip"]
        return self._host_ip

    @staticmethod
    def is_filestream(input_object):
        """
        Determines whether the given input object is a file stream or a filepath

        :param input_object: An instance of IOBase or a filepath
        :type: io.IOBase or str
        :return: bool
        """
        return isinstance(input_object, IOBase)
