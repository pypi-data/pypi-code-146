from typing import Optional

from bin.models.bin_base_model import BinBaseModel
from bin.models.sem_ver_spec import SemVerSpec
from bin.models.str_command import StrCommand
from bin.requirements.dtos.base_requirement_dto import BaseRequirementDto
from bin.requirements.requirement import Requirement
from bin.requirements.sem_ver_requirement import SemVerRequirement


class SemVerRequirementDto(BinBaseModel, BaseRequirementDto):
    name: str
    run: StrCommand
    version: SemVerSpec
    help: Optional[str]

    def to_requirement(self) -> Requirement:
        return SemVerRequirement(name=self.name, run_cmd=self.run, version=self.version, help=self.help)
