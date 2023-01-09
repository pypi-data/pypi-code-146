from typing import Optional, Union, List, Dict, Callable

import ROOT

from quickstats import PathManager
from quickstats.components import ROOTObject
from quickstats.interface.root import RooRealVar

class ComponentSource(ROOTObject):
    
    """

    class ModelType(DescriptiveEnum):
        SIGNAL     = (0, "Signal Model")
        BACKGROUND = (1, "Background Model")
        AUXILIARY  = (2, "Auxiliary Model")
    
                
    @property
    def model_type(self) -> ModelType:
        return self._model_type
    
    @model_type.setter
    def model_type(self, value:Union[str, ModelType]):
        if isinstance(value, ModelType):
            self._model_type = value
        else:
            self._model_type = ModelType.parse(value)
    """
    
    @property
    def observable(self) -> RooRealVar:
        return self._observable
    
    @observable.setter
    def observable(self, value:Union[RooRealVar, ROOT.RooRealVar, dict, str]):
        if value is None:
            self._observable = None
        elif isinstance(value, RooRealVar):
            self._observable = value
        else:
            self._observable = RooRealVar()
            self._observable.parse(value)
            
    @property
    def input_paths(self) -> PathManager:
        return self._input_paths
    
    @input_paths.setter
    def input_paths(self, value:Optional[Union[PathManager, str, List[str]]]=None):
        if value is None:
            self._input_paths = None
        if isinstance(value, PathManager):
            self._input_paths = value
        else:
            self._input_paths = PathManager(files=value)            
    
    def __init__(self, input_paths:Optional[Union[PathManager, str, List[str]]]=None,
                 observable:Optional[Union[RooRealVar, ROOT.RooRealVar, dict, str]]=None,
                 verbosity:Optional[Union[int, str]]="INFO"):
        super().__init__(verbosity=verbosity)
        
        self.input_paths  = input_paths
        self.observable   = observable
    
    def get_resolved_input_paths(self, **file_kwargs):
        if self.input_paths is None:
            raise RuntimeError("input path(s) not set")
        full_paths = []
        for name in self.input_paths.files:
            path = self.input_paths.get_resolved_file(name, check_exist=True, **file_kwargs)
            full_paths.append(path)
        return full_paths
        
    def set_observable(self, observable:Union[RooRealVar, ROOT.RooRealVar]):
        self.observable = observable