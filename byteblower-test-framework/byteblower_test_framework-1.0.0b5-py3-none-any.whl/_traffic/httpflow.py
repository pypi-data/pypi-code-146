from datetime import timedelta
from typing import Optional, Union  # for type hinting

from .._endpoint.port import Port  # for type hinting
from .tcpflow import HttpMethod, TcpFlow


class HTTPFlow(TcpFlow):

    __slots__ = (
        '_tcp_server_port',
        '_tcp_client_port',
        '_request_duration',
        '_initial_time_to_wait',
        '_rate_limit',
        '_receive_window_scaling',
        '_slow_start_threshold',
        '_ip_tos',
    )

    _CONFIG_ELEMENTS = TcpFlow._CONFIG_ELEMENTS + (
        'tcp_server_port',
        'rate_limit',
        'receive_window_scaling',
        'slow_start_threshold',
    )

    def __init__(
        self,
        source: Port,
        destination: Port,
        name: Optional[str] = None,
        http_method: HttpMethod = HttpMethod.AUTO,
        tcp_server_port: Optional[int] = None,
        tcp_client_port: Optional[int] = None,
        request_duration: Optional[Union[timedelta, float, int]] = None,
        initial_time_to_wait: Optional[Union[timedelta, float,
                                             int]] = None,  # [seconds]
        rate_limit: Optional[int] = None,
        receive_window_scaling: Optional[int] = None,
        slow_start_threshold: Optional[int] = None,
        ip_tos: Optional[int] = None,
        **kwargs
    ) -> None:
        super().__init__(
            source, destination, name=name, http_method=http_method, **kwargs
        )
        self._tcp_server_port = tcp_server_port
        self._tcp_client_port = tcp_client_port
        if isinstance(request_duration, (float, int)):
            # Convert to timedelta
            self._request_duration = timedelta(seconds=request_duration)
        else:
            # Either already timedelta or None:
            self._request_duration = request_duration
        if isinstance(initial_time_to_wait, (float, int)):
            # Convert to timedelta
            self._initial_time_to_wait = timedelta(
                seconds=initial_time_to_wait
            )
        else:
            # Either already timedelta or None:
            # Default to 0s
            self._initial_time_to_wait = initial_time_to_wait or timedelta()
        self._rate_limit = rate_limit
        self._receive_window_scaling = receive_window_scaling
        self._slow_start_threshold = slow_start_threshold
        self._ip_tos = ip_tos

    @property
    def tcp_server_port(self) -> Optional[int]:
        """TCP port of the HTTP server."""
        if self._bb_tcp_server:
            return self._bb_tcp_server.PortGet()
        return self._tcp_server_port

    @property
    def rate_limit(self) -> Optional[int]:
        """Return the requested HTTP rate limit.

        :return: The rate limit, in bytes per second.
        :rtype: Optional[int]
        """
        return self._rate_limit

    @property
    def receive_window_scaling(self) -> Optional[int]:
        """TCP Receive Window scaling."""
        if self._bb_tcp_server:
            if self._bb_tcp_server.ReceiveWindowScalingIsEnabled():
                return self._bb_tcp_server.ReceiveWindowScalingValueGet()
            return None
        return self._receive_window_scaling

    @property
    def slow_start_threshold(self) -> Optional[int]:
        """TCP Slow Start Threshold."""
        if self._bb_tcp_server:
            return self._bb_tcp_server.SlowStartThresholdGet()
        return self._slow_start_threshold

    def apply(
        self,
        duration: Optional[Union[timedelta, float]] = None,
        **_kwargs
    ) -> None:
        """Open a session, send the file and close the connection."""
        if self._request_duration is None:
            if isinstance(duration, (float, int)):
                # Convert to timedelta
                self._request_duration = timedelta(seconds=duration)
            else:
                # Either already timedelta or None:
                self._request_duration = duration
        # Create a TCP server on the destination.
        http_server = self._set_tcp_server(
            tcp_port=self._tcp_server_port,
            receive_window_scaling=self._receive_window_scaling,
            slow_start_threshold=self._slow_start_threshold
        )
        if http_server is not None:
            # New HTTP server (not re-using existing one)
            http_server.Start()

        # Create the first client session so we will get started
        self._add_client_session(
            request_duration=self._request_duration,
            rate_limit=self._rate_limit,
            ittw=self._initial_time_to_wait,
            receive_window_scaling=self._receive_window_scaling,
            slow_start_threshold=self._slow_start_threshold,
            tcp_port=self._tcp_client_port,
            ip_tos=self._ip_tos
        )
