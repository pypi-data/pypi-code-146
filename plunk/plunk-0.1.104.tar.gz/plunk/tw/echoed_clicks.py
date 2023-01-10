from collections import deque
from itertools import islice
from functools import partial

from lined import Pipe  # pip install lined


def sliding_window(iterable, chk_size):
    # sliding_window('ABCDEFG', 4) -> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = deque(islice(it, chk_size), maxlen=chk_size)
    if len(window) == chk_size:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def streams_to_named_streams(*streams):
    """
    >>> stream_0 = [1, 2, 3, 4, 5, 6]
    >>> stream_1 = [-1, -2, -3, 0, -5, -6]
    >>> streams_to_named_streams(stream_0, stream_1)
    {0: [1, 2, 3, 4, 5, 6], 1: [-1, -2, -3, 0, -5, -6]}
    """
    return dict(enumerate(streams))


def interleaved_sliding_window_hunks(named_streams, chk_size):
    """
    >>> from functools import partial
    >>> hunker = partial(interleaved_sliding_window_hunks, chk_size=2)
    >>> named_streams = {0: [1, 2, 3, 4, 5, 6], 1: [-1, -2, -3, 0, -5, -6]}
    >>> assert list(hunker(named_streams)) == [
    ...     ((1, -1), (2, -2)),
    ...     ((2, -2), (3, -3)),
    ...     ((3, -3), (4, 0)),
    ...     ((4, 0), (5, -5)),
    ...     ((5, -5), (6, -6))
    ... ]


    """
    return sliding_window(zip(*named_streams.values()), chk_size)


def indexed_mapper(slabs, slab_func, indexer=enumerate):
    """
    >>> indexed_apply = partial(
    ...     indexed_mapper, slab_func=lambda x: x * 10, indexer=enumerate)
    >>> list(indexed_apply([-1, -2, -3, -4]))
    [(0, -10), (1, -20), (2, -30), (3, -40)]
    """
    for i, slab in indexer(slabs):
        func_result = slab_func(slab)
        yield i, func_result


stream_0 = [1, 2, 3, 4, 5, 6]
stream_1 = [-1, -2, -3, 0, -5, -6]
# list(event_detection_filter(click_channel_0, click_channel_1, min_lag=1, max_lag=1))


def mk_pipe(
    *, chk_size=1, slab_func=lambda x: x, filt=lambda x: True, indexer=enumerate
):
    return Pipe(
        streams_to_named_streams,
        hunker=partial(interleaved_sliding_window_hunks, chk_size=chk_size),
        indexed_tags=partial(indexed_mapper, slab_func=slab_func, indexer=indexer),
        user_filter=partial(filter, filt),
    )


def test_mk_pipe():
    p = mk_pipe(chk_size=2, slab_func=lambda x: any(map(sum, x)), indexer=enumerate)
    assert list(p(stream_0, stream_1)) == [
        (0, False),
        (1, False),
        (2, True),
        (3, True),
        (4, False),
    ]

    p = mk_pipe(
        chk_size=2, slab_func=lambda x: any(map(sum, x)), filt=lambda x: x[1] is True
    )

    assert list(p(stream_0, stream_1)) == [(2, True), (3, True)]


# test_mk_pipe()
