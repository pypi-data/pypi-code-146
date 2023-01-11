# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""TextGrid CRUD API."""
import logging
from io import BytesIO
from typing import Optional

import requests
from requests.models import Response
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer

from tgclients.config import TextgridConfig
from tgclients.databinding.textgrid_metadata_2010 import MetadataContainerType

logger = logging.getLogger(__name__)
RESPONSE_ENCODING = 'utf-8'


class TextgridCrudRequest:
    """Provide low level access to the TextGrid CRUD Service."""

    def __init__(self, config: TextgridConfig = TextgridConfig(), nonpublic: bool = False) -> None:
        if nonpublic:
            self._url = config.crud
        else:
            self._url = config.crud_public
        self._config = config

    def read_data(self, textgrid_uri: str, sid: Optional[str] = None) -> Response:
        """Read Data

        Args:
            textgrid_uri (str): Textgrid URI
            sid (Optional[str]): Session ID. Defaults to None.

        Raises:
            TextgridCrudException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            Response: HTTP response from service
        """
        # defer downloading the response body until accessing Response.content
        response = requests.get(self._url + '/' + textgrid_uri + '/data',
                                {'sessionId':  sid},
                                stream=True,
                                timeout=self._config.http_timeout)
        return self._handle_response(response)

    def read_metadata(self, textgrid_uri: str, sid: Optional[str] = None) -> Response:
        """Read Metadata

        Args:
            textgrid_uri (str): Textgrid URI
            sid (Optional[str]): Session ID. Defaults to None.

        Raises:
            TextgridCrudException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            Response: HTTP response from service
        """
        response = requests.get(self._url + '/' + textgrid_uri + '/metadata',
                                {'sessionId':  sid},
                                stream=True,
                                timeout=self._config.http_timeout)
        return self._handle_response(response)

    def create_resource(self, sid: str, project_id: str, data, metadata) -> Response:
        """Create a TextGrid object

        Args:
            sid (str): Session ID
            project_id (str): Project ID
            data ([type]): the data
            metadata ([type]): the metadata

        Raises:
            TextgridCrudException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            Response: HTTP response from service with metadata from newly created object
        """
        encoder = self._prepare_multipart(metadata, data)
        params = {'sessionId': sid, 'projectId': project_id,
                  'createRevision': 'false'}
        response = requests.post(
            self._url + '/' + 'create', params=params, data=encoder,
            headers={'Content-Type': encoder.content_type},
            timeout=self._config.http_timeout)
        return self._handle_response(response)

    def update_resource(self, sid: str, textgrid_uri: str, data, metadata) -> Response:
        """Update a TextGrid object

        Args:
            sid (str): Session ID
            textgrid_uri (str): Textgrid URI
            data ([type]): the data
            metadata ([type]): the metadata

        Raises:
            TextgridCrudException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            Response: HTTP response from service with updated metadata
        """
        encoder = self._prepare_multipart(metadata, data)
        params = {'sessionId': sid}
        response = requests.post(
            self._url + '/' + textgrid_uri + '/update', params=params, data=encoder,
            headers={'Content-Type': encoder.content_type},
            timeout=self._config.http_timeout)
        return self._handle_response(response)

    def update_metadata(self, sid: str, textgrid_uri: str, metadata) -> Response:
        """Update metadata for TextGrid object

        Args:
            sid (str): Session ID
            textgrid_uri (str): Textgrid URI
            metadata ([type]): the metadata

        Returns:
            Response: HTTP response from service with updated metadata
        """
        encoder = self._prepare_multipart(metadata)
        params = {'sessionId': sid}
        response = requests.post(
            self._url + '/' + textgrid_uri + '/updateMetadata', params=params, data=encoder,
            headers={'Content-Type': encoder.content_type},
            timeout=self._config.http_timeout)
        return self._handle_response(response)

    def delete_resource(self, sid: str, textgrid_uri: str) -> Response:
        """Delete a TextGrid object

        Args:
            sid (str): Session ID
            textgrid_uri (str): Textgrid URI

        Raises:
            TextgridCrudException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            Response: HTTP response from service
        """
        params = {'sessionId': sid}
        response = requests.get(
            self._url + '/' + textgrid_uri + '/delete', params=params,
            timeout=self._config.http_timeout)
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response: Response) -> Response:
        """Error handling for responses from crud

        Args:
            response (Response): a response from tgcrud

        Raises:
            TextgridCrudException: if HTTP status code >= 400

        Returns:
            Response: the response
        """
        response.encoding = RESPONSE_ENCODING
        if not response.ok:
            message = '[Error] HTTP Code: ' + \
                str(response.status_code) + ' - ' + response.text[0:255]
            logger.warning(message)
            raise TextgridCrudException(message)
        return response

    @staticmethod
    def _prepare_multipart(metadata, data=None):
        """Create a streaming multipart object.
        Monitor the upload progress if log level is DEBUG.

        See also: https://toolbelt.readthedocs.io/en/latest/uploading-data.html

        Args:
            metadata ([type]): the metadata
            data ([type]): the data

        Returns:
            [MultipartEncoder]: Multipart containing data and metadata
        """
        fields = {
            'tgObjectMetadata': ('tgObjectMetadata', metadata, 'text/xml')
        }
        if data:
            fields['tgObjectData'] = (
                'tgObjectData', data, 'application/octet-stream')

        encoder = MultipartEncoder(fields=fields)
        if logger.isEnabledFor(logging.DEBUG):
            return MultipartEncoderMonitor(encoder, TextgridCrudRequest._debug_monitor_callback)

        return encoder

    @staticmethod
    def _debug_monitor_callback(monitor: MultipartEncoderMonitor):
        """Callback for _prepare_multipart.
        Helper to log upload progress for streaming multipart when log level is DEBUG.

        Args:
            monitor (MultipartEncoderMonitor): the monitor
        """
        logger.debug('[debug multipart upload] bytes read: %s ',
                     monitor.bytes_read)


class TextgridCrudException(Exception):
    """Exception communicating with tgcrud"""


class TextgridCrud(TextgridCrudRequest):
    """Provide access to the Textgrid CRUD Service using a XML data binding """

    def __init__(self, config: TextgridConfig = TextgridConfig(), nonpublic: bool = False) -> None:
        super().__init__(config, nonpublic)
        # It’s recommended to either reuse the same parser/serializer instance
        # or reuse the context instance. see https://xsdata.readthedocs.io/en/latest/xml.html
        context = XmlContext()
        self._parser = XmlParser(context=context)
        self._serializer = XmlSerializer()

    def create_resource(self, sid: str, project_id: str,
                        data, metadata: MetadataContainerType) -> MetadataContainerType:
        """Create a TextGrid object

        Args:
            sid (str): Session ID
            project_id (str): Project ID
            data ([type]): the data
            metadata (MetadataContainerType): the metadata

        Raises:
            TextgridCrudException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            MetadataContainerType: metadata for newly created object
        """
        metadata_string = self._serializer.render(metadata)
        response = super().create_resource(sid, project_id, data, metadata_string)
        return self._parser.parse(BytesIO(response.content), MetadataContainerType)

    def read_metadata(self, textgrid_uri: str, sid: Optional[str] = None) -> MetadataContainerType:
        """Read Metadata

        Args:
            textgrid_uri (str): Textgrid URI
            sid (Optional[str]): Session ID. Defaults to ''.

        Raises:
            TextgridCrudException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
             MetadataContainerType: metadata for object
        """
        response = super().read_metadata(textgrid_uri, sid)
        return self._parser.parse(BytesIO(response.content), MetadataContainerType)

    def update_metadata(self, sid: str, textgrid_uri: str,
                        metadata: MetadataContainerType) -> MetadataContainerType:
        """Update metadata for TextGrid object

        Args:
            sid (str): Session ID
            textgrid_uri (str): Textgrid URI
            metadata (MetadataContainerType): the metadata

        Returns:
            MetadataContainerType: updated metadata
        """
        metadata_string = self._serializer.render(metadata)
        response = super().update_metadata(sid, textgrid_uri, metadata_string)
        return self._parser.parse(BytesIO(response.content), MetadataContainerType)

    def update_resource(self, sid: str, textgrid_uri: str,
                        data, metadata: MetadataContainerType) -> MetadataContainerType:
        """Update a TextGrid object

        Args:
            sid (str): Session ID
            textgrid_uri (str): Textgrid URI
            data ([type]): the data
            metadata (MetadataContainerType): the metadata

        Raises:
            TextgridCrudException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            MetadataContainerType: updated metadata
        """
        metadata_string = self._serializer.render(metadata)
        response = super().update_resource(sid, textgrid_uri, data, metadata_string)
        return self._parser.parse(BytesIO(response.content), MetadataContainerType)
