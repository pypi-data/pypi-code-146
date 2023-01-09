from dataclasses import dataclass
from typing import Callable, Dict
from front import ELEMENT_KEY
from streamlitfront.elements import SuccessNotification
from i2 import Sig
from streamlitfront.elements import FileUploader

from collections import defaultdict, ChainMap
import collections.abc
from dol.paths import KeyPath
from dol import Store

# recursive defaultdict
from collections import defaultdict

recursivedict = lambda: defaultdict(recursivedict)

# def update(d, u):
#     for k, v in u.items():
#         if isinstance(v, collections.abc.Mapping):
#             d[k] = update(d.get(k, {}), v)
#         else:
#             d[k] = v
#     return d

# def expand_dotted_dict(d):
#     dict_list = [process(k,v) for k, v in d.items()]
#     print(dict_list)
#     d={}
#     result=deep_update(d, dict_list)

#     return result

# def process(dotted_key, value):
#     head, *tail = dotted_key.split('.')
#     res = dict()
#     if not tail:
#         return {head:value}
#     res[head]=process('.'.join(tail), value)
#     return res

# def deep_update(mapping, *updating_mappings):
#     updated_mapping = mapping.copy()
#     for updating_mapping in updating_mappings:
#         for k, v in updating_mapping.items():
#             if k in updated_mapping and isinstance(updated_mapping[k], dict) and isinstance(v, dict):
#                 updated_mapping[k] = deep_update(updated_mapping[k], v)
#             else:
#                 updated_mapping[k] = v
#     return updated_mapping


def mk_dotted_recursive_dict():
    d = recursivedict()
    d = KeyPath('.')(d)
    return d


def todict(d):
    if not isinstance(d, defaultdict) and not isinstance(
        d, Store
    ):  # make recursivedict a type and recognize it
        return d
    return {k: todict(v) for k, v in d.items()}


dflt_template = mk_dotted_recursive_dict()
dflt_template['execution.output'] = {
    ELEMENT_KEY: SuccessNotification,
}


@dataclass
class Component:
    func: Callable = None
    label: str = None
    _configs = dflt_template
    # param_to_mall_map: Dict[str, str] = ()
    # output_store_name: str = None

    @property
    def configs(self):
        s = self._configs

        return s

    def mk_configs(self, overwrites=()):  # list of KV or
        overwrites = dict(overwrites)
        self._configs.update(overwrites)
        return self.configs

    def to_dict(self):
        return todict(self.configs)

    __call__ = mk_configs


if __name__ == '__main__':  # put in a module in plunk and make it a test
    from plunk.sb.front_demo.user_story1.utils.funcs import upload_sound
    from pprint import pprint

    upload_component = Component(func=upload_sound)
    pprint(upload_component.to_dict())
    result = upload_component.mk_configs(
        {
            'execution.inputs.train_audio': {
                ELEMENT_KEY: FileUploader,
                'type': 'wav',
                'accept_multiple_files': True,
            },
        }
    )
    pprint(upload_component.to_dict())
