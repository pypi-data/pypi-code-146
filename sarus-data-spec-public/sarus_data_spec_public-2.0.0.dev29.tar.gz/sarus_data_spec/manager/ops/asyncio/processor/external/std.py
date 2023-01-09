from typing import Any


async def add(val_1: Any, val_2: Any) -> Any:
    return val_1 + val_2


async def sub(val_1: Any, val_2: Any) -> Any:
    return val_1 - val_2


async def rsub(val_1: Any, val_2: Any) -> Any:
    return val_2 - val_1


async def mul(val_1: Any, val_2: Any) -> Any:
    return val_1 * val_2


async def div(val_1: Any, val_2: Any) -> Any:
    return val_1 / val_2


async def rdiv(val_1: Any, val_2: Any) -> Any:
    return val_2 / val_1


async def invert(val: Any) -> Any:
    return ~val


async def length(val: Any) -> Any:
    return len(val)


async def getitem(val: Any, key: Any) -> Any:
    return val[key]


async def setitem(val: Any, key: Any, newvalue: Any) -> Any:
    val.__setitem__(key, newvalue)
    return val


async def greater_than(val_1: Any, val_2: Any) -> Any:
    return val_1 > val_2


async def greater_equal(val_1: Any, val_2: Any) -> Any:
    return val_1 >= val_2


async def lower_than(val_1: Any, val_2: Any) -> Any:
    return val_1 < val_2


async def lower_equal(val_1: Any, val_2: Any) -> Any:
    return val_1 <= val_2


async def not_equal(val_1: Any, val_2: Any) -> Any:
    return val_1 != val_2


async def neg(val_1: Any) -> Any:
    return -val_1


async def pos(val_1: Any) -> Any:
    return +val_1


async def _abs(val_1: Any) -> Any:
    return abs(val_1)


async def _round(*args: Any, **kwargs: Any) -> Any:
    return round(*args, **kwargs)


async def modulo(val_1: Any, val_2: Any) -> Any:
    return val_1 % val_2


async def rmodulo(val_1: Any, val_2: Any) -> Any:
    return val_2 % val_1


async def _or(val_1: Any, val_2: Any) -> Any:
    return val_1 | val_2


async def ror(val_1: Any, val_2: Any) -> Any:
    return val_2 | val_1


async def _and(val_1: Any, val_2: Any) -> Any:
    return val_1 & val_2


async def rand(val_1: Any, val_2: Any) -> Any:
    return val_2 & val_1


async def _int(*args: Any, **kwargs: Any) -> Any:
    return int(*args, **kwargs)


async def _float(*args: Any, **kwargs: Any) -> Any:
    return float(*args, **kwargs)


async def _list(*args: Any, **kwargs: Any) -> Any:
    return list(args)


async def _dict(*args: Any, **kwargs: Any) -> Any:
    return dict(kwargs)


async def _slice(*args: Any, **kwargs: Any) -> Any:
    return slice(*args, **kwargs)


async def _set(*args: Any, **kwargs: Any) -> Any:
    return set(args)


async def _tuple(*args: Any, **kwargs: Any) -> Any:
    return tuple(args)


async def keys(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    return list(parent_val.keys(*args, **kwargs))


async def values(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    return list(parent_val.values(*args, **kwargs))


async def sudo(val: Any) -> Any:
    return val


async def extend(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    parent_val.extend(*args, **kwargs)
    return parent_val


async def append(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    parent_val.append(*args, **kwargs)
    return parent_val


async def pop(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    return parent_val.pop(*args, **kwargs)
