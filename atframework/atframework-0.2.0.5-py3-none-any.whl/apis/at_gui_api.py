"""
Created on Mar 03, 2021

@author: Siro

"""
from atframework.model.at_closing import AtClosing
from atframework.model.at_opening import AtOpening
from atframework.model.at_waiting import AtWaiting
from atframework.model.at_show import AtShow
from atframework.model.at_click import AtClick
from atframework.model.at_type import AtType
from atframework.model.at_select import AtSelect
from atframework.model.at_get import AtGet
from atframework.model.at_expand import AtExpand
from atframework.model.at_scroll import AtScroll
from atframework.model.at_clear import AtClear



class AtGuiAPI(AtClosing, AtOpening, AtWaiting, AtClear,
                  AtType, AtShow, AtClick, AtSelect,
                  AtGet, AtExpand, AtScroll):
    """
    Integrate all GUI api into this class, Use this class to drive test steps
    """
