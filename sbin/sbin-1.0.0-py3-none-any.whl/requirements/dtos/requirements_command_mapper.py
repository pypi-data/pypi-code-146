from typing import List

from bin.commands.command import Command
from bin.requirements.dtos import RequirementDto
from bin.requirements.requirements_command import RequirementsCommand


class RequirementsCommandMapper:
    @staticmethod
    def to_command(dtos: List[RequirementDto]) -> Command:
        return RequirementsCommand(requirements=[d.to_requirement() for d in dtos])
