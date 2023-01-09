import requests
import json
from typing import Union
from arinrest.common import exceptions


class ArinRestConnection:
    def __init__(
        self,
        service: Union[str, None],
        api_key: Union[str, None],
        dev: bool = False,
        use_ssl: bool = True,
        verify_ssl: bool = True,
    ) -> None:

        if service == "rpki" or service == "irr":
            service = "reg"

        self.host = "{}.arin.net".format(service)
        ## if dev switch to the OT&E environment
        if dev:
            self.host = "{}.ote.arin.net".format(service)

        self.base_url = "https://{host}".format(
            host=self.host,
        )

        self.api_key = api_key
        self.session = requests.Session()

        if use_ssl and verify_ssl:
            self.session.verify = verify_ssl
        else:
            self.session.verify = False

        self.session.headers.update({"Accept": "application/xml"})
        self.session.headers.update({"Content-Type": "application/xml"})

        if service == "rdap":
            self.session.headers.update({"Accept": "application/json"})
            self.session.headers.update({"Content-Type": "application/json"})

    def __request(self, method: str, body: str = None, url: str = None):

        # add the api key as the final step to the url
        url = url + f"?apikey={self.api_key}"

        verbs = ["GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"]
        if method not in verbs:
            raise exceptions.BadHttpMethod(method)

        request = requests.Request(method=method, url=url)

        if method != "GET":
            if not self.api_key:
                raise exceptions.AuthException(
                    "Authentication credentials were not provided"
                )

            # GET requests usually dont have body content.

        prepared_request = self.session.prepare_request(request)
        if body:
            # preparedRequests have a prepare_body method.  This
            # just encodes the text to a binary using the encode
            # str method to utf-8
            prepared_request.prepare_body(data=body, files=None)

        try:
            response = self.session.send(prepared_request)
        except requests.exceptions.ConnectionError:
            err_msg = "Unable to connect to ARIN on host: {}".format(self.host)
            raise ConnectionError(err_msg) from None
        except requests.exceptions.Timeout:
            raise TimeoutError(
                "Connection to ARIN host, {}, timed out".format(self.host)
            ) from None
        except Exception as e:
            raise Exception(e)
        finally:
            self.close()

        # process all non 200 responses
        if not 200 <= response.status_code < 300:
            self.__raise_error(response.status_code, response.content)

        return response

    def get(self, url: str = None) -> str:
        """make http GET request"""
        url = self.base_url + url
        response = self.__request(method="GET", url=url)

        return response.text

    def put(self, url: str = None, body: dict = None):
        """make HTTP PUT request"""
        url = self.base_url + url
        response = self.__request(method="PUT", body=body, url=url)

        return response.text

    def post(self, url: str = None, body: dict = None):
        url = self.base_url + url
        response = self.__request(method="POST", body=body, url=url)
        return response.text

    def delete(self, url: str = None):
        response = self.__request("DELETE", url=url)
        if 200 <= response.status_code < 300:
            return True

    def close(self):
        self.session.close()

    def __raise_error(self, http_status_code, http_response):
        """Raise error with detailed information from http request."""
        try:
            error_msg = json.loads(http_response)
        except json.JSONDecodeError:
            error_msg = http_response

        if http_status_code == 404:
            raise exceptions.NotFoundException(error_msg)
        elif http_status_code == 403:
            raise exceptions.AuthorizationException(error_msg)
        elif http_status_code == 400:
            raise exceptions.ClientException(error_msg)
        elif http_status_code == 503:
            raise exceptions.ServerException(error_msg)
