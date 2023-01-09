"""ByteBlower IPv4 Port interface module."""
import logging
from ipaddress import IPv4Address, IPv4Network
from typing import Optional, Sequence  # for type hinting

from byteblowerll.byteblower import (  # for type hinting
    DHCPv4Protocol,
    IPv4Configuration,
)

from ..._host.server import Server  # for type hinting
from ..port import Port, VlanConfig  # for type hinting

#: Default netmask for an :class:`IPv4Port`
DEFAULT_IPV4_NETMASK = '255.255.255.0'


class IPv4Port(Port):
    """ByteBlower Port interface for IPv4."""

    __slots__ = ('_dhcp_failed', )

    def __init__(
        self,
        server: Server,
        interface: str = None,
        name: Optional[str] = None,
        mac: Optional[str] = None,
        vlans: Optional[Sequence[VlanConfig]] = None,
        ipv4: Optional[str] = None,
        netmask: Optional[str] = DEFAULT_IPV4_NETMASK,
        gateway: Optional[str] = None,
        tags: Optional[Sequence[str]] = None,
        **kwargs,
    ) -> None:
        """
        Initialize a ByteBlowerPort.

        .. note::
           L2 is *only* configured if:

           1. Explicitly given MAC address
           2. Layer 3 is configured

           A port without L2/L3 configuration can for example be used
           for pure 'promiscuous' capturing of data.
        """
        super().__init__(server,
                         interface=interface,
                         name=name,
                         mac=mac,
                         vlans=vlans,
                         tags=tags,
                         **kwargs)
        self._dhcp_failed = False

        if ipv4 is not None:
            self._conf['ipv4'] = ipv4
        else:
            # No config? Just do DHCPv4
            self._conf['ipv4'] = 'dhcp'
        self._conf['netmask'] = netmask
        if gateway:
            self._conf['gateway'] = gateway

        self._configure()

    def _configure_L3(self) -> IPv4Configuration:
        ipv4_addr = self._conf.get('ipv4')
        assert ipv4_addr is not None, \
            'The IPv4Port constructor should have set the ipv4 configuration.'
        # If we don't have a mac address yet, generate one automatically
        self._configure_L2()
        # Layer 2.5 configuration MUST be done after L2 and before L3
        self._configure_L2_5()
        port_l3: IPv4Configuration = self._bb_port.Layer3IPv4Set()
        # Verify we have a valid IP or netmask
        if ipv4_addr.lower() == 'dhcp':
            try:
                # Perform DHCP
                port_l3_dhcp: DHCPv4Protocol = port_l3.ProtocolDhcpGet()
                port_l3_dhcp.Perform()
            except Exception:
                logging.exception('DHCP failed for %s on %s!', self._name,
                                  self._interface)
                self._dhcp_failed = True
        else:
            try:
                address = IPv4Address(ipv4_addr)
                nm = IPv4Address(self._conf['netmask'])
                port_l3.IpSet(str(address))
                port_l3.NetmaskSet(str(nm))
            except Exception:
                # Maybe it is an IP and netmask format
                try:
                    network = IPv4Network(ipv4_addr, strict=False)
                    port_l3.IpSet(ipv4_addr.split("/")[0])
                    port_l3.NetmaskSet(str(network.netmask))
                except Exception:
                    logging.exception('Invalid IPv4 adress: %s', ipv4_addr)
        gw = self._conf.get('gateway')
        if gw is not None:
            try:
                port_l3.GatewaySet(gw)
            except Exception:
                logging.exception('Error while setting gateway to %r', gw)

        return port_l3

    @property
    def failed(self) -> bool:
        return self._dhcp_failed

    @property
    def ip(self) -> IPv4Address:
        return IPv4Address(self.layer3.IpGet())

    @property
    def network(self) -> IPv4Network:
        return IPv4Network(self.layer3.IpGet() + "/" +
                           self.layer3.NetmaskGet(),
                           strict=False)

    @property
    def gateway(self) -> IPv4Address:
        return IPv4Address(self.layer3.GatewayGet())

    @property
    def layer3(self) -> IPv4Configuration:
        """
        IPv4 configuration of the ByteBlower Lower Layer API.

        .. note::
           Subject to change in dual stack implementations.
        """
        return super().layer3
