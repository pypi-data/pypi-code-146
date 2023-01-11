from typing import (
    Callable,
    List,
    Optional,
)

from platon_typing import (
    Bech32Address,
    HexStr,
)
from hexbytes import (
    HexBytes,
)

from platon._utils.compat import (
    Protocol,
)
from platon._utils.rpc_abi import (
    RPC,
)
from platon.method import (
    Method,
    default_root_munger,
)
from platon.types import (
    PnodeWallet,
    TxParams,
)

import_raw_key: Method[Callable[[str, str], Bech32Address]] = Method(
    RPC.personal_importRawKey,
    mungers=[default_root_munger],
)


new_account: Method[Callable[[str], Bech32Address]] = Method(
    RPC.personal_newAccount,
    mungers=[default_root_munger],
)


list_accounts: Method[Callable[[], List[Bech32Address]]] = Method(
    RPC.personal_listAccounts,
    mungers=None,
)


list_wallets: Method[Callable[[], List[PnodeWallet]]] = Method(
    RPC.personal_listWallets,
    mungers=None,
)


send_transaction: Method[Callable[[TxParams, str], HexBytes]] = Method(
    RPC.personal_sendTransaction,
    mungers=[default_root_munger],
)


lock_account: Method[Callable[[Bech32Address], bool]] = Method(
    RPC.personal_lockAccount,
    mungers=[default_root_munger],
)


class UnlockAccountWrapper(Protocol):
    def __call__(self, account: Bech32Address, passphrase: str,
                 duration: Optional[int] = None) -> bool:
        pass


unlock_account: Method[UnlockAccountWrapper] = Method(
    RPC.personal_unlockAccount,
    mungers=[default_root_munger],
)


sign: Method[Callable[[str, Bech32Address, Optional[str]], HexStr]] = Method(
    RPC.personal_sign,
    mungers=[default_root_munger],
)


# sign_typed_data: Method[Callable[[Dict[str, Any], Bech32Address, str], HexStr]] = Method(
#     RPC.personal_signTypedData,
#     mungers=[default_root_munger],
# )


ec_recover: Method[Callable[[str, HexStr], Bech32Address]] = Method(
    RPC.personal_ecRecover,
    mungers=[default_root_munger],
)

