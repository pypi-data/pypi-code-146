"""
subthreshold_qc_plots.py

Modules for sanity checks 
of subthreshold processing 

"""

import os 

import numpy as np 

import matplotlib.pyplot as plt
from matplotlib import style

from ..utils.plots.save import (create_path)

cwd = os.getcwd()

###################################################################################################
###################################################################################################

def ri_plot(v_peak = None, i = None, figdir = None, figname = None, figextension = None, **linregress_dict): 
    """ sanity check plot :: input resistance """
    
    plt.style.use(os.path.join(cwd,'brainspike/utils/plots/paper.mplstyle'))
    fig, ax = plt.subplots(1,1, figsize = (5,5))
    
    ax.scatter(i, v_peak, color = 'royalblue')
    
    ax.set_ylabel('Voltage deflection (mV)')
    ax.set_xlabel('Current (pA)')
    
    r2 = linregress_dict['r2_value']
    if r2 != np.nan: 
        ax.axline(xy1=(0,linregress_dict['intercept']),\
            slope = linregress_dict['slope'], label=f'r\u00b2 = {round(r2,3)}',\
                color = 'tab:red', ls = '--')
        
        ax.legend(loc="upper left")
    
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
    
    plt.show()