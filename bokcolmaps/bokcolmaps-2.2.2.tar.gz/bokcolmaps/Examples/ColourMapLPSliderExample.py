"""
To run this example at the command line enter:
python3 ColourMap3LPSLiderExample.py
"""

from bokeh.plotting import show

from bokcolmaps.ColourMapLPSlider import ColourMapLPSlider
from bokcolmaps.Examples import example_data

x, y, z, D = example_data()

cm = ColourMapLPSlider(x, y, z, D, xlab='x val', ylab='y val',
                       zlab='power val', dmlab='Function val')

show(cm)
