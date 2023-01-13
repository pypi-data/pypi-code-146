import json
import typing

from . import string_cleaner

if typing.TYPE_CHECKING:
    from .models import BaseGWDGUser


class IDMNotReachableError(Exception):
    pass


class IDMRequestError(Exception):
    pass


class BadJsonError(Exception):
    pass


class AlreadyDeletedError(Exception):
    pass


class InvalidUIDException(Exception):
    pass


def pretty_print(obj: "BaseGWDGUser | list[BaseGWDGUser]") -> str:
    if isinstance(obj, list):
        return pretty_multy_print(obj)
    else:
        return pretty_single_print(obj)


def pretty_single_print(obj: "BaseGWDGUser") -> str:
    return json.dumps(obj.dict(), indent=2)


def pretty_multy_print(obj: list["BaseGWDGUser"]) -> str:
    return json.dumps([entry.dict() for entry in obj], indent=2)


def username_prediction(given_name, surname):
    given_name = string_cleaner.clean(given_name)
    surname = string_cleaner.clean(surname)
    if not given_name and not surname:
        raise InvalidUIDException(
            "Givenname oder Surname ist nach dem StringClean leer und es kann daher kein username aus givenname.surname generiert werden."
        )

    username = f"{given_name}.{surname}"
    if len(username) > 18:
        username = f"{given_name[0]}.{surname}"

    if len(username) > 18:
        username = f"{given_name[0]}.{surname[:16]}"

    return username
