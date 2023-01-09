from arinrest.common.connection import ArinRestConnection
from arinrest.rpki.rpki import Rpki
from arinrest.irr import IRRClient
from arinrest.rdap import RdapClient
from typing import Union


class ArinRest(object):
    def __init__(
        self,
        api_key: Union[str, None],
    ) -> None:
        self.api_key = api_key

    def rpki(self, private_key: str, **kwargs):
        dev = kwargs.get("dev", False)

        connection = ArinRestConnection("rpki", self.api_key, dev=dev)

        return Rpki(connection, private_key=private_key)

    def irr(self, **kwargs):
        dev = kwargs.get("dev", False)

        connection = ArinRestConnection("irr", self.api_key, dev=dev)
        return IRRClient(connection)

    def rdap(self, **kwargs):
        connection = ArinRestConnection("rdap", None)
        return RdapClient(connection)
