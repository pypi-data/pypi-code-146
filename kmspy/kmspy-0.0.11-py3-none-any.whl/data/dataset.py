from __future__ import annotations


from collections import defaultdict
import copy
from itertools import product
import logging
import random
import re
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, Set

from .prefetch_generator import PrefetchGenerator
from ..utils import is_available, width

import numpy as np


logger = logging.getLogger(__name__)


class Dataset:
    """
    """
    
    def __init__(self, data: List[Dict[str, Any]] = None, shuffle: bool = False, *args, **kwargs) -> None:
        if data is None:
            pass
        else:
            if isinstance(data, list):
                if data:
                    if isinstance(data[0], dict):
                        pass
                    else:
                        raise(ValueError("각각의 요소는 dict 타입이어야 합니다."))
            else:
                raise(ValueError("data는 list 타입이어야 합니다."))

        self._data = data if data is not None else []
        self._shuffle = shuffle

    def append(self, data: Dict[str, Any]) -> None:
        self._data.append(data)

    add = append

    def drop(self, condition: function) -> Dataset:
        return self.filter(lambda x: not condition(x))

    def filter(self, condition: function) -> Dataset:
        return Dataset(list(filter(condition, self._data)))

    def merge(self, key: str, values: Union[List[str], Tuple[str]], sort: bool = True) -> Dataset:
        if isinstance(values, (list, tuple)):
            if sort:
                values = sorted([str(v) for v in values])
            new_values = "+".join(values)
            return Dataset([{k: (new_values if (key == k and d[k] in values) else d[k]) for k in d.keys()} for d in self._data])
        else:
            raise TypeError("unsupported operand type(values) for merge")

    def __add__(self, other: Dataset) -> Dataset:
        cls = Dataset(shuffle=self._shuffle)
        cls._data.extend(copy.deepcopy(self._data))
        cls._data.extend(copy.deepcopy(other._data))
        return cls

    def __radd__(self, other: Dataset) -> Dataset:
        return self + other

    def __getitem__(self, index: Union[int, slice]) -> Dataset:
        cls = Dataset()
        data = self._data[index]
        if isinstance(data, dict):
            cls._data.append(data)
        else:
            cls._data.extend(data)
        return cls

    def __len__(self) -> int:
        return self.num_data

    @property
    def data(self) -> List[Dict[str, Any]]:
        if self._shuffle:
            random.shuffle(self._data)
        return self._data

    @property
    def num_data(self):
        return len(self._data)

    def counts(self, keys: Optional[Union[List[str], Tuple[str], Set[str], str]] = None):
        if keys is not None and isinstance(keys, str):
            keys = set([keys])
        _counts = defaultdict(lambda: defaultdict(int))
        for d in self._data:
            for k, v in d.items():
                if keys is not None and k in keys:
                    _counts[k][v] += 1
                else:
                    _counts[k][v] += 1
        return {k1: dict(v1) for k1, v1 in _counts.items()}

    def combination_counts(self, keys: Union[List[str], Tuple[str], Set[str]], views: Optional[Union[List[str], Tuple[str], Set[str], str]] = None) -> List[Dict[str, Any]]:
        def _cond(keys, values):
            def _wrapper(data):
                for k, v in zip(keys, values):
                    if data[k] == v:
                        pass
                    else:
                        b = False
                        break
                else:
                    b = True
                return b
            return _wrapper

        if not isinstance(keys, list):
            keys = list(keys)
        
        if views is not None:
            if isinstance(views, str):
                views = [views]
                
        _kvs = {k: list(v.keys()) for k, v in self.counts(keys).items() if k in keys}

        combinations = _kvs[keys[0]]
        for i in range(len(keys)-1):
            combinations = ["\x1b".join(p) for p in product(combinations, _kvs[keys[i+1]])]
        combinations = [c.split("\x1b") for c in combinations]

        _counts = []
        for c in combinations:
            ds = self.filter(_cond(keys, c))
            if ds.num_data > 0:
                _tmp = {k: v for k, v in zip(keys, c)}
                if views:
                    _ds_counts = ds.counts()
                    for v in views:
                        _tmp[v] = list(set(_ds_counts[v]))
                _counts.append(_tmp)
                _tmp["count"] = ds.num_data
            
        # max_lengths = [0 for _ in range(len(keys))]
        # for c in combinations:
        #     for i in range(len(keys)):
        #         if max_lengths[i] < width(c[i]):
        #             max_lengths[i] = width(c[i])
        # _counts = {}
        # for c in combinations:
        #     name = ", ".join([f"{k.title()}: {v:{max_lengths[i]}s}" for i, (k, v) in enumerate(zip(keys, c))])
        #     n = self.filter(_cond(keys, c)).num_data
        #     if n > 0:
        #         _counts[name] = n
        return _counts
        
    def print_counts(self, max_display: int = 10, keys: Optional[Union[List[str], Tuple[str], Set[str], str]] = None, print_all: bool = False):
        if print_all:
            max_display = int(1e10)
        _warn = True
        _counts = self.counts(keys)
        _repr = []
        for k, v in _counts.items():
            _tmp = []
            for _i, (_k, _v) in enumerate(v.items()):
                if _i+1 == max_display+1:
                    if not print_all and _warn:
                        logger.warning(f"표시할 요소의 개수가 {max_display:d}개를 초과합니다. 모든 요소를 표시하려면 'print_all=True' 옵션을 사용하세요.")
                        _warn = False
                    _tmp.append("...")
                    break
                _tmp.append(f"{_k if _v == 1 else f'{_k}({_v})'}")
            _repr.append(f"{k}: {', '.join(_tmp)}")
        _repr = "\n".join(_repr)
        _repr = re.sub(r"^", " " * 4, _repr, 0, re.M)
        print(f"Dataset: {self.num_data}\n{_repr}")

    def __repr__(self):
        return f"Dataset: {self.num_data}\n"

    def __iter__(self):
        return iter(self._data)


class DataLoader:
    def __init__(self, dataset: Dataset, shuffle: bool = False, batch_size: int = 1, collate_fn: Optional[Callable] = None, prefetch_factor: int = 1, num_workers: int = 1, format: Optional[str] = None, padding_value: int = 0, **kwargs) -> None:
        self.dataset = dataset
        self._shuffle = shuffle
        self._batch_size = batch_size
        self._collate_fn = collate_fn
        self._prefetch_factor = prefetch_factor
        self._num_workers = num_workers
        self._format = format if format in {"tf", "tensorflow", "torch", "pytorch"} else "numpy"
        if self._format in {"tf", "tensorflow"}:
            if is_available("tensorflow"):
                import tensorflow as tf
        elif self._format in {"torch", "pytorch"}:
            if is_available("torch"):
                import torch
        self._padding_value = padding_value
        self._gen = PrefetchGenerator(self.dataset._data, num_prefetch=self._prefetch_factor*self._batch_size, num_workers=self._num_workers, shuffle=self._shuffle, processing_func=self._collate_fn, name="DataLoader")

    def as_format(self, batch):
        if is_available("numpy"):
            ranks = [len(b) for b in batch]
            rank = np.unique(ranks)
            if len(rank) == 1:
                rank = rank[0]
                datas = [[] for _ in range(rank)]
                for b in batch:
                    for i in range(rank):
                        datas[i].append(b[i])
                for i, data in enumerate(datas):
                    max_len = np.amax(np.array([d.shape if hasattr(d, "__len__") else 1 for d in data]), axis=0)
                    min_len = np.amin(np.array([d.shape if hasattr(d, "__len__") else 1 for d in data]), axis=0)
                    if np.all(max_len == min_len):
                        datas[i] = np.array(data)
                    else:
                        padded_begin = np.zeros(max_len.shape).astype(np.int32)
                        datas[i] = np.array([np.pad(d, np.stack((padded_begin, max_len - d.shape)).T, constant_values=self._padding_value) for d in data])                        
            else:
                raise ValueError("collate_fn에서 출력하는 데이터의 개수가 동일하지 않습니다.")
        else:
            raise ModuleNotFoundError("numpy")
        if self._format == "tf":
            if is_available("tensorflow"):
                import tensorflow as tf
                for i in range(len(datas)):
                    datas[i] = tf.convert_to_tensor(datas[i])
            else:
                raise ModuleNotFoundError("tensorflow")
        elif self._format == "torch":
            if is_available("torch"):
                import torch
                for i in range(len(datas)):
                    datas[i] = torch.tensor(datas[i])
            else:
                raise ModuleNotFoundError("torch")
        return datas

    def __next__(self):
        data = []
        for _ in range(self._batch_size):
            try:
                data.append(next(self._gen))
            except StopIteration:
                if data:
                    return self.as_format(data)
                else:
                    raise StopIteration
        return self.as_format(data)

    def __iter__(self):
        return self

    def __len__(self):
        return self.dataset.num_data//self._batch_size + (0 if self.dataset.num_data%self._batch_size == 0 else 1)