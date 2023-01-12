"""ByteBlower Server interface module."""
import logging

from byteblowerll.byteblower import ByteBlowerServer  # for type hinting
from byteblowerll.byteblower import ByteBlower, ConfigError


class Server(object):
    """ByteBlower Server interface."""

    __slots__ = (
        '_host_ip',
        '_bb_server',
    )

    def __init__(self, ip_or_host: str) -> None:
        """
        Connect to the ByteBlower server.

        :param ip_or_host: The connection address. This can be
           the hostname or IPv4/IPv6 address of the ByteBlower server.
        """
        self._host_ip = ip_or_host
        self._bb_server = ByteBlower.InstanceGet().ServerAdd(self._host_ip)

    @property
    def info(self) -> str:
        """Return connection address this server."""
        return self._host_ip

    def start(self) -> None:
        """Start all ByteBlower Ports configured on this server."""
        logging.debug('Starting all ByteBlowerPorts')
        for port in self._bb_server.PortGet():
            try:
                port.Start()
            except ConfigError:
                continue

    def stop(self) -> None:
        """Stop all ByteBlower Ports configured on this server."""
        logging.debug('Stopping all ByteBlowerPorts')
        for port in self._bb_server.PortGet():
            port.Stop()

    @property
    def bb_server(self) -> ByteBlowerServer:
        """Server object from the ByteBlower API."""
        return self._bb_server
