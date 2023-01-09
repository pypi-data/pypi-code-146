from typing import List, Dict, Union, Optional
import os
import copy
from itertools import chain
from dataclasses import dataclass

import pandas as pd
import numpy as np

from quickstats import (semistaticmethod, DescriptiveEnum, DataclassObject,
                        ConfigComponent, ConfigParser, ConfigurableObject)
from .analysis_base import AnalysisBase
from .data_preprocessing import fix_negative_weights, shuffle_arrays, get_class_label_encodings

@dataclass
class SampleTransformation(DataclassObject):
    normalize_weight: bool = False

@dataclass
class DatasetTransformation(DataclassObject):
    scale_weight_by_mean: bool = False
    negative_weight_mode: int = 0
    random_state: int = None 

class DataTransformer(object):
    
    def __init__(self, sample_weight_scales:Optional[Dict]=None,
                 sample_transformation:Optional[Dict]=None,
                 dataset_transformation:Optional[Dict]=None,
                 **kwargs):
        self.set_sample_weight_scales(sample_weight_scales)
        self.sample_transformation  = SampleTransformation.from_dict(sample_transformation)
        self.dataset_transformation = DatasetTransformation.from_dict(dataset_transformation)
        
    def set_random_state(self, random_state:Optional[int]=-1):
        self.dataset_transformation.random_state = random_state
        
    @semistaticmethod
    def make_copy(self, x:pd.DataFrame, y:pd.DataFrame,
                  weight:Optional[pd.DataFrame]=None):
        x_copy = x.copy()
        y_copy = y.copy()
        if weight is not None:
            weight_copy = weight.copy()
        else:
            weight_copy = None
        return x_copy, y_copy, weight_copy
    
    def transform_sample_data(self, x:pd.DataFrame, y:pd.DataFrame,
                              weight:Optional[pd.DataFrame]=None,
                              sample:Optional[str]=None,
                              **kwargs):
        x, y, weight = self.make_copy(x, y, weight)
        if weight is not None:
            if self.sample_transformation.normalize_weight:
                weight["weight"] = weight["weight"] / weight["weight"].sum()
            if sample in self.sample_weight_scales:
                weight_scale = self.sample_weight_scales[sample]
                weight["weight"] = weight["weight"] * weight_scale
        return x, y, weight
    
    def transform_dataset_data(self, x:pd.DataFrame, y:pd.DataFrame,
                               weight:Optional[pd.DataFrame]=None,
                               **kwargs):
        x, y, weight = self.make_copy(x, y, weight)      
        if weight is not None:
            if self.dataset_transformation.scale_weight_by_mean:
                weight["weight"] = weight["weight"] / weight['weight'].mean()
            mode = self.dataset_transformation.negative_weight_mode
            fix_negative_weights(weight, mode=mode, weight_col="weight")
        random_state = self.dataset_transformation.random_state
        if weight is None:
            x, y = shuffle_arrays(x, y, random_state=random_state)
        else:
            x, y, weight = shuffle_arrays(x, y, weight, random_state=random_state)
        return x, y, weight
    
    def transform_and_merge(self, sample_data:Dict, **kwargs):
        transformed_data = {}
        for sample, data in sample_data.items():
            x, y, weight = self.transform_sample_data(**data, sample=sample, **kwargs)
            transformed_data[sample] = {"x": x, "y": y, "weight": weight}
        else:
            has_weight = weight is not None
        # concatenate samples
        x      = pd.concat([transformed_data[sample]["x"] for sample in transformed_data], ignore_index=True)
        y      = pd.concat([transformed_data[sample]["y"] for sample in transformed_data], ignore_index=True)
        if has_weight:
            weight = pd.concat([transformed_data[sample]["weight"] for sample in transformed_data], ignore_index=True)
        else:
            weight = None
        x, y, weight = self.transform_dataset_data(x, y, weight, **kwargs)
        return x, y, weight
                  
    def set_sample_weight_scales(self, sample_weight_scales:Optional[Dict]=None):
        if sample_weight_scales is None:
            self.sample_weight_scales = {}
        else:
            self.sample_weight_scales = sample_weight_scales

class SplitAlgoBase(ConfigurableObject):
    def get_analysis_dataset_names(self) -> List[str]:
        # use the full dataset by default
        return None
        
    def get_extra_variables(self):
        return []
    
    def train_val_test_split(self, analysis_datasets:Dict,
                             data_transformer:DataTransformer,
                             **kwargs):
        raise NotImplementedError
        
    def set_random_state(self, random_state:Optional[int]=-1):
        self.config["random_state"] = random_state        
                  
    def combine_analysis_datasets(self, analysis_datasets:List[Dict]):
        combined_dataset = {}
        for dataset in analysis_datasets:
            for sample in dataset:
                if sample not in combined_dataset:
                    combined_dataset[sample] = dataset[sample].copy()
                    continue
                combined_dataset[sample]["x"] = pd.concat([combined_dataset[sample]["x"], dataset[sample]["x"]],
                                                           ignore_index=True)
                combined_dataset[sample]["y"] = pd.concat([combined_dataset[sample]["y"], dataset[sample]["y"]],
                                                           ignore_index=True)
                if dataset[sample]["weight"] is None:
                    continue
                combined_dataset[sample]["weight"] = pd.concat([combined_dataset[sample]["weight"], dataset[sample]["weight"]],
                                                               ignore_index=True)
        return combined_dataset                  
        
    def get_dataset_split(self, data_transformer:DataTransformer,
                         dataset_type:str, sample_data:Dict,
                         sample_index:Optional[Dict]=None):
        x, y, weight = data_transformer.transform_and_merge(sample_data)
        extra_variables = self.get_extra_variables()
        if len(extra_variables) > 0:
            x = x.drop(columns=extra_variables)
        dataset_split = {
            f"x_{dataset_type}"      : x,
            f"y_{dataset_type}"      : y,
            f"weight_{dataset_type}" : weight,
        }
        if sample_index is not None:
            dataset_split[f"index_{dataset_type}"] = sample_index
        return dataset_split

class KFoldSplitAlgo(SplitAlgoBase):
    
    CONFIG_FORMAT = {
        "datasets": ConfigComponent(dtypes=["LIST[STR]", "NONE"], default=None,
                                    description="dataset(s) that should be used in kfold splitting; if none, the "
                                                "full dataset will be used"),
        "index_variable": ConfigComponent(dtypes=["STR", "NONE"], default=None,
                                          description="the variable used for indexing (to keep track of "
                                                      "train/val events in each fold); if none, "
                                                      "no indices will be saved"),
        "n_splits": ConfigComponent(dtypes="INT", required=True,
                                    description="number of splits (= number of folds); one of the split "
                                                "will be used for validation and the rest for training "
                                                "with each fold rotating the splits"),
        "random_state": ConfigComponent(dtypes=["INT", "NONE"], default=-1,
                                        description="random state for shuffling data in each fold; "
                                                    "if negative, no shuffling will be made; "
                                                    "if None, the global random state instance from "
                                                    "numpy.random will be used (so every shuffle "
                                                    "will give a different result)")
    }
    
    def get_analysis_dataset_names(self) -> List[str]:
        dataset_config = self.config.get("datasets", None)
        if dataset_config is not None:
            dataset_names = list(dataset_config)
        else:
            dataset_names = None
        return dataset_names
    
    def get_extra_variables(self):
        index_variable = self.config.get("index_variable", None)
        if index_variable is not None:
            return [index_variable]
        return []
    
    def train_val_test_split(self, analysis_datasets:Dict,
                             data_transformer:DataTransformer,
                             **kwargs):
        
        n_splits     = self.config["n_splits"]
        random_state = self.config["random_state"]
        
        self.stdout.info("INFO: Data will be split using the KFold method.")
        self.stdout.info(f"   Analysis datasets used: {self.get_analysis_dataset_names()}")
        self.stdout.info(f"         Number of splits: {n_splits}")
        self.stdout.info(f"       KFold random state: {random_state}")
        
        from sklearn.model_selection import KFold
        
        index_variable = self.config.get("index_variable", None)
        kfolds = {}
        kfold_splits = {}
        combined_dataset = self.combine_analysis_datasets(list(analysis_datasets.values()))
        random_state = self.config["random_state"]
        if (random_state is not None) and (random_state < 0):
             shuffle = False
             random_state = None
        else:
             shuffle = True
        for sample in combined_dataset:
            kfolds[sample] = KFold(n_splits=n_splits,
                                   shuffle=shuffle,
                                   random_state=random_state)
            kfold_splits[sample] = kfolds[sample].split(combined_dataset[sample]["x"])
        for i in range(n_splits):
            train_dataset = {}
            val_dataset = {}
            train_var_index = {}
            val_var_index = {}
            for sample in combined_dataset:
                train_index, val_index = next(kfold_splits[sample])
                for index, dataset_i, var_index in [(train_index, train_dataset, train_var_index),
                                                    (val_index, val_dataset, val_var_index)]:
                    dataset_i[sample] = {
                        "x": combined_dataset[sample]["x"].loc[index],
                        "y": combined_dataset[sample]["y"].loc[index]
                    }
                    if combined_dataset[sample]["weight"] is not None:
                        dataset_i[sample]["weight"] = combined_dataset[sample]["weight"].loc[index]
                    if index_variable is not None:
                        var_index[sample] = dataset_i[sample]["x"][index_variable].values
            result_i = {}
            for dataset_type, dataset_i, var_index in [("train", train_dataset, train_var_index),
                                                       ("val", val_dataset, val_var_index)]:
                
                result_i.update(self.get_dataset_split(data_transformer, dataset_type, dataset_i, var_index))
            yield result_i
    
class CustomSplitAlgo(SplitAlgoBase):
    
    CONFIG_FORMAT = {
        "datasets": {
            "train": ConfigComponent(dtypes="LIST[STR]", required=True,
                                     description="dataset(s) that should be used as the train dataset"),
            "validation": ConfigComponent(dtypes=["LIST[STR]", "NONE"], default=None,
                                          description="dataset(s) that should be used as the validation dataset; "
                                                      "if none, no validation dataset will be loaded"),
            "test": ConfigComponent(dtypes=["LIST[STR]", "NONE"], default=None,
                                    description="dataset(s) that should be used as the test dataset; "
                                                "if none, no test dataset will be loaded")
        }
    }
    
    def get_train_val_test_map(self):
        datasets_config = self.config["datasets"]
        dataset_map = {}
        dataset_map["train"] = list(datasets_config["train"])
        if "validation" in datasets_config:
            dataset_map["val"] = list(datasets_config["validation"])
        if "test" in datasets_config:
            dataset_map["test"] = list(datasets_config["test"])
        return dataset_map
    
    def get_analysis_dataset_names(self) -> List[str]:
        dataset_map = self.get_train_val_test_map()
        dataset_names = list(chain.from_iterable(dataset_map.values()))
        return dataset_names
    
    def train_val_test_split(self, analysis_datasets:Dict, data_transformer:DataTransformer):
        dataset_map = self.get_train_val_test_map()
        self.stdout.info("INFO: Data will be split using custom analysis datasets.")
        self.stdout.info(f'        Train dataset: {dataset_map["train"]}')
        self.stdout.info(f'   Validation dataset: {dataset_map.get("val", None)}')
        self.stdout.info(f'         Test dataset: {dataset_map.get("test", None)}')
        result = {}
        for dataset_type, dataset_names in dataset_map.items():
            selected_datasets = [analysis_datasets[dataset_name] for dataset_name in dataset_names]
            combined_dataset = self.combine_analysis_datasets(selected_datasets)
            result.update(self.get_dataset_split(data_transformer, dataset_type, combined_dataset))
        return result
    
class IndexSplitAlgo(SplitAlgoBase):
    
    CONFIG_FORMAT = {
        "indices":{
            "train": ConfigComponent(dtypes="DICT", required=True,
                                     description="a dictionary containing that maps the sample to the corresponding "
                                                 "selection indices for the train dataset in the form "
                                                 "{<sample_name>: <array of index values>}"),
            "validation": ConfigComponent(dtypes=["DICT", "NONE"], default=None,
                                          description="a dictionary containing that maps the sample to the corresponding "
                                                      "selection indices for the validation dataset in the form "
                                                      "{<sample_name>: <array of index values>}; if none, no validation "
                                                      "dataset will be loaded"),
            "test": ConfigComponent(dtypes=["DICT", "NONE"], default=None,
                                    description="a dictionary containing that maps the sample to the corresponding "
                                                "selection indices for the test dataset in the form "
                                                "{<sample_name>: <array of index values>}; if none, no test "
                                                "dataset will be loaded"),
        },
        "index_variable": ConfigComponent(dtypes="STR", required=True,
                                          description="the variable used for indexing")
    }

    def get_extra_variables(self):
        index_variable = self.config["index_variable"]
        return [index_variable]
    
    def get_split_indices(self):
        split_indices = {}
        split_indices["train"] = self.config["indices"]["train"]
        if "validation" in self.config["indices"]:
            split_indices["val"] = self.config["indices"]["validation"]
        if "test" in self.config["indices"]:
            split_indices["test"] = self.config["indices"]["test"]
        return split_indices
    
    def train_val_test_split(self, analysis_datasets:Dict, data_transformer:DataTransformer):
        
        index_variable = self.config["index_variable"]
        self.stdout.info("INFO: Data will be split using custom event indices.")
        self.stdout.info(f"       Index variable: {index_variable}")
        
        analysis_dataset = analysis_datasets[None]
        concat_kwargs = {
            "axis": 1,
            "sort": False,
            "copy": False
        }
        train_variables = None
        sample_dfs = {}
        for sample, sample_dataset in analysis_dataset.items():
            x, y, weight = sample_dataset["x"], sample_dataset["y"], sample_dataset["weight"]
            if weight is None:
                sample_dfs[sample] = pd.concat([x, y], **concat_kwargs)
            else:
                sample_dfs[sample] = pd.concat([x, y, weight], **concat_kwargs)
            sample_dfs[sample].set_index(index_variable, inplace=True)
        else:
            train_variables = list(x.columns)
        split_indices = self.get_split_indices()
        result = {}
        for dataset_type, indices in split_indices.items():
            dataset_i = {}
            unique_indices = {}
            for sample, sample_df in sample_dfs.items():
                sample_indices = indices.get(sample, None)
                if sample_indices is None:
                    raise RuntimeError(f'missing event indices for the sample "{sample}" when selecting events '
                                       f'for the "{dataset_type}" dataset')
                # need to make sure the event indices are unique to avoid further duplication
                sample_indices = np.unique(sample_indices)
                unique_indices[sample] = sample_indices
                missing_indices = np.setdiff1d(sample_indices, sample_df.index.values)
                if len(missing_indices) > 0:
                    raise RuntimeError(f'failed to select events from the given indices for the '
                                       f'sample "{sample}" for the "{dataset_type}" dataset')
                df_selected = sample_df.loc[sample_indices].reset_index()
                # make sure all data are copied so any subsequent transformation only act on the copy
                dataset_i[sample] = {
                    "x": df_selected[train_variables],
                    "y": df_selected[["true_label"]]
                }
                if "weight" in df_selected.columns:
                    dataset_i[sample]["weight"] = df_selected[["weight"]]
            result.update(self.get_dataset_split(data_transformer, dataset_type, dataset_i, unique_indices))
        return result
    
class ManualSplitAlgo(SplitAlgoBase):
    
    CONFIG_FORMAT = {
        "datasets": ConfigComponent(dtypes=["LIST[STR]", "NONE"], default=None,
                                    description="dataset(s) that should be used in the manual splitting; if none, the "
                                                "full dataset will be used"),
        "split_func": ConfigComponent(dtypes="ANY", required=True,
                                      description="A callable with signature (x, y, weight, **kwargs) -> "
                                                  "{<dataset_name>: (x, y, weight)}"),
        "extra_variables": ConfigComponent(dtypes="LIST[STR]", default=[],
                                           description="extra variables needed for the manual split method")     
    }
    
    def get_analysis_dataset_names(self) -> List[str]:
        dataset_config = self.config.get("datasets", None)
        if dataset_config is not None:
            dataset_names = list(dataset_config)
        else:
            dataset_names = None
        return None
    
    def get_extra_variables(self):
        return self.config.get("extra_variables", [])
    
    def train_val_test_split(self, analysis_datasets:Dict, data_transformer:DataTransformer):
        
        self.stdout.info("INFO: Data will be split using a user-defined function.")
        
        split_func = self.config["split_func"]
        extra_variables = self.config.get("extra_variables", [])
        analysis_dataset = self.combine_analysis_datasets(list(analysis_datasets.values()))
        splitted_dataset = {}
        for sample, sample_dataset in analysis_dataset.items():
            x, y, weight = sample_dataset["x"], sample_dataset["y"], sample_dataset["weight"]
            splitted_sample_dataset = split_func(x, y, weight, sample=sample)
            for dataset_type in splitted_sample_dataset:
                if dataset_type not in splitted_dataset:
                    splitted_dataset[dataset_type] = {}
                splitted_dataset[dataset_type][sample] = splitted_sample_dataset[dataset_type]
        result = {}
        for dataset_type, dataset_i in splitted_dataset.items():
            result.update(self.get_dataset_split(data_transformer, dataset_type, dataset_i))
        return result

class DatasetSplitMethod(DescriptiveEnum):
    KFOLD  = (0, "select event using the k-fold method", KFoldSplitAlgo)
    CUSTOM = (1, "select event using event number modularity", CustomSplitAlgo)
    INDEX  = (2, "select event using from a given set of indices", IndexSplitAlgo)
    MANUAL = (3, "select event using a custom function", ManualSplitAlgo)
    
    def __new__(cls, value:int, description:str, split_algo:SplitAlgoBase):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        obj.split_algo = split_algo
        return obj
    
class DataLoader(AnalysisBase):
    
    REQUIRED_CONFIG_COMPONENTS = ["paths:arrays", "samples:*", "kinematic_regions:*",
                                  "variables:*", "training:*", "channels:*",
                                  "names:weight", "names:event_number"]
    
    DEFAULT_DATASET_SPLIT_SETUP = {
        "method": "kfold",
        "options": {
            "datasets": None,
            "index_variable": None,
            "n_splits": 5,
            "random_state": -1
        }
    }
    
    def __init__(self, analysis_config:Union[Dict, str],
                 array_dir:Optional[str]=None,
                 model_dir:Optional[str]=None,
                 verbosity:Optional[Union[int, str]]="INFO",
                 **kwargs):
        super().__init__(analysis_config=analysis_config,
                         array_dir=array_dir,
                         model_dir=model_dir,
                         verbosity=verbosity,
                         **kwargs)
        self.set_data_transformer()
        self.set_split_algo()
        self.data_format = self.get_analysis_data_format()
        
    def set_data_transformer(self, data_transformer:Optional[DataTransformer]=None):
        if data_transformer is None:
            train_config = self.config["training"]
            sample_transformation  = train_config.get("sample_transformation", {})
            dataset_transformation = train_config.get("dataset_transformation", {})
            data_transformer = DataTransformer(sample_transformation=sample_transformation,
                                               dataset_transformation=dataset_transformation)
        self.data_transformer = data_transformer
        
    def set_split_algo(self, split_algo:Optional[SplitAlgoBase]=None):
        if split_algo is None:
            try:
                split_method = self.config["training"]["datasets"]["split_method"]
                split_options = self.config["training"]["datasets"]["split_options"]
            except:
                split_method = self.DEFAULT_DATASET_SPLIT_SETUP["method"]
                split_options = self.DEFAULT_DATASET_SPLIT_SETUP["options"]
            split_method = DatasetSplitMethod.parse(split_method)
            split_algo = split_method.split_algo(split_options,
                                                 verbosity=self.stdout.verbosity)
        self.split_algo = split_algo
        
    def set_random_state(self, random_state:Optional[int]=-1):
        self.data_transformer.set_random_state(random_state)
        self.split_algo.set_random_state(random_state)

    def _format_selection(self, samples:List[str],
                          old_selection:Optional[Union[Dict, str]]=None,
                          new_selection:Optional[Union[Dict, str]]=None):
        if old_selection is None:
            selection = {sample: None for sample in samples}
        elif isinstance(old_selection, str):
            selection = {sample: old_selection for sample in samples}
        elif isinstance(old_selection, dict):
            selection = {sample: old_selection.get(sample, None) for sample in samples}
        else:
            raise ValueError("invalid selection format")
        if new_selection is None:
            return selection
        if isinstance(new_selection, str):
            for sample in samples:
                if selection[sample] is None:
                    selection[sample] = new_selection
                else:
                    selection[sample] = f"({selection['sample']}) and ({new_selection})"                    
        elif isinstance(new_selection, dict):
            for sample, sample_new_selection in new_selection.items():
                if sample not in samples:
                    continue
                if selection[sample] is None:
                    selection[sample] = sample_new_selection
                else:
                    selection[sample] = f"({selection['sample']}) and ({sample_new_selection})"
        return selection

    @semistaticmethod
    def _read_data_from_file(self, filename:str, key:Optional[str]=None,
                             columns:Optional[List[str]]=None,
                             selection:Optional[str]=None) -> pd.DataFrame:
        """
            Load array data from a file (csv or h5).
            
            Arguments:
                filename: string
                    Path to the input data (only csv or h5 formats are allowed).
                selection: (optional) str
                    Selection applied to the input data (via pandas.DataFrame.query)
        """        
        extension = os.path.splitext(filename)[-1]
        if extension not in [".csv", ".h5"]:
            raise RuntimeError(f'unsupported data format "{extension.strip(".")}"; allowed '
                               'formats are: csv, h5')
        if extension == ".csv":
            df = pd.read_csv(filename, usecols=columns)
        else:
            df = pd.read_hdf(filename, key=key, columns=columns)
        if selection not in [None, "1", 1]:
            df = df.query(selection).reset_index(drop=True)
        return df

    def get_sample_df(self, sample:str, key:Optional[str]=None,
                      columns:Optional[List[str]]=None,
                      selection:Optional[str]=None,
                      kinematic_region:Optional[str]=None)->pd.DataFrame:
        if kinematic_region is not None:
            sample_path = self.get_file("train_sample",
                                        subdirectory=kinematic_region,
                                        sample=sample,
                                        fmt=self.data_format)
        else:
            sample_path = self.get_file("train_sample",
                                        sample=sample,
                                        fmt=self.data_format)
        self.stdout.info(f'INFO: Loading inputs for the sample "{sample}" from "{sample_path}"')
        df = self._read_data_from_file(sample_path, key=key, columns=columns, selection=selection)
        return df
    
    def get_sample_dfs(self, samples:List[str], key:Optional[str]=None,
                       columns:Optional[List[str]]=None,
                       selection:Optional[Union[Dict, str]]=None,
                       kinematic_region:Optional[str]=None)->pd.DataFrame:
        dfs = {}
        selection = self._format_selection(samples, selection)
        for sample in samples:
            sample_selection = selection.get(sample, None)
            df = self.get_sample_df(sample=sample, key=key,
                                    columns=columns,
                                    selection=sample_selection,
                                    kinematic_region=kinematic_region)
            dfs[sample] = df
        return dfs
    
    def get_analysis_datasets(self, samples:List[str], train_variables:List[str],
                              class_label_map:Dict,
                              dataset_names:Optional[List[str]]=None,
                              key:Optional[str]=None, 
                              weight_variable:Optional[str]=None,
                              selection_variables:Optional[List[str]]=None,
                              selection:Optional[Union[Dict, str]]=None,
                              kinematic_region:Optional[str]=None):
        for sample in samples:
            if sample not in class_label_map:
                raise RuntimeError(f'missing class label definition for the sample "{sample}"')
        columns = list(train_variables)
        if weight_variable is not None:
            columns.append(weight_variable)
        if selection_variables is not None:
            columns.extend(selection_variables)
        sample_dfs_map = {}
        if dataset_names is not None:
            dataset_selections = {}
            additional_columns = set()
            try:
                spec = self.config["training"]["datasets"]["specification"]
            except:
                spec = {}            
            for dataset_name in list(set(dataset_names)):
                if dataset_name not in spec:
                    raise RuntimeError(f'missing specification for the dataset "{dataset_name}" in '
                                       'analysis config')
                if 'selection' not in spec[dataset_name]:
                    raise RuntimeError(f'missing definition for selection of the dataset "{dataset_name}" '
                                       'in analysis config')
                dataset_selections[dataset_name] = spec[dataset_name]['selection']
                if ('variables' in spec[dataset_name]) and (spec[dataset_name]['variables'] is not None):
                    additional_columns |= set(spec[dataset_name]['variables'])
            columns = list(set(columns).union(additional_columns))
            sample_dfs = self.get_sample_dfs(samples, key=key, columns=columns,
                                             selection=selection,
                                             kinematic_region=kinematic_region)

            for dataset_name in dataset_selections:
                sample_dfs_map[dataset_name] = {}
                selection = dataset_selections[dataset_name]
                for sample, sample_df in sample_dfs.items():
                    sample_dfs_map[dataset_name][sample] = sample_df.query(selection).reset_index(drop=True)
        else:
            sample_dfs_map[None] = self.get_sample_dfs(samples, key=key, columns=columns,
                                                       selection=selection,
                                                       kinematic_region=kinematic_region)

        datasets = {}
        for dataset_name, sample_dfs in sample_dfs_map.items():
            datasets[dataset_name] = {}
            for sample, sample_df in sample_dfs.items():
                data_size = len(sample_df)
                class_label = class_label_map[sample]
                datasets[dataset_name][sample] = {
                    "x": sample_df[train_variables],
                    "y": pd.DataFrame(np.full((data_size,), class_label), columns=['true_label'])
                }
                if weight_variable is None:
                    datasets[dataset_name][sample]["weight"] = None
                else:
                    datasets[dataset_name][sample]["weight"] = sample_df[[weight_variable]]
        return datasets

    def load_train_data(self, samples:List[str],
                        train_variables:List[str],
                        class_label_map:Dict,
                        weight_variable:Optional[str]=None,
                        selection_variables:Optional[List[str]]=None,
                        selection:Optional[Union[Dict, str]]=None,
                        kinematic_region:Optional[str]=None,
                        split_algo:Optional[SplitAlgoBase]=None):
        kwargs = {
            "samples"             : samples,
            "class_label_map"     : class_label_map,
            "weight_variable"     : weight_variable,
            "selection_variables" : selection_variables,
            "selection"           : selection,
            "kinematic_region"    : kinematic_region
        }
        if split_algo is None:
            split_algo = self.split_algo
        extra_variables = split_algo.get_extra_variables()
        for variable in extra_variables:
            if variable in train_variables:
                raise RuntimeError(f'the additional variable "{variable}" used in dataset splitting is '
                                    'already part of the train variables, please double check your input')
        dataset_names = split_algo.get_analysis_dataset_names()
        kwargs["train_variables"] = list(train_variables)
        kwargs["train_variables"].extend(extra_variables)
        
        analysis_datasets = self.get_analysis_datasets(dataset_names=dataset_names, **kwargs)
        
        train_data =  split_algo.train_val_test_split(analysis_datasets, self.data_transformer)
        
        return train_data
                                  
    def get_class_label_map(self, class_labels:Dict):
        labels = list(class_labels.keys())
        encodings = get_class_label_encodings(labels)
        class_label_map = {}
        for label, samples in class_labels.items():
            resolved_samples = self.resolve_samples(samples)
            for sample in resolved_samples:
                if sample in class_label_map:
                    raise RuntimeError(f'multiple class label found for the sample "{sample}"')
                class_label_map[sample] = encodings[label]
        return class_label_map                                  
    
    def load_channel_train_data(self, channel:str, scale_factors:Optional[Dict]=None,
                               custom_indices:Optional[Dict[str, Dict[str, np.ndarray]]]=None,
                               index_variable:Optional[str]=None):
        if channel not in self.all_channels:
            raise ValueError(f"unknown channel: {channel}")
            
        channel_config  = self.config["channels"][channel]
        training_config = self.config["training"]
        class_labels = channel_config['class_labels']
        class_label_map = self.get_class_label_map(class_labels)
        
        if scale_factors is None:
            scale_factors = channel_config.get('SF', {})
        self.data_transformer.set_sample_weight_scales(scale_factors)
        
        if custom_indices is not None:
            if index_variable is None:
                index_variable = self.get_event_index_variable()
            split_options = {
                "indices": custom_indices,
                "index_variable": index_variable
            }
            split_algo = IndexSplitAlgo(split_options)
        else:
            split_algo = self.split_algo
            
        kwargs = {
            "samples"                : self.resolve_samples(channel_config['train_samples']),
            "train_variables"        : self.resolve_variables(channel_config['train_variables']),
            "class_label_map"        : class_label_map,
            "weight_variable"        : self.config['names'].get("weight", None),
            "selection"              : channel_config.get('selection', None),
            "selection_variables"    : channel_config.get('selection_variables', None),
            "kinematic_region"       : channel_config.get('kinematic_region', None),
            "split_algo"             : split_algo
        }
        self.stdout.info(f"INFO: Loading data for the channel: {channel}")
        return self.load_train_data(**kwargs)
        
    def print_channel_summary(self, channels:Optional[Union[List[str],str]]=None):
        if channels is None:
            channels = self.all_channels
        elif isinstance(channels, str):
            channels = [channels]
        for channel in channels:
            if channel not in self.all_channels:
                raise ValueError(f"unknwon channel: {channel}")
            selection = self.config['channels'][channel]['selection']
            train_samples = self.config['channels'][channel]['train_samples']
            test_samples = self.config['channels'][channel]['test_samples']
            train_variables = self.config['channels'][channel]['train_variables']
            class_labels = self.config['channels'][channel]['class_labels']
            train_samples = self.resolve_samples(train_samples)
            test_samples = self.resolve_samples(test_samples)
            train_variables = self.resolve_variables(train_variables)
            scale_factors = self.config['channels'][channel]['SF']
            self.stdout.info("=============================== CHANNEL SUMMARY ===============================")
            self.stdout.info("Channel Name: ".rjust(20) + f"{channel}")
            self.stdout.info("Channel Selection: ".rjust(20) + f"{selection}")
            self.stdout.info("*******************************************************************************")
            self.stdout.info("Train Samples: ".rjust(20) + ", ".join(train_samples))
            self.stdout.info("Test Samples: ".rjust(20) + ", ".join(test_samples))
            self.stdout.info("*******************************************************************************")
            self.stdout.info("Class Labels: ".rjust(20))
            for label in class_labels:
                samples = self.resolve_samples(class_labels[label])
                self.stdout.info(f"\t{label}: " + ", ".join(samples))
            self.stdout.info("*******************************************************************************")
            self.stdout.info("Train Variables: ".rjust(20) + ", ".join(train_variables))
            self.stdout.info("*******************************************************************************")
            self.stdout.info("Scale Factors: ".rjust(20) + str(scale_factors))
            self.stdout.info("*******************************************************************************")
            self.stdout.info("")
            
            
def index_modularity_split(index_variable:str, modulo:int,
                           train_remainders:List[int],
                           val_remainders:Optional[List[int]]=None,
                           test_remainders:Optional[List[int]]=None):
    def split_func(x, y, weight=None, **kwargs):
        masks = {}
        masks["train"] = (x[index_variable] % modulo).isin(train_remainders)
        if val_remainders is not None:
            masks["val"] = (x[index_variable] % modulo).isin(val_remainders)
        if test_remainders is not None:
            masks["test"] = (x[index_variable] % modulo).isin(test_remainders)
        result = {}
        for dataset_type, mask in masks.items():
            result[dataset_type] = {
                "x": x[mask],
                "y": y[mask]
            }
            if weight is not None:
                result[dataset_type]["weight"] = weight[mask]
        return result
    return split_func