from typing import Optional
import uuid
import array
import numpy as np

from quickstats.interface.root import TObject, TArrayData
from quickstats.interface.root import load_macro
from quickstats.interface.cppyy.vectorize import as_np_array, vector_to_pointer

class TF1(TObject):
    
    def __init__(self, f:"ROOT.TF1"):
        self.f = f
        
    def GenerateRandomArray(self, size:int, xmin:Optional[float]=None, xmax:Optional[float]=None,
                            fmt:str="pointer"):
        import ROOT
        if (xmin is None) and (xmax is None):
            rand_arr = ROOT.TF1Utils.GetRandomArray(self.f, size)
        else:
            rand_arr = ROOT.TF1Utils.GetRandomArray(self.f, size, xmin, xmax)
        if fmt == "numpy":
            return as_np_array(rand_arr)
        elif fmt == "vector":
            return rand_arr
        elif fmt == "pointer":
            return vector_to_pointer(rand_arr)
        raise ValueError(f'invalid output format: {fmt}')