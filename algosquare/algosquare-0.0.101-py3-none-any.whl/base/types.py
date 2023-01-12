"""Types and auxiliary functions."""

from enum import IntEnum

class Datatype(IntEnum):
    """Datatype of feature."""
    VOID = 0
    INT = 1
    FLOAT = 2
    STR = 3

class Metatype(IntEnum):
    """Metatype of feature."""
    VOID = 0
    NUMERICAL = 1
    CATEGORICAL = 2
    BINARY = 3
    DATETIME = 4
    TIMESTAMP = 5
    DELIM_PIPE = 6
    DELIM_SEMICOLON = 7
    LIST = 8
    TEXT = 9

DELIMITER_METATYPES = {Metatype.DELIM_PIPE, Metatype.DELIM_SEMICOLON}
TARGET_METATYPES = {Metatype.BINARY, Metatype.CATEGORICAL, Metatype.NUMERICAL}

def is_delimiter_metatype(metatype, strict = False):
    """Checks if metatype is delimiter metatype.

    Args:
        metatype: Metatype or int.
        strict: checks if metatype is Metatype.

    Returns:
        bool.
    """
    if strict and not isinstance(metatype, Metatype):
        return False

    try:
        return Metatype(metatype) in DELIMITER_METATYPES
    except ValueError:
        return False

def get_delimiter(metatype):
    """Maps delimiter metatype to delimiter.

    Args:
        metatype: Metatype or int.

    Returns:
        str.

    Raises:
        ValueError
    """
    metatype = Metatype(metatype)
    if metatype == Metatype.DELIM_PIPE:
        return '|'

    if metatype == Metatype.DELIM_SEMICOLON:
        return ';'

    raise ValueError('invalid delimiter metatype')

def is_classification_metatype(metatype, strict = False):
    """Checks if metatype is valid classification target metatype.

    Args:
        metatype: Metatype or int.
        strict: checks if metatype is Metatype.

    Returns:
        bool.
    """
    if strict and not isinstance(metatype, Metatype):
        return False

    try:
        return Metatype(metatype) in (Metatype.BINARY, Metatype.CATEGORICAL)
    except ValueError:
        return False

def is_target_metatype(metatype, strict = False):
    """Checks if metatype is valid target metatype.

    Args:
        metatype: Metatype or int.
        strict: checks if metatype is Metatype.

    Returns:
        bool.
    """
    if strict and not isinstance(metatype, Metatype):
        return False

    try:
        return Metatype(metatype) in TARGET_METATYPES
    except ValueError:
        return False

def string_to_metatype(string):
    """Converts string to Metatype.

    Args:
        string: str.

    Returns:
        Metatype.

    Raises:
        TypeError, ValueError
    """
    if not isinstance(string, str):
        raise TypeError('string must be a str')

    return Metatype[string.upper()]

class PredictionMethod(IntEnum):
    """Prediction method of predictor."""
    PREDICT = 0
    PREDICT_PROBA = 1
    DECISION_FUNCTION = 2

def is_prediction_method(prediction_method, strict = False):
    """Checks if prediction_method is valid.

    Args:
        prediction_method: PredictionMethod or int.
        strict: checks if prediction_method is PredictionMethod.

    Returns:
        bool.
    """
    if strict and not isinstance(prediction_method, PredictionMethod):
        return False

    try:
        PredictionMethod(prediction_method)
    except ValueError:
        return False

    return True
