from typing import Dict, Union

from bin.custom_commands.dtos.command_tree_dto import CommandTreeDto
from bin.custom_commands.dtos.str_custom_command_dto import StrCustomCommandDto

CustomCommandsDto = Dict[str, Union[CommandTreeDto, StrCustomCommandDto]]
