from typing import Optional, Union, Dict, List

import matplotlib.patches as patches
import matplotlib.lines as lines
import pandas as pd

from quickstats.plots import AbstractPlot
from quickstats.utils.common_utils import combine_dict

class UpperLimit2DPlot(AbstractPlot):
    
    STYLES = {
        'axis':{
            'tick_bothsides': False
        },
        'errorbar': {
            "linewidth": 1,
            "markersize": 5,
            "marker": 'o',
        }
    }
    
    COLOR_PALLETE = {
        '2sigma': '#FDC536',
        '1sigma': '#4AD9D9',
        'expected': 'k',
        'observed': 'k'
    }
    
    COLOR_PALLETE_EXTRA = {
        '2sigma': '#FDC536',
        '1sigma': '#4AD9D9',
        'expected': 'r',
        'observed': 'r'
    }
    
    LABELS = {
        '2sigma': 'Expected limit $\pm 2\sigma$',
        '1sigma': 'Expected limit $\pm 1\sigma$',
        'expected': 'Expected limit (95% CL)',
        'observed': 'Observed limit (95% CL)'
    }
    
    LABELS_EXTRA = {
        '2sigma': 'Expected limit $\pm 2\sigma$',
        '1sigma': 'Expected limit $\pm 1\sigma$',
        'expected': 'Expected limit (95% CL)',
        'observed': 'Observed limit (95% CL)'
    }

    CONFIG = {
        'primary_hatch'  : '\\\\\\',
        'secondary_hatch': '///',
        'primary_alpha'  : 0.9,
        'secondary_alpha': 0.8,
        'curve_line_styles': {
            'color': 'darkred' 
        },
        'curve_fill_styles':{
            'color': 'hh:darkpink'
        },
        'highlight_styles': {
            'linewidth' : 0,
            'marker' : '*',
            'markersize' : 20,
            'color' : '#E9F1DF',
            'markeredgecolor' : 'black'
        },
        'errorband_plot_styles':{
            'alpha': 1
        },
        'expected_plot_styles': {
            'marker': 'None',
            'linestyle': '--',
            'alpha': 1,
            'linewidth': 1
        },
        'observed_plot_styles': {
            'marker': 'o',
            'alpha': 1,
            'linewidth': 1
        }
    }
    
    def __init__(self, data:pd.DataFrame,
                 additional_data:Optional[List[Dict]]=None,
                 scale_factor:float=None,
                 color_pallete:Optional[Dict]=None,
                 labels:Optional[Dict]=None,
                 styles:Optional[Union[Dict, str]]=None,
                 analysis_label_options:Optional[Union[Dict, str]]='default',
                 config:Optional[Dict]=None):
        super().__init__(color_pallete=color_pallete,
                         styles=styles,
                         analysis_label_options=analysis_label_options,
                         config=config)
        self.data     = data
        
        self.additional_data = []
        if additional_data is not None:
            for _data in additional_data:
                self.add_data(**_data)
        
        self.labels = combine_dict(self.LABELS, labels)
 
        self.scale_factor = scale_factor
        
        self.curve_data     = None
        self.highlight_data = None
        
    def get_default_legend_order(self):
        return ['observed', 'expected', '1sigma', '2sigma', 'curve', 'highlight']
    
    def add_curve(self, x, y, yerrlo=None, yerrhi=None,
                  label:str="Theory prediction",
                  line_styles:Optional[Dict]=None,
                  fill_styles:Optional[Dict]=None):
        curve_data = {
            'x'     : x,
            'y'     : y,
            'yerrlo'  : yerrlo,
            'yerrhi'  : yerrhi,
            'label' : label,
            'line_styles': line_styles,
            'fill_styles': fill_styles,
        }
        self.curve_data = curve_data
                        
    def add_highlight(self, x:float, y:float, label:str="SM prediction",
                      styles:Optional[Dict]=None):
        highlight_data = {
            'x'     : x,
            'y'     : y,
            'label' : label,
            'styles': styles
        }
        self.highlight_data = highlight_data        
    
    def draw_curve(self, ax, data):
        line_styles = data['line_styles']
        fill_styles = data['fill_styles']
        if line_styles is None:
            line_styles = self.config['curve_line_styles']
        if fill_styles is None:
            fill_styles = self.config['curve_fill_styles']
        if (data['yerrlo'] is None) and (data['yerrhi'] is None):
            line_styles['color'] = fill_styles['color']
        handle_line = ax.plot(data['x'], data['y'], label=data['label'], **line_styles)
        handles = handle_line[0]
        if (data['yerrlo'] is not None) and (data['yerrhi'] is not None):
            handle_fill = ax.fill_between(data['x'], data['yerrlo'], data['yerrhi'],
                                          label=data['label'], **fill_styles)
            handles = (handle_fill, handle_line[0])
        self.update_legend_handles({'curve': handles}, idx=0)
        
    def draw_highlight(self, ax, data):
        styles = data['styles']
        if styles is None:
            styles = self.config['highlight_styles']
        handle = ax.plot(data['x'], data['y'], label=data['label'], **styles)
        self.update_legend_handles({'highlight': handle[0]}, idx=0)
        
    def draw_single_data(self, ax, data, scale_factor=None,
                         log:bool=False, 
                         draw_observed:bool=True,
                         color_pallete:Optional[Dict]=None,
                         labels:Optional[Dict]=None,
                         sigma_band_hatch:Optional[str]=None,
                         draw_errorband:bool=True,
                         idx:int=0):
        
        if color_pallete is None:
            color_pallete = self.color_pallete
        if labels is None:
            labels = self.labels
        if scale_factor is None:
            scale_factor = 1.0
            
        indices = data.index.astype(float).values
        exp_limits = data['0'].values * scale_factor
        n1sigma_limits = data['-1'].values * scale_factor
        n2sigma_limits = data['-2'].values * scale_factor
        p1sigma_limits = data['1'].values * scale_factor
        p2sigma_limits = data['2'].values * scale_factor
        
        handles_map = {}
        
        # draw +- 1, 2 sigma bands 
        if draw_errorband:
            handle_2sigma = ax.fill_between(indices, n2sigma_limits, p2sigma_limits, 
                                            facecolor=color_pallete['2sigma'],
                                            label=labels['2sigma'],
                                            hatch=sigma_band_hatch,
                                            **self.config["errorband_plot_styles"])
            handle_1sigma = ax.fill_between(indices, n1sigma_limits, p1sigma_limits, 
                                            facecolor=color_pallete['1sigma'],
                                            label=labels['1sigma'],
                                            hatch=sigma_band_hatch,
                                            **self.config["errorband_plot_styles"])
            handles_map['1sigma'] = handle_1sigma
            handles_map['2sigma'] = handle_2sigma
        
        if log:
            draw_fn = ax.semilogy
        else:
            draw_fn = ax.plot
 
        if draw_observed:
            obs_limits = data['obs'].values * scale_factor
            handle_observed = draw_fn(indices, obs_limits, color=color_pallete['observed'], 
                                      label=labels['observed'], 
                                      **self.config["observed_plot_styles"])
            handles_map['observed'] = handle_observed[0]
            
        handle_expected = draw_fn(indices, exp_limits, color=color_pallete['expected'],
                                  label=labels['expected'],
                                  **self.config["expected_plot_styles"])
        handles_map['expected'] = handle_expected[0]

        self.update_legend_handles(handles_map, idx=idx)
        
    def add_data(self, data:pd.DataFrame, color_pallete:Optional[Dict]=None,
                 labels:Optional[Dict]=None, draw_observed:bool=False,
                 draw_errorband:bool=False):
        config = {
            "data": data,
            "color_pallete": combine_dict(self.COLOR_PALLETE_EXTRA, color_pallete),
            "labels": combine_dict(self.LABELS_EXTRA, labels),
            "draw_observed": draw_observed,
            "draw_errorband": draw_errorband
        }
        self.additional_data.append(config)
            
    def draw(self, xlabel:str="", ylabel:str="", ylim=None, xlim=None,
             log:bool=False, draw_observed:bool=True, draw_errorband:bool=True,
             draw_sec_errorband:bool=False, draw_hatch:bool=True):
        
        ax = self.draw_frame()
        
        if len(self.additional_data) > 0:
            if draw_hatch:
                sigma_band_hatch = self.config['secondary_hatch']
                alpha = self.config['secondary_alpha']
            else:
                sigma_band_hatch = None
                alpha = 1.
            for idx, config in enumerate(self.additional_data):
                self.draw_single_data(ax, config["data"],
                                      scale_factor=self.scale_factor,
                                      log=log, 
                                      draw_observed=config["draw_observed"],
                                      color_pallete=config["color_pallete"],
                                      labels=config["labels"],
                                      sigma_band_hatch=sigma_band_hatch,
                                      draw_errorband=config["draw_errorband"],
                                      idx=idx + 1)
            if draw_hatch:
                sigma_band_hatch = self.config['primary_hatch']
                alpha = self.config['primary_alpha']
            else:
                sigma_band_hatch = None
                alpha = 1.
        else:
            sigma_band_hatch = None
            alpha = 1.
        self.draw_single_data(ax, self.data,
                              scale_factor=self.scale_factor,
                              log=log, 
                              draw_observed=draw_observed,
                              color_pallete=self.color_pallete,
                              labels=self.labels,
                              sigma_band_hatch=sigma_band_hatch,
                              draw_errorband=draw_errorband,
                              idx=0)
        
        if self.curve_data is not None:
            self.draw_curve(ax, self.curve_data)   
        if self.highlight_data is not None:
            self.draw_highlight(ax, self.highlight_data)
            
        self.draw_axis_components(ax, xlabel=xlabel, ylabel=ylabel)
        
        if ylim is not None:
            ax.set_ylim(*ylim)
        if xlim is not None:
            ax.set_xlim(*xlim)

        # border for the legend
        border_leg = patches.Rectangle((0, 0), 1, 1, facecolor = 'none', edgecolor = 'black', linewidth = 1)
        for legend_data in self.legend_data_ext.values():
            for sigma in ['1sigma', '2sigma']:
                if sigma in legend_data:
                    legend_data[sigma]['handle'] = (legend_data[sigma]['handle'], border_leg)        
        
        if self.curve_data is not None:
            if isinstance(self.legend_data_ext[0]['curve']['handle'], tuple):
                self.legend_data_ext[0]['curve']['handle'] = (*self.legend_data_ext[0]['curve']['handle'], border_leg)
        
        indices = sorted(self.legend_data_ext.keys())
        handles, labels = self.get_legend_handles_labels(idx=indices)
        ax.legend(handles, labels, **self.styles['legend'])
        return ax
