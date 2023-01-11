"""
ap_plots.py

Figure plots for action potentials. 
All processing completed using ap_object. 
"""

# metadata
import brainspike.ap.metadata as ap_metadata

# matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.font_manager as font_manager
from matplotlib.ticker import AutoMinorLocator
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator)  

# scipy
from scipy.ndimage import gaussian_filter1d
from scipy.stats import linregress, norm, sem

# numpy
import numpy as np

# libraries
import os
import math

# error raise
class DataTypeError(Exception): pass
class FileIdTypeError(Exception): pass
class SelectIdentifier(Exception): pass
class SelectEphysFeature(Exception): pass
class NoSpike(Exception): pass

#---------------------

def maxfiring_ap(ap_object, identifier = None, fname = None, ylim_v = [-80, 60], ylim_stimulus = [0, 300], show_ephys_features = None, auto_save = True, dpi = 500): 
    """
    Plotting the max firing sweep for selected ap_object. 
    Highlights idx for peak v detection, thresholds.

    Option to plot by an identifier, or just by parsing in the ap_object. 
    Automatically provides the identifier id for plotting. 

    Arguments
    ---------


    Returns
    -------


    """
    
    # figure
    plt.style.use('brainspike/ap/util/plots/paper.mplstyle')
    fig, ax = plt.subplots(2,1, figsize=(6,5), gridspec_kw={'height_ratios': [3.8, 1]})
    
    if isinstance(ap_object, list) == False: 
        time = ap_object.time
        voltage = ap_object.voltage
        stimulus = ap_object.stimulus
        sample_rate_hz = ap_object.metadata.sample_rate_hz
        start = (min(ap_object.currentinj_start_end[0])/sample_rate_hz).values[0] # start time of stimulus
        end = (max(ap_object.currentinj_start_end[0])/sample_rate_hz).values[0] # end time of stimulus
        currentstep = ap_object.report_summary.current_analysed_sweep_pa.values[0] # current step
        max_firing_sweep = ap_object.report_summary.sweep_number.values[0]
        max_firing_spike_features = ap_object.spikes_features[ap_object.spikes_features.sweep_number == max_firing_sweep]
        
    elif isinstance(ap_object, list) == True: 
        
        if identifier != None: 
            metadata_df = ap_metadata.get_metadata(ap_object)
            id_idx = metadata_df.index.get_loc(identifier)

            time = ap_object[id_idx].time
            voltage = ap_object[id_idx].voltage
            stimulus = ap_object[id_idx].stimulus
            sample_rate_hz = ap_object[id_idx].metadata.sample_rate_hz
            start = (min(ap_object[id_idx].currentinj_start_end[0])/sample_rate_hz).values[0] # start time of stimulus
            end = (max(ap_object[id_idx].currentinj_start_end[0])/sample_rate_hz).values[0] # end time of stimulus
            currentstep = ap_object[id_idx].report_summary.current_analysed_sweep_pa.values[0] # current step
            max_firing_sweep = ap_object[id_idx].report_summary.sweep_number.values[0]
            max_firing_spike_features = ap_object[id_idx].spikes_features[ap_object[id_idx].spikes_features.sweep_number == max_firing_sweep]
            
        else: 
            raise SelectIdentifier("Parse an identifier")

    #-------------
    # figure plots
    ax[0].plot(time[max_firing_sweep], voltage[max_firing_sweep], color = 'k', linewidth=2)
    ax[1].plot(time[max_firing_sweep], stimulus[max_firing_sweep], color = 'k', linewidth=2) 

    # overlay features 
    if isinstance(show_ephys_features, str): # str input --> default to list
        show_ephys_features = [show_ephys_features]

    for feature in show_ephys_features: 

        marker_size = 100 # s

        # feature extract
        if feature == 'peak_v': 
            ax[0].scatter(max_firing_spike_features.loc[:,'peak_t'], max_firing_spike_features.loc[:,'peak_v'], s=marker_size , facecolors='none', edgecolors='k', label = 'ap peak')
        elif feature == 'threshold_v': 
            ax[0].scatter(max_firing_spike_features.loc[:,'threshold_t'], max_firing_spike_features.loc[:,'threshold_v'], s=marker_size , facecolors='none', edgecolors='royalblue', label = 'threshold')
        
        elif feature == 'trough_v': 
            ax[0].scatter(max_firing_spike_features.loc[:,'trough_t'], max_firing_spike_features.loc[:,'trough_v'], s=marker_size , facecolors='none', edgecolors='forestgreen', label = 'trough')
        elif feature == 'fast_trough_v': 
            ax[0].scatter(max_firing_spike_features.loc[:,'fast_trough_t'], max_firing_spike_features.loc[:,'fast_trough_v'], s=marker_size , facecolors='none', edgecolors='limegreen', label = 'fast trough')
        elif feature == 'slow_trough_v': 
            ax[0].scatter(max_firing_spike_features.loc[:,'slow_trough_t'], max_firing_spike_features.loc[:,'slow_trough_v'], s=marker_size , facecolors='none', edgecolors='tab:green', label = 'slow trough')
        
        elif feature == 'upstroke_v': 
            ax[0].scatter(max_firing_spike_features.loc[:,'upstroke_t'], max_firing_spike_features.loc[:,'upstroke_v'], s=marker_size , facecolors='none', edgecolors='tab:red', label = 'upstroke')
        elif feature == 'downstroke_v': 
            ax[0].scatter(max_firing_spike_features.loc[:,'downstroke_t'], max_firing_spike_features.loc[:,'downstroke_v'], s=marker_size , facecolors='none', edgecolors='navy', label = 'downstroke')
        else: 
            raise SelectEphysFeature("Select features of either: peak_v, threshold_v, trough_v, fast_trough_v, slow_trough_v, upstroke_v or downstroke_v")

    ax[0].legend(bbox_to_anchor=[1.2, 0.8], loc='center')

    #-------------
    # aesthetics subplot 1
    ax[0].set_ylim(ylim_v) # ylim change
    ax[0].set_xlim([start-0.4,end+0.4]) 
    ax[0].axis('off')
    
    # aesthetics subplot 2
    ax[1].set_ylim(ylim_stimulus) 
    ax[1].set_xlim([start-0.4,end+0.4]) 
    ax[1].grid()
    ax[1].axis('off')
    
    # horizontal lines
    ax[0].axhline(y=-60, color='k', linestyle='--', alpha=0.3)
    ax[0].axhline(y=0, color='k', linestyle='--', alpha=0.3)

    # subplot title
    if (identifier != None) and (isinstance(ap_object, list) == True): 
        ax[0].title.set_text(identifier)

    # text 
    ymin, ymax = ax[0].get_ylim()
    currentstep = str(currentstep) + ' pA' 
    ax[1].text(+0.61, -0.2, currentstep, verticalalignment='bottom', horizontalalignment='right', transform=ax[1].transAxes, color='k', fontsize=18) 
    ax[0].text(0, abs(ymin-(0))/(ymax-ymin)-0.038, '0 mV', verticalalignment='bottom', horizontalalignment='right', transform=ax[0].transAxes, color='darkgray', fontsize=18)
    ax[0].text(0, abs(ymin-(-60))/(ymax-ymin)-0.036, '-60 mV', verticalalignment='bottom', horizontalalignment='right', transform=ax[0].transAxes, color='darkgray', fontsize=18)

    # save out
    # auto_save == True must be selected for save function
    if (fname != None) and (identifier == None) and (auto_save == True):
        print(f'... saving | {fname}')
        create_path(fname)
        plt.savefig(fname, dpi = dpi, bbox_inches='tight')

    if (fname != None) and (identifier != None) and (auto_save == True):
        print(f'... saving | {fname}')
        create_path(fname)
        plt.savefig(fname, dpi = dpi, bbox_inches='tight')

    if (fname == None) and (identifier != None) and (auto_save == True):
        fname = 'figures/max_ap/' + str(identifier) + '.pdf' # create fname and save by default
        print(f'... saving | {fname}')
        create_path(fname)
        plt.savefig(fname, dpi = dpi, bbox_inches='tight')

    plt.show()


def maxfiring_phaseplot(ap_object, identifier = None, fname = None, ylim_v = [-80, 60], ylim_mv = [-200, 200], xlim_mv = [-80, 80], auto_save = True, dpi = 500): 
    """
    Plot phase plot for max ap on max firing sweep.
    
    
    Arguments
    ---------
    

    
    Returns
    -------
    
    
    """
    
    plt.style.use('brainspike/ap/util/plots/paper.mplstyle')
    fig, ax = plt.subplots(1,2, figsize=(7,3))
    
    if isinstance(ap_object, list) == False: 
        voltage = ap_object.voltage
        sample_rate_hz = ap_object.metadata.sample_rate_hz
        currentstep = ap_object.report_summary.current_analysed_sweep_pa.values[0] # current step
        max_firing_sweep = ap_object.report_summary.sweep_number.values[0]
        peak_t = ap_object.report_summary.peak_t.values[0] 

    elif isinstance(ap_object, list) == True: 
        
        if identifier != None: 
            metadata_df = ap_metadata.get_metadata(ap_object)
            id_idx = metadata_df.index.get_loc(identifier)

            voltage = ap_object[id_idx].voltage
            sample_rate_hz = ap_object[id_idx].metadata.sample_rate_hz
            currentstep = ap_object[id_idx].report_summary.current_analysed_sweep_pa.values[0] # current step
            peak_t = ap_object[id_idx].report_summary.peak_t.values[0] 
            max_firing_sweep = ap_object[id_idx].report_summary.sweep_number.values[0]

        else: 
            raise SelectIdentifier("Parse an identifier")
    
    hertz_ms = (sample_rate_hz/1000) # sampling rate (ms conversion)
    peak_v_slice = voltage[max_firing_sweep][(int(peak_t*sample_rate_hz)-8*int(hertz_ms[0])):(int(peak_t*sample_rate_hz)+10*int(hertz_ms[0]))] # -8/+ 10 ms slice around peak_v idx
    
    # calculate first derivative for phase plot
    peakv_deriv = np.diff(peak_v_slice) # derivative for each row / each trace
    peakv_deriv = peakv_deriv * hertz_ms[0] # scale to v/s (mV/ms) 

    # signal time arr
    signal_time = np.arange(-8,10,(1/sample_rate_hz[0])*1000) 

    # smooth deriv
    peakv_deriv_smoothed = gaussian_filter1d(peakv_deriv, sigma=2)

    #-----------------------------------------
    # subplot 1
    ax[0].plot(signal_time, peak_v_slice, linewidth=2, color = 'b')

    # aesthetics subplot 1
    ax[0].set_ylim(ylim_v) 
    ax[0].set_xlim([-8, 10]) # xlim change
    ax[0].grid()
    ax[0].axis('off')

    # scale bar subplot 1
    fontprops = fm.FontProperties(size=16)
    scalebar_x = AnchoredSizeBar(ax[0].transData, 2, "2 ms", 'upper right', frameon=False, size_vertical=0.5, pad=1, fontproperties=fontprops) # X-axis
    ax[0].add_artist(scalebar_x)

    # horizontal lines
    ax[0].axhline(y=-60, color='k', linestyle='--', alpha=0.3)
    ax[0].axhline(y=0, color='k', linestyle='--', alpha=0.3)

    # text subplot 1
    ymin, ymax = ax[0].get_ylim()
    currentstep = str(currentstep) + ' pA' 
    ax[0].text(0, abs(ymin-(0))/(ymax-ymin)-0.045, '0 mV', verticalalignment='bottom', horizontalalignment='right', transform=ax[0].transAxes, color='darkgray', fontsize=16)
    ax[0].text(0, abs(ymin-(-60))/(ymax-ymin)-0.053, '-60 mV', verticalalignment='bottom', horizontalalignment='right', transform=ax[0].transAxes, color='darkgray', fontsize=16)


    #-----------------------------------------
    # subplot 2
    ax[1].plot(peak_v_slice[1:], peakv_deriv_smoothed, linewidth=2, color = 'red')

    ax[1].set_ylim(ylim_mv) #Ylim change
    ax[1].set_xlim(xlim_mv) #Xlim change

    # move left y-axis and bottim x-axis to centre, passing through (0,0)
    ax[1].spines['left'].set_position('center')
    ax[1].spines['bottom'].set_position('center')

    # eliminate upper and right axes
    ax[1].spines['right'].set_color('none')
    ax[1].spines['top'].set_color('none')

    # show ticks in the left and lower axes only
    ax[1].xaxis.set_ticks_position('bottom')
    ax[1].yaxis.set_ticks_position('left')
    ax[1].yaxis.set_major_locator(MultipleLocator(400))  # For y-ticks   
    ax[1].yaxis.set_minor_locator(AutoMinorLocator())  
    ax[1].xaxis.set_major_locator(MultipleLocator(80))  # For x-ticks   
    ax[1].xaxis.set_minor_locator(AutoMinorLocator())  
    ax[1].set_xticks([xlim_mv[0], xlim_mv[1]]) # Removing tick labels
    ax[1].set_yticks([ylim_mv[0], ylim_mv[1]])

    # text subplot 2
    plt.figtext(+1, +0.55, 'Membrane \n potential (mV)' , ha="center", fontsize=16) # 0 mV
    plt.figtext(+0.86, +0.07, 'Δ Membrane \n potential (mV/ms)' , ha="center", fontsize=16) # 0 mV

    # save out
    # auto_save == True must be selected for save function
    if (fname != None) and (identifier == None) and (auto_save == True):
        print(f'... saving | {fname}')
        create_path(fname)
        plt.savefig(fname, dpi = dpi, bbox_inches='tight')

    if (fname != None) and (identifier != None) and (auto_save == True):
        print(f'... saving | {fname}')
        create_path(fname)
        plt.savefig(fname, dpi = dpi, bbox_inches='tight')

    if (fname == None) and (identifier != None) and (auto_save == True):
        fname = 'figures/max_phaseplot/' + str(identifier) + '.pdf' # create fname and save by default
        print(f'... saving | {fname}')
        create_path(fname)
        plt.savefig(fname, dpi = dpi, bbox_inches='tight')

    plt.show()


def ap(ap_object, sweep_number = None, identifier = None, fname = None, ylim_v = [-80, 60], ylim_stimulus = [0, 300], show_ephys_features = None, auto_save = True, dpi = 500): 
    """
    Plotting the max firing sweep for selected ap_object. 
    Highlights idx for peak v detection, thresholds.

    Option to plot by an identifier, or just by parsing in the ap_object. 
    Automatically provides the identifier id for plotting. 

    **to do --> make this an option to parse in a data object without identifier**

    Arguments
    ---------


    Returns
    -------


    """
    
    # figure
    plt.style.use('brainspike/ap/util/plots/paper.mplstyle')
    fig, ax = plt.subplots(2,1, figsize=(6,5), gridspec_kw={'height_ratios': [3.8, 1]})

    if identifier == None: 
        raise SelectIdentifier("Parse an identifier")
    if sweep_number == None: 
        raise SelectIdentifier("Parse a sweep number")
    
    if isinstance(ap_object, list) == True: 
        
        metadata_df = ap_metadata.get_metadata(ap_object)
        id_idx = metadata_df.index.get_loc(identifier)

        time = ap_object[id_idx].time
        voltage = ap_object[id_idx].voltage
        stimulus = ap_object[id_idx].stimulus
        sample_rate_hz = ap_object[id_idx].metadata.sample_rate_hz
        start = (min(ap_object[id_idx].currentinj_start_end[0])/sample_rate_hz).values[0] # start time of stimulus
        end = (max(ap_object[id_idx].currentinj_start_end[0])/sample_rate_hz).values[0] # end time of stimulus
        currentstep = (ap_object[id_idx].metadata.min_current_injected_pa.values[0]) + ((ap_object[id_idx].metadata.current_step_pa.values[0])*sweep_number) # current step
        spike_features = ap_object[id_idx].spikes_features[ap_object[id_idx].spikes_features.sweep_number == sweep_number]
    else: 
        raise DataTypeError("Parse list of ap_objects")

    #-------------
    # figure plots
    ax[0].plot(time[sweep_number], voltage[sweep_number], color = 'k', linewidth=2)
    ax[1].plot(time[sweep_number], stimulus[sweep_number], color = 'k', linewidth=2) 

    # overlay features 
    if isinstance(show_ephys_features, str): # str input --> default to list
        show_ephys_features = [show_ephys_features]

    for feature in show_ephys_features: 

        marker_size = 100 # s

        # feature extract
        if feature == 'peak_v': 
            ax[0].scatter(spike_features.loc[:,'peak_t'], spike_features.loc[:,'peak_v'], s=marker_size , facecolors='none', edgecolors='k', label = 'ap peak')
        elif feature == 'threshold_v': 
            ax[0].scatter(spike_features.loc[:,'threshold_t'], spike_features.loc[:,'threshold_v'], s=marker_size , facecolors='none', edgecolors='royalblue', label = 'threshold')
        
        elif feature == 'trough_v': 
            ax[0].scatter(spike_features.loc[:,'trough_t'], spike_features.loc[:,'trough_v'], s=marker_size , facecolors='none', edgecolors='forestgreen', label = 'trough')
        elif feature == 'fast_trough_v': 
            ax[0].scatter(spike_features.loc[:,'fast_trough_t'], spike_features.loc[:,'fast_trough_v'], s=marker_size , facecolors='none', edgecolors='limegreen', label = 'fast trough')
        elif feature == 'slow_trough_v': 
            ax[0].scatter(spike_features.loc[:,'slow_trough_t'], spike_features.loc[:,'slow_trough_v'], s=marker_size , facecolors='none', edgecolors='tab:green', label = 'slow trough')
        
        elif feature == 'upstroke_v': 
            ax[0].scatter(spike_features.loc[:,'upstroke_t'], spike_features.loc[:,'upstroke_v'], s=marker_size , facecolors='none', edgecolors='tab:red', label = 'upstroke')
        elif feature == 'downstroke_v': 
            ax[0].scatter(spike_features.loc[:,'downstroke_t'], spike_features.loc[:,'downstroke_v'], s=marker_size , facecolors='none', edgecolors='navy', label = 'downstroke')
        else: 
            raise SelectEphysFeature("select features of either: peak_v, threshold_v, trough_v, fast_trough_v, slow_trough_v, upstroke_v or downstroke_v")

    ax[0].legend(bbox_to_anchor=[1.2, 0.8], loc='center')

    #-------------
    # aesthetics subplot 1
    ax[0].set_ylim(ylim_v) # ylim change
    ax[0].set_xlim([start-0.4,end+0.4]) 
    ax[0].axis('off')
    
    # aesthetics subplot 2
    ax[1].set_ylim(ylim_stimulus) 
    ax[1].set_xlim([start-0.4,end+0.4]) 
    ax[1].grid()
    ax[1].axis('off')
    
    # horizontal lines
    ax[0].axhline(y=-60, color='k', linestyle='--', alpha=0.3)
    ax[0].axhline(y=0, color='k', linestyle='--', alpha=0.3)

    # subplot title
    if (identifier != None) and (isinstance(ap_object, list) == True): 
        ax[0].title.set_text(identifier)

    # text 
    ymin, ymax = ax[0].get_ylim()
    currentstep = str(currentstep) + ' pA' 
    ax[1].text(+0.61, -0.2, currentstep, verticalalignment='bottom', horizontalalignment='right', transform=ax[1].transAxes, color='k', fontsize=18) 
    ax[0].text(0, abs(ymin-(0))/(ymax-ymin)-0.038, '0 mV', verticalalignment='bottom', horizontalalignment='right', transform=ax[0].transAxes, color='darkgray', fontsize=18)
    ax[0].text(0, abs(ymin-(-60))/(ymax-ymin)-0.036, '-60 mV', verticalalignment='bottom', horizontalalignment='right', transform=ax[0].transAxes, color='darkgray', fontsize=18)

    # save out
    # auto_save == True must be selected for save function
    if (fname != None) and (identifier == None) and (auto_save == True):
        print(f'... saving | {fname}')
        create_path(fname)
        plt.savefig(fname, dpi = dpi, bbox_inches='tight')

    if (fname != None) and (identifier != None) and (auto_save == True):
        print(f'... saving | {fname}')
        create_path(fname)
        plt.savefig(fname, dpi = dpi, bbox_inches='tight')

    if (fname == None) and (identifier != None) and (auto_save == True):
        fname = 'figures/selected_ap/' + str(identifier) + "_sweep_number_" + str(sweep_number) + '.pdf' # create fname and save by default
        print(f'... saving | {fname}')
        create_path(fname)
        plt.savefig(fname, dpi = dpi, bbox_inches='tight')

    plt.show()


def phaseplot(ap_object, sweep_number = None, identifier = None, fname = None, ylim_v = [-80, 60], ylim_mv = [-200, 200], xlim_mv = [-80, 80], auto_save = True, dpi = 500): 
    """
    Plot phase plot for max ap on max firing sweep.
    
    
    Arguments
    ---------
    

    
    Returns
    -------
    
    
    """
    
    plt.style.use('brainspike/ap/util/plots/paper.mplstyle')
    fig, ax = plt.subplots(1,2, figsize=(7,3))

    if identifier == None: 
        raise SelectIdentifier("Parse an identifier")
    if sweep_number == None: 
        raise SelectIdentifier("Parse a sweep number")
    
    if isinstance(ap_object, list) == True: 
        
        metadata_df = ap_metadata.get_metadata(ap_object)
        id_idx = metadata_df.index.get_loc(identifier)

        voltage = ap_object[id_idx].voltage
        sample_rate_hz = ap_object[id_idx].metadata.sample_rate_hz
        currentstep = (ap_object[id_idx].metadata.min_current_injected_pa.values[0]) + ((ap_object[id_idx].metadata.current_step_pa.values[0])*sweep_number) # current step
        spike_features = ap_object[id_idx].spikes_features[ap_object[id_idx].spikes_features.sweep_number == sweep_number]
        
        if math.isnan(max(spike_features.peak_v)) == False: 
            peak_t = spike_features[spike_features.peak_v == max(spike_features.peak_v)].peak_t.values[0]
        else: 
            raise NoSpike(f'No spike detected for {identifier} sweep {sweep_number}')
    else: 
        raise DataTypeError("Parse list of ap_objects")
    
    hertz_ms = (sample_rate_hz/1000) # sampling rate (ms conversion)
    peak_v_slice = voltage[sweep_number][(int(peak_t*sample_rate_hz)-8*int(hertz_ms[0])):(int(peak_t*sample_rate_hz)+10*int(hertz_ms[0]))] # -8/+ 10 ms slice around peak_v idx
    
    # calculate first derivative for phase plot
    peakv_deriv = np.diff(peak_v_slice) # derivative for each row / each trace
    peakv_deriv = peakv_deriv * hertz_ms[0] # scale to v/s (mV/ms) 

    # signal time arr
    signal_time = np.arange(-8,10,(1/sample_rate_hz[0])*1000) 

    # smooth deriv
    peakv_deriv_smoothed = gaussian_filter1d(peakv_deriv, sigma=2)

    #-----------------------------------------
    # subplot 1
    ax[0].plot(signal_time, peak_v_slice, linewidth=2, color = 'b')

    # aesthetics subplot 1
    ax[0].set_ylim(ylim_v) 
    ax[0].set_xlim([-8, 10]) # xlim change
    ax[0].grid()
    ax[0].axis('off')

    # scale bar subplot 1
    fontprops = fm.FontProperties(size=16)
    scalebar_x = AnchoredSizeBar(ax[0].transData, 2, "2 ms", 'upper right', frameon=False, size_vertical=0.5, pad=1, fontproperties=fontprops) # X-axis
    ax[0].add_artist(scalebar_x)

    # horizontal lines
    ax[0].axhline(y=-60, color='k', linestyle='--', alpha=0.3)
    ax[0].axhline(y=0, color='k', linestyle='--', alpha=0.3)

    # text subplot 1
    ymin, ymax = ax[0].get_ylim()
    currentstep = str(currentstep) + ' pA' 
    ax[0].text(0, abs(ymin-(0))/(ymax-ymin)-0.045, '0 mV', verticalalignment='bottom', horizontalalignment='right', transform=ax[0].transAxes, color='darkgray', fontsize=16)
    ax[0].text(0, abs(ymin-(-60))/(ymax-ymin)-0.053, '-60 mV', verticalalignment='bottom', horizontalalignment='right', transform=ax[0].transAxes, color='darkgray', fontsize=16)

    #-----------------------------------------
    # subplot 2
    ax[1].plot(peak_v_slice[1:], peakv_deriv_smoothed, linewidth=2, color = 'red')

    ax[1].set_ylim(ylim_mv) #Ylim change
    ax[1].set_xlim(xlim_mv) #Xlim change

    # move left y-axis and bottim x-axis to centre, passing through (0,0)
    ax[1].spines['left'].set_position('center')
    ax[1].spines['bottom'].set_position('center')

    # eliminate upper and right axes
    ax[1].spines['right'].set_color('none')
    ax[1].spines['top'].set_color('none')

    # show ticks in the left and lower axes only
    ax[1].xaxis.set_ticks_position('bottom')
    ax[1].yaxis.set_ticks_position('left')
    ax[1].yaxis.set_major_locator(MultipleLocator(400))  # For y-ticks   
    ax[1].yaxis.set_minor_locator(AutoMinorLocator())  
    ax[1].xaxis.set_major_locator(MultipleLocator(80))  # For x-ticks   
    ax[1].xaxis.set_minor_locator(AutoMinorLocator())  
    ax[1].set_xticks([xlim_mv[0], xlim_mv[1]]) # Removing tick labels
    ax[1].set_yticks([ylim_mv[0], ylim_mv[1]])

    # text subplot 2
    plt.figtext(+1, +0.55, 'Membrane \n potential (mV)' , ha="center", fontsize=16) # 0 mV
    plt.figtext(+0.86, +0.07, 'Δ Membrane \n potential (mV/ms)' , ha="center", fontsize=16) # 0 mV

    # save out
    # auto_save == True must be selected for save function
    if (fname != None) and (identifier == None) and (auto_save == True):
        print(f'... saving | {fname}')
        create_path(fname)
        plt.savefig(fname, dpi = dpi, bbox_inches='tight')

    if (fname != None) and (identifier != None) and (auto_save == True):
        print(f'... saving | {fname}')
        create_path(fname)
        plt.savefig(fname, dpi = dpi, bbox_inches='tight')

    if (fname == None) and (identifier != None) and (auto_save == True):
        fname = 'figures/phaseplot/' + str(identifier) + "_sweep_" + str(sweep_number) + '.pdf' # create fname and save by default
        print(f'... saving | {fname}')
        create_path(fname)
        plt.savefig(fname, dpi = dpi, bbox_inches='tight')

    plt.show()


def ap_allsweeps(ap_object, identifier = None, fname = None, dpi = 500, auto_save = True): 
    """
    Plot evoked aps across all sweeps. 
    """

    if isinstance(ap_object, list) == False: 
        time = ap_object.time
        voltage = ap_object.voltage
        sample_rate_hz = ap_object.metadata.sample_rate_hz
        start = (min(ap_object.currentinj_start_end[0])/sample_rate_hz).values[0] - 0.2 # start time of stimulus
        end = (max(ap_object.currentinj_start_end[0])/sample_rate_hz).values[0] + 0.4 # end time of stimulus
        max_firing_sweep = ap_object.report_summary.sweep_number.values[0]

    elif isinstance(ap_object, list) == True: 
        
        if identifier != None: 
            metadata_df = ap_metadata.get_metadata(ap_object)
            id_idx = metadata_df.index.get_loc(identifier)

            time = ap_object[id_idx].time
            voltage = ap_object[id_idx].voltage
            sample_rate_hz = ap_object[id_idx].metadata.sample_rate_hz
            start = (min(ap_object[id_idx].currentinj_start_end[0])/sample_rate_hz).values[0] - 0.2 # start time of stimulus
            end = (max(ap_object[id_idx].currentinj_start_end[0])/sample_rate_hz).values[0] + 0.4 # end time of stimulus
            max_firing_sweep = ap_object[id_idx].report_summary.sweep_number.values[0]

        else: 
            raise SelectIdentifier("Parse an identifier")

    # figure plots
    plt.style.use('brainspike/ap/util/plots/paper.mplstyle')
    plt.figure(figsize=(8, 5))

    for sweep_number in range(len(voltage)):
        plt.plot(time[sweep_number][int(start*sample_rate_hz):int(end*sample_rate_hz)] + (.25) * sweep_number, voltage[sweep_number][int(start*sample_rate_hz):int(end*sample_rate_hz)] + 15 * sweep_number, color='lightgray', lw = 1)
        
        if sweep_number == max_firing_sweep: 
            plt.plot(time[sweep_number][int(start*sample_rate_hz):int(end*sample_rate_hz)] + (.25) * sweep_number, voltage[sweep_number][int(start*sample_rate_hz):int(end*sample_rate_hz)] + 15 * sweep_number, color='royalblue', lw = 1.2)

    plt.gca().axis('off') 

    # save out
    # auto_save == True must be selected for save function
    if (fname != None) and (identifier == None) and (auto_save == True):
        print(f'... saving | {fname}')
        create_path(fname)
        plt.savefig(fname, dpi = dpi, bbox_inches='tight')

    if (fname != None) and (identifier != None) and (auto_save == True):
        print(f'... saving | {fname}')
        create_path(fname)
        plt.savefig(fname, dpi = dpi, bbox_inches='tight')

    if (fname == None) and (identifier != None) and (auto_save == True):
        fname = 'figures/ap_allsweeps/' + str(identifier) + '.pdf' # create fname and save by default
        print(f'... saving | {fname}')
        create_path(fname)
        plt.savefig(fname, dpi = dpi, bbox_inches='tight')

    plt.show()


def i_f(ap_object, identifier = None, fname = None, dpi = 500, auto_save = True): 
    """
    Plot relationship between current injection
    and firing frequency (Hz). 
    """

    plt.style.use('brainspike/ap/util/plots/paper.mplstyle')
    fig, ax = plt.subplots(1,1, figsize=(7,5))

    if identifier == None: 
        raise SelectIdentifier("Parse an identifier")
    
    if isinstance(ap_object, list) == True: 
        
        metadata_df = ap_metadata.get_metadata(ap_object)
        id_idx = metadata_df.index.get_loc(identifier)

        current_steps = ap_object[id_idx].sweeps_features.current_analysed_sweep_pa.values
        avg_rates = ap_object[id_idx].sweeps_features.avg_rate.values
        rheobase = ap_object[id_idx].report_summary.rheobase_pa.values[0]
        max_firing_rate_current = ap_object[id_idx].report_summary.current_analysed_sweep_pa.values[0]

    else: 
        raise DataTypeError("Parse list of ap_objects")

    # figure plot
    ax.plot(current_steps, avg_rates, lw = 2., color = 'black', alpha = 1)

    # highlight idx for rheobase and max ap selected
    idx_max_firing_current = np.where(current_steps == max_firing_rate_current)
    idx_rheobase_current = np.where(current_steps == rheobase)
    ax.scatter(max_firing_rate_current, avg_rates[idx_max_firing_current], s=180, facecolors='none', edgecolors='royalblue', label = 'max firing ap')
    ax.scatter(rheobase, avg_rates[idx_rheobase_current], s=180, facecolors='none', edgecolors='orange', label = 'rheobase')

    # legend
    ax.legend(frameon = False, loc = 2, bbox_to_anchor=(1., 0.8, 0.3, 0.2))

    # labels
    ax.set_xlabel('Current (pA)')
    ax.set_ylabel('Firing frequency (Hz)')

    # minor tick adjustments
    y_minor_locator = AutoMinorLocator(5)
    x_minor_locator = AutoMinorLocator(5)
    ax.xaxis.set_minor_locator(x_minor_locator)
    ax.yaxis.set_minor_locator(y_minor_locator)

    # save out
    # auto_save == True must be selected for save function
    if (fname != None) and (identifier == None) and (auto_save == True):
        print(f'... saving | {fname}')
        create_path(fname)
        plt.savefig(fname, dpi = dpi, bbox_inches='tight')

    if (fname != None) and (identifier != None) and (auto_save == True):
        print(f'... saving | {fname}')
        create_path(fname)
        plt.savefig(fname, dpi = dpi, bbox_inches='tight')

    if (fname == None) and (identifier != None) and (auto_save == True):
        fname = 'figures/i_f/' + str(identifier) + '.pdf' # create fname and save by default
        print(f'... saving | {fname}')
        create_path(fname)
        plt.savefig(fname, dpi = dpi, bbox_inches='tight')

    plt.show()

    plt.show()


# ----------------

def moving_average(x, w):

    return np.convolve(x, np.ones(w), 'same') / w # same


def smooth_data(data): 
    
    smooth_data = moving_average(data, 2) # window 2
    smooth_data = np.insert(smooth_data, 0, 0) # default to zero
        
    return smooth_data 

# ----------------

def create_path(fname): 
    """

    Get file name from path. Create path if it does not exist.

    Arguments
    ---------


    Returns
    -------
    
    
    """

    # find file name search for file path
    filename_idx = (fname.rfind('/'))
    if filename_idx: 

        isExist = os.path.exists(fname[:filename_idx]) 
        if not isExist:
            os.makedirs(fname[:filename_idx])
            print(f"The new directory is created for {fname}")



