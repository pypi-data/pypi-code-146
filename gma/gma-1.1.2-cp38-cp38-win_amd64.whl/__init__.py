# -*- coding: utf-8 -*-

try: 
    import os, warnings
    Here = os.path.dirname(__file__)
    if Here not in os.environ['PATH']:
        os.environ['PATH'] = Here + ';' + os.environ['PATH']
    try:
        os.add_dll_directory(Here) 
    except:
        os.environ.setdefault('PATH', Here)
    warnings.filterwarnings("ignore")
finally:
    del os, warnings, Here

try:
    from . import rsvi, climet, math, osf, rasp, vesp, smc, raa, config
    from .algorithm.core.dataio import Open
 
except ModuleNotFoundError as F:
    Package = str(F).split()[-1].replace("'",'').split('.')[0]
    if Package == 'osgeo':
        MESS = "Missing GDAL library! See https://gdal.org/api/python_bindings.html"
    else:
        MESS = f"The {Package} library is missing, please install it with 'pip install {Package}' in the terminal!"
    
    raise ModuleNotFoundError(MESS) from None
    
except ImportError as I:
    Module = str(I).split()
    raise ImportError(str(I)) from None

try:
    from importlib.metadata import version
    __version__ = version(__name__)
except: 
    __version__ = "unknown"
finally:
    del version
    
    
try:
    __gdalversion__ = rasp._rasp.gdal.__version__
except:
      raise ImportError('Currently installed GDAL is not supported, please update GDAL!')
      
if __gdalversion__ < '3.4.1':
    raise ImportError(f'The GDAL version is too low, the current version {__gdalversion__}, the minimum version is 3.4.1, please update GDAL!')




