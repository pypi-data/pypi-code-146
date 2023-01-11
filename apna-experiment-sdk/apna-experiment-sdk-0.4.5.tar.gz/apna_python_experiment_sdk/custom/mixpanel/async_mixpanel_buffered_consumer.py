# Reference - https://github.com/jessepollak/mixpanel-python-async/blob/master/mixpanel_async/async_buffered_consumer.py

from mixpanel import BufferedConsumer, MixpanelException
import threading
import logging
import copy


class FlushThread(threading.Thread):
    '''
    FlushThread is used to asynchronously flush the events stored in
    the AsyncBufferedConsumer's buffers.
    '''

    def __init__(self, consumer, endpoint=None):
        threading.Thread.__init__(self)
        self._consumer = consumer
        self._endpoint = endpoint

    def run(self):
        with self._consumer._flush_lock:
            self._consumer._sync_flush_endpoint(self._endpoint)


class AsyncBufferedConsumer(BufferedConsumer):
    """A consumer that maintains per-endpoint buffers of messages and then sends
    them asynchronously in batches to Mixpanel.

    Args:
        max_size (int, optional): max_size: number of :meth:`~.send` calls for a given endpoint to
            buffer before flushing automatically. Defaults to 50.
        events_url (_type_, optional): override the default events API endpoint. Defaults to None.
        people_url (_type_, optional): override the default people API endpoint. Defaults to None.
        import_url (_type_, optional): override the default import API endpoint. Defaults to None.
        request_timeout (_type_, optional): connection timeout in seconds. Defaults to None.
        groups_url (_type_, optional): override the default groups API endpoint. Defaults to None.
        api_host (str, optional): the Mixpanel API domain where all requests should be
            issued (unless overridden by above URLs). Defaults to "api.mixpanel.com".
        retry_limit (int, optional): number of times to retry each retry in case of
            connection or HTTP 5xx error; 0 to fail after first attempt. Defaults to 4.
        retry_backoff_factor (float, optional): In case of retries, controls sleep time. e.g.,
            sleep_seconds = backoff_factor * (2 ^ (num_total_retries - 1)). Defaults to 0.25.
        verify_cert (bool, optional): whether to verify the server certificate. Defaults to True.
    """

    def __init__(self, buffer_size=50, max_size=1000, events_url=None, people_url=None, import_url=None,
                 request_timeout=None, groups_url=None, api_host="api.mixpanel.com",
                 retry_limit=4, retry_backoff_factor=0.25, verify_cert=True):

        super(AsyncBufferedConsumer, self).__init__(max_size=max_size, events_url=events_url, people_url=people_url, import_url=import_url,
                                                    request_timeout=request_timeout, groups_url=groups_url, api_host=api_host, retry_limit=retry_limit, retry_backoff_factor=retry_backoff_factor, verify_cert=verify_cert)
        self._buffer_size = buffer_size
        self._async_buffers = copy.deepcopy(self._buffers)
        self._flush_thread = None
        self._flush_lock = threading.Lock()

    def send(self, endpoint, json_message, api_key=None, api_secret=None):
        """Record an event or profile update

        Internally, adds the message to a buffer, and then flushes the buffer
        if it has reached the configured maximum size.

        Args:
            endpoint ("events" | "people" | "groups" | "imports"): the Mixpanel API endpoint appropriate for the message
            json_message (str): a JSON message formatted for the endpoint
            api_key (str, optional): your Mixpanel project's API key. Defaults to None.
            api_secret (str, optional): your Mixpanel project's API secret. Defaults to None.

        Raises:
            MixpanelException: if the endpoint doesn't exist, the server is
            unreachable, or any buffered message cannot be processed
        """
        if endpoint not in self._async_buffers:
            raise MixpanelException('No such endpoint "{0}". Valid endpoints are one of {1}'.format(
                endpoint, self._async_buffers.keys()))

        if not isinstance(api_key, tuple):
            api_key = (api_key, api_secret)

        buf = self._async_buffers[endpoint]
        buf.append(json_message)

        self._api_key = api_key
        self._api_secret = api_secret

        if len(self._async_buffers[endpoint]) >= self._buffer_size:
            self._flush_endpoint(endpoint)

    def flush(self, asynchronous: bool = True):
        """Immediately send all buffered messages to Mixpanel.

        Args:
            asynchronous (bool, optional): Send messages asynchronously. Defaults to True.

        Raises:
            MixpanelException: if the server is unreachable or any buffered
            message cannot be processed
        """
        for endpoint in self._buffers.keys():
            self._flush_endpoint(endpoint, asynchronous)

    def _flush_endpoint(self, endpoint, asynchronous: bool = True):
        """Send the messages in the buffer to Mixpanel

        Args:
            endpoint ("events" | "people" | "groups" | "imports"): the Mixpanel API endpoint appropriate for the message
            asynchronous (bool, optional): Send messages asynchronously. Defaults to True.
        """
        if asynchronous:
            if self._flush_thread_is_available():
                self._flush_thread = FlushThread(self, endpoint=endpoint)
                self._flush_thread.start()
        else:
            self._sync_flush_endpoint(endpoint=endpoint)

    def _sync_flush_endpoint(self, endpoint):
        """Send the messages in the buffer to Mixpanel (synchronously).

        Args:
            endpoint ("events" | "people" | "groups" | "imports"): the Mixpanel API endpoint appropriate for the message
        """
        event_count = len(self._async_buffers[endpoint])
        logging.info(
            f"Flushing {event_count} events from async mixpanel buffered consumer to MixPanel.")
        self._transfer_buffer(endpoint=endpoint)
        super(AsyncBufferedConsumer, self)._flush_endpoint(endpoint=endpoint)

    def _flush_thread_is_available(self) -> bool:
        """
        Check whether the flush_thread is currently being used to flush events.
        Used to ensure that only one thread is flushing the events at a time.

        Returns:
            bool: True, if thread is available to flush events, False if the thread is already being used.
        """
        if self._flush_thread is None:
            return True

        if not self._flush_thread.is_alive():
            return True

        return False

    def _transfer_buffer(self, endpoint):
        """Transfer events from AsyncBufferedConsumer's `_async_buffers` to BufferedConsumer's `_buffers`
        where they will be flushed from by the flushing thread.

        Args:
            endpoint ("events" | "people" | "groups" | "imports"): the Mixpanel API endpoint appropriate for the message
        """
        buf = self._async_buffers[endpoint]
        while buf:
            self._buffers[endpoint].append(buf.pop(0))

    def _join_flush_thread(self):
        """Wait until the _flush_thread is completed
        """
        if self._flush_thread:
            self._flush_thread.join()
