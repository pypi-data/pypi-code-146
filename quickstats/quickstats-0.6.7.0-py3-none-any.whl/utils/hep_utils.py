from typing import Optional, Union, List, Dict

import numpy as np

from quickstats.maths.numerics import get_proper_ranges

def get_analysis_region_splitting_1D(value_range:List[float], signal_range:Optional[List[float]]=None,
                                     nominal_value:Optional[float]=None):
    if value_range is not None:
        value_range = get_proper_ranges(value_range, nominal_value)
        if value_range.shape != (1, 2):
            raise ValueError("value range must be list of size 2")
    if signal_range is not None:
        if value_range is None:
            raise RuntimeError("can not define signal range without defining value range")
        signal_range = get_proper_ranges(signal_range)
        if signal_range.shape != (1, 2):
            raise ValueError("signal range must be list of size 2")
        combined_range = np.array([[value_range[0][0], signal_range[0][0]],
                                   [signal_range[0][0], signal_range[0][1]],
                                   [signal_range[0][1], value_range[0][1]]])
        combined_range = get_proper_ranges(combined_range, no_overlap=True)
        return combined_range
    return value_range