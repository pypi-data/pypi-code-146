from typing import Optional, Union, Dict, List, Any

from quickstats.utils.common_utils import combine_dict
from quickstats.plots import AbstractPlot

class CollectiveDataPlot(AbstractPlot):
    
    def __init__(self, collective_data:Dict[str, Any],
                 plot_options:Optional[Dict[str, Dict]]=None,
                 label_map:Optional[Dict[str, str]]=None,
                 color_pallete:Optional[Dict]=None,
                 color_cycle:Optional[Dict]=None,
                 styles:Optional[Union[Dict, str]]=None,
                 analysis_label_options:Optional[Union[Dict, str]]=None,
                 figure_index:Optional[int]=None,
                 config:Optional[Dict]=None):
        
        super().__init__(color_pallete=color_pallete,
                         color_cycle=color_cycle,
                         styles=styles, 
                         analysis_label_options=analysis_label_options,
                         figure_index=figure_index,
                         config=config)
        
        self.set_data(collective_data)
        self.plot_options = combine_dict({}, plot_options)
        self.label_map    = combine_dict({}, label_map)
        
    def set_data(self, collective_data:Dict[str, Any]):
        if not isinstance(collective_data, dict):
            raise ValueError("data collection must be contained in a dictionary")
        resolved_data = {}
        for label, data in collective_data.items():
            resolved_data[label] = self.parse_data(data)
        self.collective_data = resolved_data
    
    @classmethod
    def parse_data(cls, data:Any):
        return data