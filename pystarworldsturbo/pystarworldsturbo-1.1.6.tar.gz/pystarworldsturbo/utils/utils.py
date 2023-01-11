from os import devnull
from typing import Any, Iterable, Iterator


def ignore(obj: Any) -> None:
    if not obj:
        return
    elif isinstance(obj, (Iterable, Iterator)):
        for elm in obj:
            ignore(elm)
    else:
        with open(devnull, "w") as f:
            f.write(str(obj))
            f.flush()
