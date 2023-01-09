from typing import Optional, Dict, List, Union
import os
import copy
import math
import time
import json

import numpy as np
import ROOT

from quickstats import DescriptiveEnum
from quickstats.maths.numerics import pretty_value
from quickstats.components.basics import WSArgument
from quickstats.components import AnalysisObject
from quickstats.utils.common_utils import parse_config

class FitMode(DescriptiveEnum):
    HYBRID  = (0, "Execute both conditional and unconditional fits for a given set of POIs")
    UNCOND  = (1, "Execute unconditional fit for a given set of POIs")
    COND    = (2, "Execute conditional fit with specified conditional values for a given set of POIs")
    NOMINAL = (3, "Execute fit without any POIs")
    NOFIT   = (4, "Do not perform any fit")

class Likelihood(AnalysisObject):
    
    def __init__(self, filename:str, poi_name:Optional[Union[str, List[str]]]=None,
                 data_name:str='combData', 
                 config:Optional[Dict]=None,
                 verbosity:Optional[Union[int, str]]="INFO"):
        config = parse_config(config)
        config['filename']  = filename
        config['poi_name']  = poi_name
        config['data_name'] = data_name
        config['verbosity'] = verbosity
        self._inherit_init(super().__init__, **config)
        self.roofit_result = None
    
    @staticmethod
    def _parse_poi_val(pois:"ROOT.RooArgSet", poi_val:Optional[Union[Dict[str, float], float]]=None):
        if poi_val is None:
            poi_val = {}
            for poi in pois:
                poi_val[poi.GetName()] = poi.getVal()
        elif not isinstance(poi_val, dict):
            poi_val_tmp = poi_val
            poi_val = {}
            for poi in pois:
                poi_val[poi.GetName()] = poi_val_tmp
        else:
            # fill in missing values
            for poi in pois:
                poi_name = poi.GetName()
                if poi_name not in poi_val:
                    poi_val[poi_name] = poi.getVal()
        return poi_val
    
    @staticmethod
    def get_combined_fit_result(uncond_fit_result:Dict, cond_fit_result:Dict):
        combined_fit_result = {}
        nll_uncond = uncond_fit_result['nll']
        nll_cond = cond_fit_result['nll']
        pnll = nll_cond - nll_uncond
        qmu  = 2 * pnll
        combined_fit_result['pnll'] = pnll
        combined_fit_result['qmu']  = qmu
        poi_val = cond_fit_result['mu']
        if (qmu >= 0):
            ndof = len(poi_val)
            if ndof == 1:
                # ndof = 1 case
                poi_name = list(poi_val)[0]
                x0 = poi_val[poi_name]
                significance = math.sqrt(qmu)
                pvalue = 1 - ROOT.Math.normal_cdf(significance, 1, x0)
            else:
                x0 = list(set(poi_val.values()))
                if len(x0) > 1:
                    combined_fit_result['significance'] = None
                    combined_fit_result['pvalue'] = None
                else:
                    pvalue = ROOT.Math.chisquared_cdf_c(qmu, ndof, x0[0])
                    significance = ROOT.RooStats.PValueToSignificance(pvalue)
            combined_fit_result['significance'] = significance
            combined_fit_result['pvalue'] = pvalue
        else:
            combined_fit_result['significance'] = None
            combined_fit_result['pvalue'] = None
        return combined_fit_result
        
    def nll_fit(self, poi_val:Optional[Union[Dict[str, float], float]]=None,
                mode:Union[int, str, FitMode]="uncond",
                snapshot_name:Optional[str]=AnalysisObject.kCurrentSnapshotName,
                do_minos:bool=False):
        """
        Perform a fit based on the Maximum Likelihood Estimate (MLE). In particular,
        the negative log-likelihood (NLL) is minimized.
        
        Parameters
        ----------------------------------------------------------------------------
        poi_val: (optional) float or dictionary of float
            Value(s) of parameter(s) of interest when performing a conditional MLE fit.
            If value is a float, then all parameters of interest will be assigned the given value.
            If value is a dictionary, it represents a map between the parameter name and the assigned value.
            Any missing parameter name will be assigned its current value (as in the snapshot).
        mode: int, str or FitMode, default = "uncond"
            Evaluation mode. Choose from:
                0 or "hybrid"  : Evaluate unconditional + conditional NLL
                1 or "uncond"  : Evaluate unconditional NLL (globally minimized NLL)
                2 or "cond"    : Evaluate conditional NLL (NLL minimized at fixed mu values)
                3 or "nominal" : Evaluate post-fit NLL (POI states remain as is)
                4 or "nofit"   : Evaluate pre-fit NLL (No fit performed)
        snapshot_name: (Optional) str or dictionary, default=AnalysisObject.kCurrentSnapshotName
            Name of snapshot to load before fitting. If value is a dictionary, it must be of the
            form {"cond": <conditional_fit_snapshot>, "uncond": <unconditional_fit_snapshot>} and
            can only be used if evaluation mode = "hybrid".
        do_minos: bool, default = False
            Evalate minos error for all parameters of interest.
        """
        mode = FitMode.parse(mode)
        if not isinstance(self.poi, ROOT.RooArgSet):
            pois = ROOT.RooArgSet(self.poi)
        else:
            pois = self.poi
            
        if snapshot_name is None:
            self.save_snapshot(self.kTempSnapshotName, WSArgument.MUTABLE)
            snapshot_name = self.kTempSnapshotName
        if isinstance(snapshot_name, dict) and (mode != FitMode.HYBRID):
            raise ValueError('snapshot name is allowed to be a dictionary only when hybrid evaluation mode is used')
        if isinstance(snapshot_name, str):
            snapshot_name = {
                "uncond": snapshot_name,
                "cond"  : snapshot_name
            }
        if "uncond" not in snapshot_name:
            snapshot_name["uncond"] = self.kCurrentSnapshotName
            self.stdout.info(f'INFO: No snapshot given for unconditional fit. The snapshot "{self.kCurrentSnapshotName}" '
                             'will be used by default')
        if "cond" not in snapshot_name:
            snapshot_name["cond"] = self.kCurrentSnapshotName
            self.stdout.info(f'INFO: No snapshot given for conditional fit. The snapshot "{self.kCurrentSnapshotName}" '
                             'will be used by default')
        if set(snapshot_name.keys()) != set(["uncond", "cond"]):
            raise ValueError('when snapshot name is given as a dictionary, it must be of the '
            'form {"cond": <conditional_fit_snapshot>, "uncond": <unconditional_fit_snapshot>}')
        
        self.load_snapshot(snapshot_name["cond"])
        poi_val = self._parse_poi_val(pois, poi_val)
        
        nll_uncond = None
        nll_cond   = None
        muhat      = None
        
        tmp_do_minos = self.minimizer.config['minos']
        
        self.minimizer.config['minos'] = do_minos
        if do_minos:
            self.minimizer.minos_set = pois
        
        start_time = time.time()
        roofit_result = {}
        muhat = {}
        muhat_errlo = {}
        muhat_errhi = {}
        
        # no poi fit
        if mode == FitMode.NOMINAL:
            # restore initial parameter values after each fit
            self.load_snapshot(snapshot_name["cond"])
            if len(pois) > 0:
                # fix other pois if they are not studied
                for poi in self.model.pois:
                    poi.setConstant(1)
                for poi in pois:
                    poi.setConstant(0)
            self.minimizer.create_nll()
            prefit_nll = self.minimizer.nll.getVal()
            fit_status = self.minimizer.minimize()
            roofit_result = self.minimizer.fit_result
            self.save_snapshot("nllFit", WSArgument.MUTABLE)
            postfit_nll = self.minimizer.nll.getVal()
            fit_time = time.time() - start_time
            
        # unconditional nll
        if mode in [FitMode.HYBRID, FitMode.UNCOND, FitMode.NOFIT]:
            # restore initial parameter values after each fit
            self.load_snapshot(snapshot_name["uncond"])
            # fix other pois if they are not studied
            for poi in self.model.pois:
                poi.setConstant(1)
            for poi in pois:
                poi.setConstant(0)
            if mode == FitMode.NOFIT:
                self.minimizer.create_nll()
                fit_status_uncond = None
                roofit_result['uncond'] = None
            else:
                fit_status_uncond = self.minimizer.minimize()
                roofit_result['uncond'] = self.minimizer.fit_result
            self.save_snapshot("uncondFit", WSArgument.MUTABLE)
            nll_uncond = self.minimizer.nll.getVal()
            for poi in pois:
                poi_name = poi.GetName()
                muhat[poi_name]       = poi.getVal()
                muhat_errlo[poi_name] = poi.getErrorLo()
                muhat_errhi[poi_name] = poi.getErrorHi()
        fit_time_uncond = time.time() - start_time
        # conditional nll
        if mode in [FitMode.HYBRID, FitMode.COND]:
            # restore initial parameter values after each fit
            self.load_snapshot(snapshot_name["cond"])
            # fix other pois if they are not studied
            for poi in self.model.pois:
                poi.setConstant(1)
            for poi in pois:
                val = poi_val[poi.GetName()]
                # profiled poi
                if val is None:
                    poi.setConstant(0)
                else:
                    poi.setConstant(1)
                    poi.setVal(val)
            fit_status_cond = self.minimizer.minimize()
            roofit_result['cond'] = self.minimizer.fit_result
            self.save_snapshot("condFit", WSArgument.MUTABLE)
            nll_cond = self.minimizer.nll.getVal()
        fit_time_cond = time.time() - fit_time_uncond - start_time
        
        fit_result = {}
        self.stdout.info("INFO: NLL evaluation completed with")
        if mode in [FitMode.HYBRID, FitMode.UNCOND, FitMode.NOFIT]:
            best_fit_str = ", ".join([f"{name} = {value:.5f}" for name, value in muhat.items()])
            self.stdout.info("best fit : ".rjust(15) + f"{best_fit_str}")
            self.stdout.info("uncond NLL = ".rjust(15) + f"{nll_uncond:.5f}")
            fit_result['uncond_fit'] = {
                'muhat': muhat,
                'muhat_errlo': muhat_errlo,
                'muhat_errhi': muhat_errhi,
                'nll': nll_uncond,
                'status': fit_status_uncond,
                'time': fit_time_uncond
            }
        if mode in [FitMode.HYBRID, FitMode.COND]:
            mu = {name:pretty_value(value) for name, value in poi_val.items()}
            mu_str = ", ".join([f"{name} = {pretty_value(value)}" for name, value in poi_val.items()])
            self.stdout.info("mu : ".rjust(15) + f"{mu_str}")
            # also add the best-fit value for profiled POIs
            for name, value in poi_val.items():
                if value == None:
                    muhat[name] = self.model.workspace.var(name).getVal()
            self.stdout.info("cond NLL = ".rjust(15)+f"{nll_cond:.5f}")
            fit_result['cond_fit'] = {
                'mu': mu,
                'muhat': muhat,
                'nll': nll_cond,
                'status': fit_status_cond,
                'time': fit_time_cond
            }
            
        if mode == FitMode.HYBRID:
            pnll = nll_cond - nll_uncond
            qmu  = 2*pnll
            self.stdout.info("PNLL = ".rjust(15) + "{:.5f}".format(nll_cond - nll_uncond))
            fit_result['pnll'] = pnll
            fit_result['qmu']  = qmu
            
            if (qmu >= 0):
                ndof = len(pois)
                if ndof == 1:
                    # ndof = 1 case
                    poi_name = pois.first().GetName()
                    x0 = poi_val[poi_name]
                    significance = math.sqrt(qmu)
                    pvalue = 1 - ROOT.Math.normal_cdf(significance, 1, x0)
                else:
                    x0 = list(set(poi_val.values()))
                    if len(x0) > 1:
                        fit_result['significance'] = None
                        fit_result['pvalue'] = None
                    else:
                        pvalue = ROOT.Math.chisquared_cdf_c(qmu, ndof, x0[0])
                        significance = ROOT.RooStats.PValueToSignificance(pvalue)
                fit_result['significance'] = significance
                fit_result['pvalue'] = pvalue
            else:
                fit_result['significance'] = None
                fit_result['pvalue'] = None
                
        if mode != FitMode.NOMINAL:
            self.stdout.info("time = ".rjust(15) + \
                             "(uncond_fit) {:.3f}, (cond_fit) {:.3f}".format(fit_time_uncond, fit_time_cond))
            fit_result['total_time'] = fit_time_uncond + fit_time_cond
        else:
            self.stdout.info("prefit NLL = ".rjust(18) + f"{prefit_nll:.5f}")
            self.stdout.info("postfit NLL = ".rjust(18) + f"{postfit_nll:.5f}")
            self.stdout.info("time = ".rjust(18) + f"{fit_time:.3f}")
            fit_result['prefit_nll'] = prefit_nll
            fit_result['postfit_nll'] = postfit_nll
            fit_result['total_time'] = fit_time
        
        self.roofit_result = roofit_result
        
        # finallizing
        self.minimizer.config['minos'] = tmp_do_minos
        self.minimizer.minos_set = ROOT.RooArgSet()
        
        return fit_result
        
    def evaluate_nll(self, poi_val:Optional[Union[Dict[str, float], float]]=None,
                     mode:Union[int, str, FitMode]="uncond",
                     snapshot_name:Optional[str]=AnalysisObject.kCurrentSnapshotName):
        """
        Evalute post-fit NLL value
        
        Parameters
        ------------------------------------------------------------------------------
        poi_val: (optional) float or dictionary of float
            Value(s) of parameter(s) of interest when performing a conditional MLE fit.
            If value is a float, then all parameters of interest will be assigned the given value.
            If value is a dictionary, it represents a map between the parameter name and the assigned value.
            Any missing parameter name will be assigned its current value (as in the snapshot).
        mode: int, str or FitMode, default = "uncond"
            Evaluation mode. Choose from:
                0: Evaluate nll_mu - nll_muhat
                1: Evaluate unconditional NLL (nll_muhat)
                2: Evaluate conditional NLL (nll_mu)
                3: Evaluate post-fit NLL (POI state remain as is)
        snapshot_name: (Optional) str, default=AnalysisObject.kCurrentSnapshotName
            Name of snapshot to load before fitting.
        """
        fit_result = self.nll_fit(poi_val=poi_val, mode=mode, snapshot_name=snapshot_name)
        mode = FitMode.parse(mode)
        if mode == FitMode.HYBRID:
            return fit_result['pnll']
        elif mode == FitMode.UNCOND:
            return fit_result['uncond_fit']['nll']
        elif mode == FitMode.COND:
            return fit_result['cond_fit']['nll']
        elif mode == FitMode.NOMINAL:
            return fit_result['postfit_nll']