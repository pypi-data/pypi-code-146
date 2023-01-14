"""
Ignore this Mess
Just for Trial Purpose...
"""

import enum

class List(list):
    __doc__ = ""
    
    @property
    def __setattr__(self):
      raise AttributeError("Core Dumped!")

    __setitem__ = {}.__setitem__
  
    @property
    def __len__(self):
      return [].__len__

    @property
    def append(self):
        raise AttributeError("Read only Attribute...")

    @property
    def pop(self):
        raise AttributeError("Read only Attribute...")

    @property
    def clear(self):
        raise AttributeError("Read only Attribute...")

    @property
    def extend(self):
        raise AttributeError("Read only Attribute...")

    @property
    def insert(self):
        raise AttributeError("Read only Attribute...")


enum._make_class_unpicklable(List)
