import re

from .cond_extractor import cast_conds

STRING_REGEX = r'^(\'[^\']*\')|("[^"]*")$'


def try_cast(data): # pylint: disable=too-many-return-statements
    if data is None:
        return data
    if isinstance(data, list):
        return [try_cast(val) for val in data]
    if isinstance(data, dict):
        return ensure_data_types(data)
    if re.match(STRING_REGEX, data):
        return data[1:-1]
    if data.lower() in ['true', 'yes']:
        return True
    if data.lower() in ['false', 'no']:
        return False
    if data.lower() in ['null', 'nil', 'none']:
        return None

    try:
        return float(data)
    except ValueError as _:
        return data


def ensure_data_types(data):
    return cast_conds({ key: try_cast(val) for key, val in data.items() })
