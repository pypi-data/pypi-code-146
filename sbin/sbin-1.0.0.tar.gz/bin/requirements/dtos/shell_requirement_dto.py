from typing import Optional

from bin.models.bin_base_model import BinBaseModel
from bin.models.str_command import StrCommand
from bin.requirements.dtos.base_requirement_dto import BaseRequirementDto
from bin.requirements.requirement import Requirement
from bin.requirements.shell_requirement import ShellRequirement


class ShellRequirementDto(BinBaseModel, BaseRequirementDto):
    name: str
    met_if: StrCommand
    help: Optional[str]

    def to_requirement(self) -> Requirement:
        return ShellRequirement(name=self.name, met_if_cmd=self.met_if, help=self.help)
