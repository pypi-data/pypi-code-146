from abc import ABC


class Model(ABC):
    """
    One model corresponds to one database table.
    """

    _primary_key: int
    _primary_key_name: str = "id"
