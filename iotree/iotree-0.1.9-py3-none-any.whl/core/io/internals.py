import orjson
import yaml
import toml
import soup2dict as std
import xmltodict as xtd

from bs4 import BeautifulSoup
from typing import Union, List, Dict, Any, Optional, Tuple, Callable, Iterable

def __call__any(funcs: List[Callable], *args, **kwargs) -> Any:
    """Try all callables in a list until one succeeds."""
    for f in funcs:
        try:
            return f(*args, **kwargs)
        except Exception as e:
            continue
    if "msg" in kwargs:
        raise ValueError(f'All functions failed. {kwargs["msg"]}')
    else:
        msg = [
            f"\n - {funcs[0].__name__} failed with args: {args} and kwargs: {kwargs}" for f in funcs
        ]
        msg = "f'All calls failed:" + "".join(msg)
        raise ValueError(msg)

orjson_options = orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_SERIALIZE_DATACLASS | orjson.OPT_SERIALIZE_UUID | orjson.OPT_NAIVE_UTC | orjson.OPT_INDENT_2 

format_dict = {
    "formats": ['.json', '.yaml', '.toml', '.xml', '.html'],
    "readers": [
        lambda path : orjson.loads(open(path,'rb').read()),
        lambda path : yaml.safe_load(open(path, 'r')),
        lambda path : toml.loads(open(path, 'r').read()),
        lambda path : xtd.parse(open(path, 'r').read()),
        lambda path : std.convert(BeautifulSoup(open(path, 'r').read(), 'html.parser'))
    ],
    "writers": [
        lambda data, path : open(path, 'wb+').write(orjson.dumps(data, option=orjson_options)),
        lambda data, path : yaml.safe_dump(data, open(path, 'w+')),
        lambda data, path : toml.dump(data, open(path, 'w+')),
        lambda data, path : open(path, "w+").write(xtd.unparse(data)),
        lambda data, path : open(path, "w+").write(std.convert(data, as_json=True))
    ],
}

format_dict["readers_compact"] = { k : v for k, v in zip(format_dict["formats"], format_dict["readers"]) }
format_dict["writers_compact"] = { k : v for k, v in zip(format_dict["formats"], format_dict["writers"]) }



def write_any(data, path) -> Any:
    """Try all writers in a list until one succeeds."""
    return __call__any(format_dict["writers"], data, path)

def read_any(funcs: List[Callable], *args, **kwargs) -> Any:
    """Try all readers in a list until one succeeds."""
    return __call__any(format_dict["readers"], path)