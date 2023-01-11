import logging
import sys
from typing import Sequence, TypeVar

T = TypeVar("T", bound=type)

logger = logging.getLogger("AutoEmbeddings")
if hasattr(sys, "ps1"):  # for python interactive mode
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(name)s - %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def is_list_of(lst: Sequence[object], tp: T) -> bool:
    return isinstance(lst, list) and all(isinstance(x, tp) for x in lst)
