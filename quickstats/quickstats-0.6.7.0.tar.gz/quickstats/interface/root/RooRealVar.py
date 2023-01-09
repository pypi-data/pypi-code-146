from typing import Dict, Union, List, Optional

from quickstats.maths.numerics import get_proper_ranges

class RooRealVar:
    
    @property
    def range(self):
        return self._range
    
    @range.setter
    def range(self, value:Optional[List[float]]=None):
        self._range = self._parse_value_range(value, self.value)
   
    @property
    def named_ranges(self):
        return self._named_ranges
    
    @named_ranges.setter
    def named_ranges(self, value:Optional[Dict[str, List[float]]]=None):
        self._named_ranges = self._parse_named_ranges(value)
        
    def __init__(self, obj:Optional[Union[Dict, "ROOT.RooRealVar"]]=None):
        if obj is not None:
            self.parse(obj)
        else:
            self.name   = None
            self.title  = None
            self.value  = None
            self.n_bins = None
            self.unit   = None
            self.range  = None
            self.named_ranges = None
        
    def parse(self, obj:Union[str, Dict, "ROOT.RooRealVar"]):
        if isinstance(obj, str):
            self.parse({"name": obj})
        elif isinstance(obj, dict):
            self.name = obj["name"]
            self.title = obj.get("title", None)
            self.value = obj.get("value", None)
            self.range = obj.get("range", None)
            self.named_ranges = obj.get("named_ranges", None)
            self.n_bins = obj.get("n_bins", None)
            self.unit = obj.get("unit", None)
        else:
            import ROOT
            if not isinstance(obj, ROOT.RooRealVar):
                raise ValueError("object must be an instance of ROOT.RooRealVar")
            self.name   = str(obj.GetName())
            self.title  = str(obj.getTitle())
            self.value  = obj.getVal()
            self.n_bins = obj.getBins()
            self.unit   = obj.getUnit()
            _range = obj.getRange()
            self.range = [_range[0], _range[1]]
            named_ranges = {}
            for name in obj.getBinningNames():
                if str(name) == "":
                    continue
                _range = obj.getRange(name)
                named_ranges[name] = [_range[0], _range[1]]
            self.named_ranges = named_ranges
        
    @staticmethod
    def _parse_named_ranges(named_ranges:Optional[Dict[str, List[float]]]=None):
        if named_ranges:
            ranges = get_proper_ranges(list(named_ranges.values()), no_overlap=False)
            result = {k:v for k, v in zip(named_ranges.keys(), ranges)}
            return result
        return None
    
    @staticmethod
    def _parse_value_range(value_range:Optional[List[float]]=None,
                           nominal_value:Optional[float]=None):
        if value_range is not None:
            result = get_proper_ranges(value_range, nominal_value)
            if result.shape != (1, 2):
                raise ValueError("value range must be list of size 2")
            return result[0]
        return None
                                
    @classmethod
    def create(cls, name:str, title:Optional[str]=None,
               value:Optional[float]=None,
               range:Optional[List[float]]=None,
               named_ranges:Optional[Dict[str, List[float]]]=None,
               n_bins:Optional[int]=None, unit:Optional[str]=None):
        instance = cls()
        kwargs = {
                    "name" : name,
                   "title" : title,
                   "value" : value,
                   "range" : range,
            "named_ranges" : named_ranges,
                  "n_bins" : n_bins,
                    "unit" : unit
        }
        instance.parse(kwargs)
        return instance
        
    def new(self):
            
        if self.name is None:
            raise RuntimeError("object not initialized")
            
        import ROOT
        
        if self.title is not None:
            title = self.title
        else:
            title = self.name
        
        if (self.value is not None) and (self.range is not None):
            variable = ROOT.RooRealVar(self.name, title, self.value,
                                       self.range[0], self.range[1])
        elif (self.value is None) and (self.range is not None):
            variable = ROOT.RooRealVar(self.name, title,
                                       self.range[0], self.range[1])
        elif (self.value is not None) and (self.range is None):
            variable = ROOT.RooRealVar(self.name, title, self.value)
        else:
            variable = ROOT.RooRealVar(self.name, title, 0.)
            
        if self.named_ranges is not None:
            for name, _range in self.named_ranges.items():
                variable.setRange(name, _range[0], _range[1])            
        
        if self.n_bins is not None:
            variable.setBins(self.n_bins)
            
        if self.unit is not None:
            variable.setUnit(self.unit)
            
        return variable