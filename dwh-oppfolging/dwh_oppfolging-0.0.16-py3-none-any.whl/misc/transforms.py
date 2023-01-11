from datetime import datetime
import hashlib
import json
import re
import pendulum
from pendulum.datetime import DateTime as PendulumDateTime
#import pytz


def string_to_naive_norwegian_datetime(
    string: str
) -> datetime:
    """converts string to a naive pendulum datetime, stripping any timezone info if naive is true
    and adjusting time using the utc offset of the tz_name timezone instead.
    >>> string_to_naive_norwegian_datetime("2022-05-05T05:05:05+01:00").isoformat()
    '2022-05-05T06:05:05'
    """
    pdl_dt = pendulum.parser.parse(string)
    assert isinstance(pdl_dt, PendulumDateTime)
    pdl_dt = pdl_dt.in_timezone("Europe/Oslo")
    pdl_dt = pdl_dt.naive()
    return pdl_dt


#def string_to_naive_norwegian_datetime(x: datetime.datetime):  # pylint: disable=invalid-name
#    """returns naive datetime offset by norwegian utc (lifted from dvh-kafka-python)
#    >>> old_dt(datetime.datetime.fromisoformat("2022-05-05T05:05:05+01:00")).isoformat()
#    '2022-05-05T06:05:05'
#    """
#    timezone = pytz.timezone("Europe/Oslo")
#    if x.tzinfo is not None:
#        x = (x - x.utcoffset()).replace(tzinfo=None)  # type: ignore
#    x += timezone.utcoffset(x, is_dst=True)  # type: ignore
#    return x


def datetime_to_naive_norwegian_datetime(dt: datetime):
    """converts datetime to naive norwegian datetime
    >>> datetime_to_naive_norwegian_datetime(datetime.fromisoformat("2022-05-05T05:05:05+01:00")).isoformat()
    '2022-05-05T06:05:05'
    """
    return string_to_naive_norwegian_datetime(dt.isoformat())


def string_to_code(string: str) -> str:
    """converts a string to a code string conforming to dwh standard
    >>> string_to_code("/&$  ØrkEn Rotte# *;-")
    'ORKEN_ROTTE'
    >>> string_to_code(" ??? ")
    'UKJENT'
    """
    code = string.upper().replace("Æ", "A").replace("Ø", "O").replace("Å", "AA")
    code = "_".join(
        word
        for word in re.findall(
            r"(\w*)",
            code,
        )
        if word
    )
    code = "UKJENT" if code == "" else code
    return code


def dict_to_string(dictionary: dict) -> str:
    """Returns a json dump of the dict
    >>> dict_to_string({"x": 2, "y": 3})
    '{"x": 2, "y": 3}'
    """
    string = json.dumps(dictionary, ensure_ascii=False)
    return string


def string_to_sha256_hash(string: str) -> str:
    """Returns the sha256 hash of the utf-8 encoded string as a hex-numerical string
    >>> string_to_sha256_hash("Hello, world!")
    '315f5bdb76d078c43b8ac0064e4a0164612b1fce77c869345bfc94c75894edd3'
    """
    sha = hashlib.sha256(string.encode("utf-8")).hexdigest()
    return sha
