from abc import ABC
import base64
import http
import json
import logging
from typing import Optional, Union

from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import Parse
import grpc
from grpc_status.rpc_status import status_pb2
import requests

from truera.client.errors import NotFoundError
from truera.client.errors import SimpleException
from truera.client.errors import TruException
from truera.client.public.auth_details import AuthDetails
from truera.client.public.auth_details import AuthDetailsMode
from truera.protobuf.public.error_details_pb2 import \
    ErrorDetails  # pylint: disable=no-name-in-module

_KEY_GRPC_STATUS_CODE_HEADER = "grpc-status"
_KEY_GRPC_ERROR_MESSAGE_HEADER = "grpc-message"
_KEY_GRPC_ERROR_DETAILS_HEADER = "grpc-status-details-bin"

# source: https://grpc.github.io/grpc/core/md_doc_http-grpc-status-mapping.html
_default_http_code_to_grpc_status_map = {
    http.HTTPStatus.BAD_REQUEST: grpc.StatusCode.INTERNAL,
    http.HTTPStatus.UNAUTHORIZED: grpc.StatusCode.UNAUTHENTICATED,
    http.HTTPStatus.FORBIDDEN: grpc.StatusCode.PERMISSION_DENIED,
    http.HTTPStatus.NOT_FOUND: grpc.StatusCode.UNIMPLEMENTED,
    http.HTTPStatus.TOO_MANY_REQUESTS: grpc.StatusCode.UNAVAILABLE,
    http.HTTPStatus.BAD_GATEWAY: grpc.StatusCode.UNAVAILABLE,
    http.HTTPStatus.SERVICE_UNAVAILABLE: grpc.StatusCode.UNAVAILABLE,
    http.HTTPStatus.GATEWAY_TIMEOUT: grpc.StatusCode.UNAVAILABLE,
}

# source: https://grpc.github.io/grpc/core/md_doc_statuscodes.html
# NOTE: Directly using grpc.StatusCode does not align with the integers
_grpc_status_code_to_enum = {
    0: grpc.StatusCode.OK,
    1: grpc.StatusCode.CANCELLED,
    2: grpc.StatusCode.UNKNOWN,
    3: grpc.StatusCode.INVALID_ARGUMENT,
    4: grpc.StatusCode.DEADLINE_EXCEEDED,
    5: grpc.StatusCode.NOT_FOUND,
    6: grpc.StatusCode.ALREADY_EXISTS,
    7: grpc.StatusCode.PERMISSION_DENIED,
    8: grpc.StatusCode.RESOURCE_EXHAUSTED,
    9: grpc.StatusCode.FAILED_PRECONDITION,
    10: grpc.StatusCode.ABORTED,
    11: grpc.StatusCode.OUT_OF_RANGE,
    12: grpc.StatusCode.UNIMPLEMENTED,
    13: grpc.StatusCode.INTERNAL,
    14: grpc.StatusCode.UNAVAILABLE,
    15: grpc.StatusCode.DATA_LOSS,
    16: grpc.StatusCode.UNAUTHENTICATED
}


# TODO: AB#6715 Move some of this Error classes to truera.client.errors
class UnknownRpcError(SimpleException):
    pass


class AuthenticationFailedError(SimpleException):

    def __init__(
        self,
        details,
        *,
        auth_details: Optional[AuthDetails] = None,
        connection_string: Optional[str] = None
    ):
        error_msg = ""
        if auth_details and auth_details.mode == AuthDetailsMode.TOKEN_AUTH:
            ui = f"at {connection_string}" if connection_string else "in the TruEra UI"
            error_msg = f"Your token is invalid or expired. Visit personal settings {ui} to generate a new auth token."
        else:
            auth_details_msg = f"- {auth_details.redacted_print()} - " if auth_details else ""
            error_msg = f"Your credentials {auth_details_msg}are invalid or expired."
        details_msg = f" Details: {str(details)}" if details else ""
        error_msg = f"{error_msg}{details_msg}"
        self.message = error_msg
        super().__init__(self.message)


class UnauthorizedAccessError(SimpleException):

    def __init__(self, details):
        self.message = "The user is not authorized to perform the attempted action. Details: " + str(
            details
        )
        super().__init__(self.message)


class ConnectionFailedError(TruException):
    pass


class AlreadyExistsError(SimpleException):
    pass


class NotSupportedError(SimpleException):
    pass


class ModelRunnerError(TruException):

    def __init__(self, message: str, job_id: str):
        self.message = message
        self.job_id = job_id
        super().__init__(self.message)


def _get_error_from_grpc_status(
    status_code: grpc.StatusCode,
    message: str,
    *,
    error_details: Optional[ErrorDetails] = None,
    auth_details: Optional[AuthDetails] = None,
    connection_string: Optional[str] = None
):
    if error_details is not None:
        _raise_error_from_error_details(
            error_details
        )  # attempt to use details first
    if status_code == grpc.StatusCode.UNAUTHENTICATED:
        return AuthenticationFailedError(
            message,
            auth_details=auth_details,
            connection_string=connection_string
        )
    if status_code == grpc.StatusCode.PERMISSION_DENIED:
        return UnauthorizedAccessError(message)
    if status_code == grpc.StatusCode.ALREADY_EXISTS:
        return AlreadyExistsError(
            "The resource or entity already exists. Details: " + str(message)
        )
    if status_code == grpc.StatusCode.NOT_FOUND:
        return NotFoundError(message)
    if status_code == grpc.StatusCode.UNIMPLEMENTED:
        raise NotSupportedError(
            f"UNIMPLEMENTED error[{message}]. Check connection string / function are in a correct and supported configuration. If the issue persists contact TruEra for help."
        )
    if status_code == grpc.StatusCode.INVALID_ARGUMENT:
        raise ValueError(message)
    if status_code == grpc.StatusCode.DEADLINE_EXCEEDED:
        raise TimeoutError(message)
    raise UnknownRpcError(
        "Unexpected error: Code: [" + str(status_code) + "][" + str(message) +
        "]. If the issue persists contact TruEra for help."
    )


def _raise_error_from_error_details(error_details: ErrorDetails):
    # eventually, more advanced logic to parse from rich error details
    if error_details.model_runner_job_id:
        raise ModelRunnerError(
            "Model runner has failed!", error_details.model_runner_job_id
        )


class HttpCommunicator(ABC):

    def __init__(
        self,
        connection_string: str,
        auth_details: AuthDetails,
        logger: logging.Logger,
        *,
        verify_cert: Union[bool, str] = True
    ):
        self.connection_string = connection_string
        self.auth_details = auth_details
        self.logger = logger or logging.getLogger(__name__)
        self.headers = {'Content-type': 'application/json'}
        self.session = requests.Session()
        self.session.verify = verify_cert
        if auth_details:
            self.headers.update(auth_details.get_auth_headers(use_http=True))
        self.session.headers.update(self.headers)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.session.close()

    def request_client(self):
        return self.session

    def get_request(self, uri, json_data_or_generator, stream=False):
        return self._execute_request(
            uri=uri,
            params=json_data_or_generator,
            data=None,
            request_func=self.request_client().get,
            stream=stream
        )

    def put_request(self, uri, json_data_or_generator):
        return self._execute_request(
            uri=uri,
            params=None,
            data=json_data_or_generator,
            request_func=self.request_client().put,
        )

    def patch_request(self, uri, json_data_or_generator):
        return self._execute_request(
            uri=uri,
            params=None,
            data=json_data_or_generator,
            request_func=self.request_client().patch,
        )

    def post_request(self, uri, json_data_or_generator, stream=False):
        return self._execute_request(
            uri=uri,
            params=None,
            data=json_data_or_generator,
            request_func=self.request_client().post,
            stream=stream
        )

    def delete_request(self, uri, json_data_or_generator):
        return self._execute_request(
            uri=uri,
            params=None,
            data=json_data_or_generator,
            request_func=self.request_client().delete,
        )

    def get_data_from_response(self, response):
        if hasattr(response, 'text'):
            return response.text
        if hasattr(response, 'content'):
            return response.content
        if hasattr(response, 'data'):
            return response.data
        return ''

    def _execute_request(
        self, uri, params, data, request_func, *, stream=False
    ):
        kwargs = {}
        kwargs["allow_redirects"] = False

        if params:
            kwargs["params"] = self._flatten_dict(self._json_to_dict(params))
        if data:
            kwargs["data"] = data
        if stream:
            kwargs["stream"] = True
            # in streaming mode, the caller takes care of dealing with
            # response and iterating through it.
            return request_func(uri, headers=self.headers, **kwargs)

        response = request_func(uri, headers=self.headers, **kwargs)
        self._handle_response(response)
        return self.get_data_from_response(response)

    def _handle_response(self, response):
        if response.status_code == http.HTTPStatus.OK:
            return
        if response.status_code == http.HTTPStatus.FOUND:
            raise AuthenticationFailedError(
                " An unexpected redirect was detected, make sure you are using the correct"
                " authentication type (token or key based) and correct authentication details."
                " Location: " + response.headers.get("Location", None)
            )
        self.logger.debug(
            "Request failed: Code: {} Headers: {}".format(
                response.status_code, json.dumps(dict(response.headers))
            )
        )
        self._parse_grpc_error_from_response(response)

        # we could not find error classification from either grpc-status or http-status
        raise ConnectionError(
            "Failed to connect to the server. Response code: " +
            str(response.status_code) + " Response header: " +
            json.dumps(dict(response.headers))
        )

    def _proto_to_json(self, proto):
        return MessageToJson(
            proto,
            including_default_value_fields=True,
            preserving_proto_field_name=True
        )

    def _json_to_proto(self, json, return_obj):
        return Parse(json, return_obj, ignore_unknown_fields=True)

    def _json_to_dict(self, json_str):
        return json.loads(json_str)

    def _flatten_dict(self, d, parent="", sep="."):
        flattened = []
        for k, v in d.items():
            flat_key = parent + sep + k if parent else k
            if isinstance(v, dict):
                flattened.extend(self._flatten_dict(v, flat_key, sep).items())
            else:
                flattened.append((flat_key, v))
        return dict(flattened)

    def _parse_grpc_error_from_response(self, response):
        error_message = response.headers.get(_KEY_GRPC_ERROR_MESSAGE_HEADER, "")
        grpc_status_str = response.headers.get(
            _KEY_GRPC_STATUS_CODE_HEADER, str(grpc.StatusCode.UNKNOWN.value[0])
        )
        error_details = self._parse_grpc_rich_error_details_from_response(
            response
        )
        grpc_status = _grpc_status_code_to_enum.get(
            int(grpc_status_str), grpc.StatusCode.UNKNOWN
        )
        # if grpc_status is unknown, try to translate error from HTTP status_code
        if grpc_status == grpc.StatusCode.UNKNOWN:
            grpc_status = _default_http_code_to_grpc_status_map.get(
                response.status_code, grpc.StatusCode.UNKNOWN
            )

        if grpc_status != grpc.StatusCode.UNKNOWN:
            raise _get_error_from_grpc_status(
                grpc_status,
                error_message,
                error_details=error_details,
                auth_details=self.auth_details,
                connection_string=self.connection_string
            )

    def _parse_grpc_rich_error_details_from_response(
        self, response
    ) -> ErrorDetails:
        error_details_proto = ErrorDetails()
        error_details_binarized = response.headers.get(
            _KEY_GRPC_ERROR_DETAILS_HEADER, ""
        )
        if not error_details_binarized:
            return error_details_proto
        try:
            rich_status = status_pb2.Status()
            rich_status.ParseFromString(
                base64.urlsafe_b64decode(error_details_binarized + "==")
            )  # adding extra padding to avoid decoding errors
            rich_status.details[0].Unpack(error_details_proto)
        except:
            self.logger.debug(
                "Failed to deserialize rich error details from headers!"
            )
        finally:
            return error_details_proto
