"""
subthreshold_plots.py

Modules for plotting subthreshold
features and sweepdata. 

"""

import os 

import numpy as np 

import matplotlib.pyplot as plt
from matplotlib import style

from ..utils.plots.save import (create_path)

cwd = os.getcwd()

###################################################################################################
###################################################################################################

def sag_plot(t = None, i = None, v = None, sweeps = None, xlim = None, ylim_v = None,\
            ylim_i = None, stable_sweeps = None, deflect_idx = None, scale_bar = True, axis = False,\
            start = None, end = None, figdir = None, figname = None, figextension = None): 
    """ plot sag features for selected sweeps """
    
    if (sweeps, list): 
        pass
    else: 
        raise TypeError('pass sweep values as a list ...')
    
    plt.style.use(os.path.join(cwd,'brainspike/utils/plots/paper.mplstyle'))
    fig, ax = plt.subplots(2,1, figsize=(6,5), gridspec_kw={'height_ratios': [4, 1]}, sharex = True)
    
    # selected sweeps 
    if sweeps is not None:
        for count, sweep in enumerate(sweeps): 
            ax[0].plot(t[sweep], v[sweep], color = 'k')
            ax[1].plot(t[sweep], i[sweep], color = 'k')
            if (deflect_idx is not None) and (deflect_idx[count] is not None): # show deflect idx 
                ax[0].scatter(t[sweep][deflect_idx[count]], v[sweep][deflect_idx[count]], s = 60, color = 'orange')
        
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
            
    # axis labels
    ax[0].set_ylabel('Voltage (mV)')
    ax[1].set_ylabel('Current (pA)')
    ax[1].set_xlabel('Time (sec.)')
    
    # lims 
    ax[1].set_xlim(xlim)
    ax[0].set_ylim(ylim_v)
    ax[1].set_ylim(ylim_i)
    
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
    elif i_min < 0: 
        currentstep = i_min 
    else: 
        currentstep = 0 
        
    label = str(currentstep) + ' pA'

    if len(label) > 8: # adjust xpos for label 
        xpos = 0.2
    elif len(label) == 8: 
        xpos = 0.16
    elif len(label) < 8: 
        xpos = 0.12
        
    ax[1].text((start + (end - start)/2) - xpos, ylim_i[0]-20, label, color='k', fontsize=18) 
    
    # scale bar
    if scale_bar: 
        ymin, ymax = ax[0].get_ylim(); xmin, xmax = ax[0].get_xlim() 
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
