from collections import defaultdict
from functools import wraps, partial, reduce
from io import BytesIO
from itertools import chain
from math import ceil
from operator import itemgetter
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import (
    Callable,
    MutableMapping,
    Protocol,
    Iterator,
    DefaultDict,
    List,
)
from wave import Wave_write

from dol import appendable, Files, wrap_kvs
from i2 import Sig
from mongodol.tracking_methods import (
    track_method_calls,
    TrackableMixin,
)
from recode import (
    encode_pcm_bytes,
    decode_wav_bytes,
)


class BulkStore(Protocol):
    """Mutable Mapping with Append Method"""

    def append(self, item):
        pass

    def __setitem__(self, __k, __v) -> None:
        pass

    def __delitem__(self, __v) -> None:
        pass

    def __getitem__(self, __k):
        pass

    def __len__(self) -> int:
        pass

    def __iter__(self) -> Iterator:
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


audio_slab_kv = itemgetter('timestamp', 'wf')


N_TO_BULK = 10


def merge_append_ts_wf(items: List[dict]):
    """Take a list of kwargs for method append(item) and return a single kwargs

    :param items: [{'item': {'timestamp': 0, 'wf': [0, 0]}},
                   {'item': {'timestamp': 1, 'wf': [1, 1]}},
                   ...]
    :return: {'item': {'timestamp': 0, 'wf': [0, 0, 1, 1, ...]}}
    """
    ts = items[0]['item']['timestamp']
    joined_wf = list(
        chain.from_iterable(
            map(
                partial(
                    reduce, lambda x, y: y(x), (itemgetter('item'), itemgetter('wf')),
                ),
                items,
            )
        )
    )
    return {'item': {'timestamp': ts, 'wf': joined_wf}}


class CountMergeExecute(TrackableMixin):
    """Make tracks factory count method calls when order of different methods is not important.
    Apply a merging method to join all arguments before executing tracked method once.
    """

    tracks_factory: DefaultDict[Callable, List[tuple]] = partial(defaultdict, list)

    _MERGE_KWARGS_MAP = {'append': merge_append_ts_wf}

    def _execute_method_tracks(self, method: Callable):
        if merge_kwargs_method := self._MERGE_KWARGS_MAP.get(method.__name__):
            sig = Sig(method)
            kwargs_list = [
                sig.kwargs_from_args_and_kwargs((self, *a), kw)
                for a, kw in self._tracks[method]
            ]
            merged_kwargs = merge_kwargs_method(kwargs_list)
            method(self, **merged_kwargs)
        else:
            for args, kwargs in self._tracks[method]:
                method(self, *args, **kwargs)

    def _execute_tracks(self):
        for method in self._tracks:
            self._execute_method_tracks(method)


def track_n_calls_of_method_then_execute(method: Callable, n_calls=N_TO_BULK):
    @wraps(method)
    def tracked_method(self: CountMergeExecute, *args, **kwargs):
        self._tracks[method].append((args, kwargs))
        if len(self._tracks[method]) >= n_calls:
            self._execute_method_tracks(method)
            del self._tracks[method]

    return tracked_method


def merge_and_write_upon_count(
    store_cls: MutableMapping = None,
    *,
    tracked_methods='append',
    tracking_mixin=CountMergeExecute,
    tracking_merge_map=None,
    calls_tracker=track_n_calls_of_method_then_execute,
    n_calls_to_execute=N_TO_BULK,
    item2kv=audio_slab_kv,
    key_of_id=None,
    id_of_key=None,
    obj_of_data=None,
    data_of_obj=None,
):
    """Equivalent of using the following 3 decorators

    @track_method_calls(
        tracked_methods='append',
        tracking_mixin=CountMergeExecute,
        calls_tracker=track_n_calls_of_method_then_execute,
    )
    @appendable(item2kv=audio_slab_kv)
    @wrap_kvs(
        key_of_id=filename_to_ts,
        id_of_key=ts_to_filename,
        obj_of_data=wav_to_wf,
        data_of_obj=wf_to_wav,
    )
    class WavFileStore(Files, BulkStore):
        pass

    :param store_cls:
    :param tracked_methods:
    :param tracking_mixin:
    :param tracking_merge_map:
    :param calls_tracker:
    :param n_calls_to_execute:
    :param item2kv:
    :param key_of_id:
    :param id_of_key:
    :param obj_of_data:
    :param data_of_obj:
    :return:
    """

    def _decorator(cls):
        if isinstance(tracking_merge_map, MutableMapping):
            _tracking_mixin = type(
                tracking_mixin.__name__,
                (tracking_mixin,),
                {'_MERGE_KWARGS_MAP': tracking_merge_map},
            )
        else:
            _tracking_mixin = tracking_mixin

        return track_method_calls(
            appendable(
                wrap_kvs(
                    cls,
                    key_of_id=key_of_id,
                    id_of_key=id_of_key,
                    obj_of_data=obj_of_data,
                    data_of_obj=data_of_obj,
                ),
                item2kv=item2kv,
            ),
            tracked_methods=tracked_methods,
            tracking_mixin=_tracking_mixin,
            calls_tracker=partial(calls_tracker, n_calls=n_calls_to_execute),
        )

    return _decorator(store_cls) if callable(store_cls) else _decorator


def ts_to_filename(ts, ext='.wav'):
    return f'{ts}{ext}'


def filename_to_ts(name, ext='.wav'):
    return int(name[: -len(ext)])


def wf_to_wav(
    wf, sr: int = 44100, width_bytes: int = 2, *, n_channels: int = 1
) -> bytes:
    bio = BytesIO()
    with Wave_write(bio) as obj:
        obj.setparams((n_channels, width_bytes, sr, 0, 'NONE', 'not compressed'))
        wf_bytes = encode_pcm_bytes(wf, width=width_bytes * 8, n_channels=n_channels)
        obj.writeframes(wf_bytes)
        bio.seek(0)
    return bio.read()


def wav_to_wf(wav):
    wf, sr = decode_wav_bytes(wav)
    return wf


@merge_and_write_upon_count(
    key_of_id=filename_to_ts,
    id_of_key=ts_to_filename,
    obj_of_data=wav_to_wf,
    data_of_obj=wf_to_wav,
)
class WavFileStore(Files, BulkStore):
    pass


def _test_merge_append_ts_wf():
    a = []
    for i in range(10):
        a.append({'item': {'timestamp': i, 'wf': [i] * 2}})
    ma = merge_append_ts_wf(a)
    assert 'item' in ma
    assert 'timestamp' in ma['item']
    assert 'wf' in ma['item']


def _test_dict_store():
    """Test decorator usage with basic dict store mapping"""

    @merge_and_write_upon_count
    class DictStore(dict, BulkStore):
        pass

    _test_store(DictStore())

    @merge_and_write_upon_count(n_calls_to_execute=7)
    class DictStore7(dict, BulkStore):
        pass

    _test_store(DictStore7(), n_bulk=7)


def _test_files_store():
    """Test decorator usage with file store"""

    with TemporaryDirectory() as tmpdirname:
        audio_store = WavFileStore(rootdir=tmpdirname)
        _test_store(audio_store)
        print(f'{len(list(Path(tmpdirname).iterdir()))=} == {len(audio_store)=}')
        assert len(list(Path(tmpdirname).iterdir())) == len(audio_store)


def _test_store(
    store_instance: MutableMapping, *, n=22, chk_size=2, log=print, n_bulk=N_TO_BULK
):
    """Test append, tracking, input, and output usage

    :param store_instance:
    :param n: number of chunks
    :param chk_size: samples per chunk
    :param log: print
    :return:
    """

    def n_append_tracks(store):
        _, append_track = next(iter(store._tracks.items()), (None, tuple()))
        return len(append_track)

    with store_instance as a:
        for i in range(n):
            a.append({'timestamp': i, 'wf': [i] * chk_size})

            _, append_track = next(iter(a._tracks.items()), (None, tuple()))

            log('print#2', f'{i=}', f'{n_append_tracks(a)=}', a)
            assert (
                n_append_tracks(a) == (i + 1) % n_bulk
            ), 'Tracking should auto flush when size limit is reached'
            log('print#3', f'{len(a) == 0=}')
            assert len(a) == (i + 1) // n_bulk, list(a)
            log(a._tracks)

        _, append_track = next(iter(a._tracks.items()), (None, tuple()))

        log('print#4', f'{n_append_tracks(a) == n=}')
        assert n_append_tracks(a) == n % n_bulk
        log('print#5', a, len(append_track))

    _, append_track = next(iter(a._tracks.items()), (None, tuple()))

    log('print#6', n_append_tracks(a), a)
    assert n_append_tracks(a) == 0
    assert len(a) == ceil(n / n_bulk), f'{len(a)=} == {ceil(n / n_bulk)=}'
    for i, (k, v) in enumerate(sorted(a.items())):
        log('print#7', f'{(k, v)=}')
        assert k == i * n_bulk
        if k + n_bulk > n:
            assert (
                len(v) / chk_size == n - k
            ), f'{i=}, {k=}, {len(v) / chk_size=}, {n - k=}'
        else:
            assert (
                len(v) / chk_size == n_bulk
            ), f'{i=}, {k=}, {len(v) / chk_size=}, {n_bulk=}'
        v_iter = iter(v)
        for j in range(i * n_bulk, min((i + 1) * n_bulk, n)):
            for _ in range(chk_size):
                assert (
                    next(v_iter) == j
                ), f'{i=}, {j=}, {k=}, {i * n_bulk=}, {min((i + 1) * n_bulk, n)=}'

    print(f'Test passed with params: {store_instance=}, {n=}, {chk_size=}, {log=}')


if __name__ == '__main__':
    _test_merge_append_ts_wf()
    _test_dict_store()
    _test_files_store()
