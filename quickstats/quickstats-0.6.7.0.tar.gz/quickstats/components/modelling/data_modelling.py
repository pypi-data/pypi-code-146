from typing import List, Optional, Union, Dict, Callable, Tuple
from itertools import repeat
import os
import sys
import copy
import json
import time
import uuid

import numpy as np

import ROOT

import quickstats
from quickstats import semistaticmethod, Timer
from quickstats.components import ROOTObject
from quickstats.components.modelling import TreeDataSource, PdfFitTool
from quickstats.utils.common_utils import combine_dict, execute_multi_tasks

class DataModelling(ROOTObject):
    
    _DEFAULT_FIT_OPTION_ = {
        'print_level': -1,
        'min_fit': 2,
        'max_fit': 3,
        'binned': False,
        'minos': False,
        'hesse': True,
        'sumw2': True,
        'strategy': 1,
        'range_expand_rate': 1        
    }
    
    _DEFAULT_PLOT_OPTION_ = {
        'bin_range': None,
        'n_bins_data': None,
        'n_bins_pdf': 1000,
        'bin_error': True,
        'show_comparison': True,
        'show_params': True,
        'show_stats': True,
        'show_error': True,        
        'value_fmt': "{:.2f}",
        'stats_list': ["chi2/ndf"],
        'comparison_options':{
            "styles": {
              "color": "k"  
            },            
            "mode": "difference",
            "label": "Fit - MC"            
        },
        'draw_options':{},
        'styles': None,
        'xlabel': None,
        'ylabel': "Events / ({bin_width:.2f})",
        'annotations': None,
        'label_map': {
            'data' : "MC",
            'pdf'  : "Fit"
        }
    }

    # pdf class defined in macros
    _EXTERNAL_PDF_ = ['RooTwoSidedCBShape']
    
    _PDF_MAP_ = {
        'RooCrystalBall_DSCB' : 'RooCrystalBall',
        'DSCB'                : 'RooTwoSidedCBShape',
        'ExpGaussExp'         : 'RooExpGaussExpShape',
        'Exp'                 : 'RooExponential',
        'Bukin'               : 'RooBukinPdf',
        'Gaussian'            : 'RooGaussian',
        'Gaus'                : 'RooGaussian'
    }
    
    _DEFAULT_ROOT_CONFIG_ = {
        "SetBatch" : True,
        "TH1Sumw2" : True
    }
    
    _REQUIRE_CONFIG_ = {
        "ROOT"  : True,
        "RooFit": True
    }
    
    @property
    def plot_options(self):
        return self._plot_options
    
    @property
    def fit_options(self):
        return self._fit_options
    
    @property
    def model_class(self):
        return self._model_class
    
    @property
    def param_templates(self):
        return self._param_templates

    def __init__(self, observable:str, fit_range:Union[List[float], Tuple[float]],
                 functional_form:Union[str, Callable],
                 param_templates:Optional[Callable]=None,
                 weight:str="weight", n_bins:Optional[int]=None,
                 fit_options:Optional[Dict]=None,
                 plot_options:Optional[Dict]=None,
                 verbosity:str="INFO"):
        """
        Modelling of a data distribution by a simple analytic function.
        
        Parameters:
            observable: str
                Name of observable.
        """
        self._fit_options  = self._DEFAULT_FIT_OPTION_
        self._plot_options = self._DEFAULT_PLOT_OPTION_
        _fit_options = {
            'functional_form' : functional_form,
            'observable'      : observable,
            'range'           : fit_range,
            'n_bins'          : n_bins,
            'weight'          : weight
        }
        fit_options = combine_dict(_fit_options, fit_options)
        self.update_fit_options(fit_options)
        self.update_plot_options(plot_options)
        self.set_param_templates(param_templates)
        self.set_functional_form(functional_form)
        roofit_config = {
            "MinimizerPrintLevel": self.fit_options.get("print_level", -1)
        }
        super().__init__(roofit_config=roofit_config,
                         verbosity=verbosity)
        
    def update_fit_options(self, options:Optional[Dict]=None):
        self._fit_options = combine_dict(self._fit_options, options)
        
    def update_plot_options(self, options:Optional[Dict]=None):
        self._plot_options = combine_dict(self._plot_options, options)        
        
    def set_param_templates(self, param_templates:Callable):
        self._param_templates = param_templates
        
    def set_functional_form(self, functional_form:Union[str, Callable]):
        self._model_class = self.get_model_class(functional_form)
        if self.param_templates is None:
            if isinstance(functional_form, str):
                param_templates = self.get_param_templates(functional_form)
                self.set_param_templates(param_templates)
            else:
                raise RuntimeError("missing parameter templates definition")
                
    @semistaticmethod
    def get_model_class(self, name:Union[str, Callable]):
        if isinstance(name, Callable):
            return name
        pdf_name = self._PDF_MAP_.get(name, name)
        if not hasattr(ROOT, pdf_name):
            if pdf_name in self._EXTERNAL_PDF_:
                self.load_extension(pdf_name)
            else:
                raise ValueError(f"{name} is not a valid pdf name defined by ROOT")
        if not hasattr(ROOT, pdf_name):
            raise RuntimeError(f"failed to load pdf {pdf_name}")
        pdf = getattr(ROOT, pdf_name)
        return pdf
    
    @semistaticmethod
    def get_param_templates(self, name:Union[str, Callable]):
        if isinstance(name, Callable):
            return name
        from .parameter_templates import get_param_templates
        return get_param_templates(name)

    def sanity_check(self):
        if self.model_class is None:
            raise RuntimeError("model pdf not set")
        if self.param_templates is None:
            raise RuntimeError("model parameter templates not set")
    
    @staticmethod
    def get_param_data(parameters:List["ROOT.RooRealVar"], value_only:bool=False):
        param_data = {}
        for name in parameters:
            if value_only:
                param_data[name] = parameters[name].getVal()
            else:
                param_data[name] = {
                    'value'  : parameters[name].getVal(),
                    'errorhi': parameters[name].getErrorHi(),
                    'errorlo': parameters[name].getErrorLo(),
                    'error'  : parameters[name].getError()
                }
        return param_data

    @semistaticmethod
    def _run(self, filename:str, tree_name:str, model_class:Callable, param_templates:Callable,
             fit_options:Dict, plot_options:Optional[Dict]=None, save_summary_as:Optional[str]=None, 
             save_param_as:Optional[str]=None, save_plot_as:Optional[str]=None):
        
        with Timer() as t:
            canvas = ROOT.TCanvas(uuid.uuid4().hex)
            observable_config = {
                'name'        : fit_options['observable'],
                'range'       : fit_options['range'],
                'n_bins'      : fit_options['n_bins']
            }
            data_source = TreeDataSource(tree_name, filename,
                                         observable=observable_config,
                                         weight_name=fit_options['weight'])
            # create dataset
            dataset_name = f"dataset_{observable_config['name']}"
            dataset = data_source.create_dataset(dataset_name)
            observable = dataset.get().first()
            
            # create model pdf
            model_name = f"model_{model_class.Class_Name()}"
            model_parameters = param_templates(data_source)
            model_pdf = model_class(model_name, model_name, observable, *model_parameters.values())

            fit_kwargs = {
                'minos'             : fit_options['minos'],
                'hesse'             : fit_options['hesse'],
                'strategy'          : fit_options['strategy'],
                'sumw2'             : fit_options['sumw2'],
                'min_fit'           : fit_options['min_fit'],
                'max_fit'           : fit_options['max_fit'],
                'range_expand_rate' : fit_options['range_expand_rate'],
                'print_level'       : fit_options['print_level']
            }

            fit_tool   = PdfFitTool(model_pdf, dataset, verbosity=self.stdout.verbosity)
            fit_result = fit_tool.mle_fit(**fit_kwargs)
            fit_result.Print()

            n_float_params = fit_result.floatParsFinal().getSize()
            fit_stats = fit_tool.get_fit_stats(n_float_params=n_float_params)
            fit_tool.print_fit_stats(fit_stats)

            # free memory
            canvas.Close()
            ROOT.gSystem.ProcessEvents()
            
        self.stdout.info(f"INFO: Task finished. Total time taken: {t.interval:.3f}s")
        
        param_data = self.get_param_data(model_parameters)
        param_data_value_only = self.get_param_data(model_parameters, value_only=True)
        summary = {"filename"    : filename,
                   "parameters"  : param_data,
                   "fit_options" : copy.deepcopy(fit_options),
                   "stats"       : fit_stats,
                   "time"        : t.interval}
        if not isinstance(summary['fit_options']['functional_form'], str):
            summary['fit_options']['functional_form'] = type(summary['fit_options']['functional_form']).__name__
            
        if save_plot_as is not None:
            self.create_plot(dataset, model_pdf, observable,
                             plot_options=plot_options,
                             model_summary=summary,
                             save_as=save_plot_as)

        if save_param_as is not None:
            with open(save_param_as, "w") as outfile:
                json.dump(param_data_value_only, outfile, indent=2)
                
        if save_summary_as is not None:
            with open(save_summary_as, "w") as outfile:
                json.dump(summary, outfile, indent=2)

        return summary
    
    @semistaticmethod
    def create_plot(self, data:ROOT.RooDataSet, pdf:ROOT.RooAbsPdf,
                    observable:Optional[ROOT.RooRealVar]=None,
                    plot_options:Optional[Dict]=None,
                    model_summary:Optional[Dict]=None,
                    save_as:Optional[str]=None):
        
        if observable is None:
            parameters = data.get()
            if len(parameters) > 1:
                raise RuntimeError("only single-observable dataset is allowed")
            observable = parameters.first()
        
        plot_options = combine_dict(self._DEFAULT_PLOT_OPTION_, plot_options)
            
        init_kwargs = {
            "bin_range"   : plot_options["bin_range"],
            "n_bins_data" : plot_options["n_bins_data"],
            "n_bins_pdf"  : plot_options["n_bins_pdf"],
            "bin_error"   : plot_options["bin_error"],
            "label_map"   : plot_options["label_map"],
            "color_cycle" : plot_options.get("color_cycle", None),
            "styles"      : plot_options.get("styles", None),
            "analysis_label_options" : plot_options.get("analysis_label_options", None),
            "config"      : plot_options.get("config", None)
        }
        
        from quickstats.plots import PdfDistributionPlot
        plotter = PdfDistributionPlot.from_roofit_data(data, pdf, observable, **init_kwargs)
        
        if model_summary is not None:
            value_fmt = plot_options["value_fmt"]
            annotation_text = ""
            if plot_options['show_params']:
                param_data = model_summary["parameters"]
                for param in param_data:
                    value = value_fmt.format(param_data[param]["value"])
                    if plot_options["show_error"]:
                        error = value_fmt.format(param_data[param]["error"])
                        annotation_text += f"{param} = {value} $\\pm$ {error}\n"
                    else:
                        annotation_text += f"{param} = {value}\n"
                annotation_text += "\n"
            if plot_options["show_stats"]:
                stats_list = plot_options["stats_list"]
                for stat in stats_list:
                    if stat not in model_summary["stats"]:
                        raise RuntimeError(f"invalid stats item: {stat}")
                    value = value_fmt.format(model_summary["stats"][stat])
                    annotation_text += f"{stat} = {value}\n"
                annotation_text += "\n"
            plotter.add_annotation(annotation_text)
        
        annotations = plot_options.get("annotations", None)
        if annotations is not None:
            if isinstance(annotations, dict):
                plotter.add_annotation(**annotations)
            elif isinstance(annotations, list):
                for annotation in annotations:
                    plotter.add_annotation(**annotation)
            else:
                raise ValueError('invalid format for the fit option "annotations"')
        
        xlabel, ylabel = plot_options["xlabel"], plot_options["ylabel"]
        if (xlabel is None):
            xlabel = observable.GetName()
        # deduce bin width from data
        if (ylabel is not None) and "bin_width" in ylabel:
            bin_width = np.unique(np.diff(plotter.collective_data['data']['x']))
            if (len(bin_width) > 1) and (not np.allclose(bin_width, bin_width[0])):
                raise RuntimeError("can not deduce bin width: non-uniform binnings detected")
            bin_width = bin_width[0]
            ylabel = ylabel.format(bin_width=bin_width)            
        
        if plot_options["show_comparison"]:
            comparison_options = {
                "reference": "data",
                "target": "pdf_data_binning"
            }
            comparison_options = combine_dict(comparison_options, plot_options["comparison_options"])
        else:
            comparison_options = None
            
        draw_options = plot_options.get("draw_options", {})

        ax = plotter.draw(xlabel=xlabel, ylabel=ylabel, targets=["data", "pdf"],
                          comparison_options=comparison_options, **draw_options)
        
        import matplotlib.pyplot as plt
        if save_as is not None:
            plt.savefig(save_as, bbox_inches="tight")
        plt.show()

    def run(self, filename:str, tree_name:str, save_summary_as:Optional[str]=None, 
            save_param_as:Optional[str]=None, save_plot_as:Optional[str]=None):
        summary = self._run(filename, tree_name, model_class=self.model_class, 
                            param_templates=self.param_templates,
                            fit_options=self.fit_options,
                            plot_options=self.plot_options,
                            save_summary_as=save_summary_as,
                            save_param_as=save_param_as,
                            save_plot_as=save_plot_as)
        return summary
    
    @staticmethod
    def _get_iter_save_paths(filenames:List[str], save_paths:Optional[Union[List[str], str]]=None):
        # do not save
        if save_paths is None:
            return repeat(None)
        # save by expression
        elif isinstance(save_paths, str):
            _save_paths = []
            for filename in filenames:
                basename = os.path.splitext(os.path.basename(filename))[0]
                _save_paths.append(save_paths.format(basename=basename))
            return _save_paths
        # save by explicit paths
        elif isinstance(save_paths, list):
            if len(filenames) != len(save_paths):
                raise RuntimeError("number of output file paths must match the number input files")
            return save_paths
        else:
            raise ValueError("invalid save option")
        
    def batch_run(self, filenames:List[str], tree_name:str,
                  save_summary_as:Optional[Union[List[str], str]]=None,
                  save_param_as:Optional[Union[List[str], str]]=None,
                  save_plot_as:Optional[Union[List[str], str]]=None,
                  plot_options:Optional[List]=None, parallel:int=-1):
        self.sanity_check()
        save_summary_as = self._get_iter_save_paths(filenames, save_summary_as)
        save_param_as   = self._get_iter_save_paths(filenames, save_param_as)
        save_plot_as    = self._get_iter_save_paths(filenames, save_plot_as)
        if plot_options is None:
            plot_options = repeat(self.plot_options)
        elif isinstance(plot_options, dict):
            plot_options = repeat(combine_dict(self.plot_options, plot_options))
        elif isinstance(plot_options, list):
            plot_options = [combine_dict(self.plot_options, _plot_options) for _plot_options in plot_options]
        else:
            raise ValueError("invalid plot options")
        args = (filenames, repeat(tree_name), repeat(self.model_class),
                repeat(self.param_templates), repeat(self.fit_options),
                plot_options, save_summary_as, save_param_as, 
                save_plot_as)
        results = execute_multi_tasks(self._run, *args, parallel=parallel)
        return results
    
    def run_over_categories(self, prefix:str, categories:List[str],
                            tree_name:str, input_dir:str="./",
                            save_summary_as:Optional[Union[List[str], str]]=None,
                            save_param_as:Optional[Union[List[str], str]]=None,
                            save_plot_as:Optional[Union[List[str], str]]=None,
                            save_merged_param_as:str="model_parameters.json",
                            plot_options:Optional[List]=None,
                            parallel:int=-1):
        filenames = []
        for category in categories:
            filename = os.path.join(input_dir, f"{prefix}_{category}.root")
            filenames.append(filename)

        results = self.batch_run(filenames, tree_name,
                                 save_summary_as=save_summary_as,
                                 save_param_as=save_param_as,
                                 save_plot_as=save_plot_as,
                                 plot_options=plot_options,
                                 parallel=parallel)
        
        # merge parameter data in each category
        category_results = dict(zip(categories, results))
        if save_merged_param_as is not None:
            param_data = {}
            for category, result in category_results.items():
                param_data[category] = {name: data["value"] for name, data in result['parameters'].items()}
            with open(save_merged_param_as, "w") as outfile:
                json.dump(param_data, outfile, indent=2)
        return category_results