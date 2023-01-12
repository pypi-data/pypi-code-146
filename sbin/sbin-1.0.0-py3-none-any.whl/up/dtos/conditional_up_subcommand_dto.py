from typing import Any, Dict, Optional

from pydantic import root_validator

from bin.models.bin_base_model import BinBaseModel
from bin.models.str_command import StrCommand
from bin.up.conditional_up_subcommand import ConditionalUpSubcommand
from bin.up.dtos.base_up_subcommand_dto import BaseUpSubcommandDto
from bin.up.simple_up_subcommand import SimpleUpSubcommand
from bin.up.up_subcommand import UpSubcommand


class ConditionalUpSubcommandDto(BinBaseModel, BaseUpSubcommandDto):
    name: Optional[str]
    up: Optional[StrCommand]
    up_unless: Optional[StrCommand]
    down: Optional[StrCommand]
    down_unless: Optional[StrCommand]

    @root_validator(pre=True)
    def must_have_valid_format(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        up = values.get("up")
        down = values.get("down")
        if up is None and down is None:
            raise ValueError("up or down is required")

        up_unless = values.get("up_unless")
        if up is None and up_unless is not None:
            raise ValueError("up is required with up_unless")

        down_unless = values.get("down_unless")
        if down is None and down_unless is not None:
            raise ValueError("down is required with down_unless")

        return values

    def to_up_subcommand(self) -> Optional[UpSubcommand]:
        if self.up is not None and self.up_unless is not None:
            return ConditionalUpSubcommand(name=self.name or self.up, run_cmd=self.up, unless_cmd=self.up_unless)

        if self.up is not None:
            return SimpleUpSubcommand(name=self.name or self.up, run_cmd=self.up)

        return None

    def to_down_subcommand(self) -> Optional[UpSubcommand]:
        if self.down is not None and self.down_unless is not None:
            return ConditionalUpSubcommand(name=self.name or self.down, run_cmd=self.down, unless_cmd=self.down_unless)

        if self.down is not None:
            return SimpleUpSubcommand(name=self.name or self.down, run_cmd=self.down)

        return None
