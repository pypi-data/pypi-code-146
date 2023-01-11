import enum


class Roles(enum.Enum):
    IDENTIFIER = "identifier_code"
    LABEL = "label"
    NUMERIC = "numeric"
    TIMESTAMP_DATE_TIME = "timestamp_date_time"
    SHORT_TEXT = "short_text"
    FREE_TEXT = "free_text"
    NOT_RECOGNIZED = "not_recognized"
    IGNORE = "ignore"


class DataTypes(enum.Enum):
    NUMBER = "int"
    STRING = "str"
    DOUBLE = "double"
    DATE_TIME = "date"
    # // FLOAT = "float"
    # // BOOLEAN = "boolean"

