from typing import Union

from bin.requirements.dtos.python_requirement_dto import PythonRequirementDto
from bin.requirements.dtos.sem_ver_requirement_dto import SemVerRequirementDto
from bin.requirements.dtos.shell_requirement_dto import ShellRequirementDto

RequirementDto = Union[SemVerRequirementDto, PythonRequirementDto, ShellRequirementDto]
