import pytest
from typing import (
    TYPE_CHECKING,
)

from platon.datastructures import (
    AttributeDict,
)
from platon.types import (
    EnodeURI,
)

if TYPE_CHECKING:
    from platon import Web3


class GoPlatonAdminModuleTest:
    def test_add_peer(self, web3: "Web3") -> None:
        result = web3.node.admin.add_peer(
            EnodeURI('enode://f1a6b0bdbf014355587c3018454d070ac57801f05d3b39fe85da574f002a32e929f683d72aa5a8318382e4d3c7a05c9b91687b0d997a39619fb8a6e7ad88e512@1.1.1.1:30303'),)
        assert result is True

    def test_admin_datadir(self, web3: "Web3", datadir: str) -> None:
        result = web3.node.admin.data_dir()
        assert result == datadir

    def test_admin_node_info(self, web3: "Web3") -> None:
        result = web3.node.admin.node_info()
        expected = AttributeDict({
            'id': '',
            'name': '',
            'enode': '',
            'ip': '',
            'ports': AttributeDict({}),
            'listenAddr': '',
            'protocols': AttributeDict({})
        })
        # Test that result gives at least the keys that are listed in `expected`
        assert not set(expected.keys()).difference(result.keys())

    def test_admin_peers(self, web3: "Web3") -> None:
        enode = web3.node.admin.node_info()['enode']
        web3.node.admin.add_peer(enode)
        result = web3.node.admin.peers()
        assert len(result) == 1

    def test_admin_start_stop_rpc(self, web3: "Web3") -> None:
        stop = web3.node.admin.stop_rpc()
        assert stop is True

        start = web3.node.admin.start_rpc()
        assert start is True

    def test_admin_start_stop_ws(self, web3: "Web3") -> None:
        stop = web3.node.admin.stop_ws()
        assert stop is True

        start = web3.node.admin.start_ws()
        assert start is True
