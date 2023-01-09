from typing import Optional, Union, List, Dict

import ROOT

from quickstats.interface.cppyy.vectorize import list2vec

from .systematic import Systematic
from .settings import RESPONSE_PREFIX, GLOBALOBS_PREFIX, CONSTRTERM_PREFIX

# basic data structure for systematic domain
# all the systematics under the same systematic domain will be merged into one response function          
class SystematicsDomain:
    
    def __init__(self, domain:str):
        self.domain = domain
        self.is_shape = None
        self.nuis_list = ROOT.RooArgList()
        self.nominal_list = []
        self.uncert_hi_list = ROOT.RooArgList()
        self.uncert_lo_list = ROOT.RooArgList()
        self.interp_code_list = []
        self.constr_term_list = []
        
    def get_response_name(self):
        return f"{RESPONSE_PREFIX}{self.domain}"
        
    def get_response_function(self):
        if not getattr(ROOT, "ResponseFunction"):
            raise RuntimeError("ResponseFunction class undefined: may be you need to load the corresponding "
                               "macro...")
        nominal_list = list2vec(self.nominal_list)
        interp_code_list = list2vec(self.interp_code_list)
        resp_name = self.get_response_name()
        resp_func = ROOT.ResponseFunction(resp_name, resp_name, self.nuis_list, nominal_list,
                                          self.uncert_lo_list, self.uncert_hi_list,
                                          interp_code_list)
        return resp_func
    
    def get_np_glob_constr_names(self, idx:int):
        if idx >= self.nuis_list.size():
            raise RuntimeError("index out of range")
        np = self.nuis_list.at(idx)
        np_name = np.GetName()
        glob_name = f"{GLOBALOBS_PREFIX}{np_name}"
        constr_name = f"{CONSTRTERM_PREFIX}{np_name}"
        return np_name, glob_name, constr_name
    
    def add_item(self, nuis:ROOT.RooRealVar, nominal:float, uncert_hi:ROOT.RooRealVar,
                 uncert_lo:ROOT.RooRealVar, interp_code:int, constr_term:str):
        self.nuis_list.add(nuis)
        self.nominal_list.append(nominal)
        self.uncert_hi_list.add(uncert_hi)
        self.uncert_lo_list.add(uncert_lo)
        self.interp_code_list.append(interp_code)
        self.constr_term_list.append(constr_term)