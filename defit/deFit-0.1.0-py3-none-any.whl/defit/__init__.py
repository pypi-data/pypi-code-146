__version__ = '0.0.1'
'''
defit
=====
Provides

Use numerical optimization to fit ordinary differential equations (ODEs) to time series data to examine the dynamic relationships between variables or the characteristics of a dynamical system. It can now be used to estimate the parameters of ODEs up to second order.

How to use the documentation
----------------------------
Documentation is available in two forms: docstrings provided
with the code, and a loose standing reference guide, available from
`the defit homepage <https://github.com/yueqinhu/defit>`_.

Use the built-in ``help`` function to view a function's docstring::

>>> from defit import defit
>>> help(defit)


'''
from .defit import *