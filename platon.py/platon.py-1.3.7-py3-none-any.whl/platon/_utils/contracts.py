import functools

from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

from platon_abi.codec import (
    ABICodec, WasmABICodec,
)
from platon_abi.registry import (
    registry_wasm,
)
from platon_typing import (
    Bech32Address,
    HexStr,
)
from platon_utils import (
    add_0x_prefix,
    encode_hex,
    function_abi_to_4byte_selector,
    is_text,
)
from platon_utils.toolz import (
    pipe,
    valmap,
)
from hexbytes import (
    HexBytes,
)

from platon._utils.abi import (
    abi_to_signature,
    check_if_arguments_can_be_encoded,
    filter_by_argument_count,
    filter_by_argument_name,
    filter_by_encodability,
    filter_by_name,
    filter_by_type,
    get_abi_input_types,
    get_aligned_abi_inputs,
    get_fallback_func_abi,
    get_receive_func_abi,
    map_abi_data,
    merge_args_and_kwargs,
)
from platon._utils.encoding import (
    to_hex,
)
from platon._utils.function_identifiers import (
    FallbackFn,
    ReceiveFn,
)
from platon._utils.normalizers import (
    abi_address_to_bech32,
    abi_bytes_to_bytes,
    abi_ens_resolver,
    abi_string_to_text,
)
from platon.exceptions import (
    ValidationError,
)
from platon.types import (
    ABI,
    ABIEvent,
    ABIFunction,
    TxParams,
)

if TYPE_CHECKING:
    from platon import Web3


def find_matching_event_abi(
        abi: ABI, event_name: Optional[str] = None,
        argument_names: Optional[Sequence[str]] = None
) -> ABIEvent:
    filters = [
        functools.partial(filter_by_type, 'event'),
    ]

    if event_name is not None:
        filters.append(functools.partial(filter_by_name, event_name))

    if argument_names is not None:
        filters.append(
            functools.partial(filter_by_argument_name, argument_names)
        )

    event_abi_candidates = pipe(abi, *filters)

    if len(event_abi_candidates) == 1:
        return event_abi_candidates[0]
    elif not event_abi_candidates:
        raise ValueError("No matching events found")
    else:
        raise ValueError("Multiple events found")


def find_matching_fn_abi(
        abi: ABI,
        abi_codec: ABICodec = None,
        fn_identifier: Optional[Union[str, Type[FallbackFn], Type[ReceiveFn]]] = None,
        args: Optional[Sequence[Any]] = None,
        kwargs: Optional[Any] = None,
) -> ABIFunction:
    args = args or tuple()
    kwargs = kwargs or dict()
    num_arguments = len(args) + len(kwargs)

    if fn_identifier is FallbackFn:
        return get_fallback_func_abi(abi)

    if fn_identifier is ReceiveFn:
        return get_receive_func_abi(abi)

    if not is_text(fn_identifier):
        raise TypeError("Unsupported function identifier")

    name_filter = functools.partial(filter_by_name, fn_identifier)
    arg_count_filter = functools.partial(filter_by_argument_count, num_arguments)
    # todo: waiting for the completion of wasm codec
    if abi_codec:
        encoding_filter = functools.partial(filter_by_encodability, abi_codec, args, kwargs)
        function_candidates = pipe(abi, name_filter, arg_count_filter, encoding_filter)
    else:
        function_candidates = pipe(abi, name_filter, arg_count_filter)

    if len(function_candidates) == 1:
        return function_candidates[0]
    else:
        matching_identifiers = name_filter(abi)
        matching_function_signatures = [abi_to_signature(func) for func in matching_identifiers]

        arg_count_matches = len(arg_count_filter(matching_identifiers))
        if abi_codec:
            encoding_matches = len(encoding_filter(matching_identifiers))

        if arg_count_matches == 0:
            diagnosis = "\nFunction invocation failed due to improper number of arguments."
        elif abi_codec and encoding_matches == 0:
            diagnosis = "\nFunction invocation failed due to no matching argument types."
        elif abi_codec and encoding_matches > 1:
            diagnosis = (
                "\nAmbiguous argument encoding. "
                "Provided arguments can be encoded to multiple functions matching this call."
            )

        message = (
            "\nCould not identify the intended function with name `{name}`, "
            "positional argument(s) of type `{arg_types}` and "
            "keyword argument(s) of type `{kwarg_types}`."
            "\nFound {num_candidates} function(s) with the name `{name}`: {candidates}"
            "{diagnosis}"
        ).format(
            name=fn_identifier,
            arg_types=tuple(map(type, args)),
            kwarg_types=valmap(type, kwargs),
            num_candidates=len(matching_identifiers),
            candidates=matching_function_signatures,
            diagnosis=diagnosis,
        )

        raise ValidationError(message)


def encode_abi(web3: "Web3",
               vm_type: str,
               abi: ABIFunction,
               arguments: Sequence[Any],
               struct_dict: dict = None,
               data: Optional[HexStr] = None,
               ) -> HexStr:
    argument_types = get_abi_input_types(abi)

    # todo: Add arguments checker for wasm
    if vm_type == 'wasm':
        normalized_arguments = arguments
    else:
        if not check_if_arguments_can_be_encoded(abi, web3.codec, arguments, {}):
            raise TypeError(
                "One or more arguments could not be encoded to the necessary "
                "ABI type.  Expected types are: {0}".format(
                    ', '.join(argument_types),
                )
            )

        normalizers = [
            abi_ens_resolver(web3),
            abi_address_to_bech32,
            abi_bytes_to_bytes,
            abi_string_to_text,
        ]
        normalized_arguments = map_abi_data(
            normalizers,
            argument_types,
            arguments,
        )

    codec = web3.codec if vm_type != 'wasm' else WasmABICodec(registry_wasm)
    encoded_arguments = codec.encode_abi(
        argument_types,
        normalized_arguments,
        identifier=abi.get('name'),
        struct_dict=struct_dict,
        data=data,
    )

    return encode_hex(encoded_arguments)


def prepare_transaction(
        address: Bech32Address,
        web3: "Web3",
        vm_type: str,
        fn_identifier: Union[str, Type[FallbackFn], Type[ReceiveFn]],
        contract_abi: Optional[ABI] = None,
        fn_abi: Optional[ABIFunction] = None,
        transaction: Optional[TxParams] = None,
        fn_args: Optional[Sequence[Any]] = None,
        fn_kwargs: Optional[Any] = None,
) -> TxParams:
    """
    :parameter `is_function_abi` is used to distinguish  function abi from contract abi
    Returns a dictionary of the transaction that could be used to call this
    TODO: make this a public API
    TODO: add new prepare_deploy_transaction API
    """
    # todo: 支持wasm codec
    if fn_abi is None:
        fn_abi = find_matching_fn_abi(contract_abi, web3.codec, fn_identifier, fn_args, fn_kwargs)

    validate_payable(transaction, fn_abi)

    if transaction is None:
        prepared_transaction: TxParams = {}
    else:
        prepared_transaction = cast(TxParams, dict(**transaction))

    if 'data' in prepared_transaction:
        raise ValueError("Transaction parameter may not contain a 'data' key")

    if address:
        prepared_transaction.setdefault('to', address)

    prepared_transaction['data'] = encode_transaction_data(
        web3,
        vm_type,
        fn_identifier,
        contract_abi,
        fn_abi,
        fn_args,
        fn_kwargs,
    )
    return prepared_transaction


def encode_transaction_data(
        web3: "Web3",
        vm_type: str,
        fn_identifier: Union[str, Type[FallbackFn], Type[ReceiveFn]],
        contract_abi: Optional[ABI] = None,
        fn_abi: Optional[ABIFunction] = None,
        args: Optional[Sequence[Any]] = None,
        kwargs: Optional[Any] = None
) -> HexStr:
    if fn_identifier is FallbackFn:
        fn_abi, fn_selector, fn_arguments = get_fallback_function_info(contract_abi, fn_abi)
    elif fn_identifier is ReceiveFn:
        fn_abi, fn_selector, fn_arguments = get_receive_function_info(contract_abi, fn_abi)
    elif is_text(fn_identifier):
        fn_abi, fn_selector, fn_arguments = get_function_info(
            # type ignored b/c fn_id here is always str b/c FallbackFn is handled above
            fn_identifier, web3.codec, contract_abi, fn_abi, args, kwargs,  # type: ignore
        )
    else:
        raise TypeError("Unsupported function identifier")

    struct_dict = get_struct_dict(contract_abi)
    if vm_type == 'wasm':
        return add_0x_prefix(encode_abi(web3, vm_type, fn_abi, fn_arguments, struct_dict=struct_dict))

    return add_0x_prefix(encode_abi(web3, vm_type, fn_abi, fn_arguments, data=fn_selector))


def get_fallback_function_info(
        contract_abi: Optional[ABI] = None,
        fn_abi: Optional[ABIFunction] = None,
) -> Tuple[ABIFunction, HexStr, Tuple[Any, ...]]:
    if fn_abi is None:
        fn_abi = get_fallback_func_abi(contract_abi)
    fn_selector = encode_hex(b'')
    fn_arguments: Tuple[Any, ...] = tuple()
    return fn_abi, fn_selector, fn_arguments


def get_receive_function_info(
        contract_abi: Optional[ABI] = None,
        fn_abi: Optional[ABIFunction] = None,
) -> Tuple[ABIFunction, HexStr, Tuple[Any, ...]]:
    if fn_abi is None:
        fn_abi = get_receive_func_abi(contract_abi)
    fn_selector = encode_hex(b'')
    fn_arguments: Tuple[Any, ...] = tuple()
    return fn_abi, fn_selector, fn_arguments


def get_function_info(
        fn_name: str,
        abi_codec: ABICodec,
        contract_abi: Optional[ABI] = None,
        fn_abi: Optional[ABIFunction] = None,
        args: Optional[Sequence[Any]] = None,
        kwargs: Optional[Any] = None,
) -> Tuple[ABIFunction, HexStr, Tuple[Any, ...]]:
    if args is None:
        args = tuple()
    if kwargs is None:
        kwargs = {}

    if fn_abi is None:
        fn_abi = find_matching_fn_abi(contract_abi, abi_codec, fn_name, args, kwargs)

    # typed dict cannot be used w/ a normal Dict
    # https://github.com/python/mypy/issues/4976
    fn_selector = encode_hex(function_abi_to_4byte_selector(fn_abi))  # type: ignore

    fn_arguments = merge_args_and_kwargs(fn_abi, args, kwargs)

    _, aligned_fn_arguments = get_aligned_abi_inputs(fn_abi, fn_arguments)

    return fn_abi, fn_selector, aligned_fn_arguments


def get_struct_dict(contract_abi: Optional[ABI] = None):
    return {abi['name']: abi for abi in contract_abi if abi['type'] == 'struct'}


def validate_payable(transaction: TxParams, abi: ABIFunction) -> None:
    """Raise ValidationError if non-zero ether
    is sent to a non payable function.
    """
    if 'value' in transaction:
        if transaction['value'] != 0:
            if "payable" in abi and not abi["payable"]:
                raise ValidationError(
                    "Sending non-zero ether to a contract function "
                    "with payable=False. Please ensure that "
                    "transaction's value is 0."
                )
