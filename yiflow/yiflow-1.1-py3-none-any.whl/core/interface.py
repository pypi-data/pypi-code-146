from abc import ABC, abstractmethod

from typing import Dict, Any
from configparser import ConfigParser
from pathlib import Path

from .flow import Flow
from ..tools import ConfigReader
from ..utils import get_proj_dir


class Interface(ABC):

    def __init__(self, config_file=None, **kwargs):
        # get default settings
        setting_dict = self._get_default_settings()
        if config_file == None:
            config_file = setting_dict["config_file"]

        # read config file
        cfg_reader = ConfigReader(config_file)

        # show config
        if setting_dict["print_config"]:
            print(cfg_reader)

        # initialize flows
        flow_config_dict = cfg_reader.get_flows()
        for name, config in flow_config_dict.items():
            flow = Flow.from_config(config=config)
            setattr(self, name, flow)

    def _get_default_settings(self) -> Dict[str, Any]:
        setting_file_path = Path(get_proj_dir()) / 'project' / 'interface' / 'setting.ini'
        assert setting_file_path.exists(), "Default setting file is not provided!"

        setting = ConfigParser()
        setting.read(str(setting_file_path))
    
        # read default config file
        config_file_path = Path(get_proj_dir()) / 'project' / setting['DEFAULT'].get("config")

        # read flag if print config
        print_config = setting["DEFAULT"].getboolean("print_config")

        return dict(config_file=str(config_file_path), print_config=print_config)

    @abstractmethod
    def __call__(self, req):
        """这个方法用于和底层服务进行对接

        Args:
            req (dict): 输入的服务调用字典

        Returns:
            dict: 输出的返回结果字典
        """

        raise NotImplementedError()
