
from typing import Any

# try:
#     import ujson as json
# 
#     def json_dump(data, fp):
#         return json.dump(data, fp, ensure_ascii=False, indent=2, escape_forward_slashes=False)
# 
#     UJSON = True
# except (ImportError, ModuleNotFoundError):
#     import json
# 
#     def json_dump(data, fp):
#         return json.dump(data, fp, ensure_ascii=False, check_circular=False, indent=2)
# 
#     UJSON = False

UJSON = False
try:
    import orjson
    _json_lib = 'orjson'

    def json_dump(data, p):
        opts = orjson.OPT_INDENT_2 | orjson.OPT_APPEND_NEWLINE | orjson.OPT_SORT_KEYS
        if isinstance(p, Path):
             return p.write_bytes(orjson.dumps(data, option=opts))
        return p.write(orjson.dumps(data, option=opts))

    def json_load(p):
        if isinstance(p, Path):
            return orjson.loads(p.read_bytes())
        return orjson.loads(p.read())


except ImportError:
    try:
        import ujson
        _json_lib = 'ujson'

        def json_dump(data, p):
            if isinstance(p, Path):
                return ujson.dump(data, p.open('w'), ensure_ascii=False, indent=2, escape_forward_slashes=False)
            return ujson.dump(data, p, ensure_ascii=False, indent=2, escape_forward_slashes=False)

        def json_load(p):
            if isinstance(p, Path):
                return ujson.load(p.open())
            return ujson.load(p)

        UJSON = True
    except ImportError:
        import json
        _json_lib = 'standard'

        def json_dump(data, p):
            if isinstance(p, Path):
                return json.dump(data, p.open('w'), ensure_ascii=False, check_circular=False, indent=2)
            return json.dump(data, p, ensure_ascii=False, check_circular=False, indent=2)

        def json_load(p):
            if isinstance(p, Path):
                return json.load(p.open())
            return json.load(p)


from ruamel.std.pathlib import Path

if not hasattr(Path, 'json'):

    class JSON:
        def __init__(self, path):
            self._path = path

        def dump(self, data):
            # handle paths in dump, as e.g. orjson requires a byte stream
            # with self._path.open('w') as fp:
            #    json_dump(data, fp)
            json_dump(data, self._path)

        def load(self):
            # with self._path.open() as fp:
            #    return json.load(fp)
            return json_load(self._path)


    class MyPath:
        @property
        def json(self):
            return JSON(self)

    Path.json = MyPath.json
