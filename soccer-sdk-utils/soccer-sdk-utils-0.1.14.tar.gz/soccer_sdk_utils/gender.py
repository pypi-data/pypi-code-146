from enum import Enum


class Gender(Enum):
    # __order__ = "ALL Male Female"
    All = 0
    Male = 1
    Female = 2

    def __repr__(self):
        if self == Gender.All:
            return "All"
        elif self == Gender.Male:
            return "Male"
        elif self == Gender.Female:
            return "Female"
        else:
            return "Unknown"

    def __str__(self):
        return self.name.lower()


def string_to_gender(value: str | None) -> Gender:
    if value is None:
        raise ValueError("Undefined gender string!")

    value = value.strip()

    if len(value) == 0:
        raise ValueError("Empty gender string!")

    value = value.lower()

    if value in ["all"]:
        return Gender.All
    elif value in ["m", "male"]:
        return Gender.Male
    elif value in ["f", "female"]:
        return Gender.Female
    else:
        raise ValueError(f"Invalid gender string '{value}'!")


if __name__ == "__main__":
    print(repr(Gender.All))
    print(repr(Gender.Male))
    print(repr(Gender.Female))
