import re
from typing import Optional

from bin.models.bin_base_model import BinBaseModel
from bin.models.sem_ver_spec import SemVerSpec
from bin.models.str_command import StrCommand
from bin.process.process import Process
from bin.requirements.requirement import Requirement

semver_pattern = r"\d+\.\d+\.\d+"


class SemVerRequirement(BinBaseModel, Requirement):
    name: str
    run_cmd: StrCommand
    version: SemVerSpec
    help: Optional[str]

    def is_met(self, process: Process) -> bool:
        result = process.run(self.run_cmd, capture_output=True)
        if result.has_failed():
            return False

        versions = re.findall(semver_pattern, result.stdout)
        if len(versions) == 0:
            return False

        return versions[0] in self.version

    def get_name(self) -> str:
        return self.name

    def get_help(self) -> Optional[str]:
        return self.help
