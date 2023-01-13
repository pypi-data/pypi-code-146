"""
spiketrain_plots.py

Modules for plotting pike train features and sweepdata. 

"""

import os 

import numpy as np 

import matplotlib.pyplot as plt
from matplotlib import style

from ..utils.plots.save import (create_path)

###################################################################################################
###################################################################################################

def spiketrain_plot(t = None, i = None, v = None, sweeps = None, xlim = None, ylim_v = None,\
            ylim_i = None, stable_sweeps = None, scale_bar = True, axis = False, start = 0, end = 2.5,\
            features_info = None, min_peak = 0, figdir = None,\
            figname = None, figextension = None): 
    """ plot sag features for selected sweeps """
    
    if (sweeps, list): 
        pass
    else: 
        raise TypeError('pass sweep values as a list ...')
    
    plt.style.use(os.path.join(os.path.dirname(__file__),'..','utils/plots/paper.mplstyle'))
    fig, ax = plt.subplots(2,1, figsize=(6,5), gridspec_kw={'height_ratios': [4, 1]}, sharex = True)
    
    # selected sweeps 
    if sweeps is not None:        
        for count, sweep in enumerate(sweeps): 
            ax[0].plot(t[sweep], v[sweep], color = 'k')
            ax[1].plot(t[sweep], i[sweep], color = 'k')

            if (features_info is not None): # + features 
                for feature_sweep, feature_idx, feature_color, feature_label in zip(features_info[:,0],\
                                                                                    features_info[:,1],\
                                                                                    features_info[:,2],\
                                                                                    features_info[:,3]): 
                    if sweep == int(feature_sweep):
                        ax[0].scatter(t[sweep][int(feature_idx)], v[sweep][int(feature_idx)], s = 60,\
                                        color = feature_color, label = feature_label[:-6])
                    else: 
                        pass 
            else: 
                pass 

    # stable sweeps vs unstable
    if stable_sweeps is not None: 
        for sweep in range(len(v)): 
            ax[0].plot(t[sweep], v[sweep], color = 'tab:red', lw = 1.5)
            ax[1].plot(t[sweep], i[sweep], color = 'tab:red', lw = 1.5)
            
        for stable_sweep in stable_sweeps: 
            ax[0].plot(t[stable_sweep], v[stable_sweep], color = 'royalblue')
            ax[1].plot(t[stable_sweep], i[stable_sweep], color = 'royalblue')
    else: 
        pass 
    
    # lims 
    ax[1].set_xlim(xlim)
    ax[0].set_ylim(ylim_v)
    ax[1].set_ylim(ylim_i)
    
    # threshold lims 
    ymin, ymax = ax[0].get_ylim(); xmin, xmax = ax[0].get_xlim() 
    ax[0].axhline(y=min_peak, color='k', linestyle='--', alpha=0.3)
    ax[0].axhline(y=-60, color='k', linestyle='--', alpha=0.3)
    ax[0].text(0, abs(ymin-(min_peak))/(ymax-ymin)-0.04, str(int(min_peak)) + ' mV',\
                    verticalalignment='bottom', horizontalalignment='right', transform=ax[0].transAxes, color='darkgray')
    ax[0].text(0, abs(ymin-(-60))/(ymax-ymin)-0.0385, '-60 mV', verticalalignment='bottom',\
                    horizontalalignment='right', transform=ax[0].transAxes, color='darkgray')
    
    # legend for feature info 
    if features_info is not None: 
        ax[0].legend(*[*zip(*{l:h for h,l in zip(*ax[0].get_legend_handles_labels())}.items())][::-1], bbox_to_anchor=[1.1, 0.5])
            
    # axis labels
    ax[0].set_ylabel('Voltage (mV)')
    ax[1].set_ylabel('Current (pA)')
    ax[1].set_xlabel('Time (sec.)')
    
    # axes
    if axis is False: 
        ax[0].axis('off')
        ax[1].axis('off')
    else: 
        pass 
    
    # current step + label 
    i_min = np.min(np.array(i).take(sweeps, axis = 0))
    i_max = np.max(np.array(i).take(sweeps, axis = 0))
    
    if i_min == 0: 
        currentstep = i_max 
        ylim_pos = ylim_i[1]+20
    elif i_min < 0: 
        currentstep = i_min 
        ylim_pos = ylim_i[0]-20
    else: 
        currentstep = 0 
        ylim_pos = -20
        
    label = str(currentstep) + ' pA'

    if len(label) > 9: # adjust xpos for label 
        xpos = 0.2
    elif len(label) == 9: 
        xpos = 0.18
    elif len(label) == 8: 
        xpos = 0.165
    elif len(label) < 8: 
        xpos = 0.12
        
    ax[1].text((start + (end - start)/2) - xpos, ylim_pos, label, color='k', fontsize=18) 
    
    # scale bar
    if scale_bar:
        ax[0].vlines(x = xmax-0.1, ymin = ymax, ymax = ymax-20, color='black', lw = 1.5) # 20 mV 
        ax[0].hlines(y = ymax-20, xmin = xmax-0.35, xmax = xmax-0.1, color='black', lw = 1.5) # 250 millisec. 
        
        ax[0].text(xmax-0.05, ymax-14, '20 mV', color='black') 
        ax[0].text(xmax-0.35, ymax-34, '250 ms', color='black') 
    else: 
        pass 

    plt.subplots_adjust(wspace=0, hspace=0) # reduce subplot gaps
    
    # save 
    #------
    if None not in [figdir, figname, figextension]: 
        if (figextension == '.png') | (figextension == '.pdf'):
            fname = create_path(figdir, figname, figextension)
            print(f"saving plt to {fname} ...")
            plt.savefig(fname, dpi = 300, bbox_inches="tight")   
            plt.show()
        else: 
            raise TypeError('file extension option are only .pdf or .png ...')
    else: 
        plt.show()
        
        
def i_f_plot(i = None, f = None, rheobase = None, max_firing = None, figdir = None,\
            figname = None, figextension = None): 
    """ current vs frequency relationship plot w/ rheobase & max firing sweep """
    
    plt.style.use(os.path.join(os.path.dirname(__file__),'..','utils/plots/paper.mplstyle'))
    fig, ax = plt.subplots(1,1, figsize=(6,5))
    
    # i vs f 
    ax.plot(i,f, color = 'royalblue')
    ax.scatter(i,f, s = 60, color = 'royalblue')
    
    # + rheobase 
    rheobase_idx = np.where(i == rheobase)
    ax.scatter(i[rheobase_idx[0]], f[rheobase_idx[0]], s = 90, color = 'tab:red', label = 'rheobase')
    
    # + max firing sweep 
    max_firing_idx = np.where(f == max_firing)
    if max_firing_idx[0].size > 1: 
        max_firing_idx = max_firing_idx[0][0] # firing rate the same :: default to 1st index
    else: 
        max_firing_idx = max_firing_idx[0]
        
    ax.scatter(i[max_firing_idx], f[max_firing_idx], s = 90, color = 'black', label = 'max firing')
    
    # legend
    ax.legend(bbox_to_anchor=[1.1, 1.0])

    # axis labels
    ax.set_ylabel('Firing frequency (Hz)')
    ax.set_xlabel('Current (pA)')
    
    # save 
    #------
    if None not in [figdir, figname, figextension]: 
        if (figextension == '.png') | (figextension == '.pdf'):
            fname = create_path(figdir, figname, figextension)
            print(f"saving plt to {fname} ...")
            plt.savefig(fname, dpi = 300, bbox_inches="tight")   
            plt.show()
        else: 
            raise TypeError('file extension option are only .pdf or .png ...')
    else: 
        plt.show()