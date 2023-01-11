import decimal
from platon_abi.codec import (
    ABICodec,
)
from platon_utils import (
    add_0x_prefix,
    apply_to_return_value,
    from_von,
    keccak as platon_utils_keccak,
    remove_0x_prefix,
    to_bytes,
    to_int,
    to_text,
    to_von,
    is_bech32_address,
    to_bech32_address,
    is_checksum_address,
    to_checksum_address
)
from functools import (
    wraps,
)
from hexbytes import (
    HexBytes,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Sequence,
    TYPE_CHECKING,
    Union,
    cast,
)

from platon_typing import (
    AnyAddress,
    HexStr,
    Primitives,
)
from platon_typing.abi import TypeStr
from platon_utils import (
    combomethod,
)

from ens import ENS
from platon._utils.abi import (
    build_default_registry,
    build_strict_registry,
    map_abi_data,
)
from platon._utils.empty import (
    empty,
)
from platon._utils.encoding import (
    hex_encode_abi_type,
    to_hex,
    to_json,
)
from platon._utils.rpc_abi import (
    RPC,
)
from platon._utils.module import (
    attach_modules,
)
from platon._utils.normalizers import (
    abi_ens_resolver,
)

from platon._utils.delegate import (
    Delegate,
)
from platon.debug import (
    Debug,
)
from platon.pip import (
    Pip,
)
from platon.restricting import (
    Restricting,
)
from platon._utils.slashing import (
    Slashing,
)
from platon._utils.staking import (
    Staking,
)
from platon.platon import (
    Platon,
)
from platon.node import (
    Node,
    Admin,
    Miner,
    Personal,
    TxPool,
)
from platon.iban import (
    Iban,
)
from platon.manager import (
    RequestManager as DefaultRequestManager,
)
from platon.net import (
    Net,
)
from platon.ppos import Ppos
from platon.providers import (
    BaseProvider, AutoProvider,
)
from platon.providers.platon_tester import (
    PlatonTesterProvider,
)
from platon.providers.ipc import (
    IPCProvider,
)
from platon.providers.async_rpc import (
    AsyncHTTPProvider,
)
from platon.providers.rpc import (
    HTTPProvider,
)
from platon.providers.websocket import (
    WebsocketProvider,
)
from platon.types import (
    MiddlewareOnion,
    Von,
)
from platon.version import (
    Version,
)

if TYPE_CHECKING:
    from platon.pm import PM


def get_default_modules() -> Dict[str, Sequence[Any]]:
    return {
        "platon": (Platon,),
        "net": (Net,),
        "version": (Version,),
        "restricting": (Restricting,),
        "ppos": (Ppos, {
            "staking": (Staking,),
            "delegate": (Delegate,),
            "slashing": (Slashing, ),
        }),
        "pip": (Pip, ),
        "node": (Node, {
            "admin": (Admin,),
            "miner": (Miner,),
            "personal": (Personal,),
            "txpool": (TxPool,),
        }),
        # "parity": (Parity, {
        #     "personal": (ParityPersonal,),
        # }),
        # "testing": (Testing,),
        "debug": (Debug, ),
    }


class Web3:
    # Providers
    HTTPProvider = HTTPProvider
    IPCProvider = IPCProvider
    PlatonTesterProvider = PlatonTesterProvider
    WebsocketProvider = WebsocketProvider
    AsyncHTTPProvider = AsyncHTTPProvider

    # Managers
    RequestManager = DefaultRequestManager

    # Iban
    Iban = Iban

    # Encoding and Decoding
    @staticmethod
    @wraps(to_bytes)
    def toBytes(
            primitive: Primitives = None, hexstr: HexStr = None, text: str = None
    ) -> bytes:
        return to_bytes(primitive, hexstr, text)

    @staticmethod
    @wraps(to_int)
    def toInt(
            primitive: Primitives = None, hexstr: HexStr = None, text: str = None
    ) -> int:
        return to_int(primitive, hexstr, text)

    @staticmethod
    @wraps(to_hex)
    def toHex(
            primitive: Primitives = None, hexstr: HexStr = None, text: str = None
    ) -> HexStr:
        return to_hex(primitive, hexstr, text)

    @staticmethod
    @wraps(to_text)
    def toText(
            primitive: Primitives = None, hexstr: HexStr = None, text: str = None
    ) -> str:
        return to_text(primitive, hexstr, text)

    @staticmethod
    @wraps(to_json)
    def toJSON(obj: Dict[Any, Any]) -> str:
        return to_json(obj)

    # Currency Utility
    @staticmethod
    @wraps(to_von)
    def toVon(number: Union[int, float, str, decimal.Decimal], unit: str) -> Von:
        return cast(Von, to_von(number, unit))

    @staticmethod
    @wraps(from_von)
    def fromVon(number: int, unit: str) -> Union[int, decimal.Decimal]:
        return from_von(number, unit)

    # Address Utility
    @staticmethod
    def is_bech32_address(value: Any):
        return is_bech32_address(value)

    @staticmethod
    def to_bech32_address(value: Union[AnyAddress, str, bytes], hrp: str):
        return to_bech32_address(value, hrp)

    @staticmethod
    def is_checksum_address(value: Any):
        return is_checksum_address(value)

    @staticmethod
    def to_checksum_address(value: Union[AnyAddress, str, bytes], hrp: str):
        return to_checksum_address(value, hrp)

    # mypy Types
    platon: Platon
    net: Net
    version: Version
    restricting: Restricting
    ppos: Ppos
    pip: Pip
    node: Node
    # parity: Parity
    debug: Debug

    def __init__(
            self,
            provider: Optional[BaseProvider] = None,
            middlewares: Optional[Sequence[Any]] = None,
            modules: Optional[Dict[str, Sequence[Any]]] = None,
            ens: ENS = cast(ENS, empty),
            chain_id: int = None,  # This value is required for versions earlier than 0.16.0
            hrp: str = None  # This value is required for versions earlier than 0.13.2
    ) -> None:
        if provider is None:
            provider = AutoProvider()

        self.manager = self.RequestManager(self, provider, middlewares)
        # this codec gets used in the module initialization,
        # so it needs to come before attach_modules
        self.codec = ABICodec(build_default_registry())

        if modules is None:
            modules = get_default_modules()

        attach_modules(self, modules)

        self.ens = ens

        self._chain_id = chain_id

        self._hrp = hrp

    @property
    def chain_id(self):
        if self._chain_id is None:
            self._chain_id = self.platon.chain_id

        return self._chain_id

    @property
    def hrp(self):
        if self._hrp is None:
            self._hrp = self.platon.get_address_hrp()

        return self._hrp

    @property
    def middleware_onion(self) -> MiddlewareOnion:
        return self.manager.middleware_onion

    @property
    def provider(self) -> BaseProvider:
        return self.manager.provider

    @provider.setter
    def provider(self, provider: BaseProvider) -> None:
        self.manager.provider = provider

    @property
    def clientVersion(self) -> str:
        return self.manager.request_blocking(RPC.web3_clientVersion, [])

    @property
    def api(self) -> str:
        from platon import __version__
        return __version__

    @staticmethod
    @apply_to_return_value(HexBytes)
    def keccak(primitive: Optional[Primitives] = None, text: Optional[str] = None,
               hexstr: Optional[HexStr] = None) -> bytes:
        if isinstance(primitive, (bytes, int, type(None))):
            input_bytes = to_bytes(primitive, hexstr=hexstr, text=text)
            return platon_utils_keccak(input_bytes)

        raise TypeError(
            "You called keccak with first arg %r and keywords %r. You must call it with one of "
            "these approaches: keccak(text='txt'), keccak(hexstr='0x747874'), "
            "keccak(b'\\x74\\x78\\x74'), or keccak(0x747874)." % (
                primitive,
                {'text': text, 'hexstr': hexstr}
            )
        )

    @combomethod
    def solidityKeccak(cls, abi_types: List[TypeStr], values: List[Any]) -> bytes:
        """
        Executes keccak256 exactly as Solidity does.
        Takes list of abi_types as inputs -- `[uint24, int8[], bool]`
        and list of corresponding values  -- `[20, [-1, 5, 0], True]`
        """
        if len(abi_types) != len(values):
            raise ValueError(
                "Length mismatch between provided abi types and values.  Got "
                "{0} types and {1} values.".format(len(abi_types), len(values))
            )

        if isinstance(cls, type):
            w3 = None
        else:
            w3 = cls
        normalized_values = map_abi_data([abi_ens_resolver(w3)], abi_types, values)

        hex_string = add_0x_prefix(HexStr(''.join(
            remove_0x_prefix(hex_encode_abi_type(abi_type, value))
            for abi_type, value
            in zip(abi_types, normalized_values)
        )))
        return cls.keccak(hexstr=hex_string)

    def isConnected(self) -> bool:
        return self.provider.isConnected()

    def is_encodable(self, _type: TypeStr, value: Any) -> bool:
        return self.codec.is_encodable(_type, value)

    @property
    def ens(self) -> ENS:
        if self._ens is cast(ENS, empty):
            return ENS.fromWeb3(self)
        else:
            return self._ens

    @ens.setter
    def ens(self, new_ens: ENS) -> None:
        self._ens = new_ens

    @property
    def pm(self) -> "PM":
        if hasattr(self, '_pm'):
            # ignored b/c property is dynamically set via enable_unstable_package_management_api
            return self._pm  # type: ignore
        else:
            raise AttributeError(
                "The Package Management feature is disabled by default until "
                "its API stabilizes. To use these features, please enable them by running "
                "`w3.enable_unstable_package_management_api()` and try again."
            )

    def enable_unstable_package_management_api(self) -> None:
        from platon.pm import PM
        if not hasattr(self, '_pm'):
            attach_modules(self, {'_pm': (PM,)})

    def enable_strict_bytes_type_checking(self) -> None:
        self.codec = ABICodec(build_strict_registry())
