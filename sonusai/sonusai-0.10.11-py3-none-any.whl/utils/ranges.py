from typing import List


def expand_range(s: str, sort: bool = True) -> List[int]:
    """Returns a list of integers from a string input representing a range."""
    import re

    clean_s = s.replace(':', '-')
    clean_s = clean_s.replace(';', ',')
    clean_s = re.sub(' +', ',', clean_s)
    clean_s = re.sub(',+', ',', clean_s)

    r = []
    for i in clean_s.split(','):
        if '-' not in i:
            r.append(int(i))
        else:
            l, h = map(int, i.split('-'))
            r += range(l, h + 1)

    if sort:
        r = sorted(r)

    return r


def consolidate_range(r: List[int]) -> str:
    """Returns a string representing a range from an input list of integers."""

    def ranges(i: List[int]) -> str:
        import itertools

        for a, b in itertools.groupby(enumerate(i), lambda pair: pair[1] - pair[0]):
            b = list(b)
            yield b[0][1], b[-1][1]

    ls = list(ranges(r))
    for idx, val in enumerate(ls):
        ls[idx] = f'{val[0]}'
        if val[0] != val[1]:
            ls[idx] += f'-{val[1]}'

    return ', '.join(ls)
