import orjson

from typing import Union, Optional

orjson_options = orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_SERIALIZE_DATACLASS | orjson.OPT_SERIALIZE_UUID | orjson.OPT_NAIVE_UTC | orjson.OPT_INDENT_2 


def dumps(data, codec: Optional[str] = "utf8") -> Union[str, bytes]:
    return orjson.dumps(data, option=orjson_options).decode(codec)