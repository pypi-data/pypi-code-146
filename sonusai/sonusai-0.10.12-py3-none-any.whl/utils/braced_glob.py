from typing import List


def expand_braces(text: str, seen: set = None) -> List[str]:
    import itertools
    import re

    if seen is None:
        seen = set()

    spans = [m.span() for m in re.finditer('\{[^\{\}]*\}', text)][::-1]
    alts = [text[start + 1: stop - 1].split(',') for start, stop in spans]

    if len(spans) == 0:
        if text not in seen:
            yield text
        seen.add(text)
    else:
        for combo in itertools.product(*alts):
            replaced = list(text)
            for (start, stop), replacement in zip(spans, combo):
                replaced[start:stop] = replacement
            yield from expand_braces(''.join(replaced), seen)


def braced_glob(path: str) -> List[str]:
    from glob import glob

    result = []
    for x in expand_braces(path):
        result.extend(glob(x))

    return result
