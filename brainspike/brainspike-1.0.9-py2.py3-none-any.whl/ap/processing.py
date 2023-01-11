"""
ap_processing.py

Action potential processing. 
"""

# ap feature extraction 
# https://allensdk.readthedocs.io/en/latest/allensdk.ephys.html
from operator import index
from brainspike.ap.lib import ephys_extractor as efex 
from brainspike.ap.lib import ephys_features as ft

import numpy as np
import pandas as pd
import math
from tqdm import tqdm as tqdm 

# error raise
class NoStim(Exception): pass
class DataTypeError(Exception): pass

# TO DO: 
    # 1 - remove all spacing in the output variables
    # 2 - add save out functions
    # 3 - fix exclusion criteria so it adds on each iteration
    # 4 - test with different protocols --> error raised? 
    # 5 - ap types needed to be determined only with 500 ms? 
    # 6 - ap types; currently not set to decipher between type 2/3 due to lack of aborted spike detection. 
    # 7 - save function for the report summary
    # 8 - currently index set for abf_id
    # 9 - options to compartmentalise the data? E.g. no metadata in the report summary? 
    # 10 - add metadata save out option + processing input save out option?? 
    # 11 - get ap half_width

#----------------------------

def feature_extract(data, filter = 10, dv_cutoff = 5, min_peak = 0, thresh_frac = 0.05,\
     max_interval = 0.020, baseline_voltage = [-80, -40], min_height=2., baseline_interval=0.1, baseline_detect_thresh=0.3): 

    """
    Conduct feature extraction on max firing sweep of an action potential, and all sweeps. 

    Steps include: 1) pre-processing 2) feature extraction 3) rheobase detection 4) find max firing sweep 5) ap type classification

    Arguments
    ---------
    Arguments adapted from the following Allen Brain API: https://allensdk.readthedocs.io/en/latest/allensdk.ephys.html
    filter : cutoff frequency for 4-pole low-pass Bessel filter in kHz (optional, default 10)
    dv_cutoff : minimum dV/dt to qualify as a spike in V/s (optional, default 20)
    max_interval : maximum acceptable time between start of spike and time of peak in sec (optional, default 0.005)
    min_height : minimum acceptable height from threshold to peak in mV (optional, default 2)
    min_peak : minimum acceptable absolute peak level in mV (optional, default 0)
    thresh_frac : fraction of average upstroke for threshold calculation (optional, default 0.05)
    baseline_interval: interval length for baseline voltage calculation (before start if start is defined, default 0.1)
    baseline_detect_thresh : dV/dt threshold for evaluating flatness of baseline region (optional, default 0.3)

    Returns
    -------


    """

    processing_summary = pd.DataFrame({'abf_id': '', 'exclusion_comments': 'No depolarisation step', 'filter_cutoff':filter, 'dv_cutoff':dv_cutoff,\
                 'max_interval_cutoff':max_interval,'min_height_cutoff':min_height, 'min_peak_cutoff':min_peak,'thresh_fraction_cutoff':thresh_frac,\
                     'baseline_interal_cutoff':baseline_interval,'baseline_detect_thresh_cutoff':baseline_detect_thresh}, index = [0])

    ap_types = []
    rheobases = []
    max_sweep_features_all = pd.DataFrame()
    max_spikes_features_all = pd.DataFrame()
    processing_summary_all = pd.DataFrame()
    metadata_summary_all = pd.DataFrame()

    pbar = tqdm(total=100, desc = 'Processed files', colour="blue", position=0, leave=True, mininterval=0) # progress bar 
    
    #---------------------------------------

    data = check_type(data) # type check for numpy or ap_objects

    ap_objects = []
    for ap_object in data: 

        #-----------------------------------
        # feature extraction for
        # action potential protocols
        sweeps_features_all = pd.DataFrame() 
        spikes_features_all = pd.DataFrame() 

        if len(ap_object.currentinj_start_end[0]) > 0:  
            for sweepnumber in range(len(ap_object.voltage)):
                
                # sweep start and end times
                start_time = (min(ap_object.currentinj_start_end[0])/ap_object.metadata.sample_rate_hz.values[0])
                end_time = (max(ap_object.currentinj_start_end[0])/ap_object.metadata.sample_rate_hz.values[0])
                
                # ephys feature extract: https://allensdk.readthedocs.io/en/latest/allensdk.ephys.html
                EphysObject = efex.EphysSweepFeatureExtractor(t = np.transpose(ap_object.time[sweepnumber]),\
                    v = np.transpose(ap_object.voltage[sweepnumber]), start = start_time, end = end_time, filter = filter,\
                        dv_cutoff = dv_cutoff, min_peak = min_peak, thresh_frac = thresh_frac, max_interval = max_interval,\
                            min_height=min_height, baseline_interval=baseline_interval, baseline_detect_thresh=baseline_detect_thresh)

                EphysObject.process_spikes()
                sweep_features = EphysObject._sweep_features # feature extract per sweep
                spikes_persweep = EphysObject._spikes_df # feature extract per spike per sweep

                if len(spikes_persweep) > 0:
                    # if not empty 
                    sweep_features = update_df(sweep_features, end_time, start_time, sweepnumber, ap_object, EphysObject)
                    spikes_persweep = update_df(spikes_persweep, end_time, start_time, sweepnumber, ap_object, EphysObject)
                else: 
                    # create empty df
                    sweep_features = empty_df_sweep_features(sweepnumber, ap_object, start_time, end_time)
                    spikes_persweep = empty_df_spikes(sweepnumber, ap_object, EphysObject, start_time, end_time)

                # check trough artefacts for spike detection
                spikes_persweep = check_troughs(spikes_persweep, end_time)

                # append sweep and spikes across all sweepnumbers
                sweeps_features_all = pd.concat([sweeps_features_all, sweep_features], axis = 0)
                spikes_features_all = pd.concat([spikes_features_all, spikes_persweep], axis = 0)

            sweeps_features_all = sweeps_features_all.reset_index(drop=True)
            spikes_features_all = spikes_features_all.reset_index(drop=True)

            # max firing sweep detect
            max_sweep_features, max_spikes_features = find_maxfiring_sweep(spikes_features_all, sweeps_features_all, baseline_voltage)

            # processing summary update 
            processing_summary['abf_id'] = ap_object.metadata.index
            processing_summary['exclusion_comments'] = processing_summary['exclusion_comments'].replace('No depolarisation step','', inplace=True) 

            # find ap types
            ap_type = find_aptype(max_sweep_features, min_peak, dv_cutoff)

            # find rheobase
            rheobase = find_rheobase(sweeps_features_all)

            # add report summary to ap_object 
            report_summary = pd.concat([processing_summary, pd.DataFrame({'ap_types': ap_type}, index = [0]),\
                max_sweep_features.reset_index(), max_spikes_features.reset_index(), pd.DataFrame({'rheobase_pa': rheobase}, index = [0])], axis = 1)

            report_summary = report_summary.loc[:,~(report_summary.columns.duplicated())] # remove any duplicate col
            report_summary = report_summary.set_index('abf_id') # set index 

            # append ap_object
            ap_object.sweeps_features = sweeps_features_all
            ap_object.spikes_features = spikes_features_all
            ap_object.report_summary = report_summary
            ap_objects.append(ap_object)

        pbar.update(100/len(data))

    return ap_objects

#-----------

def check_type(data): 
    """
    Check data type parsed. 
    Raise error if incorrect.
    """
    if isinstance(data, list): 
        if len(data) > 0: 
            if type(data[0]) != list or int or str or pd.DataFrame: # unpack first ap_object only
                return data
            else: 
                raise DataTypeError("Wrong data type | parse a list of ap_objects processed using ap_loader")
        else: 
            raise DataTypeError("No data found")

    elif isinstance(data, np.ndarray): 
         raise DataTypeError("Wrong data type | parse a list of ap_objects processed using ap_loader")
    elif isinstance(data, dict): 
        raise DataTypeError("Wrong data type | parse a list of ap_objects processed using ap_loader")
    elif isinstance(data, pd.DataFrame): 
        raise DataTypeError("Wrong data type | parse a list of ap_objects processed using ap_loader")
    elif isinstance(data, str):
        raise DataTypeError("Wrong data type | parse a list of ap_objects processed using ap_loader")
    elif isinstance(data, int):
        raise DataTypeError("Wrong data type | parse a list of ap_objects processed using ap_loader")


def check_troughs(spikes_features, end_time): 
    """
    Delete artefactual troughs near end of current stimulus
    detected due to current drop-off.
    """ 

    clip_time = 0.0002 # remove troughs < 0.2 ms from current stimulus end

    if "trough_t" in spikes_features.columns:
        troughs_clippingstim = spikes_features[(spikes_features['trough_t'] >= (end_time-clip_time))].index 
        if troughs_clippingstim.size > 0: 
            spikes_features.at[troughs_clippingstim[0],'trough_t'] = np.nan 

    return spikes_features

#-----------

def find_rheobase(sweep_features_all): 
    """
    Returns rheobase (pA) per sweep as df. 
    """

    rheobase = pd.DataFrame(columns=['rheobase (pA)'])

    if not sweep_features_all.empty:

        # find sweep > 0 Hz
        firing_sweeps = sweep_features_all[(sweep_features_all['avg_rate'] !=0) & (sweep_features_all['avg_rate'] != np.nan)] 
        
        # first sweep with avg_rate > 0 Hz
        if len(firing_sweeps) > 0: 
            rheobase_idx = firing_sweeps.index[0] # selecting first sweep with avg_rate > 0 Hz
            current_steps = sweep_features_all['current_analysed_sweep_pa'] 
            rheobase = current_steps[rheobase_idx]

        else: 
            rheobase = np.nan

        return rheobase


def find_maxfiring_sweep(spikes_features_all, sweeps_features_all, baseline_voltage):
    """
    Returns max firing sweep features. 
    Max firing sweep determined by the following: 

    - find highest frequency firing sweep 
    - find sweep with lowest spike height adaptation
    - remove sweeps not within baseline voltage (default: baseline_voltage = [-80, -40])
    - find sweep with max ap (if more than one found, defaults to the earliest spike (i.e. lowest peak_index value))

    Arguments
    ---------


    Returns
    -------


    """

    if not spikes_features_all.empty:
        
        # removing spikes on selected sweep 
        # not within baseline voltage
        maxfiring_sweeps = sweeps_features_all[(sweeps_features_all['baseline_voltage'] >= baseline_voltage[0])
        & (sweeps_features_all['baseline_voltage'] <= baseline_voltage[1])] 
        
        if len(maxfiring_sweeps) > 0: 
            
            # isolating highest avg_rate firing sweeps
            maxfiring_sweeps = maxfiring_sweeps[maxfiring_sweeps['avg_rate'] == max(maxfiring_sweeps['avg_rate'])]

            # find sweep with lowest spike-height adaptation ratio
                # if only one selection default to highest firing rate only
            if maxfiring_sweeps['spike_height_adaptation'].isna().sum() == len(maxfiring_sweeps): 
                maxfiring_sweeps = maxfiring_sweeps
            else: 
                maxfiring_sweeps = maxfiring_sweeps[(maxfiring_sweeps['spike_height_adaptation']
                == min(maxfiring_sweeps['spike_height_adaptation']))]

            # selecting spike data from sweep with highest frequency and lowest spike-height adaptation
            max_spikes_features_all = spikes_features_all[spikes_features_all['sweep_number'].isin(maxfiring_sweeps['sweep_number'])]

            # find max firing sweep with max ap
            if not max_spikes_features_all.empty:  

                # sub-select highest amplitude spike 
                # on spikes from highest firing sweeps
                max_spikes_features_all = max_spikes_features_all[max_spikes_features_all['peak_v'] == max(max_spikes_features_all['peak_v'])]

                if len(max_spikes_features_all) > 1: # if more than 1 spike found defaul to first spike
                    max_spikes_features_all = max_spikes_features_all[max_spikes_features_all['peak_index'] == min(max_spikes_features_all['peak_index'])]

                # finding sweep number with highest AP spike
                max_sweeps_features_all = maxfiring_sweeps[maxfiring_sweeps['sweep_number'].isin(max_spikes_features_all['sweep_number'])] 

                #re-index
                max_sweeps_features_all.reset_index(drop=True, inplace=True) 
                max_spikes_features_all.reset_index(drop=True, inplace=True)

        return max_sweeps_features_all, max_spikes_features_all


def find_aptype(max_sweeps_features_all, min_peak, dv_cutoff): 
    """
    Breakdown the number of AP analysed into different AP types as shown [here](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5071135/). 
    Calculated for default settings (AP amplitude >= 0 mV, dv/dt == 5). 
    Conducted on highest firing sweep. 

    Note: that ap type classification was based on 500 ms depolarisation steps, hence Hz metrics need to be considered.
    However, will stand for 1s + stimulations. 

    AP Type breakdown
    -----------------
    Type 5: >= 10 Hz firing freq
    Type 4: > 4  and < 10 Hz firing freq
    Type 2/3: > 0 and <= 2 avg_rate
    Type 1: == 0 Hz firing_freq
    
    Arguments
    ---------


    Returns
    -------


    """

    if min_peak == 0 and dv_cutoff == 5: 

        if len(max_sweeps_features_all) >= 1:
            avg_rate = max_sweeps_features_all.avg_rate.values[0]

            if avg_rate >= 10: 
                ap_type = 'Type 5'
            if (avg_rate >= 4) and (avg_rate < 10): 
                ap_type = 'Type 4'
            if (avg_rate > 0) and (avg_rate < 4): 
                ap_type = 'Type 2/3'
            if avg_rate == 0: 
                ap_type = 'Type 1'
                
            if math.isnan(avg_rate) == True: # exclude if no average rate found
                ap_type = np.nan
        else: 
            ap_type = np.nan
        
    else: 
        ap_type = 'min_peak != 0 & dv_cutoff != 5'
        
    return ap_type

#-----------

def update_df(df, end_time, start_time, sweepnumber, ap_object, EphysObject): 
    """
    Add the following values to df: 
        1. 'current stimulus length (s)'
        2. 'sweep_number',\
        3. 'current stimulus for analysed sweep (pA)'
        4. 'baseline_voltage'
    """

    if isinstance(df, dict): 
        df = pd.DataFrame(df, index = [0]) # dict --> df conversion

    df[['current_stimulus_length_sec', 'sweep_number',\
            'current_analysed_sweep_pa', 'baseline_voltage']] = pd.DataFrame([[round(end_time-start_time,2),\
                sweepnumber, max(ap_object.stimulus[sweepnumber]), EphysObject._get_baseline_voltage()]], index=df.index) 
    
    return df

#-----------

def empty_df_sweep_features(sweepnumber, ap_object, start_time, end_time):
    """
    Return empty df_sweep_features. 
    """

    df_sweep_features = pd.DataFrame({'avg_rate': 0, 'adapt': np.nan, 'latency': np.nan, 'isi_cv': np.nan,\
         'mean_isi': np.nan, 'median_isi': np.nan, 'first_isi': np.nan, 'adaptation_index': np.nan, 'spike_height_adaptation': np.nan,\
              'current_stimulus_length_sec': round(end_time-start_time,2), 'sweep_number': sweepnumber,\
                   'current_analysed_sweep_pa': max(ap_object.stimulus[sweepnumber]), 'baseline_voltage': np.nan}, index = [0])

    return df_sweep_features


def empty_df_spikes(sweepnumber, ap_object, EphysObject, start_time, end_time):
    """
    Return empty df_spikes. 
    """

    df_spikes = pd.DataFrame({'threshold_index': np.nan, 'clipped':np.nan, 'threshold_t':np.nan, 'threshold_v':np.nan, 'peak_index':np.nan,\
        'peak_t':np.nan, 'peak_v':np.nan, 'trough_index':np.nan, 'trough_t':np.nan, 'trough_v':np.nan, 'upstroke_index':np.nan, 'upstroke':np.nan,\
             'upstroke_t':np.nan, 'upstroke_v':np.nan, 'downstroke_index':np.nan, 'downstroke':np.nan, 'downstroke_t':np.nan, 'downstroke_v':np.nan,\
                  'isi_type':np.nan, 'fast_trough_index':np.nan, 'fast_trough_t':np.nan, 'fast_trough_v':np.nan, 'adp_index':np.nan, 'adp_t':np.nan,\
                       'adp_v':np.nan, 'slow_trough_index':np.nan, 'slow_trough_t':np.nan, 'slow_trough_v':np.nan, 'width':np.nan, 'upstroke_downstroke_ratio':np.nan,\
                            'current_stimulus_length_sec': round(end_time-start_time,2), 'sweep_number': sweepnumber,\
                                 'current_analysed_sweep_pa': max(ap_object.stimulus[sweepnumber]),\
                                      'baseline_voltage': EphysObject._get_baseline_voltage()}, index = [0])

    return df_spikes
