#!/usr/bin/env python3

"""
Description of the data to be processed.
"""

from pathlib import Path
from typing import Any, Dict

from pudb import set_trace as bp  # noqa: F401

import radiocc
from radiocc.model import RadioDataType

DESCRIPTOR_FILE_NAME = "descriptor.yaml"


class Descriptor:
    """Structure representation of the description of the data to be processed."""

    def __init__(self, META_KERNEL: str, RADIO_DATA_TYPE: RadioDataType) -> None:
        # Path to the folder containing the data to be processed.
        self.META_KERNEL = META_KERNEL

        # Type of the radio data.
        self.RADIO_DATA_TYPE = RADIO_DATA_TYPE

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to hashmap."""
        return dict(
            meta_kernel=self.META_KERNEL,
            radio_data_type=self.RADIO_DATA_TYPE.name,
        )


class DescriptorBuilder:
    """
    Builder of the structure representation of the description of the data to be
    processed.
    """

    __META_KERNEL: str
    __RADIO_DATA_TYPE: RadioDataType

    def __init__(self) -> None:
        pass

    def meta_kernel(self, META_KERNEL: str) -> "DescriptorBuilder":
        """Set meta kernel folder path."""
        self.__META_KERNEL = META_KERNEL
        return self

    def radio_data_type(self, TYPE: RadioDataType) -> "DescriptorBuilder":
        """Set radio data type."""
        self.__RADIO_DATA_TYPE = TYPE
        return self

    def build(self) -> Descriptor:
        """Build Descriptor."""
        return Descriptor(self.__META_KERNEL, self.__RADIO_DATA_TYPE)


def load(PATH: Path) -> Descriptor:
    """Load descriptor from a file."""
    CONTENTS = radiocc.utils.read_yaml(PATH)

    builder = DescriptorBuilder()
    builder.meta_kernel(CONTENTS.meta_kernel)
    builder.radio_data_type(CONTENTS.radio_data_type)

    return builder.build()
