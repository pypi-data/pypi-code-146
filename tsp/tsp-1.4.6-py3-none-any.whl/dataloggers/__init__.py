from .HOBO import HOBO, HOBOProperties
from .FG2 import FG2
from .GP5W import GP5W
from .Geoprecision import detect_geoprecision_type
from .logr import LogR

HOBO.__module__ = __name__
HOBOProperties.__module__ = __name__
FG2.__module__ =__name__
GP5W.__module__ = __name__
LogR.__module__ = __name__

__all__ = ['HOBO','HOBOProperties',
           'FG2','GP5W', 'detect_geoprecision_type',
           'LogR']
