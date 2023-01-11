import pytest
from typing import (
    TYPE_CHECKING,
)

from platon_utils import (
    is_string,
)

if TYPE_CHECKING:
    from platon import Web3


class VersionModuleTest:
    def test_platon_protocol_version(self, web3: "Web3") -> None:
        with pytest.warns(DeprecationWarning):
            protocol_version = web3.platon.protocol_version

        assert is_string(protocol_version)
        assert protocol_version.isdigit()

    def test_platon_protocolVersion(self, web3: "Web3") -> None:
        with pytest.warns(DeprecationWarning):
            protocol_version = web3.platon.protocolVersion

        assert is_string(protocol_version)
        assert protocol_version.isdigit()
