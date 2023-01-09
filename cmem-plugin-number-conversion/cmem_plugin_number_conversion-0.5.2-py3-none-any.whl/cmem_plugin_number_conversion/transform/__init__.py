"""Number Conversion transform plugin module"""
from typing import Sequence
import collections

from cmem_plugin_base.dataintegration.description import (
    Plugin,
    PluginParameter,
)
from cmem_plugin_base.dataintegration.parameter.choice import ChoiceParameterType
from cmem_plugin_base.dataintegration.plugins import TransformPlugin

NUMBER_BASES = collections.OrderedDict(
    {
        "bin": "Binary",
        "oct": "Octal",
        "int": "Decimal",
        "hex": "Hexadecimal",
    }
)


@Plugin(
    label="Convert Number Base",
    plugin_id="cmem-plugin-number-conversion",
    description="Convert numbers between different number bases (binary, octal,"
                " decimal, hexadecimal).",
    documentation="""Transform plugin allows users to easily convert numbers
    from one base to another. With support for binary, octal, decimal, and hexadecimal,
    users can choose the source and target bases to suit their needs.""",
    categories=["Numeric", "Conversion"],
    parameters=[
        PluginParameter(
            name="source_base",
            label="Source Base",
            description="Source Number Base",
            param_type=ChoiceParameterType(NUMBER_BASES),
        ),
        PluginParameter(
            name="target_base",
            label="Target Base",
            description="Source Number Base",
            param_type=ChoiceParameterType(NUMBER_BASES),
        ),
    ],
)
class NumberConversion(TransformPlugin):
    """Number Conversion Transform Plugin"""

    def __init__(self, source_base: str, target_base: str):
        self.source_base = source_base
        self.target_base = target_base

    def transform(self, inputs: Sequence[Sequence[str]]) -> Sequence[str]:
        result = []
        for _ in inputs:
            for num in _:
                target_base_number = self.convert_number_to_target_base(
                    self.convert_source_base_str_to_int(num)
                )
                result.append(f"{target_base_number}")

        return result

    def convert_source_base_str_to_int(self, num: str) -> int:
        """Convert string to int"""
        base = self.source_base
        if base == "bin":
            result = int(num, base=2)
        if base == "oct":
            result = int(num, base=8)
        if base == "int":
            result = int(num, base=10)
        if base == "hex":
            result = int(num, base=16)
        return result

    def convert_number_to_target_base(self, num: int):
        """Convert int to target base number"""
        base = self.target_base
        if base == "bin":
            return bin(num)
        if base == "oct":
            return oct(num)
        if base == "int":
            return int(num)
        if base == "hex":
            return hex(num)
        return None
