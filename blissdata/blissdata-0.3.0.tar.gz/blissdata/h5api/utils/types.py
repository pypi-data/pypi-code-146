from typing import Tuple, Union, Sequence
from numbers import Number, Integral

try:
    from types import EllipsisType

    SingleDataIndexType = Union[Integral, slice, Sequence, EllipsisType]
except ImportError:
    SingleDataIndexType = Union[Integral, slice, Sequence]
from numpy.typing import ArrayLike

DataType = Union[bytes, Number, ArrayLike]
DataIndexType = Union[SingleDataIndexType, Tuple[SingleDataIndexType]]
