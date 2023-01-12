# -*- coding: utf-8 -*-
# Copyright (c) 2023 Miroslav Hruska
"""
*********
Shortcuts
*********

Abbreviated names of common functions from :mod:`~daul.pandas_utils`.

Overview
********

Shortcuts: :class:`~pandas.DataFrame` columns
=============================================

.. autosummary::
   pduc
   pdutc
   pdufc
   pdca

Shortcuts: Conversion of :class:`~pandas.DataFrame`\ s to dictionaries
======================================================================

.. autosummary::
   pdtcd
   pdtcdf
   pdtcdfd

   pdtclvd
   pdtclvdf
   pdtclvdfd   

Shortcuts: Inner frames
=======================

.. autosummary::
   pdioc

Shortcuts: Other
================

.. autosummary::
   pdri

"""


#%% Modules
# global
from daul import pandas_utils as _pdu
  
#%% * Columns
pduc = _pdu.update_column
pdutc = _pdu.update_tuple_col
pdufc = _pdu.update_fixed_column 
pdca = _pdu.column_apply 

#%% * Dictionaries
pdtcd   = _pdu.twocol_dict 
pdtcdf  = _pdu.twocol_dictf
pdtcdfd = _pdu.twocol_dictfd

#%% * Listvaldicts
pdtclvd   = _pdu.twocol_listvaldict 
pdtclvdf  = _pdu.twocol_listvaldictf
pdtclvdfd = _pdu.twocol_listvaldictfd

#%% * Inner frames
pdioc = _pdu.include_outer_col

#%% * Other
pdri = _pdu.renumber_index 
