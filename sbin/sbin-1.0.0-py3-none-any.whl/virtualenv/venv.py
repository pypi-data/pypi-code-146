from bin.models.bin_base_model import BinBaseModel
from bin.models.str_command import StrCommand


class Venv(BinBaseModel):
    create_cmd: StrCommand
    exists_cmd: StrCommand
    activate_cmd: StrCommand
    remove_cmd: StrCommand
