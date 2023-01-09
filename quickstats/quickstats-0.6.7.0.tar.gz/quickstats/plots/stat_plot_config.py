from typing import List, Union, Dict, Optional, Callable

import numpy as np
import matplotlib.pyplot as plt

from quickstats import GeneralEnum

class StatMeasure(GeneralEnum):
    MEAN   = (0, np.mean)
    STD    = (1, np.std)
    MIN    = (2, np.min)
    MAX    = (3, np.max)
    MEDIAN = (4, np.median)
    
    def __new__(cls, value:int, operator:Callable):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.operator = operator
        return obj           

class StatPlotConfig:
    
    @property
    def stat_measures(self):
        return self._stat_measures
    
    @stat_measures.setter
    def stat_measures(self, values):
        parsed = []
        for value in values:
            parsed.append(StatMeasure.parse(value))
        self._stat_measures = parsed            
    
    def __init__(self, stat_measures:List[Union[StatMeasure, str]],
                 axis_method:str, options:Dict,
                 handle_options:Optional[Dict]=None,
                 handle_return_method:Optional[Callable]=None):
        self.stat_measures  = stat_measures
        self.axis_method    = axis_method
        self.options        = options
        if handle_options is None:
            self.handle_options = self.get_default_handle_options()
        else:
            self.handle_options = handle_options
        self.quantities     = {}
        self.handle_return_method = handle_return_method
        
    def set_data(self, x:np.ndarray):
        quantities = {}
        for stat_measure in self.stat_measures:
            quantity = stat_measure.operator(x)
            name = stat_measure.name.lower()
            quantities[name] = quantity
        self.quantities = quantities
    
    def get_default_handle_options(self):
        return {}
    
    def apply(self, ax, main_handle:Optional=None):
        if not hasattr(ax, self.axis_method):
            raise RuntimeError(f"matplotlib.axes.Axes has no method named {self.axis_method}")
        if not self.quantities:
            raise RuntimeError(f"stat data not initialized")
        method = getattr(ax, self.axis_method)
        resolved_options = {}
        for name in self.options:
            if callable(self.options[name]):
                resolved_options[name] = self.options[name](self.quantities)
            else:
                resolved_options[name] = self.options[name]
        if (main_handle is not None) and (self.handle_options is not None):
            for name in self.handle_options:
                if name in resolved_options:
                    continue
                resolved_options[name] = self.handle_options[name](main_handle)
        result = method(**resolved_options)
        if self.handle_return_method is not None:
            return self.handle_return_method(result)
        return result

class HandleMatchConfig(StatPlotConfig):
    def get_default_handle_options(self):
        handle_options = {
            "color": lambda handle: handle.get_color()
        }
        return handle_options
    
class AverageLineH(HandleMatchConfig):
    def __init__(self, **styles):
        options = {
            "y":  lambda x: x["mean"],
            **styles
        }
        super().__init__(["mean"], "axhline", options=options)
        
class AverageLineV(HandleMatchConfig):
    def __init__(self, **styles):
        options = {
            "x":  lambda x: x["mean"],
            **styles
        }
        super().__init__(["mean"], "axvline", options=options)        
        
class StdBandH(HandleMatchConfig):
    def __init__(self, **styles):
        options = {
            "ymin": lambda x: x["mean"] - x["std"],
            "ymax": lambda x: x["mean"] + x["std"],
            **styles
        }
        super().__init__(["mean", "std"], "axhspan", options=options)
        
class StdBandV(HandleMatchConfig):
    def __init__(self, **styles):
        options = {
            "xmin": lambda x: x["mean"] - x["std"],
            "xmax": lambda x: x["mean"] + x["std"],
            **styles
        }
        super().__init__(["mean", "std"], "axvspan", options=options)        