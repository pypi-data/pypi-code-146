from tempfile import NamedTemporaryFile
from typing import Union

import requests
from requests import Response

from compredict.exceptions import ClientError, ServerError
from compredict.exceptions import Error
from compredict.utils.utils import extract_error_message


class Connection:

    def __init__(self, url, token=None):
        """
        Class response for HTTP requests and communication.

        :param url: The base url string
        :param token: The API authorization token.
        """
        self.url = url
        self.last_error = False
        self.fail_on_error = False
        self.ssl = True
        self.response = None
        self.headers = dict(Accept='application/json')
        self.last_request = None
        if token is not None:
            self.headers['Authorization'] = 'Bearer ' + token

    def set_token(self, token):
        """
        Set the token for authorization.

        :param token: String API Key
        :return: None
        """
        self.headers['Authorization'] = 'Bearer ' + token

    def POST(self, endpoint, data, files=None):
        """
        Responsible for sending POST request and uploading files if specified.

        :param endpoint: the endpoint of the URL.
        :param data: The form data to be sent.
        :param files: The files to be sent.
        :return: JSON if request is correct otherwise false.
        """
        address = self.url + endpoint
        if files is not None:
            if 'Content-Type' in self.headers:
                del self.headers['Content-Type']
        else:
            self.headers['Content-Type'] = 'application/json'
        self.last_request = requests.post(address, files=files, data=data, headers=self.headers, verify=self.ssl)
        return self.handle_response(self.last_request, self.fail_on_error)

    def GET(self, endpoint):
        """
        Responsible for sending GET requests.

        :param endpoint: the targeted endpoint.
        :return: JSON if request is correct otherwise false.
        """
        address = self.url + endpoint
        self.headers['Content-Type'] = 'application/json'
        self.last_request = requests.get(address, None, headers=self.headers, verify=self.ssl)
        return self.handle_response(self.last_request, self.fail_on_error)

    def DELETE(self, endpoint):
        """
        Responsible for canceling the job.

        :param endpoint: targeted delete endpoint
        :return: JSON with task instance otherwise
        """
        address = self.url + endpoint
        self.headers['Content-Type'] = 'application/json'
        self.last_request = requests.delete(address, None, headers=self.headers, verify=self.ssl)
        return self.handle_response(self.last_request, self.fail_on_error)

    def handle_response(self, response: Response, fail_on_error: bool) -> Union[dict, bool]:
        """
        Handles responses based on the status code. In addition it raises exception if fail_on_error is True.

        :param response: response from AI Core API
        :param fail_on_error: indicated whether errors should be raised or not
        :return: JSON if request is correct otherwise false
        """

        if 400 <= response.status_code <= 499:
            if fail_on_error:
                raise ClientError(response.json())
            else:
                error = Error(response.json(), response.status_code)
                self.last_error = error
                return False

        elif 500 <= response.status_code <= 599:
            try:
                err_msg = response.json()
                is_json = True
            except ValueError:
                err_msg = extract_error_message(response.text) if response.text else "Internal Server Error"
                is_json = False

            if fail_on_error:
                raise ServerError(f"{response.status_code}: {err_msg}")
            else:
                error = Error(err_msg, status_code=response.status_code, is_json=is_json)
                self.last_error = error
                return False

        if '/template' in response.url or '/graph' in response.url:
            ext = '.png' if response.headers['Content-Type'] == 'image/png' else '.json'
            response = NamedTemporaryFile(suffix=ext)
            response.write(response.content)
            response.seek(0)
        else:
            response = response.json()

        return response
