from typing import Optional, List, Dict, Union, Callable
import os
import glob
import json

import numpy as np

from quickstats import ConfigurableObject, semistaticmethod
from .analysis_path_manager import AnalysisPathManager
from .config_format_templates import DEFAULT_SAMPLE_CONFIG_FORMAT

class NTupleProcessTool(ConfigurableObject):
    """ Tool for processing root ntuples
    """
    
    CONFIG_FORMAT = DEFAULT_SAMPLE_CONFIG_FORMAT
    
    REQUIRED_CONFIG_COMPONENTS = ["sample_dir", "sample_subdir", "samples", "merge_samples"]
    
    DEFAULT_SAMPLE_OUTNAME         = "{sample_name}_{sample_type}.root"
    DEFAULT_MERGED_SAMPLE_OUTNAME  = "{sample_name}.root"
    DEFAULT_CUTFLOW_OUTNAME        = "cutflow_{sample_name}_{sample_type}.csv"
    DEFAULT_WEIGHT_OUTNAME         = "yield_{sample_name}_{sample_type}.json"
    DEFAULT_MERGED_CUTFLOW_OUTNAME = "cutflow_{sample_name}.csv"
    
    @property
    def sample_config(self):
        return self.config
    
    def __init__(self, sample_config:Union[Dict, str], outdir:str='output',
                 processor_config:Optional[str]=None,
                 processor_flags:Optional[List[str]]=None,
                 use_template:bool=False,
                 multithread:bool=True,
                 disable_config_message:bool=False,
                 verbosity:Optional[Union[int, str]]="INFO",
                 **kwargs):
        
        super().__init__(disable_config_message=disable_config_message,
                         verbosity=verbosity)
        self.outdir = outdir
        self.path_manager = AnalysisPathManager(outdir)
        self.path_manager.set_directory("ntuple", "ntuples")
        self.path_manager.set_directory("cutflow", "cutflow")
        
        self.load_sample_config(sample_config)
        
        self.processor = None        
        if processor_config is not None:
            self.load_processor_config(processor_config,
                                       use_template=use_template,
                                       multithread=multithread)
            
        if processor_flags is not None:
            self.processor_flags = list(processor_flags)
        else:
            self.processor_flags = []
        
        self.cutflow_report = None
        
    def load_sample_config(self, config_source:Union[Dict, str]):
        if isinstance(config_source, str):
            if not os.path.exists(config_source):
                raise FileNotFoundError(f'config file "{config_source}" does not exist')
            config_path = os.path.abspath(config_source)
            self.path_manager.set_file("sample_config", config_path)
        self.load_config(config_source)
        
        self.all_samples = list(self.sample_config['samples'])
        merge_samples = self.sample_config['merge_samples']
        if not merge_samples:
            self.all_merged_samples = list(self.all_samples)
        else:
            self.all_merged_samples = list(merge_samples)
            # fill missing samples
            for sample in self.all_samples:
                if ((sample not in merge_samples) and 
                    all(sample not in _samples for _samples in merge_samples.values())):
                    self.all_merged_samples.append(sample)
        
    def load_processor_config(self, config_path:str,
                              multithread:bool=True,
                              use_template:bool=False):
        from quickstats.components.processors import RooProcessor
        self.processor = RooProcessor(config_path,
                                      use_template=use_template,
                                      multithread=multithread,
                                      verbosity=self.stdout.verbosity)
        self.path_manager.set_file("processor_config", os.path.abspath(config_path))
        
    def get_validated_samples(self, samples:Optional[List[str]]=None, merged:bool=False):
        if merged:
            ref_samples = self.all_merged_samples
        else:
            ref_samples = self.all_samples
            
        if samples is not None:
            for sample in samples:
                if sample not in ref_samples:
                    raise RuntimeError(f'no information regarding the sample "{sample}" '
                                       f'is specified in the sample config file')
        else:
            samples = ref_samples
        return samples
    
    @semistaticmethod
    def get_sample_outpath(self, sample_config:Dict, outdir:str):
        sample_name = sample_config["name"]
        sample_type = sample_config["type"]
        basename = self.DEFAULT_SAMPLE_OUTNAME.format(sample_name=sample_name,
                                                      sample_type=sample_type)
        return os.path.join(outdir, basename)
    
    @semistaticmethod
    def get_merged_sample_outpath(self, sample_config:Dict, outdir:str):
        sample_name = sample_config["name"]
        basename = self.DEFAULT_MERGED_SAMPLE_OUTNAME.format(sample_name=sample_name)        
        return os.path.join(outdir, basename)
    
    @semistaticmethod
    def get_cutflow_outpath(self, sample_config:Dict, outdir:str):
        sample_name = sample_config["name"]
        sample_type = sample_config["type"]
        basename_cutflow = self.DEFAULT_CUTFLOW_OUTNAME.format(sample_name=sample_name,
                                                               sample_type=sample_type)
        basename_weight  = self.DEFAULT_WEIGHT_OUTNAME.format(sample_name=sample_name,
                                                              sample_type=sample_type)
        return [os.path.join(outdir, basename_cutflow), os.path.join(outdir, basename_weight)]  
    
    @semistaticmethod
    def get_merged_cutflow_outpath(self, sample_config:Dict, outdir:str):
        sample_name = sample_config["name"]
        basename = self.DEFAULT_MERGED_CUTFLOW_OUTNAME.format(sample_name=sample_name)
        return os.path.join(outdir, basename)    
    
    def prerun_process(self, sample_config:Dict):
        pass

    def process_samples(self, samples:Optional[List[str]]=None,
                        sample_types:Optional[List[str]]=None):
        if self.processor is None:
            raise RuntimeError("processor not initialized (probably missing a processor config)")
        samples       = self.get_validated_samples(samples)
        sample_dir    = self.sample_config.get('sample_dir', './')
        sample_subdir = self.sample_config.get('sample_subdir', {})
        sample_specs  = self.sample_config['samples']
        outdir = self.path_manager.base_path
        for sample in samples:
            self.processor.set_flags(self.processor_flags)
            for sample_type in sample_specs[sample]:
                if (sample_types is not None) and (sample_type not in sample_types):
                    continue
                all_files = []
                subsamples = sample_specs[sample][sample_type]
                if isinstance(subsamples, str):
                    subsamples = [subsamples]
                for subsample in subsamples:
                    sample_path = os.path.join(sample_dir, sample_subdir.get(sample_type, ''), 
                                               subsample)
                    if os.path.isdir(sample_path):
                        subfiles = glob.glob(os.path.join(sample_path, "*.root"))
                    else:
                        subfiles = glob.glob(sample_path)
                    if len(subfiles) == 0:
                        raise RuntimeError(f"no matching samples found for {sample_path}")
                    all_files += subfiles
                sample_config = {
                    "name": sample,
                    "path": sample_path,
                    "type": sample_type
                }
                self.processor.global_variables['sample'] = sample
                self.processor.global_variables['sample_type'] = sample_type
                self.processor.global_variables['outdir'] = outdir
                self.prerun_process(sample_config)                
                self.processor.run(all_files)
                self.processor.clear_global_variables()
                
    def merge_outputs(self, source_path_func:Callable,
                      target_path_func:Callable,
                      merge_func:Callable,
                      outdir:str,
                      samples:Optional[List[str]]=None,
                      subdirs:Optional[List[str]]=None):
        samples = self.get_validated_samples(samples, merged=True)
        sample_specs = self.sample_config['samples']
        if 'merge_samples' in self.sample_config:
            merged_sample_specs = self.sample_config['merge_samples']
        else:
            merged_sample_specs = {sample: [sample] for sample in samples}
        for sample in samples:
            if (sample not in merged_sample_specs) and \
               all(sample not in _samples for _samples in merged_sample_specs.values()):
                merged_sample_specs[sample] = [sample]
        if subdirs is None:
            subdirs = [""]
        for subdir in subdirs:
            sample_subdir = os.path.join(outdir, subdir)
            for sample in merged_sample_specs:
                # only merge what is requested
                if sample not in samples:
                    continue
                subsamples = merged_sample_specs[sample]
                source_files = []
                for subsample in subsamples:
                    # merge n-tuples from different mc campaigns / data years
                    for sample_type in sample_specs[subsample]:
                        sample_config = {
                            "name": subsample,
                            "type": sample_type
                        }
                        file = source_path_func(sample_config, sample_subdir)
                        source_files.append(file)
                sample_config = {"name": sample}
                target_file = target_path_func(sample_config, sample_subdir)
                self.stdout.info(f'INFO: Merging outputs for the sample "{sample}"')
                merge_func(source_files, target_file)                      
    
    def merge_samples(self, samples:Optional[List[str]]=None, subdirs:Optional[List[str]]=None):
        outdir = self.path_manager.get_directory("ntuple")
        self.merge_outputs(self.get_sample_outpath,
                           self.get_merged_sample_outpath,
                           self._merge_samples_with_hadd,
                           outdir=outdir,
                           samples=samples,
                           subdirs=subdirs)
    
    def _merge_samples_with_hadd(self, fnames:List[str], outname:str):
        for fname in fnames:
            if not os.path.exists(fname):
                raise FileNotFoundError(f'missing ntuple file "{fname}"')
        hadd_cmd = "hadd -f {} {}".format(outname, " ".join(fnames))
        os.system(hadd_cmd)
            
    def merge_cutflows(self, samples:Optional[List[str]]=None, subdirs:Optional[List[str]]=None):
        outdir = self.path_manager.get_directory("cutflow")
        self.merge_outputs(self.get_cutflow_outpath,
                           self.get_merged_cutflow_outpath,
                           self._merge_cutflow_data,
                           outdir=outdir,
                           samples=samples,
                           subdirs=subdirs)
            
    def _merge_cutflow_data(self, fnames:List[str], outname:str):
        import pandas as pd
        merged_df = None
        for fname in fnames:
            if isinstance(fname, (list, tuple)):
                # first file contains cutflow information
                # second file contains weight information                
                assert len(fname) == 2
                cutflow_fname = fname[0]
                weight_fname = fname[1]
            else:
                cutflow_fname = fname
                weight_fname = None
            if not os.path.exists(cutflow_fname):
                raise FileNotFoundError(f'missing cutflow file "{cutflow_fname}"')
            cutflow_df = pd.read_csv(cutflow_fname).set_index(['name'])
            if (weight_fname is None) or not os.path.exists(weight_fname):
                weight_data = None
            else:
                with open(weight_fname, 'r') as file:
                    weight_data = np.array(list(json.load(file).values()))
            if merged_df is None:
                merged_df = cutflow_df.copy()
                if weight_data is not None:
                    assert len(merged_df) == len(weight_data)
                    merged_df['yield'] = weight_data
            else:
                merged_df['all']  += cutflow_df['all']
                merged_df['pass'] += cutflow_df['pass']
                if 'yield' in merged_df:
                    if weight_data is None:
                        raise RuntimeError(f'missing weight file that is in association with the '
                                           f'cutflow file "{cutflow_fname}"')
                    merged_df['yield'] += weight_data
        if 'yield' in merged_df:
            yields = merged_df['yield'].values
            yield_efficiency = [100]
            yield_cumul_efficiency = [100]
            for i in range(1, len(yields)):
                yield_efficiency.append(100 * (yields[i] / yields[i-1]))
                yield_cumul_efficiency.append(100 * (yields[i] / yields[0]))
            merged_df['yield_efficiency'] = yield_efficiency
            merged_df['yield_cumulative_efficiency'] = yield_cumul_efficiency
        merged_df.to_csv(outname)
        self.stdout.info(f'INFO: Saved cutflow data as "{outname}"')
        
    def load_cutflow_report(self, samples:Optional[List[str]]=None):
        import pandas as pd
        samples = self.get_validated_samples(samples, merged=True)
        
        sample_spec   = self.sample_config['samples']
        cutflow_dir   = self.path_manager.get_directory("cutflow")
        
        cutflow_report = {}
        for sample in self.all_merged_samples:
            if sample not in samples:
                continue
            sample_config = {
                "name": sample
            }
            cutflow_file = self.get_merged_cutflow_outpath(sample_config, cutflow_dir)
            if not os.path.exists(cutflow_file):
                self.stdout.warning(f'WARNING: Missing cutflow file for the sample "{sample}".')
                continue
            df = pd.read_csv(cutflow_file)
            cutflow_report[sample] = df
            
        self.cutflow_report = cutflow_report

    def plot_cutflow_report(self, samples:Optional[List[str]]=None,
                            label_map:Optional[Dict]=None):

        import matplotlib.pyplot as plt
        
        plt.rcParams['figure.dpi'] = 200
        
        # Load the cutflow report if it doesn't exist yet
        if self.cutflow_report is None:
            self.load_cutflow_report(samples)

        colors = ["#36B1BF","#F2385A","#FDC536"]  # turqouise, pink, yellow

        if samples is None:
            samples = list(self.cutflow_report.keys())
            
        if label_map is None:
            label_map = {}
            
        # Loop over each sample and make a plot of the cutflow
        for sample in samples: 
            
            if sample not in self.cutflow_report:
                print(f'WARNING: Missing cutflow report for the sample "{sample}". Skipped.')
                continue

            df = self.cutflow_report[sample] 

            cut_labels = [label_map.get(name, name) for name in df["name"]]

            fig, axs = plt.subplots(3, 1, figsize=(17, 8))
            fig.tight_layout(pad=3.0)

            for i in range(len(axs)): # set x-axes style
                axs[i].tick_params(axis='x', rotation =15, labelsize=10) 

            # Yields bar chart 
            axs[0].bar(cut_labels, df["yield"], color=colors[0])
            axs[0].set_ylabel("Yields", fontsize=14)
            
            # Efficiency bar chart 
            axs[1].bar(cut_labels, df["yield_efficiency"], color=colors[1])
            axs[1].set_ylabel("Efficiency [%]", fontsize=14)
            
            # Culmulative efficiency bar chart 
            axs[2].bar(cut_labels, df["yield_cumulative_efficiency"], color=colors[2])
            axs[2].set_ylabel("Cumulative Efficiency [%]", fontsize=14)

            fig.suptitle(f"Sample: {sample}", fontsize=20, y=0.98)
            
            plt.show()