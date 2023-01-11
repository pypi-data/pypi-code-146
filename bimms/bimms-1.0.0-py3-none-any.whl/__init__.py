""" Bio Impedance Measurement System, a portable and versatile platform for bio-impedance measurements"""

# Meta information
__title__           = 'BIMMS'
__version__         = '0.0.1'
__date__            = '2021–07–12'
__author__          = 'Louis Regnacq'
__contributors__    = 'Louis Regnacq, Florian Kolbl, Yannick Bornat'
__copyright__       = 'Louis Regnacq'
__license__         = 'CeCILL'

# Public interface
from .BIMMS import *
from .PostProcessing import *
from .Measures import *
from . import constants as cst