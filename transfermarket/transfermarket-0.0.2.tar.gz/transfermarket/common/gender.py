from enum import Enum


class Gender(Enum):
    # __order__ = "ALL Male Female"
    All = 0
    Male = 1
    Female = 2

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.name.lower()

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name.lower() == other.lower()

        return self.name == other.name


def string_to_gender(value: str) -> Gender:
    if value is None:
        raise ValueError("Undefined gender string!")

    value = value.strip()

    if len(value) == 0:
        raise ValueError("Empty gender string!")

    value = value.lower()

    if value in ["all"]:
        return Gender.All

    if value in ["m", "male"]:
        return Gender.Male

    if value in ["f", "female"]:
        return Gender.Female

    raise ValueError(f"Invalid gender string '{value}'!")
