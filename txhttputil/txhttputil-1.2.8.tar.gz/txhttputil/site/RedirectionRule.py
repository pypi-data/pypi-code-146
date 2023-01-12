class RedirectionRule:
    def __init__(self, origin: str = "", destination: str = ""):
        """A definition of Resource redirection rule
        :param str from: a source uri as in twisted.web.http.Request
        :param str to: a destination url.
        """
        self._origin: str = origin
        self._destination: str = destination

    @property
    def origin(self) -> bytes:
        return self._origin.encode()

    @property
    def destination(self) -> bytes:
        return self._destination.encode()