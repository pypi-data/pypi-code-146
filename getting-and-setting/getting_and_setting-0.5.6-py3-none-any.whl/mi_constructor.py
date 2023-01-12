from typing import TypedDict
from typing import Optional
from typing import Type
from typing import Dict
from typing import Literal
from typing import List
from typing import Union
from dataclasses import make_dataclass
from dataclasses import field
from dataclasses import fields

from . mi_models import MiTransactionMetadata

_TYPES: Dict[str, Type] = {
    'Alpha': str,
    'Integer': int
}

class MiMeta(TypedDict):
    name: str
    description: str
    fieldtype: str
    length: str
    mandetory: Literal['true', 'false']

class PyMeta(TypedDict):
    name: str
    description: str
    fieldtype: type
    length: int
    mandetory: bool
    
    
def mi_meta_to_py_meta(meta: MiMeta) -> PyMeta:
    """ Converts metadata strings from the MiApi to python types and values """
    return {
        'name': meta['name'],
        'description': meta['description'],
        'fieldtype': _TYPES[meta['fieldtype']],
        'length': int(meta['length']),
        'mandetory': True if meta['mandetory'] == 'true' else False
    }
    

def construct_dataclass_from_meta(name: str, metadata: List[MiMeta]):
    metadata_ = [mi_meta_to_py_meta(r) for r in metadata]
    
    return make_dataclass(
        name,
        [
            (
                r['name'],
                r['fieldtype'] if r['mandetory'] else Optional[r['fieldtype']], 
                field(
                    default_factory=r['fieldtype'],
                    metadata={
                        'length': r['length'],
                        'description': r['description']
                    }
                )
            )    
            for r in metadata_
        ]
    )



