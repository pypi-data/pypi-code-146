from datetime import datetime,timedelta
from tabulate import tabulate
from traceback import print_exc
from dataclasses import fields
from distutils.util import strtobool
TYPES = {cls.__name__: cls for cls in [str, int, float, bool, dict]}
TYPES['bool']=strtobool #allows us to convert the string input to a bool in a more intuitive way

def add_to_dte(dte,days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    return dte + timedelta(days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)

def dte_to_str(dte):
    if dte is None:
        return None
    return dte.strftime("%Y-%m-%d")
    
def now():
    return datetime.utcnow()

def first(lst,matching_fxn):
    try:
        return next(item for item in lst if matching_fxn(item))
    except StopIteration as e:
        return None
        
# A decorator that catches exceptions and logs them. 
# Requires that the function be an instance method and the instance has a self.logger.error() function
def catches_exceptions(fxn):
    def wrapper(self,*args,**kwargs):
        try:
            fxn(self,*args,**kwargs)
        except Exception as e:
            self.logger.error(f'Exception occurred during {fxn.__qualname__}: {str(e)}') 
            print_exc()
    return wrapper

# Accepts a dict and returns the dict data as an object of type cls. 
# Note, cls must be a dataclass or other class insantiatiable with keyword arguments.
def get_instance_from_dict(d : dict, cls):
    converted_dict = {}
    for field in fields(cls):
        val, type_name=None, None
        if field.name in d:
            val = d[field.name]
            
            type_name=field.type
            if type(type_name)!=str: #for some odd reason, type_name is sometimes a string literal and sometimes a class object (e.g. sometimes the string 'int' and sometimes the class int)
                type_name = type_name.__name__
        
        if val is not None:
            converted_dict[field.name]=TYPES[type_name](val)
        else:
            converted_dict[field.name]=None
    return cls(**converted_dict)
    
def print_table(rows,col_headers):
    rows = [col_headers, *rows]
    print(tabulate(rows, headers='firstrow', tablefmt='fancy_grid'))
    
def get_mapped_val(map,key):
    if key not in map:
        raise ValueError(f'unrecognized key: {key}')
    return map[key]