"""
spike_feature_adaptation.py

Modules for determine spike height
adaptations across spike trains.

"""

import numpy as np 

import pandas as pd 

###################################################################################################
###################################################################################################

def spikeheight_adaptation(df_spikes): 
    """ return spike height adaptation for single sweep """
    
    if len(df_spikes) > 1: 
        peak_v = df_spikes['peak_v'].values
        return peak_v[0]/peak_v[-1]
    else: 
        return np.nan # no spk height adaptation 
    
    
def trough_adaptation(df_spikes): 
    """ return trough adaptation changes for single sweep """
    
    if len(df_spikes) > 1: 
        trough_v = df_spikes['trough_v'].values
        return trough_v[0]/trough_v[-1]
    else: 
        return np.nan # no trough adaptation 
    
    
def upstroke_adaptation(df_spikes): 
    """ return upstroke adaptation changes for single sweep """
    
    if len(df_spikes) > 1: 
        upstroke = df_spikes['upstroke'].values
        return upstroke[0]/upstroke[-1]
    else: 
        return np.nan # no upstroke adaptation 
    
    
def downstroke_adaptation(df_spikes): 
    """ return downstroke adaptation changes for single sweep """
    
    if len(df_spikes) > 1: 
        downstroke = df_spikes['downstroke'].values
        return downstroke[0]/downstroke[-1]
    else: 
        return np.nan # no donwstroke adaptation 