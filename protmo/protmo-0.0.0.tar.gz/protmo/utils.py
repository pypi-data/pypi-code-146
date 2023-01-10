import sys


def cap(s: str) -> str:
    if not s:
        return s
    return s[0].upper() + s[1:]


def print_sterr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
