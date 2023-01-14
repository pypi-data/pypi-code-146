import functools
import hashlib
import random
import string
from typing import Union


def rdm_str(n: int):
    seed = string.digits + string.ascii_letters
    return ''.join(random.choices(seed, k=n))


def md5(data: Union[str, bytes]) -> str:
    if isinstance(data, str):
        data = data.encode(encoding='utf-8')
    return hashlib.md5(data).hexdigest()


def ip_2_int(ip: str):
    # 先把 192.168.1.13 变成16进制的 c0.a8.01.0d ，再去了“.”后转成10进制的 3232235789 即可。
    # (((((192 * 256) + 168) * 256) + 1) * 256) + 13
    return functools.reduce(lambda x, y: (x << 8) + y, map(int, ip.split('.')))


__all__ = ('rdm_str', 'md5', 'ip_2_int')
