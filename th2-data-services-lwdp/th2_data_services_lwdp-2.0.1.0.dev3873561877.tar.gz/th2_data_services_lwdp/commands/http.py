#  Copyright 2022 Exactpro (Exactpro Systems Limited)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from abc import abstractmethod
from typing import List, Optional, Union, Generator, Any
from datetime import datetime
from functools import partial

from th2_data_services import Data
from th2_data_services.exceptions import EventNotFound, MessageNotFound
from th2_data_services.interfaces import IStreamAdapter
from th2_data_services.utils.converters import DatetimeConverter, ProtobufTimestampConverter
from th2_data_services_lwdp.interfaces.command import IHTTPCommand
from th2_data_services_lwdp.data_source.http import HTTPDataSource
from th2_data_services_lwdp.source_api.http import HTTPAPI
from th2_data_services_lwdp.streams import Streams, Stream
from th2_data_services.sse_client import SSEClient
from th2_data_services_lwdp.adapters.adapter_sse import get_default_sse_adapter
from th2_data_services.decode_error_handler import UNICODE_REPLACE_HANDLER
from th2_data_services_lwdp.filters.event_filters import LwDPEventFilter
from th2_data_services_lwdp.utils import (
    Page,
    _check_milliseconds,
    _check_list_or_tuple,
)
from th2_grpc_common.common_pb2 import Event


# LOG import logging

# LOG logger = logging.getLogger(__name__)


class SSEHandlerClassBase(IHTTPCommand):
    def __init__(
        self,
        sse_handler: IStreamAdapter,
        cache: bool,
        char_enc: str = "utf-8",
        decode_error_handler: str = UNICODE_REPLACE_HANDLER,
    ):
        """SSEHandlerClassBase Constructor.

        Args:
            sse_handler (IStreamAdapter): SSEEvents Handler
            cache (bool): Cache Status
            char_enc (Optional, str): Encoder, Defaults To 'UTF-8'
            decode_error_handler (Optional, str): Decode Error Handler, Defaults To 'UNICODE_REPLACE_HANDLER'
        """
        self._current_handle_function = self._data_object
        self._char_enc = char_enc
        self._decode_error_handler = decode_error_handler
        self._sse_handler = sse_handler
        self._cache = cache

    def return_sse_bytes_stream(self):
        """Returns SSEBytes Stream.

        Returns:
           Generator[bytes, None, None]
        """
        self._current_handle_function = self._sse_bytes_stream
        return self

    def return_sse_events_stream(self):
        """Returns SSEEvents Stream.

        Returns:
            Generator[Event, Any, None]
        """
        self._current_handle_function = self._sse_events_stream
        return self

    def return_data_object(self):
        """Returns Parsed 'Data' Object.

        Returns:
            Data
        """
        self._current_handle_function = self._data_object
        return self

    def _sse_bytes_stream(
        self, data_source: HTTPDataSource
    ) -> Generator[bytes, None, None]:  # noqa
        api: HTTPAPI = data_source.source_api
        urls: List[str] = self._get_urls(data_source.source_api)
        for url in urls:
            # LOG             logger.info(url)
            yield from api.execute_sse_request(url)

    def _sse_events_stream(self, data_source: HTTPDataSource) -> Generator[Event, Any, None]:
        """Turns SSEByte Stream Into SSEEvent Stream.

        Args:
            data_source: HTTPDataSource

        Returns:
             Generator[Event, Any, None]
        """
        sse_bytes_stream = partial(self._sse_bytes_stream, data_source)

        client = SSEClient(
            sse_bytes_stream(),
            char_enc=self._char_enc,
            decode_errors_handler=self._decode_error_handler,
        )

        yield from client.events()

    def _data_object(self, data_source: HTTPDataSource) -> Data:
        """Parses SSEEvents Into Data Object.

        Args:
            data_source: HTTPDataSource

        Returns:
             Data
        """
        sse_events_stream = partial(self._sse_events_stream, data_source)
        data = Data(sse_events_stream).map_stream(self._sse_handler.handle).use_cache(self._cache)
        data.metadata["urls"] = self._get_urls(data_source.source_api)
        return data

    @abstractmethod
    def _get_urls(self, api: HTTPAPI) -> List[str]:
        pass

    def handle(
        self, data_source: HTTPDataSource
    ) -> Union[Generator[bytes, None, None], Generator[Event, None, None], Data]:
        """Handles Stream By Handle Function, Defaults To `Data`.

        Args:
            data_source: data_source

        Returns:
            Union[Generator[bytes, None, None], Generator[Event, None, None], Data]
        """
        return self._current_handle_function(data_source)


class GetEventScopes(IHTTPCommand):
    """A Class-Command for request to lw-data-provider.

    It retrieves a list of event scopes in book.

    Returns:
        dict: List[str].
    """

    def __init__(self, book_id: str):
        """GetEventScopes constructor.

        Args:
            book_id: Name of book to search in.
        """
        super().__init__()
        self._book_id = book_id

    def handle(self, data_source: HTTPDataSource) -> List[str]:  # noqa: D102
        api: HTTPAPI = data_source.source_api
        url = api.get_url_get_scopes(self._book_id)

        # LOG         logger.info(url)

        return api.execute_request(url).json()


class GetMessageAliases(IHTTPCommand):
    """A Class-Command for request to lw-data-provider.

    It retrieves a list of message aliases in book.

    Returns:
        dict: List[str].
    """

    def __init__(self, book_id: str):
        """GetMessageAliases constructor.

        Args:
            book_id: Name of book to search in.
        """
        super().__init__()
        self._book_id = book_id

    def handle(self, data_source: HTTPDataSource) -> List[str]:  # noqa: D102
        api: HTTPAPI = data_source.source_api
        url = api.get_url_get_message_aliases(self._book_id)

        # LOG         logger.info(url)

        return api.execute_request(url).json()


class GetMessageGroups(IHTTPCommand):
    """A Class-Command for request to lw-data-provider.

    It retrieves a list of message groups in book.

    Returns:
        dict: List[str].
    """

    def __init__(self, book_id: str):
        """GetMessageGroups constructor.

        Args:
            book_id: Name of book to search in.
        """
        super().__init__()
        self._book_id = book_id

    def handle(self, data_source: HTTPDataSource) -> List[str]:  # noqa: D102
        api: HTTPAPI = data_source.source_api
        url = api.get_url_get_message_groups(self._book_id)

        # LOG         logger.info(url)

        return api.execute_request(url).json()


class GetBooks(IHTTPCommand):
    """A Class-Command for request to lw-data-provider.

    It retrieves a list of books from provider.

    Returns:
        dict: List[str].
    """

    def __init__(self):
        """GetBooks constructor."""
        super().__init__()

    def handle(self, data_source: HTTPDataSource) -> List[str]:  # noqa: D102
        api: HTTPAPI = data_source.source_api
        url = api.get_url_get_books()

        # LOG         logger.info(url)

        return api.execute_request(url).json()


class GetPages(SSEHandlerClassBase):
    def __init__(
        self,
        book_id: str,
        start_timestamp: datetime,
        end_timestamp: datetime,
        result_limit: int = None,
        sse_handler: IStreamAdapter = None,
        buffer_limit: int = 250,
        cache: bool = False,
    ) -> None:
        """GetPages Constructor.

        Args:
            book_id (str): Book ID.
            start_timestamp (datetime): Start Timestamp. API expects timestamp in milliseconds.
            end_timestamp (datetime): End Timestamp. API expects timestamp in milliseconds.
            result_limit (Optional, int): Return Result Limit.
            sse_handler (Optional, IStreamAdapter): SSE Events Handler. Defaults To `SSEAdapter`.
            cache (Optional, bool): Cache Status. Defaults To `False`.
            buffer_limit: SSEAdapter BufferedJSONProcessor buffer limit.
        """
        _check_milliseconds(start_timestamp)
        _check_milliseconds(end_timestamp)
        self._sse_handler = sse_handler or get_default_sse_adapter(buffer_limit=buffer_limit)
        super().__init__(self._sse_handler, cache)
        self._book_id = book_id
        self._start_timestamp = DatetimeConverter.to_milliseconds(start_timestamp)
        self._end_timestamp = DatetimeConverter.to_milliseconds(end_timestamp)
        self._result_limit = result_limit

    def _get_urls(self, api: HTTPAPI):
        return [
            api.get_url_get_pages_info(
                self._book_id, self._start_timestamp, self._end_timestamp, self._result_limit
            )
        ]

    def _sse_events_to_pages(self, data_source: HTTPDataSource):  # noqa
        source = partial(self._sse_handler.handle, self._sse_events_stream(data_source))
        for event_data in source():
            yield Page(event_data)

    def _data_object(self, data_source: HTTPDataSource) -> Data:
        """Parses SSEEvents Into Data Object.

        Args:
            data_source: HTTPDataSource

        Returns:
             Data
        """
        source = partial(self._sse_events_to_pages, data_source)
        data = Data(source, cache=self._cache)
        data.metadata["urls"] = self._get_urls(data_source.source_api)
        return data


class GetEventById(IHTTPCommand):
    """A Class-Command for request to lw-data-provider.

    It retrieves the event by id with `attachedMessageIds` list.

    Returns:
        dict: Th2 event.

    Raises:
        EventNotFound: If event by Id wasn't found.
    """

    def __init__(self, id: str, use_stub=False):
        """GetEventById constructor.

        Args:
            id: Event id.
            use_stub: If True the command returns stub instead of exception.

        """
        super().__init__()
        self._id = id
        self._stub_status = use_stub

    def handle(self, data_source: HTTPDataSource) -> dict:  # noqa: D102
        api: HTTPAPI = data_source.source_api
        url = api.get_url_find_event_by_id(self._id)

        # LOG         logger.info(url)

        response = api.execute_request(url)
        # +TODO - perhaps we have to move it to api.execute_request
        if response.status_code == 404 and self._stub_status:
            stub = data_source.event_stub_builder.build(
                {data_source.event_struct.EVENT_ID: self._id}
            )
            return stub
        elif response.status_code == 404:
            # LOG             logger.error(f"Unable to find the message. Id: {self._id}")
            raise EventNotFound(self._id)
        else:
            return response.json()


class GetEventsById(IHTTPCommand):
    """A Class-Command for request to lw-data-provider.

    It retrieves the events by ids with `attachedMessageIds` list.

    Returns:
        List[dict]: Th2 events.

    Raises:
        EventNotFound: If any event by Id wasn't found.
    """

    def __init__(self, ids: List[str], use_stub=False):
        """GetEventsById constructor.

        Args:
            ids: Event id list.
            use_stub: If True the command returns stub instead of exception.

        """
        super().__init__()
        self._ids: ids = ids
        self._stub_status = use_stub

    def handle(self, data_source: HTTPDataSource) -> List[dict]:  # noqa: D102
        result = []
        for event_id in self._ids:
            event = GetEventById(event_id, use_stub=self._stub_status).handle(data_source)
            result.append(event)

        return result


# class GetEvents(SSEHandlerClassBase):
class GetEventsByBookByScopes(SSEHandlerClassBase):
    """A Class-Command for request to lw-data-provider.

    It searches events stream by options.

    Returns:
        Iterable[dict]: Stream of Th2 events.
    """

    def __init__(
        self,
        start_timestamp: datetime,
        book_id: str,
        scopes: List[str],
        end_timestamp: Optional[datetime] = None,
        parent_event: str = None,
        search_direction: str = "next",
        result_count_limit: int = None,
        filters: Union[LwDPEventFilter, List[LwDPEventFilter]] = None,
        # Non-data source args.
        # +TODO - add `max_url_length: int = 2048,`
        #   It'll be required when you implement `__split_requests` in source_api/http.py
        cache: bool = False,
        sse_handler: Optional[IStreamAdapter] = None,
        char_enc: str = "utf-8",
        decode_error_handler: str = UNICODE_REPLACE_HANDLER,
        buffer_limit=250,
    ):
        """GetEventsByBookByScopes constructor.

        Args:
            start_timestamp: Start timestamp of search. API expects timestamp in milliseconds.
            book_id: Book ID for messages.
            scopes: Scope names for events.
            end_timestamp: End timestamp of search. API expects timestamp in milliseconds.
            parent_event: Match events to the specified parent.
            search_direction: Search direction.
            result_count_limit: Result count limit.
            filters: Filters using in search for messages.
            cache: If True, all requested data from lw-data-provider will be saved to cache.
            sse_handler: SSEEvents handler, by default uses StreamingSSEAdapter
            char_enc: Encoding for the byte stream.
            decode_error_handler: Registered decode error handler.
            max_url_length: API request url max length.
            buffer_limit: SSEAdapter BufferedJSONProcessor buffer limit.
        """
        _check_milliseconds(start_timestamp)
        _check_milliseconds(end_timestamp)
        self._sse_handler = sse_handler or get_default_sse_adapter(buffer_limit=buffer_limit)
        super().__init__(
            sse_handler=self._sse_handler,
            cache=cache,
            char_enc=char_enc,
            decode_error_handler=decode_error_handler,
        )

        self._cache = cache
        # +TODO - we can make timestamps optional datetime or int. We have to check that it's in ms.

        self._start_timestamp = DatetimeConverter.to_milliseconds(start_timestamp)
        self._end_timestamp = DatetimeConverter.to_milliseconds(end_timestamp)
        self._parent_event = parent_event
        self._search_direction = search_direction
        self._result_count_limit = result_count_limit
        self._filters = filters
        self._book_id = book_id
        self._scopes = scopes
        if isinstance(filters, LwDPEventFilter):
            self._filters = filters.url()
        elif isinstance(filters, (tuple, list)):
            self._filters = "".join([filter_.url() for filter_ in filters])

        _check_list_or_tuple(self._scopes, var_name="scopes")

    def _get_urls(self, api: HTTPAPI):
        return [
            api.get_url_search_sse_events(
                start_timestamp=self._start_timestamp,
                end_timestamp=self._end_timestamp,
                parent_event=self._parent_event,
                search_direction=self._search_direction,
                result_count_limit=self._result_count_limit,
                filters=self._filters,
                book_id=self._book_id,
                scope=scope,
            )
            for scope in self._scopes
        ]


class GetEventsByPageByScopes(SSEHandlerClassBase):
    """A Class-Command for request to lw-data-provider.

    It searches events stream by options.

    Returns:
        Iterable[dict]: Stream of Th2 events.
    """

    def __init__(
        self,
        page: Page,
        scopes: List[str],
        parent_event: str = None,
        search_direction: str = "next",
        result_count_limit: int = None,
        filters: Union[LwDPEventFilter, List[LwDPEventFilter]] = None,
        # Non-data source args.
        # +TODO - add `max_url_length: int = 2048,`
        #   It'll be required when you implement `__split_requests` in source_api/http.py
        cache: bool = False,
        sse_handler: Optional[IStreamAdapter] = None,
        char_enc: str = "utf-8",
        decode_error_handler: str = UNICODE_REPLACE_HANDLER,
        buffer_limit=250,
    ):
        """GetEventsByPageByScopes constructor.

        Args:
            page: Page to search with.
            scopes: Scope names for events.
            parent_event: Match events to the specified parent.
            search_direction: Search direction.
            result_count_limit: Result count limit.
            filters: Filters using in search for messages.
            cache: If True, all requested data from lw-data-provider will be saved to cache.
            sse_handler: SSEEvents handler, by default uses StreamingSSEAdapter
            char_enc: Encoding for the byte stream.
            decode_error_handler: Registered decode error handler.
            max_url_length: API request url max length.
            buffer_limit: SSEAdapter BufferedJSONProcessor buffer limit.
        """
        self._sse_handler = sse_handler or get_default_sse_adapter(buffer_limit=buffer_limit)
        super().__init__(
            sse_handler=self._sse_handler,
            cache=cache,
            char_enc=char_enc,
            decode_error_handler=decode_error_handler,
        )

        self._cache = cache
        # +TODO - we can make timestamps optional datetime or int. We have to check that it's in ms.

        self._start_timestamp = ProtobufTimestampConverter.to_milliseconds(page.start_timestamp)
        self._end_timestamp = (
            DatetimeConverter.to_milliseconds(datetime.now().replace(microsecond=0))
            if page.end_timestamp is None
            else ProtobufTimestampConverter.to_milliseconds(page.end_timestamp)
        )
        self._book_id = page.book
        self._parent_event = parent_event
        self._search_direction = search_direction
        self._result_count_limit = result_count_limit
        self._filters = filters
        self._scopes = scopes
        if isinstance(filters, LwDPEventFilter):
            self._filters = filters.url()
        elif isinstance(filters, (tuple, list)):
            self._filters = "".join([filter_.url() for filter_ in filters])

        _check_list_or_tuple(self._scopes, var_name="scopes")

    def _get_urls(self, api: HTTPAPI):
        return [
            api.get_url_search_sse_events(
                start_timestamp=self._start_timestamp,
                end_timestamp=self._end_timestamp,
                parent_event=self._parent_event,
                search_direction=self._search_direction,
                result_count_limit=self._result_count_limit,
                filters=self._filters,
                book_id=self._book_id,
                scope=scope,
            )
            for scope in self._scopes
        ]


class GetMessageById(IHTTPCommand):
    """A Class-Command for request to lw-data-provider.

    It retrieves the message by id.

    Returns:
        dict: Th2 message.

    Raises:
        MessageNotFound: If message by id wasn't found.
    """

    def __init__(self, id: str, use_stub=False):
        """GetMessageById constructor.

        Args:
            id: Message id.
            use_stub: If True the command returns stub instead of exception.

        """
        super().__init__()
        self._id = id
        self._stub_status = use_stub

    def handle(self, data_source: HTTPDataSource) -> dict:  # noqa: D102
        api: HTTPAPI = data_source.source_api
        url = api.get_url_find_message_by_id(self._id)

        # LOG         logger.info(url)
        response = api.execute_request(url)
        if response.status_code in (404, 408) and self._stub_status:
            stub = data_source.message_stub_builder.build(
                {data_source.message_struct.MESSAGE_ID: self._id}
            )
            return stub
        elif response.status_code in (404, 408):
            # LOG             logger.error(f"Unable to find the message. Id: {self._id}")
            raise MessageNotFound(self._id)
        else:
            return response.json()


class GetMessagesById(IHTTPCommand):
    """A Class-Command for request to lw-data-provider.

    It retrieves the messages by ids.

    Returns:
        List[dict]: Th2 messages.

    Raises:
        MessageNotFound: If any message by id wasn't found.
    """

    def __init__(self, ids: List[str], use_stub=False):
        """GetMessagesById constructor.

        Args:
            ids: Message id list.
            use_stub: If True the command returns stub instead of exception.

        """
        super().__init__()
        self._ids: ids = ids
        self._stub_status = use_stub

    def handle(self, data_source: HTTPDataSource) -> List[dict]:  # noqa: D102
        result = []
        for message_id in self._ids:
            message = GetMessageById(
                message_id,
                use_stub=self._stub_status,
            ).handle(data_source)
            result.append(message)

        return result


class GetMessagesByBookByStreams(SSEHandlerClassBase):
    """A Class-Command for request to lw-data-provider.

    It searches messages stream by options.

    Returns:
        Iterable[dict]: Stream of Th2 messages.
    """

    def __init__(
        self,
        start_timestamp: datetime,
        book_id: str,
        streams: Union[List[Union[str, Streams, Stream]], Streams],
        message_ids: List[str] = None,
        search_direction: str = "next",
        result_count_limit: int = None,
        end_timestamp: datetime = None,
        response_formats: List[str] = None,
        keep_open: bool = False,
        # Non-data source args.
        # +TODO - we often repeat these args. Perhaps it's better to move them to some class.
        max_url_length: int = 2048,
        char_enc: str = "utf-8",
        decode_error_handler: str = UNICODE_REPLACE_HANDLER,
        cache: bool = False,
        sse_handler: Optional[IStreamAdapter] = None,
        buffer_limit=250,
    ):
        """GetMessages constructor.

        Args:
            start_timestamp: Start timestamp of search. API expects timestamp in milliseconds.
            book_id: Book ID for messages
            streams: List of aliases to request. If direction is not specified all directions will be requested for stream.
            message_ids: List of message IDs to restore search. If given, it has
                the highest priority and ignores streams (uses streams from ids), startTimestamp and resumeFromId.
            search_direction: Search direction.
            result_count_limit: Result count limit.
            end_timestamp: End timestamp of search. API expects timestamp in milliseconds.
            response_formats: The format of the response
            keep_open: If the search has reached the current moment.
                It needs to wait further for the appearance of new data.
            char_enc: Encoding for the byte stream.
            decode_error_handler: Registered decode error handler.
            cache: If True, all requested data from lw-data-provider will be saved to cache.
            sse_handler: SSEEvents handler, by default uses StreamingSSEAdapter
            max_url_length: API request url max length.
            buffer_limit: SSEAdapter BufferedJSONProcessor buffer limit.
        """
        _check_milliseconds(start_timestamp)
        _check_milliseconds(end_timestamp)
        self._sse_handler = sse_handler or get_default_sse_adapter(buffer_limit=buffer_limit)
        super().__init__(
            sse_handler=self._sse_handler,
            cache=cache,
            char_enc=char_enc,
            decode_error_handler=decode_error_handler,
        )

        self._streams = streams
        self._search_direction = search_direction
        self._result_count_limit = result_count_limit
        self._response_formats = response_formats
        self._keep_open = keep_open
        self._message_ids = message_ids
        self._book_id = book_id
        self._max_url_length = max_url_length
        self._char_enc = char_enc
        self._decode_error_handler = decode_error_handler
        self._cache = cache

        # + TODO - we can make timestamps optional datetime or int
        self._start_timestamp = DatetimeConverter.to_milliseconds(start_timestamp)
        self._end_timestamp = (
            end_timestamp
            if end_timestamp is None
            else DatetimeConverter.to_milliseconds(end_timestamp)
        )

        if self._start_timestamp is None and not self._message_ids:
            raise TypeError("One of start_timestamp or message_id arguments must not be empty")

        if isinstance(streams, Streams):
            self._streams = streams.as_list()
        elif isinstance(streams, (tuple, list, Streams)):
            self._streams = []
            for stream in streams:
                if isinstance(stream, Stream):
                    self._streams.append(stream.url()[8:])
                elif isinstance(stream, Streams):
                    self._streams += stream.as_list()
                else:
                    self._streams.append(stream)
        else:
            raise TypeError(
                f"streams argument has to be list, tuple or Streams type. "
                f"Got {type(self._streams)}"
            )

    def _get_urls(self, api: HTTPAPI):
        return api.get_url_search_sse_messages(
            start_timestamp=self._start_timestamp,
            message_ids=self._message_ids,
            stream=self._streams,
            search_direction=self._search_direction,
            result_count_limit=self._result_count_limit,
            end_timestamp=self._end_timestamp,
            response_formats=self._response_formats,
            keep_open=self._keep_open,
            book_id=self._book_id,
            max_url_length=self._max_url_length,
        )


class GetMessagesByBookByGroups(SSEHandlerClassBase):
    """A Class-Command for request to lw-data-provider.

    It searches messages stream by groups.

    Returns:
        Iterable[dict]: Stream of Th2 messages.
    """

    def __init__(
        self,
        start_timestamp: datetime,
        end_timestamp: datetime,
        book_id: str,
        groups: List[str],
        sort: bool = None,
        response_formats: List[str] = None,
        keep_open: bool = None,
        # Non-data source args.
        max_url_length: int = 2048,
        char_enc: str = "utf-8",
        decode_error_handler: str = UNICODE_REPLACE_HANDLER,
        cache: bool = False,
        sse_handler: Optional[IStreamAdapter] = None,
        buffer_limit=250,
    ):
        """GetMessagesByGroups Constructor.

        Args:
            start_timestamp: Sets the search starting point. API expects timestamp in milliseconds.
            end_timestamp: Sets the timestamp to which the search will be performed, starting with 'start_timestamp'.
                 API expects timestamp in milliseconds.
            book_id: book ID for requested groups.
            groups: List of groups to search messages from.
            sort: Enables message sorting within a group. It is not sorted between groups.
            response_formats: The format of the response
            keep_open: If true, keeps pulling for new message until don't have one outside the requested range.
            char_enc: Encoding for the byte stream.
            decode_error_handler: Registered decode error handler.
            cache: If True, all requested data from lw-data-provider will be saved to cache.
            sse_handler: SSEEvents handler, by default uses StreamingSSEAdapter
            max_url_length: API request url max length.
            buffer_limit: SSEAdapter BufferedJSONProcessor buffer limit.
        """
        self._sse_handler = sse_handler or get_default_sse_adapter(buffer_limit=buffer_limit)
        super().__init__(
            sse_handler=self._sse_handler,
            cache=cache,
            char_enc=char_enc,
            decode_error_handler=decode_error_handler,
        )

        self._char_enc = char_enc
        self._decode_error_handler = decode_error_handler
        self._cache = cache
        self._start_timestamp = DatetimeConverter.to_milliseconds(start_timestamp)
        self._end_timestamp = (
            end_timestamp
            if end_timestamp is None
            else DatetimeConverter.to_milliseconds(end_timestamp)
        )
        self._groups = groups
        self._sort = sort
        self._response_formats = response_formats
        self._keep_open = keep_open
        self._book_id = book_id
        self._max_url_length = max_url_length

        _check_list_or_tuple(self._groups, var_name="groups")

    def _get_urls(self, api: HTTPAPI):
        return api.get_url_search_messages_by_groups(
            start_timestamp=self._start_timestamp,
            end_timestamp=self._end_timestamp,
            groups=self._groups,
            response_formats=self._response_formats,
            keep_open=self._keep_open,
            sort=self._sort,
            book_id=self._book_id,
            max_url_length=self._max_url_length,
        )


class GetMessagesByPageByStreams(SSEHandlerClassBase):
    def __init__(
        self,
        page: Page,
        stream: List[str],
        message_ids: List[None] = None,
        search_direction: Optional[str] = "next",
        result_count_limit: int = None,
        response_formats: List[str] = None,
        keep_open: bool = None,
        max_url_length: int = 2048,
        char_enc: str = "utf-8",
        decode_error_handler: str = UNICODE_REPLACE_HANDLER,
        cache: bool = False,
        sse_handler: Optional[IStreamAdapter] = None,
        buffer_limit: int = 250,
    ):
        """GetMessagesByPageByStreams Constructor.

        Args:
            page: Page to search with.
            stream: In which streams to search.
            message_ids: Search for message ids.
            result_count_limit: Max results to get.
            search_direction: Search direction.
            response_formats: The format of the response
            keep_open: If true, keeps pulling for new message until don't have one outside the requested range.
            max_url_length: API request url max length.
            char_enc: Encoding for the byte stream.
            decode_error_handler: Registered decode error handler.
            cache: If True, all requested data from lw-data-provider will be saved to cache.
            sse_handler: SSEEvents handler, by default uses StreamingSSEAdapter
            buffer_limit: SSEAdapter BufferedJSONProcessor buffer limit.
        """
        self._sse_handler = sse_handler or get_default_sse_adapter(buffer_limit=buffer_limit)
        super().__init__(
            sse_handler=self._sse_handler,
            cache=cache,
            char_enc=char_enc,
            decode_error_handler=decode_error_handler,
        )

        self._char_enc = char_enc
        self._decode_error_handler = decode_error_handler
        self._cache = cache
        self._page = page
        self._start_timestamp = ProtobufTimestampConverter.to_milliseconds(page.start_timestamp)
        self._end_timestamp = (
            DatetimeConverter.to_milliseconds(datetime.now().replace(microsecond=0))
            if page.end_timestamp is None
            else ProtobufTimestampConverter.to_milliseconds(page.end_timestamp)
        )
        self._book_id = page.book
        self._result_count_limit = result_count_limit
        self._search_direction = search_direction
        self._response_formats = response_formats
        self._message_ids = message_ids
        self._keep_open = keep_open
        self._max_url_length = max_url_length
        self._stream = stream

    def _get_urls(self, api: HTTPAPI):
        return api.get_url_search_sse_messages(
            start_timestamp=self._start_timestamp,
            book_id=self._book_id,
            message_ids=self._message_ids,
            stream=self._stream,
            search_direction=self._search_direction,
            result_count_limit=self._result_count_limit,
            end_timestamp=self._end_timestamp,
            response_formats=self._response_formats,
            keep_open=self._keep_open,
            max_url_length=self._max_url_length,
        )


class GetMessagesByPageByGroups(SSEHandlerClassBase):
    """A Class-Command for request to lw-data-provider.

    It searches messages stream by page & groups.

    Returns:
        Iterable[dict]: Stream of Th2 messages.
    """

    def __init__(
        self,
        page: Page,
        groups: List[str],
        sort: bool = None,
        response_formats: List[str] = None,
        keep_open: bool = None,
        # Non-data source args.
        max_url_length: int = 2048,
        char_enc: str = "utf-8",
        decode_error_handler: str = UNICODE_REPLACE_HANDLER,
        cache: bool = False,
        sse_handler: Optional[IStreamAdapter] = None,
        buffer_limit=250,
    ):
        """GetMessagesByPageByGroups Constructor.

        Args:
            page: Page to search with.
            groups: List of groups to search messages from.
            sort: Enables message sorting within a group. It is not sorted between groups.
            response_formats: The format of the response
            keep_open: If true, keeps pulling for new message until don't have one outside the requested range.
            char_enc: Encoding for the byte stream.
            decode_error_handler: Registered decode error handler.
            cache: If True, all requested data from lw-data-provider will be saved to cache.
            sse_handler: SSEEvents handler, by default uses StreamingSSEAdapter
            max_url_length: API request url max length.
            buffer_limit: SSEAdapter BufferedJSONProcessor buffer limit.
        """
        self._sse_handler = sse_handler or get_default_sse_adapter(buffer_limit=buffer_limit)
        super().__init__(
            sse_handler=self._sse_handler,
            cache=cache,
            char_enc=char_enc,
            decode_error_handler=decode_error_handler,
        )

        self._char_enc = char_enc
        self._decode_error_handler = decode_error_handler
        self._cache = cache
        self._page = page
        self._page_data = page.data
        self._start_timestamp = ProtobufTimestampConverter.to_milliseconds(page.start_timestamp)
        self._end_timestamp = (
            DatetimeConverter.to_milliseconds(datetime.now().replace(microsecond=0))
            if page.end_timestamp is None
            else ProtobufTimestampConverter.to_milliseconds(page.end_timestamp)
        )
        self._book_id = page.book
        self._groups = groups
        self._sort = sort
        self._response_formats = response_formats
        self._keep_open = keep_open
        self._max_url_length = max_url_length

        _check_list_or_tuple(self._groups, var_name="groups")

    def _get_urls(self, api: HTTPAPI):
        return api.get_url_search_messages_by_groups(
            start_timestamp=self._start_timestamp,
            end_timestamp=self._end_timestamp,
            groups=self._groups,
            response_formats=self._response_formats,
            keep_open=self._keep_open,
            sort=self._sort,
            book_id=self._book_id,
            max_url_length=self._max_url_length,
        )
