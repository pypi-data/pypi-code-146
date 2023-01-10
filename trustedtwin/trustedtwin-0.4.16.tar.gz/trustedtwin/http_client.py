"""HTTP client for TrustedTwin API client"""
import json
import logging
import threading
from base64 import b64encode
from typing import Dict, Optional, Any

from requests import Response, Session

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import TTResponse

logger = logging.getLogger("trustedtwin")

TT_DICT_HEADER = 'X-TrustedTwin'


def http_header_encode(dictionary: Dict) -> str:
    """Encode dictionary into base64 string"""
    return b64encode(json.dumps(dictionary).encode('utf-8')).decode('utf-8')


class HTTPClient:
    """HTTP client used by TrustedTwin Service"""

    def __init__(
            self,
            host_name: str,
            auth: Optional[str] = None,
            session: Optional[Session] = None,
            tt_dict: Optional[Dict] = None
    ):
        """Initialize object.

        :param auth: authorization token
        :param host_name: string containing host name
        """
        self.host_name = host_name
        self._headers = {"Content-Type": "application/json"}
        self._locals = threading.local()
        self._session = session

        if auth:
            self._headers["Authorization"] = auth
        else:
            logger.warning("Warning - Auth token not set")

        if tt_dict:
            self._headers[TT_DICT_HEADER] = http_header_encode(tt_dict)

    def __repr__(self) -> str:
        """Return nicer print presentation."""
        return "{} - {}".format(self.__class__.__name__, self.host_name)

    def _call(
        self,
        method: RESTMethod,
        url: str,
        headers: Optional[Dict] = None,
        body: Optional[Dict] = None,
        params: Optional[Dict] = None,
        **kwargs: Any
    ) -> Response:
        """Perform actual call to API

        :param method: REST API method to be executed on an endpoint e.g. 'GET', 'POST', 'PATCH'
        :param url: url to be called
        :param headers: headers for request
        :param body: optional payload passed as a json object
        :param params: optional parameters passed as key-worded arguments
        :return: endpoint response
        """
        _method = str(method).lower()
        logging.debug("Calling url: %s", url)

        if getattr(self._locals, "session", None) is None:
            self._locals.session = self._session or Session()

        return self._locals.session.request(
            method=_method,
            url=url,
            data=json.dumps(body) if body else None,
            headers=headers,
            params=params,
            **kwargs
        )


    def execute_request(
        self,
        method: RESTMethod,
        url_root: str,
        endpoint: str,
        body: Optional[Dict] = None,
        params: Optional[Dict] = None,
        **kwargs: Any
    ) -> TTResponse:
        """Execute API request"""
        url = "{}/{}".format(url_root, endpoint)
        params = (
            {key: value for key, value in params.items() if value is not None}
            if params
            else {}
        )

        response = self._call(
            method=method,
            url=url,
            body=body,
            params=params,
            headers=self._headers,
            **kwargs
        )

        return TTResponse(body=response.text, http_code=response.status_code)
