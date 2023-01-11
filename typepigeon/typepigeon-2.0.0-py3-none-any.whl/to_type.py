import ast
import contextlib
import json
import sys
from datetime import date, datetime, time, timedelta
from enum import Enum, EnumMeta
from functools import lru_cache
from typing import Any, Collection, Iterable, List, Mapping, Union

from typepigeon.types import subscripted_type


@lru_cache
def installed_packages() -> List[str]:
    try:
        from importlib import metadata as importlib_metadata
    except ImportError:  # for Python<3.8
        import importlib_metadata
    installed_distributions = importlib_metadata.distributions()
    return [
        distribution.metadata["Name"].lower()
        for distribution in installed_distributions
        if distribution.metadata["Name"] is not None
    ]


def to_type(input_value: Any, output_type: Union[type, Collection[type]]) -> Any:
    """
    convert a value to the specified type

    :param input_value: Python value
    :param output_type: type to convert to
    :return: converted value

    >>> to_type(0.55, str)
    '0.55'
    >>> to_type('0.55', float)
    0.55
    >>> to_type('0.55', 'float')
    0.55
    >>> to_type(0.55, int)
    0

    >>> to_type([1], str)
    '[1]'
    >>> to_type([1, 2, '3', '4'], [int])
    [1, 2, 3, 4]
    >>> to_type([1, 2, '3', '4'], (int, str, float, str))
    (1, '2', 3.0, '4')

    >>> to_type({'a': 2.5, 'b': 4, 3: '18'}, {str: float})
    {'a': 2.5, 'b': 4.0, '3': 18.0}

    >>> to_type(datetime(2021, 3, 26), str)
    '2021-03-26 00:00:00'
    >>> to_type('20210326', datetime)
    datetime(2021, 3, 26)
    >>> to_type('01:13:20:00', timedelta)
    timedelta(days=1, hours=13, minutes=20, seconds=0)
    >>> to_type(timedelta(hours=1), str)
    '01:00:00.0'
    >>> to_type(timedelta(hours=1), int)
    3600

    >>> to_type(CRS.from_epsg(4326), int)
    4326
    >>> to_type(CRS.from_epsg(4326), str)
    GEOGCRS["WGS 84",ENSEMBLE["World Geodetic System 1984 ensemble",MEMBER["World Geodetic System 1984 (Transit)"],MEMBER["World Geodetic System 1984 (G730)"],MEMBER["World Geodetic System 1984 (G873)"],MEMBER["World Geodetic System 1984 (G1150)"],MEMBER["World Geodetic System 1984 (G1674)"],MEMBER["World Geodetic System 1984 (G1762)"],ELLIPSOID["WGS 84",6378137,298.257223563,LENGTHUNIT["metre",1]],ENSEMBLEACCURACY[2.0]],PRIMEM["Greenwich",0,ANGLEUNIT["degree",0.0174532925199433]],CS[ellipsoidal,2],AXIS["geodetic latitude (Lat)",north,ORDER[1],ANGLEUNIT["degree",0.0174532925199433]],AXIS["geodetic longitude (Lon)",east,ORDER[2],ANGLEUNIT["degree",0.0174532925199433]],USAGE[SCOPE["Horizontal component of 3D system."],AREA["World."],BBOX[-90,-180,90,180]],ID["EPSG",4326]]
    >>> to_type(4326, CRS)
    CRS.from_epsg(4326)
    """

    if isinstance(output_type, str):
        output_type = getattr(sys.modules["builtins"], output_type)

    if isinstance(input_value, Enum):
        input_value = input_value.name

    output_type = subscripted_type(output_type)

    if output_type is None:
        input_value = None
    elif output_type is Any:
        return input_value

    if isinstance(output_type, Collection):
        collection_type = type(output_type)
        if collection_type is not EnumMeta:
            if not issubclass(collection_type, Mapping):
                if input_value is not None:
                    output_type = list(output_type)
                    if not isinstance(input_value, Iterable) or isinstance(input_value, str):
                        try:
                            evaluated_value = ast.literal_eval(input_value)
                            if not isinstance(evaluated_value, Collection):
                                raise TypeError()
                            input_value = evaluated_value
                        except:
                            if isinstance(input_value, str):
                                if '\n' in input_value:
                                    entries = input_value.splitlines()
                                elif ',' in input_value:
                                    entries = input_value.split(",")
                                else:
                                    entries = [input_value]
                                input_value = [entry.strip() for entry in entries]
                            else:
                                input_value = [input_value]
                    if len(output_type) == 1:
                        output_type = [output_type[0] for _ in input_value]
                    elif len(output_type) == len(input_value):
                        output_type = output_type[: len(input_value)]
                    else:
                        raise ValueError(
                            f"unable to convert list of values of length {len(input_value)} "
                            f"to list of types of length {len(output_type)}: "
                            f"{input_value} -/> {output_type}"
                        )
                    input_value = collection_type(
                        to_type(input_value[index], current_type)
                        for index, current_type in enumerate(output_type)
                    )
                else:
                    input_value = collection_type()
            elif isinstance(input_value, str):
                input_value = json.loads(input_value)

            elif isinstance(input_value, Mapping):
                converted_items = []
                key_to_type = list(output_type)[0]
                value_to_type = output_type[key_to_type]
                for key, sub_value in input_value.items():
                    key = to_type(key, key_to_type)
                    converted_items.append((key, to_type(sub_value, value_to_type)))
                input_value = collection_type(converted_items)
            elif "pyproj" in installed_packages():
                from pyproj import CRS

                if isinstance(input_value, CRS):
                    input_value = input_value.to_json_dict()
        elif input_value is not None:
            try:
                input_value = output_type[input_value]
            except (KeyError, ValueError):
                try:
                    input_value = output_type(input_value)
                except (KeyError, ValueError) as error:
                    raise ValueError(
                        f'unrecognized entry "{input_value}"; must be one of {list(output_type)}'
                    ) from error
    elif type(input_value) is not output_type and input_value is not None:
        if isinstance(input_value, timedelta):
            if issubclass(output_type, str):
                hours, remainder = divmod(input_value, timedelta(hours=1))
                minutes, remainder = divmod(remainder, timedelta(minutes=1))
                seconds = remainder / timedelta(seconds=1)
                input_value = f"{hours:02}:{minutes:02}:{seconds:04.3}"
            else:
                input_value /= timedelta(seconds=1)
        elif "pyproj" in installed_packages():
            from pyproj import CRS

            if isinstance(input_value, CRS):
                if issubclass(output_type, str):
                    input_value = input_value.to_wkt()
                elif issubclass(output_type, dict):
                    input_value = input_value.to_json_dict()
                elif issubclass(output_type, int):
                    input_value = input_value.to_epsg()
        if issubclass(output_type, bool):
            try:
                input_value = ast.literal_eval(f"{input_value}")
            except ValueError:
                input_value = bool(input_value)
        elif issubclass(output_type, (datetime, date)):
            with contextlib.suppress(ModuleNotFoundError, TypeError):
                from dateutil.parser import parse as parse_date

                input_value = parse_date(input_value)
            if (
                    issubclass(output_type, datetime)
                    and isinstance(input_value, date)
                    and not isinstance(input_value, datetime)
            ):
                input_value = datetime.combine(input_value, time(0, 0, 0))
            elif issubclass(output_type, date) and not issubclass(output_type, datetime):
                input_value = input_value.date()

        elif issubclass(output_type, timedelta):
            if isinstance(input_value, str) and ":" in input_value:
                parts = [float(part) for part in input_value.split(":")]
                if len(parts) > 4:
                    raise ValueError(f'unable to parse timedelta from input "{input_value}"')
                components = {}
                if len(parts) > 3:
                    components["days"] = parts.pop(0)
                if len(parts) > 2:
                    components["hours"] = parts.pop(0)
                components["minutes"] = parts[0]
                components["seconds"] = parts[1]
                input_value = timedelta(**components)
            else:
                input_value = timedelta(seconds=float(input_value))
        elif "shapely" in installed_packages():
            from shapely import wkb, wkt
            from shapely.errors import GEOSException
            from shapely.geometry import shape as shapely_shape
            from shapely.geometry.base import GEOMETRY_TYPES

            if output_type.__name__ in GEOMETRY_TYPES:
                try:
                    input_value = wkb.loads(input_value, hex=True)
                except:
                    try:
                        input_value = wkt.loads(input_value)
                    except:
                        try:
                            input_value = wkb.loads(input_value)
                        except (TypeError, GEOSException):
                            if isinstance(input_value, str):
                                input_value = ast.literal_eval(input_value)
                            try:
                                input_value = shapely_shape(input_value)
                            except:
                                input_value = output_type(input_value)

        if not isinstance(input_value, output_type):
            if isinstance(input_value, (str, bytes)):
                try:
                    input_value = output_type.from_string(input_value)
                except AttributeError:
                    input_value = output_type(input_value)
            else:
                input_value = output_type(input_value)

    return input_value
