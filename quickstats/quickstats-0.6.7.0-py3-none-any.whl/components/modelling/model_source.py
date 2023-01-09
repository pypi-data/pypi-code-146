from typing import Optional, Union, List, Dict, Callable

import ROOT

from quickstats import AbstractObject, PathManager
from quickstats.interface.root import RooRealVar
from .component_source import ComponentSource

class ModelSource(ComponentSource):
    
    def __init__(self, input_paths:Optional[Union[PathManager, str, List[str]]],
                 observable:Optional[RooRealVar]=None,
                 weight_name:Optional[str]=None,
                 verbosity:Optional[Union[int, str]]="INFO"):
        super().__init__(input_paths=input_paths,
                         observable=observable,
                         verbosity=verbosity)
        self.weight_name = weight_name
        
    def create_model(self, workspace:ROOT.RooWorkspace):
        pass