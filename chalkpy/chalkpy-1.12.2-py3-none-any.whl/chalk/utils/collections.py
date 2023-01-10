import collections.abc
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple, TypeVar, Union, cast, overload

T = TypeVar("T")


def flatten(v: Sequence[Union[T, Sequence[Union[T, Sequence[T]]]]]) -> List[T]:
    ret = []
    for x in v:
        if isinstance(x, collections.abc.Sequence) and not isinstance(x, (str, bytes, bytearray)):
            ret.extend(flatten(x))
        else:
            ret.append(x)
    return ret


@overload
def chunks(lst: List[T], n: int) -> Iterable[List[T]]:
    ...


@overload
def chunks(lst: Set[T], n: int) -> Iterable[Set[T]]:
    ...


@overload
def chunks(lst: Tuple[T, ...], n: int) -> Iterable[Tuple[T, ...]]:
    ...


@overload
def chunks(lst: Iterable[T], n: int) -> Iterable[Iterable[T]]:
    ...


def chunks(lst: Iterable[T], n: int) -> Iterable[Iterable[T]]:
    """Yield successive n-sized chunks from ``lst``, potentially lazily.

    Chunks are generated up-front if ``lst`` is a list, tuple, or set. In this case,
    the result will be an iterator of n-sized chunks of the underlying collection type.

    Otherwise, the chunks and the contents of each chunk are generated lazily, where at most one sample from ``lst`` is read in advance.

    Args:
        lst: The collection
        n: The chunk size. If <=0, then everything will be yielded back as one chunk.
    """
    if n <= 0:
        yield lst

    iterator = iter(lst)

    # Greedily loading the next sample to detect if we exhausted the iterable, so we don't yield an empty chunk at the end
    have_sample_to_yield = True
    try:
        next_sample = next(iterator)
    except StopIteration:
        have_sample_to_yield = False
        return

    def _get_chunk() -> Iterable[T]:
        """Get a chunk of size n from the generator, or raises StopIteration of the lst is empty"""
        nonlocal next_sample, have_sample_to_yield
        for _ in range(n):
            yield next_sample

            try:
                next_sample = next(iterator)
            except StopIteration:
                have_sample_to_yield = False
                break

    while have_sample_to_yield:
        chunk = _get_chunk()
        if isinstance(lst, (tuple, set, list)):
            # If the underlying collection is already allocated, then allocate the entire chunk at once
            # For backwards compatibility
            yield type(lst)(chunk)
        else:
            yield chunk


def flatten_sets(v: List[Set[T]]) -> Set[T]:
    return set().union(*v)


def ensure_tuple(x: Union[T, Sequence[T], Dict[Any, T], None]) -> Tuple[T, ...]:
    """Converts ``x`` into a tuple.
    * If ``x`` is ``None``, then ``tuple()`` is returned.
    * If ``x`` is a tuple, then ``x`` is returned as-is.
    * If ``x`` is a list, then ``tuple(x)`` is returned.
    * If ``x`` is a dict, then ``tuple(v for v in x.values())`` is returned.
    Otherwise, a single element tuple of ``(x,)`` is returned.
    Args:
        x (Any): The input to convert into a tuple.
    Returns:
        tuple: A tuple of ``x``.
    """
    # From https://github.com/mosaicml/composer/blob/020ca02e3848ee8fb6b7fff0c8123f597b05be8a/composer/utils/iter_helpers.py#L40
    if x is None:
        return ()
    if isinstance(x, (str, bytes, bytearray)):
        return (cast(T, x),)
    if isinstance(x, collections.abc.Sequence):
        return tuple(x)
    if isinstance(x, dict):
        return tuple(x.values())
    return (x,)


def get_unique_item(collection: Iterable[Optional[T]], name: str) -> T:
    item = None
    for x in collection:
        if x is None:
            raise ValueError(f"Item in {name} is None")
        if item is not None:
            if x != item:
                raise ValueError(f"Multiple values in {name} are not permitted. Found {x}, {item}")
        item = x
    if item is None:
        raise ValueError(f"There should be at least one item in {name}")
    return item
