import logging
import time
from subprocess import PIPE, Popen

from .cli_response import CLIResponse
from .return_codes import ReturnCodes


class BaseCLI:
    def __init__(self, name, custom_path='', allure=None, sudo=False):
        self.name = name
        self.path = custom_path
        self.allure = allure
        self.logger = logging.getLogger(__name__)
        self.sudo = sudo

    def _log_request(self, command, arguments, sudo):
        rq_msg = f'INPUT: {"sudo " if sudo else ""}{self.name} {command or ""}'
        if arguments:
            rq_msg += f' {" ".join(arguments)}'
        self.logger.info(rq_msg)
        if self.allure:
            self.allure.attach(rq_msg, 'INPUT', attachment_type=self.allure.attachment_type.TEXT)

    def _log_response(self, process, output, error, start_time, end_time):
        rs_msg = f'OUTPUT (code {process.returncode}, elapsed time {"{0:.2f}".format(end_time - start_time)}s):'
        rs_msg = f'{rs_msg}\n{output or error or "<EMPTY MESSAGE>"}'
        self.logger.info(rs_msg)
        if self.allure:
            self.allure.attach(rs_msg, 'OUTPUT', attachment_type=self.allure.attachment_type.TEXT)

    def do(self, command: str, *args, **kwargs) -> CLIResponse:
        _args = [arg for arg_group in args for arg in _parse_command(arg_group)]

        is_sudo = self.sudo or ('sudo' in kwargs and kwargs.get('sudo'))

        _cmd = ['sudo'] if is_sudo else []
        _cmd.extend([f'{self.path}{self.name}', *_parse_command(command), *_args])

        self._log_request(command, _args, is_sudo)
        start_time = time.time()

        process = Popen(_cmd, stdout=PIPE, stderr=PIPE)
        output, error = (_bytes.decode().strip() for _bytes in process.communicate())

        end_time = time.time()
        self._log_response(process, output, error, start_time, end_time)

        return CLIResponse(status=ReturnCodes(process.returncode), output=output, error=error)


def _parse_command(command):
    commands = []
    chars = []
    is_quoted = False

    if not command:
        return commands

    for char in command:
        if char == '"':
            is_quoted = not is_quoted
        if char in [' ', '='] and not is_quoted:
            commands.append(''.join(chars))
            chars = []
        else:
            chars.append(char)
    commands.append(''.join(chars))

    return commands
