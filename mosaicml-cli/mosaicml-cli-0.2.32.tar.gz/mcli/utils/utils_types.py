"""Type Utils for converting between nested structures"""
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Type, TypeVar, Union

PathLike = Union[str, Path]
EnumType = TypeVar('EnumType', bound=Enum)  # pylint: disable=invalid-name


class CommonEnum(Enum):
    """Base class for enums that provides a proper __str__ method and ensure_enum
    """

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def ensure_enum(cls: Type[EnumType], val: Union[str, EnumType]) -> EnumType:
        if isinstance(val, str):
            try:
                return cls[val]
            except KeyError as e:
                valid = ', '.join(str(x) for x in cls)
                raise ValueError(f'Invalid {cls.__name__}: got {val}. Must be one of: {valid}') from e

        elif isinstance(val, cls):
            return val
        raise ValueError(f'Unable to ensure {val} is a {cls.__name__} enum')


def get_hours_type(max_value: Optional[float] = None) -> Callable[[Union[str, float]], float]:
    """Returns a type checker that verifies a value is a float and lies between 0 and max_value
    """

    def _validate_hours(value: Union[str, float]) -> float:
        float_value: float = float(value)
        if float_value <= 0 or (max_value and float_value > max_value):
            if not max_value:
                range_str = f'between 0 and {max_value}'
            else:
                range_str = 'greater than 0'
            raise ValueError(f'The value for `--hours` must be a float {range_str}, but {float_value} was specified. '
                             'Please specify a value within this range.')
        return float_value

    return _validate_hours


def dot_to_nested(config: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a dot-syntax dictionary to a nested dictionary

    Takes as input a dot-syntax dictionary, e.g.
    ```
    config = {"a.b.c": "foo",
              "a.b.d": "bar"}
    ```
    and outputs a nested dictionary, e.g.
    ```
    dot_to_nested(config) == {"a": {"b": {"c": "foo", "d": "bar"}}}
    ```

    Arguments:
        config (Dict[str, Any]): A dot-syntax dictionary

    Returns:
        Dict[str, Any]: A nested dictionary
    """

    nested = {}
    for dot_key, v in config.items():
        keys = dot_key.split('.')
        inner = nested
        for key in keys[:-1]:
            inner = inner.setdefault(key, {})
        inner[keys[-1]] = v
    return nested


def nested_to_dot(data: Dict[str, Any], separator: str = '.') -> Dict[str, Any]:
    """
    Flattens a dictionary with list or sub dicts to have dot syntax
    i.e. {
        "sub_dict":{
        "sub_list":[
            "sub_sub_dict":{
            "field1": 12,
            "field2": "tomatoes"
            }
        ]
        },
        "field3": "potatoes"
    }
    returns:
    {
        "sub_dict.sub_list.sub_sub_dict.field1": 12,
        "sub_dict.sub_list.sub_sub_dict.field2": "tomatoes,
        "field3": "potatoes",
    }
    """

    def get_flattened_dict(d, _prefix, separator):
        all_items = {}
        for key, val in d.items():
            key_items = _prefix + [key]
            key_name = separator.join(key_items)
            if isinstance(val, dict):
                all_items.update(get_flattened_dict(val, key_items, separator))
            elif isinstance(val, list):
                found_sub_dicts = False
                for item in val:
                    if isinstance(item, dict):
                        found_sub_dicts = True
                        for sub_key, sub_val in item.items():
                            all_items.update(get_flattened_dict(sub_val, key_items + [sub_key], separator))
                if not found_sub_dicts:
                    all_items[key_name] = val
            else:
                all_items[key_name] = val
        return all_items

    return get_flattened_dict(data, [], separator)
