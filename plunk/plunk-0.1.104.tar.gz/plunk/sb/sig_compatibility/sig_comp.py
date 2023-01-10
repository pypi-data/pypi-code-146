from dataclasses import dataclass
from typing import Optional
from collections import Counter
from i2 import Sig
from i2.signatures import PK, VP, VK, PO, KO
from inspect import getcallargs
from typing import List
from i2.tests.util import sig_to_inputs
from i2.signatures import var_param_kinds


kind_to_symbol = {PO: 'PO', PK: 'PK', VP: 'VP', KO: 'KO', VK: 'VK'}


def transform_key(d, func):
    return {func(k): v for k, v in d.items()}


def param_kind_counter_for_func(func):
    sig = Sig(func)
    param_list = [param.kind for param in sig.parameters.values()]
    cc = Counter(param_list)
    res = transform_key(dict(cc), kind_to_symbol_func)
    return res


def kind_to_symbol_func(k):
    return kind_to_symbol[k]


@dataclass
class DefinitionSig:
    PO: Optional[int] = 0
    PK: Optional[int] = 0
    VP: Optional[int] = 0
    KO: Optional[int] = 0
    VK: Optional[int] = 0


@dataclass
class CallSig:
    pos: int = 0
    k: int = 0


def region_type(d: DefinitionSig) -> int:
    """Classifies a definition sig into 4 types

    Args:
        d (DefinitionSig)

    Returns:
        int: an integer in [0,1,2,3]
    """
    vp, vk = d.VP, d.VK
    return 2 * vk + vp


def point_is_in_region(point, segment, region_type) -> bool:
    """Check whether a point is in an (infinite) region
       defined by a segment and a region type

    Args:
        point: Tuple[int, int]
        segment: List[point]
        region_type: int

    Returns:
        bool : is in region or not
    """
    x, y = point
    po, pk, ko = segment

    if region_type == 0:
        return po <= x <= po + pk and x + y == sum(list(segment))
    if region_type == 1:
        return ko + pk >= y >= ko and x + y >= sum(list(segment))
    if region_type == 2:
        return po <= x <= po + pk and x + y >= sum(list(segment))
    if region_type == 3:
        return x >= po and y >= ko and x + y >= sum(list(segment))


def segment_is_in_region(segment_1, segment_2, region_type):
    po_1, pk_1, ko_1 = segment_1
    point_a = (po_1, pk_1 + ko_1)
    point_b = (po_1 + pk_1, ko_1)

    cond_a = point_is_in_region(point_a, segment_2, region_type)
    cond_b = point_is_in_region(point_b, segment_2, region_type)

    return cond_a and cond_b


def segment_from_definition_sig(d: DefinitionSig):
    segment = (d.PO, d.PK, d.KO)
    return segment


def is_compatible_with(d: DefinitionSig, e: DefinitionSig):
    """Check whether ways of calling a function having a given signature,
    are allowed for the second signature. Names of the variables are not checked.

    """
    region_type_d = region_type(d)
    region_type_e = region_type(e)
    if (region_type_d, region_type_e) in [
        (1, 2),
        (2, 1),
        (1, 0),
        (2, 0),
        (3, 0),
        (3, 1),
        (3, 2),
    ]:
        return False

    segment_d = segment_from_definition_sig(d)
    segment_e = segment_from_definition_sig(e)
    return segment_is_in_region(segment_d, segment_e, region_type_e)


def call_is_compatible(d: DefinitionSig, c=CallSig):
    """Check is a particular way of calling a function having signature size d is allowed"""
    point_c = (c.pos, c.k)
    region_type_d = region_type(d)
    segment_d = segment_from_definition_sig(d)

    cond = point_is_in_region(point_c, segment_d, region_type_d)

    return cond


def invert_dict(d):
    inv_map = {}
    for k, v in d.items():
        inv_map[v] = inv_map.get(v, []) + [k]
    return inv_map


def var_names_by_kind(sig):
    d = invert_dict(sig.kinds)
    func = kind_to_symbol_func
    result = transform_key(d, func)
    return result


def sig_to_func(sig):  # check Thor's function
    @Sig(sig)
    def func(*args, **kwargs):
        return args, kwargs

    return func


def args_compatible_with_sig(sig, *args, **kwargs):
    func = sig_to_func(sig)
    return getcallargs(func, *args, **kwargs)


def possible_named_args(sig):
    d = var_names_by_kind(sig)
    print(d)
    return d.get('PK', []) + d.get('KO', [])


def named_args_are_valid(named_args1: List[str], vk2: int, named_args2: List[str]):
    if vk2 > 0:
        return True
    excess = set(named_args1) - set(named_args2)
    if excess:
        ValueError(
            f'The following named arguments cannot be accepted by the second function: {excess}'
        )
    else:
        return True


def is_compatible_func(f, g):
    sig1 = Sig(f)
    sig2 = Sig(g)
    named_args1 = possible_named_args(sig1)
    named_args2 = possible_named_args(sig2)
    vk2 = param_kind_counter(g).get('VK', 0)

    d1 = DefinitionSig(**param_kind_counter(sig1))
    d2 = DefinitionSig(**param_kind_counter(sig2))

    named_cond = named_args_are_valid(named_args1, vk2, named_args2)
    arg_count_cond = is_compatible_with(d1, d2)

    return named_cond and arg_count_cond


def sig_to_func(sig):  # check Thor's function: could not find it
    @Sig(sig)
    def func(*args, **kwargs):
        return args, kwargs

    return func


def variadic_compatibility(vp1, vp2, vk1, vk2):
    # True False or None: much better
    # early_return = False
    early_result = None
    if vp1 and not vp2:
        # early_return = True
        early_result = False
    if vk1 and not vk2:
        # early_return = True
        early_result = False
    # if vp2 and vk2:
    #    early_return = True
    #    early_result = True

    return early_result


def param_kind_counter(sig):
    param_list = [param.kind for param in sig.parameters.values()]
    cc = Counter(param_list)
    res = transform_key(dict(cc), kind_to_symbol_func)
    return res


def kind_to_symbol_func(k):
    return kind_to_symbol[k]


def variadics_from_sig(sig):
    d = param_kind_counter(sig)
    vp = 'VP' in d
    vk = 'VK' in d

    return vp, vk


def is_valid_input_for_func(func, input):
    args, kwargs = input
    try:
        func(*args, **kwargs)
        return True
    except TypeError:
        return False


def remove_variadics_from_sig(sig):
    non_variadics_params = [
        param for param in sig.params if param.kind not in var_param_kinds
    ]
    new_sig = Sig.from_params(non_variadics_params)

    return new_sig


def comp(sig1, sig2):  # <= __leq__
    vp1, vk1 = variadics_from_sig(sig1)  # example: (True, False)
    vp2, vk2 = variadics_from_sig(sig2)

    early_result = variadic_compatibility(vp1, vp2, vk1, vk2)
    if early_result is not None:  # early_result := not None etc...
        return early_result

    new_sig1 = remove_variadics_from_sig(sig1)
    new_sig2 = remove_variadics_from_sig(sig2)
    func1 = sig_to_func(new_sig1)
    func2 = sig_to_func(new_sig2)
    inputs = sig_to_inputs(new_sig1)
    # assert valid for func1 !
    is_valid = all([is_valid_input_for_func(func2, input) for input in inputs])

    return is_valid
