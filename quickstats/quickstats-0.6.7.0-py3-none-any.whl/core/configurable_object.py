from typing import Dict, List, Optional, Union

from .decorators import semistaticmethod
from .abstract_object import AbstractObject
from .configs import ConfigParser

class ConfigurableObject(AbstractObject):
    
    CONFIG_FORMAT = {
    }
    
    REQUIRED_CONFIG_COMPONENTS = []
    
    OPTIONAL_CONFIG_COMPONENTS = []
    
    def __init__(self, config_source:Optional[Union[Dict, str]]=None,
                 disable_config_message:bool=False,
                 verbosity:Optional[Union[int, str]]="INFO",
                 **kwargs) -> None:
        
        super().__init__(verbosity=verbosity)
        
        config_parser = ConfigParser(config_format=self.CONFIG_FORMAT,
                                     required_components=self.REQUIRED_CONFIG_COMPONENTS,
                                     optional_components=self.OPTIONAL_CONFIG_COMPONENTS,
                                     disable_message=disable_config_message)
        self.config_parser = config_parser
        if config_source is not None:
            self.load_config(config_source)
        else:
            self.config = None
        
    @semistaticmethod
    def explain_config(self, node_label:Optional[str]="",
                       required_only:bool=True,
                       indent:str="    ", bullet:str="=>",
                       linebreak:int=100) -> None:
        # call from class
        if not isinstance(self, ConfigurableObject):
            config_parser = ConfigParser(config_format=self.CONFIG_FORMAT,
                                         required_components=self.REQUIRED_CONFIG_COMPONENTS,
                                         optional_components=self.OPTIONAL_CONFIG_COMPONENTS)
            config_parser.explain(node_label, required_only=required_only,
                                  indent=indent, bullet=bullet, linebreak=linebreak)
        else:
            self.config_parser.explain(node_label, required_only=required_only,
                                       indent=indent, bullet=bullet, linebreak=linebreak)
        
    def load_config(self, config_source:Optional[Union[Dict, str]]) -> None:
        self.config = self.config_parser.parse_config(config_source)