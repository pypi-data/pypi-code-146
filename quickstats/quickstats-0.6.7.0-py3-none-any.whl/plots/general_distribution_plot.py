from typing import Optional, Union, Dict, List, Tuple, Callable

from cycler import cycler

import numpy as np
import pandas as pd

from quickstast import semistaticmethod
from quickstats.plots.color_schemes import QUICKSTATS_PALETTES

from quickstats.plots import AbstractPlot, CollectiveDataPlot
from quickstats.plots.template import suggest_markersize, ratio_frames, centralize_axis, create_transform
from quickstats.utils.common_utils import combine_dict
from quickstats import GeneralEnum

class ErrorDisplayFormat(GeneralEnum):
    ERRORBAR = 0
    FILL     = 1

class GeneralDistributionPlot(AbstractPlot):
    
    STYLES = {
        'errorbar': {
            "marker": 'o',
            "markersize": None,
            "linewidth": 0,
            "elinewidth": 1,
            "capsize": 3,
            "capthick": 1
        },
        "annotation": {
            "xy": (0.05, 0.9),
            "xycoords": "axes fraction",
            "horizontalalignment": "left",
            "verticalalignment": "top",
            "fontsize": 20
        },
        "legend": {
            "borderpad": 1
        },
        "ratio_frames": {
            "height_ratios": (4, 1)
        }
    }
    
    CONFIG = {
        "blind_region_styles":{
            "linestyle": "--"
        },
        'ratio_line_styles':{
            'color': 'gray',
            'linestyle': '--'
        }        
    }
    
    def __init__(self, collective_data:Dict[str, Union[Dict[str, np.ndarray], pd.DataFrame]],
                 blind_ranges:Optional[Union[List[float], List[List[float]]]],
                 plot_options:Optional[Dict[str, Dict]]=None,
                 scale_map:Optional[Dict[str, float]]=None,
                 label_map:Optional[Dict[str, str]]=None,
                 color_cycle:Optional[Dict]=None,
                 styles:Optional[Union[Dict, str]]=None,
                 analysis_label_options:Optional[Union[Dict, str]]=None,
                 figure_index:Optional[int]=None,
                 config:Optional[Dict]=None):
        """
        
        Parameters:
            collective_data: dictionary
                Input data of the form {data_label: {"x": array, "y": array}, ...}.
                To specify symmetric errors, use {"x": array, "y": array, "xerr": array, "yerr": array}.
                To specify asymmetric errors, use {"x": array, "y": array,
                "xerrlo": array, "xerrhi": array, "yerrlo": array, "yerrhi": array}.
        """

        self.error_options = {}
        self.scale_map     = combine_dict({}, scale_map)
        self.colors        = {} 
        self.annotation    = None
        
        self.blind_ranges(blind_ranges)
        
        super().__init__(collective_data=collective_data,
                         plot_options=plot_options,
                         label_map=label_map,
                         color_cycle=color_cycle,
                         styles=styles, 
                         analysis_label_options=analysis_label_options,
                         figure_index=figure_index,
                         config=config)
        
    def set_blind_ranges(self, blind_ranges:Optional[Union[List[float], List[List[float]]]]=None):
        if blind_ranges is None:
            self.blind_ranges = None
            return None
        from quickstats.maths.numerics import get_proper_ranges
        self.blind_ranges = get_proper_ranges(blind_ranges)
        
    def set_data(self, collective_data:Dict[str, "pandas.DataFrame"]):
        super().set_data(collective_data)
        self.legend_order = list(collective_data.keys())
        for name in self.collective_data:
            if name not in self.error_options:
                self.set_error_options(name)        
        
    @classmethod
    def parse_data(cls, data:Dict[str, Union[Dict[str, np.ndarray], pd.DataFrame]]):
        if not isinstance(data, (dict, pd.DataFrame)):
            raise ValueError("input data must be a dataframe or dictionary")
        for attribute in ["x", "y"]:
            if attribute not in data:
                raise RuntimeError(f'missing attribute "{attribute}" from input data')
        x, y = np.array(data['x']), np.array(data['y'])
        error_data = cls.get_error_data(data)
        # check shape consistency
        if x.shape != y.shape:
            raise ValueError('invalid input: "x" and "y" values must have the same shape')
        data_shape = x.shape
        for label in ["xerr", "yerr"]:
            err_values = error_data[label]
            if err_values is None:
                continue
            if isinstance(err_values, tuple):
                valid_shape = (error_values[0].shape == data_shape) and (error_values[1].shape == data_shape)
            else:
                valid_shape = error_values.shape == data_shape
            if not valid_shape:
                raise RuntimeError('inconsistent shape between data and error values')
        parsed_data = {
            'x'    : x,
            'y'    : y,
            'xerr' : error_data['xerr']
            'yerr' : error_data['yerr']
        }
        return parsed_data           

    @semistaticmethod
    def get_error_data(data:Union[Dict[str, np.ndarray], pd.DataFrame]):
        error_data = {}
        for label in ["xerr", "yerr"]:
            err   = data.get(label, None)
            errlo = data.get(f"{label}lo", None)
            errhi = data.get(f"{label}hi", None)
            # set default to None
            error_data[label] = None
            if (err is None):
                if  (errlo is not None) and (errhi is None):
                    values = np.array(errlo)
                    error_data[label] = (values, np.zeros(values.shape))
                elif (errlo is None) and (errhi is not None):
                    values = np.array(errhi)
                    error_data[label] = (np.zeros(values.shape), values)
                elif (errlo is not None) and (errhi is not None):
                    error_data[label] = (np.array(errlo), np.array(errhi))
            else:
                if ((errlo is not None) or (errhi is not None)):
                    raise ValueError(f'invalid input: received both "{label}" and '
                                     f'"{label}lo"/"{label}hi" attributes')
                error_data[label] = np.array(err)
        return error_data
    
    @semistaticmethod
    def select_data(self, data:Dict[str, np.ndarray], key:str,
                    value_ranges:np.ndarray):
        if err is None:
            return None
        elif isinstance(err, tuple):
            new_err = []
            for err_i in err:
                new_err.append(err_i[mask])
            return tuple(new_err)
        else:
            return err[mask]

    def draw_single_data(self, ax, data, label:str, label_blind:Optional[str]=None,
                         blind_range:Optional[List[float]]=None,
                         plot_options:Optional[Dict]=None, show_error:bool=True,
                         error_format:Union[ErrorDisplayFormat, str]="error_bar",
                         error_styles:Optional[Dict]=None,
                         scale_by:Optional[float]=None):
        pdata = self.process_data(data, blind_range=blind_range, scale_by=scale_by)
        has_errorbar = not ((pdata['xerr'] is None) and (pdata['yerr'] is None))
        draw_blind = blind_range is not None
        if not has_errorbar:
            combined_options = combine_dict(self.styles['plot'], plot_options)
            combined_options['label'] = label
            if draw_blind:
                # draw sideband low
                handle_sblo = ax.plot(pdata['x'][pdata['sideband_lo']], 
                                      pdata['y'][pdata['sideband_lo']],
                                      **combined_options)
                # avoid going through internal color cycle for the three regions
                combined_options['color'] = handle_sblo[0].get_color()
                # draw sideband high
                handle_sbhi = ax.plot(pdata['x'][pdata['sideband_hi']], 
                                      pdata['y'][pdata['sideband_hi']],
                                      **combined_options)
                combined_options['linestyle'] = self.config['blind_region_styles']['linestyle']
                if label_blind is None:
                    combined_options['label'] = f"{label} (blind)"
                else:
                    combined_options['label'] = label_blind
                x_blind_plus_sideband_edge = [pdata['x'][pdata['sideband_lo']][-1]] + \
                                             list(pdata['x'][pdata['blind']]) + \
                                             [pdata['x'][pdata['sideband_hi']][0]]
                y_blind_plus_sideband_edge = [pdata['y'][pdata['sideband_lo']][-1]] + \
                                             list(pdata['y'][pdata['blind']]) + \
                                             [pdata['y'][pdata['sideband_hi']][0]]                
                handle_blind = ax.plot(x_blind_plus_sideband_edge, 
                                       y_blind_plus_sideband_edge,
                                       **combined_options)
                handle = [handle_sblo[0], handle_blind[0]]
            else:
                handle = ax.plot(pdata['x'], pdata['y'], **combined_options)
                handle = handle[0]
        else:
            
            combined_options = combine_dict(plot_options, {"label": label})
            if combined_options.get('markersize', None) is None:
                nbins = len(pdata['x'])
                combined_options['markersize'] = suggest_markersize(nbins)
                
            if draw_blind:
                x = pdata['x'][pdata['sideband']]
                y = pdata['y'][pdata['sideband']]
                xerr = self._get_selected_err(pdata['xerr'], pdata['sideband'])
                yerr = self._get_selected_err(pdata['yerr'], pdata['sideband'])
            else:
                x = pdata['x']
                y = pdata['y']
                xerr = pdata['xerr']
                yerr = pdata['yerr']
            if not show_error:
                error_format = None
            handle = self._draw_data(ax, x, y, xerr, yerr,
                                     plot_options=combined_options,
                                     error_format=error_format,
                                     error_styles=error_styles)
        return handle
    
    def _draw_data(self, ax, x:np.ndarray, y:np.ndarray,
                   xerr:Optional[np.ndarray]=None,
                   yerr:Optional[np.ndarray]=None,
                   plot_options:Optional[Dict]=None,
                   error_format:Optional[Union[ErrorDisplayFormat, str]]="error_bar",
                   error_styles:Optional[Dict]=None):
        combined_options = combine_dict(plot_options, self.styles['errorbar'])
        if error_format is None:
            combined_options['elinewidth'] = 0
            combined_options['capsize'] = 0
            combined_options['capthick'] = 0
            handle = ax.errorbar(x, y, xerr=xerr, yerr=yerr,
                                 **combined_options)
        elif (error_format == ErrorDisplayFormat.ERRORBAR):
            combined_options = combine_dict(combined_options, error_styles)
            handle = ax.errorbar(x, y, xerr=xerr, yerr=yerr,
                                 **combined_options)
        elif (error_format == ErrorDisplayFormat.FILL):
            combined_options['elinewidth'] = 0
            combined_options['capsize'] = 0
            combined_options['capthick'] = 0
            handle = ax.errorbar(x, y, xerr=xerr, yerr=yerr,
                                 **combined_options)
            fill_options = combine_dict(self.styles['fill_between'], error_styles)
            if "zorder" not in fill_options:
                fill_options["zorder"] = 5
            if yerr is not None:
                handle_fill = ax.fill_between(x, y - yerr[0], y + yerr[1],
                                              **fill_options)
            else:
                handle_fill = None
        else:
            raise RuntimeError(f"unkown error display format: {error_format}")
        return handle
    
    def draw_comparison(self, ax, reference_data, target_data, 
                        xlabel:str="", ylabel:str="",  mode:str="ratio",
                        plot_options:Optional[Dict]=None, show_error:bool=True, 
                        blind_range:Optional[List[float]]=None,
                        error_format:Union[ErrorDisplayFormat, str]="error_bar",
                        error_styles:Optional[Dict]=None,                        
                        draw_ratio_line:bool=True):
        pdata_ref = self.process_data(reference_data, blind_range=blind_range)
        pdata_tgt = self.process_data(target_data, blind_range=blind_range)
        if not np.allclose(pdata_tgt['x'], pdata_ref['x']):
            raise RuntimeError("cannot compare two distributions with different binnings")
        pdata_comp = {}
        pdata_comp['x'] = pdata_ref['x']
        pdata_comp['yerr'] = 0
        pdata_comp['xerr'] = pdata_ref['xerr']
        if pdata_ref['yerr'] is None:
            if isinstance(pdata_tgt['yerr'], tuple):
                yerr_ref = (np.zeros(pdata_ref['y'].shape), np.zeros(pdata_ref['y'].shape))
            else:
                yerr_ref = np.zeros(pdata_ref['y'].shape)
        else:
             yerr_ref = pdata_ref['yerr']
        if pdata_tgt['yerr'] is None:
            if isinstance(pdata_ref['yerr'], tuple):
                yerr_tgt = (np.zeros(pdata_tgt['y'].shape), np.zeros(pdata_tgt['y'].shape))
            else:
                yerr_tgt = np.zeros(pdata_tgt['y'].shape)
        else:
             yerr_tgt = pdata_tgt['yerr']
        if mode == "ratio":
            vmode = 0
        elif mode in ["diff", "difference"]:
            vmode = 1
        else:
            raise ValueError(f"unsupported mode \"{mode}\", choose between \"ratio\" and \"difference\"")
        if vmode == 0:
            pdata_comp['y'] = pdata_tgt['y'] / pdata_ref['y']
            if isinstance(yerr_ref, tuple):
                errlo = np.sqrt((yerr_ref[0]/pdata_ref['y'])**2 + (yerr_tgt[0]/pdata_tgt['y'])**2)
                errhi = np.sqrt((yerr_ref[1]/pdata_ref['y'])**2 + (yerr_tgt[1]/pdata_tgt['y'])**2)
                pdata_comp['yerr'] = (errlo, errhi)
            else:
                pdata_comp['yerr'] = np.sqrt((yerr_ref/pdata_ref['y'])**2 + (yerr_tgt/pdata_tgt['y'])**2)
        elif vmode == 1:
            pdata_comp['y'] = pdata_tgt['y'] - pdata_ref['y']
            if isinstance(yerr_ref, tuple):
                errlo = np.sqrt(yerr_ref[0]**2 + yerr_tgt[0]**2)
                errhi = np.sqrt(yerr_ref[1]**2 + yerr_tgt[1]**2)
                pdata_comp['yerr'] = (errlo, errhi)
            else:
                pdata_comp['yerr'] = np.sqrt(yerr_ref**2 + yerr_tgt**2)
            
        combined_options = combine_dict(plot_options)
        if combined_options.get('markersize', None) is None:
            nbins = len(pdata_comp['x'])
            combined_options['markersize'] = suggest_markersize(nbins)
            
        draw_blind = blind_range is not None
        if draw_blind:
            x = pdata_comp['x'][pdata_ref['sideband']]
            y = pdata_comp['y'][pdata_ref['sideband']]
            xerr = self._get_selected_err(pdata_comp['xerr'], pdata_ref['sideband'])
            yerr = self._get_selected_err(pdata_comp['yerr'], pdata_ref['sideband'])
        else:
            x = pdata_comp['x']
            y = pdata_comp['y']
            xerr = pdata_comp['xerr']
            yerr = pdata_comp['yerr']
            
        if not show_error:
            error_format = None
        handle = self._draw_data(ax, x, y, xerr, yerr,
                                 plot_options=combined_options,
                                 error_format=error_format,
                                 error_styles=error_styles)
            
        ylim = list(ax.get_ylim())
        if ylim[0] > np.min(y):
            ylim[0] = np.min(y)
        if ylim[1] < np.max(y):
            ylim[1] = np.max(y)
        ax.set_ylim(ylim)
        
        if vmode == 0:
            centralize_axis(ax, which="y", ref_value=1)
            if draw_ratio_line:
                ratio_linestyles = self.config['ratio_line_styles']
                ax.axhline(1, zorder=0, **ratio_linestyles)
        elif vmode == 1:
            centralize_axis(ax, which="y", ref_value=0)
            if draw_ratio_line:
                ratio_linestyles = self.config['ratio_line_styles']
                ax.axhline(0, zorder=0, **ratio_linestyles)
        if not ylabel:
            if vmode == 0:
                ylabel = "Fit / Data"
            elif vmode == 1:
                ylabel = "Fit - Data"
            else:
                ylabel = ""
        self.draw_axis_components(ax, xlabel=xlabel, ylabel=ylabel)
        return handle
        
    def set_error_options(self, target:str,
                          display_format:Optional[Union[ErrorDisplayFormat, str]]="errorbar",
                          styles:Optional[Dict]=None):
        if display_format is not None:
            display_format = ErrorDisplayFormat.parse(display_format)
        self.error_options[target] = {
            "display_format": display_format,
            "styles": styles
        }

    def draw(self, xlabel:str="", ylabel:str="",
             targets:Optional[List]=None,
             logx:bool=False, logy:bool=False,
             blind_range:Optional[List[float]]=None,
             show_error:bool=True,
             comparison_options:Optional[Union[Dict, List[Dict]]]=None,
             xmin:Optional[float]=None, xmax:Optional[float]=None,
             ymin:Optional[float]=None, ymax:Optional[float]=None,
             ypad:Optional[float]=None):
        
        if comparison_options is not None:
            ax, ax_ratio = self.draw_frame(ratio_frames, logx=logx, logy=logy,
                                           **self.styles["ratio_frames"])
        else:
            ax = self.draw_frame(logx=logx, logy=logy)

        for name in self.collective_data:
            if (targets is not None) and(name not in targets):
                continue
            data = self.collective_data[name]
            label = self.label_map.get(name, name)
            label_blind = self.label_map.get(f"{name}_blind", None)
            plot_options = self.plot_options.get(name, {})
            scale_by = self.scale_map.get(name, None)
            if (name not in self.error_options) or \
               (self.error_options[name]["display_format"] is None):
                error_format = None
                error_styles = None
            else:
                error_format = self.error_options[name]["display_format"]
                error_styles = self.error_options[name]["styles"]
            handle = self.draw_single_data(ax, data, label,
                                           label_blind=label_blind,
                                           blind_range=blind_range,
                                           plot_options=plot_options,
                                           show_error=show_error,
                                           error_format=error_format,
                                           error_styles=error_styles,
                                           scale_by=scale_by)
            # case draw blind
            if isinstance(handle, list) and len(handle) == 2:
                blind_name = f"{name}_blind"
                self.legend_order.append(blind_name)
                self.update_legend_handles({name: handle[0], blind_name: handle[1]})
                self.colors[name] = handle[0].get_color()
            else:
                self.update_legend_handles({name: handle})
                if not handle.get_children():
                    self.colors[name] = handle.get_color()
                else:
                    self.colors[name] = handle[0].get_color()
        
        self.draw_axis_components(ax, xlabel=xlabel, ylabel=ylabel)
        self.set_axis_range(ax, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, ypad=ypad)  
        handles, labels = self.get_legend_handles_labels()
        ax.legend(handles, labels, **self.styles['legend'])
        
        if comparison_options is not None:
            if not isinstance(comparison_options, list):
                comparison_options = [comparison_options]
            for options in comparison_options:
                reference = options['reference']
                target    = options['target']
                mode      = options.get('mode', "ratio")
                ylabel    = options.get('label', "")
                labelsize = options.get('labelsize', None)
                styles    = options.get('styles', {})
                draw_ratio_line = options.get('draw_ratio_line', True)
                plot_options = self.plot_options.get(reference, {})
                if 'color' not in plot_options:
                    plot_options['color'] = self.colors[target]
                plot_options.update(styles)
                if (reference not in self.error_options) or \
                   (self.error_options[reference]["display_format"] is None):
                    error_format = None
                    error_styles = None
                else:
                    error_format = self.error_options[reference]["display_format"]
                    error_styles = self.error_options[reference]["styles"]
                self.draw_comparison(ax_ratio,
                                     self.collective_data[reference],
                                     self.collective_data[target],
                                     xlabel=ax.get_xlabel(),
                                     ylabel=ylabel, mode=mode,
                                     plot_options=plot_options,
                                     show_error=show_error,
                                     error_format=error_format,
                                     error_styles=error_styles,
                                     blind_range=blind_range,
                                     draw_ratio_line=draw_ratio_line)
                if labelsize is not None:
                    ax_ratio.yaxis.label.set_size(labelsize)                
            ax.set(xlabel=None)
            ax.tick_params(axis="x", labelbottom=False)

        if self.annotation:
            kwargs = combine_dict(self.styles['annotation'], self.annotation)
            ax.annotate(**kwargs)
            
        if comparison_options is not None:
            return ax, ax_ratio
        
        return ax
