"""
ONGOING WORK
"""

from pathlib import Path

from typing import Dict, Iterable, Union, List

from ..defs import FMT_SRCDOCUMENT, DOC_TYPES
from ..dump import dump_text, dump_yaml
from ..helper.exception import InvArgException, InvalidDocument
from ..helper.io import load_datafile, base_extension

from .localdoc import BaseLocalSrcDocument


TYPE_CHUNK = Union[Dict, str, List]



# --------------------------------------------------------------------------


class IndexedLocalSrcDocument(BaseLocalSrcDocument):
    """
    A dict-like interface for a local source document
    """

    def __init__(self, doc: BaseLocalSrcDocument):
        """
        """
        # how can we use references in prev & next context chunks???
        self.doc = {chunk['id']: chunk for chunk in doc}

    def __iter__(self):
        return iter(self.doc)

    def __getitem__(self, chunkid):
        return self.doc[chunkid]

    def keys(self):
        pass

    def values(self):
        pass

    def items(self):
        pass

    def __getattr__(self, name):
        return getattr(self.doc, name)
