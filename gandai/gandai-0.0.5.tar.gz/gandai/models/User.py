from dataclasses import asdict, dataclass, field

from dacite import from_dict

from gandai.datastore import Cloudstore

ds = Cloudstore()


@dataclass
class User:
    phone: str
    key: str = field(init=False)

    def __post_init__(self):
        self.key = f"user/{self.phone}"


def user_exists(phone: str) -> bool:
    keys = ds.keys("user")
    return f"user/{phone}" in keys


def find_user(phone: str) -> User:
    if user_exists(phone):
        key = f"user/{phone}"
        return from_dict(User, ds[key])


def create_user(phone: str) -> User:
    user = User(phone=phone)
    ds[user.key] = asdict(user)
    return user
