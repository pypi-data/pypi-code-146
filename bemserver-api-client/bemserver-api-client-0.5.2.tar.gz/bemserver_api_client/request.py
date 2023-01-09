"""BEMServer API client request"""
import logging
import os
import requests
import requests.exceptions as req_exc

from .enums import DataFormat
from .response import BEMServerApiClientResponse
from .exceptions import BEMServerAPIInternalError, BEMServerAPIClientValueError


class BEMServerApiClientRequest:
    """API client requester"""

    _ETAG_HEADER_BY_HTTP_METHOD = {
        "GET": "If-None-Match",
        "PUT": "If-Match",
        "DELETE": "If-Match",
    }

    def __init__(self, base_uri, authentication_method, *, logger=None):
        self.base_uri = base_uri

        self._logger = logger or logging.getLogger(__name__)
        self._session = requests.Session()
        self._session.auth = authentication_method

    def _build_uri(self, endpoint_uri):
        return f"{self.base_uri}{endpoint_uri}"

    def _prepare_accept_header(self, format):
        """

        :raises TypeError: when format is None or not an enum type
        :raises BEMServerAPIClientValueError: when format is not in DataFormat enum
        """
        if format not in DataFormat:
            raise BEMServerAPIClientValueError(f"Invalid data format: {format}")
        return {"Accept": format.value}

    def _prepare_etag_header(self, http_method, etag):
        etag_header = {}
        if etag is not None:
            try:
                etag_header = {
                    self._ETAG_HEADER_BY_HTTP_METHOD[http_method.upper()]: etag
                }
            except KeyError:
                pass
        return etag_header

    def _execute(self, http_method, endpoint, *, etag=None, **kwargs):
        full_endpoint_uri = self._build_uri(endpoint)
        headers = {
            **kwargs.pop("headers", {}),
            **self._prepare_etag_header(http_method, etag),
        }
        self._logger.debug(f"{http_method} {full_endpoint_uri}")
        try:
            raw_resp = self._session.request(
                http_method, full_endpoint_uri, headers=headers, **kwargs
            )
        except req_exc.RequestException as exc:
            self._logger.error(
                f"Unexpected error while requesting {full_endpoint_uri}: {exc}"
            )
            raise BEMServerAPIInternalError from exc
        return BEMServerApiClientResponse(raw_resp)

    @staticmethod
    def _exclude_empty_files(files):
        """

        :param dict files:
            key is the upload field name (csv_file, timeseries_csv or sites_csv...)
            value is a file stream (tempfile.SpooledTemporaryFile)
        """
        not_empty_files = {}
        for k, v in files.items():
            if v is not None and v.seek(0, os.SEEK_END) > 0:
                v.seek(0, os.SEEK_SET)
                not_empty_files[k] = v
        return not_empty_files

    def getall(self, endpoint, *, etag=None, **kwargs):
        return self._execute("GET", endpoint, etag=etag, **kwargs)

    def getone(self, endpoint, *, etag=None):
        return self._execute("GET", endpoint, etag=etag)

    def create(self, endpoint, payload):
        return self._execute("POST", endpoint, json=payload)

    def update(self, endpoint, payload, etag):
        return self._execute("PUT", endpoint, json=payload, etag=etag)

    def delete(self, endpoint, etag):
        return self._execute("DELETE", endpoint, etag=etag)

    def upload_files(self, endpoint, files, **kwargs):
        """Upload files.

        :param dict files:
            key is the upload field name (csv_file, timeseries_csv or sites_csv...)
            value is a file stream (tempfile.SpooledTemporaryFile)
        """
        not_empty_files = self._exclude_empty_files(files)
        return self._execute("POST", endpoint, files=not_empty_files, **kwargs)

    def upload_data(self, endpoint, data, *, format=DataFormat.json, **kwargs):
        """Upload data from specified format.

        :param str data: data to upload (for example a read content of file stream)
        :param DataFormat format: (optional, default JSON)
            data format, either CSV or JSON
        """
        kwargs["headers"] = {
            **kwargs.pop("headers", {}),
            **self._prepare_accept_header(format),
        }
        return self._execute("POST", endpoint, data=data, **kwargs)

    def download(self, endpoint, *, format=DataFormat.json, **kwargs):
        """Download data in specified format.

        :param DataFormat format: (optional, default JSON)
            data format, either CSV or JSON
        """
        kwargs["headers"] = {
            **kwargs.pop("headers", {}),
            **self._prepare_accept_header(format),
        }
        return self._execute("GET", endpoint, **kwargs)
