import functools
import re
from typing import List, Tuple, TypeVar, Iterable, Iterator, Type, Union, Sequence, Mapping, Callable, Generic, Dict
from typing import Optional

from torch.nn import ELU, Identity, ReLU, LeakyReLU, Sigmoid, Softmax, Tanh, Module


T = TypeVar('T')


class AttributeDict(Generic[T]):
    def __init__(self, dictionary: Dict[str, T]) -> None:
        self.dictionary = dictionary

        for key, value in self.items():
            setattr(self, key.lower().replace(' ', '_'), value)

    def __getattr__(self, name):
        return getattr(self, name)

    def __getitem__(self, key):
        return self.dictionary[key]

    def __repr__(self):
        return repr(self.dictionary)

    def __len__(self):
        return len(self.dictionary)

    def __contains__(self, item):
        return item in self.dictionary

    def __iter__(self):
        return iter(self.dictionary)

    def keys(self):
        return self.dictionary.keys()

    def values(self):
        return self.dictionary.values()

    def items(self):
        return self.dictionary.items()


def get_pairs(items: Iterable[T]) -> Iterator[Tuple[T, T]]:
    first = None

    for index, item in enumerate(items):
        if index % 2 == 0:
            first = item
        else:
            yield first, item  # type: ignore


def create_selector(indices: Union[int, Sequence[int]]) -> Callable[[Sequence[T]], Union[T, Tuple[T, ...]]]:
    def select(items: Sequence[T]) -> Union[T, Tuple[T, ...]]:
        if isinstance(indices, int):
            return items[indices]

        return tuple(items[index] for index in indices)

    return select


def to_list(*args: Union[Sequence[T], T]) -> List[T]:
    items: List[T] = []

    for argument in args:
        if isinstance(argument, Sequence):
            items += argument
        else:
            items.append(argument)

    return items


def to_bool(value: Optional[str]) -> Optional[bool]:
    if value is None:
        return None

    if value == '0' or value.lower() == 'false':
        return False

    return bool(value)


def to_bool_or_false(value: Optional[str]) -> bool:
    return to_bool(value) or False


def get_activation(name: str) -> Type[Module]:
    return {
        'elu': ELU,
        'identity': Identity,
        'relu': ReLU,
        'leaky_relu': LeakyReLU,
        'sigmoid': Sigmoid,
        'softmax': Softmax,
        'tanh': Tanh,
    }[name]


def parse_map_sequence(string: str, sequence_type: Type[T]) -> Mapping[str, Sequence[T]]:
    substrings = re.split(r'(?<=]),', string)

    output = {}

    for substring in substrings:
        key, value = substring.split(':')

        output[key] = list(map(sequence_type, value.strip('[]').split(',')))

    return output


parse_map_ints = functools.partial(parse_map_sequence, sequence_type=int)
parse_map_floats = functools.partial(parse_map_sequence, sequence_type=float)
parse_map_strings = functools.partial(parse_map_sequence, sequence_type=str)
