from typing import List
from geodesic.bases import _APIObject
from geodesic.client import raise_on_error
from geodesic.config import get_config
from geodesic.descriptors import _IntDescr, _StringDescr
from geodesic.service import ServiceClient

ted_client = ServiceClient("ted", 1, "share")


class Token(_APIObject):
    """ The token class represents the share tokens created when a user shares a dataset through Ted

    Args:
        **token: values corresponding to the token and the dataset it shares
    """
    token = _StringDescr(doc="unique 32-bit token created by Ted and used to access a shared dataset")
    servicer = _StringDescr(doc="the servicer of the dataset shared by the token")
    dataset = _StringDescr(doc="the dataset shared by the token")
    project = _StringDescr(doc="the project of the dataset shared by the token")
    ttl = _IntDescr(doc="the remaining time in seconds until the token expires")

    _limit_setitem = [
        "token",
        "servicer",
        "dataset",
        "project",
        "ttl"
    ]

    def __init__(self, **token):
        self.__client = ted_client
        super().__init__(self, **token)

    @property
    def url(self) -> str:
        """
        Returns the URL that can be used to access a datset shared through Ted on the current environment

        Raises:
            requests.HTTPErrror for fault

        Returns:
            the URL to access the token in question
        """
        return '{api_host}/ted/api/v1/share/{token}/'.format(api_host=get_config().host, token=self.token)

    def update_ttl(self, ttl: int):
        """
        Update the time to live of a token in redis

        Args:
            ttl: the amount of seconds before the token should expire. Valid values are either -1,
                 representing an infinite token life, or n, where 0 < n <= 2147483647.

        Raises:
            requests.HTTPErrror for fault

        Note: If successful, nothing is returned.
        """
        res = raise_on_error(ted_client.patch(str(self.token) + '/' + str(ttl)))
        return

    def unshare(self):
        """
        Expires an active token created by the user, revoking access from anyone using the token

        Raises:
            requests.HTTPErrror for fault

        Note: If successful, nothing is returned. Deleting a non-existent token does not raise an error.
        """
        res = raise_on_error(ted_client.delete(str(self.token)))
        return


def get_tokens() -> List[Token]:
    """
    Returns all active tokens created by a user

    Raises:
        requests.HTTPErrror for fault
    """
    res = raise_on_error(ted_client.get(''))
    js = res.json()
    if js == {}:
        return []
    return [Token(**token) for token in js['tokens']]
