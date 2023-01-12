

#set up matplotlib defaults
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from whacc import utils
import matplotlib as mpl

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Arial'


# selecting colors
cmap_col = 'inferno'
# cmap_col = 'viridis'
plot_it = False
color_list = np.arange(30)
color_list = color_list/np.max(color_list)
cmap = cm.get_cmap(cmap_col)
color_dict = dict()
# plt.grid()
for i, k1 in enumerate(color_list):
    color_dict[i] = np.asarray(cmap(k1)[:-1])
    if plot_it:
        plt.plot(i, i, '.', color=color_dict[i])

## colors and axes

CB91_Blue = '#2CBDFE'
CB91_Green = '#47DBCD'
CB91_Pink = '#F3A0F2'
CB91_Purple = '#9D2EC5'
CB91_Violet = '#661D98'
CB91_Amber = '#F5B14C'

color_list_tmp = [CB91_Blue, CB91_Pink, CB91_Green, CB91_Amber, CB91_Purple, CB91_Violet]
color_list = []
for k in color_list_tmp:
    color_list.append(utils.hex_to_rgb(k))
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list_tmp)
"""
https://matplotlib.org/stable/tutorials/introductory/customizing.html
"""
import seaborn as sns
sns.set_theme(rc={
 'font.size': 14,
 'axes.labelsize': 14,
 'axes.titlesize': 20,
 'xtick.labelsize': 14,
 'ytick.labelsize': 14,
 'legend.fontsize': 14,
 'legend.title_fontsize': 14,
 'axes.axisbelow': False,
 'axes.edgecolor': 'k',#'lightgrey',
 'axes.facecolor': 'None',
 'axes.grid': False,
 'axes.labelcolor': 'k',#'dimgrey',
 'axes.spines.right': False,
 'axes.spines.top': False,
 'figure.facecolor': 'None',
 'lines.solid_capstyle': 'round',
 'patch.edgecolor': 'w',
 'patch.force_edgecolor': True,
 'text.color': 'k',#'dimgrey',
 'xtick.bottom': True,
 'xtick.color': 'k',#'dimgrey',
 'xtick.direction': 'out',
 'xtick.top': False,
 'ytick.color': 'k',#'dimgrey',
 'ytick.direction': 'out',
 'ytick.left': True,
 'ytick.right': False,
 'grid.color': '#b0b0b0',
 'axes.axisbelow' : True,
 'patch.linewidth': 0.0, # no border on bar graph
 'lines.markeredgewidth': 0})

"""
scatter.edgecolors: face  

lines.markeredgecolor: auto
lines.markeredgewidth: 1.0 

boxplot.flierprops.markeredgecolor: black
boxplot.flierprops.markeredgewidth: 1.0

boxplot.meanprops.markeredgecolor: C2  




"""
# ax.set_axisbelow(True)
#
# grid.color:     "#b0b0b0"  # grid color
# grid.linestyle: -          # solid
# grid.linewidth: 0.8        # in points
# grid.alpha:     1.0        # transparency, between 0.0 and 1.0

# sns.set_context("notebook", rc={"font.size":16,
#                                 "axes.titlesize":20,
#                                 "axes.labelsize":18})

## font

# !sudo apt install msttcorefonts -qq
# !rm ~/.cache/matplotlib -rf

import matplotlib
# matplotlib.rcParams['font.family'] = "sans-serif"
# matplotlib.rcParams['font.sans-serif'] = "Arial"

# plt.rcParams.update({'font.family':'Arial'})

# plt.rcParams.update({'font.family':'sans-serif', 'fontname':'Arial'})
from matplotlib.font_manager import findfont, FontProperties
font = findfont(FontProperties(family=['sans-serif']))
print('pretty plots activated')



# def colors():
#     d = dict()
#     return d



