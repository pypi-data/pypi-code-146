from typing import Optional, Union, List, Dict

import ROOT

from quickstats import semistaticmethod, AbstractObject
from quickstats.utils.common_utils import combine_dict
from quickstats.utils.root_utils import load_macro

class ROOTObject(AbstractObject):   
    
    _DEFAULT_ROOT_CONFIG_ = {
        "SetBatch" : True,
        "TH1Sumw2" : None
    }
    
    _DEFAULT_ROOFIT_CONFIG_ = {
        "GlobalKillBelow"     : "ERROR",
        "MinimizerPrintLevel" : -1,
        "RemoveMessage"       : {
            "NumIntegration" : True,
            "Fitting"        : True,
            "Minimization"   : True,
            "InputArguments" : True,
            "Eval"           : True
        }
    }     
    
    _REQUIRE_CONFIG_ = {
        "ROOT"  : False,
        "RooFit": False
    }
    
    def __init__(self, root_config:Optional[Dict]=None,
                 roofit_config:Optional[Dict]=None,
                 verbosity:str="INFO"):
        super().__init__(verbosity=verbosity)
        self._root_config   = combine_dict(self._DEFAULT_ROOT_CONFIG_, root_config)
        self._roofit_config = combine_dict(self._DEFAULT_ROOFIT_CONFIG_, roofit_config)
        
        self._initialize()
    
    def configure_roofit(self):
        if "MinimizerPrintLevel" in  self._roofit_config:
            ROOT.Math.MinimizerOptions.SetDefaultPrintLevel(self._roofit_config["MinimizerPrintLevel"])
        if "RemoveMessage" in self._roofit_config:
            stream = ROOT.RooMsgService.instance().getStream(1)
            for topic, do_remove in self._roofit_config["RemoveMessage"].items():
                if not do_remove:
                    continue
                try:
                    roofit_topic = getattr(ROOT.RooFit, topic)
                    stream.removeTopic(roofit_topic)
                except:
                    self.stdout.warning(f'WARNING: Failed to remove RooFit message topic "{topic}".')
        if "GlobalKillBelow" in self._roofit_config:
            try:
                kill_level = self._roofit_config["GlobalKillBelow"]
                roofit_kill_level = getattr(ROOT.RooFit, kill_level)
                ROOT.RooMsgService.instance().setGlobalKillBelow(roofit_kill_level)
            except:
                self.stdout.warning(f'WARNING: Failed to set RooFit global kill below "{kill_level}"')
                
    def configure_root(self):
        set_batch = self._root_config.get("SetBatch", None)
        if set_batch is not None:
            ROOT.gROOT.SetBatch(set_batch)
        th1_sumw2 = self._root_config.get("TH1Sumw2", None)
        if th1_sumw2 is not None:
            ROOT.TH1.SetDefaultSumw2(th1_sumw2)
            
    def _initialize(self):
        if self._REQUIRE_CONFIG_["ROOT"]:
            self.configure_root()
        if self._REQUIRE_CONFIG_["RooFit"]:
            self.configure_roofit()
            
    @semistaticmethod
    def load_extension(self, name:str):
        result = load_macro(name)
        if (result is not None) and hasattr(ROOT, name):
            self.stdout.info(f'INFO: Loaded extension module "{name}"')            