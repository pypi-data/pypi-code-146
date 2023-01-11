import math
from .constants import PhysicalUnits


class ObisValueFloat():
    def __init__(self, raw_value: float, unit: PhysicalUnits = PhysicalUnits(0), scale: int = 0) -> None:
        self._raw_value = raw_value
        self._scale = scale
        self._unit = unit

    def __add__(self, other):
        if (self.Unit == other.Unit):
            x = self.Value + other.Value
            return ObisValueFloat(x, self.Unit)
        else:
            return ObisValueFloat(math.nan)

    def __sub__(self, other):
        if (self.Unit == other.Unit):
            x = self.Value - other.Value
            return ObisValueFloat(x, self.Unit)
        else:
            return ObisValueFloat(math.nan)
        
    @property
    def RawValue(self) -> float:
        return self._raw_value

    @property
    def Scale(self) -> float:
        return self._scale

    @property
    def Unit(self) -> PhysicalUnits:
        return self._unit

    @property
    def Value(self) -> float:
        return self._raw_value * 10**self._scale

    @property
    def ValueString(self) -> str:
        return f"{self.Value} {self.Unit.name}"


class ObisValueString():
    def __init__(self, raw_value: str) -> None:
        self._raw_value = raw_value

    @property
    def RawValue(self) -> str:
        return self._raw_value
    
    @property
    def Value(self) -> str:
        return self._raw_value.decode() 

