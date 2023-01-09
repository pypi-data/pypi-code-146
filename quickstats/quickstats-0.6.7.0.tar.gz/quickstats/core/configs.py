from typing import Dict, List, Optional, Union, Tuple, Any, Callable
import os
import re
import sys
import copy
import fnmatch

from .enums import GeneralEnum
from .abstract_object import AbstractObject

from dataclasses import MISSING, _MISSING_TYPE


class BasicConfigTypes(GeneralEnum):
    NONE        = (0, lambda x: x is None)
    ANY         = (1, lambda x: True)
    STR         = (2, lambda x: isinstance(x, str))
    FLOAT       = (3, lambda x: isinstance(x, (int, float)))
    BOOL        = (4, lambda x: isinstance(x, bool))
    INT         = (5, lambda x: isinstance(x, int))
    LIST        = (6, lambda x: isinstance(x, list))
    DICT        = (7, lambda x: isinstance(x, dict))
    
    def __new__(cls, value:int, validate_method:Callable):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.validate = validate_method
        return obj

class CompositeConfigTypes(object):
    
    def __init__(self, signature:str):
        nest_level = signature.count("[")
        if nest_level == 0:
            # interpret as basic type
            config_type = BasicConfigTypes.parse(signature)
            self.name = config_type.name
            self.validate = config_type.validate
        else:
            if signature.count("]") != nest_level:
                raise ValueError(f'Incomplete bracket in the type signature "{signature}"')
            type_strings = signature.strip("]").split("[")
            config_types = []
            for type_string in type_strings:
                try:
                    config_type = BasicConfigTypes.parse(type_string)
                except Exception as e:
                    raise ValueError(f'Failed to parse the type signature "{signature}". An error '
                                     f'was received when parsing the component "{type_string}": {e}')
                config_types.append(config_type)
            if len(config_types) != (nest_level + 1):
                raise ValueError(f'Found spurious brackets in the type signature "{signature}"')
            if not all(config_type in [BasicConfigTypes.LIST, BasicConfigTypes.DICT] \
                       for config_type in config_types[:-1]):
                raise ValueError(f'Invalid nested type signature "{signature}": only dictionary or list nestings are allowed')
            validate = None
            for config_type in config_types[::-1]:
                validate = self._create_nested_lambda(config_type, validate)
            self.name = signature
            self.validate = validate
            
    def _create_nested_lambda(self, config_type, lambda_func):
        if lambda_func is None:
            return config_type.validate
        if config_type == BasicConfigTypes.LIST:
            return lambda x : isinstance(x, list) and all(lambda_func(y) for y in x)
        elif config_type == BasicConfigTypes.DICT:
            return lambda x : isinstance(x, dict) and all(lambda_func(y) for y in x.values())
        return None

class ConfigComponent(object):
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        assert isinstance(value, str)
        self._name = value
    
    @property
    def dtypes(self):
        return self._dtypes
    
    @dtypes.setter
    def dtypes(self, value):
        if isinstance(value, (tuple, list)):
            self._dtypes = [CompositeConfigTypes(v) for v in value]
        else:
            self._dtypes = [CompositeConfigTypes(value)]
    
    @property
    def required(self):
        return self._required
    
    @required.setter
    def required(self, value):
        assert isinstance(value, bool) 
        self._required = value
        
    @property
    def required_strict(self):
        return self._required_strict
    
    @required_strict.setter
    def required_strict(self, value):
        assert isinstance(value, bool) 
        self._required_strict = value        
        
    @property
    def default(self):
        return self._default
    
    @default.setter
    def default(self, value):
        if value == MISSING:
            self._default = MISSING
        else:
            self.type_check(value)
            self._default = value
            
    @property
    def default_factory(self):
        return self._default_factory
    
    @default_factory.setter
    def default_factory(self, value):
        if value == MISSING:
            self._default_factory = MISSING
        else:
            self.type_check(value())
            self._default_factory = value            
    
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        assert isinstance(value, (str, type(None)))
        self._description = value
    
    @property
    def example(self):
        return self._example
    
    @example.setter
    def example(self, value):
        assert isinstance(value, (str, type(None)))
        self._example = value    
    
    @property
    def choice(self):
        return self._choice
    
    @choice.setter
    def choice(self, value):
        if value is None:
            self._choice = None
        else:
            assert isinstance(value, (tuple, list))
            for v in value:
                self.type_check(v)
            self._choice = value
        
    @property    
    def deprecated(self):
        return self._deprecated
    
    @deprecated.setter
    def deprecated(self, value):
        assert isinstance(value, bool)
        self._deprecated = value
        
    @property
    def deprecation_message(self):
        return self._deprecation_message   
    
    @deprecation_message.setter
    def deprecation_message(self, value):
        assert isinstance(value, (str, type(None)))
        self._deprecation_message = value
    
    def __init__(self, dtypes:Union[str, Tuple[str], List[str]]="ANY",
                 name:str="",
                 required:bool=False,
                 default:Optional[Any]=MISSING,
                 default_factory:Optional[Callable]=MISSING,
                 description:Optional[str]=None,
                 example:Optional[str]=None,
                 choice:Optional[List[Any]]=None,
                 deprecated:bool=False,
                 deprecation_message:Optional[str]=None):
        self.name = name
        self.dtypes = dtypes
        self.required = required
        self.required_strict = False
        self.choice = choice
        self.default = default
        self.default_factory = default_factory
        if ((not isinstance(self.default, _MISSING_TYPE)) and
            (not isinstance(self.default_factory, _MISSING_TYPE))):
            raise ValueError('cannot specify both default and default_factory')
        self.description = description
        self.example = example
        self.deprecated = deprecated
        self.deprecation_message = deprecation_message      
        
    def type_check(self, value):
        passed = any(dtype.validate(value) for dtype in self.dtypes)
        if not passed:
            raise RuntimeError(f'Type check failed for the config component "{self.name}". '
                               f'Allowed types: {", ".join([dtype.name for dtype in self.dtypes])}')
            
    def has_default(self):
        return ((not isinstance(self.default, _MISSING_TYPE)) or 
                (not isinstance(self.default_factory, _MISSING_TYPE)))
    
    def get_default(self):
        if not isinstance(self.default, _MISSING_TYPE):
            return self.default
        if not isinstance(self.default_factory, _MISSING_TYPE):
            return self.default_factory()
        raise RuntimeError('default value not set')

    def validate(self, value=MISSING):
        if isinstance(value, _MISSING_TYPE):
            # throw error if missing value but no default value available
            if self.required or (self.required_strict and (not self.has_default())):
                raise RuntimeError(f'Missing value for the config component "{self.name}":\n'
                                   f'{self.get_explain_text()}')
            return self.get_default()
        self.type_check(value)
        if (self.choice is not None) and (value not in self.choice):
            raise RuntimeError(f'Invalid value for the config component "{self.name}". '
                               f'Supported values: {self.choice}')
        return value
    
    def get_explain_text(self, leftmargin:int=0, linebreak:int=100):
        components = {
            "dtype"       : "|".join([dtype.name for dtype in self.dtypes]),
            "required"    : str(self.required),
        }
        if self.has_default():
            components["default"] = str(self.get_default())
        components["description"] = self.description
        if self.example is not None:
            components["example"] = self.example
        if self.deprecated:
            components["deprecation"] = self.deprecation_message
        if self.choice is not None:
            components["choice"] = ", ".join([f"{i}" for i in self.choice])
            
        from quickstats.utils.common_utils import itemize_dict
        text = itemize_dict(components, leftmargin=leftmargin, linebreak=linebreak)
        return text

    def explain(self, linebreak:int=100):
        sys.stdout.write(self.get_explain_text(linebreak=linebreak))
    
class ConfigParser(AbstractObject):
    
    @property
    def config_format(self):
        return self._config_format
    
    @config_format.setter
    def config_format(self, value):
        if not isinstance(value, dict):
            raise ValueError("config format must be a dictionary")
        copied_value = copy.deepcopy(value)
        component_map = self.parse_config_format(copied_value)
        self._config_format = copied_value
        self._component_map = component_map
        
    @property
    def component_map(self):
        return self._component_map        
        
    def __init__(self, config_format:Dict,
                 required_components:Optional[List[str]]=None,
                 optional_components:Optional[List[str]]=None,
                 disable_message:bool=False,
                 verbosity:Optional[Union[int, str]]="INFO"):
        self.config_format = config_format
        self.set_components_requirement(required_components, optional_components)
        self.disable_message = disable_message
        
    def set_components_requirement(self, required_components:Optional[List[str]]=None,
                                   optional_components:Optional[List[str]]=None):
        
        # require everything by default
        if required_components is None:
            required_components = ["*"]
        if optional_components is None:
            optional_components = []            
        for label, component in self.component_map.items():
            component.required_strict = False
            for required_component in required_components:
                if fnmatch.fnmatch(label, required_component):
                    component.required_strict = True
                    break
            for optional_component in optional_components:
                if fnmatch.fnmatch(label, required_component):
                    component.required_strict = False
                    break
                    
    def get_required_components(self):
        components = [component for component in self.component_map.values() if component.required_strict]
        return components                
    
    def get_config_component(self, component_label:str):
        if component_label in self.component_map:
            return self.component_map[component_label]
        for label, component in self.component_map.items():
            label = label.replace("?:", "*").replace("?", "*")
            if fnmatch.fnmatch(component_label, label):
                return component
        return None
        
    def get_explain_text(self, node_label:Optional[str]="",
                         required_only:bool=False,
                         indent:str="    ", bullet:str="=>",
                         linebreak:int=100):
        if required_only:
            required_labels = set()
            for component in self.get_required_components():
                tokens = component.name.split(":")
                required_labels |= set([":".join(tokens[:i+1]) for i in range(len(tokens))])
            required_labels = list(required_labels)
        else:
            required_labels = None
        def traverse_node(config_node:Dict, level:int=0,
                          current_text:str="", config_label:str="",
                          write:bool=False, filter_labels:Optional[List[str]]=None):
            margin = indent * level
            indent_text = margin + bullet
            for key, value in config_node.items():
                if isinstance(value, ConfigComponent):
                    if (filter_labels is not None) and (value.name not in filter_labels):
                        continue
                    current_text += write * (indent_text + key + "\n")
                    current_text += write * (value.get_explain_text(leftmargin=len(indent_text.expandtabs()),
                                                                    linebreak=linebreak))
                elif isinstance(value, dict):
                    new_config_label = self._get_config_label(key, config_label)
                    new_write = write
                    if (not write):
                        match_label = new_config_label.replace("?:", "*").replace("?", "*")                        
                        if fnmatch.fnmatch(node_label, match_label):
                            new_write = True
                    if (filter_labels is not None) and (new_config_label not in filter_labels):
                        continue                            
                    current_text += new_write * (indent_text + key + "\n")
                    current_text = traverse_node(value, level + int(new_write),
                                                 current_text, new_config_label,
                                                 new_write, filter_labels)
                else:
                    raise RuntimeError("invalid config node")
            return current_text
        
        if self.get_config_component(node_label) is not None:
            component = self.get_config_component(node_label)
            text = bullet + node_label + "\n"
            text += component.get_explain_text(linebreak=linebreak)
        else:
            text = traverse_node(self.config_format, write=node_label=="",
                                 filter_labels=required_labels)
        if not text:
            if required_only:
                self.stdout.critical('ERROR: No required components matches the requested scope. '
                                     'Try using "required_only=False" instead.')
            elif node_label:
                self.stdout.critical(f'ERROR: Config node "{node_label}" does not exist.')
            else:
                self.stdout.critical(f'ERROR: Config format is empty.')                
        return text
    
    def explain(self, node_label:Optional[str]="",
                required_only:bool=False,
                indent:str="    ",
                bullet:str="=>",
                linebreak:int=100):
        sys.stdout.write(self.get_explain_text(node_label=node_label,
                                               required_only=required_only,
                                               indent=indent,
                                               bullet=bullet,
                                               linebreak=linebreak))
        
    def parse_config_format(self, config_format, label:str="",
                            component_map:Optional[Dict]=None):
        if component_map is None:
            component_map = {}
        if isinstance(config_format, ConfigComponent):
            config_format.name = label
            if label in component_map:
                raise RuntimeError(f"duplicated config component: {label}")
            component_map[label] = config_format                
        elif isinstance(config_format, dict):
            for key, value in config_format.items():
                new_label = self._get_config_label(key, label)
                if not isinstance(key, str):
                    raise ValueError(f'found non-string key in the config component "{new_label}"')
                self.parse_config_format(value, new_label, component_map)
        else:
            raise ValueError(f'found unsupported format in the config component "{label}"')
        return component_map
    
    def parse_config(self, config:Union[Dict, str]):
        if isinstance(config, str):
            extension = os.path.splitext(config)[-1]
            if not self.disable_message:
                self.stdout.info(f'INFO: Reading configuration file "{config}".')
            if extension == ".json":
                import json
                with open(config, "r") as file:
                    config = json.load(file)
            elif extension == ".yaml":
                import yaml
                with open(config, "r") as file:
                    config = yaml.safe_load(file)
            else:
                raise RuntimeError(f'Unsupported config format "{extension.strip(".")}. '
                                   'Allowed formats are: json, yaml')
        if not isinstance(config, dict):
            raise ValueError("config must be a dictionary or path to a json/yaml file")
        resolved_config = copy.deepcopy(config)
        self.validate_and_resolve(resolved_config, self.config_format)
        return resolved_config
    
    def _get_config_label(self, key:str, prefix:str=""):
        return f"{prefix}:{key}" if prefix else key
        
    def validate_and_resolve(self, config, formatter, prefix:str="",
                             extra_configs:Optional[List]=None):
        if extra_configs is None:
            extra_configs = []       
        if not isinstance(config, dict):
            return None
        if not isinstance(formatter, dict):
            raise RuntimeError("invalid config formatter")
        config_keys = list(config.keys())
        formatter_keys = list(formatter.keys())
        # optional layer
        if (formatter_keys == ["?"]) and isinstance(formatter["?"], dict):
            if (("*" not in formatter["?"]) and set(config_keys).issubset(set(formatter["?"].keys()))) or \
               (("*" in formatter["?"]) and set(formatter["?"].keys()).issubset(set(config_keys))):
                return self.validate_and_resolve(config, formatter["?"], prefix, extra_configs)
            else:
                formatter_keys = ["*" if k == "?" else k for k in formatter_keys]
        extra_keys = list(set(config_keys) - set(formatter_keys))
        if "*" not in formatter_keys:
            extra_configs += [self._get_config_label(key, prefix) for key in extra_keys]
        for key in formatter_keys:
            config_label = self._get_config_label(key, prefix)
            if (key == "*") and (key not in formatter):
                component = formatter["?"]
            else:
                component = formatter[key]
            if isinstance(component, ConfigComponent):
                if key in config:
                    config[key] = component.validate(config[key])
                elif key == "*":
                    for config_key in extra_keys:
                        config[config_key] = component.validate(config[config_key])
                else:
                    # only fill default if component is strictly required
                    if component.required_strict:
                        config[key] = component.validate(MISSING)
                        if not self.disable_message:
                            self.stdout.info(f'INFO: Auto-filled missing config component "{config_label}" with '
                                         f'default value "{config[key]}".')
            else:
                if key == "*":
                    config_keys = extra_keys
                else:
                    if key not in config:
                        config[key] = {}
                    config_keys = [key]
                for config_key in config_keys:
                    self.validate_and_resolve(config[config_key], component,
                                              config_label, extra_configs)
        return extra_configs