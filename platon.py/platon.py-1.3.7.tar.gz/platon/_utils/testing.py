from typing import (
    Optional,
)

from platon._utils.rpc_abi import (
    RPC,
)
from platon.module import (
    Module,
)


class Testing(Module):

    def __getattribute__(self):
        raise ModuleNotFoundError('This module is not available')

    # def timeTravel(self, timestamp: int) -> None:
    #     return self.web3.manager.request_blocking(RPC.testing_timeTravel, [timestamp])
    #
    # def mine(self, num_blocks: int = 1) -> None:
    #     return self.web3.manager.request_blocking(RPC.evm_mine, [num_blocks])
    #
    # def snapshot(self) -> int:
    #     self.last_snapshot_idx = self.web3.manager.request_blocking(RPC.evm_snapshot, [])
    #     return self.last_snapshot_idx
    #
    # def reset(self) -> None:
    #     return self.web3.manager.request_blocking(RPC.evm_reset, [])
    #
    # def revert(self, snapshot_idx: Optional[int] = None) -> None:
    #     if snapshot_idx is None:
    #         revert_target = self.last_snapshot_idx
    #     else:
    #         revert_target = snapshot_idx
    #     return self.web3.manager.request_blocking(RPC.evm_revert, [revert_target])
