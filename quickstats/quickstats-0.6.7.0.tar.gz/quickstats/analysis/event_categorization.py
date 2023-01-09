from typing import Optional, Union, List, Dict, Tuple
import os
import math
import json
from itertools import combinations, combinations_with_replacement

import numpy as np
import pandas as pd

from quickstats import semistaticmethod, DescriptiveEnum, Timer
from quickstats.maths.numerics import str_encode_value
from quickstats.maths.statistics import (get_poisson_interval, get_counting_significance,
                                         get_combined_counting_significance)
from quickstats.utils.common_utils import is_valid_file, combine_dict
from quickstats.parsers import ParamParser
from .data_loading import DataLoader
from .multi_class_boundary_tree import MultiClassBoundaryTree
from .data_preprocessing import get_class_label_encodings

class CategorizationOutputMode(DescriptiveEnum):
    MINIMAL  = (0, "Save only outputs needed for statistical evaluation")
    MINITREE = (1, "Save minitrees for all test samples")
    ARRAY    = (2, "Save arrays(csv/h5) for all test samples")
    STANDARD = (3, "Save arrays(csv/h5) and minitrees for all test samples")
    FULL     = (4, "Save arrays(csv/h5), histograms and minitrees for all test samples")
    
class CategorizationOutputFormat(DescriptiveEnum):
    ARRAY     = (0, "array file (csv/h5)", "categorized_array", "categorized_array_sample", "array")
    MINITREE  = (1, "ROOT file containing minitrees", "categorized_minitree", "categorized_minitree_sample", "minitree")
    HISTOGRAM = (2, "ROOT file containing histograms", "categorized_histogram", "categorized_histogram_sample", "histogram")
    
    def __new__(cls, value:int, description:str="", dirname:str="", filename:str="", short_name:str=""):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        obj.dirname = dirname
        obj.filename = filename
        obj.short_name = short_name
        return obj

class EventCategorization(DataLoader):
    
    REQUIRED_CONFIG_COMPONENTS = ["paths:arrays", "paths:model", "paths:output",
                                  "samples:*", "kinematic_regions:*",
                                  "variables:*", "training:*", "channels:*",
                                  "observables:*", "categorization:*",
                                  "benchmark:*", "names:weight", "names:event_number"]
    
    def __init__(self, study_name:str, target_channels:List[str],
                 analysis_config:Optional[Union[Dict, str]]=None,
                 array_dir:Optional[str]=None, outdir:Optional[str]=None,
                 data_preprocessor=None, do_blind:bool=True,
                 verbosity:Optional[Union[int, str]]="INFO",
                 **kwargs):
        """
        Module for performing event categorization based on score outputs from the machine learning
        model.
        
        Parameters
        ----------
        study_name: str
            Name of the study (for grouping outputs)
        target_channels: list of str
            List of channels to be included in the study
        analysis_config_path: str
            Path to the central configuration file of the analysis
        outdir: (optional) str
            Save outputs to a custom directory instead of the default directory
            from the configuration file (i.e. config['paths']['outputs'])
        array_dir: (optional) str
            Load csv array inputs from a custom directory instead of the default
            directory from the configuration file (i.e. config['paths']['arrays'])
        data_preprocessor: callable function
            Function for preprocessing input data after which the output is
            fed to the machine learning model for prediction
        do_blind: bool
            Perform a blind analysis. This will remove data events from the signal region when
            saving outputs for statistical tests.
        verbosity: (optional) str
            Message verbosity level. Available chocie: ['DEBUG', 'INFO', 'WARNING', 'ERROR']
        """
        super().__init__(analysis_config=analysis_config,
                         array_dir=array_dir,
                         outdir=outdir,
                         verbosity=verbosity,
                         **kwargs)
        
        # append the study name to the output directory
        self.set_study_name(study_name)
        self.do_blind  = do_blind
        self.data_preprocessor = data_preprocessor
        self.models = None
        self.initialize_channels(target_channels)
        self.reset_channel_information()
        self.boundary_trees = {}
        self.summary    = {}
        self.category_yields     = {}
        self.category_yields_err = {}
        self.benchmark_significance = {}
    
    def reset_channel_information(self) -> None:
        self.active_channel = None
        self.channel_df     = None
        self.channel_config = None
        
    def set_active_channel(self, channel:str) -> None:
        if channel not in self.target_channels:
            raise ValueError(f"{channel} is not a target channel of this study")
        self.reset_channel_information()
        self.active_channel = channel
        self.channel_config = self.channel_configs[channel]
        
    def set_models(self, models:Dict)-> None:
        """
        Define machine learning models used for categorization.
        
        Parameters
        ----------
        models: dictionary
            A dictionary with key as the channel name and value as the machine learning model used
            to evaluate event-level scores.
        """
        channel_models = {}
        for channel in self.target_channels:
            model = models.get(channel, None)
            if model is None:
                raise ValueError(f"missing model for the channel: {channel}")
            channel_models[channel] = model
        self.models = channel_models
        
    def validate(self, check_model:bool=False, check_df:bool=False,
                 check_boundaries:bool=False, check_categories:bool=False,
                 check_channels:bool=False) -> None:
        """
        Check if inputs are available for various steps in the categorization procedure.

        Parameters
        ----------
        check_model: bool, default = False
            Check whether machine learning models are defined for the active channel.
        check_df: bool, default = False
            Check whether the channel-level sample dataframes are loaded.
        check_boundaries: bool, default = False
            Check whether the channel-level boundaries are defined.
        check_categories: bool, default = False
            Check whether the channel-level categories are defined.
        check_channels: bool, default = False
            Check whether boundaries for all channels are defined
        """
        if self.active_channel is None:
            raise RuntimeError("active channel not set")
        if check_model and ((self.models is None) or (self.models.get(self.active_channel, None) is None)):
            raise RuntimeError(f'model for the channel "{self.active_channel}" not set')
        if check_df and (not self.channel_df):
            raise RuntimeError(f"channel dataframes not initialized")
        if check_boundaries and (self.active_channel not in self.boundary_trees):
            raise RuntimeError(f"channel score boundaries not defined")
        if check_categories:
            class_labels = self.get_class_labels()
            columns = [self.get_category_column_name(class_label) for class_label in class_labels]
            for sample in self.channel_df:
                if not set(columns).issubset(self.channel_df[sample].columns):
                    raise RuntimeError("category columns not defined")
        if check_channels:
            category_names = self.get_all_category_names(valid_only=True)
            involved_channels = set([self.get_category_channel(category_name) for category_name in category_names])
            missing_channels = set(self.target_channels) - involved_channels
            if len(missing_channels) > 0:
                raise RuntimeError(f'missing boundary information for the channel(s): {", ".join(missing_channels)}')
    
    def resolve_train_samples(self, channel:str) -> List[str]:
        channel_config  = self.config['channels'][channel]
        train_samples   = self.resolve_samples(channel_config['train_samples'])
        # add samples that are indirectly used in the training
        indirect_train_samples = self.resolve_samples(channel_config.get('indirect_train_samples', []))
        train_samples.extend(indirect_train_samples)
        return train_samples
    
    def initialize_channels(self, target_channels:List[str], **kwargs) -> None:
        """
        Initializes channel-level information used in the categorization procedure.

        Parameters
        ----------
        target_channels: list of string
            Channels to perform the initialization.
        """
        
        bc_ds = self.config["categorization"]["boundary_scan"].get("datasets", None)
        eval_ds = self.config["categorization"]["evaluation"].get("datasets", None)
        if bc_ds is not None:
            self.stdout.info("INFO: Boundary scan will be performed on the following analysis "
                            f"dataset(s): {', '.join(bc_ds)}")
        else:
            self.stdout.info("INFO: Boundary scan will be performed on the full analysis dataset.")
        if eval_ds is not None:
            self.stdout.info("INFO: Statistical evaluation will be performed on the following analysis "
                            f"dataset(s): {', '.join(eval_ds)}")
        else:
            self.stdout.info("INFO: Statistical evaluation will be performed on the full analysis dataset.")
            
        self.target_channels = self.resolve_channels(target_channels)
        channel_configs  = {}
        channel_metadata = {}
        for channel in self.target_channels:
            self.stdout.info(f'INFO: Initializing configuration for the channel "{channel}"')
            channel_config  = self.config['channels'][channel]
            train_variables = self.resolve_variables(channel_config['train_variables'])
            train_samples   = self.resolve_train_samples(channel)
            test_samples    = self.resolve_samples(channel_config['test_samples'])
            num_class = len(channel_config["class_labels"])
            # check that class labels are valid
            if num_class == 2:
                class_labels = set(channel_config["class_labels"].keys())
                if class_labels != set(["0", "1"]):
                    raise RuntimeError('binary classification must have class labels "0" (background) '
                                       'and "1" (signal)')
            elif num_class < 2:
                raise RuntimeError("number of training classes can not be less than 2")
            class_labels = channel_config['class_labels']
            class_label_encodings = get_class_label_encodings(list(class_labels.keys()))
            # set up score labels, category labels for the given classes
            class_metadata = {}
            category_metadata = {}
            if num_class > 2:
                buffer = []
                for class_label in channel_config["counting_significance"]:
                    class_metadata[class_label] = {
                        "score_column_name"    : f'{class_label}_{self.names["score"]}',
                        "category_column_name" : f'{class_label}_{self.names["category"]}',
                        "encoded_index"        : class_label_encodings[class_label],
                        "counting_significance": channel_config["counting_significance"][class_label]
                    }
                    buffer_new = []
                    n_boundaries = class_metadata[class_label]["counting_significance"]["n_boundaries"]
                    for i in range(n_boundaries + 1):
                        if len(buffer) == 0:
                            index = tuple([i])
                            label = f"{class_label}_{i}"
                            category_metadata[index] = {
                                "label": label,
                                "valid": False
                            }
                            buffer_new.append((label, index))
                        else:
                            for j in buffer:
                                index = tuple(list(j[1]) + [i])
                                label = f"{j[0]}_{class_label}_{i}"
                                category_metadata[index] = {
                                    "label": label,
                                    "valid": False
                                }
                                buffer_new.append((label, index))
                    buffer.extend(buffer_new)
            # binary classification, single score                
            else:
                class_metadata[None] = {
                    "score_column_name"    : self.names["score"],
                    "category_column_name" : self.names["category"],
                    "encoded_index"        : None,
                    "counting_significance": channel_config["counting_significance"]
                }
                n_boundaries = class_metadata[None]["counting_significance"]["n_boundaries"]
                for i in range(n_boundaries + 1):
                    category_metadata[i] = {
                        "label": str(i),
                        "valid": False
                    }
            
            channel_configs[channel] = {
                "train_variables"   : train_variables,
                "train_samples"     : train_samples,
                "test_samples"      : test_samples,
                "num_class"         : num_class,
                "selection"         : channel_config.get("selection", None),
                "kinematic_region"  : channel_config.get("kinematic_region", None),
                "exclude_categories": channel_config["exclude_categories"]
            }

            channel_metadata[channel] = {
                "classes"   : class_metadata,
                "categories": category_metadata
            }
        self.channel_configs  = channel_configs
        self.channel_metadata = channel_metadata
    
    def _parse_channel(self, channel:Optional[str]=None):
        if channel is None:
            self.validate()
            channel = self.active_channel
        elif channel not in self.target_channels:
            raise RuntimeError(f'channel "{channel}" is not a target channel of this study')
        return channel
        
    def get_boundary_tree(self, channel:Optional[str]=None) -> MultiClassBoundaryTree:
        """
        Get boundary data in a given channel.
        
        Parameters
        ----------
        channel: (optional) str
            The channel from which the boundary data are retrieved.
            By default, the current channel is used.
        """        
        channel = self._parse_channel(channel)
        if channel not in self.boundary_trees:
            raise RuntimeError(f'boundaries not initialized for the channel "{channel}"')
        return self.boundary_trees[channel]
    
    def get_class_labels(self, channel:Optional[str]=None) -> List[str]:
        """
        Get class labels in a given channel.
        
        Parameters
        ----------
        channel: (optional) str
            The channel from which the class labels are retrieved.
            By default, the current channel is used.
        """
        channel = self._parse_channel(channel)
        class_labels = list(self.channel_metadata[channel]["classes"].keys())
        return class_labels
    
    def get_class_metadata(self, class_label:Optional[str]=None,
                           channel:Optional[str]=None) -> Dict:
        """Get metadata of a class defined in machine learning training in a given channel.
        
        Arguments:
            class_label: (optional) str
                Name of the class defined in machine learning training.
            channel: (optional) str
                The channel from which the class_label is retrieved.
                By default, the current channel is used.
        """
        channel = self._parse_channel(channel)
        class_metadata = self.channel_metadata[channel]["classes"]
        if class_label not in class_metadata:
            raise ValueError(f'undefined class label: "{class_label}"')
        return class_metadata[class_label]
        
    def get_score_column_name(self, class_label:Optional[str]=None,
                              channel:Optional[str]=None) -> str:
        """Get score column name associated with the class label in a given channel.
        
        Arguments:
            class_label: (optional) str
                The class label for which the corresponding score column name should be obtained.
                In case of binary classification, the class label can be omitted.
            channel: (optional) str
                The channel from which the score column name is retrieved.
                By default, the current channel is used.
        """
        class_metadata = self.get_class_metadata(class_label=class_label,
                                                 channel=channel)
        return class_metadata["score_column_name"]
    
    def get_category_column_name(self, class_label:Optional[str]=None,
                                 channel:Optional[str]=None) -> str:
        """
        Get category column name associated with the class label in a given channel.
        
        Parameters
        ----------
        class_label: str
            The class label for which the corresponding category column name should be obtained.
            In case of binary classification, the class label can be omitted.
        channel: (optional) str
            The channel from which the category column name is retrieved.
            By default, the current channel is used.
        """
        class_metadata = self.get_class_metadata(class_label=class_label,
                                                 channel=channel)
        return class_metadata["category_column_name"]
    
    def get_category_label(self, index:Union[int, Tuple[int], List[int]],
                           channel:Optional[str]=None) -> str:
        """
        Get category label associated with the category index in a given channel.
        
        Parameters
        ----------
        index: int, tuple of int, list of int
            The category index that the category label is associated with.
        channel: (optional) str
            The channel from which the category label is retrieved.
            By default, the current channel is used.
        """
        
        channel = self._parse_channel(channel)
        category_metadata = self.channel_metadata[channel]["categories"]
        if isinstance(index, list):
            index = tuple(index)
        if index not in category_metadata:
            raise RuntimeError(f'no category with index "{index}" found in the channel "{channel}"')
        return category_metadata[index]["label"]
    
    def get_category_name(self, index_or_label:Union[str, int, Tuple[int], List[int]],
                          channel:Optional[str]=None) -> str:
        """
        Get category name associated with the category index/label in a given channel.
        
        Parameters
        ----------
        index: str, int, tuple of int, list of int
            The category index/label that the category name is associated with.
        channel: (optional) str
            The channel from which the category name is retrieved.
            By default, the current channel is used.
        """        
        channel = self._parse_channel(channel)
        if isinstance(index_or_label, str):
            category_label = index_or_label
        else:
            category_label = self.get_category_label(index_or_label, channel=channel)
        category_name  = f"{channel}_{category_label}"
        return category_name
    
    def get_category_index(self, label:str, channel:Optional[str]=None):
        """
        Get category index associated with the category label in a given channel.
        
        Parameters
        ----------
        label: str
            The category label that the category index is associated with.
        channel: (optional) str
            The channel from which the category index is retrieved.
            By default, the current channel is used.
        """           
        channel = self._parse_channel(channel)
        category_metadata = self.channel_metadata[channel]["categories"]
        for index, data in category_metadata.items():
            if (data["label"] == label) or (f'{channel}_{data["label"]}' == label):
                return index
        raise RuntimeError(f'no category with label "{label}" found in the channel "{channel}"')
        
    def get_category_channel(self, category_name:str):
        """
        Get channel associated with the given category name.
        
        Parameters
        ----------
        category_name: str
            The category name that the channel is associated with.
        """
        for channel in self.target_channels:
            category_metadata = self.channel_metadata[channel]["categories"]
            for index in category_metadata:
                if self.get_category_name(index, channel=channel) == category_name:
                    return channel
        raise RuntimeError(f'no category named "{category_name}" found')
        
    def get_category_labels(self, channel:Optional[str]=None, valid_only:bool=True) -> List[str]:
        """
        Get all category labels in a given channel.
        
        Parameters
        ----------
        channel: (optional) str
            The channel from which the category labels are retrieved.
            By default, the current channel is used.
        valid: bool, default = True
            Whether to filter invalid categories.
        """
        channel = self._parse_channel(channel)
        category_metadata = self.channel_metadata[channel]["categories"]
        if valid_only:
            return [data["label"] for data in category_metadata.values() if data["valid"]]
        return [data["label"] for data in category_metadata.values()]
    
    def get_category_indices(self, channel:Optional[str]=None,
                             valid_only:bool=True) -> List[Union[int, Tuple[int]]]:
        """
        Get all category indices in a given channel.
        
        Parameters
        ----------
        channel: (optional) str
            The channel from which the category indices are retrieved.
            By default, the current channel is used.
        valid: bool, default = True
            Whether to filter invalid categories.
        """
        channel = self._parse_channel(channel)
        category_metadata = self.channel_metadata[channel]["categories"]
        if valid_only:
            return [index for index, data in category_metadata.items() if data["valid"]]
        return list(category_metadata.keys())
    
    def get_category_names(self, channel:Optional[str]=None,
                           valid_only:bool=True) -> List[str]:
        """
        Get all category names in a given channel.
        
        Parameters
        ----------
        channel: (optional) str
            The channel from which the category names are retrieved.
            By default, the current channel is used.
        valid_only: bool, default = True
            Whether to filter invalid categories.
        """
        channel = self._parse_channel(channel)
        categories = []
        category_labels = self.get_category_labels(channel=channel,
                                                   valid_only=valid_only)
        category_names = [f"{channel}_{category_label}" for category_label in category_labels]
        return category_names
    
    def get_all_category_names(self, valid_only:bool=True) -> List[str]:
        """
        Get category names in all target channels.
        
        Parameters
        ----------
        valid_only: bool, default = True
            Whether to filter invalid categories.
        """
        category_names = []
        for channel in self.target_channels:
            category_names += self.get_category_names(channel=channel,
                                                      valid_only=valid_only)
        return category_names
    
    def get_columns_to_load(self, channel:Optional[str]=None):
        """
        Get the list of columns to load from data arrays.
        
        Parameters
        ----------
        channel: (optional) str
            The channel from which the columns are retrieved.
            By default, the current channel is used.
        """
        channel = self._parse_channel(channel)
        columns = set()
        for column in ["event_number", "weight"]:
            if (column in self.names) and (self.names[column] is not None):
                columns |= set([self.names[column]])
        columns |= set(self.config["categorization"].get("save_variables", []))
        columns |= set(self.channel_configs[channel]["train_variables"])
        # columns needed for selecting analysis datasets
        for spec in self.config["training"]["datasets"]["specification"].values():
            dataset_selection_variables = spec.get("variables", [])
            columns |= set(dataset_selection_variables)
        channel_selection_variables = self.channel_configs[channel].get("selection_variables", None)
        if channel_selection_variables is not None:
            columns |= set(channel_selection_variables)
        return list(columns)
    
    def get_columns_to_save(self, channel:Optional[str]=None):
        """
        Get the list of columns to be saved in array/minitree outputs.
        
        Parameters
        ----------
        channel: (optional) str
            The channel from which the columns are retrieved.
            By default, the current channel is used.
        """
        channel = self._parse_channel(channel)
        columns = set()
        for column in ["event_number", "weight", "total_weight"]:
            if (column in self.names) and (self.names[column] is not None):
                columns |= set([self.names[column]])
        columns |= set(self.config["categorization"].get("save_variables", []))
        # score variables and category variables
        class_labels     = self.get_class_labels(channel)
        score_columns    = [self.get_score_column_name(class_label) for class_label in class_labels]
        category_columns = [self.get_category_column_name(class_label) for class_label in class_labels]
        columns |= set(score_columns)
        columns |= set(category_columns)
        if ("observable" in self.config) and ("name" in self.config["observable"]):
            columns |= set([self.config["observable"]["name"]])
        return list(columns)    
  
    def get_analysis_dataset_weight_expr(self, dataset_names:Union[List[str], str]):
        if isinstance(dataset_names, str):
            dataset_names = [dataset_names]
        effective_weight = 0
        weight_components = []
        dataset_specs = self.config["training"]["datasets"]["specification"]
        for dataset_name in dataset_names:
            if dataset_name not in dataset_specs:
                raise RuntimeError(f'analysis dataset "{dataset_name}" not defined')
            ds_selection = dataset_specs[dataset_name]["selection"]
            ds_effective_weight = dataset_specs[dataset_name]["effective_weight"]
            weight_components.append(ds_selection)
            effective_weight += ds_effective_weight
        weight_expr = " or ".join([f"({c})" for c in weight_components])
        weight_expr = f"(({weight_expr}) * {1 / effective_weight})"
        return weight_expr
    
    def get_blind_selection(self):
        # analysis specific, should be overriden
        return "1"
    
    def get_sample_weight_expr(self, sample:str, for_boundary_scan:bool=True,
                               ignore_dataset_weight:bool=False) -> str:
        """
        Get expression for filtering and weighting events.
            
        Parameters
        ----------
        sample: str
            Name of sample.
        for_boundary_scan: boolean, default = True
            Whether the expression is used for boundary scan.
        ignore_dataset_weight: boolean, default = False
            Whether to ignore weight correction from using specific analysis datasets.
            Only relevant when `for_boundary_scan` is set to True.
        """
        weight_components = []
        weight_components.append(self.names["weight"])
        train_samples = self.channel_config["train_samples"]
        if for_boundary_scan:
            # boundary scan specific selection
            bs_config = self.config["categorization"]["boundary_scan"]
            selection = bs_config.get("selection", {})
            sample_selection = selection.get(sample, None)
            if sample_selection is not None:
                weight_components.append(sample_selection)
            bs_datasets = bs_config.get("datasets", [])
            if bs_datasets and (not ignore_dataset_weight):
                if (not bs_config["adaptive_dataset"]) or (sample in train_samples):
                    weight_expr = self.get_analysis_dataset_weight_expr(bs_datasets)
                    weight_components.append(weight_expr)
        else:
            # statistical evaluation specific selection
            eval_config = self.config["categorization"]["evaluation"]
            selection = eval_config.get("selection", {})
            sample_selection = selection.get(sample, None)
            if sample_selection is not None:
                weight_components.append(sample_selection)
            eval_datasets = eval_config.get("datasets", [])
            if eval_datasets:
                if (not eval_config["adaptive_dataset"]) or (sample in train_samples):
                    weight_expr = self.get_analysis_dataset_weight_expr(eval_datasets)
                    weight_components.append(weight_expr)
            # remove data events in the signal region in case of blind analysis
            if self.is_data_sample(sample) and self.do_blind:
                blind_selection = self.get_blind_selection()
                weight_components.append(blind_selection)
        weight_expr = " * ".join(weight_components)
        # convert c expression to python expression
        weight_expr = weight_expr.replace("&&", "&")
        weight_expr = weight_expr.replace("!", "not")
        return weight_expr
    
    def apply_observable(self, df:pd.DataFrame):
        name      = self.config["observable"]["name"]
        if (name not in df.columns):
            eval_expr = self.config["observable"].get("eval_expr", None)
            if eval_expr is None:
                raise RuntimeError(f'Failed evaluate observable "{name}": no evaluation expression available. '
                                    'Please specify the expression in config["observable"]["eval_expr"]')
            df[name] = df.eval(eval_expr)
            
    def initialize_df(self, df:pd.DataFrame, sample:str,
                      apply_score:bool=True,
                      event_indices:Optional[np.ndarray]=None):
        
        # evaluate observable if not already exists
        self.apply_observable(df)
        
        use_custom_events = event_indices is not None
        weight_name = self.names["weight"]
        # weight for categorization
        cat_weight_expr = self.get_sample_weight_expr(sample, for_boundary_scan=True,
                                                      ignore_dataset_weight=use_custom_events)
        cat_weight_name = self.names["cat_weight"]
        if event_indices is None:
            df[cat_weight_name] = df.eval(cat_weight_expr)
        # validation data from cross-validation
        else:
            index_variable = self.get_event_index_variable()
            df.set_index(index_variable, inplace=True)
            df[cat_weight_name] = 0.
            # scale from validation dataset to inclsuive dataset
            inclusive_weight = df[weight_name].sum()
            selected_weight = (df.loc[event_indices])[weight_name].sum()
            weight_scale = inclusive_weight / selected_weight
            cat_weight = df.loc[event_indices].eval(cat_weight_expr) * weight_scale
            df.loc[event_indices, cat_weight_name] = cat_weight
            df.reset_index(inplace=True)

        # weight for stat analysis
        total_weight_expr = self.get_sample_weight_expr(sample, for_boundary_scan=False)
        total_weight_name = self.names["total_weight"]
        df[total_weight_name] = df.eval(total_weight_expr)

        # evaluate MVA score
        if apply_score:
            self.apply_score(df)

    def get_samples_to_load(self, channel:Optional[str]=None):
        channel = self._parse_channel(channel)
        channel_config = self.channel_configs[channel]
        return channel_config['test_samples']
    
    def set_boundary_scan_dataset_options(self, datasets:Optional[str]=None,
                                          adaptive:bool=True):
        self.config["categorization"]["boundary_scan"]["datasets"] = boundary_scan
        self.config["categorization"]["boundary_scan"]["adaptive_dataset"] = adaptive
        
    def set_evaluation_dataset_options(self, datasets:Optional[str]=None,
                                       adaptive:bool=True):
        self.config["categorization"]["evaluation"]["datasets"] = boundary_scan
        self.config["categorization"]["evaluation"]["adaptive_dataset"] = adaptive
    
    def load_channel_df(self, samples:Optional[List]=None, apply_score:bool=True,
                        event_indices:Optional[Dict[str, np.ndarray]]=None) -> None:
        if apply_score:
            self.validate(check_model=True)
        else:
            self.validate(check_model=False)
        channel = self.active_channel
        channel_selection = self.channel_config['selection']
        kinematic_region  = self.channel_config['kinematic_region']
        self.stdout.info(f"INFO: Loading inputs for the channel: {channel}")
        if samples is None:
            samples = self.get_samples_to_load()
            
        channel_df = {}
        for sample in samples:
            sample_df = self.get_sample_df(sample, columns=None,
                                           selection=channel_selection,
                                           kinematic_region=kinematic_region)
            if event_indices is not None:
                sample_event_indices = event_indices.get(sample, None)
            else:
                sample_event_indices = None
            self.initialize_df(sample_df, sample=sample,
                               apply_score=apply_score,
                               event_indices=sample_event_indices)
            channel_df[sample] = sample_df
        self.channel_df = channel_df
    
    def apply_score(self, df:pd.DataFrame) -> None:
        """
        Evaluate score value from the machine learning model using events from a given dataframe and
        append the score to a new column in the dataframe.

        Parameters
        ----------
        df: pandas.Dataframe
            The dataframe to evaluate the score and append the score column.
        """
        self.validate(check_model=True)
        channel = self.active_channel
        model = self.models[channel]
        train_variables = self.channel_config["train_variables"]
        train_data = df[train_variables]
        if self.data_preprocessor is not None:
            train_data = self.data_preprocessor(train_data)
        # use custom data format for an xgboost model
        if model.__class__.__module__.startswith("xgboost"):
            import xgboost as xgb
            train_data = xgb.DMatrix(train_data)
        score = model.predict(train_data)
        # check score quality
        score_min, score_max = np.min(score), np.max(score)
        if ((score_min < 0.) or (score_max > 1.)):
            raise RuntimeError("detected score value outside the range [0, 1]")
        
        # add score variable to dataframe
        ndim = np.ndim(score)
        num_class = self.channel_config["num_class"]

        channel_metadata = self.channel_metadata[channel]
        if num_class == 2:
            # require only output score to have dimension 1 in case of binary classification
            if (ndim != 1):
                raise RuntimeError(f"expect single output from binary classification but {ndim} received")
            score_column_name = self.get_score_column_name()
            df[score_column_name] = score
        else:
            for class_label, metadata in channel_metadata["classes"].items():
                score_column_name = self.get_score_column_name(class_label)
                class_index = metadata["encoded_index"]
                df[score_column_name] = score[:, class_index]
    
    def get_class_score_hist(self, class_label:Optional[str]=None,
                             cuts:Optional[str]=None) -> Dict[str, np.ndarray]:
        """
        Extract score distributions for the given MVA output class in the current channel
        
        Parameters
        ----------
        class_label: str
            name of the MVA output class from which the score distributions are extracted
        cuts: (optional) str
            additional cuts applied to each sample dataframes
        """
        self.validate(check_df=True)
        channel = self.active_channel
        num_class = self.channel_config["num_class"]
        if num_class == 2:
            if class_label:
                raise RuntimeError("class label is not needed for binary classification which gives only "
                                   "one score distribution")
        else:
            if not class_label:
                raise RuntimeError("class label must be given for multi-class MVA outputs to extract the "
                                   "corresponding score distributions")
        score_column_name = self.get_score_column_name(class_label)
        channel_metadata = self.channel_metadata[channel]
        scan_config = channel_metadata["classes"][class_label]["counting_significance"]
        n_bins = scan_config["n_bins"]
        bins = np.arange(0, 1, 1 / n_bins)
        signal_samples     = self.resolve_samples(scan_config["signal"])
        background_samples = self.resolve_samples(scan_config["background"])
        all_samples = self.resolve_samples(self.channel_config["test_samples"])
        all_hists   = {}
        for sample in all_samples:
            sample_df = self.channel_df[sample]
            if cuts is not None:
                sample_df =  sample_df.query(cuts,  engine="python")
            digits = np.digitize(sample_df[score_column_name], bins)
            group  = sample_df.groupby(digits)
            cat_weight_name = self.names["cat_weight"]
            bin_values  = group[cat_weight_name].sum().values
            bin_indices = group[cat_weight_name].sum().index.values - 1
            all_hists[sample] = np.zeros(n_bins)
            all_hists[sample][bin_indices] = bin_values
        signal_hists = np.zeros(n_bins)
        background_hists = np.zeros(n_bins)
        for sample in all_hists:
            if sample in signal_samples:
                signal_hists += all_hists[sample]
            elif sample in background_samples:
                background_hists += all_hists[sample]
        hists = {
            'all': all_hists,
            'signal': signal_hists,
            'background': background_hists
        }
        return hists
    
    def scan_class_bounds(self, class_score_hist, n_bins:int, n_boundaries:int,
                          minimum_yields:Optional[Dict]=None,
                          filter_regions:Optional[List[int]]=None) -> Dict:
        """
        Perform a boundary scan for the given MVA output class in the current channel
        
        Parameters
        ----------
        class_score_hist: dictionary
            A dictionary containing the histogram values for various type of samples.
        n_bins:
            Number of bins used for constructing the score histogram.
        n_boundaries:
            Number of score boundaries to use.
        minimum_yields: (optional) dictionary
            A dictionary with key as the sample that has a minimum yield requirement in
            all score regions formed from the score boundaries, and value as the value
            of the minimum yield.
        """
        all_hists = class_score_hist['all']
        signal_hists = class_score_hist['signal']
        background_hists = class_score_hist['background']
        if (n_bins != len(signal_hists)) or (n_bins != len(background_hists)):
            raise RuntimeError("number of bins requested must match the number of bins in the class score "
                               "histograms")
        with Timer() as t:
            boundary_indices  = self.get_boundary_indices(n_bins, n_boundaries)
            n_combinations = len(boundary_indices)
            self.stdout.info(f"INFO: Total number of boundary combinations: {n_combinations}")
            signal_yields     = self.get_region_yields(signal_hists, boundary_indices, filter_regions=filter_regions)
            background_yields = self.get_region_yields(background_hists, boundary_indices, filter_regions=filter_regions)
            # filter boundaries which the regions contain no signal or background yields
            valid_boundaries = np.all(background_yields != 0., axis=1) & np.all(signal_yields != 0., axis=1)
            # filter boundaries which the regions contain less than the minimum required yields for specific
            # samples such as the yy background
            if minimum_yields is not None:
                for sample in minimum_yields:
                    if sample not in all_hists:
                        raise RuntimeError(f"the sample {sample} is not used in testing")
                    min_yield = minimum_yields[sample]
                    sample_yields = self.get_region_yields(all_hists[sample], boundary_indices, filter_regions=filter_regions)
                    valid_boundaries &= np.all(sample_yields > min_yield, axis=1)
            self.stdout.info(f"INFO: Number of valid boundary combinations: {valid_boundaries.sum()}")
            if valid_boundaries.sum() == 0:
                self.stdout.info("INFO: Not enough combinations to scan due to minimum yield requirements. "
                                 "No boundaries are set.")
                return None
            combined_significances = get_combined_counting_significance(signal_yields[valid_boundaries],
                                                                        background_yields[valid_boundaries])
            bins = np.arange(0, 1, 1 / n_bins)
            max_boundary_idx = np.argmax(combined_significances)
            max_significance = combined_significances[max_boundary_idx]
            min_boundary_idx = np.argmin(combined_significances)
            min_significance = combined_significances[min_boundary_idx]
            if ((max_significance - min_significance) / min_significance) < 0.1:
                self.stdout.info("INFO: Improvement in Z is less than 10%. "
                                 "No boundaries are set.")
                return None
            max_bins         = boundary_indices[valid_boundaries][max_boundary_idx]
            max_boundary     = [bins[i] for i in max_bins]
        self.stdout.info(f"INFO: Boundary scan finished. Total time taken: {t.interval:.3f}s")
        result = {
            'boundaries'  : [round(v, 8) for v in max_boundary],
            'significance': max_significance 
        }
        return result
    
    def load_boundaries(self, filename:Optional[str]=None,
                        channel:Optional[str]=None) -> MultiClassBoundaryTree:
        """
        Load boundary information for a given channel.
        
        Parameters
        ----------
        filename: str
            Path to the json file containing the boundary data.
        channel: str
            The channel to which the boundary information is loaded.
            If None, the current channel is used.
        """
        channel = self._parse_channel(channel)
        if filename is None:
            filename = self.get_file("boundary_data", channel=channel)
        if not os.path.exists(filename):
            raise FileNotFoundError(f'boundary output "{filename}" does not exist')
        self.stdout.info(f'INFO: Cached boundary output for the channel {channel} from "{filename}"')
        boundary_tree = MultiClassBoundaryTree(score_base_name=self.names["score"])
        boundary_tree.load_tree(filename)
        self.boundary_trees[channel] = boundary_tree
        self.update_valid_categories(channel)
        self.update_summary(channel)
        return boundary_tree
                
    def scan_bounds(self, cache:bool=True) -> None:
        """
        Scan score boundaries for the current channel
        
        Parameters
        ----------
        cache: bool
            Whether to cache boundary data.
        """
        self.validate(check_df=True)
        channel = self.active_channel
        channel_config  = self.config['channels'][channel]
        boundary_tree = MultiClassBoundaryTree(score_base_name=self.names["score"])
        
        # caching
        if cache:
            # cache from existing data
            if (channel in self.boundary_trees) and (self.boundary_trees[channel]):
                return None
            # cache from boundary file
            elif self._has_file("boundary_data", channel=channel):
                filename = self.get_file("boundary_data", channel=channel)
                self.load_boundaries(filename)
                return None
            
        exclude_categories = channel_config["exclude_categories"]
        
        self.stdout.info("INFO: Scanning score boundaries...")
        # run over class
        class_labels = self.get_class_labels()
        class_metadata = self.channel_metadata[channel]["classes"]
        for depth, class_label in enumerate(class_labels):
            class_config = class_metadata[class_label]['counting_significance']
            cut_maps = boundary_tree.get_cut_maps()
            # run over preceding class regions
            for branch_index, cut_expr in cut_maps.items():
                if exclude_categories:
                    if depth == 0:
                        filter_regions = [category[depth] for category in exclude_categories]
                    else:
                        filter_regions = [category[depth] for category in exclude_categories \
                                          if category[:depth] == list(branch_index)]
                else:
                    filter_regions = None
                # multi-class case
                if class_label:
                    if branch_index is not None:
                        preceding_category_label = self.get_category_label(branch_index)
                        self.stdout.info(f"Class Name: {class_label} (region = {preceding_category_label})")
                    else:
                        self.stdout.info(f"Class Name: {class_label}")
                class_score_hist = self.get_class_score_hist(class_label, cut_expr)
                result = self.scan_class_bounds(class_score_hist,
                                                class_config['n_bins'],
                                                class_config['n_boundaries'],
                                                class_config['min_yield'],
                                                filter_regions=filter_regions)
                if result is not None:
                    # append the new boundaries to the preceding branch
                    boundary_tree.set_boundaries(class_label, **result, branch_index=branch_index)
                    self.stdout.info("\t boundaries: {}".format(result['boundaries']))
                    self.stdout.info("\t counting significance: {}".format(result['significance']))
        self.boundary_trees[channel] = boundary_tree
        self.update_valid_categories()
        self.update_summary()
    
    def update_valid_categories(self, channel:Optional[str]=None,
                                ignore_boundary_result:bool=False):
        """
        Update valid categories based on the boundary information from the current channel.
        
        Parameters
        ----------
        channel: (optional) str
            The channel from which the categories are retrieved.
            By default, the current channel is used.
        ignore_boundary_result: bool, default = False
            Ignore invalid boundaries from the boundary result. This will force all
            categories to be valid except those found in the exclude categories list. 
        """
        channel = self._parse_channel(channel)
        channel_config = self.channel_configs[channel]
        num_class = channel_config["num_class"]
        exclude_categories = channel_config["exclude_categories"]
        category_metadata = self.channel_metadata[channel]["categories"]
        boundary_tree = self.get_boundary_tree(channel)
        valid_category_indices = boundary_tree.get_branch_indices()
        if num_class == 2:
            for idx in valid_category_indices:
                if len(idx) != 1:
                    raise RuntimError(f'invalid category index {idx} from boundary tree: '
                                      f'expect index of size 1 for binary classification')
            for idx in exclude_categories:
                if not isinstance(idx, int) and (len(idx) != 1):
                    raise RuntimError(f'invalid category index {idx} from exclude categories: '
                                      f'expect index of size 1 for binary classification')
            valid_category_indices = [idx[0] for idx in valid_category_indices]
            exclude_categories = [idx[0] if not isinstance(idx, int) else idx for idx in exclude_categories]
        for category_index, category_data in category_metadata.items():
            if category_index in exclude_categories:
                category_data["valid"] = False
                continue
            if ignore_boundary_result or (category_index in valid_category_indices):
                category_data["valid"] = True
                
    def update_summary(self, channel:Optional[str]=None):
        """
        Update boundary and significance information to the category summary after boundaries are set.
        
        Parameters
        ----------
        channel: (optional) str
            The channel from which the summary information is updated.
            By default, the current channel is used.  
        """
        channel = self._parse_channel(channel)
        boundary_tree = self.get_boundary_tree(channel)
        
        boundary_summary = {}
        category_indices = self.get_category_indices(channel=channel)
        for category_index in category_indices:
            category_label = self.get_category_label(category_index, channel=channel)
            boundary_summary[category_label] = boundary_tree.get_combined_boundaries(category_index)
            
        significance_summary = boundary_tree.get_significance_summary()
        
        summary = {
            "boundary"    : boundary_summary,
            "significance": significance_summary
        }
        
        self.summary[channel] = summary
        
    def get_category_yields(self, resampling:bool=False,
                            resampling_random_state:Optional[int]=None):
        """
        Return category yields for the test samples in the current channel after category labels are applied.
        
        Parameters
        ----------
        resampling: bool, default = False
            Whether to resample the events (for bootstrapping).
        resampling_random_state: (optional) int
            The random state used to resample the events.        
        """
        self.validate(check_df=True, check_categories=True)
        channel = self.active_channel
        category_indices = self.get_category_indices()
        samples = self.channel_config['test_samples']
        weight_name = self.names["total_weight"]
        yields     = {}
        yields_err = {}
        for category_index in category_indices:
            category_name = self.get_category_name(category_index)
            yields[category_name]     = {}
            yields_err[category_name] = {}
            for sample in samples:
                is_data = self.is_data_sample(sample)
                do_blind = is_data and self.do_blind                
                category_df = self.get_category_df(sample, category_index,
                                                   do_blind=do_blind)
                key = sample
                if do_blind:
                    key = self.get_blind_sample_name(sample)
                if resampling:
                    category_df = self.get_resampled_df(category_df, random_state=resampling_random_state)
                yields[category_name][key] = float(category_df[weight_name].sum())
                if is_data:
                    #calculate poisson interval
                    poisson_interval = get_poisson_interval([yields[category_name][key]])
                    yields_err[category_name][key] = {"errlo": poisson_interval["lo"][0],
                                                      "errhi": poisson_interval["hi"][0]}
                else:
                    err_val = np.sqrt((category_df[weight_name] ** 2).sum())
                    yields_err[category_name][key] = {"errlo": err_val, "errhi": err_val}
        return yields, yields_err
    
    def update_category_yields(self):
        """
        Update category yields for the test samples in the current channel after category labels are applied.
        """        
        self.stdout.info(f"INFO: Evaluating sample yields")
        yields, yields_err = self.get_category_yields()
        channel = self.active_channel
        self.category_yields[channel]     = yields
        self.category_yields_err[channel] = yields_err
        
    def apply_category(self, df:pd.DataFrame):
        """
        Apply category label to a given sample dataframe according to the score boundaries.
        
        Parameters
        ----------
        df: pandas.DataFrame
            Sample dataframe to apply to category label.
        """
        self.validate(check_boundaries=True)
        channel       = self.active_channel
        channel_index = self.target_channels.index(channel)
        num_class     = self.channel_config['num_class']
        boundary_tree = self.get_boundary_tree()
        if num_class == 2:
            boundaries = boundary_tree.get_boundaries()
            score_column_name = self.get_score_column_name()
            cattegory_column_name = self.get_category_column_name()
            categories = 1000 * channel_index + np.digitize(df[score_column_name], boundaries)
            df[cattegory_column_name] = categories
        else:
            cut_maps = boundary_tree.get_cut_maps()
            class_labels = self.get_class_labels()
            category_column_names = [self.get_category_column_name(class_label) for class_label in class_labels]
            for category_index, cut_expr in cut_maps.items():
                masks = df.query(cut_expr).index
                columns, indices = self.pair_category_columns(category_index)
                df.loc[masks, columns]  = indices
                df.loc[masks, columns] += 1000 * channel_index
            df.fillna(-1, inplace=True)

    def apply_categories(self):
        """
        Apply category label to all sample dataframes for the current channel.
        """
        self.validate(check_df=True, check_boundaries=True)
        for sample, sample_df in self.channel_df.items():
            self.apply_category(sample_df)
    
    def pair_category_columns(self, category_index:Union[int, List[int], Tuple[int]]) -> Tuple:
        # index for binary classification
        if isinstance(category_index, int):
            return ([self.get_category_column_name()], [category_index])
        else:
            class_labels = self.get_class_labels()
            category_column_names = [self.get_category_column_name(class_label) for class_label in class_labels]
            return category_column_names[:len(category_index)], list(category_index)
    
    def get_category_query_str(self, category_or_index:Union[str, int, List[int], Tuple[int]]) -> str:
        """
        Parameters
        ----------
        category_or_index: str / int / list of int / tuple of int
            The category name or category index to perform the query.
            If string, it is interpretated as a category name (without the channel prefix).
            If any of (int, list of int, tuple of int), it is interpreted as the category
            index.
        """
        if isinstance(category_or_index, str):
            category_index = self.get_category_index(category_or_index)
        else:
            category_index = category_or_index
        
        components = []
        columns, indices = self.pair_category_columns(category_index)
        for column, index in zip(columns, indices):
            components.append(f"({column} % 1000 == {index})")
        query_str = " & ".join(components)
        return query_str
    
    def get_category_df(self, sample_or_df:Union[str, pd.DataFrame],
                        category_or_index:Optional[Union[str, int, List[int], Tuple[int]]]=None,
                        resampling:bool=False,
                        resampling_random_state:Optional[int]=None,
                        columns:Optional[List[str]]=None,
                        selection:Optional[str]=None,
                        do_blind:bool=False):
        """
        Return dataframe from a given category.
            
        Parameters
        ----------
        sample_or_df: str / pandas.DataFrame
            If str, it is the name of the sample loaded in the current channel.
            If pandas.DataFrame, it is a custom dataframe with columns containing
            the proper category indices.
        category_or_index: str / int / list of int / tuple of int
            The category name or category index to perform the query.
            If string, it is interpretated as a category name (without the channel prefix).
            If any of (int, list of int, tuple of int), it is interpreted as the category
            index.
        resampling: bool, default = False
            Whether to resample the events (for bootstrapping).
        resampling_random_state: (optional) int
            The random state used to resample the events.
        columns: (optional) list of str
            Columns to keep in the output dataframe.
        selection: (optional) str
            Additional selection applied to the dataframe.
        do_blind: bool, default = False
            Whether to apply a blind selection.
        """
        if isinstance(sample_or_df, str):
            if category_or_index in self.target_channels:
                self.validate(check_df=True)
            else:
                self.validate(check_df=True, check_boundaries=True, check_categories=True)
            df = self.channel_df[sample_or_df]
        else:
            df = sample_or_df
        if category_or_index is not None:
            if category_or_index not in self.target_channels:
                query_str = self.get_category_query_str(category_or_index)
                df = df.query(query_str)
        if selection is not None:
            df = df.query(selection)
        if do_blind:
            df = self.get_blind_df(df)
        if resampling:
            df = self.get_resampled_df(df, random_state=resampling_random_state)
        if columns is not None:
            available_columns = list(df.columns)
            valid_columns = [c for c in columns if c in available_columns]
            missing_columns = [c for c in columns if c not in available_columns]
            if len(missing_columns) > 0:
                self.stdout.debug(f'DEBUG: Found missing columns in the datafarme: {", ".join(missing_columns)}')
            df = df[valid_columns]
        return df
    
    def get_resampled_df(self, df:pd.DataFrame,
                         random_state:Optional[int]=None):
        """
        Return dataframe with resampled events (for bootstrapping).
            
        Parameters
        ----------
        df: pandas.DataFrame
            Target dataframe.
        random_state: (optional) int
            The random state used to resample the events.
        """        
        df = df[df[self.names["total_weight"]] != 0]
        df = df.sample(n=df.shape[0], replace=True, random_state=random_state)
        return df
    
    def get_blind_df(self, df:pd.DataFrame) -> pd.DataFrame:
        """
        Return dataframe with events in the signal region removed.
        
        Parameters
        ----------
        df: pandas.DataFrame
            Target dataframe.
        """
        blind_selection = self.get_blind_selection()
        if blind_selection not in ["1", None]:
            df = df.query(blind_selection)
        return df
    
    def _get_sumed_sample_yields(self, samples:List[str],
                                 category_or_index:Union[str, int, List[int], Tuple[int]],
                                 weight_name:str):
        yields = 0.
        for sample in samples:
            category_df = self.get_category_df(sample, category_or_index)
            yields += category_df[weight_name].sum()
        return yields
    
    def evaluate_benchmark_significance(self):
        self.validate(check_df=True, check_boundaries=True, check_categories=True)
        if ('benchmark' not in self.config) or ('counting_significance' not in self.config['benchmark']):
            self.stdout.info("INFO: No significance benchmark defined. Skipped evaluation.")
        benchmark_config = self.config['benchmark']['counting_significance']
        benchmarks = list(benchmark_config)
        benchmark_significance = {}
        channel = self.active_channel
        category_labels = self.get_category_labels(valid_only=True)
        for benchmark in benchmarks:
            benchmark_significance[benchmark] = {}
            signal_samples     = self.resolve_samples(benchmark_config[benchmark]['signal'])
            background_samples = self.resolve_samples(benchmark_config[benchmark]['background'])
            Z = []
            for category_label in category_labels:
                yield_s = self._get_sumed_sample_yields(signal_samples, category_label, self.names["cat_weight"])
                yield_b = self._get_sumed_sample_yields(background_samples, category_label, self.names["cat_weight"])
                Z_cat   = get_counting_significance(yield_s, yield_b)
                category_name = f"{channel}_{category_label}"
                benchmark_significance[benchmark][category_name] = Z_cat
                Z.append(Z_cat)
            combined_Z = float(np.sqrt(np.sum(np.array(Z) ** 2)))
            benchmark_significance[benchmark][f"{channel}_combined"] = combined_Z
        self.benchmark_significance = combine_dict(self.benchmark_significance, benchmark_significance)
        
    def update_combined_benchmark_significance(self):
        self.validate(check_channels=True)
        category_names = self.get_all_category_names()
        benchmarks = list(self.config['benchmark']['counting_significance'])
        for benchmark in benchmarks:
            if benchmark not in self.benchmark_significance:
                raise RuntimeError(f'missing benchmark information for the benchmark "{benchmark}"')
            benchmark_data = self.benchmark_significance[benchmark]
            Z = []
            for category_name in category_names:
                if category_name not in benchmark_data:
                    raise RuntimeError(f'missing benchmark information for the category "{category_name}"')
                Z.append(benchmark_data[category_name])
            combined_Z = float(np.sqrt(np.sum(np.array(Z) ** 2)))
            benchmark_data['combined'] = combined_Z
    
    def run_channel_categorization(self, channel:str, cache_boundaries:bool=True,
                                   event_indices:Optional[Dict[str, np.ndarray]]=None):
        """
        Perform event categorization for a given channel.
            
        Parameters
        ----------
        channel: str
           Name of analysis channel.
        cache: bool, default = True
           Cache categorization result.
        cat_event_number: (optional) dict
           If specified, event categorization will be performed on a specific set of events for each sample
           given in the dictionary. The format is { sample: array of event numbers }.
        """
        if event_indices is not None:
            self.stdout.info("INFO: Categorization will be done on a given set of event numbers for each sample")
        self.set_active_channel(channel)
        self.load_channel_df(event_indices=event_indices)
        self.scan_bounds(cache=cache_boundaries)
        self.apply_categories()
        self.evaluate_benchmark_significance()
    
    def save_dataframe_as_array(self, df:pd.DataFrame, savepath:str, fmt:Optional[str]=None):
        """
        Save dataframe in array (csv/ht) format.

        Parameters
        ----------
        df: pandas.DataFrame
            Dataframe to save.
        savepath: string
            Path to save the output.       
        """
        if fmt is None:
            fmt = self.get_analysis_data_format()
        if fmt == "csv":
            df.to_csv(savepath, mode="w", index=False)
        elif fmt == "h5":
            df.to_hdf(outpath, key="categorized_data", mode="w",
                      index=False, complevel=None)
        
    def save_dataframe_as_histogram(self, df:pd.DataFrame, savepath:str):
        """
        Save dataframe in root histogram format.

        Parameters
        ----------
        df: pandas.DataFrame
            Dataframe to save.
        savepath: string
            Path to save the output.       
        """
        from quickstats.components import ExtendedRFile
        kwargs = {
            "name"   : self.config["observable"]["name"],
            "n_bins" : self.config["observable"]["n_bins"],
            "xmin"   : self.config["observable"]["bin_range"][0],
            "xmax"   : self.config["observable"]["bin_range"][1],
            "column" : self.config["observable"]["name"],
            "weight" : self.names["total_weight"]
        }
        rf = ExtendedRFile(df[[kwargs["column"], kwargs["weight"]]])
        hist = rf.get_Histo1D(**kwargs)
        # remove bins with negative weights
        from quickstats.interface.root import TH1
        neg_bin_indices, neg_bin_values = TH1.remove_negative_bins(hist)
        if len(neg_bin_indices) > 0:
            index_str = [f"{i}" for i in (neg_bin_indices + 1)]
            value_str = [f"{v}" for v in neg_bin_values]
            self.stdout.warning(f'WARNING: Detected bins with negative weights '
                                f'(bins = {", ".join(index_str)}, '
                                f'weights = {", ".join(value_str)}). '
                                f'Bin weight will be set to 0.')
        rf.save_components(savepath, components=[hist])
        
    def save_dataframe_as_minitree(self, df:pd.DataFrame, savepath:str):
        """
        Save dataframe in root minitree format.

        Parameters
        ----------
        df: pandas.DataFrame
            Dataframe to save.
        savepath: string
            Path to save the output.       
        """
        from quickstats.utils.data_conversion import dataframe2root
        dataframe2root(df, savepath, self.treename)
            
    def save_channel_summary(self, channel:Optional[str]=None) -> None:
        """
        Save category summary and boundary data for a given channel.
        
        Parameters
        ----------
        channel: (optional) str
            The channel from which the category summary and boundary data are retrieved.
            By default, the current channel is used.
        """
        channel = self._parse_channel(channel)
        # save category summary
        savepath = self.get_file("category_summary", channel=channel)
        if channel not in self.summary:
            raise RuntimeError(f'category summary for the chanenl "{channel}" not initialized')
        with open(savepath, "w") as outfile:
            json.dump(self.summary[channel], outfile, indent=2)
        self.stdout.info(f'INFO: Saved category summary to {savepath}')
        # save boundary data
        savepath = self.get_file("boundary_data", channel=channel)
        boundary_tree = self.get_boundary_tree(channel=channel)
        with open(savepath, "w") as outfile:
            json.dump(boundary_tree.tree, outfile, indent=2)
        self.stdout.info(f'INFO: Saved boundary data to {savepath}')
        
    def save_channel_yields(self, channel:Optional[str]=None,
                            resampling:bool=False,
                            resampling_random_state:Optional[int]=None) -> None:
        """
        Save yield information for a given channel.
        
        Parameters
        ----------
        channel: (optional) str
            The channel from which the yield information is retrieved.
            By default, the current channel is used.
        resampling: bool, default = False
            Whether to resample the events (for bootstrapping).
        resampling_random_state: (optional) int
            The random state used to resample the events.                
        """
        channel = self._parse_channel(channel)
        if (channel not in self.category_yields) or (channel not in self.category_yields_err):
            raise RuntimeError(f'yield information for the channel "{channel}" not initialized')
        if resampling and (channel != self.active_channel):
            raise RuntimeError('resampling can only be performed on the active channel')
        if resampling:
            yields, yields_err = self.get_category_yields(resampling=resampling,
                                                          resampling_random_state=resampling_random_state)
        else:
            yields     = self.category_yields[channel]
            yields_err = self.category_yields_err[channel]
        for category, category_yields in yields.items():
            savepath = self.get_file("yield_data", category=category)
            with open(savepath, "w") as outfile:
                json.dump(category_yields, outfile, indent=2)
            self.stdout.info(f'INFO: Saved yield information to {savepath}')
        for category, category_yields_err in yields_err.items():
            savepath = self.get_file("yield_err_data", category=category)
            with open(savepath, "w") as outfile:
                json.dump(category_yields_err, outfile, indent=2)
            self.stdout.info(f'INFO: Saved yield uncertainty information to {savepath}')
            
    def _get_minimal_sample_outputs(self):
        """Get minimal set of output samples to be saved; analysis specific
        """
        ARRAY     = CategorizationOutputFormat.ARRAY
        MINITREE  = CategorizationOutputFormat.MINITREE
        HISTOGRAM = CategorizationOutputFormat.HISTOGRAM        
        minimal_samples = {
            ARRAY     : [],
            MINITREE  : [],
            HISTOGRAM : []
        }
        return minimal_samples
    
    def _get_standard_sample_outputs(self):
        """Get standard set of output samples to be saved; analysis specific
        """
        ARRAY     = CategorizationOutputFormat.ARRAY
        MINITREE  = CategorizationOutputFormat.MINITREE
        HISTOGRAM = CategorizationOutputFormat.HISTOGRAM        
        minimal_samples = {
            ARRAY     : [],
            MINITREE  : [],
            HISTOGRAM : []
        }
        return minimal_samples
    
    def _get_required_sample_outputs(self, mode:Union[str, CategorizationOutputMode]="minimal"):
        """
        Return the list of samples to be saved in array (csv/h5), histogram and minitree formats 
        in the current channel.

        The full sample list is taken from "test_samples" of a channel-level configuration.

        Parameters
        ----------
        mode: str or CategorizationOutputMode
            Output mode. Available choices are
                "minimal"  : custom minimal output mode defined by analysis
                "minitree" : save minitrees for all samples
                "array"    : save array (csv/h5) for all samples
                "standard" : custom standard output mode defined by analysis
                "full"     : save array (csv/h5), histograms and minitrees for all samples
        """
        self.validate()
        all_samples = list(self.channel_config['test_samples'])
        
        resolved_mode = CategorizationOutputMode.parse(mode)
        ARRAY     = CategorizationOutputFormat.ARRAY
        MINITREE  = CategorizationOutputFormat.MINITREE
        HISTOGRAM = CategorizationOutputFormat.HISTOGRAM
        sample_outputs = {
            ARRAY     : [],
            MINITREE  : [],
            HISTOGRAM : []
        }
        if resolved_mode == CategorizationOutputMode.MINIMAL:
            sample_outputs = self._get_minimal_sample_outputs()
        elif resolved_mode == CategorizationOutputMode.MINITREE:
            sample_outputs[MINITREE] = all_samples
        elif resolved_mode == CategorizationOutputMode.ARRAY:
            sample_outputs[ARRAY] = all_samples
        elif resolved_mode == CategorizationOutputMode.STANDARD:
            sample_outputs[ARRAY]     = all_samples
            sample_outputs[MINITREE]  = all_samples            
        elif resolved_mode == CategorizationOutputMode.FULL:
            sample_outputs[ARRAY]     = all_samples
            sample_outputs[HISTOGRAM] = all_samples
            sample_outputs[MINITREE]  = all_samples
        else:
            raise ValueError(f'unknown output mode "{mode}"')
        return sample_outputs
                
    def save_channel_outputs(self, cache:bool=True, mode:str="minimal",
                             save_yield:bool=True,
                             save_summary:bool=True,
                             resampling:bool=False,
                             resampling_random_state:Optional[int]=None,
                             **kwargs):
        """
        Save collection of category outputs for the current channel.
        
        Parameters
        ----------
        resampling: bool, default = False
            Whether to resample the events (for bootstrapping).
        resampling_random_state: (optional) int
            The random state used to resample the events.                
        """        
        
        self.validate(check_df=True, check_boundaries=True, check_categories=True)
        
        channel = self.active_channel
        columns = self.get_columns_to_save()
        
        category_indices = self.get_category_indices()
        samples = self.channel_config['test_samples']
        sample_outputs = self._get_required_sample_outputs(mode=mode)
        self.check_missing_columns(columns)
        
        if resampling:
            self.stdout.info("NOTE: Resampling mode is enabled. The following outputs will "
                             "be saved with resampled events: csv, minitree, histogram, "
                             "yield, data point.")
        save_methods = {
            CategorizationOutputFormat.ARRAY     : self.save_dataframe_as_array,
            CategorizationOutputFormat.MINITREE  : self.save_dataframe_as_minitree,
            CategorizationOutputFormat.HISTOGRAM : self.save_dataframe_as_histogram,
        }

        for output_format in sample_outputs:
            self.path_manager.makedirs([output_format.dirname])
            
        fmt = self.get_analysis_data_format() 
        # also save the channel-level df
        category_indices.append(None)
        
        for sample in samples:
            for category_index in category_indices:
                if category_index is None:
                    category_name = channel
                else:
                    category_name = self.get_category_name(category_index)
                do_blind = self.is_data_sample(sample) and self.do_blind
                df = self.get_category_df(sample, category_index,
                                          columns=columns,
                                          do_blind=do_blind,
                                          resampling=resampling,
                                          resampling_random_state=resampling_random_state)
                for output_format in CategorizationOutputFormat:
                    if sample not in sample_outputs[output_format]:
                        continue
                    savepath = self.get_file(output_format.filename, sample=sample,
                                             category=category_name, fmt=fmt)
                    if cache and os.path.exists(savepath):
                        self.stdout.info(f'INFO: Cached {output_format.short_name} output from {savepath}')
                        continue
                    save_methods[output_format](df, savepath)
                    self.stdout.info(f'INFO: Saved {output_format.short_name} output to {savepath}')
                    
        if save_yield:
            self.update_category_yields()
            self.path_manager.makedirs(["yield"])
            self.save_channel_yields(channel,
                                     resampling=resampling,
                                     resampling_random_state=resampling_random_state)
            
        if save_summary:
            self.path_manager.makedirs(["summary"])
            self.save_channel_summary(channel)
    
    def check_missing_columns(self, columns:List[str]):
        self.validate(check_df=True)
        
        missing_column_by_sample = {}
        samples = self.channel_config['test_samples']
        for sample in samples:
            missing_columns = list(set(columns) - set(self.channel_df[sample].columns))
            if len(missing_columns) > 0:
                missing_column_by_sample[sample] = missing_columns
        if len(missing_column_by_sample) > 0:
            missing_same_columns = len(set(tuple(cols) for cols in missing_column_by_sample.values())) == 1
            all_samples_missing = set(missing_column_by_sample.keys()) == set(self.channel_df.keys())
            if missing_same_columns:
                columns = list(missing_column_by_sample.values())[0]
                if all_samples_missing:
                    self.stdout.warning(f"WARNING: The following save columns are missing for all samples: "
                                        f"{', '.join(columns)}")
                else:
                    samples = list(missing_column_by_sample.keys())
                    self.stdout.warning(f"WARNING: The following save columns are missing for the samples "
                                        f"{', '.join(samples)}: {', '.join(columns)}")
            else:
                for sample, columns in missing_column_by_sample.items():
                    self.stdout.warning(f"WARNING: The following save columns are missing for the sample {sample}: "
                                        f"{', '.join(columns)}")
    
    def get_yield_files_and_description(self):
        result = {
            "yield_data"     : "yield information",
            "yield_err_data" : "yield uncertainty information"
        }
        return result
    
    def save_combined_yields(self, cache:bool=True):
        self.validate(check_channels=True)
        category_names = self.get_all_category_names()
        yield_info = self.get_yield_files_and_description()
        for yield_file, description in yield_info.items():
            merged_yield_file = f"merged_{yield_file}"
            savepath = self.get_file(merged_yield_file)
            if cache and os.path.exists(savepath):
                self.stdout.info(f"INFO: Cached combined {description} from {savepath}")
            yield_data = {}
            for category_name in category_names:
                filepath = self.get_file(yield_file, validate=True, category=category_name)
                with open(filepath, "r") as file:
                    yield_data[category_name] = json.load(file)
            with open(savepath, "w") as outfile:
                json.dump(yield_data, outfile, indent=2)
                self.stdout.info(f"INFO: Saved combined {description} to {savepath}")
                
    def save_combined_benchmark_significance(self, cache:bool=True):
        self.validate(check_channels=True)
        benchmark_savepath = self.get_file("benchmark_significance")
        if (is_valid_file(benchmark_savepath)) and cache:
            self.stdout.info(f"INFO: Cached benchmark significance data from {benchmark_savepath}")
            if not self.benchmark_significance:
                with open(benchmark_savepath, "r") as file:
                    self.benchmark_significance = json.load(file)
        elif self.benchmark_significance:
            with open(benchmark_savepath, "w") as file:
                json.dump(self.benchmark_significance, file)
                self.stdout.info(f"INFO: Saved benchmark significance data to {benchmark_savepath}")
                      
    def merge_category_outputs(self, save_yield:bool=True,
                               save_benchmark:bool=True,
                               cache:bool=True):
        for channel in self.target_channels:
            if channel not in self.boundary_trees:
                self.load_boundaries(channel=channel)
        
        self.stdout.info("INFO: Merging outputs from all channels...")
       
        if save_yield:
            self.save_combined_yields(cache=cache)

        # merge benchmark significance
        if self.benchmark_significance:
            self.update_combined_benchmark_significance()
            
        if save_benchmark:
            self.save_combined_benchmark_significance(cache=cache)
    
    def load_cached_category_df(self, category:str, samples:Optional[List[str]]=None):
        if category in self.target_channels:
            channel = category
        else:
            channel = self.get_category_channel(category)
        if samples is None:
            resolved_samples = self.channel_configs[channel]['test_samples']
        elif isinstance(samples, str):
            resolved_samples = [samples]
        else:
            resolved_samples = samples
        
        dfs = {}
        fmt = self.get_analysis_data_format()
        for sample in resolved_samples:
            sample_path = self.get_file("categorized_array_sample", sample=sample,
                                        category=category, fmt=fmt)
            if not os.path.exists(sample_path):
                raise FileNotFoundError(f'missing categorized array file for the sample "{sample}" '
                                        f'({sample_path})')
            df = DataLoader._read_data_from_file(sample_path)
            if self.is_data_sample(sample) and self.do_blind:
                df = self.get_blind_df(df)
            dfs[sample] = df
        if isinstance(samples, str):
            return dfs[samples]
        return dfs

    @staticmethod
    def get_boundary_indices(n_bins:int, n_cut:int=2):
        n = n_bins
        k = n_cut
        a = np.ones((k, n-k+1), dtype="int32")
        a[0] = np.arange(n-k+1)
        for j in range(1, k):
            reps = (n-k+j) - a[j-1]
            a = np.repeat(a, reps, axis=1)
            ind = np.add.accumulate(reps)
            a[j, ind[:-1]] = 1-reps[1:]
            a[j, 0] = j
            a[j] = np.add.accumulate(a[j])
        a = a.T
        mask = (a[:, 0] != 0)
        return a[mask]

    @staticmethod
    def get_region_yields(data:np.ndarray, boundary_indices:np.ndarray,
                          filter_regions:Optional[List[int]]=None):
        # much faster implementation
        n = data.shape[0]
        d1, d2 = boundary_indices.shape[0], boundary_indices.shape[1]
        slice_indices = np.insert(boundary_indices, [0, d2], [0, n], axis=1).flatten()
        new_data = np.insert(data, n, 0)
        result = np.add.reduceat(new_data, slice_indices).reshape(d1, d2 + 2)
        result = np.delete(result, -1, axis=1)
        # remove yields from disgarded region(s)
        if filter_regions is not None:
            result = np.delete(result, filter_regions, axis=1)
        return result