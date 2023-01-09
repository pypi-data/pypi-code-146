from chalk.features import Features, features


@features
class UserProfile:
    user_id: str
    profile_id: str
    address: int


@features
class Account:
    account_id: str
    balance: int


@features
class Transaction:
    user_id: str
    amount: int
    source_account_id: int
    dest_account_id: int


@features
class MypyUserFeatures:
    uid: str
    name: str
    bday: str
    age: int


def name_age_good(
    age: MypyUserFeatures.age,
) -> Features[MypyUserFeatures.name, MypyUserFeatures.age]:
    # Correctly knows that age is an in
    age_int_cast: int = age
    print(age_int_cast)
    # Correctly casts UserFeatures.__init__ to Features[name, age]
    return MypyUserFeatures(name="4", age=4)


def name_age_good_flipped(
    age: MypyUserFeatures.age,
) -> Features[MypyUserFeatures.age, MypyUserFeatures.name]:
    # Flips name and age to match
    return MypyUserFeatures(name="4", age=4)


def name_age_bad() -> Features[MypyUserFeatures.name, MypyUserFeatures.age]:
    # We're getting Features[name, bday] and expected Features[name, age]
    return MypyUserFeatures(name="4", bday="")


def name_bad_type() -> Features[MypyUserFeatures.name]:
    # Knows that name should be a string, not an int
    return MypyUserFeatures(name=4)  # pyright: ignore
