import abc
from datetime import date, datetime
from typing import Any, Optional, Union


class Dimension(abc.ABC):
    """
    Dimensions define the actual axes of the data/cube.
    """

    _type: Optional[type] = None
    default = None

    def __init__(self, name: Optional[str] = None, null: bool = False):
        """
        Name could be supplied later on if the dimension is declared in HCube class specification
        for example
        """
        self.name: Optional[str] = name
        self.null = null

    def to_python(self, value: Any):
        """
        Simple implementation that uses `self._type` for conversion. Child classes may completely
        override this method.
        """
        if not self._type:
            raise NotImplementedError("Dimension type is not specified")
        self._check_null(value)
        if value is None:
            return value
        if isinstance(value, self._type):
            return value
        return self._type(value)

    def _check_null(self, value):
        if value is None and not self.null:
            raise ValueError("Null value is only allowed if the dimension has null=True")


class StringDimension(Dimension):

    _type = str
    default = ""


class IntDimension(Dimension):

    _type = int
    default = 0

    def __init__(
        self, name: Optional[str] = None, null: bool = False, signed: bool = True, bits: int = 32
    ):
        """
        Backends are not required to use the `signed` and `bits` information. They are there just
        as hints to backends which support it.
        """
        super().__init__(name, null)
        self.signed = signed
        self.bits = bits


class DateDimension(Dimension):

    _type = date
    default = date(1970, 1, 1)

    def to_python(self, value: Union[str, date, datetime]):
        self._check_null(value)
        if value is None:
            return None
        if isinstance(value, date):
            return value
        if isinstance(value, datetime):
            return value.date()
        return date.fromisoformat(value)


class DateTimeDimension(Dimension):

    _type = datetime
    default = datetime(1970, 1, 1, 0, 0, 0)

    def to_python(self, value: Union[str, date, datetime]):
        self._check_null(value)
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, date):
            return datetime(value.year, value.month, value.day)
        return datetime.fromisoformat(value)


class ArrayDimension(Dimension):

    _type = list
    default = []

    def __init__(self, name: Optional[str] = None, null: bool = False, dimension: Dimension = None):
        super().__init__(name, null)
        self.dimension = dimension
