from bin.models.bin_base_model import BinBaseModel
from bin.models.str_command import StrCommand
from bin.virtualenv.venv import Venv


class VenvDto(BinBaseModel):
    create: StrCommand
    exists: StrCommand
    activate: StrCommand
    remove: StrCommand

    def to_venv(self) -> Venv:
        return Venv(create_cmd=self.create, exists_cmd=self.exists, activate_cmd=self.activate, remove_cmd=self.remove)
