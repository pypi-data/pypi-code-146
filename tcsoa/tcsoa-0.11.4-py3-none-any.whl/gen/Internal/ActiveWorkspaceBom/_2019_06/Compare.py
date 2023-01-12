from __future__ import annotations

from tcsoa.gen.BusinessObjects import Awb0Element, Awb0ProductContextInfo
from tcsoa.gen.Internal.ActiveWorkspaceBom._2018_12.Compare import CompareOptionsMap
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CompareContentAsyncData2(TcBaseObj):
    """
    Input containing Awb0Element objects, configuration information and various actions using which compare is to be
    performed.
    
    :var source: 'CompareContentAsyncInfo' for source object to compare.
    :var target: 'CompareContentAsyncInfo' data for target object to compare.
    :var compareOptionsMap: A map (string, list of strings) containing an option for compare as key and list of its
    associated attributes as values.This can have equivalence criterias to use , list of partial match properties to
    use for comparison.
    """
    source: CompareContentAsyncInfo2 = None
    target: CompareContentAsyncInfo2 = None
    compareOptionsMap: CompareOptionsMap = None


@dataclass
class CompareContentAsyncInfo2(TcBaseObj):
    """
    Input containing Awb0Element objects, configuration information and depth describing how deep traversal and compare
    to be performed.
    
    :var element: Awb0Element whose children are to be compared.
    :var productContextInfo: Awb0ProductContextInfo containing configuration information for the element.
    :var depth: Level to which the source or target is to be expanded for compare.
    
    If depth > 0 it signifies level to which the source is target is to be expanded for compare.
    If depth == 0 then only leaf nodes will be compared.
    If depth == -1 then all levels of structure will be compared.
    """
    element: Awb0Element = None
    productContextInfo: Awb0ProductContextInfo = None
    depth: int = 0
