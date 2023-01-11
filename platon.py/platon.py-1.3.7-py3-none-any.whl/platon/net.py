from platon._utils.net import (
    listening,
    peer_count,
    version,
)
from platon.module import (
    Module,
)


class Net(Module):
    _listening = listening
    _peer_count = peer_count
    _version = version

    @property
    def listening(self) -> bool:
        return self._listening()

    @property
    def peer_count(self) -> int:
        return self._peer_count()

    @property
    def version(self) -> str:
        return self._version()
