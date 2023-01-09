"""Utility functions concerning data sources."""

from dataclasses import dataclass
from typing import Dict, Union

import numpy as np
import pandas as pd

from bitfount.data.types import DataPathModifiers


@dataclass
class OphthalmologyDataSourceArgs:
    """Arguments for ophthalmology data.

    Args:
        oct_string: The string pointing to OCT files in the filename. Defaults to 'OCT'.
            Refers to Optical Coherence Tomography (OCT), typically these are a series
            of 2D images used to show a cross-section of the tissue layers in the
            retina (specifically the macula), combined to form a 3D image.
        slo_string: The string pointing to SLO files in the filename. Defaults to
            'SLO_IR'. Refers to Scanning Laser Ophthalmoscope (SLO), typically referred
            to as an 'en-face' image of the retina (specifically the macula).
    """

    oct_string: str = "OCT"
    slo_string: str = "SLO_IR"


def _modify_column(
    column: Union[np.ndarray, pd.Series],
    modifier_dict: DataPathModifiers,
) -> Union[np.ndarray, pd.Series]:
    """Modify the given column.

    Args:
        column: The column you are operating on.
        modifier_dict: A dictionary with the key as the
            prefix/suffix and the value to be prefixed/suffixed.
    """
    # Get the modifier dictionary:
    for modifier_type, modifier_string in modifier_dict.items():
        if modifier_type == "prefix":
            column = modifier_string + column.astype(str)

        elif modifier_type == "suffix":
            column = column.astype(str) + modifier_string
    return column


def _modify_file_paths(
    data: pd.DataFrame, modifiers: Dict[str, DataPathModifiers]
) -> None:
    """Modifies image file paths if provided.

    Args:
        data: The dataframe to modify.
        modifiers: A dictionary with the column name and
            prefix and/or suffix to modify file path.
    """
    for column_name in modifiers:
        # Get the modifier dictionary:
        modifier_dict = modifiers[column_name]
        data[column_name] = _modify_column(data[column_name], modifier_dict)
