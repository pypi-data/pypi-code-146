from typing import Optional, Union, Dict, List

import pandas as pd
import numpy as np

from matplotlib import colors
from matplotlib.ticker import MaxNLocator
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon

from quickstats.plots import AbstractPlot
from quickstats.plots.template import single_frame, parse_styles, create_transform
from quickstats.utils.common_utils import combine_dict
from quickstats.maths.statistics import min_max_to_range

class VariableDistributionPlot(AbstractPlot):
    
    def __init__(self, data_map:Dict[str, pd.DataFrame], plot_options:Dict[str, Dict],
                 styles:Optional[Union[Dict, str]]=None,
                 analysis_label_options:Optional[Dict]=None,
                 config:Optional[Dict]=None):
        """
        Arguments:
            plot_options: dicionary
                A dictionary containing plot options for various group of samples.
                Format: { <sample_group>: {
                            "samples": <list of sample names>,
                            "styles": <options in mpl.hist>},
                            "type": "hist" or "errorbar"
                          ...}
             
        """
        self.data_map = data_map
        self.plot_options = plot_options
        super().__init__(styles=styles,
                         analysis_label_options=analysis_label_options,
                         config=config)
    
    def draw(self, column_name:str, weight_name:Optional[str]="weight",
             xlabel:str="", ylabel:str="Fraction of Events / {bin_width:.2f}",
             nbins:int=25, xmin:Optional[float]=None, xmax:Optional[float]=None,
             ypad:float=0.4, rescale_by:Optional[float]=None,
             normalize:bool=True):
        """
        
        Arguments:
            column_name: string, default = "score"
                Name of the variable in the dataframe.
            weight_name: (optional) string, default = "weight"
                If specified, normalize the histogram by the "weight_name" variable
                in the dataframe.
            xlabel: string, default = "Score"
                Label of x-axis.
            ylabel: string, default = "Fraction of Events / {bin_width}"
                Label of y-axis.
            boundaries: (optional) list of float
                If specified, draw score boundaries at given values.
            nbins: int, default = 25
                Number of histogram bins.
            xmin: (optional) float
                Minimum value of the bins.
            xmax: (optional) float
                Maximum value of the bins.
            ypad: float, default = 0.4
                Fraction of the y-axis that should be padded.
            rescale_by: (optional) float
                Rescale variable values by a factor.
            normalize: bool, default = True
                Normalize histogram to unity.
        """
        ax = self.draw_frame()
        data_xmin = None
        data_xmax = None
        bin_range = min_max_to_range(xmin, xmax)
        for key in self.plot_options:
            samples = self.plot_options[key]["samples"]
            plot_style = self.plot_options[key].get("styles", {})
            plot_type = self.plot_options[key].get("type", "hist")
            df = pd.concat([self.data_map[sample] for sample in samples], ignore_index = True)
            x = df[column_name].values
            if rescale_by is not None:
                x = x * rescale_by
            if data_xmin is None:
                data_xmin = np.min(x)
            else:
                data_xmin = min(data_xmin, np.min(x))
            if data_xmax is None:
                data_xmax = np.max(x)
            else:
                data_xmax = max(data_xmax, np.max(x))
            if weight_name is not None:
                weights = df[weight_name]
            else:
                weights = None
            if plot_type == "hist":
                if normalize and (weights is not None):
                    weights = weights / weights.sum()
                plot_style = combine_dict(self.styles["hist"], plot_style)
                y, x, _ = ax.hist(x, nbins, range=bin_range,
                                  weights=weights, **plot_style, zorder=-5)
            elif plot_type == "errorbar":
                from quickstats.maths.statistics import get_hist_data
                hist_data = get_hist_data(x, weights,
                                          normalize=normalize,
                                          range=bin_range,
                                          bins=nbins)
                plot_style = combine_dict(self.styles["errorbar"], plot_style)
                ax.errorbar(**hist_data, **plot_style)
            else:
                raise RuntimeError(f'unknown plot type: {plot_type}')
        if bin_range is None:
            axis_xmin = data_xmin
            axis_xmax = data_xmax
        else:
            axis_xmin = bin_range[0]
            axis_xmax = bin_range[1]
        bin_width = (xmax - xmin) / nbins
        ylabel = ylabel.format(bin_width=bin_width)
        
        self.draw_axis_components(ax, xlabel=xlabel, ylabel=ylabel)
        self.set_axis_range(ax, xmin=axis_xmin, xmax=axis_xmax, ypad=ypad)

        handles, labels = ax.get_legend_handles_labels()
        new_handles = [Line2D([], [], c=h.get_edgecolor(), linestyle=h.get_linestyle(),
                       **self.styles['legend_Line2D']) if isinstance(h, Polygon) else h for h in handles]
        ax.legend(handles=new_handles, labels=labels, **self.styles['legend'])
        return ax