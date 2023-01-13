#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File        : global_config.py
@Description : 用于项目的全局配置读取
@Date        : 2020/10/29 11:37:51
@Author      : merlinbao
@Version     : 1.0
"""

import os
import imp
import json

from typing import Dict
from pathlib import Path

from ..utils import general_funcs


class ConfigReader:

    def __init__(self, config_file):
        """ConfigReader负责配置文件的读取，并将用户写好的Stage类载入环境中

        Args:
            config_file (str): 配置文件的路径
        """

        assert config_file is not None and config_file.endswith('.py'), "Config file is invalid."

        self.load_config(config_file)
        self.register_stages()

    def load_config(self, config_file):
        config_file = ConfigReader.fix_references(config_file)
        self.config = eval(open(config_file, 'r').read())

    def register_stages(self):
        stages_dir_path = Path(general_funcs.get_proj_dir()) / 'project' / 'stages'
        assert stages_dir_path.exists(), "Stages are not defined!"

        for stage_path in stages_dir_path.glob('*.py'):
            if 'stage' in str(stage_path):
                _ = imp.load_source(stage_path.name, str(stage_path))

    def get_flows(self) -> Dict[str, Dict]:
        flow_dict = {}
        for k, v in self.config.items():
            if k.endswith('flow'):
                flow_dict[k] = v
        return flow_dict

    @staticmethod
    def fix_references(config_file):
        """修复配置文件中的路径指代为真实路径

        Args:
            config_file (str): 配置文件路径
        """

        # fix file path
        content = None
        with open(config_file, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                lines[i] = line.replace('$YF_PROJ_PATH', general_funcs.get_proj_dir())
            content = ''.join(lines)

        # make temp dir to keep fixed config file
        tmp_dir_path = Path(general_funcs.get_proj_dir()) / '.tmp' / 'config.py'
        if not tmp_dir_path.parent.exists():
            tmp_dir_path.parent.mkdir(parents=True)
        with tmp_dir_path.open('w') as f:
            f.write(content)

        return str(tmp_dir_path)

    def __str__(self):
        main_str = ''
        main_str += general_funcs.wrap_title("Flow configuration:") + '\n'
        dump_str = json.dumps(self.config, indent=4)
        # dump_str = utils.make_list_flat(dump_str, ['classes'])
        return main_str + dump_str
