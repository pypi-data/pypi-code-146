
import os
from typing import Optional
from pydantic import BaseModel
from pydantic.fields import ModelField
from dotenv import load_dotenv as __load_dotenv
from pathlib import Path as __Path

ENV_PATH = '.env'
__load_dotenv(ENV_PATH)

__spl = lambda a, b, c: a.split(b, 1)[c] if b in a else a
__unwrap = lambda a, b: a.removeprefix(b)[:-1] if b in a else a

#c:str=chr(39) -> ord(*single_quote*) == 39
def __get_typename(__mf: ModelField,a:str='typing.',b:str='optional[',c:str=chr(39)):
    result = str(__mf.outer_type_).removeprefix(a).lower()
    return str(__spl(__spl(__unwrap(result, b), c, 1), c, 0))

def __parse_collection(tname:str,value:str,typemap:dict[str,type]):
    result = value.split(',') if ',' in value else [value]
    etype = typemap.get(tname.replace('[', '').replace(']', ''), None)
    result = result if etype is None else [etype(v) for v in result]
    return set(result) if tname.startswith('set') else result

def __parse_value(tname:str,value:str,typemap:dict[str,type]):
    ftype = typemap.get(tname, None)
    return value if ftype is None else ftype(value.strip())

__is_collection = lambda __tname:__tname.startswith('list') or __tname.startswith('set')
def __get_value(value, tname: str):
    result, typemap = None, dict(str=str, int=int, bool=bool)
    if value:
        parser = __parse_collection if __is_collection(tname) else __parse_value
        result = parser(tname,value,typemap)
    return result


class Env(BaseModel):

    PROJECT_ID:Optional[str]


env = Env(
    **{
        name: __get_value(os.environ.get(name,''), __get_typename(field))
        for name, field in Env.__fields__.items()
    }
)


def __update_env():

    print(env.json(indent=4))

    encoding = 'utf-8'
    errors = 'ignore'
    unsuffix = lambda __str,__sub:unsuffix(__str.removesuffix(__sub)) if __str.endswith(__sub) else __str
    path = __Path(__file__).parent.parent.joinpath(ENV_PATH)
    text = unsuffix(path.read_text(encoding=encoding,errors=errors), '\n')
    kv_lines = list(filter(lambda v: '=' in v and v[0] != '=',text.splitlines(keepends=False)))
    active_env = dict((line.split('=', 1) for line in kv_lines))
    missing_fields = list(filter(lambda b: b not in active_env, Env.__fields__.keys()))
    if missing_fields:
        kv_lines.extend((f'{mf}=' for mf in missing_fields))
        path.write_text(data='\n'.join(sorted(kv_lines)),encoding=encoding,errors=errors)


if __name__ == '__main__':

    if env is not None:
        __update_env()

