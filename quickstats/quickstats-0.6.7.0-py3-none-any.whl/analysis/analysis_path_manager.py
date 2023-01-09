from typing import Optional, Union, Dict, List, Tuple
import os

from quickstats import PathManager
from quickstats.utils.common_utils import combine_dict

class AnalysisPathManager(PathManager):
    
    DEFAULT_DIRECTORIES = {
        "categorized_array"     : "categorized_arrays",
        "categorized_minitree"  : "categorized_minitrees",
        "categorized_histogram" : "categorized_histograms",
        "yield"                 : "yields",
        "summary"               : "summary",
        "plot"                  : "plots",
        "xml"                   : "xmls",
        "workspace"             : "xmls/workspace",
        "xml_config"            : "xmls/config",
        "xml_data"              : "xmls/config/data",
        "xml_model"             : "xmls/config/models",
        "xml_category"          : "xmls/config/categories",
        "limit"                 : "limits",
        "likelihood"            : "likelihoods"
    }
    
    DEFAULT_FILES = {
        "ntuple_sample"                            : ("ntuple", "{sample}.root"),
        "train_sample"                             : ("array", "{sample}.{fmt}"),
        "array_sample"                             : ("array", "{sample}.{fmt}"),
        "categorized_array_sample"                 : ("categorized_array", "{sample}_{category}.{fmt}"),
        "categorized_minitree_sample"              : ("categorized_minitree", "{sample}_{category}.root"),
        "categorized_histogram_sample"             : ("categorized_histogram", "{sample}_{category}.root"),
        "category_summary"                         : ("summary", "category_summary_{channel}.json"),
        "boundary_data"                            : ("summary", "boundary_tree_{channel}.json"),
        "score_distribution_plot"                  : ("plot", "score_distribution_{channel}.pdf"),
        "variable_distribution_plot"               : ("plot", "distribution_{variable}_{category}.pdf"),   
        "merged_yield_data"                        : ("yield", "yields.json"),
        "merged_yield_err_data"                    : ("yield", "yields_err.json"),
        "yield_data"                               : ("yield", "yields_{category}.json"),
        "yield_err_data"                           : ("yield", "yields_err_{category}.json"),  
        "signal_modelling_plot"                    : ("plot", "modelling_{category}.pdf"),
        "signal_modelling_data"                    : ("signal_model", "model_parameters.json"),
        "signal_modelling_summary"                 : ("signal_model", "model_summary_{category}.json"),
        "input_xml"                                : ("xml_config", "input.xml"),
        "limit_summary"                            : ("summary", "limit_summary.json"),
        "likelihood_summary"                       : ("summary", "likelihood_summary.json"),
        "benchmark_significance"                   : ("summary", "benchmark_significance.json")
    }
    
    def __init__(self, study_name:str="", base_path:Optional[str]=None,
                 directories:Optional[Dict[str, str]]=None,
                 files:Optional[Dict[str, Union[str, Tuple[Optional[str], str]]]]=None):
        
        directories = combine_dict(self.DEFAULT_DIRECTORIES, directories)
        files       = combine_dict(self.DEFAULT_FILES, files)
            
        super().__init__(base_path=base_path, directories=directories, files=files)
        
        self.study_name    = study_name
        self.raw_base_path = base_path
        self.update()
        
    def update(self):
        if self.raw_base_path is None:
            base_path = self.study_name
        else:
            base_path = os.path.join(self.raw_base_path, self.study_name)
        self.base_path = base_path
        
    def set_study_name(self, study_name:str):
        self.study_name = study_name
        self.update()
        
    def set_base_path(self, base_path:str):
        self.raw_base_path = base_path
        self.update()