"""
subthrshold_processing.py

Class for detecting subthreshold features
in action potential sweepdata (subselected
for hyperpolarizing steps).

Note: subthreshold feature extraction modules adapted from iPFX
[https://github.com/AllenInstitute/ipfx/tree/797e677070ff161960bf72c97d70b40b91aef74a]

"""

import pandas as pd 

import numpy as np 

from ...abf.abf_obj import ABF
from ...features.ipfx.subthresh_features import (voltage_deflection, sag, input_resistance)
from ...curation.subthresh_sweepdata_qc import (drop_unstablesweeps_rms, drop_depolsweeps, measure_linregress)
from ...curation.subthresh_artefact_checks import (rem_sag_amps)
from ...plots.subthreshold_qc_plots import (ri_plot)
from ...plots.subthreshold_plots import (sag_plot)
from ...exporters.dataframes import (export_df)
from ...utils.core.core_load_utils import (find_srate, find_stimuli, find_sweepdata, find_sweeptimes)

###################################################################################################
###################################################################################################

class SubthresholdFeatures: 
    
    """ class for detecting sag current features in ap sweep data """
    
    def __init__(self, data, baseline_interval = 0.1, peak_width = 0.005, rms_cutoff = 0.2,\
                    sag_amp_threshold = [-5, -200], r2_cutoff = 0.8): 
        """
        """
        
        self.baseline_interval = baseline_interval 
        self.peak_width = peak_width
        self.rms_cutoff = rms_cutoff
        self.sag_amp_threshold = sag_amp_threshold
        self.r2_cutoff = r2_cutoff
        self.filtered_amp_idx = None 
        self.data = data 
                
                 
    @property
    def process_sag(self): 
        """ find sag features across all sweepdata for a single voltage recording """
        
        try: 
            isinstance(self.data, ABF)
            self.sweeptimes = find_sweeptimes(self.data)
            self.sweepdata = find_sweepdata(self.data)
            self.stimuli = find_stimuli(self.data)
            self.srate = find_srate(self.data)
            self.start = self.data.metadata['start_sec'] # start + end stimuli (seconds)
            self.end = self.data.metadata['end_sec']
            self._sweep_qc
            
        except AttributeError: 
            raise AttributeError("pass single data object ...")   
        
        # find sag and voltage deflections
        #----------------------------------
        # iterate across all 'stable' sweeps 
        
        if len(self.stable_sweepdata) > 0: 
            
            deflect_vset = []; deflect_indexset = []; sag_values = []; # better way to do this? 
            sag_voltages_fromsteady = []; sag_currentsteps = []; 
            for t, v, i in zip(self.stable_sweeptimes, self.stable_sweepdata, self.stable_stimuli): 
        
                # voltage_deflection
                #--------------------
                deflect_v, deflect_index = voltage_deflection(t,v,i, start = self.start,\
                                            end = self.end, deflect_type = None) # ipfx src code 
                
                # sag feature extraction
                #-----------------------
                sag_value, sag_voltage_fromsteady = sag(t,v,i, start = self.start, end = self.end,\
                                                        peak_width=self.peak_width,\
                                                        baseline_interval=self.baseline_interval) # ipfx src code 
                
                deflect_vset.append(deflect_v) 
                deflect_indexset.append(deflect_index)
                sag_values.append(sag_value)
                sag_voltages_fromsteady.append(sag_voltage_fromsteady)
                sag_currentsteps.append(min(i))
                
                # remove low amplitude sag 
                #--------------------------
                # filter sag between amp cutoffs
                # note: sag voltage must be a negative value

                self.filtered_amp_idx = rem_sag_amps(sag_voltages_fromsteady = sag_voltages_fromsteady,\
                                        amp_cutoffs = self.sag_amp_threshold) 
                
                ##################
                # sag feature df 
                ##################
                # output df for all sag features 
                # across stable sweeps 
                
                df_sag_all_sweeps = pd.DataFrame({'stable_sweep_number': self.adjusted_sweepnumbers[self.stable_sweepidx[0][self.filtered_amp_idx]],\
                                                'deflect_v': np.array(deflect_vset)[self.filtered_amp_idx],\
                                                'deflect_index': np.array(deflect_indexset)[self.filtered_amp_idx],\
                                                'sag_values': np.array(sag_values)[self.filtered_amp_idx],\
                                                'sag_voltages_fromsteady': np.array(sag_voltages_fromsteady)[self.filtered_amp_idx],\
                                                'sag_currentsteps': np.array(sag_currentsteps)[self.filtered_amp_idx]},\
                                                index = self.stable_sweepidx[0][self.filtered_amp_idx])
                
        else:
            df_sag_all_sweeps = pd.DataFrame({'stable_sweep_number': np.nan, 'deflect_v': np.nan, 'deflect_index': np.nan,\
                                            'sag_values': np.nan, 'sag_voltages_fromsteady': np.nan,\
                                            'sag_currentsteps': np.nan},\
                                            index = [0]) # empty df 
            
        return df_sag_all_sweeps

    
    @property
    def process_inputresistance(self): 
        """ find imput resistance for all sweeps """
        
        # process sag first to
        # remove unstable sweepdata 
        # and ensure all sweeps are 
        # hyperpolarizing ... 
        #--------------------------
        df_sag_all_sweeps = self.process_sag
        
        if len(self.stable_sweeptimes[self.filtered_amp_idx]) >= 3: 
             
            try: 
                v_peak = df_sag_all_sweeps['deflect_v'].values
                i = df_sag_all_sweeps['sag_currentsteps'].values
                
                linregress_dict = measure_linregress(i = i, v = v_peak) # check linearity 

                if linregress_dict['r2_value'] >= self.r2_cutoff: 
                
                    ri = input_resistance(self.stable_sweeptimes[self.filtered_amp_idx], self.stable_stimuli[self.filtered_amp_idx],\
                                            self.stable_sweepdata[self.filtered_amp_idx], start = self.start, end = self.end,\
                                                baseline_interval = self.baseline_interval)
                
                    return ri, linregress_dict['r2_value']
                
                else: 
                    return np.nan, linregress_dict['r2_value'] # if < r2 value cutoff 
            except: 
                return np.nan, np.nan   
        else: 
            return np.nan, np.nan  # sanity check :: < 3 sweeps // insufficient to calc. Ri 
            
          
    def df_subthreshold(self, i_search = -80, fdir = None, fname = None, file_extension = '.xlsx'): 
        """ sag features + ri + qc + detection parameters for select sweep with export option """
        
        if (i_search is not None) and (isinstance(i_search, int)): 
        
            df = pd.DataFrame(index = [self.data.metadata['abf_id']]) 
            
            # process sag features 
            df_sag_all_sweeps = self.process_sag
            
            # find values closest to i_search 
            # default set at -80 mV for HCN current
            #---------------------------------------
            sag_currentsteps = df_sag_all_sweeps['sag_currentsteps'].values
            sag_currentsteps_min_idx = np.absolute(sag_currentsteps - (i_search)).argmin()

            if sag_currentsteps_min_idx.size == 1: 
                
                # + metadata 
                df = pd.concat([pd.DataFrame(self.data.metadata,\
                    index = [self.data.metadata['abf_id']]), df], axis = 1, ignore_index = False)

                # + preprocessing params 
                try: 
                    self.data.preprocessed_params
                    df = pd.concat([df, pd.DataFrame(self.data.preprocessed_params,\
                        index = [self.data.metadata['abf_id']])], axis = 1, ignore_index = False)
                except: 
                    pass 
            
                # better way to insert vals to df here? 
                
                # + detection parameters 
                df['baseline_interval'] = self.baseline_interval
                df['peak_width'] = self.peak_width
                df['rms_cutoff'] = self.rms_cutoff
                df['sag_amp_threshold_min'] = self.sag_amp_threshold[0]
                df['sag_amp_threshold_max'] = self.sag_amp_threshold[1]
                df['i_search'] = i_search 
                df['r2_cutoff'] = self.r2_cutoff
            
                # + qc parameters
                df['total_sweep_count'] = len(self.sweepdata)
                df['analysed_sweep_count'] = len(self.stable_sweepdata)
                df['stable_sweep_currentsteps'] = [sag_currentsteps]
                
                # + sag values closest to i search 
                df['sag_currentstep'] = sag_currentsteps[sag_currentsteps_min_idx]
                df['sag_value'] = df_sag_all_sweeps['sag_values'].values[sag_currentsteps_min_idx]
                df['deflect_index'] = df_sag_all_sweeps['deflect_index'].values[sag_currentsteps_min_idx]
                df['deflect_v'] = df_sag_all_sweeps['deflect_v'].values[sag_currentsteps_min_idx]
                df['sweep_number'] = df_sag_all_sweeps['stable_sweep_number'].values[sag_currentsteps_min_idx]
                
                # + ri across all stable sweeps
                ri, r2 = self.process_inputresistance
                df['input_resistance'] = ri
                df['r2_value'] = r2
                    
                # export
                if None not in [fdir, fname, file_extension]:
                    export_df(data = self.data, df = df, fdir = fdir, fname = fname, file_extension = '.xlsx')
                    return df
                else: 
                    return df
            
            else: 
                raise ValueError(f'> 1 current steps found close to {i_search}'
                                 ' for subthreshold feature selection...')
        else: 
            raise TypeError('pass a current step to select sag'
                            ' values for as an int type ...')
    
        
    def df_all_sag_features(self, fdir = None, fname = None, file_extension = '.xlsx'): 
        """ return df of all sag features found per sweep """
        
        df_all_sag_features = self.process_sag
        
        # export
        if None not in [fdir, fname, file_extension]:
            export_df(data = self.data, df = df_all_sag_features,\
                        fdir = fdir, fname = fname, file_extension = '.xlsx')
        else: 
            pass
    
        return df_all_sag_features
    
    
    @property
    def _sweep_qc(self): 
        """ qc on sweepdata for rms stability + depol steps """
        
        # check for depolarization steps :: remove sweeps < 0 pA stimuli 
        self.hyperpol_sweepdata, self.hyperpol_sweeptimes,\
            self.hyperpol_stimuli, self.adjusted_sweepnumbers = drop_depolsweeps(self.sweepdata, self.sweeptimes, self.stimuli)

        # remove unstable sweeps :: remove sweeps > rms cutoff 
        if self.rms_cutoff is not None: 
            self.stable_sweepidx, self.stable_sweepdata, self.stable_sweeptimes,\
                self.stable_stimuli = drop_unstablesweeps_rms(self.hyperpol_sweepdata, self.hyperpol_sweeptimes, self.hyperpol_stimuli,\
                                                            end = self.end, srate = self.srate, rms_cutoff = self.rms_cutoff,\
                                                            baseline_interval = self.baseline_interval)
        else: 
            # set >> 10 if no stability to be checked
            raise ValueError(f'remove unstable sweeps for sag calculations | pass an rms cutoff: {self.rms_cutoff}') 
    
    
    def plot_ri(self, figdir = None, figname = None, figextension = None): 
        """ sanity check :: plot input resistance relationship """
        
        df_sag_all_sweeps = self.process_sag
        
        v_peak = df_sag_all_sweeps['deflect_v'].values
        i = df_sag_all_sweeps['sag_currentsteps'].values
        
        linregress_dict = measure_linregress(i = i, v = v_peak)
        
        ri_plot(v_peak = v_peak, i = i, figdir = figdir, figname = figname,\
                figextension = figextension, **linregress_dict)
    
    
    def plot_sag(self, sweeps = None, deflect_v = False, show_all_stable = False, xlim = [0, 2.5],\
                ylim_v = [-100, 40], ylim_i = [-100, 0], scale_bar = True, axis = False,\
                figdir = None, figname = None, figextension = None):
        """ plot sag features """
        
        
        # update this! // make fixes like for ap plots! // adjusted_sweepnumbers ... 
    
        if sweeps is not None: 
            pass
        else: 
            sweeps = self.stable_sweepidx[0] # default :: collect all stable
            
        df_sag_all_sweeps = self.process_sag
        
        # collect stable sweeps 
        if show_all_stable:
            stable_sweeps = self.stable_sweepidx[0]
            print(f'plotting stable sweeps | {stable_sweeps}')
        else: 
            stable_sweeps = None 
            
        # deflect idx 
        if deflect_v:
            if sum(np.in1d(self.stable_sweepidx, np.array(sweeps))) > 0: 
                
                deflect_idx = []
                for sweep in sweeps: 
                    try: 
                        deflect_idx.append(df_sag_all_sweeps.loc[sweep, 'deflect_index'])
                    except: 
                        deflect_idx.append(None)
                show_all_stable = False # default off 
            else: 
                deflect_idx = None 
        else: 
            deflect_idx = None 
        
        sag_plot(t = self.sweeptimes, i = self.stimuli, v = self.sweepdata, sweeps = sweeps,\
                xlim = xlim, ylim_v = ylim_v, ylim_i = ylim_i, stable_sweeps = stable_sweeps,\
                scale_bar = scale_bar, deflect_idx = deflect_idx, axis = axis,\
                start = self.start, end = self.end, figdir = figdir, figname = figname, figextension = figextension)
        
        
#####################        
        
        
class SubthresholdGroupFeatures(SubthresholdFeatures): 
    """ class for group subthreshold feature extractions """
    
    def __init__(self, data = None, baseline_interval = 0.1, peak_width = 0.005, rms_cutoff = 0.2,\
                    sag_amp_threshold = [-5, -200], r2_cutoff = 0.8, i_search = -80, group_data = None): 
        """
        """
        
        super().__init__(data, baseline_interval, peak_width, rms_cutoff,\
                            sag_amp_threshold, r2_cutoff)
        
        self.i_search = i_search 
        self.group_data = group_data
        
        
    def group_df_subthreshold(self, fdir = 'processed/subthreshold/df_subthreshold/master', fname = 'df_subthreshold'): 
        """ return group df for all subthreshold features """
        
        df = pd.DataFrame() 
        
        if self.group_data is not None: 
            for data in self.group_data: 
                
                self.data = data 
                self.filtered_amp_idx = None
                
                fname = data.metadata['abf_id']
                df_subthreshold = (self.df_subthreshold(i_search = self.i_search))

                df = df.append(df_subthreshold, ignore_index = False)    
        
        else: 
            raise ValueError(f'pass group data objects | group_data: {self.group_data} ...')
        
        if fdir is not None: 
            export_df(data = self.data, df = df, fdir = fdir, fname = fname, file_extension = '.xlsx') 
        else: 
            pass
        
        return df 
        
        
    def group_export_all_sag_features(self, fdir = 'processed/subthreshold/df_all_sag_features', file_extension = '.xlsx'): 
        """ export all sag features for data group """
        
        if self.group_data is not None: 
            for data in self.group_data: 
                
                self.data = data 
                self.filtered_amp_idx = None
                
                if fdir is not None: 
                    fname = data.metadata['abf_id'] # default to abf id 
                    self.df_all_sag_features(fdir = fdir, fname = fname, file_extension = file_extension) # export on each iteration 
                else: 
                    raise ValueError('pass a file directory for export | fdir: {fdir} ...')

            print('finished exporting all sag features ...')
            
        else: 
            raise ValueError(f'pass group data objects | group_data: {self.group_data} ...')
        
        
    def group_export_sag_plots(self, figdir = 'figures/subthreshold/sag', file_extension = '.pdf', xlim = None, scale_bar = False): 
        """ export all sag plots for selected 'stable' sweeps """
        
        if self.group_data is not None: 
            for data in self.group_data: 
                
                self.data = data 
                self.filtered_amp_idx = None
                self.df_all_sag_features() # process features
                
                if len(self.stable_sweepidx[0]) > 0: 
                    
                    figname = self.data.metadata['abf_id']
                    self.plot_sag(sweeps = self.stable_sweepidx[0], deflect_v = True, xlim = xlim,\
                                    ylim_v = None, ylim_i = None, scale_bar = scale_bar, axis = False,\
                                    figdir = figdir, figname = figname, figextension = file_extension)
                    
                else: 
                    pass # no sweeps found
                
                print('exported all subthreshold example plots ...')
        else: 
            raise ValueError(f'pass group data objects | group_data: {self.group_data} ...')