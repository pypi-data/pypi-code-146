from __future__ import annotations

import privateprefs.core.database as _db


def load(key: str) -> str | None:
    """
    Loads the value for a given key.
    :param key: A key return the value for
    :return: The stored value or None if key does not exist.
    """
    return _db.read(key)


def load_keys(keys: list = None, return_as_list: bool = False) -> dict | list:
    """
    Loads and returns key-value pairs for the given keys.
    :param keys: List of keys to return, by default all key-value pairs will be returned.
    :param return_as_list: If true a list of tuples will be returned, If false the default dict will be returned
    :return: A dict of key-value pairs by default, or a list of tuples.
    """
    return _db.read_keys(keys, return_as_list)


def delete_all() -> None:
    """
    Deletes all stored key-value pairs.
    :return: None
    """
    _db.delete_all()


def delete(key: str) -> None:
    """
    Delete the value for the given key.
    :param key: The key to delete the value of
    :return: None
    """
    _db.delete(key)
