from typing import Optional, Dict
import copy
from dataclasses import asdict, dataclass

class DataclassObject(object):
    
    @classmethod
    def from_dict(cls, source:Optional[Dict]=None):
        if source is None:
            return cls()
        return cls(**source)
    
    def to_dict(self):
        return asdict(self)
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                value_copy = copy.deepcopy(value)
                setattr(self, key, value_copy)