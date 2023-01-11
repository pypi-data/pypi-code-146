"""
Classes representing FITS header schemas.

Each header card is represented by a `~dkist_data_simulator.schemas.Key` class,
with a `~dkist_data_simulator.schemas.Section` of the schema being a collection
of ``Key`` classes and a `~dkist_data_simulator.schemas.Schema` being a
collection of ``Section`` classes.

``Schema`` classes are provided which load the DKIST Spec 122 and 214 schemas
from `fits_validator`.
"""
import string
import datetime
from typing import Any, Dict, List, Tuple, Union, Iterable
from functools import partial
from dataclasses import fields, dataclass

import astropy.units as u
import numpy as np
from dkist_fits_specifications.utils import schema_type_hint

__all__ = [
    "ValuesRangeKey",
    "ExampleValuesKey",
    "ValuesKey",
    "TimeKey",
    "DefaultKey",
    "Key",
    "Section",
    "Schema",
]


@dataclass
class Key:
    """
    A representation of the schema for a single key.

    Parameters
    ----------
    key
        The FITS key for this card.
    required
        If this key is required to be in the header for it to pass validation.
    type
        The type of this header value. One of {'int', 'float', 'str', 'bool', 'time'}.
    """

    key: str
    required: bool
    expected: bool
    type: Union[str, type]  # Converted to a type on init.

    def __init_subclass__(cls):
        KEY_SCHEMAS.append(cls)

    def __post_init__(self):
        type_lookup = {
            "int": int,
            "float": float,
            "str": str,
            "bool": bool,
            "time": datetime.datetime,
            "unit": u.Unit,
        }

        if self.type not in type_lookup:
            raise ValueError(f"{self.type!r} is not a known type for a Key schema.")

        self.type = type_lookup[self.type]
        self._extra = {}
        self.random = np.random.default_rng()

    def generate_value(self) -> Any:
        max_int = max_float = 1e6
        len_str = 30
        if self.type is bool:
            return bool(self.random.integers(0, 1))
        elif self.type is int:
            return int(self.random.integers(0, int(max_int)))
        elif self.type is float:
            return float(self.random.uniform(0, max_float))
        elif self.type is str:
            return "".join(
                self.random.choice(list(string.ascii_uppercase + string.digits))
                for _ in range(len_str)
            )

        raise NotImplementedError(
            f"Can not generate a random value for schema type {self.type}"
        )


KEY_SCHEMAS: List[type] = [Key]


@dataclass
class DefaultKey(Key):
    """
    A key which has a default value.
    """

    default: Any

    def generate_value(self) -> Any:
        return self.default


@dataclass(init=False)
class TimeKey(Key):
    """
    A representation of the schema for a single key.

    Parameters
    ----------
    key
        The FITS key for this card.
    required
        If this key is required to be in the header for it to pass validation.
    format
        The time string format.
    """

    format: str = "isot"
    """
    The time string format.
    """

    def __init__(
        self,
        key: str,
        required: bool,
        expected: bool,
        type: str = "time",
        format: str = "isot",
    ):
        self.format = format
        super().__init__(key, required, expected, type)

    def generate_value(
        self, start: str = "2019-11-08", stop: str = "2059-11-08"
    ) -> str:
        trange_start = datetime.datetime.fromisoformat(start).timestamp()
        trange_stop = datetime.datetime.fromisoformat(stop).timestamp()

        delta = trange_stop - trange_start

        rand_delta = self.random.uniform(0, delta)

        if self.format == "isot":
            return datetime.datetime.utcfromtimestamp(
                trange_start + rand_delta
            ).isoformat("T")

        raise NotImplementedError(
            f"Generation of times with format {self.format} is not implemented."
        )


@dataclass(init=False)
class UnitKey(Key):
    """
    A representation of the schema for a single key.

    Parameters
    ----------
    key
        The FITS key for this card.
    required
        If this key is required to be in the header for it to pass validation.
    """

    format: str = "unit"
    """
    The time string format.
    """

    def __init__(
        self,
        key: str,
        required: bool,
        expected: bool,
        type: str = "unit",
        format: str = "unit",
    ):
        super().__init__(key, required, expected, type)

    def generate_value(self) -> str:
        unit = self.random.choice((u.m, u.arcsec, u.deg))
        return unit.to_string(format="fits")


@dataclass
class ValuesKey(Key):
    """
    A key which can take an enumerated list of values.

    Parameters
    ----------
    key
        The FITS key for this card.
    required
        If this key is required to be in the header for it to pass validation.
    type
        The type of this header value. One of {'int', 'float', 'str', 'bool', 'time'}.
    values
        A list of values which the key can take. Must be of type ``type``.
    """

    values: List[Any]
    format: str = None

    def generate_value(self) -> Any:
        return self.type(self.random.choice(self.values))


@dataclass
class ValuesRangeKey(Key):
    """
    A key which can take a value somewhere in a numerical range.

    Parameters
    ----------
    key
        The FITS key for this card.
    required
        If this key is required to be in the header for it to pass validation.
    type
        The type of this header value. One of {'int', 'float', 'str', 'bool', 'time'}.
    values
        A list of values which the key can take. Must be of type ``type``.
    """

    values_range: List[Any]
    format: str = None

    def generate_value(self) -> Any:
        low = self.values_range[0]
        try:
            high = self.values_range[1]
        except IndexError:
            high = 1000000
        return self.type(self.random.uniform(low=low, high=high))


@dataclass
class ExampleValuesKey(Key):
    """
    A key which can take an enumerated list of example values.

    Parameters
    ----------
    key
        The FITS key for this card.
    required
        If this key is required to be in the header for it to pass validation.
    type
        The type of this header value. One of {'int', 'float', 'str', 'bool', 'time'}.
    example_values
        A list of example values which the key can take. Must be of type ``type``.
    """

    example_values: List[Any]
    format: str = None

    def generate_value(self) -> Any:
        return self.type(self.random.choice(self.example_values))


def construct_key_from_dict(schema: dict, random=None) -> Key:
    core_keys = {
        "key",
        "type",
        "required",
        "expected",
        "format",
        "values",
        "values_range",
        "example_values",
    }
    extra_keys = set(schema.keys()).difference(core_keys)
    extra = tuple(schema.pop(ek) for ek in extra_keys if ek in schema)

    key_schemas = {ks: {f.name for f in fields(ks)} for ks in KEY_SCHEMAS}
    for key_schema, fds in key_schemas.items():
        # Some values keys have a format others don't.
        # To prevent having to add all format to all the keys,
        # we add a default format to all values schemas here.
        fmt = getattr(key_schema, "format", None)
        if "values" in fds and "format" in fds and "format" not in schema:
            schema["format"] = fmt

        if set(schema.keys()) == fds:
            if fmt and schema["format"] != fmt:
                continue
            ks = key_schema(**schema)
            ks._extra = extra
            ks.random = random
            return ks

    raise ValueError(f"Could not find a matching schema for {schema}")


@dataclass
class Section:
    """
    A representation of a single schema section (file).

    Parameters
    ----------
    keys
        A list of `~dkist_data_simulator.schemas.Key` objects representing the
        cards in this section.
    """

    keys: Tuple[Key, ...]

    @classmethod
    def from_dict(cls, section_dict: schema_type_hint, random: Any = None):
        schema: List[Dict[str, Any]] = [
            {"key": key, **value} for key, value in section_dict.items()
        ]
        keys = tuple(map(partial(construct_key_from_dict, random=random), schema))
        return cls(keys)

    def generate(
        self, *, required_only=False, expected_only=False, **kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate values for this section.

        Parameters
        ----------
        kwargs
            All keyword arguments override randomly generated values.
        """
        filtering = expected_only or required_only
        section_header = {
            k.key: k.generate_value()
            for k in self.keys
            if not filtering
            or ((expected_only and k.expected) or (required_only and k.required))
        }
        # We explicitly exclude some keys which should only be conditionally written to the file
        section_header.pop("SIMPLE", None)
        section_header.pop("BLANK", None)
        section_header.pop("END", None)
        return {**section_header, **kwargs}


@dataclass
class Schema:
    """
    A base representation of a FITS header schema

    Parameters
    ----------
    sections
        A list of `~dkist_data_simulator.schemas.Section` objects representing
        the sections of this schema.
    """

    sections: Tuple[Section, ...]
    random: Any = np.random.default_rng()

    @classmethod
    def sections_from_dicts(
        cls, sections: Iterable[schema_type_hint], random: Any = None
    ):
        """
        Construct a schema from a list of section dicts.
        """
        random = random or cls.random
        return [
            Section.from_dict(schema_dict, random=random) for schema_dict in sections
        ]

    def generate(
        self, *, required_only=False, expected_only=False, **kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a header following this schema.

        Parameters
        ----------
        kwargs
            All keyword arguments override randomly generated values.
        """
        section_headers = [
            section.generate(required_only=required_only, expected_only=expected_only)
            for section in self.sections
        ]
        schema_headers = section_headers[0]
        for sh in section_headers[1:]:
            schema_headers.update(sh)
        return {**schema_headers, **kwargs}

    def __getitem__(self, item):
        for section in self.sections:
            for key in section.keys:
                if key.key == item:
                    return key
        raise KeyError(f"The key {item} is not found in any sections of this schema.")
