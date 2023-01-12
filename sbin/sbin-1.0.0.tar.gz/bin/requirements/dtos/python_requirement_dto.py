from bin.models.bin_base_model import BinBaseModel
from bin.models.sem_ver_spec import SemVerSpec
from bin.requirements.dtos.base_requirement_dto import BaseRequirementDto
from bin.requirements.requirement import Requirement
from bin.requirements.sem_ver_requirement import SemVerRequirement


class PythonRequirementDto(BinBaseModel, BaseRequirementDto):
    python: SemVerSpec

    def to_requirement(self) -> Requirement:
        return SemVerRequirement(
            name=f"Python {self.python}",
            run_cmd="python3 --version",
            version=self.python,
            help="Install Python @ https://www.python.org/downloads",
        )
