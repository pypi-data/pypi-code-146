from platon_typing import (
    Bech32Address,
    HexAddress,
    HexStr,
)
from platon_utils.address import (
    to_bech32_address
)
from hexbytes import (
    HexBytes,
)

ACCEPTABLE_STALE_HOURS = 48

AUCTION_START_GAS_CONSTANT = 25000
AUCTION_START_GAS_MARGINAL = 39000

EMPTY_SHA3_BYTES = HexBytes(b'\0' * 32)
EMPTY_ADDR_HEX = HexAddress(HexStr('0x' + '00' * 20))

REVERSE_REGISTRAR_DOMAIN = 'addr.reverse'

# todo: update ens address
ENS_MAINNET_ADDR = to_bech32_address(HexAddress(HexStr('0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e')), hrp='lat')
