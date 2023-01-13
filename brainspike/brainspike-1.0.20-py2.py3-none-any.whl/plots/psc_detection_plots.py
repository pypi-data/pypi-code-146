"""
detection_plots.py

Modules for visualizing detected
PSC events. 

"""

import os 

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

###################################################################################################
###################################################################################################

def psc_detect_fig(sweepdata = None, event_times = None, burst_num = None, srate = None):
    """ detected PSC event """

    pstart = event_times[:,0]
    pend = event_times[:,1]
    
    bstart = pstart[burst_num] # isolate selected event time
    bend = pend[burst_num] 
    
    #--------
    pstart_plot = bstart - (0.1*srate) # 10 ms window around bstart and bend
    pend_plot = bend + (0.1*srate)

    print(f'start {bstart/srate} seconds | end {bend/srate} seconds')

    plt.style.use(os.path.join(os.path.dirname(__file__),'..','utils/plots/paper.mplstyle'))
    fig, ax = plt.subplots(1, 1, figsize=(10, 4))

    times = np.arange(0, len(sweepdata), 1)/srate
    ax.plot(times[int(pstart_plot):int(pend_plot)], abs(sweepdata[int(pstart_plot):int(pend_plot)]))

    # shaded box to outline start and end detection times
    trans = matplotlib.transforms.blended_transform_factory(ax.transData, fig.transFigure)
    rect = mpatches.Rectangle(xy=(bstart/srate,0.11), width=(bend-bstart)/srate, height=0.77, transform=trans, ec='black', fc='orange', alpha=0.1, lw = 2, clip_on=False)
    fig.add_artist(rect)

    # aesthetics
    ax.set_ylabel('Current (pA)')
    ax.set_xlabel('Time (s)')
    y_minor_locator = AutoMinorLocator(5)
    x_minor_locator = AutoMinorLocator(10)
    ax.xaxis.set_minor_locator(x_minor_locator)
    ax.yaxis.set_minor_locator(y_minor_locator)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_title(f'PSC event #: {burst_num}')

    plt.show()