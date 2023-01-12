import binascii
import logging
from ipaddress import IPv4Address
from time import sleep
from typing import Dict, Optional, Sequence, Tuple  # for type hinting

from byteblowerll.byteblower import (  # for type hinting
    Capture,
    CapturedFrame,
    CaptureResultSnapshot,
    Frame,
    Stream,
)
from scapy.all import raw
from scapy.layers.inet import IP, UDP, Ether

from ..._host.server import Server  # for type hinting
from ..._traffic.frame import UDP_DYNAMIC_PORT_START
from .port import DEFAULT_IPV4_NETMASK, IPv4Port

_CACHE_KEY_FORMAT = '{}/{}'


class NatResolver(object):

    __slots__ = (
        '_port',
        '_cache',
        '_public_ip',
    )

    def __init__(self, port: IPv4Port) -> None:
        self._port = port
        self._cache: Dict[str, Tuple[str, int]] = {}
        self._public_ip: Optional[str] = None

    def resolve(self,
                public_port: IPv4Port,
                public_udp_port: int = UDP_DYNAMIC_PORT_START,
                nat_udp_port: int = UDP_DYNAMIC_PORT_START) -> Tuple[str, int]:

        # Collect generic information:
        public_port_l3 = public_port.layer3
        public_ip_address = public_port_l3.IpGet()

        nat_port_l3 = self._port.layer3
        nat_ip_address = nat_port_l3.IpGet()
        # Check if it is already in our cache
        _cache_key = _CACHE_KEY_FORMAT.format(public_ip_address,
                                              public_udp_port, nat_udp_port)
        _cache_entry = self._cache.get(_cache_key)
        if _cache_entry:
            return _cache_entry

        # Prepare stream configuration
        # Resolve destination MAC address
        mac: str = None
        try:
            mac = nat_port_l3.Resolve(public_ip_address)
        except Exception:
            logging.debug(
                'Exception occurred while trying to resolve'
                ' public IP address %s from NATted port %r',
                public_ip_address,
                self._port.name,
                exc_info=True)
            mac = nat_port_l3.Resolve(nat_port_l3.GatewayGet())
        logging.debug("NATTED PORT %r DEST MAC: %s", self._port.name, mac)

        # Build frame content
        # NOTE: Done in byteblower_test_framework.logging.configure_logging():
        # logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

        payload = 'a' * (200)
        scapy_udp_payload = raw(payload.encode('ascii', 'strict'))
        scapy_udp_header = UDP(dport=public_udp_port, sport=nat_udp_port)
        scapy_ip_header = IP(src=nat_ip_address, dst=public_ip_address)
        scapy_ethernet_header = Ether(src=self._port.mac, dst=mac)
        scapy_frame = (scapy_ethernet_header / scapy_ip_header /
                       scapy_udp_header / scapy_udp_payload)
        logging.debug('NatResolver for %r: Transmit Content: %s',
                      self._port.name, scapy_frame.summary())

        # Configure stream
        stream: Stream = self._port.bb_port.TxStreamAdd()
        stream.InterFrameGapSet(10 * 1000 * 1000)  # 10ms
        stream.NumberOfFramesSet(-1)

        # Add frame to the stream
        frame_content = bytearray(bytes(scapy_frame))
        # The ByteBlower API expects an 'str' as input
        # for the Frame::BytesSet(), we need to convert the bytearray.
        hexbytes = ''.join((format(b, '02x') for b in frame_content))

        tx_frame: Frame = stream.FrameAdd()
        tx_frame.BytesSet(hexbytes)

        # Create destination capture
        capture: Capture = public_port.bb_port.RxCaptureBasicAdd()
        capture.FilterSet('dst host {!s} and udp'.format(public_ip_address))

        # Start resolution process
        capture.Start()
        stream.Start()

        sleep(0.2)

        # Stop stream (should have stopped by itself already)
        stream.Stop()
        # Remove the stream, no longer required
        self._port.bb_port.TxStreamRemove(stream)

        # stop capture
        capture.Stop()

        capture_result: CaptureResultSnapshot = capture.ResultGet()
        capture_frames: Sequence[CapturedFrame] = capture_result.FramesGet()
        if len(capture_frames) == 0:
            public_port.bb_port.RxCaptureBasicRemove(capture)
            raise RuntimeError('NAT failed, no packets received on public port'
                               ' for NATted port {}.'.format(self._port.name))

        result = None
        for capture_frame in capture_frames:
            captured_bytes = capture_frame.BytesGet()
            # logging.debug('Checking frame %s for public IPaddress.',
            #               captured_bytes)
            raw_bytes = binascii.unhexlify(captured_bytes)
            # get source ip and udp port from captured packet
            # Layer 2 decoding
            # -- decoding LENGTH/TYPE field
            ether = Ether(raw_bytes)
            logging.debug('NatResolver for %r: Received Content: %s',
                          self._port.name, ether.summary())
            if ether.haslayer(IP) and ether.haslayer(UDP):
                nat_public_ip: str = ether[IP].src
                nat_public_udp: int = ether[UDP].sport
                self._public_ip = nat_public_ip
                result = (nat_public_ip, nat_public_udp)
                self._cache[_cache_key] = result
                break

        # Cleanup the capture
        public_port.bb_port.RxCaptureBasicRemove(capture)

        if result is None:
            raise RuntimeError('Could not resolve public NAT information'
                               f' for {self._port.name!r}')

        return result

    @property
    def public_ip(self) -> Optional[str]:
        return self._public_ip


class NattedPort(IPv4Port):

    __slots__ = ('_nat_resolver', )

    def __init__(self,
                 server: Server,
                 interface: str = None,
                 mac: Optional[str] = None,
                 ipv4: Optional[str] = None,
                 netmask: Optional[str] = DEFAULT_IPV4_NETMASK,
                 gateway: Optional[str] = None,
                 name: Optional[str] = None,
                 tags: Optional[Sequence[str]] = None,
                 **kwargs) -> None:
        super().__init__(server,
                         interface=interface,
                         mac=mac,
                         ipv4=ipv4,
                         netmask=netmask,
                         gateway=gateway,
                         name=name,
                         tags=tags,
                         **kwargs)
        self._nat_resolver = NatResolver(self)

    @property
    def public_ip(self) -> IPv4Address:
        # TODO - Return ip when public_ip is not (yet) resolved?
        if self._nat_resolver.public_ip:
            return IPv4Address(self._nat_resolver.public_ip)
        # TODO - Resolve NAT when not yet done?
        #      * For example when only performing TCP tests
        #        (NAT is not resolved then via the NatResolver)
        return self.ip

    @property
    def is_natted(self) -> bool:
        return True

    def nat_discover(
            self,
            public_port: IPv4Port,
            public_udp_port: int = UDP_DYNAMIC_PORT_START,
            nat_udp_port: int = UDP_DYNAMIC_PORT_START) -> Tuple[str, int]:
        """
        Resolve the public IPv4 address (UDP port) as seen by `public_port`.

        .. note::
           UDP ports can be left to the default if
           you are only interested in the public IP.
        """
        if self._nat_resolver is None:
            self._nat_resolver = NatResolver(self)
        return self._nat_resolver.resolve(public_port,
                                          public_udp_port=public_udp_port,
                                          nat_udp_port=nat_udp_port)
