import logging
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional, Union  # for type hinting

# // from byteblowerll.byteblower import ConvertHTTPRequestStatusToString
# Helper functions to parse the strings (HTTP Method, ...)
# to the enumerations used by the API and vice versa
from byteblowerll.byteblower import HTTPClient  # for type hinting
from byteblowerll.byteblower import HTTPServer  # for type hinting
from byteblowerll.byteblower import (  # helper functions
    HTTPServerStatus,
    ParseHTTPRequestMethodFromString,
    ParseTCPCongestionAvoidanceAlgorithmFromString,
    RequestStartType,
)

from .._endpoint.ipv4.nat import NattedPort  # for type hinting
from .._endpoint.port import Port  # for type hinting
from .flow import Flow

_DEFAULT_DURATION_SECONDS: float = 10.0
_SECONDS_PER_NANOSECOND: int = 1000000000

_BYTES_PER_MB: float = 1000000.0


class HttpMethod(Enum):
    """HTTP method used for HTTP (client) sessions."""

    AUTO = 'Automatic'
    GET = 'GET'
    PUT = 'PUT'


class TCPCongestionAvoidanceAlgorithm(Enum):
    NONE = 'None'
    new_reno = 'new-reno'
    new_reno_with_cubic = 'new-reno-with-cubic'
    sack = 'sack'
    sack_with_cubic = 'sack-with-cubic'


class TcpFlow(Flow):
    """
    Flow, supporting multiple and/or restarting TCP clients.

    - Single HTTP server on the "WAN side" of the network.
    - One or multiple clients on the "CPE side" of the network.
    """

    __slots__ = (
        '_bb_tcp_server',
        '_bb_tcp_clients',
        '_http_method',
    )

    _CONFIG_ELEMENTS = Flow._CONFIG_ELEMENTS + ('http_method', )

    def __init__(
        self,
        source: Union[Port, NattedPort],
        destination: Union[Port, NattedPort],
        name: Optional[str] = None,
        http_method: HttpMethod = HttpMethod.AUTO,
        **kwargs
    ) -> None:
        """
        Create a new TCP Flow.

        No clients, servers or sessions are created yet.
        """
        super().__init__(source, destination, name=name, **kwargs)
        self._bb_tcp_server: HTTPServer = None
        self._bb_tcp_clients: List[HTTPClient] = list()
        self._http_method = http_method

        # Sanity checks
        if self._http_method != HttpMethod.AUTO:
            raise NotImplementedError(
                'TCP Flow {!r} only support automatic HTTP method for now'
                .format(self.name)
            )

    @property
    def http_method(self) -> str:
        """HTTP method used for HTTP (client) session."""
        return self._http_method.value

    def _set_tcp_server(
        self,
        server_port: Optional[Port] = None,
        tcp_port: Optional[int] = None,
        receive_window_scaling: Optional[int] = None,
        slow_start_threshold: Optional[int] = None,
        caa: Optional[TCPCongestionAvoidanceAlgorithm] = None,
    ) -> Optional[HTTPServer]:
        """Create a HTTP server.

        .. note::
           When a TCP port is given, an existing HTTP server can be re-used.

        :param server_port: Force HTTP server on the given ByteBlower Port.
           When set to ``None``, choose the port based on the :ref:HttpMethod,
           defaults to None
        :type server_port: Optional[Port], optional
        :param tcp_port: TCP port where the HTTP server listens to,
           defaults to None
        :type tcp_port: Optional[int], optional
        :param receive_window_scaling: When given, enable receive window
           scaling with the given scale factor, defaults to None
        :type receive_window_scaling: Optional[int], optional
        :param slow_start_threshold: TCP Slow start threshold value,
           defaults to None
        :type slow_start_threshold: Optional[int], optional
        :param caa: Use the given TCP congestion avoidance algorithm,
           defaults to None (server default)
        :type caa: Optional[TCPCongestionAvoidanceAlgorithm], optional
        :raises RuntimeError: _description_
        :raises NotImplementedError: When no ``server_port`` is given and
           HttpMethod is not set to AUTO.
        :raises ValueError: When an HTTP server is already configured
           with incompatible settings.
        :return: The new or existing HTTP Server. When it is already active,
           ``None`` is returned since we don't allow reconfiguring it
           once started.
        :rtype: Optional[HTTPServer]
        """
        # Sanity checks
        if self._bb_tcp_server:
            raise RuntimeError('TCP server is already set')

        # Set the default client and server port
        if not server_port:
            if self._http_method != HttpMethod.AUTO:
                # TODO - Implement for given HTTP Method
                raise NotImplementedError(
                    'TCP Flow {!r} only support automatic HTTP method'
                    ' (for now)'.format(self.name)
                )
            if self.source.is_natted:
                # Base Flow does not allow both source and destination NAT
                assert not self.destination.is_natted, \
                    'Source + destination natted is not supported'
                server_port = self.destination
            else:
                server_port = self.source

        if tcp_port is not None:
            # Re-use existing HTTP Server.
            # Raise an error when incompatible settings are requested.
            for http_server in \
                    server_port.bb_port.ProtocolHttpServerGet():
                if http_server.PortGet() != tcp_port:
                    continue

                if receive_window_scaling is not None:
                    if not http_server.ReceiveWindowScalingIsEnabled():
                        raise ValueError(
                            'Incompatible existing HTTP server found'
                        )
                    if (http_server.ReceiveWindowScalingValueGet() !=
                            receive_window_scaling):
                        raise ValueError(
                            'Incompatible existing HTTP server found'
                        )
                if slow_start_threshold is not None:
                    if (http_server.SlowStartThresholdGet() !=
                            slow_start_threshold):
                        raise ValueError(
                            'Incompatible existing HTTP server found'
                        )
                if caa is not None:
                    if (http_server.TcpCongestionAvoidanceAlgorithmGet() !=
                            ParseTCPCongestionAvoidanceAlgorithmFromString(
                                caa.value)):
                        raise ValueError(
                            'Incompatible existing HTTP server found'
                        )

                self._bb_tcp_server = http_server

                http_server_status = http_server.StatusGet()
                if http_server_status == HTTPServerStatus.Running:
                    # Do not return the HTTP server.
                    # The caller should not start or re-configure
                    # active HTTP servers.
                    return None
                return self._bb_tcp_server

        # Create a TCP server on the destination.
        http_server: HTTPServer = \
            server_port.bb_port.ProtocolHttpServerAdd()
        if tcp_port is not None:
            http_server.PortSet(tcp_port)
        if receive_window_scaling is not None:
            http_server.ReceiveWindowScalingEnable(True)
            http_server.ReceiveWindowScalingValueSet(receive_window_scaling)
        if slow_start_threshold is not None:
            http_server.SlowStartThresholdSet(slow_start_threshold)
        if caa is not None:
            http_server.TcpCongestionAvoidanceAlgorithmSet(
                ParseTCPCongestionAvoidanceAlgorithmFromString(caa.value)
            )

        self._bb_tcp_server = http_server

        return self._bb_tcp_server

    def _add_client_session(
        self,
        client_port: Optional[Union[Port, NattedPort]] = None,
        server_port: Optional[Port] = None,
        request_duration: Optional[timedelta] = None,
        request_size: Optional[int] = None,
        rate_limit: Optional[int] = None,
        ittw: timedelta = timedelta(seconds=0),
        receive_window_scaling: Optional[int] = None,
        slow_start_threshold: Optional[int] = None,
        caa: Optional[TCPCongestionAvoidanceAlgorithm] = None,
        tcp_port: Optional[int] = None,
        ip_tos: Optional[int] = None,
    ) -> HTTPClient:
        """
        Start a "scheduled" HTTP session.

        .. note::
           The returned HTTP client session is added to the
           list of client sessions, but not yet started!

        :param ittw: Initial time to wait.

        :return:
            The newly created HTTP Client.
        """
        # Sanity checks
        if request_size is None and request_duration is None:
            logging.info(
                'Neither HTTP request size or duration are given.'
                ' Default to duration of %fs', _DEFAULT_DURATION_SECONDS
            )
            request_duration = timedelta(seconds=_DEFAULT_DURATION_SECONDS)

        # Set the default client and server port
        if not client_port and not server_port:
            if self.source.is_natted:
                # Base Flow does not allow both source and destination NAT
                assert not self.destination.is_natted, \
                    'Source + destination natted is not supported'
                logging.debug('%s: Server at destination', self.name)
                server_port = self.destination
                client_port = self.source
            else:
                logging.debug('%s: Server at source', self.name)
                server_port = self.source
                client_port = self.destination
        elif not server_port:
            raise ValueError(
                'TCP Flow {!r}: Client Port {!r} given without server Port',
                self.name, client_port.name
            )
        elif not client_port:
            raise ValueError(
                'TCP Flow {!r}: Server Port {!r} given without client Port',
                self.name, server_port.name
            )

        # Create the client
        clientsession: HTTPClient = client_port.bb_port.ProtocolHttpClientAdd()
        if tcp_port is not None:
            clientsession.LocalPortSet(tcp_port)
        clientsession.RemoteAddressSet(str(server_port.ip))
        tcpserverport = self._bb_tcp_server.PortGet()
        clientsession.RemotePortSet(tcpserverport)

        if self._http_method == HttpMethod.AUTO:
            if client_port == self.source:
                logging.debug('%s: Using PUT', self.name)
                http_method = HttpMethod.PUT.value
            else:
                logging.debug('%s: Using GET', self.name)
                http_method = HttpMethod.GET.value
            clientsession.HttpMethodSet(
                ParseHTTPRequestMethodFromString(http_method)
            )
        else:
            clientsession.HttpMethodSet(
                ParseHTTPRequestMethodFromString(self._http_method.value)
            )

        clientsession.RequestStartTypeSet(RequestStartType.Scheduled)
        ittw_nanoseconds = int(ittw.total_seconds() * _SECONDS_PER_NANOSECOND)
        clientsession.RequestInitialTimeToWaitSet(ittw_nanoseconds)

        # Sanity checks
        if request_duration is not None:
            if request_size is not None:
                logging.warning(
                    'Both HTTP request duration and size are given.'
                    ' Using duration.'
                )
            # Set the duration
            logging.debug('Requesting HTTP data during %s.', request_duration)
            duration_nanoseconds = \
                int(request_duration.total_seconds() * _SECONDS_PER_NANOSECOND)
            clientsession.RequestDurationSet(duration_nanoseconds)
        elif request_size is not None:
            # Set the size
            logging.debug(
                'Requesting HTTP data of %f MB.', request_size / _BYTES_PER_MB
            )
            clientsession.RequestSizeSet(request_size)

        # Session metrics
        if rate_limit:
            clientsession.RequestRateLimitSet(rate_limit)

        # IP settings
        if ip_tos is not None:
            clientsession.TypeOfServiceSet(ip_tos)

        # TCP settings
        if receive_window_scaling is not None:
            clientsession.ReceiveWindowScalingEnable(True)
            clientsession.ReceiveWindowScalingValueSet(receive_window_scaling)
        if slow_start_threshold is not None:
            clientsession.SlowStartThresholdSet(slow_start_threshold)
        if caa is not None:
            clientsession.TcpCongestionAvoidanceAlgorithmSet(
                ParseTCPCongestionAvoidanceAlgorithmFromString(caa.value)
            )

        self._bb_tcp_clients.append(clientsession)

        return clientsession

    def _last_client_session(self) -> HTTPClient:
        if not self._bb_tcp_clients:
            raise ValueError('No TCP client created yet')
        return self._bb_tcp_clients[-1]

    def wait_until_finished(self, wait_for_finish: timedelta) -> None:
        finish_time = datetime.now() + wait_for_finish
        for tcp_client in self._bb_tcp_clients:
            remaining_wait_time = finish_time - datetime.now()
            if remaining_wait_time > timedelta(seconds=0):
                tcp_client.WaitUntilFinished(
                    remaining_wait_time.seconds * _SECONDS_PER_NANOSECOND
                )
            else:
                return None
