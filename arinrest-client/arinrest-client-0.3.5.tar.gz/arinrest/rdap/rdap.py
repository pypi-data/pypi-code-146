from arinrest.common.connection import ArinRestConnection
from ipaddress import IPv4Network, IPv6Network
from typing import Union
import json


class RdapClient(object):
    def __init__(self, connection: ArinRestConnection):
        self.connection = connection

    def entity(self, handle: str):
        url = f"/registry/entity/{handle}"
        return self.get_json(url)

    def asn(self, asn: int):
        url = f"/registry/autnum/{asn}"
        return self.get_json(url)

    def domain(self, domain: str):
        url = f"/registry/domain/{domain}"
        return self.get_json(url)

    def network(self, network: Union[IPv4Network, IPv6Network]):
        url = f"/registry/ip/{network.network_address}/{network.prefixlen}"
        return self.get_json(url)

    def get_json(self, url):
        return json.loads(self.connection.get(url))
