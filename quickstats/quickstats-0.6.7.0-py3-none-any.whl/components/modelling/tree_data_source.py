from typing import Optional, Union, List, Dict, Callable

import ROOT

from quickstats import AbstractObject, DescriptiveEnum, PathManager
from quickstats.interface.root import RooRealVar

from .component_source import ComponentSource

class TreeDataSource(ComponentSource):
    """
    Handling Tree data from a ROOT file in the form of a RooDataSet.
    """
    
    _REQUIRE_CONFIG_ = {
        "ROOT"  : False,
        "RooFit": True
    }    

    def __init__(self, tree_name:str,
                 input_paths:Optional[Union[PathManager, str, List[str]]],
                 observable:Optional[Union[RooRealVar, ROOT.RooRealVar, dict, str]]=None,
                 weight_name:Optional[str]=None,
                 verbosity:Optional[Union[int, str]]="INFO"):
        super().__init__(input_paths=input_paths,
                         observable=observable,
                         verbosity=verbosity)
        self.weight_name  = weight_name
        self.tree_name    = tree_name
        
    def get_tree(self, **file_kwargs):
        if self.tree_name is None:
            raise RuntimeError("tree name not set")
        chain = ROOT.TChain(self.tree_name)
        input_paths = self.get_resolved_input_paths(**file_kwargs)
        for path in input_paths:
            chain.Add(path)
        return chain
        
    def create_dataset_from_tree(self, name:str, tree:Union[ROOT.TTree, ROOT.TChain]):
        """
        """
        variables = ROOT.RooArgSet()
        if self.observable is None:
            raise RuntimeError("observable not set")
        observable = self.observable.new()
        variables.add(observable)
        if self.weight_name is not None:
            weight_var = ROOT.RooRealVar(self.weight_name, self.weight_name, 1)
            variables.add(weight_var)
            dataset = ROOT.RooDataSet(name, name, variables,
                                      ROOT.RooFit.Import(tree),
                                      ROOT.RooFit.WeightVar(weight_var))
        else:
            dataset = ROOT.RooDataSet(name, name, variables,
                                      ROOT.RooFit.Import(tree))
        return dataset
    
    def create_dataset(self, name:str, **file_kwargs):
        """
        """
        tree = self.get_tree(**file_kwargs)
        dataset = self.create_dataset_from_tree(name, tree)
        return dataset
    
    def create_histogram(self, name:Optional[str]=None, n_bins:Optional[int]=None,
                         bin_range:Optional[List[float]]=None, **file_kwargs):
        tree = self.get_tree(**file_kwargs)
        if name is None:
            import uuid
            h_name = uuid.uuid4().hex
        else:
            h_name = name
        obs = self.observable.new()
        obs_name = obs.GetName()
        if n_bins is None:
            n_bins = obs.numBins()
        if bin_range is None:
            vmin, vmax = obs.getMin(), obs.getMax()
        else:
            vmin, vmax = bin_range[0], bin_range[1]
        if (vmin == -1e30) and (vmax == 1e30):
            self.stdout.warning("WARNING: Observable range is unbounded (-1e30, 1e30). "
                                "The resulting histogram could be buggy.")
        hist = ROOT.TH1D(h_name, h_name, n_bins, vmin, vmax)
        canvas = ROOT.TCanvas(uuid.uuid4().hex)
        if self.weight_name is not None:
            tree.Draw(f"{obs_name} >> {h_name}", self.weight_name)
        else:
            tree.Draw(f"{obs_name} >> {h_name}")
        del canvas
        hist.SetDirectory(0)
        return hist