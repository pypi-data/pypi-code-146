from typing import Optional, Dict, List
import uuid

import ROOT

from .tree_data_source import TreeDataSource

def template_Gaussian(reference_data:TreeDataSource):
    hist = reference_data.create_histogram()
    # evaluate shape properties
    hist_max             = hist.GetMaximum()
    hist_bin_pos_max     = hist.GetMaximumBin()
    hist_pos_max         = hist.GetBinCenter(hist_bin_pos_max)
    hist_pos_FWHM_low    = hist.GetBinCenter(hist.FindFirstBinAbove(0.5 * hist_max))
    hist_pos_FWHM_high   = hist.GetBinCenter(hist.FindLastBinAbove(0.5 * hist_max))
    hist_sigma_effective = (hist_pos_FWHM_high - hist_pos_FWHM_low) / 2.355;
    # free memory
    hist.Delete()
    parameters = {
        'mean'  : ROOT.RooRealVar("mean", "mean", hist_pos_max, hist_pos_FWHM_low, hist_pos_FWHM_high),
        'sigma' : ROOT.RooRealVar("sigma", "sigma", hist_sigma_effective, 0., 5 * hist_sigma_effective)
    }
    return parameters

def template_DSCB(reference_data:TreeDataSource):
    hist = reference_data.create_histogram()
    # evaluate shape properties
    hist_max             = hist.GetMaximum()
    hist_bin_pos_max     = hist.GetMaximumBin()
    hist_pos_max         = hist.GetBinCenter(hist_bin_pos_max)
    hist_pos_FWHM_low    = hist.GetBinCenter(hist.FindFirstBinAbove(0.5 * hist_max))
    hist_pos_FWHM_high   = hist.GetBinCenter(hist.FindLastBinAbove(0.5 * hist_max))
    hist_sigma_effective = (hist_pos_FWHM_high - hist_pos_FWHM_low) / 2.355;
    # free memory
    hist.Delete()
    parameters = {
        'muCBNom'    : ROOT.RooRealVar("muCBNom", "mean of CB", hist_pos_max, hist_pos_FWHM_low, hist_pos_FWHM_high),
        'sigmaCBNom' : ROOT.RooRealVar("sigmaCBNom", "sigma of CB", hist_sigma_effective, 0., 5 * hist_sigma_effective),
        'alphaCBLo'  : ROOT.RooRealVar("alphaCBLo", "Location of transition to a power law on the left", 1, 0., 5.),
        'nCBLo'      : ROOT.RooRealVar("nCBLo", "Exponent of power-law tail on the left", 10, 0., 200.),
        'alphaCBHi'  : ROOT.RooRealVar("alphaCBHi", "Location of transition to a power law on the right", 1, 0., 5.),
        'nCBHi'      : ROOT.RooRealVar("nCBHi", "Exponent of power-law tail on the right", 10, 0., 200.)
    }
    return parameters

def template_Bukin(reference_data:TreeDataSource):
    hist = reference_data.create_histogram()
    # evaluate shape properties
    hist_max             = hist.GetMaximum()
    hist_bin_pos_max     = hist.GetMaximumBin()
    hist_pos_max         = hist.GetBinCenter(hist_bin_pos_max)
    hist_pos_FWHM_low    = hist.GetBinCenter(hist.FindFirstBinAbove(0.5 * hist_max))
    hist_pos_FWHM_high   = hist.GetBinCenter(hist.FindLastBinAbove(0.5 * hist_max))
    hist_sigma_effective = (hist_pos_FWHM_high - hist_pos_FWHM_low) / 2.355;    
    parameters = {
        "Xp"  : ROOT.RooRealVar("Bukin_Xp", "peak position", hist_pos_max, hist_pos_FWHM_low, hist_pos_FWHM_high),
        "sigp": ROOT.RooRealVar("Bukin_sigp", "peak width as FWHM divided by 2*sqrt(2*log(2))=2.35",
                                      hist_sigma_effective, 0.1, 5 * hist_sigma_effective),
        "xi"  : ROOT.RooRealVar("Bukin_xi", "peak asymmetry", 0.0, -1, 1),
        "rho1": ROOT.RooRealVar("Bukin_rho1", "left tail", -0.1, -1.0, 0.0),
        "rho2": ROOT.RooRealVar("Bukin_rho2", "right tail", 0.0, 0.0, 1.0)
    }
    return parameters

def template_ExpGaussExp(reference_data:TreeDataSource):
    parameters = {
        "EGE_mean"  : ROOT.RooRealVar("EGE_mean", "mean of EGE", 124.5, 123., 126.),
        "EGE_sigma" : ROOT.RooRealVar("EGE_sigma", "sigma of EGE", 2.5, 0.5, 8.0),
        "EGE_kLo"   : ROOT.RooRealVar("EGE_kLo", "kLow of EGE", 2.5, 0.01, 10.0),
        "EGE_kHi"   : ROOT.RooRealVar("EGE_kHi", "kHigh of EGE", 2.4, 0.01, 10.0)
    }
    return parameters

def template_Exp(reference_data:TreeDataSource):
    parameters = {
        "Exp_c": ROOT.RooRealVar("Exp_c", "Exp_c", 1, -10, 10)
    }
    return parameters

template_maps = {
    'DSCB': template_DSCB,
    'RooCrystalBall_DSCB': template_DSCB,
    'RooTwoSidedCBShape': template_DSCB,
    'ExpGaussExp': template_ExpGaussExp,
    'RooExpGaussExpShape': template_ExpGaussExp,
    'Bukin': template_Bukin,
    'RooBukinPdf': template_Bukin,
    'Exp': template_Exp,
    'RooExponential': template_Exp,
    'RooGaussian': template_Gaussian,
    'Gaussian': template_Gaussian
}

def get_param_templates(model:str):
    if model not in template_maps:
        raise RuntimeError(f"no default parameter templates found for the model \"{model}\"")
    return template_maps[model]