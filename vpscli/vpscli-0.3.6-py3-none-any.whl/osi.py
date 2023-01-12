import subprocess
from dataclasses import dataclass

import codefast as cf


class Symbols:
    smiley = '😀'
    sad = '😞'
    question = '❓'
    info = 'ℹ️'
    warning = '⚠️'
    error = '🚫'
    success = '✅'
    fail = '❌'
    ok = '✅'
    turtule = '🐢'
    mokey = '🐵'


@dataclass
class Cmd:
    pre_msg: str = ''
    command: str = ''
    post_msg: str = ''


class BashRunner:
    @staticmethod
    def get_hostname():
        return subprocess.check_output(['hostname']).decode('utf-8').strip()

    @staticmethod
    def get_output(command: str) -> str:
        try:
            return subprocess.check_output(
                command.split(' ')).decode('utf-8').strip()
        except subprocess.CalledProcessError:
            return ''

    @staticmethod
    def call(command: str) -> int:
        '''return 0 if no error occurs'''
        return subprocess.call(command, shell=True)

    @staticmethod
    def call_with_msg(cmd_obj: Cmd) -> None:
        cf.info(cmd_obj.pre_msg)
        resp = BashRunner.call(cmd_obj.command)
        if resp == 0:
            cf.info(cmd_obj.post_msg + ' ' + Symbols.success)
        else:
            raise Exception(f'{cmd_obj.post_msg} failed')

    @staticmethod
    def get_app_path(app_name: str) -> str:
        resp = BashRunner.get_output('which {}'.format(app_name))
        if resp and resp.endswith(app_name):
            return resp
        return '/usr/local/bin/{}'.format(app_name)

    @staticmethod
    def check_if_app_installed(app_name: str) -> bool:
        resp = BashRunner.get_output('apt-cache policy {}'.format(app_name))
        return 'Installed: (none)' not in resp
