#!/usr/bin/env python
"""Functional Programming data structure.
"""
import collections
import heapq
import json
import math
import random
import re
from collections.abc import Iterable
from functools import reduce
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

from codefast.base.format_print import FormatPrint as fp


class nstr(str):

    @property
    def last(self):
        return self[-1]

    @property
    def first(self):
        return self[0]

    @property
    def size(self):
        return len(self)

    @property
    def length(self):
        return len(self)

    def __add__(self, s: str) -> str:
        return nstr(super().__add__(s))

    def __mul__(self, n: int) -> str:
        return nstr(super().__mul__(n))

    def is_cn(self) -> bool:
        return True if re.search(u'[\u4e00-\u9fff]', self) else False

    def is_cn_or_punc(self) -> bool:
        if self.is_cn():
            return True
        punctuations = '，。？！；：、【】（）《》——'
        return self in punctuations

    def dump(self, file: str, mode: str = 'w') -> 'self':
        with open(file, mode) as f:
            f.write(self)
        return self


class DictItem(object):
    key: Any
    value: Any


class fpdict(dict):

    def __init__(self, d: dict = {}) -> None:
        super().__init__(d)

    def contains(self, key: str) -> bool:
        return key in self

    def filter(self, f: Callable[[str], bool]) -> 'fpdict':
        return fpdict({p[0]: p[1] for p in self.items() if f(p)})

    def filter_keys(self, keylist: List) -> 'fpdict':
        """ filter out items whose key not in keylist
        """
        return fpdict({k: self[k] for k in keylist if k in self})

    def consume(self, f: Callable[[str], Any]) -> 'fpdict':
        for p in self.items():
            f(p)

    def map_values(self, f: Callable[[str], Any]) -> 'fpdict':
        """ Apply f to values to generate new 
        """
        return fpdict({k: f(v) for k, v in self.items()})

    def map_keys(self, f: Callable[[str], Any]) -> 'fpdict':
        """ Apply f to keys to generate new 
        """
        return fpdict({f(k): v for k, v in self.items()})

    def map_tuples(self, fk: Callable[[str], Any],
                   fv: Callable[[str], Any]) -> 'fpdict':
        """ Apply f to both keys and values to generate new 
        """
        return fpdict({fk(k): fv(v) for k, v in self.items()})

    def fmap_values(self, f: Callable[[str], Any], *args, **kwargs) -> 'fpdict':
        return fpdict({k: f(v, *args, **kwargs) for k, v in self.items()})

    def on_empty(self, f: Callable[[str], Any], *args, **kwargs) -> 'fpdict':
        if not self:
            f(*args, **kwargs)
        return self

    def lvalues(self) -> 'fplist':
        """List of values"""
        return fplist(self.values())

    def lkeys(self) -> 'fplist':
        return fplist(self.keys)


class fpjson(object):
    """functional json"""

    def __init__(self, js: dict = {}) -> None:
        self.js = js

    def dump(self, file_name: str) -> 'fp.json':
        with open(file_name, 'w') as f:
            json.dump(self.js, f)
        return self

    def from_file(self, file_path: str) -> 'fpjson':
        self.js = json.load(open(file_path))
        return self


class fplist(object):
    '''List support more functionnal programming methods.'''

    def __init__(self, inputs: Union[List, int] = None) -> None:
        self.data = []
        if inputs:
            if isinstance(inputs, int):
                self.data = list(range(inputs))
            else:
                self.data = [e for e in inputs]

    @property
    def last(self):
        return self.data[-1]

    @property
    def first(self):
        return self.data[0]

    @property
    def second(self):
        return self.data[1]

    @property
    def size(self):
        return len(self.data)

    @property
    def len(self):
        return len(self.data)

    @property
    def length(self):
        return len(self.data)

    def is_empty(self) -> bool:
        return len(self.data) == 0

    def append(self, e: Any) -> 'fplist':
        self.data.append(e)
        return self

    def extend(self, other: List) -> 'fplist':
        self.data.extend(other)
        return self

    def __iter__(self):
        return iter(self.data)

    def pop(self, index: int = None) -> Any:
        if index is None:
            return self.data.pop()
        else:
            return self.data.pop(index)

    def push(self, e: Any) -> 'fplist':
        self.data.append(e)
        return self

    def map(self, func: Any) -> List:
        self.data = [func(e) for e in self.data]
        return self

    def fmap(self, f: Callable, *args, **kwargs) -> 'fplist':
        """ Apply f to each element of self
        """
        self.data = [f(e, *args, **kwargs) for e in self.data]
        return self

    def reduce(self, func: Any, initial: Any = None) -> Any:
        return reduce(func, self.data, initial)

    def groupby(self, func: Any) -> dict:
        '''Group self by func'''
        D = collections.defaultdict(list)
        for e in self.data:
            D[func(e)].append(e)
        return D

    def __add__(self, other: List) -> List:
        return self.data + other

    def __contains__(self, item):
        return item in self.data

    def __str__(self) -> str:
        return str(self.data)

    def print(self) -> 'self':
        for d in self.data:
            print(d)
        return self

    def shuffle(self) -> 'fplist':
        random.shuffle(self.data)
        return self

    def split(self, seperator: str) -> List:
        return fplist(self.data.split(seperator))

    def __mul__(self, n: int) -> List:
        return self.data * n

    def __eq__(self, other: List) -> bool:
        return self.data == other

    def __len__(self) -> int:
        return len(self.data)

    def __delitem__(self, key):
        del self.data[key]
        return self

    def each_with_index(self, func: Any) -> List:
        '''Apply func to each element of self'''
        for i, e in enumerate(self.data):
            self.data[i] = func(e, i)
        return self

    def sort(self, func: Any = None, *args, **kwargs) -> 'fplist':
        '''Sort self by func'''
        if func:
            self.data = sorted(self.data, key=func, *args, **kwargs)
        else:
            self.data = sorted(self.data, *args, **kwargs)
        return self

    # deprecated
    def tolist(self) -> List:
        return self.to_list()

    def to_list(self) -> List:
        '''Convert self to list'''
        return list(self.data)

    def to_dict(self) -> Dict:
        """ Convert self to dict, each element of self should be a tuple of length 2
        """
        return dict(self.data)

    def to_csv(self, csv_file: str, header: List[str]):
        """ Write self to csv file
        """
        import csv
        with open(csv_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(self.data)
        return self

    def slice(self, start: int, end: int) -> 'self':
        self.data = self.data[start:end]
        return self

    def on_empty(self, func: Callable, *args, **kwargs) -> 'self':
        """ Apply func to self if self is empty"""
        if self.is_empty():
            func(*args, **kwargs)
        return self

    def chunks(self, n: int) -> List[List]:
        '''Yield successive n-sized chunks from self'''
        for i in range(0, len(self), n):
            yield self.data[i:i + n]

    def flatten(self):
        self.data = list(flatten(self.data))
        return self

    def dump(self, file_path: str):
        # Dump content to local file
        with open(file_path, 'w') as f:
            f.write(str(self.data))
        return self

    def toset(self) -> set:
        '''Convert self to set'''
        return set(self.data)

    def top(self, n: int):
        self.data = self.data[:n]
        return self

    def sample(self, n: int):
        self.data = random.sample(self.data, n)
        return self

    def each(self, func: Any) -> List:
        '''Apply func to each element of self'''
        for i, e in enumerate(self.data):
            self.data[i] = func(e)
        return self

    def __setitem__(self, key, value):
        self.data[key] = value
        return self

    def __getitem__(self, key):
        return self.data[key]

    def __repr__(self) -> str:
        return str(self.data)

    def filter(self, func: Any) -> List:
        self.data = [e for e in self.data if func(e)]
        return self

    def filter_not(self, func: Any) -> List:
        self.data = [e for e in self.data if not func(e)]
        return self

    def counter(self) -> collections.Counter:
        return collections.Counter(self.data)

    def hist(self,
             bin_number: int = 20,
             upper_bound: int = 1 << 30,
             step: int = -1):
        """ Draw a histogram of the data.
        Args:
            bin_number(int): the number of bins
            upper_bound(int): the upper bound of the data
            step(int): the step of the data, if set, the bin number will be ignored
        """
        self = self.sort().filter(lambda x: x < upper_bound)
        if step > 0:
            bin_number = math.ceil((self.last - self.first) / step)
        else:
            step = (self.last - self.first) / bin_number + 0.1
        cter = self.each(lambda n: math.floor(
            (n - self.first) / step)).counter()
        acc = 0
        print('\nlist length: {}'.format(self.len))
        print('bin number: {}'.format(bin_number))
        print('step: {}\n'.format(step))
        print('max value: {}'.format(self.last))
        print('min value: {}'.format(self.first))
        print('')
        for i in range(bin_number):
            b = cter.get(i, 0)
            acc += b
            ratio = acc * 100 / self.len
            symbols = fp.cyan('#') * int(b * 100 / self.len)
            print("{:>3} | {} {:.2f}%, <={:<5}".format(i + 1, symbols, ratio,
                                                       int((i + 1) * step)))

    def join(self, seperator: str) -> nstr:
        return nstr(seperator.join(self.data))


class PriorityQueue:

    def __init__(self):
        self._ds = []

    def push(self, item: Any) -> bool:
        heapq.heappush(self._ds, item)
        return True

    def pop(self) -> Any:
        return heapq.heappop(self._ds)

    def is_empty(self) -> bool:
        return len(self._ds) == 0

    @property
    def size(self) -> int:
        return len(self._ds)

    @property
    def length(self) -> int:
        return len(self._ds)

    def nsmallest(self, count: int) -> list:
        return heapq.nsmallest(count, self._ds)

    def nlargest(self, count: int) -> list:
        return heapq.nlargest(count, self._ds)

    @property
    def first(self) -> Any:
        return heapq.nsmallest(1, self._ds)[0]

    @property
    def last(self) -> Any:
        return heapq.nlargest(1, self._ds)[0]

    def __getitem__(self, idx: int):
        return self._ds[idx]

    def __repr__(self):
        _str = ''
        for item in self._ds:
            _str += ', '.join(repr(e) for e in item) + '\n'
        return _str


def pair_sample(la: list, lb: list, ratio: float, stable: bool = False):
    '''set stable = True to ensure same result
    '''
    assert len(la) == len(lb), 'size of two list is different.'
    if stable:
        random.seed(63)
    m = int(len(la) * ratio) if ratio <= 1 else min(int(ratio), len(la))
    _pair = zip(*random.sample(list(zip(la, lb)), m))
    random.seed(None)
    return _pair


def flatten(l: List) -> List:
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes, dict)):
            yield from flatten(el)
        else:
            yield el
