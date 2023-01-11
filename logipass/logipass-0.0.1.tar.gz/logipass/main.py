""" This file includes functions of the password generation. """

from random import choices
import string
from typing import List

SPECIALS = "~!@#$%^&*()_-+={[}]|:<,>.?/"

ALL_PASS_CHARS = string.ascii_letters + string.digits + SPECIALS


def password_gen(*, remove: List[str] = None, password_length: int = 8):
    """
    This function generates the password when called. It also contains the
    feature to provide the password containing chars based on user provided
    length and also to remove/filter certain chars if not required
    in the password.
    Args:
     - remove: filter the not required chars from password
     - password_length: provide the length of the password

    Returns:
        password as per the user requirement
    """
    assert isinstance(remove, list) or remove is None, (
        f"Not of a required type 'List' " f"instead it is '{type(remove)}'."
    )
    assert isinstance(password_length, int), (
        f"Not of a required type 'int' instead it " f"is '{type(remove)}'."
    )
    if remove:
        filtered_pass = str([ALL_PASS_CHARS.replace(i, "") for i in remove])
        return "".join(choices(filtered_pass, k=password_length))

    return "".join(choices(ALL_PASS_CHARS, k=password_length))


if __name__ == "__main__":
    print(f"Password is: {password_gen()}")
