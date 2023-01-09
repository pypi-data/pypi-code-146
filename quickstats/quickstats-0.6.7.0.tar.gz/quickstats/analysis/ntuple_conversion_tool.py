from typing import Union, List, Optional, Dict
from itertools import repeat
import os
import sys
import copy

import numpy as np
import pandas as pd

from quickstats import semistaticmethod, AbstractObject
from quickstats.utils.common_utils import execute_multi_tasks
from quickstats.utils.data_conversion import downcast_dataframe
from quickstats.analysis import AnalysisBase

class NTupleConversionTool(AnalysisBase):
    
    REQUIRED_CONFIG_COMPONENTS = ["paths:*"]
    
    DEFAULT_COLUMNS = {}
    
    DEFAULT_NTUPLE_SAMPLE_BASENAME = "{sample_name}.root"
    DEFAULT_ARRAY_SAMPLE_BASENAME  = "{sample_name}.{fmt}"
    
    DEFAULT_H5_KEY = "analysis_data"
    
    def __init__(self, analysis_config:Optional[Union[Dict, str]]=None,
                 ntuple_dir:Optional[str]=None,
                 array_dir:Optional[str]=None,
                 verbosity:Optional[Union[int, str]]="INFO",
                 **kwargs):
        super().__init__(analysis_config=analysis_config,
                         ntuple_dir=ntuple_dir,
                         array_dir=array_dir,
                         disable_config_message=True,
                         verbosity=verbosity,
                         **kwargs)
        self.stdout.info(f'INFO: Initialized ntuple directory as "{self.get_directory("ntuple")}".')
        self.stdout.info(f'INFO: Initialized array directory as "{self.get_directory("array")}".')
        self.stdout.info(f'INFO: Initialized ntuple treename as "{self.treename}".')
        
    @semistaticmethod
    def _save(self, df, outpath:str, fmt:str="csv",
              mode:str="a", complevel:int=None):
        
        assert (fmt in ["csv", "h5"])
        assert (mode in ["w", "a", "r"])
        
        if fmt == "csv":
            if mode in ["w", "r"]:
                header = True
            else:
                header = False
            df.to_csv(outpath, mode=mode, index=False, header=header)
        elif fmt == "h5":
            df.to_hdf(outpath, key=self.DEFAULT_H5_KEY, mode=mode,
                      index=False, complevel=complevel)
                
    @semistaticmethod
    def _postprocess(self, df, **kwargs):
        return df
    
    @semistaticmethod
    def _finalize(self, df, **kwargs):
        pass

    @semistaticmethod
    def _convert(self, filename:str, sample_name:str, treename:str,
                 outdir:str, columns:Optional[Union[List, Dict]]=None,
                 apply_columns:Optional[Dict]=None,
                 drop_columns:Optional[List]=None,
                 fmt:str="csv",
                 downcast:bool=True,
                 complevel:int=None,
                 chunksize:int=100000,
                 library:str="quickstats",
                 kwargs:Optional[Dict]=None):
        
        if columns is None:
            columns = copy.deepcopy(self.DEFAULT_COLUMNS)

        self.stdout.info(f'INFO: Processing file "{filename}"')

        #NTupleProcessTool.remove_csv(sample, outdir)
        
        if library == "quickstats":
            # does not support chunksize
            from quickstats.utils.data_conversion import root2dataframe
            df = root2dataframe(filename, treename, columns=columns,
                                remove_non_standard_types=False,
                                downcast=downcast, library="root")
            df_iter = [df]
        elif library == "root_pandas":
            import root_pandas
            _columns = ["noexpand:" + k for k in columns.values()]
            df_iter = root_pandas.read_root(filename, 
                                            key=treename,
                                            columns=_columns,
                                            chunksize=chunksize)
        else:
            raise RuntimeError(f"invalid library: {library}")
                               
        for i, df in enumerate(df_iter):
            
            if len(df) == 0: 
                continue            
            
            if library == "root_pandas":
                df.columns = list(columns)
                df.reset_index(drop=True, inplace=True)
                
                # Fix some columns which are just arrays of length 1
                for col in df.columns:
                    if df[col].dtype == 'object' and df[col].iloc[0].size == 1: df[col] = df[col].str[0]
                        
                if downcast:
                    downcast_dataframe(df)
                
            if apply_columns is not None:
                for key, value in apply_columns.items():
                    result = df.apply(lambda x: value(x), axis=1)
                    df[list(key)] = df.apply(lambda x: value(x), axis=1)
            
            df = self._postprocess(df, **kwargs, sample_name=sample_name)
            
            if drop_columns is not None:
                df = df.drop(drop_columns, axis=1)
                
            outpath = self.get_array_sample_path(sample_name=sample_name, dirname=outdir, fmt=fmt)
            if i == 0:
                self.stdout.info(f'INFO: Saving data array as "{outpath}"')
                self._save(df, outpath=outpath, fmt=fmt, 
                           mode='w', complevel=complevel)
            else:
                self._save(df, outpath=outpath, fmt=fmt, 
                           mode='a', complevel=complevel)
                
            self._finalize(df, **kwargs, sample_name=sample_name, outdir=outdir,
                           fmt=fmt, complevel=complevel, iteration=i)
            
    @semistaticmethod
    def get_ntuple_sample_path(self, sample_name:Dict, dirname:str):
        basename = self.DEFAULT_NTUPLE_SAMPLE_BASENAME.format(sample_name=sample_name)
        return os.path.join(dirname, basename)
    
    @semistaticmethod
    def get_array_sample_path(self, sample_name:Dict, dirname:str, fmt:str):
        basename = self.DEFAULT_ARRAY_SAMPLE_BASENAME.format(sample_name=sample_name, fmt=fmt)
        return os.path.join(dirname, basename)    
                 
    def convert_samples(self, samples:Optional[List[str]]=None,
                        kinematic_regions:Optional[List]=None,
                        columns:Optional[Union[List, Dict]]=None,
                        apply_columns:Optional[Dict]=None,
                        drop_columns:Optional[List]=None,
                        library:str="quickstats",
                        fmt:Optional[str]=None,
                        downcast:Optional[bool]=None,
                        complevel:Optional[int]=None,
                        chunksize:int=100000,
                        parallel:int=0,
                        **kwargs):
        if fmt is None:
            fmt = self.get_analysis_data_format()
        if fmt not in ["csv", "h5"]:
            raise ValueError("only csv or h5 formats are allowed")
            
        if (fmt != "h5") and (complevel is not None):
            raise ValueError("compression level is only allowed in h5 format")
        
        if downcast is None:
            if fmt == "csv":
                downcast = False
            else:
                downcast = True
                
        if self.all_samples:
            samples = self.resolve_samples(samples)
        if samples is None:
            raise RuntimeError("no samples specified")
            
        if kinematic_regions is None:
            kinematic_regions = self.all_kinematic_regions
        # no kinematic regions defined, use inclusive data with no sub-directories
        if not kinematic_regions:
            kinematic_regions = [""]
            
        if library == "quickstats":
            import ROOT
            if ROOT.IsImplicitMTEnabled():
                ROOT.DisableImplicitMT()
            if parallel != 0:
                parallel = 0
                sys.stdout.write("INFO: Disabling multi-processing when using ROOT backend\n")            
        
        ntuple_dir = self.get_directory("ntuple")
        array_dir = self.get_directory("array")
        
        for kinematic_region in kinematic_regions:
            if kinematic_region:
                self.stdout.info(f'INFO: Converting ntuples in the kinematic region "{kinematic_region}"')
                ntuple_subdir = os.path.join(ntuple_dir, kinematic_region)
                array_subdir = os.path.join(array_dir, kinematic_region)
            else:
                ntuple_subdir = ntuple_dir
                array_subdir  = array_dir
                
            if not os.path.exists(array_subdir):
                os.makedirs(array_subdir)
                
            filenames = []
            for sample in samples:
                filename = self.get_ntuple_sample_path(sample_name=sample, dirname=ntuple_subdir)
                filenames.append(filename)

            args = (filenames, samples, repeat(self.treename), repeat(array_subdir),
                    repeat(columns), repeat(apply_columns), repeat(drop_columns),
                    repeat(fmt), repeat(downcast), repeat(complevel), repeat(chunksize),
                    repeat(library), repeat(kwargs))

            execute_multi_tasks(self._convert, *args, parallel=parallel)