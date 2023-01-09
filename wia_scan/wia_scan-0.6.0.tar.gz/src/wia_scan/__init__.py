"""
wia_scan 0.6.0
==========

A simple utility for using document scanners that support Windows Image Acquisition (WIA) and is
easy to install. If your scanner works using Windows Fax and Scan, there is a good chance it will
work with this python script.

See https://github.com/JonasZehn/python_wia_scan for usage and source.

"""

__version__ = "0.6.0"

from .scan_functions import *
from .scan_main import *
