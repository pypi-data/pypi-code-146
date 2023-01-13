"""
preprocessing_plots.py

Modules for visualising pre-processing 
steps for PSC recording. 

"""

import os 

import math 

import numpy as np 

import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.font_manager as font_manager
from matplotlib.ticker import AutoMinorLocator
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import matplotlib

from ..abf.abf_obj import ABF

###################################################################################################
###################################################################################################

def psc_preprocesing_fig(data_obj, xlim = [None, None], ylim = [None, None]):
    """ pre-processing figure """
    
    if isinstance(data_obj, ABF): 
        
        try: 
            
            data_obj.preprocessed_params
            
            original_data = data_obj.sweepdata[0]
            preprocessed_data = data_obj.preprocessed_sweepdata[0]
            srate = data_obj.metadata['sample_rate_hz']
            
            # note: plotting to only be conducted on
            # recordings from voltage clamp 
            # hence, no multidimensional arrays
            if len(data_obj.sweepdata) == 1: 
                pass
            else: 
                raise ValueError("voltage clamp recordings to only be used"
                                f"for psc preprocessing figure | {data_obj.sweepdata} sweepdata found ...")
            
        except AttributeError: 
            print("no preprocessing conducted on the data obj ...")
        
    else: 
        raise TypeError("pass the data object for a single file ...")

    plt.style.use(os.path.join(os.path.dirname(__file__),'..','utils/plots/paper.mplstyle'))
    fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex = True, sharey = True)
    
    try: 
        
        ax[0].plot(np.arange(0, len(original_data), 1)/srate, original_data, color = 'black', label = 'original')
        ax[1].plot(np.arange(0, len(preprocessed_data), 1)/srate, preprocessed_data, color = 'royalblue', label = 'preprocessed')
        
        # axes + labels + titles
        for i in range(2):
            ax[i].set_ylabel('Current (pA)')
            
            ax[i].legend(loc = 'upper left', bbox_to_anchor=[0, 1.1])
            
            ax[i].set_xlim(xlim) # xlim 
            ax[i].set_ylim(ylim) # ylim
            
        ax[1].set_xlabel('Time (sec.)')

        plt.show()
    
    except UnboundLocalError: 
        print("no preprocessing conducted on the data obj ...")
        
    
def psc_baselinesub_fig(data_obj, xlim = [None, None], ylim = [None, None]):
    """ baseline subtract figure """
    
    if isinstance(data_obj, ABF): 
        
        try: 
            
            data_obj.preprocessed_params['baseline_subtract']
            
            original_data = data_obj.sweepdata[0]
            preprocessed_data = data_obj.preprocessed_sweepdata[0]
            baselinecorr_data = data_obj.baselinecorr_sweepdata[0]
            
            srate = data_obj.metadata['sample_rate_hz']
            
            # note: plotting to only be conducted on
            # recordings from voltage clamp 
            # hence, no multidimensional arrays
            if len(data_obj.sweepdata) == 1: 
                pass
            else: 
                raise ValueError("voltage clamp recordings to only be used"
                                f"for baseline subtraction figure | {data_obj.sweepdata} sweepdata found ...")
            
        except AttributeError: 
            raise KeyError(print("no baseline subtraction found ..."))
        
    else: 
        raise TypeError("pass the data object for a single file ...")
    
    try: 
        plt.style.use(os.path.join(os.path.dirname(__file__),'..','utils/plots/paper.mplstyle'))
        fig, ax = plt.subplots(3, 1, figsize=(10, 10), sharex = True, sharey = True)
        
        ax[0].plot(np.arange(0, len(original_data), 1)/srate, original_data, color = 'black', label = 'original')
        ax[1].plot(np.arange(0, len(preprocessed_data), 1)/srate, preprocessed_data, color = 'royalblue', label = 'preprocessed')
        ax[2].plot(np.arange(0, len(baselinecorr_data), 1)/srate, baselinecorr_data, color = 'tab:red', label = 'preprocessed + baseline subtraction')
        
        # axes 
        for i in range(3): 
            ax[i].axhline(y = 0, ls = '--', color = 'darkgray', lw = 1.5)
            ax[i].set_ylabel('Current (pA)')
            ax[i].legend(loc = 'upper left', bbox_to_anchor=[0, 1.2])  
            ax[i].set_xlim(xlim) 
            ax[i].set_ylim(ylim) 
            
        ax[2].set_xlabel('Time (sec.)')

        plt.show()
    
    except UnboundLocalError: 
        print("no baseline subtraction found ...")
    
    
def psc_sigdrop_fig(data_obj, xlim = [None, None], ylim = [None, None]):
    """ signal drop loc figure """
    
    if isinstance(data_obj, ABF): 
        
        try: 
            
            signal_drop_time = data_obj.preprocessed_params['signal_drop_time']
            
            if math.isnan(signal_drop_time): 
                raise KeyError('no signal drop time found | select a new data object ...')
            
            baselinecorr_dropped_data = data_obj.baselinecorr_sweepdata_dropped[0]
            baselinecorr_data = data_obj.baselinecorr_sweepdata[0]
            
            thresh = data_obj.preprocessed_params['signal_drop_thresh']
            srate = data_obj.metadata['sample_rate_hz']
            
            # note: plotting to only be conducted on
            # recordings from voltage clamp 
            # hence, no multidimensional arrays
            #---------------------------------------
            
            if len(data_obj.baselinecorr_sweepdata) == 1: 
                pass
            else: 
                raise ValueError("voltage clamp recordings to only be used"
                                f"for signal drop figure | {data_obj.baselinecorr_sweepdata}"
                                "baseline corrected sweepdata found ...")
            
        except KeyError or AttributeError: 
            print("no signal drop time found ...")
        
    else: 
        raise TypeError("pass the data object for a single file ...")
    
    plt.style.use(os.path.join(os.path.dirname(__file__),'..','utils/plots/paper.mplstyle'))
    fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex = True, sharey = True)

    ax[0].plot(np.arange(0, len(baselinecorr_data), 1)/srate, baselinecorr_data, color = 'tab:red', label = 'preprocessed + baseline subtraction')
    ax[1].plot(np.arange(0, len(baselinecorr_dropped_data), 1)/srate, baselinecorr_dropped_data, color = 'navy', label = 'dropped signal')
    
    # shaded box
    trans = matplotlib.transforms.blended_transform_factory(ax[0].transData, fig.transFigure)
    rect=mpatches.Rectangle(xy=(signal_drop_time,0.12), width=(len(baselinecorr_data)/srate)-signal_drop_time,\
        height=0.74, transform=trans, ec='black', fc='orange', alpha=0.1, lw = 1, linestyle = '--', clip_on=False)
    fig.add_artist(rect)
    
    # axes 
    for i in range(2): 
        ax[i].set_ylabel('Current (pA)')
        ax[i].axhline(y = thresh, ls = '--', color = 'darkgray', lw = 2) # label = 'thresh'
        ax[i].legend(loc = 'upper left', bbox_to_anchor=[0, 1.2])  
        ax[i].set_xlim(xlim) 
        ax[i].set_ylim(ylim) 
        
    ax[1].set_xlabel('Time (sec.)')

    plt.show()
        
        
def psc_straightened_fig(data_obj, xlim = [None, None], ylim = [None, None]): 
    """ straightened signal figure """
    
    if isinstance(data_obj, ABF): 
        
        try: 
            
            data_obj.preprocessed_params['straightening_time_segment']
            srate = data_obj.metadata['sample_rate_hz']
            
            try: 
                straightened_data = data_obj.straightened_sweepdata[0]
                baselinecorr_data = data_obj.baselinecorr_sweepdata_dropped[0]
                color_baselinecorr = 'navy'
                
            except AttributeError: 
                straightened_data = data_obj.straightened_sweepdata[0]
                baselinecorr_data = data_obj.baselinecorr_sweepdata[0]
                color_baselinecorr = 'tab:red'
                
            except KeyError: 
                print('no dropped signal found | defaulting to baseline corrected ...')
                straightened_data = data_obj.baselinecorr_sweepdata[0]
                baselinecorr_data = data_obj.straightened_sweepdata[0]
                color_baselinecorr = 'tab:red'
                
            except: 
                raise ValueError('no baseline & straightened corrected signals found ...')
                
        except: 
            raise ValueError("no straightened data found ...")
        
    else: 
        raise TypeError("pass the data object for a single file ...")
    
    plt.style.use(os.path.join(os.path.dirname(__file__),'..','utils/plots/paper.mplstyle'))  
    fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex = True, sharey = True)
    
    try: 
        ax[0].plot(np.arange(0, len(baselinecorr_data), 1)/srate, baselinecorr_data, color = color_baselinecorr, label = 'pre-')
        ax[1].plot(np.arange(0, len(straightened_data), 1)/srate, straightened_data, color = 'orange', label = 'post-straighten')
        
        # axes 
        for i in range(2): 
            ax[i].set_ylabel('Current (pA)')
            ax[i].legend(loc = 'upper left', bbox_to_anchor=[0, 1.2])  
            ax[i].set_xlim(xlim) 
            ax[i].set_ylim(ylim) 
            
        ax[1].set_xlabel('Time (sec.)')
        
        plt.show()
        
    except UnboundLocalError: 
        print("no straightened data found ...")