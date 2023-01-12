from typing import Union

from bin.up.dtos.conditional_up_subcommand_dto import ConditionalUpSubcommandDto
from bin.up.dtos.str_up_subcommand_dto import StrUpSubcommandDto

UpSubcommandDto = Union[ConditionalUpSubcommandDto, StrUpSubcommandDto]
