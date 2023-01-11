from enum import Enum


class DataType(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    STRING = "STRING"
    CURRENCY = "CURRENCY"
    DATE = "DATE"
    NUMBER = "NUMBER"
    YEAR = "YEAR"
    BOOLEAN = "BOOLEAN"
    INTEGER = "INTEGER"
