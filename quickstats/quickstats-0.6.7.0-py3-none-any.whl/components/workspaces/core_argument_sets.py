from typing import Optional, Union, List, Dict

import ROOT

from quickstats import DescriptiveEnum, AbstractObject
from quickstats.maths.numerics import is_float

from .settings import (OBS_SET, POI_SET, NUIS_SET, GLOB_SET)

class CoreArgumentSets(AbstractObject):
    
    def __init__(self, verbosity:str="INFO"):
        super().__init__(verbosity=verbosity)
        self.obs_set    = ROOT.RooArgSet()
        self.poi_set    = ROOT.RooArgSet()
        self.nuis_set   = ROOT.RooArgSet()
        self.glob_set   = ROOT.RooArgSet()
        self.constr_set = ROOT.RooArgSet()
        
    def get_argset_by_names(self, ws:ROOT.RooWorkspace, var_names:[str, List[str]], strict:bool=False):
        if isinstance(var_names, str):
            var_names = [var_names]
        argset = ROOT.RooArgSet()
        for var_name in var_names:
            var = ws.var(var_name)
            if not var:
                if strict:
                    raise RuntimeError(f'the variable "{var_name}" is not defined in the workspace "{ws.GetName()}"')
                continue
            argset.add(var)
        return argset
    
    def validate(self):
        if self.obs_set.size() == 0:
            raise RuntimeError('observable set not initialized')
        if self.poi_set.size() == 0:
            raise RuntimeError('POIs set not initialized')
   
    def define_argsets(self, ws:ROOT.RooWorkspace):
        self.validate()
        for argset, name in [(self.obs_set, OBS_SET), (self.poi_set, POI_SET),
                             (self.nuis_set, NUIS_SET), (self.glob_set, GLOB_SET)]:
            ws.defineSet(name, argset)
        self.stdout.debug(f'DEBUG: Defined argument set "{name}" for the workspace "{ws.GetName()}".')
        