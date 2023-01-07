from enum import Enum


class Division(Enum):
    # __order__ = "ALL DI DII DIII NAIA NJCAA"
    All = 0
    DI = 1
    DII = 2
    DIII = 3
    NAIA = 4
    NJCAA = 5

    def __repr__(self):
        if self == Division.All:
            return "All"
        elif self == Division.DI:
            return "DI"
        elif self == Division.DII:
            return "DII"
        elif self == Division.DIII:
            return "DIII"
        elif self == Division.NAIA:
            return "NAIA"
        elif self == Division.NJCAA:
            return "NJCAA"
        else:
            return "Unknown"


    def __str__(self):
        return self.name.lower()


def string_to_division(value: str) -> Division | None:
    if value is None:
        return None

    value = value.strip()
    value = value.lower()

    for current_division in Division:
        if current_division.name.lower() == value:
            return current_division

    return None


DivisionList = [Division.DI, Division.DII, Division.DIII, Division.NAIA, Division.NJCAA]


if __name__ == "__main__":
    division = Division.DI

    print(repr(division))
