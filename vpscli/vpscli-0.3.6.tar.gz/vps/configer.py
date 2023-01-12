import base64
import json
import os
import pathlib
from abc import ABC, abstractmethod

import codefast as cf

from vps.bash_scripts import EMACS_CONFIG, PROMPT, UTILS, VIM_CONFIG, WARP
from vps.meta import (GOST_CONFIG_BASE64, SHADOWSOCKS_CONFIG_BASE64,
                      SUPVISOR_CONF_TEMPLATE, VPS_STATUS_DEMO)
from vps.osi import BashRunner, Cmd
from typing import Dict


class SupervisorConfig(ABC):

    def run(self):
        try:
            cf.info('update {} supervisor config file'.format(self.app_name))
            cf.io.write(self.conf, self.conf_path)
            cf.info('restart supervisor')
            BashRunner.call(f'supervisorctl update')
        except Exception as e:
            cf.error(e)


class GostConfig(SupervisorConfig):

    def __init__(self):
        self.app_name = 'gost'
        _bash = BashRunner.call('which bash')
        self.command = f'{_bash} /app/gost'
        self.conf = SUPVISOR_CONF_TEMPLATE.replace('PLACEHOLDER',
                                                   self.app_name)
        self.conf = self.conf.replace('COMMAND', self.command)
        self.conf_path = '/etc/supervisor/conf.d/{}.conf'.format(self.app_name)

        self.init_config_file()

    def init_config_file(self):
        cf.info('init gost config file')
        content = base64.b64decode(GOST_CONFIG_BASE64).decode('utf-8')
        cf.io.write(content, '/app/gost')


from abc import ABC, abstractmethod


class KOConfig(ABC):
    """Knivesout app config

    Args:
        ABC (_type_): _description_
    """

    @abstractmethod
    def run(self):
        pass

    def start_knivesd(self):
        os.system('knivesd start')

    def get_config(self) -> Dict:
        config_ = {
            "program": self.name,
            "directory": self.path,
            "command": self.command
        }
        return config_

    def init_config_file(self):
        cf.info('init {} config file'.format(self.name))
        content = self.get_config()
        try:
            cf.js.write(content, self.config_path)
        except FileNotFoundError as e:
            os.makedirs('/data/knivesd')
            cf.js.write(content, self.config_path)

    def kostart(self):
        os.system('ko start {}'.format(self.config_path))


class EndlessConfig(KOConfig):

    def __init__(self):
        self.name = 'endlessh'
        self.command = cf.shell("which endlessh").strip()
        self.path = '/tmp'
        self.config_path = '/data/knivesd/{}.json'.format(self.name)

    def run(self):
        self.start_knivesd()
        self.init_config_file()
        

class SystemConfig:

    def __init__(self) -> None:
        self.cmds = ['timedatectl set-timezone Asia/Shanghai', 'mkdir -p /app']

    def config_vim(self):
        _path = str(pathlib.Path('~/.vimrc').expanduser().resolve())
        cf.io.write(VIM_CONFIG, _path)

    def config_emacs(self):
        cf.info('configuring EMACS')
        _path = str(pathlib.Path('~/.emacs.d/init.el').expanduser().resolve())
        if not cf.io.exists(_path.strip('init.el')):
            cf.io.mkdir(_path.strip('init.el'))
        cf.io.write(EMACS_CONFIG, _path)

    def add_bash_library(self):
        '''Copy some bash scripts to local'''
        cf.io.write(UTILS, '/app/utils.sh')
        cf.io.write(WARP, '/app/warp')

    def config_PS1(self):
        '''Add color to PS1 and `ls` to be colorized.'''
        _path = str(pathlib.Path('~/.bashrc').expanduser().resolve())
        with open(_path, 'a') as f:
            f.write(PROMPT)

    def run(self):
        for cmd in self.cmds:
            str_cmd = Cmd(f'Running {cmd}', cmd, f'{cmd} finished')
            BashRunner.call_with_msg(str_cmd)

        self.add_bash_library()
        self.config_vim()
        self.config_emacs()
        self.config_PS1()


class MonitorConfig(SupervisorConfig):
    '''VPS monitor configuration'''

    def __init__(self):
        self.app_name = 'vpsmonitor'
        self.command = '/usr/local/bin/vps_monitor -vps_name {} -alert_time 08-40 -task_types vnstat -interface eth0'.format(
            BashRunner.get_hostname())
        self.conf = SUPVISOR_CONF_TEMPLATE.replace('PLACEHOLDER',
                                                   self.app_name)
        self.conf = self.conf.replace('COMMAND', self.command)
        self.conf_path = '/etc/supervisor/conf.d/{}.conf'.format(self.app_name)


class StatusMonitorConfig(SupervisorConfig):

    def __init__(self) -> None:
        self.app_name = 'vpsstatus'
        self.command = BashRunner.get_app_path('vpsstatus')
        self.conf = SUPVISOR_CONF_TEMPLATE.replace('PLACEHOLDER',
                                                   self.app_name)
        self.conf = self.conf.replace('COMMAND', self.command)
        self.conf_path = '/etc/supervisor/conf.d/{}.conf'.format(self.app_name)

        self.init_demo_config()

    def init_demo_config(self):
        """Add a demo config file for vpsstatus"""
        cf.info('init vpsstatus config file')
        _path = str(
            pathlib.Path('~/.config/vpsstatus.json').expanduser().resolve())
        cf.js.write(VPS_STATUS_DEMO, _path)


class QbittorrentConfig(SupervisorConfig):
    '''Qbittorrent configuration'''

    def __init__(self):
        self.app_name = 'qbittorrent'
        self.command = BashRunner.get_app_path('qbittorrent-nox')
        self.conf = SUPVISOR_CONF_TEMPLATE.replace('PLACEHOLDER',
                                                   self.app_name)
        self.conf = self.conf.replace('COMMAND', self.command)
        self.conf_path = '/etc/supervisor/conf.d/qbittorrent.conf'


class CalculatePrime(SupervisorConfig):
    '''NSQ consumer configuration'''

    def __init__(self):
        self.app_name = 'primeconsumer'
        self.command = BashRunner.get_app_path('calculate_prime')
        self.conf = SUPVISOR_CONF_TEMPLATE.replace('PLACEHOLDER',
                                                   self.app_name)
        self.conf = self.conf.replace('COMMAND', self.command)
        self.conf_path = '/etc/supervisor/conf.d/primeconsumer.conf'


class AbstractSystemctl(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def run(self):
        pass


class Shadowsocks(AbstractSystemctl):

    def __init__(self):
        super().__init__('shadowsocks')
        _cont = base64.b64decode(SHADOWSOCKS_CONFIG_BASE64).decode('utf-8')
        self._config = json.loads(_cont)
        self._config_path = '/etc/shadowsocks-libev/config.json'

    def run(self):
        cf.info('overwrite config file')
        cf.js.write(self._config, self._config_path)
        cf.info('restart shadowsocks')
        BashRunner.call('systemctl restart shadowsocks-libev')
        cf.warning('please check if the port is openned')


class Sar(object):

    def run(self):
        cf.info('installing sar')
        cf.net.download('https://host.ddot.cc/config_sar.pl',
                        '/tmp/config_sar.pl')
        resp = cf.shell('perl /tmp/config_sar.pl')
        cf.info(resp)
