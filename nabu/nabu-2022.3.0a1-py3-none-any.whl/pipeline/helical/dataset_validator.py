from ..fullfield.dataset_validator import *


class HelicalDatasetValidator(FullFieldDatasetValidator):
    """Allows more freedom in the choice of the slice indices"""

    # this in the fullfield base  class is instead True
    _check_also_z = False

    def _check_slice_indices(self):
        """Slice indices can be far beyond what fullfield pipeline accepts"""
        return
