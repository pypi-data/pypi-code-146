from .keapsession import KeapSession


class KeapRestClient(KeapSession):

    def __init__(self, app):
        KeapSession.__init__(self, app)

    def validate_auth(self):
        return self.is_authorized()

    def make_request(self, method, endpoint, data=None, json_data=None, **kwargs):
        if not self.is_authorized():
            raise KeapAuthError("Keap is not authorized.")

        url = f"{self.api_base_url}{endpoint}"
        attempts = 0
        while attempts < 3:
            if method == "get":
                response = self.request(method, url, params=kwargs)
            else:
                response = self.request(method, url, data=data, json_data=json_data)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 204 or 201:
                return True
            elif response.status_code == 401:
                self.refresh_session_auth()
                attempts += 1
            else:
                self.handle_keap_error(response)
                attempts = 3

    def _get(self, endpoint, data=None, **kwargs):
        return self.make_request('get', endpoint, data=data, **kwargs)

    def _post(self, endpoint, data=None, json_data=None, **kwargs):
        return self.make_request('post', endpoint, data=data, json_data=json_data, **kwargs)

    def _delete(self, endpoint, **kwargs):
        return self.make_request('delete', endpoint, **kwargs)

    def _patch(self, endpoint, data=None, json_data=None, **kwargs):
        return self.make_request('patch', endpoint, data=data, json_data=json_data, **kwargs)

    def _put(self, endpoint, json_data=None, **kwargs):
        return self.make_request('put', endpoint, json_data=json_data, **kwargs)

    @staticmethod
    def handle_keap_error(response):
        """
            This method get the response request and returns json_data data or raise exceptions
            :param response:
            :return:
        """
        if response.status_code == 400:
            raise KeapDataError(
                "The URL {0} retrieved an {1} error. "
                "Please check your request body and try again.\nRaw message: {2}".format(
                    response.url,
                    response.status_code,
                    response.text
                )
            )
        elif response.status_code == 401:

            raise KeapAuthError(
                "The URL {0} retrieved and {1} error. Please check your credentials, "
                "make sure you have permission to perform this action and try again.".format(
                    response.url,
                    response.status_code
                )
            )
        elif response.status_code == 403:
            raise KeapAuthError(
                "The URL {0} retrieved and {1} error. This action was forbidden.".format(
                    response.url,
                    response.status_code
                )
            )
        elif response.status_code == 404:
            raise ConnectionError(
                "The URL {0} retrieved an {1} error. Please check the URL and try again.\n"
                "Raw message: {2}".format(
                    response.url,
                    response.status_code,
                    response.text
                )
            )
        else:
            raise KeapException(
                "An Unknown Issue occurred"
            )


class KeapException(Exception):
    """Base exception for all library errors."""
    pass


class KeapAuthError(KeapException):
    """Something is wrong with authentication."""
    pass


class KeapTokenError(KeapAuthError):
    """Something is wrong with the tokens."""
    pass


class KeapDataError(KeapException, ValueError):
    """Something is wrong with the data."""
    pass


class KeapConnectionError(KeapException, ConnectionError):
    """Something is wrong with the connection."""
    pass
