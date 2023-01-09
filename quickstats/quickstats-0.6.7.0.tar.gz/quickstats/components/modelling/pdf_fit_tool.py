from typing import List, Optional, Union, Dict, Callable, Tuple

import ROOT

from quickstats import AbstractObject, semistaticmethod

class PdfFitTool(AbstractObject):
    
    def __init__(self, pdf:"ROOT.RooAbsPdf", data:"ROOT.RooAbsData",
                 verbosity:str="INFO"):
        super().__init__(verbosity=verbosity)
        
        self.pdf        = pdf
        self.data       = data
        
    @staticmethod
    def is_fit_success(fit_result:"ROOT.RooFitResult"):
        status   = fit_result.status()
        cov_qual = fit_result.covQual()
        return (status == 0) and (cov_qual in [-1, 3])
    
    @staticmethod
    def _set_pdf_param_values(pdf:ROOT.RooAbsPdf, observable:ROOT.RooRealVar, param_values:Dict):
        params = pdf.getParameters(observable)
        for param in params:
            param_name = param.GetName()
            if param_name not in param_values:
                raise RuntimeError(f"missing value for the parameter: {param_name}")
            param_value = param_values[param_name]
            param.setVal(param_value)
            
    @semistaticmethod
    def _get_fit_stats(self, model:"ROOT.RooAbsPdf", data:"ROOT.RooAbsData",
                       n_bins:Optional[int]=None, n_float_params:int=0):
        observable = self.get_observable(data)
        if n_bins is None:
            n_bins = observable.numBins()
        # +1 is there to account for the normalization that is done internally in RootFit
        ndf = n_bins - (n_float_params + 1)
        frame = observable.frame()
        data.plotOn(frame)
        model.plotOn(frame)
        chi2_reduced = frame.chiSquare(n_float_params)
        chi2 = chi2_reduced * ndf
        pvalue = ROOT.TMath.Prob(chi2, ndf)
        fit_stats = {
            'n_bins': n_bins,
            'n_float_params': n_float_params,
            'ndf': ndf,
            'chi2/ndf': chi2_reduced,
            'chi2': chi2,
            'pvalue': pvalue
        }
        return fit_stats
    
    def get_fit_stats(self, n_bins:Optional[int]=None, n_float_params:int=0):
        """
        Parameters
            n_bins: (optional) int
                Number of bins used for chi2 calculation. If not specified, the number of bins of the 
                observable is used.
            n_float_params: int, default = 0
                Number of floating parameters in the fit. This decreases the number of degrees of freedom
                used in chi2 calculation.
        """
        return self._get_fit_stats(self.pdf, self.data, n_bins=n_bins, n_float_params=n_float_params)
    
    @semistaticmethod
    def print_fit_stats(self, fit_stats:Dict):
        self.stdout.info(f"INFO: chi^2/ndf = {fit_stats['chi2/ndf']}, "
                         f"Number of Floating Parameters + Normalization = {fit_stats['n_float_params'] + 1}, "
                         f"Number of bins = {fit_stats['n_bins']}, "
                         f"ndf = {fit_stats['ndf']}, "
                         f"chi^2 = {fit_stats['chi2']}, "
                         f"p_value = {fit_stats['pvalue']}")
    
    @staticmethod
    def get_observable(data:"ROOT.RooAbsData"):
        parameters = data.get()
        if len(parameters) > 1:
            raise RuntimeError("only single-observable fit is allowed")
        observable = parameters.first()
        return observable
        
    def mle_fit(self, minos:bool=False, hesse:bool=True, sumw2:bool=True, strategy:int=1,
                min_fit:int=2, max_fit:int=3, range_expand_rate:Optional[int]=None, print_level:int=-1):
        
        observable = self.get_observable(self.data)
        vmin = observable.getMin()
        vmax = observable.getMax()
        observable.setRange("fitRange", vmin, vmax)
        
        model_name = self.pdf.GetName()
        data_name  = self.data.GetName()
        obs_name   = observable.GetName()
        
        self.stdout.info(f"INFO: Begin model fitting...")
        self.stdout.info(f"      Model : ".rjust(20) + f"{model_name}")
        self.stdout.info(f"    Dataset : ".rjust(20) + f"{data_name}")
        self.stdout.info(f" Observable : ".rjust(20) + f"{obs_name}")
        
        fit_args = [ROOT.RooFit.Range("fitRange"), ROOT.RooFit.PrintLevel(print_level),
                    ROOT.RooFit.Minos(minos), ROOT.RooFit.Hesse(hesse),
                    ROOT.RooFit.Save(), ROOT.RooFit.SumW2Error(sumw2),
                    ROOT.RooFit.Strategy(strategy)]

        status_label = {
            True  : 'SUCCESS',
            False : 'FAIL'
        }

        for i in range(1, max_fit + 1):
            fit_result = self.pdf.fitTo(self.data, *fit_args)
            is_success = self.is_fit_success(fit_result)
            self.stdout.info(f" Fit iteration {i} : ".rjust(20) + f"{status_label[is_success]}")
            if i >= min_fit:
                if is_success:
                    return fit_result
                elif range_expand_rate is not None:
                    new_vmin = observable.getRange("fitRange").first - range_expand_rate
                    new_vmax = observable.getRange("fitRange").second + range_expand_rate
                    self.stdout.info(f"INFO: Fit failed to converge, refitting with "
                                     f"expanded fit range [{new_vmin}, {new_vmax}]")
                    observable.setRange("fitRange", new_vmin, new_vmax)
        return fit_result