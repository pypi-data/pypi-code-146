from chalk.features import Features
from tests.mypy.mypy_test import MypyUserFeatures


def name_age_bad() -> Features[MypyUserFeatures.name, MypyUserFeatures.age]:
    # We're getting Features[name, bday] and expected Features[name, age]
    return MypyUserFeatures(name="4", bday="")


def name_age_good_flipped() -> Features[MypyUserFeatures.age, MypyUserFeatures.name]:
    # Flips name and age to match
    return MypyUserFeatures(name="4", age=4)


def name_bad_type() -> Features[MypyUserFeatures.name]:
    # Knows that name should be a string, not an int
    MypyUserFeatures(what=4)
    return MypyUserFeatures(name=4)
