from typing import Dict, List, Optional, Union, Tuple
import os
import copy
import json

from quickstats import ConfigurableObject, ConfigComponent

from .analysis_path_manager import AnalysisPathManager
from .config_format_templates import DEFAULT_ANALYSIS_CONFIG_FORMAT

class AnalysisBase(ConfigurableObject):
    
    CONFIG_FORMAT = DEFAULT_ANALYSIS_CONFIG_FORMAT
    
    REQUIRED_CONFIG_COMPONENTS = []
    
    @property
    def names(self) -> Dict[str, str]:
        try:
            names = self.config["names"]
        except:
            names = {}
        return names
    
    def __init__(self, analysis_config:Optional[Union[Dict, str]]=None,
                 plot_config:Optional[Union[Dict, str]]=None,
                 outdir:Optional[str]=None,
                 ntuple_dir:Optional[str]=None,
                 array_dir:Optional[str]=None,
                 model_dir:Optional[str]=None,
                 path_manager:Optional[AnalysisPathManager]=None,
                 disable_config_message:bool=False,
                 verbosity:Optional[Union[int, str]]="INFO"):
        
        super().__init__(disable_config_message=disable_config_message,
                         verbosity=verbosity)
        
        if path_manager is None:
            self.path_manager = AnalysisPathManager()
        else:
            self.path_manager = path_manager
        
        self.load_analysis_config(analysis_config)
        self.load_plot_config(plot_config)
        
        paths = {
            "outdir": outdir,
            "ntuple_dir": ntuple_dir,
            "array_dir": array_dir,
            "model_dir": model_dir
        }
        for dirname, config_key in [("outdir", "outputs"),
                                    ("ntuple_dir", "ntuples"),
                                    ("array_dir", "arrays"),
                                    ("model_dir", "models")]:
            # use custom path given by the user
            if paths[dirname] is not None:
                continue
            # already defined in path manager
            if (dirname == "outdir") and (self.path_manager.base_path is not None):
                continue
            elif (dirname.replace("_dir", "") in self.path_manager.directories):
                continue
            # use path defined in config file
            try:
                paths[dirname] = self.config["paths"][config_key]
            # use path defined in the default config format
            except:
                paths[dirname] = DEFAULT_ANALYSIS_CONFIG_FORMAT["paths"][config_key].default
            
        # setup file paths used in the analysis pipeline
        self.update_paths(**paths)
                                        
    def update_paths(self, outdir:Optional[str]=None,
                     directories:Optional[Dict[str, str]]=None,
                     files:Optional[Dict[str, Union[str, Tuple[Optional[str], str]]]]=None,
                     ntuple_dir:Optional[str]=None,
                     array_dir:Optional[str]=None,
                     model_dir:Optional[str]=None):
        
        if outdir is not None:
            self.path_manager.set_base_path(outdir)
        if directories is not None:
            self.path_manager.update_directories(directories)
        if files is not None:
            self.path_manager.update_files(files)
        if ntuple_dir is not None:
            self.path_manager.set_directory("ntuple", ntuple_dir, absolute=True)
        if array_dir is not None:
            self.path_manager.set_directory("array", array_dir, absolute=True)
        if model_dir is not None:
            self.path_manager.set_directory("model", model_dir, absolute=True)
            
    def set_study_name(self, study_name:str):
        self.path_manager.set_study_name(study_name)
        if "model" in self.path_manager.directories:
            model_dir = self.path_manager.directories["model"]
            basename = os.path.basename(os.path.dirname(model_dir))
            if basename != study_name:
                model_dir = os.path.join(model_dir, study_name)
                self.path_manager.set_directory("model", model_dir)
        
    def get_study_name(self):
        return self.path_manager.study_name
    
    def get_directory(self, directory_name:str):
        return self.path_manager.get_directory(directory_name)
    
    def get_file(self, file_name:str, validate:bool=False, **parameters):
        if validate:
            self._check_file(file_name, **parameters)
        return self.path_manager.get_resolved_file(file_name, **parameters)
    
    def _has_directory(self, directory_name:str):
        return self.path_manager.directory_exists(directory_name)
    
    def _has_file(self, file_name:str, **parameters):
        return self.path_manager.file_exists(file_name, **parameters)
    
    def _check_directory(self, directory_name:str):
        self.path_manager.check_directory(directory_name)
    
    def _check_file(self, file_name:str, **parameters):
        self.path_manager.check_file(file_name, **parameters)
        
    def load_analysis_config(self, config_source:Optional[Union[Dict, str]]=None):
        if isinstance(config_source, str):
            if not os.path.exists(config_source):
                raise FileNotFoundError(f'config file "{config_source}" does not exist')
            config_path = os.path.abspath(config_source)
            self.path_manager.set_file("analysis_config", config_path)
        if config_source is None:
            self.load_config({})
        else:
            self.load_config(config_source)
        try:
            self.all_channels = list(self.config['channels'])
        except:
            self.all_channels = []
        try:
            self.all_kinematic_regions = list(self.config['kinematic_regions'])
        except:
            self.all_kinematic_regions = []
        try:
            self.all_samples = list(self.config['samples']['all'])
        except:
            self.all_samples = []
        try:
            self.extra_samples = list(self.config['samples']['extra'])
        except:
            self.extra_samples = []            
        try:
            self.all_variables = list(self.config['variables']['all'])
        except:
            self.all_variables = []
        try:
            self.treename = self.config['names']['tree_name']
        except:
            self.treename = DEFAULT_CONFIG_FORMAT["names"]["tree_name"].default
        
    def load_plot_config(self, config_source:Optional[Union[Dict, str]]=None):
        if isinstance(config_source, str):
            if not os.path.exists(config_source):
                raise FileNotFoundError(f'config file "{config_source}" does not exist')
            config_path = os.path.abspath(config_source)
            self.path_manager.set_file("plot_config", config_path)
        # use the default plot config from the framework
        if config_source is None:
            self.plot_config = {}
            return None
        elif isinstance(config_source, str):
            with open(config_source, "r") as file:
                self.plot_config = json.load(file)
        elif isinstance(config_source, dict):
            self.plot_config = copy.deepcopy(config_source)
        else:
            raise RuntimeError("invalid plot config format")  
        
    def resolve_channels(self, channels:List[str]):
        for channel in channels:
            if channel not in self.all_channels:
                raise ValueError(f"unknown channel: {channel}")
        return channels
    
    def resolve_samples(self, samples:Optional[List[str]]=None):
        if samples is None:
            return self.all_samples
        resolved_samples = []
        for sample_key in samples:
            if sample_key in self.config['samples']:
                for sample in self.config['samples'][sample_key]:
                    if sample not in resolved_samples:
                        resolved_samples.append(sample)
            elif (sample_key in self.all_samples) or (sample_key in self.extra_samples):
                resolved_samples.append(sample_key)
            else:
                raise RuntimeError(f"unknown sample \"{sample_key}\"")
        return resolved_samples

    def resolve_variables(self, variables:Optional[List[str]]=None):
        if variables is None:
            return self.all_variables
        resolved_variables = []
        for variable_key in variables:
            if variable_key in self.config['variables']:
                for variable in self.config['variables'][variable_key]:
                    if variable not in resolved_variables:
                        resolved_variables.append(variable)
            elif variable_key in self.all_variables:
                resolved_variables.append(variable_key)
            else:
                raise RuntimeError(f"unknown variable \"{variable_key}\"")
        return resolved_variables
    
    def resolve_class_labels(self, class_labels:Dict):
        resolved_class_labels = {}
        for label in class_labels:
            resolved_samples = self.resolve_samples(class_labels[label])
            for sample in resolved_samples:
                if sample not in resolved_class_labels:
                    resolved_class_labels[sample] = label
                else:
                    raise RuntimeError(f"multiple class labels found for the sample \"{sample}\"")
        return resolved_class_labels
    
    def get_analysis_data_format(self):
        try:
            fmt = self.config["data_storage"]["analysis_data_arrays"]["storage_format"]
        except:
            fmt = DEFAULT_CONFIG_FORMAT["data_storage"]["analysis_data_arrays"]["storage_format"]
        return fmt
    
    def get_event_index_variable(self):
        if "event_number" not in self.names:
            raise RuntimeError('no event index variable defined')
        index_variable = self.names["event_number"]
        return index_variable
    
    def get_blind_sample_name(self, sample:str):
        return f"{sample}_blind"
    
    def is_data_sample(self, sample:str):
        """Check whether a given sample is the observed data. Analysis specific, should be overridden.
        """
        return "data" in sample