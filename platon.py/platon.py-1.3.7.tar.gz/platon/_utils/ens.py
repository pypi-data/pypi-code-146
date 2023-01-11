from contextlib import (
    contextmanager,
)
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterator,
    cast,
)

from platon_typing import (
    Bech32Address,
)
from platon_utils import (
    is_0x_prefixed,
    is_hex,
    is_hex_address,
    is_bech32_address,
)

from ens import ENS
from platon.exceptions import (
    NameNotFound,
)

if TYPE_CHECKING:
    from platon import Web3
    from platon.contract import (
        Contract,
    )


def is_ens_name(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    elif is_hex_address(value):
        return False
    elif is_0x_prefixed(value) and is_hex(value):
        return False
    elif is_bech32_address(value):
        return False
    else:
        return ENS.is_valid_name(value)


def validate_name_has_address(ens: ENS, name: str) -> Bech32Address:
    addr = ens.address(name)
    if addr:
        return addr
    else:
        raise NameNotFound("Could not find address for name %r" % name)


class StaticENS:
    def __init__(self, name_addr_pairs: Dict[str, Bech32Address]) -> None:
        self.registry = dict(name_addr_pairs)

    def address(self, name: str) -> Bech32Address:
        return self.registry.get(name, None)


@contextmanager
def ens_addresses(w3: "Web3", name_addr_pairs: Dict[str, Bech32Address]) -> Iterator[None]:
    original_ens = w3.ens
    w3.ens = cast(ENS, StaticENS(name_addr_pairs))
    yield
    w3.ens = original_ens


@contextmanager
def contract_ens_addresses(
    contract: "Contract", name_addr_pairs: Dict[str, Bech32Address]
) -> Iterator[None]:
    """
    Use this context manager to temporarily resolve name/address pairs
    supplied as the argument. For example:

    with contract_ens_addresses(mycontract, [('resolve-as-1s.platon', '0x111...111')]):
        # any contract call or transaction in here would only resolve the above ENS pair
    """
    with ens_addresses(contract.web3, name_addr_pairs):
        yield
