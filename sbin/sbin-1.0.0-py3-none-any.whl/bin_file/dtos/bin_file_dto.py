from typing import Any, Dict, List, Optional

from pydantic import validator

from bin.bin_file.dtos.base_bin_file_dto import BaseBinFileDto
from bin.commands.command import Command
from bin.commands.errors import CommandParseError
from bin.commands.internal.factory import InternalCommandFactory
from bin.commands.internal.log_title_command import LogTitleCommand
from bin.custom_commands.command_tree import CommandTree
from bin.custom_commands.dtos import CustomCommandsDto
from bin.custom_commands.dtos.custom_commands_mapper import CustomCommandsMapper
from bin.env.env import Env
from bin.env.log_env_command import LogEnvCommand
from bin.models.bin_base_model import BinBaseModel
from bin.process.emoji import Emoji
from bin.requirements.dtos import RequirementDto
from bin.requirements.dtos.requirements_command_mapper import RequirementsCommandMapper
from bin.up.dtos import UpSubcommandDto
from bin.up.dtos.up_command_mapper import UpCommandMapper
from bin.version.version_command import VersionCommand
from bin.virtualenv.dtos import VenvDto
from bin.virtualenv.dtos.venv_command_mapper import VenvCommandMapper

RESERVED_KEYWORDS = ["env", "req", "requirements", "venv", "up", "down", "update-bin", "--version"]
BIN_FILE_DTO_TOP_KEYS = {
    "name",
    "description",
    "env",
    "requirements",
    "venv",
    "up",
    "commands",
    "update-bin",
    "--version",
}


class ErrorMsg:
    INVALID_FILE = f"{Emoji.ERROR}  invalid bin file, details:"
    EXTRA_TOP_LEVEL_KEYWORDS = f"{Emoji.THINKING_FACE}  unexpected top level keyword"

    VALID = f"{Emoji.SUCCESS}  all good"
    ERROR = f"{Emoji.ERROR}  something is wrong"

    MUST_BE_A_LIST = f"{Emoji.ERROR}  must be a list"
    MUST_BE_A_DICT = f"{Emoji.ERROR}  must be a dictionary"
    MUST_BE_A_FLAT_DICT = f"{Emoji.ERROR}  must be a flat dictionary"

    EMPTY_REQ = f"{Emoji.SUCCESS}  none defined, weird {Emoji.THINKING_FACE}, but OK"
    EMPTY_ENV = f"{Emoji.SUCCESS}  none defined"
    EMPTY_VENV = f"{Emoji.SUCCESS}  none defined"
    EMPTY_UP = f"{Emoji.SUCCESS}  none defined"
    EMPTY_COMMANDS = f"{Emoji.SUCCESS}  none defined"

    INVALID_VENV_MSG = "must only contain: create, exists, activate, remove"
    INVALID_COMMANDS_MSG = "make sure aliases are fine and the structure is correct"
    COMMANDS_USING_RESERVED_KEYWORDS = (
        f"{Emoji.ERROR}  commands names are clashing with reserved keywords: " + ", ".join(RESERVED_KEYWORDS)
    )

    @staticmethod
    def list_valid(at: int) -> str:
        return f"@[{at}] {Emoji.SUCCESS} "

    @staticmethod
    def list_invalid(at: int) -> str:
        return f"@[{at}] {Emoji.ERROR} "

    @staticmethod
    def custom_error(msg: str) -> str:
        return f"{Emoji.ERROR}  {msg}"


class _ReqValidationDto(BinBaseModel):
    req: RequirementDto


class _UpValidationDto(BinBaseModel):
    up: UpSubcommandDto


class _CommandsValidationDto(BinBaseModel):
    commands: CustomCommandsDto


class BinFileDto(BinBaseModel, BaseBinFileDto):
    name: Optional[Any]
    description: Optional[Any]
    env: Env = Env({})
    requirements: List[RequirementDto] = []
    venv: Optional[VenvDto] = None
    up: List[UpSubcommandDto] = []
    commands: CustomCommandsDto = {}

    @validator("commands")
    def must_not_clash_with_reserved_keywords(cls, commands: CustomCommandsDto) -> CustomCommandsDto:
        if any(reserved in commands for reserved in RESERVED_KEYWORDS):
            raise ValueError("must not use reserved keywords in custom commands")

        return commands

    @classmethod
    def parse_obj_explicitly(cls, data: Dict[str, Any]) -> "BinFileDto":
        try:
            return BinFileDto.parse_obj(data)
        except Exception:
            msg = (
                f"{ErrorMsg.INVALID_FILE}\n"
                f"{cls.__validate_extra_keywords(data)}"
                f"  env         : {cls.__validate_env(data)}\n"
                f"  requirements: {cls.__validate_requirements(data)}"
                f"  venv        : {cls.__validate_venv(data)}"
                f"  up          : {cls.__validate_up(data)}"
                f"  commands    : {cls.__validate_commands(data)}"
            )
            raise CommandParseError(msg)

    def to_command(self) -> Command:
        req = InternalCommandFactory.with_setup(
            [LogTitleCommand.requirements()], RequirementsCommandMapper.to_command(self.requirements)
        )

        return InternalCommandFactory.wrap_with_env(
            self.env,
            CommandTree(
                subcommands_tree={
                    "--version": VersionCommand(),
                    "env": LogEnvCommand(env=self.env),
                    "req": req,
                    "requirements": req,
                    "up": self.__to_up(),
                    "down": self.__to_down(),
                    **self.__to_venv(),
                    **self.__to_custom_command_dict(),
                }
            ),
        )

    @classmethod
    def __validate_extra_keywords(cls, data: Dict[str, Any]) -> str:
        extra_keys = [key for key in data if key not in BIN_FILE_DTO_TOP_KEYS]
        extra_keys = sorted(extra_keys)
        if len(extra_keys) > 0:
            return f"  {ErrorMsg.EXTRA_TOP_LEVEL_KEYWORDS}: " + ", ".join(extra_keys) + "\n"

        return ""

    @classmethod
    def __validate_env(cls, data: Dict[str, Any]) -> str:
        env = data.get("env")
        if env is None:
            return ErrorMsg.EMPTY_ENV

        try:
            Env.validate(env)
            return ErrorMsg.VALID
        except ValueError as e:
            return ErrorMsg.custom_error(str(e))

    @classmethod
    def __validate_requirements(cls, data: Dict[str, Any]) -> str:
        reqs = data.get("requirements", [])
        if not isinstance(reqs, list):
            return f"{ErrorMsg.MUST_BE_A_LIST}\n"

        if len(reqs) == 0:
            return f"{ErrorMsg.EMPTY_REQ}\n"

        msg = []
        failed_once = False
        for i, req in enumerate(reqs):
            try:
                _ReqValidationDto(req=req)
                msg.append(f"    {ErrorMsg.list_valid(i)}")
            except Exception:
                msg.append(f"    {ErrorMsg.list_invalid(i)}")
                failed_once = True

        if not failed_once:
            return f"{ErrorMsg.VALID}\n"

        return f"{ErrorMsg.ERROR}\n" + "\n".join(msg) + "\n"

    @classmethod
    def __validate_venv(cls, data: Dict[str, Any]) -> str:
        if "venv" not in data:
            return f"{ErrorMsg.EMPTY_VENV}\n"

        venv = data.get("venv", {})
        if not isinstance(venv, dict):
            return f"{ErrorMsg.MUST_BE_A_FLAT_DICT}\n"

        try:
            VenvDto.parse_obj(venv)
            return f"{ErrorMsg.VALID}\n"
        except Exception:
            return f"{ErrorMsg.ERROR}\n" f"    {ErrorMsg.INVALID_VENV_MSG}\n"

    @classmethod
    def __validate_up(cls, data: Dict[str, Any]) -> str:
        ups = data.get("up", [])
        if not isinstance(ups, list):
            return f"{ErrorMsg.MUST_BE_A_LIST}\n"

        if len(ups) == 0:
            return f"{ErrorMsg.EMPTY_UP}\n"

        msg = []
        failed_once = False
        for i, up in enumerate(ups):
            try:
                _UpValidationDto(up=up)
                msg.append(f"    {ErrorMsg.list_valid(i)}")
            except Exception:
                msg.append(f"    {ErrorMsg.list_invalid(i)}")
                failed_once = True

        if not failed_once:
            return f"{ErrorMsg.VALID}\n"

        return f"{ErrorMsg.ERROR}\n" + "\n".join(msg) + "\n"

    @classmethod
    def __validate_commands(cls, data: Dict[str, Any]) -> str:
        commands = data.get("commands", {})
        if not isinstance(commands, dict):
            return f"{ErrorMsg.MUST_BE_A_DICT}"

        if len(commands) == 0:
            return f"{ErrorMsg.EMPTY_COMMANDS}"

        if any(reserved in commands for reserved in RESERVED_KEYWORDS):
            return f"{ErrorMsg.ERROR}\n    {ErrorMsg.COMMANDS_USING_RESERVED_KEYWORDS}"

        try:
            CustomCommandsMapper.to_command_dict(commands)
            return f"{ErrorMsg.VALID}"
        except Exception:
            return f"{ErrorMsg.ERROR}\n    {ErrorMsg.INVALID_COMMANDS_MSG}"

    def __to_up(self) -> Command:
        return InternalCommandFactory.with_setup(
            self.__up_down_setup(LogTitleCommand.up()),
            UpCommandMapper.to_up_command(self.up),
        )

    def __to_down(self) -> Command:
        return InternalCommandFactory.with_setup(
            self.__up_down_setup(LogTitleCommand.down()),
            UpCommandMapper.to_down_command(self.up),
        )

    def __to_venv(self) -> Dict[str, Command]:
        if self.venv is None:
            return {}

        return VenvCommandMapper.to_command_dict("venv", self.venv)

    def __to_custom_command_dict(self) -> Dict[str, Command]:
        current = CustomCommandsMapper.to_command_dict(self.commands)
        if self.venv is None:
            return current

        setup = [
            InternalCommandFactory.mute_logs(),
            VenvCommandMapper.to_create_venv_command(self.venv),
            VenvCommandMapper.to_activate_venv_command(self.venv),
            InternalCommandFactory.unmute_logs(),
        ]
        return {cmd_name: InternalCommandFactory.with_setup(setup, cmd) for cmd_name, cmd in current.items()}

    def __up_down_setup(self, title_cmd: Command) -> List[Command]:
        setup = []
        if self.venv is not None:
            setup.extend(
                [
                    LogTitleCommand.venv(),
                    VenvCommandMapper.to_create_venv_command(self.venv),
                    VenvCommandMapper.to_activate_venv_command(self.venv),
                ]
            )

        setup.append(title_cmd)
        return setup
