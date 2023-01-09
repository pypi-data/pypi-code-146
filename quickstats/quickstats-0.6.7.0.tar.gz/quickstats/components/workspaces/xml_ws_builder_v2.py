###############################################################################
### This is a reimplementation of xmlAnaWSBuilder library in python
### original author: Hongtao Yang
###############################################################################
import os
import re
import time
from typing import Optional, Union, List, Dict

import numpy as np

import ROOT

from quickstats import semistaticmethod, DescriptiveEnum, PathManager
from quickstats.components import ExtendedModel
from quickstats.utils.io import Verbosity
from quickstats.utils.xml_tools import TXMLTree
from quickstats.utils.common_utils import remove_list_duplicates, format_delimiter_enclosed_text
from quickstats.maths.numerics import is_float, pretty_value
from quickstats.interface.root import TH1, RooDataSet

from quickstats.components.workspaces import (XMLWSBase, Sample, Systematic, SystematicType,
                                              SystematicsDomain, AsimovHandler, CoreArgumentSets)

from .settings import *

class DataStorageType(DescriptiveEnum):
    Tree      = (0, "Store data as a tree")
    Vector    = (1, "Store data as a vector")
    Composite = (2, "Store data as a mixture of tree and vector")

class SampleFactorType(DescriptiveEnum):
    NormFactor  = (0, "Normalization factor")
    ShapeFactor = (1, "Shape factor")
    
class XMLWSBuilder(XMLWSBase):
    
    EPSILON = 1e-6
    
    def __init__(self, source:str, basedir:Optional[str]=None,
                 use_binned:bool=False,
                 data_storage_type:str="vector",
                 minimizer_config:Optional[Dict]=None,
                 unlimited_stack:bool=True,
                 verbosity:Optional[Union[int, str]]="INFO") -> None:
        super().__init__(source=source, basedir=basedir,
                         unlimited_stack=unlimited_stack,
                         verbosity=verbosity)
        self.use_binned = use_binned
        self.data_storage_type = data_storage_type
        self.minimizer_config = minimizer_config
        self.load_extension()
        self.initialize(source=source)

    def initialize(self, source:str) -> None:
        self.core_config = self.parse_core_xml(source)
        self.update_paths()
        self.reset()
        self.set_data_storage_type(self.data_storage_type)
        self.set_integrator(self.core_config['integrator'])
        self.print_init_summary()
        
    def reset(self) -> None:
        self.cat_config      = {}
        self.cat_ws          = {}
        self.datahists       = {}
        self.datasets        = {}
        self.datasets_binned = {}
        self.time_taken      = 0.
        ws_name = self.core_config['workspace_name']
        mc_name = self.core_config['model_config_name']
        self.comb_ws      = ROOT.RooWorkspace(ws_name)
        self.model_config = ROOT.RooStats.ModelConfig(mc_name, self.comb_ws)
        
    def update_paths(self) -> None:
        self.path_manager.set_file("output", self.core_config["output_name"])
        categories = []
        for category, file in self.core_config['input_categories'].items():
            self.path_manager.set_file(f"__Cat_{category}", file)
                                       
    @semistaticmethod
    def set_data_storage_type(self, data_storage_type:Union[str, DataStorageType]="vector") -> None:
        data_storage_type = DataStorageType.parse(data_storage_type)
        self.stdout.info(f'INFO: Set data storage type to "{data_storage_type.name}"')
        if data_storage_type == DataStorageType.Tree:
            ROOT.RooAbsData.setDefaultStorageType(ROOT.RooAbsData.StorageType.Tree)
        elif data_storage_type == DataStorageType.Vector:
            ROOT.RooAbsData.setDefaultStorageType(ROOT.RooAbsData.StorageType.Vector)
        elif data_storage_type == DataStorageType.Composite:
            ROOT.RooAbsData.setDefaultStorageType(ROOT.RooAbsData.StorageType.Composite)            
        else:
            raise RuntimeError(f'unknown data storage type "{data_storage_type}"')
            
    @semistaticmethod
    def set_integrator(self, integrator:Optional[str]=None) -> None:
        if integrator:
            self.stdout.warn(f'WARNING: Set default integrator to "{integrator}"')
            ROOT.RooAbsReal.defaultIntegratorConfig().method1D().setLabel(integrator)
    
    def parse_core_xml(self, filename:str) -> Dict:
        self.stdout.info(f'INFO: Parsing file "{filename}"')
        # load xml file
        core_xml = TXMLTree.load_as_dict(filename)
        # parse core attributes
        attributes = core_xml['attrib']
        core_config = {
            'base_dir'           : os.path.dirname(filename),
            'workspace_name'     : self._get_node_attrib(core_xml, 'WorkspaceName'),
            'model_config_name'  : self._get_node_attrib(core_xml, 'ModelConfigName'),
            'dataset_name'       : self._get_node_attrib(core_xml, 'DataName'),
            'output_name'        : self._get_node_attrib(core_xml, 'OutputFile'),
            'do_blind'           : self._get_node_attrib(core_xml, 'Blind',
                                                         required=False, default=False, dtype="bool"),
            'scale_lumi'         : self._get_node_attrib(core_xml, 'ScaleLumi',
                                                         required=False, default=-1., dtype="float"),
            'integrator'         : self._get_node_attrib(core_xml, 'Integrator',
                                                         required=False, default=""),
            'generate_hist_data' : self._get_node_attrib(core_xml, 'GenHistData',
                                                         required=False, default=False, dtype="bool"),
            'poi_names'          : [],
            'input_categories'   : {},
            'asimov_definitions' : []
        }
        # config for import class codes
        class_decl_import_dir = self._get_node_attrib(core_xml, 'ClassDeclImportDir',
                                                      required=False, default='inc/')
        class_decl_import_dir = self.path_manager.get_relpath(class_decl_import_dir)
        class_impl_import_dir = self._get_node_attrib(core_xml, 'ClassImplImportDir',
                                                      required=False, default='src/')
        class_impl_import_dir = self.path_manager.get_relpath(class_impl_import_dir)
        if os.path.isdir(class_decl_import_dir) and os.path.isdir(class_impl_import_dir):
            core_config['class_code_dirs'] = {
                'decl': class_decl_import_dir,
                'impl': class_impl_import_dir,
            }
        elif (not os.path.isdir(class_decl_import_dir)) and (not os.path.isdir(class_impl_import_dir)):
            core_config['class_code_dirs'] = {
                'decl': None,
                'impl': None,
            }
        else:
            raise FileNotFoundError("directories for importing class code do not exist "
                                    f"(decl = `{class_decl_import_dir}`, impl = `{class_impl_import_dir}`)")
        # make sure output filename has .root extension
        if not core_config['output_name'].endswith(".root"):
            core_config['output_name'] = os.path.splitext(core_config['output_name'])[0] + ".root"
            self.stdout.warning('WARNING: Output file name does not contain ".root" postfix. '
                                'Adding it to avoid confusion.')
        # parse child level nodes
        nodes = core_xml['children']
        for node in nodes:
            tag = node['tag']
            if tag == "Input":
                file = node['text']
                tree = TXMLTree(file=self.path_manager.get_relpath(file))
                category = tree.root.get_attribute("Name")
                if category in core_config['input_categories']:
                    raise RuntimeError(f'duplicated category name: "{category}"')
                core_config['input_categories'][category] = file
            elif tag == "POI":
                poi_expr = node['text']
                core_config['poi_names'] += poi_expr.split(",")
            elif tag == "Asimov":
                definitions = node['attrib']
                core_config['asimov_definitions'].append(definitions)
            else:
                raise RuntimeError(f"unknown item `{tag}`")
        return core_config
    
    def print_init_summary(self) -> None:
        if not self.core_config:
            raise RuntimeError("core config not set")
        self.stdout.info("="*74)
        self.stdout.info("Output file: ".rjust(20) + f"{self.core_config['output_name']}")
        self.stdout.info("Workspace name: ".rjust(20) + f"{self.core_config['workspace_name']}")
        self.stdout.info("ModelConfig name: ".rjust(20) + f"{self.core_config['model_config_name']}")
        self.stdout.info("Dataset name: ".rjust(20) + f"{self.core_config['dataset_name']}")
        self.stdout.info("Blind analysis: ".rjust(20) + ("True" if self.core_config['do_blind'] else "False"))
        self.stdout.info("Generate hist data: ".rjust(20) + ("True" if self.core_config['generate_hist_data'] else "False"))
        self.stdout.info("Scale lumi: ".rjust(20) + f"{self.core_config['scale_lumi']}")
        self.stdout.info("POIs: ".rjust(20) + ", ".join(self.core_config['poi_names']))
        self.stdout.info("")
        self.stdout.info("Categories to be included:")
        input_categories = self.core_config['input_categories']
        for i,input_category in enumerate(input_categories.values()):
            self.stdout.info(f"XML file {i}: ".rjust(20) + f"{input_category}")
        asimov_definitions = self.core_config['asimov_definitions']
        if asimov_definitions:
            self.stdout.info("")
            self.stdout.info("The following asimov dataset(s) will be generated:")
            for asimov_def in asimov_definitions:
                is_gen_asimov = GEN_ASIMOV_ACTION in asimov_def['Action']
                if is_gen_asimov:
                    asimov_name = asimov_def['Name']
                    self.stdout.info(f"\t{asimov_name}")
        self.stdout.info("="*74)

    def print_final_summary(self) -> None:
        ws_name = self.comb_ws.GetName()
        model = ExtendedModel(self.comb_ws, data_name=self.core_config['dataset_name'], verbosity="WARNING")
        pdf = model.pdf
        cat = pdf.indexCat()
        n_cat = len(cat)
        data = model.data
        data_list = data.split(cat, True)
        # start writing summary
        self.stdout.info("="*74)
        title_str = format_delimiter_enclosed_text("Begin summary", "~")
        self.stdout.info(title_str)
        self.stdout.info(f"\tThere are {n_cat} sub channels:")
        for i in range(n_cat):
            cat.setBin(i)
            cat_name = cat.getLabel()
            pdf_i = pdf.getPdf(cat_name)
            data_i = data_list.FindObject(cat_name)
            sum_entries = pretty_value(data_i.sumEntries(), 5)
            self.stdout.info(f"\t\tIndex: {i}, Pdf: {pdf_i.GetName()}, Data: {data_i.GetName()}, SumEntries: {sum_entries}")
        title_str = format_delimiter_enclosed_text("POI", "-")
        self.stdout.info(title_str)
        if Verbosity.INFO >= self.stdout.verbosity:
            model.pois.Print("v")
        title_str = format_delimiter_enclosed_text("Dataset", "-")
        self.stdout.info(title_str)
        if Verbosity.INFO >= self.stdout.verbosity:
            for dataset in model.workspace.allData():
                dataset.Print()
        title_str = format_delimiter_enclosed_text("End Summary", "~")
        self.stdout.info(title_str)
        output_path = self.path_manager.get_file("output")
        self.stdout.info(f"Workspace `{ws_name}` has been successfully generated and saved in file `{output_path}`")
        #output_plot_path = self.get_output_plot_path()
        #self.stdout.info(f"Plots for each category are summarized in `{output_plot_path}`")
        self.stdout.info(f"Total time taken: {self.time_taken:.3f}s")
        self.stdout.info("="*74)
                         
    def generate_asimov(self, ws:Optional["ROOT.RooWorkspace"]=None) -> None:
        if ws is None:
            ws = self.comb_ws
        asimov_definitions = self.core_config['asimov_definitions']
        if self.use_binned:
            data_name = self.core_config['dataset_name'] + "binned"
            self.stdout.warning("REGTEST: Fitting binned dataset.", "red")
        else:
            data_name = self.core_config['dataset_name']
        range_name = self.get_fit_range_name()
        self._generate_asimov(ws, asimov_definitions=asimov_definitions,
                              data_name=data_name, range_name=range_name,
                              minimizer_config=self.minimizer_config)
        
    def get_fit_range_name(self) -> Optional[str]:
        """Get range name used in fitting. Returns None if the analysis is unblinded.
        """
        do_blind = self.core_config['do_blind']
        if do_blind:
            return self.get_sideband_range_name()
        else:
            return None
        
    def get_sideband_range_name(self) -> str:
        """Get sideband range name to be used in fitting.
        """
        range_name_SBLo = RANGE_NAME_SB_LO
        range_name_SBHi = RANGE_NAME_SB_HI
        return f"{range_name_SBLo},{range_name_SBHi}"
    
    def get_blind_range_name(self) -> str:
        """Get blind range name that are excluded from the fit.
        """
        return RANGE_NAME_BLIND
        
    def generate_single_category(self, category:str) -> "ROOT.RooWorkspace":
        """
        Generate workspace for a single category.
        
        Parameters
        ----------
        category: str
            Name of the category.
        """
        ws         = ROOT.RooWorkspace(f"__Cat_{category}")
        ws_factory = ROOT.RooWorkspace(f"factory_{category}")
        resp_func_map  = {}
        # load category xml file
        filepath = self.path_manager.get_file(f"__Cat_{category}", check_exist=True)
        cat_xml = TXMLTree.load_as_dict(filepath)
            
        title_str = format_delimiter_enclosed_text(f"Category {category}", "-")
        self.stdout.info(title_str)
        
        self.active_category = category
        category_type = self._get_node_attrib(cat_xml, 'Type').lower()
    
        # define luminosity
        if self.core_config['scale_lumi'] > 0:
            lumi_default = 1
        else:
            lumi_default = -1
        luminosity = self._get_node_attrib(cat_xml, "Lumi", required=False,
                                           default=lumi_default, dtype="float")
        if luminosity > 0:
            if self.core_config['scale_lumi'] > 0:
                lumi_expr = f"{LUMI_NAME}[{luminosity}]"
            else:
                lumi_expr = f"{LUMI_NAME}[1]"
            self.import_expression(ws_factory, lumi_expr)
        
        self.cat_config[category] = {
            'input_file': filepath,
            'category_type': category_type,
            'luminosity': luminosity,
            'observable': {'name': ""},
            'samples': {},
            'systematics': {},
            'items_highpriority': [],
            'items_lowpriority': [],
            'weighted_data': False,
            'resp_func_map': {}
        }
        core_argsets = CoreArgumentSets(verbosity=self.stdout.verbosity)
        self.cat_config[category]['core_argsets'] = core_argsets

        nodes = cat_xml['children']
        
        # define dataset
        data_node = self.fetch_node(nodes, "Data", xml_filename=filepath, xml_type="channel",
                                    allow_multiple=False, allow_missing=False)
        self.read_data_node(data_node, ws_factory)
        
        # define correlation terms        
        correlate_node = self.fetch_node(nodes, "Correlate", xml_filename=filepath, xml_type="channel",
                                         allow_multiple=False, allow_missing=True)
        self.read_correlate_node(correlate_node)

        remained_nodes = [node for node in nodes if node['tag'] not in ["Data", "Correlate"]]
        self.read_channel_xml_nodes(remained_nodes, ws_factory)
 
        self._fix_item_priority()
        items_highpriority  = self.cat_config[category]['items_highpriority']
        items_lowpriority   = self.cat_config[category]['items_lowpriority']
        
        self.stdout.debug("REGTEST: High priority items:")
        for item in items_highpriority:
            self.stdout.debug(f"\t{item}")
        self.stdout.debug("REGTEST: Low priority items:")
        for item in items_lowpriority:
            self.stdout.debug(f"\t{item}")
        # first implement high priority items: common variables 
        # and functions not involving systematic uncertainties
        self.import_expressions(ws_factory, items_highpriority)
        
        # secondly implement systematics and import them into the workspace
        self.implement_systematics(ws_factory)

        # work on remaining common variables and functions to be implemented
        self.import_expressions(ws_factory, items_lowpriority)
        
        if self.debug_mode:
            ws_factory.Print()
        
        # implement the scale factors on each sample
        self.implement_samples(ws_factory)
        
        if self.debug_mode:
            ws_factory.Print()
        
        # generate the combined signal + background pdf
        self.implement_sum_pdf(ws_factory)
        sum_pdf = ws_factory.pdf(SUM_PDF_NAME)

        self.implement_blind_range(ws_factory)
        
        self.check_nuisance_parameters(sum_pdf, core_argsets.nuis_set)
        
        # keep track of correlated variables
        correlated_terms = self.get_correlated_terms(ws_factory, core_argsets.nuis_set)
        correlated_str = ",".join(correlated_terms)
        
        self.stdout.debug(f"REGTEST: The following variables will not be renamed: {correlated_str}")
        # import pdf to new workspace, rename objects as appropriate
        self.import_object(ws, ws_factory.pdf(SUM_PDF_NAME),
                           ROOT.RooFit.RenameAllNodes(category),
                           ROOT.RooFit.RenameAllVariablesExcept(category, correlated_str))
        
        # import constraint terms
        self.attach_constraints(ws, core_argsets.constr_set)
        
        # define variable sets: observable, POIs, nuisance parameters, global observables
        poi_names = self.get_poi_names()
        core_argsets.poi_set = core_argsets.get_argset_by_names(ws, poi_names)
        core_argsets.define_argsets(ws)
        
        if self.debug_mode:
            ws.Print()
            
        obs = self.get_observable(ws)
        weight_var = ROOT.RooRealVar("wt", "wt", 1)
        dataset, datahist = self.generate_dataset(obs, weight_var)
    
        # prepare binned data
        dataset_binned_name = f"{OBS_DATASET_NAME}binned"
        dataset_binned = dataset.Clone(dataset_binned_name)
        
        # consider that blinded analysis the number of bins will reduce
        do_blind = self.core_config['do_blind']
        if do_blind:
            blind_range = self.cat_config[category]['dataset']['blind_range']
        else:
            blind_range = None
        blind_sf = 1
        if do_blind and blind_range:
            blind_sf = 1 - (blind_range[1] - blind_range[0]) / (obs.getMax() - obs.getMin())
        if (dataset.numEntries() > (obs.numBins() * blind_sf)):
            dataset_binned = ROOT.RooDataSet(dataset_binned_name, dataset_binned_name,
                                             ROOT.RooArgSet(obs, weight_var),
                                             ROOT.RooFit.WeightVar(weight_var))
            RooDataSet.fill_from_TH1(dataset_binned, datahist, blind_range=blind_range,
                                     min_bin_value=self.EPSILON / 1000.)
        num_events = pretty_value(dataset.sumEntries(), 5)
        self.stdout.info(f"REGTEST: Number of data events: {num_events}")
        self.import_object(ws, dataset)
        self.import_object(ws, dataset_binned)
        
        if self.core_config['generate_hist_data']:
            datahist_name = f"{OBS_DATASET_NAME}hist"
            rdatahist = ROOT.RooDataHist(datahist_name, datahist_name, ROOT.RooArgSet(obs), datahist)
            ws.Import(rdatahist)
        
        self.datahists[category]       = datahist
        self.datasets[category]        = dataset
        self.datasets_binned[category] = dataset_binned
        
        return ws
    
    def implement_sum_pdf(self, ws:ROOT.RooWorkspace):
        cat_config = self.get_active_category_config()
        samples = cat_config['samples']
        sum_pdf_components = [f"{sample.norm_name}*{sample.model_name}" for _, sample in samples.items()]
        sum_pdf_str = f"SUM::{SUM_PDF_NAME}({','.join(sum_pdf_components)})"
        self.stdout.debug(f"REGTEST: Sum pdf expr = {sum_pdf_str}")
        self.import_expression(ws, sum_pdf_str)
        
    def implement_samples(self, ws:ROOT.RooWorkspace):
        category = self.active_category
        cat_config = self.get_active_category_config()
        resp_func_map = cat_config['resp_func_map']
        samples = cat_config['samples']
        for _, sample in samples.items():
            self.stdout.debug(f'DEBUG: Implementing sample for the process "{sample.process}"')
            self.import_expressions(ws, sample.shape_factors)
            sample.norm_name = YIELD_PREFIX + sample.process
            norm_factor_components = []
            sample_norm_factors = self.import_expressions(ws, sample.norm_factors)
            norm_factor_components.append(sample_norm_factors)
            # common systematics: only add if exist
            for syst_domain in sample.syst_domains:
                if syst_domain in resp_func_map:
                    norm_factor_components.append(resp_func_map[syst_domain])
                # sample without systematics
                elif sample.process == syst_domain:
                    continue
                else:
                    raise RuntimeError(f"unknown systematic domain {syst_domain} in sample {sample.process}")
            norm_factor_components_str = ",".join(norm_factor_components)
            norm_factor_expr = f"prod::{sample.norm_name}({norm_factor_components_str})"
            self.import_expression(ws, norm_factor_expr)
            proc_yield = ws.function(sample.norm_name).getVal()
            self.stdout.info(f'INFO: Yield for category "{category}" '
                             f'process "{sample.process}": {proc_yield}')
            if self.debug_mode:
                ws.Print()
            self.implement_sample_model(ws, sample)      
    
    def implement_systematics(self, ws:ROOT.RooWorkspace):
        cat_config = self.get_active_category_config()
        systematics = cat_config['systematics']
        for domain, syst_list in systematics.items():
            syst_domain = SystematicsDomain(domain)
            for syst in syst_list:
                is_shape = syst.is_shape_syst()
                if syst_domain.is_shape is None:
                    syst_domain.is_shape = is_shape
                elif syst_domain.is_shape != is_shape:
                    raise RuntimeError(f'found mixture of shape and non-shape systematics in the domain "{domain}"')
                nuis_expr = f"{syst.name}[0, -5, 5]"
                nuis_name = self.import_expression(ws, nuis_expr)
                nuis = ws.var(nuis_name)
                uncert_hi_expr = syst.get_uncert_hi_expr()
                uncert_lo_expr = syst.get_uncert_lo_expr()
                uncert_hi_name = self.import_expression(ws, uncert_hi_expr)
                uncert_lo_name = self.import_expression(ws, uncert_lo_expr)
                uncert_hi = ws.var(uncert_hi_name)
                uncert_lo = ws.var(uncert_lo_name)
                syst_domain.add_item(nuis, syst.nominal, uncert_hi, uncert_lo,
                                     syst.get_interp_code(), syst.constr_term)
            self.build_response_function(ws, syst_domain)
        
    def generate_dataset(self, obs:ROOT.RooRealVar, weight_var:ROOT.RooRealVar):
        category_name = self.active_category
        cat_config = self.get_active_category_config()
        data_config = cat_config['dataset']
        obs_min = obs.getMin()
        obs_max = obs.getMax()
        n_bins = obs.getBins()
        do_blind = self.core_config['do_blind']
        if do_blind:
            blind_range = cat_config['dataset']['blind_range']
        else:
            blind_range = None
        data_scale = data_config['scale_data']
        data_name = OBS_DATASET_NAME
        filename = data_config['filename']
        filepath = self.path_manager.get_relpath(filename)
        filetype = data_config['filetype']
        obs_plus_weight = ROOT.RooArgSet(obs, weight_var)
        
        dataset = ROOT.RooDataSet(data_name, data_name, obs_plus_weight,
                                  ROOT.RooFit.WeightVar(weight_var))
        datahist = ROOT.TH1D(category_name, category_name, n_bins, obs_min, obs_max)
        datahist.Sumw2()
        
        is_counting = cat_config['category_type'] == DATA_SOURCE_COUNTING
        num_data = data_config['num_data']
        
        # counting experiment
        if (is_counting and num_data >= 0):
            bin_center = (obs_min + obs_max) / 2.
            if num_data == 0:
                weight = self.EPSILON / 1000.
            else:
                weight = num_data * data_scale
            obs.setVal(bin_center)
            weight_var.setVal(weight)
            dataset.add(ROOT.RooArgSet(obs, weight_var), weight)
            datahist.Fill(bin_center, weight)
        #  histogram
        elif (filetype == DATA_SOURCE_HISTOGRAM):
            histname = data_config['histname']
            h = self.get_histogram(filename, histname)
            neg_bin_indices, _ = TH1.remove_negative_bins(h)
            for i in neg_bin_indices:
                self.stdout.warning(f"REGTEST: Input data histogram bin {i} in "
                                    f"category {category_name} has negative weight. "
                                    f"Will force it to zero.", "red")
            if blind_range:
                TH1.apply_blind_range(h, blind_range)
            RooDataSet.fill_from_TH1(dataset, h,
                                     blind_range=blind_range,
                                     min_bin_value=self.EPSILON / 1000.,
                                     weight_scale=data_scale)
            rebin_ratio = TH1.rebin_to_variable(h, obs, tol=self.EPSILON)
            if rebin_ratio != 1:
                self.stdout.warning(f"REGTEST: Rebinning input data histogram "
                                    f"`{histname}` in category {category_name} by "
                                    f"{rebin_ratio} to match the binning of the observable")
            TH1.copy_histogram_in_effective_range(h, datahist, tol=self.EPSILON,
                                                  weight_scale=data_scale)
        else:
            if filetype == DATA_SOURCE_ASCII:
                filepath = self.path_manager.get_relpath(filename)
                dataset_tmp = self.get_dataset_from_ascii_file(filepath, obs, weight_var)
            else:
                cut      = data_config['cut']
                treename = data_config['treename']
                varname  = data_config['varname']
                chain, _ = self.get_chain_and_branch(filepath, treename, varname, cut)
                x_tree = ROOT.RooRealVar(varname, varname, obs.getMin(), obs.getMax())
                _dataset_name = f"{OBS_DATASET_NAME}_tmp"
                dataset_tmp = ROOT.RooDataSet(_dataset_name, _dataset_name,
                                              ROOT.RooArgSet(x_tree),
                                              ROOT.RooFit.Import(chain))
            xdata_tmp = dataset_tmp.get().first()          
            for i in range(dataset_tmp.numEntries()):
                dataset_tmp.get(i)
                x_val = xdata_tmp.getVal()
                obs.setVal(x_val)
                weight = dataset_tmp.weight() * data_scale
                weight_var.setVal(weight)
                # ignore data in the blind range
                if (blind_range) and (x_val > blind_range[0]) and (x_val < blind_range[1]):
                    continue
                dataset.add(ROOT.RooArgSet(obs, weight_var), weight)
                datahist.Fill(x_val, weight)
        n_event = dataset.sumEntries()
        n_event_binned = datahist.Integral()
        if abs(n_event - n_event_binned) > self.EPSILON:
            raise RuntimeError(f"Binned ({n_event_binned}) and unbinned ({n_event}) "
                               f"datasets have different number of entries in "
                               f"category {category_name}")
        if self.debug_mode:
            dataset.Print("v")
        # inject ghost
        if data_config['inject_ghost']:
            RooDataSet.add_ghost_weights(dataset, blind_range=blind_range, ghost_weight=self.EPSILON / 1000.)
            TH1.add_ghost_weights(datahist, blind_range=blind_range, ghost_weight=self.EPSILON / 1000.)
        return dataset, datahist
    
    def get_dataset_from_ascii_file(self, file:str, obs:ROOT.RooRealVar, weight_var:ROOT.RooRealVar):
        cat_config = self.get_active_category_config()
        weighted_data = cat_config['weighted_data']
        if weighted_data:
            dataset_name = f"{OBS_DATASET_NAME}_tmp"
            dataset = ROOT.RooDataSet(dataset_name, dataset_name,
                                      ROOT.RooArgSet(obs, weight_var),
                                      ROOT.RooFit.WeightVar(weight_var))
            try:
                data = np.loadtxt(file)
            except:
                raise RuntimeError('invalid ascii file format')
            assert (data.ndim == 2) and (data.shape[1] == 2)
            for data_i in data:
                obs.setVal(data_i[0])
                weight.setVal(data_i[1])
                dataset.add(ROOT.RooArgSet(obs, weight), weight)
        else:
            dataset = ROOT.RooDataSet.read(file, ROOT.RooArgList(obs))
        return dataset    
        
    def release_ghost(self, dataset:ROOT.RooDataSet, datahist:ROOT.RooDataHist,
                      obs:ROOT.RooRealVar, weight_var:ROOT.RooRealVar, ghost_weight:float):
        do_blind = self.core_config['do_blind']
        cat_config = self.get_active_category_config()
        blind_range = cat_config['dataset']['blind_range']
        n_bins = datahist.GetNbinsX()
        for i in range(1, n_bins + 1):
            if datahist.GetBinContent(i) == 0:
                bin_center = datahist.GetBinCenter(i)
                if (do_blind and blind_range) and \
                   (bin_center > blind_range[0]) and (bin_center < blind_range[1]):
                    continue
                obs.setVal(bin_center)
                weight_var.setVal(ghost_weight)
                dataset.add(ROOT.RooArgSet(obs, weight_var), ghost_weight)
                # also put the ghost weight in the histograms
                datahist.SetBinContent(i, ghost_weight)
                
    def attach_constraints(self, ws:ROOT.RooWorkspace, constraints:ROOT.RooArgSet):
        category_name = self.active_category
        self.stdout.debug(f"REGTEST: Attaching contraint pdfs to workspace for the category {category_name}")
        sum_pdf_name = f"{SUM_PDF_NAME}_{category_name}"
        final_pdf_name = f"{FINAL_PDF_NAME}_{category_name}"
        remove_set = ROOT.RooArgSet()
        pdf = ws.pdf(sum_pdf_name)
        if not pdf:
            raise RuntimeError(f"sum pdf `{sum_pdf_name}` not defined")
        for constraint in constraints:
            constr_name = constraint.GetName()
            np_name = constr_name.replace(CONSTRTERM_PREFIX, "")
            if not pdf.getVariables().find(np_name):
                self.stdout.warning(f"WARNING: constraint term {constr_name} with NP "
                                    f"{np_name} is redundant in the category {category_name}. "
                                    f"It will be removed...", "red")
                remove_set.add(constraint)
            else:
                self.import_object(ws, constraint)
        for constraint in remove_set:
            constraints.remove(constraint)
        pdf_components = [sum_pdf_name] + [constraint.GetName() for constraint in constraints]
        pdf_str = ",".join(pdf_components)
        model_expr = f"PROD::{final_pdf_name}({pdf_str})"
        self.import_expression(ws, model_expr)
        
    def get_correlated_terms(self, ws:ROOT.RooWorkspace, nuis:ROOT.RooArgSet) -> List[str]:
        correlated_terms = []
        cat_config = self.get_active_category_config()
        # correlate custom variables
        correlated_terms.extend(cat_config['correlate_items'])
        # correlate POIs
        poi_names = self.get_poi_names()
        correlated_terms.extend(poi_names)
        # correlate nuisance parameters
        nuis_names = [np.GetName() for np in nuis]
        correlated_terms.extend(nuis_names)
        # correlate observable
        observable_name = cat_config['observable']['name']
        correlated_terms.append(observable_name)
        # remove duplicate terms
        correlated_terms = remove_list_duplicates(correlated_terms)
        # check validity of variables
        valid_correlated_terms = []
        for item in correlated_terms:
            # does not exist
            if (not ws.obj(item)):
                continue
            if (not ws.var(item)):
                raise RuntimeError(f"correlated variable `{item}` is not properly implemented"
                                   f" as RooRealVar in the workspace")
            valid_correlated_terms.append(item)
        return valid_correlated_terms
    
    def get_poi_names(self):
        return self.core_config['poi_names']
    
    def get_observable(self, ws:ROOT.RooWorkspace):
        cat_config = self.get_active_category_config()
        observable_name = cat_config['observable']['name']
        obs = ws.var(observable_name)
        if not obs:
            category = self.active_category
            raise RuntimeError(f"observable for the category `{category}` not defined in the workspace")
        return obs

    def implement_blind_range(self, ws:ROOT.RooWorkspace):
        # range_name = "" : fully blinded
        # range_name = None: no blinding
        # otherwise partially blinded
        cat_config = self.get_active_category_config()
        category = self.active_category
        obs = self.get_observable(ws)
        obs_range = [obs.getMin(), obs.getMax()]
        # now handle blinding if needed
        do_blind = self.core_config["do_blind"]
        if do_blind:
            blind_range = cat_config['dataset']['blind_range']
            if blind_range:
                self.stdout.info(f"REGTEST: Implement blind range [{blind_range[0]}, {blind_range[1]}]")
                sideband_lo_range_name = f"{RANGE_NAME_SB_LO}_{category}"
                sideband_hi_range_name = f"{RANGE_NAME_SB_HI}_{category}"
                blind_range_name = f"{RANGE_NAME_BLIND}_{category}"
                obs.setRange(sideband_lo_range_name, obs_range[0], blind_range[0])
                obs.setRange(blind_range_name, blind_range[0], blind_range[1])
                obs.setRange(sideband_hi_range_name, blind_range[1], obs_range[1])
                if (blind_range[0] == obs_range[0]) and \
                   (blind_range[1] == obs_range[1]):
                    self.stdout.info(f"REGTEST: Category `{category}` is fully blinded. "
                                     f"No side-band exists.")
                    cat_config['range_name'] = ""
                elif (blind_range[1] == obs_range[1]):
                    cat_config['range_name'] = sideband_lo_range_name
                elif (blind_range[0] == obs_range[0]):
                    cat_config['range_name'] = sideband_hi_range_name
                else:
                    cat_config['range_name'] = f"{sideband_lo_range_name},{sideband_hi_range_name}"
            # do blind but no range specified : fully blinded
            else:
                cat_config['range_name'] = ""
        else:
            cat_config['range_name'] = None
        
    @staticmethod
    def _generate_expr(head:str, argset:ROOT.RooArgSet, close_expr:bool=True):
        tokens = [i.GetName() for i in argset]
        expr_str = head + ",".join(tokens)
        if close_expr:
            expr_str += ")"
            expr_str = expr_str.strip().replace(",)", ")")
        return expr_str
    
    def _fix_item_priority(self):
        cat_config = self.get_active_category_config()
        items_highpriority  = cat_config['items_highpriority']
        items_lowpriority   = cat_config['items_lowpriority']
        _items_highpriority = []
        for item in items_highpriority:
            if self._item_has_dependent(item, items_lowpriority):
                items_lowpriority.append(item)
            else:
                _items_highpriority.append(item)
        cat_config['items_highpriority'] = _items_highpriority
    
    def _item_has_dependent(self, expr:str, reference_list:List[str]):
        _, item_type = self._get_object_name_and_type_from_expr(expr)
        self.stdout.debug(f"REGTEST: item `{expr}` has type `{item_type}`")
        if item_type in ['variable', 'defined']:
            return False
        item_list = self._decompose_function_expr(expr)
        self.stdout.debug(f"REGTEST: Composition of high priority item {expr}: "
                          f"{', '.join(item_list)}")
        for this_name in item_list:
            for reference in reference_list:
                that_name, _ = self._get_object_name_and_type_from_expr(reference)
                if this_name == that_name:
                    return True
        return False

    @staticmethod
    def _decompose_function_expr(expr:str):
        start = expr.find("(")
        end = expr.rfind(")")
        if (start < 0) or (end < 0):
            raise RuntimeError(f"not a valid function expression `{expr}`")
        tokens = expr[start + 1 : end].split(",")
        if ("expr::" in expr) or ("EXPR::" in expr):
            tokens = tokens[1:]
        return tokens
        
    @staticmethod
    def _get_object_name_and_type_from_expr(expr:str):
        if ("::" in expr) and ("(" in expr):
            object_type = "function"
            object_name = expr.split("::")[1].split("(")[0]
        elif ("[" in expr):
            object_type = "variable"
            object_name = expr.split("[")[0]
        elif (":" in expr) and not ("::" in expr):
            raise RuntimeError(f"syntax error for the expression `{expr}`: missing colon pair")
        else:
            object_type = "defined"
            object_name = expr
        return object_name, object_type
            
    def import_uncert_expr(self, ws:ROOT.RooWorkspace, expr:str, var_name:str, prefix:str):
        if is_float(expr):
            new_expr = f"{prefix}{var_name}[{expr}]"
            return self.import_expression(ws, new_expr)
        else:
            return self.import_expression(ws, expr)

    def _translate_keyword(self, expr:str):
        category_name = self.active_category
        observable_name = self.cat_config[category_name]['observable']['name']
        expr = expr.replace(RESPONSE_KEYWORD, 
                            RESPONSE_PREFIX + \
                            SHAPE_SYST_KEYWORD + "_")
        expr = expr.replace(OBSERVABLE_KEYWORD,
                            observable_name)
        expr = expr.replace(CATEGORY_KEYWORD,
                            category_name)
        expr = expr.replace(COMMON_SYST_DOMAIN_KEYWORD,
                            Systematic.common_domain())
        expr = expr.replace(LT_OP, "<")
        expr = expr.replace(LE_OP, "<=")
        expr = expr.replace(GT_OP, ">")
        expr = expr.replace(GE_OP, ">=")
        expr = expr.replace(AND_OP, "%%")
        expr = expr.replace(OR_OP, "||")
        return expr
       
    def _translate_node_attrib(self, node:Dict, attrib_name:str, process:str="",
                               required:bool=True, default:str=""):
        expr = self._get_node_attrib(node, attrib_name, required, default)
        expr = self._translate_keyword(expr)
        if (PROCESS_KEYWORD in expr):
            if process == "":
                raise RuntimeError(f"process name not provided for the expression `{expr}`")
            expr = expr.replace(PROCESS_KEYWORD, f"_{process}")
        return expr
    
    def get_chain_and_branch(self, filename:str, treename:str, varname:str,
                             cut:str="", check_only:bool=False):
        chain = ROOT.TChain(treename)
        filenames = filename.split(",")
        filepaths = [self.path_manager.get_relpath(filename) for filename in filenames]
        for filepath in filepaths:
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"input data file `{filepath}` not found")
            status = chain.AddFile(filepath, -1)
            if not status:
                raise RuntimeErrro(f"cannot find TTree `{treename}` in data file `{filepath}`")
        if cut != "":
            chain = chain.CopyTree(cut)
        branch = chain.FindBranch(varname)
        if not branch:
            raise RuntimeError(f"cannot find TBranch `{varname}` in TTree `{treename}` "
                               f"in data file `{filename}`")
        if check_only:
            return Nones
        return chain, branch
    
    def get_histogram(self, filename:str, histname:str, check_only:bool=False):
        filepath = self.path_manager.get_relpath(filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"input data file `{filepath}` not found")
        f = ROOT.TFile(filepath)
        category_name = self.active_category
        data_config = self.cat_config[category_name]['dataset']
        histname = data_config['histname']
        histogram = f.Get(histname)
        if not isinstance(histogram, ROOT.TH1):
            raise RuntimeError(f"no TH1 named `{histanme}` found in data file `{filepath}`")
        if check_only:
            return None
        histogram.SetDirectory(0)        
        return histogram
    
    def data_file_sanity_check(self):
        category_name = self.active_category
        category_type = self.cat_config[category_name]['category_type']
        data_config = self.cat_config[category_name]['dataset']
        filename = data_config['filename']    
        if category_type == DATA_SOURCE_COUNTING:
            if (filename != "") and (self.check_file_exist(filename)):
                raise FileNotFoundError(f"input data file `{filepath}` not found")
            if (filename == "") and (data_config.get("num_data", -1) < 0):
                raise RuntimeError("pleasee provide either a valid input data filename, or "
                                   "a valid number of data events for a counting experiment")
        else:
            if data_config['filetype'] != DATA_SOURCE_ASCII:
                if data_config['filetype'] == DATA_SOURCE_HISTOGRAM:
                    histname = data_config['histname']
                    self.get_histogram(filename, histname, check_only=True)
                else:
                    treename = data_config['treename']
                    varname = data_config['varname']
                    self.get_chain_and_branch(filename, treename, varname, check_only=True)
    
    def fetch_node(self, nodes:List, tag:str, xml_filename:str, xml_type:str="channel", 
                   allow_missing:bool=False, allow_multiple:bool=False):
        target_node = [node for node in nodes if node['tag'] == tag]
        if (len(target_node) > 1) and (not allow_multiple):
            raise RuntimError(f"Multiple `{tag}` node found in {xml_type} XML file `{xml_filename}`")
        elif (len(target_node) == 0) and (not allow_missing):
            raise RuntimError(f"No `{tag}` node found in {xml_type} XML file `{xml_filename}`")
        elif (len(target_node) == 1) and (not allow_multiple):
            target_node = target_node[0]
        return target_node
    
    def get_active_category_config(self):
        category_name = self.active_category
        if category_name not in self.cat_config:
            raise RuntimeError(f"no config info found for the category `{category_name}`")
        cat_config = self.cat_config[category_name]
        return cat_config
        
    def read_systematics_node(self, node:Dict, domain:str):
        # Read XML config file. Domain name is also passed in some cases, and will replace the :process: keyword in case it is there
        cat_config = self.get_active_category_config()
        syst_expr = self._get_node_attrib(node, "Name")
        self.stdout.debug(f"REGTEST: Reading systematic `{syst_expr}`")
        syst = Systematic()
        syst.name = self._translate_node_attrib(node, "Name", domain)
        # if the process of the systematic is specified, use the 
        # specified process. Otherwise it is set to empty
        syst.process = self._translate_node_attrib(node, "Process", domain, False, "")
        syst.whereto = self._get_node_attrib(node, "WhereTo")
        syst.nominal = self._get_node_attrib(node, "CentralValue", dtype="float")
        syst.constr_term = self._get_node_attrib(node, "Constr")
        syst.set_domain(domain)
        syst.validate()
        magitude_expr = self._get_node_attrib(node, "Mag", dtype="str_list")
        syst.set_magnitudes(magitude_expr)
        self.add_syst_object(syst)

    def add_syst_object(self, syst:Systematic):
        cat_config = self.get_active_category_config()
        systematics = cat_config['systematics']
        if syst.domain not in systematics:
            systematics[syst.domain] = []
        syst_list = systematics[syst.domain]
        if any(syst_i == syst for syst_i in syst_list):
            raise RuntimeError(f"systematic `{syst.name}` applied on `{syst.whereto}` "
                               f"is duplicated for the process `{syst.process}`")
        syst_list.append(syst)
        
    def add_sample_object(self, sample:Sample):
        cat_config = self.get_active_category_config()
        sample_map = cat_config['samples']
        process = sample.process
        if process in sample_map:
            category = self.active_category
            raise RuntimeError(f"duplicated sample `{sample.process}` in the category `{category}`")
        sample_map[process] = sample
        
    def read_item_node(self, node:Dict):
        cat_config = self.get_active_category_config()
        item = self._translate_node_attrib(node, "Name")
        if (RESPONSE_KEYWORD in item) or \
           (RESPONSE_PREFIX in item):
            cat_config['items_lowpriority'].append(item)
        else:
            cat_config['items_highpriority'].append(item)
        
    def read_channel_import_node(self, node:Dict, ws:ROOT.RooWorkspace):
        filename = self._translate_node_attrib(node, "FileName")
        filepath = self.path_manager.get_relpath(filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"import XML file `{filepath}` not found")
        self.stdout.debug(f"REGTEST: Reading import XML file `{filepath}`")
        xml_data = TXMLTree.load_as_dict(filepath)
        nodes = xml_data['children']
        self.read_channel_xml_nodes(nodes, ws)
        
    def read_sample_import_node(self, node:Dict, sample:Sample):
        filename = self._translate_node_attrib(node, "FileName")
        filepath = self.path_manager.get_relpath(filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"import XML file `{filepath}` not found")
        self.stdout.info(f"REGTEST: Importing items for `{sample.process}` from {filepath}")
        xml_data = TXMLTree.load_as_dict(filepath)
        nodes = xml_data['children']
        self.read_sample_subnode(nodes, sample)
    
    def read_sample_factor_node(self, node:Dict, sample:Sample):
        """Parse Norm/Shape factors from a Sample Node
        
        Example implementation:
        <Sample Name="ggF" InputFile="models/ggF.xml" ImportSyst=":common:">
          <NormFactor Name="yield_ggF[0.0078]" Correlate=0 />
        </Sample>
        """
        factor_type = SampleFactorType.parse(node["tag"])
        factor = self._translate_node_attrib(node, "Name", sample.process)
        if factor_type == SampleFactorType.NormFactor:
            sample.norm_factors.append(factor)
        elif factor_type == SampleFactorType.ShapeFactor:
            sample.shape_factors.append(factor)
        is_correlated = self._get_node_attrib(node, "Correlate", required=False, default=0, dtype="int")
        if is_correlated:
            cat_config = self.get_active_category_config()
            item_name, item_type = self._get_object_name_and_type_from_expr(factor)
            cat_config['correlate_items'].append(item_name)
    
    def read_data_node(self, node:Dict, ws:ROOT.RooWorkspace):
        cat_config = self.get_active_category_config()
        # extract observable information
        observable_expr = self._translate_node_attrib(node, "Observable")
        observable_name = self.import_expression(ws, observable_expr)
        observable = ws.var(observable_name)
        observable_min = observable.getMin()
        observable_max = observable.getMax()
        if observable_min >= observable_max:
            raise RuntimeError(f"invalid range for observable `{observable_name}`: "
                               f"min={observable_min}, max={observable_max}")
        is_counting = cat_config['category_type'] == DATA_SOURCE_COUNTING
        if is_counting:
            observable_nbins = 1
        else:
            observable_nbins = int(self._get_node_attrib(node, "Binning"))
        ws.var(observable_name).setBins(observable_nbins)
        
        cat_config['observable'] = {
            'name': observable_name,
            'min': observable_min,
            'max': observable_max,
            'nbins': observable_nbins
        }
        
        core_argsets = cat_config['core_argsets']
        core_argsets.obs_set = ROOT.RooArgSet(observable)
        
        data_filename = self._translate_node_attrib(node, "InputFile", "",
                                                    required=not is_counting,
                                                    default="")
        data_filetype = self._get_node_attrib(node, "FileType", required=False,
                                              default=DATA_SOURCE_ASCII).lower()
        data_config = {}
        data_config['filename'] = data_filename
        data_config['filetype'] = data_filetype
        # reading from text file (event-by-event)
        if data_filetype == DATA_SOURCE_ASCII:
            cat_config['weighted_data'] = self._get_node_attrib(node, "HasWeight", required=False,
                                                                default=False, dtype="bool")
        # reading from root histogram
        elif data_filetype == DATA_SOURCE_HISTOGRAM:
            data_config['histname'] = self._translate_node_attrib(node, ["HistName", "HistoName"])
        # reading from root ntuples
        else:
            data_config['treename'] = self._translate_node_attrib(node, "TreeName")
            data_config['varname'] = self._translate_node_attrib(node, "VarName")
            data_config['cut'] = self._translate_node_attrib(node, "Cut", "",
                                                             required=False, default="")

        inject_ghost = self._get_node_attrib(node, "InjectGhost", required=False, default=0, dtype="int")
        data_config['inject_ghost'] = inject_ghost
        if (is_counting and data_filename == ""):
            data_config['num_data'] = self._get_node_attrib(node, "NumData", dtype="int")
        else:
            data_config['num_data'] = -1
        data_config['scale_data'] = self._get_node_attrib(node, "ScaleData",
                                                          required=False, default=1, dtype="float")
        if self.core_config['scale_lumi'] > 0:
            data_config['scale_data'] *= self.core_config['scale_lumi']
        blind_range = self._get_node_attrib(node, "BlindRange", required=False, default=None)
        if blind_range:
            blind_range = blind_range.split(",")
            if (len(blind_range) != 2) or (not is_float(blind_range[0])) or (not is_float(blind_range[1])):
                raise RuntimeError(f"invalid blind range format: {blind_range}")
            blind_range = [float(r) for r in blind_range]
            if (blind_range[1] <= blind_range[0]) or (blind_range[0] < observable_min) or (blind_range[1] > observable_max):
                raise RuntimeError(f"invalid blind range given: min={blind_range[0]}, max={blind_range[1]}")
        data_config['blind_range'] = blind_range
        cat_config['dataset'] = data_config
        
        self.data_file_sanity_check()
        
    def read_correlate_node(self, node:Optional[Dict]=None):
        cat_config = self.get_active_category_config()
        if node:
            item_str = node['text']
            if not item_str:
                filename = cat_config['input_file']
                raise RuntimeError(f"no items defined for correlation in channel XML file `{filename}`")
            correlate_items = item_str.split(",")
        else:
            correlate_items = []
        cat_config['correlate_items'] = correlate_items
        
    def read_sample_node(self, node:Dict):
        cat_config = self.get_active_category_config()
        is_counting = cat_config['category_type'] == DATA_SOURCE_COUNTING
        sample = Sample()
        sample.process = self._translate_node_attrib(node, "Name")
        sample.input_file = self._translate_node_attrib(node, "InputFile", sample.process,
                                                        required=not is_counting, default="")
        syst_domains = self._translate_node_attrib(node, "ImportSyst", sample.process,
                                                   required=False, default=SELF_SYST_DOMAIN_KEYWORD)
        syst_domains = re.sub('\s+', '', syst_domains).split(",")
        sample.set_syst_domains(syst_domains)
        
        # assemble the yield central value
        
        if cat_config['luminosity'] > 0:
            multiply_lumi = self._get_node_attrib(node, "MultiplyLumi",
                                                  required=False, default=1, dtype="int")
            if multiply_lumi:
                sample.norm_factors.append(LUMI_NAME)

        norm_factor_names = {
            'norm': ('Norm', NORM_PREFIX),
            'xs': ('XSection', XS_PREFIX),
            'br': ('BR', BR_PREFIX),
            'efficiency': ('SelectionEff', EFFICIENCY_PREFIX),
            'acceptance': ('Acceptance', ACCEPTANCE_PREFIX),
            'correction': ('Correction', CORRECTION_PREFIX)
        }
        
        # sample level normalization factors
        for key, (name, prefix) in norm_factor_names.items():
            norm_value = self._translate_node_attrib(node, name, sample.process,
                                                     required=False, default="")
            if norm_value != "":
                sample.norm_factors.append(f"{prefix}_{sample.process}[{norm_value}]")
                
        sample.share_pdf_group = self._translate_node_attrib(node, "SharePdf", sample.process,
                                                             required=False, default="")
        subnodes = node['children']
        self.stdout.debug(f"REGTEST: Reading sample `{sample.process}`")
        self.read_sample_subnode(subnodes, sample)    
        self.add_sample_object(sample)
        
    def read_sample_subnode(self, nodes:List, sample:Sample):
        for node in nodes:
            name = node['tag']
            if name == "Systematic":
                self.read_systematics_node(node, sample.process)
            elif SampleFactorType.has_member(name):
                self.read_sample_factor_node(node, sample)
            elif name == "ImportItems":
                self.read_sample_import_node(node, sample)
            else:
                raise RuntimeError(f"unsupported node `{name}`")        
    
    def read_channel_xml_nodes(self, nodes:List, ws:ROOT.RooWorkspace):
        for node in nodes:
            name = node['tag']
            if name == "Item":
                self.read_item_node(node)
            elif name == "Systematic":
                self.read_systematics_node(node, domain=Systematic.default_domain())
            elif name == "Sample":
                self.read_sample_node(node)
            elif name == "ImportItems":
                self.read_channel_import_node(node, ws)
            else:
                raise RuntimeError(f"unsupported node `{name}`")
                
    def build_response_function(self, ws:ROOT.RooWorkspace, syst_domain:SystematicsDomain):
        cat_config = self.get_active_category_config()
        core_argsets = cat_config['core_argsets']
        resp_func_map = cat_config['resp_func_map']
        resp_func = syst_domain.get_response_function()
        ws.Import(resp_func, ROOT.RooFit.RecycleConflictNodes())
        if (not syst_domain.is_shape):
            resp_func_map[syst_domain.domain] = syst_domain.get_response_name()
        for i in range(syst_domain.nuis_list.size()):
            np_name, glob_name, constr_name = syst_domain.get_np_glob_constr_names(i)
            if syst_domain.constr_term_list[i] == CONSTR_DFD:
                self.stdout.debug(f"REGTEST: Creating DFD constraint term for NP {np_name}")
                constr_expr = (f"EXPR::{constr_name}('1/((1+exp(@2*(@0-@3-@1)))*(1+exp(-1*@2*(@0-@3+@1))))', "
                               f"{np_name}, DFD_e[1], DFD_w[500], {glob_name}[0,-5,5])")
                self.import_expression(ws, constr_expr, True)
            else:
                self.stdout.debug(f"REGTEST: Creating RooGaussian constraint term for NP {np_name}")
                constr_expr = f"RooGaussian::{constr_name}({np_name},{glob_name}[0,-5,5],1)"
            self.import_expression(ws, constr_expr, True)
            core_argsets.nuis_set.add(ws.var(np_name), True)
            core_argsets.glob_set.add(ws.var(glob_name), True)
            core_argsets.constr_set.add(ws.pdf(constr_name), True)
            self.stdout.debug(f"REGTEST: Finished implementing the systematic {np_name}")
            
    def implement_sample_model(self, ws:ROOT.RooWorkspace, sample:Sample):
        self.stdout.debug("REGTEST: Getting model")
        sample.update_model_name()
        if ws.pdf(sample.model_name):
            if is_shared_pdf:
                # use shared pdf
                self.stdout.debug(f"REGTEST: PDF {sample.model_name} has been created in the workpace.")
                return None
            else:
                raise RuntimeError(f"PDF {sample.model_name} already exists but the user asks to create it again")
        self.stdout.debug(sample.model_name)
        cat_config = self.get_active_category_config()
        is_counting = cat_config['category_type'] == DATA_SOURCE_COUNTING
        if is_counting:
            # in counting experiment we only need a uniform pdf
            obs_name = cat_config['observable']['name']
            self.import_expression(ws, f"RooUniform::{sample.model_name}({obs_name})")
        else:
            filename = sample.input_file            
            self.read_model_xml(filename, ws, sample)
            
    def read_model_xml(self, filename:str, ws:ROOT.RooWorkspace, sample:Sample):
        cat_config = self.get_active_category_config()
        filepath = self.path_manager.get_relpath(filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f'model xml file "{filepath}" does not exist')
        root_node = TXMLTree.load_as_dict(filepath)
        
        model_type = self._get_node_attrib(root_node, "Type").lower()
        if model_type == USERDEF_MODEL:
            self.stdout.debug(f'REGTEST: Creating user-defined pdf from "{filepath}"')
            self.build_userdef_model(root_node, ws, sample)
        elif model_type == EXTERNAL_MODEL:
            self.build_external_model(root_node, ws, sample)
        elif model_type == HISTOGRAM_MODEL:
            self.build_histogram_model(root_node, ws, sample)
        else:
            raise RuntimeError(f"unknown model type: {model_type} . Available choice: "
                               f" {USERDEF_MODEL}, {EXTERNAL_MODEL}, "
                               f" {HISTOGRAM_MODEL}")
    
    def build_userdef_model(self, root_node:Dict, ws:ROOT.RooWorkspace, sample:Sample):
        cat_config = self.get_active_category_config()
        tag_name = sample.get_tag_name()
        obs_name = cat_config['observable']['name']
        cache_binning = self._get_node_attrib(root_node, "CacheBinning", False, "-1", dtype="int")
        obs = ws.var(obs_name)
        if cache_binning > 0:
            if not obs:
                raise RuntimeError("observable not initialized")
            # for the accuracy of Fourier transformation
            obs.setBins(cache_binning, "cache")
        is_success = False
        nodes = root_node['children']
        for node in nodes:
            name = node['tag']
            self.stdout.debug(f"REGTEST: Reading node `{name}`")
            if name == "Item":
                expr = self._translate_node_attrib(node, "Name", tag_name)
                self.import_expression(ws, expr)
            elif name == "ModelItem":
                factory_str = self._translate_node_attrib(node, "Name", tag_name)
                str_start = factory_str.find("::")+2
                str_end   = factory_str.find("(")
                pdf_name = factory_str[str_start:str_end]
                factory_str = factory_str[:str_start] + sample.model_name + factory_str[str_end:]
                self.import_expression(ws, factory_str)
                is_success = True
                break
            else:
                raise RuntimeError(f'unknown node "{name}"')
        if not is_success:
            raise RuntimeError('missing node "ModelItem" from model xml')
    
    def build_external_model(self, root_node:Dict, ws:ROOT.RooWorkspace, sample:Sample,
                             nuis:ROOT.RooArgSet, constraints:ROOT.RooArgSet, globobs:ROOT.RooArgSet):
        cat_config = self.get_active_category_config()
        _observable_name = cat_config['observable']['name']
        filename = self._translate_node_attrib(root_node, "Input")
        filepath = self.path_manager.get_relpath(filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f'input file "{filepath}" not found')
        ws_name = self._translate_node_attrib(root_node, "WSName")
        model_name = self._translate_node_attrib(root_node, "ModelName")
        observable_name = self._translate_node_attrib(root_node, "ObservableName")
        tag_name = sample.get_tag_name()
        nodes = root_node['children']
        np_list, glob_list, constr_list = [], [], []
        self.stdout.debug(f"REGTEST: Use existing PDF `{model_name}` from the workspace `{filename}`")
        
        f_ext = ROOT.TFile(filename)
        ws_ext = f_ext.Get(ws_name)
        pdf_ext = ws_ext.function(model_name)
        
        name_maps = {}
        do_not_touch = [observable_name]
        
        for node in nodes:
            name = node['tag']
            if name == "Item":
                expr = self._translate_node_attrib(node, "Name", tag_name)
                self.import_object(ws, expr)
            elif name == "Fix":
                var_name = self._translate_node_attrib(node, "Name")
                var = ws_ext.var(var_name)
                if not var:
                    raise RuntimeError(f"no variable named `{var_name}` found im the workspace `{filepath}`")
                var.setConstant(1)
                var_val = self._get_node_attrib(node, "Value", False, "")
                if var_val != "":
                    var.setVal(float(var))
                self.stdout.debug(f"REGTEST: Fixed variable `{var_name}` at `{var.getVal()}")
            elif name == "Rename":
                # rename the object names in the input workspace
                old_name = self._translate_node_attrib(node, "OldName", tag_name)
                new_name = self._translate_node_attrib(node, "NewName", tag_name)
                do_not_touch.append(old_name)
                name_maps[old_name] = new_name
            elif name == "ExtSyst":
                # adding external systematics
                np_name = self._translate_node_attrib(node, "NPName")
                glob_name = self._translate_node_attrib(node, "GOName", "", False, "")
                constr_name = self._translate_node_attrib(node, "ConstrName", "",
                                                          required=glob_name!="", default="")
                np_list.append(np_name)
                glob_list.append(glob_name)
                constr_list.append(constr_name)
                do_not_touch.append(np_name)
            else:
                raise RuntimeError(f"unknown node `{name}`")
        # remove duplicated variables
        do_not_touch = ",".join(remove_list_duplicates(do_not_touch))
    
        # rename everything in the model by adding a tag to it
        ws_temp = ROOT.RooWorkspace("ws_temp")
        self.import_object(ws, pdf_ext, ROOT.RooFit.RenameAllNodes(tag_name),
                           ROOT.RooFit.RenameAllVariablesExcept(tag_name, do_not_touch))
        #ws_temp.importClassCode()
        if self.debug_mode:
            ws_temp.Print()
            
        pdf = ws_temp.function(f"{model_name}_{tag_name}")
        obs_ext = ws_temp.var(observable_name)
        if not obs_ext:
            raise RuntimeError(f"observable `{observable_name}` not found in the workspace `{filepath}`")
        if not isinstance(pdf, ROOT.RooAbsPdf):
            self.stdout.warning(f"WARNING: The object {model_name} is not a p.d.f as seen from RoOFit")
            self.stdout.warning("REGTEST: Constructing RooRealSumPdf for the pdf from histFactory")
            dummy_pdf = ROOT.RooUniform(f"{sample.model_name}_dummpy_pdf", "for RooRealSumPdf construction",
                                        obs_ext)
            frac = ROOT.RooRealVar(f"{sample.model_name}_real_pdf_frac", "for RooRealSumPdf construction", 1)
            pdf = ROOT.RooRealSumPdf(sample.model_name, "from histFactory", ROOT.RooArgList(pdf, dummy_pdf),
                                     ROOT.RooArgList(frac))
        else:
            name_maps[pdf.GetName()] = sample.model_name
        
        # rename observable (this step should never happen for a HistFactory workspace)
        if observable_name != _observable_name:
            name_maps[observable_name] = _observable_name
        self.stdout.info("REGTEST: The following variables will be renamed:")
        old_str = ",".join(name_maps.keys())
        new_str = ",".join(name_maps.values())
        self.stdout.info(f"REGTEST: Old: {old_str}")
        self.stdout.info(f"REGTEST: New: {new_str}")
        
        self.import_object(ws, pdf, ROOT.RooFit.RenameVariable(old_str, new_str),
                           ROOT.RooFit.RecycleConflictNodes())
        # import constraint terms
        for np_name, glob_name, constr_name in zip(np_list, glob_list, constr_list):
            new_np_name = np_name
            # check wheterh NP has been renamed. If yes, update the NP name
            for old_name, new_name in name_maps.items():
                if np_name == old_name:
                    new_np_name == new_name
                    break
            if glob_name != "":
                if (not ws_ext.var(np_name)) or (not ws_ext.var(glob_name)) or (not ws_ext.pdf(constr_name)):
                    raise RuntimeError(f"constraint pdf {constr_name} with NP = {np_name} and "
                                       f"GlobObs = {glob_name} does not exist")
                new_constr_name = CONSTRTERM_PREFIX + new_np_name
                new_glob_name = GLOBALOBS_PREFIX + new_np_name
                constr_pdf = ws_ext.pdf(constr_name)
                old_str = ",".join([constr_name, glob_name, np_name])
                new_str = ",".join([new_constr_name, new_glob_name, new_np_name])
                self.import_object(ws, constr_pdf, 
                                   ROOT.RooFit.RenameVariable(old_str, new_str))
                self.stdout.debug(f"REGTEST: Import systematics {new_np_name} "
                                  f"with constraint term {new_constr_name}")
                constraints.add(ws.pdf(new_constr_name), True)
                globobs.add(ws.var(new_glob_name), True)
            ws.var(new_np_name).setConstant(False)
            nuis.add(ws.var(new_np_name), True)
    
    def build_histogram_model(self, root_node:Dict, ws:ROOT.RooWorkspace, sample:Sample):
        cat_config = self.get_active_category_config()
        obs_name = cat_config['observable']['name']
        filename = self._translate_node_attrib(root_node, "Input")
        filepath = self.path_manager.get_relpath(filename)
        histname = self._translate_node_attrib(root_node, "ModelName")
        rebin = self._get_node_attrib(root_node, "Rebin", False, "-1", dtype="int")
        self.stdout.debug(f"REGTEST: Creating histogram pdf from `{filepath}`")
        h = self.get_histogram(filename, histname)
        if rebin > 0:
            h.Rebin(rebin)
        obs = ws.var(obs_name)
        if not obs:
            raise RuntimeError("observable not initialized")
        h_data = ROOT.RooDataHist("hdata", "hdata", obs, h)
        h_pdf = ROOT.RooHistPdf(sample.model_name, sample.model_name, obs, h_data)
        self.import_object(ws, h_pdf)
    
    def check_nuisance_parameters(self, model:ROOT.RooAbsPdf, nuis:ROOT.RooArgSet):
        cat_config = self.get_active_category_config()
        obs_name = cat_config['observable']['name']        
        var_set = model.getVariables()
        float_set = ROOT.RooArgSet()
        for var in var_set:
            if (not var.isConstant()):
                if var.getMin() == var.getMax():
                    var_name = var.GetName()
                    self.stdout.info(f"REGTEST: Fixing {var_name} to constant as it has same upper and loer boundary")
                    var.setConstant(True)
                else:
                    float_set.add(var)
        poi_obs_names = self.core_config['poi_names'] + [obs_name]
        # reove POI and observable from float set
        for name in poi_obs_names:
            float_var = float_set.find(name)
            if float_var:
                float_set.remove(float_var)
        num_np = len(nuis)
        num_poi = len(self.core_config['poi_names'])
        for var in float_set:
            if not nuis.find(var):
                nuis.add(var)
                var_name = var.GetName()
                self.stdout.info(f"REGTEST: Adding {var_name} to the nuisance parameter set")

        num_float = len(float_set)
        if num_float < num_np:
            self.stdout.warning(f"WARNING: There supposed to be {num_poi + num_np} free parameters, "
                                f"but only seen {num_float} in the category {self.active_category}. "
                                f"This is in principle not an issue, but please make sure you "
                                f"understand what you are doing")
            if self.debug_mode:
                self.stdout.debug("REGTEST: All free parameters: ")
                float_set.Print()
                self.stdout.debug("REGTEST: All nuisance parameters: ")
                nuis.Print()
        else:
            self.stdout.info("REGTEST: Number of nuisance parameters looks good!")
  
    def get_pdf_name(self, category:str):
        return f"{FINAL_PDF_NAME}_{category}"
    
    def implement_model_config_and_sets(self, ws:"ROOT.RooWorkspace", mc:"ROOT.RooStats.ModelConfig",
                                        obs:ROOT.RooArgSet, pois:ROOT.RooArgSet,
                                        nuis:ROOT.RooArgSet, globs:ROOT.RooArgSet):
        ws.defineSet("nuisanceParameters", nuis)
        ws.defineSet("globalObservables", globs)
        ws.defineSet("Observables", obs)        
        ws.defineSet("POI", pois)
        mc.SetPdf(ws.pdf("CombinedPdf"))
        mc.SetObservables(ws.set("Observables"))
        mc.SetParametersOfInterest(ws.set("POI"))
        mc.SetNuisanceParameters(ws.set("nuisanceParameters"))
        mc.SetGlobalObservables(ws.set("globalObservables"))
        self.import_object(ws, mc, silent=False)
                    
    def generate_workspace(self):
        t0 = time.time()
        channel_list = ROOT.RooCategory("channellist", "channellist")
        combined_pdf = ROOT.RooSimultaneous("CombinedPdf", "", channel_list)
        
        obs          = ROOT.RooArgSet()
        pois         = ROOT.RooArgSet()
        nuis         = ROOT.RooArgSet()
        globs        = ROOT.RooArgSet()
        constraints  = ROOT.RooArgSet()
        
        self.reset()
        
        categories = list(self.core_config['input_categories'])
        
        for category in categories:
            ws_cat = self.generate_single_category(category)
            self.cat_ws[category] = ws_cat
            
            # import channel pdf
            channel_list.defineType(category)
            pdf_name = self.get_pdf_name(category)
            pdf_cat = ws_cat.pdf(pdf_name)
            if not pdf_cat:
                raise RuntimeError(f"model pdf `{pdf_name}` for the category "
                                   f"`{category}` is not defined")
            combined_pdf.addPdf(pdf_cat, category)
            
            obs.add(ws_cat.set(OBS_SET), True)
            pois.add(ws_cat.set(POI_SET), True)
            nuis.add(ws_cat.set(NUIS_SET), True)
            globs.add(ws_cat.set(GLOB_SET), True)
            if self.debug_mode:
                ws_i.Print()
                
        self.stdout.info("REGTEST: Making combined workspace")
                
        # implement main pdf
        self.import_object(self.comb_ws, combined_pdf)
        
        # implement model config
        self.implement_model_config_and_sets(self.comb_ws, self.model_config,
                                             obs, pois, nuis, globs)
        
        weight_var = ROOT.RooRealVar("wt", "wt", 1)
        args = ROOT.RooArgSet()
        args.add(obs)
        args.add(weight_var)
        
        dataset_map = ExtendedModel.get_dataset_map(self.datasets)
        dataset_binned_map = ExtendedModel.get_dataset_map(self.datasets_binned)
        
        dataset_name = self.core_config['dataset_name']
        obs_data = ROOT.RooDataSet(dataset_name, "Combined data", args,
                                   ROOT.RooFit.Index(channel_list),
                                   ROOT.RooFit.Import(dataset_map),
                                   ROOT.RooFit.WeightVar(weight_var))
        obs_data_binned = ROOT.RooDataSet(dataset_name + "binned", 
                                          "Binned combined data", args,
                                          ROOT.RooFit.Index(channel_list),
                                          ROOT.RooFit.Import(dataset_binned_map),
                                          ROOT.RooFit.WeightVar(weight_var))
        self.import_object(self.comb_ws, obs_data, silent=False)
        if (obs_data_binned.numEntries() < obs_data.numEntries()):
            self.import_object(self.comb_ws, obs_data_binned, silent=False)
        else:
            self.stdout.warning("REGTEST: No need to keep binned dataset, as the "
                                "number of data events is smaller than or equal "
                                "to the number of bins in all categories", "red")
            self.use_binned = False
        
        # save the original snapshot
        # self.comb_ws.saveSnapshot("nominalNuis", self.model_config.GetNuisanceParameters())
        # self.comb_ws.saveSnapshot("nominalGlobs", self.model_config.GetGlobalObservables())
        
        # generate asimov datasets
        self.generate_asimov()
        
        # import class code
        class_code_dirs = self.core_config["class_code_dirs"]
        if (class_code_dirs["decl"] is not None) and (class_code_dirs["impl"] is not None):
            self.stdout.warning("REGTEST: Importing class code")            
            self.comb_ws.addClassDeclImportDir(class_code_dirs["decl"])
            self.comb_ws.addClassImplImportDir(class_code_dirs["impl"])
            self.comb_ws.importClassCode()
            
        # save final workspace
        self.path_manager.makedir_for_files("output")
        output_path = self.path_manager.get_file("output")
        self.comb_ws.writeToFile(output_path, True)
        
        t1 = time.time()
        self.time_taken += (t1 - t0)
        self.print_final_summary()