from functools import (
    wraps,
)
from typing import (
    TYPE_CHECKING,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
)

from platon_typing import (
    Address,
    Bech32Address,
    HexAddress,
)
from platon_utils import (
    is_bech32_address,
    to_bech32_address,
)
from hexbytes import (
    HexBytes,
)

from ens import abis
from ens.constants import (
    EMPTY_ADDR_HEX,
    ENS_MAINNET_ADDR,
    REVERSE_REGISTRAR_DOMAIN,
)
from ens.exceptions import (
    AddressMismatch,
    UnauthorizedError,
    UnownedName,
)
from ens.utils import (
    address_in,
    address_to_reverse_domain,
    default,
    dict_copy,
    init_web3,
    is_none_or_zero_address,
    is_valid_name,
    label_to_hash,
    normal_name_to_hash,
    normalize_name,
    raw_name_to_hash,
)

if TYPE_CHECKING:
    from platon import Web3
    from platon.contract import (
        Contract,
    )
    from platon.providers import (
        BaseProvider,
    )
    from platon.types import (
        TxParams,
    )


class ENS:
    """
    Quick access to common Platon Name Service functions,
    like getting the address for a name.

    Unless otherwise specified, all addresses are assumed to be a `str` in
    `bech32 format, like: ``"lat1drz94my95tskswnrcnkdvnwq43n8jt6dmzf8h8"``
    """

    @staticmethod
    @wraps(label_to_hash)
    def labelhash(label: str) -> HexBytes:
        return label_to_hash(label)

    @staticmethod
    @wraps(raw_name_to_hash)
    def namehash(name: str) -> HexBytes:
        return raw_name_to_hash(name)

    @staticmethod
    @wraps(normalize_name)
    def nameprep(name: str) -> str:
        return normalize_name(name)

    @staticmethod
    @wraps(is_valid_name)
    def is_valid_name(name: str) -> bool:
        return is_valid_name(name)

    @staticmethod
    @wraps(address_to_reverse_domain)
    def reverse_domain(address: Bech32Address) -> str:
        return address_to_reverse_domain(address)

    def __init__(
        self, provider: 'BaseProvider' = cast('BaseProvider', default), addr: Bech32Address = None
    ) -> None:
        """
        :param provider: a single provider used to connect to Platon
        :type provider: instance of `platon.providers.base.BaseProvider`
        :param hex-string addr: the address of the ENS registry on-chain. If not provided,
            ENS.py will default to the mainnet ENS registry address.
        """
        self.web3 = init_web3(provider)

        ens_addr = addr if addr else ENS_MAINNET_ADDR
        self.ens = self.web3.platon.contract(abi=abis.ENS, address=ens_addr)
        self._resolverContract = self.web3.platon.contract(abi=abis.RESOLVER)

    @classmethod
    def fromWeb3(cls, web3: 'Web3', addr: Bech32Address = None) -> 'ENS':
        """
        Generate an ENS instance with platon

        :param `web3.Web3` web3: to infer connection information
        :param hex-string addr: the address of the ENS registry on-chain. If not provided,
            ENS.py will default to the mainnet ENS registry address.
        """
        return cls(web3.manager.provider, addr=addr)

    def address(self, name: str) -> Optional[Bech32Address]:
        """
        Look up the Platon address that `name` currently points to.

        :param str name: an ENS name to look up
        :raises InvalidName: if `name` has invalid syntax
        """
        return cast(Bech32Address, self.resolve(name, 'addr'))

    def name(self, address: Bech32Address) -> Optional[str]:
        """
        Look up the name that the address points to, using a
        reverse lookup. Reverse lookup is opt-in for name owners.

        :param address:
        :type address: hex-string
        """
        reversed_domain = address_to_reverse_domain(address)
        return self.resolve(reversed_domain, get='name')

    @dict_copy
    def setup_address(
        self,
        name: str,
        address: Union[Address, Bech32Address, HexAddress] = cast(Bech32Address, default),
        transact: "TxParams" = {}
    ) -> HexBytes:
        """
        Set up the name to point to the supplied address.
        The sender of the transaction must own the name, or
        its parent name.

        Example: If the caller owns ``parentname.platon`` with no subdomains
        and calls this method with ``sub.parentname.platon``,
        then ``sub`` will be created as part of this call.

        :param str name: ENS name to set up
        :param str address: name will point to this address, in bech32 format. If ``None``,
            erase the record. If not specified, name will point to the owner's address.
        :param dict transact: the transaction configuration, like in
            :meth:`~platon.platon.Platon.send_transaction`
        :raises InvalidName: if ``name`` has invalid syntax
        :raises UnauthorizedError: if ``'from'`` in `transact` does not own `name`
        """
        owner = self.setup_owner(name, transact=transact)
        self._assert_control(owner, name)
        if is_none_or_zero_address(address):
            address = None
        elif address is default:
            address = owner
        elif not is_bech32_address(address):
            raise ValueError("You must supply the address in bech32 format")
        if self.address(name) == address:
            return None
        if address is None:
            address = EMPTY_ADDR_HEX
        transact['from'] = owner
        resolver: 'Contract' = self._set_resolver(name, transact=transact)
        return resolver.functions.setAddr(raw_name_to_hash(name), address).transact(transact)

    @dict_copy
    def setup_name(
        self, name: str, address: Bech32Address = None, transact: "TxParams" = {}
    ) -> HexBytes:
        """
        Set up the address for reverse lookup, aka "caller ID".
        After successful setup, the method :meth:`~ens.main.ENS.name` will return
        `name` when supplied with `address`.

        :param str name: ENS name that address will point to
        :param str address: to set up, in bech32 format
        :param dict transact: the transaction configuration, like in
            :meth:`~platon.platon.send_transaction`
        :raises AddressMismatch: if the name does not already point to the address
        :raises InvalidName: if `name` has invalid syntax
        :raises UnauthorizedError: if ``'from'`` in `transact` does not own `name`
        :raises UnownedName: if no one owns `name`
        """
        if not name:
            self._assert_control(address, 'the reverse record')
            return self._setup_reverse(None, address, transact=transact)
        else:
            resolved = self.address(name)
            if is_none_or_zero_address(address):
                address = resolved
            elif resolved and address != resolved and resolved != EMPTY_ADDR_HEX:
                raise AddressMismatch(
                    "Could not set address %r to point to name, because the name resolves to %r. "
                    "To change the name for an existing address, call setup_address() first." % (
                        address, resolved
                    )
                )
            if is_none_or_zero_address(address):
                address = self.owner(name)
            if is_none_or_zero_address(address):
                raise UnownedName("claim subdomain using setup_address() first")
            if not is_bech32_address(address):
                raise ValueError("You must supply the address in bech32 format")
            self._assert_control(address, name)
            if not resolved:
                self.setup_address(name, address, transact=transact)
            return self._setup_reverse(name, address, transact=transact)

    def resolve(self, name: str, get: str = 'addr') -> Optional[Union[Bech32Address, str]]:
        normal_name = normalize_name(name)
        resolver = self.resolver(normal_name)
        if resolver:
            lookup_function = getattr(resolver.functions, get)
            namehash = normal_name_to_hash(normal_name)
            address = lookup_function(namehash).call()
            if is_none_or_zero_address(address):
                return None
            return lookup_function(namehash).call()
        else:
            return None

    def resolver(self, normal_name: str) -> Optional['Contract']:
        resolver_addr = self.ens.caller.resolver(normal_name_to_hash(normal_name))
        if is_none_or_zero_address(resolver_addr):
            return None
        return self._resolverContract(address=resolver_addr)

    def reverser(self, target_address: Bech32Address) -> Optional['Contract']:
        reversed_domain = address_to_reverse_domain(target_address)
        return self.resolver(reversed_domain)

    def owner(self, name: str) -> Bech32Address:
        """
        Get the owner of a name. Note that this may be different from the
        deed holder in the '.platon' registrar. Learn more about the difference
        between deed and name ownership in the ENS `Managing Ownership docs
        <http://docs.ens.domains/en/latest/userguide.html#managing-ownership>`_

        :param str name: ENS name to look up
        :return: owner address
        :rtype: str
        """
        node = raw_name_to_hash(name)
        return self.ens.caller.owner(node)

    @dict_copy
    def setup_owner(
        self,
        name: str,
        new_owner: Bech32Address = cast(Bech32Address, default),
        transact: "TxParams" = {}
    ) -> Bech32Address:
        """
        Set the owner of the supplied name to `new_owner`.

        For typical scenarios, you'll never need to call this method directly,
        simply call :meth:`setup_name` or :meth:`setup_address`. This method does *not*
        set up the name to point to an address.

        If `new_owner` is not supplied, then this will assume you
        want the same owner as the parent domain.

        If the caller owns ``parentname.platon`` with no subdomains
        and calls this method with ``sub.parentname.platon``,
        then ``sub`` will be created as part of this call.

        :param str name: ENS name to set up
        :param new_owner: account that will own `name`. If ``None``, set owner to empty addr.
            If not specified, name will point to the parent domain owner's address.
        :param dict transact: the transaction configuration, like in
            :meth:`~platon.platon.Platon.send_transaction`
        :raises InvalidName: if `name` has invalid syntax
        :raises UnauthorizedError: if ``'from'`` in `transact` does not own `name`
        :returns: the new owner's address
        """
        (super_owner, unowned, owned) = self._first_owner(name)
        if new_owner is default:
            new_owner = super_owner
        elif not new_owner:
            new_owner = Bech32Address(EMPTY_ADDR_HEX)
        else:
            new_owner = to_bech32_address(new_owner)
        current_owner = self.owner(name)
        if new_owner == EMPTY_ADDR_HEX and not current_owner:
            return None
        elif current_owner == new_owner:
            return current_owner
        else:
            self._assert_control(super_owner, name, owned)
            self._claim_ownership(new_owner, unowned, owned, super_owner, transact=transact)
            return new_owner

    def _assert_control(self, account: Bech32Address, name: str,
                        parent_owned: Optional[str] = None) -> None:
        if not address_in(account, self.web3.platon.accounts):
            raise UnauthorizedError(
                "in order to modify %r, you must control account %r, which owns %r" % (
                    name, account, parent_owned or name
                )
            )

    def _first_owner(self, name: str) -> Tuple[Optional[Bech32Address], Sequence[str], str]:
        """
        Takes a name, and returns the owner of the deepest subdomain that has an owner

        :returns: (owner or None, list(unowned_subdomain_labels), first_owned_domain)
        """
        owner = None
        unowned = []
        pieces = normalize_name(name).split('.')
        while pieces and is_none_or_zero_address(owner):
            name = '.'.join(pieces)
            owner = self.owner(name)
            if is_none_or_zero_address(owner):
                unowned.append(pieces.pop(0))
        return (owner, unowned, name)

    @dict_copy
    def _claim_ownership(
        self,
        owner: Bech32Address,
        unowned: Sequence[str],
        owned: str,
        old_owner: Bech32Address = None,
        transact: "TxParams" = {}
    ) -> None:
        transact['from'] = old_owner or owner
        for label in reversed(unowned):
            self.ens.functions.setSubnodeOwner(
                raw_name_to_hash(owned),
                label_to_hash(label),
                owner
            ).transact(transact)
            owned = "%s.%s" % (label, owned)

    @dict_copy
    def _set_resolver(
        self, name: str, resolver_addr: Bech32Address = None, transact: "TxParams" = {}
    ) -> 'Contract':
        if is_none_or_zero_address(resolver_addr):
            resolver_addr = self.address('resolver.platon')
        namehash = raw_name_to_hash(name)
        if self.ens.caller.resolver(namehash) != resolver_addr:
            self.ens.functions.setResolver(
                namehash,
                resolver_addr
            ).transact(transact)
        return self._resolverContract(address=resolver_addr)

    @dict_copy
    def _setup_reverse(
        self, name: str, address: Bech32Address, transact: "TxParams" = {}
    ) -> HexBytes:
        if name:
            name = normalize_name(name)
        else:
            name = ''
        transact['from'] = address
        return self._reverse_registrar().functions.setName(name).transact(transact)

    def _reverse_registrar(self) -> 'Contract':
        addr = self.ens.caller.owner(normal_name_to_hash(REVERSE_REGISTRAR_DOMAIN))
        return self.web3.platon.contract(address=addr, abi=abis.REVERSE_REGISTRAR)
