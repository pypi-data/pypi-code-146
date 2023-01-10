from __future__ import annotations

from tcsoa.gen.BusinessObjects import Awb0Element
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ApplyMarkupData(TcBaseObj):
    """
    The parameter to apply Markup.
    
    :var element: Awb0Element object for which Markup is to be applied
    :var recursive: Flag that indicates whether to apply all Markups for all elements under the specified element.
    :var evaluate: Flag that indicates whether to check write access (true) or actually modify (false) the element.
    """
    element: Awb0Element = None
    recursive: bool = False
    evaluate: bool = False
