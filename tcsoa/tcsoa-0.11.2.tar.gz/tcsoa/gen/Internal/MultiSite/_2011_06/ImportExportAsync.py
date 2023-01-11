from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ImportExportOptionsInfo(TcBaseObj):
    """
    The 'ImportExportOptionsInfo' structures holds the name/value pairs of export option(s). Value can be single or
    multiple valued. The export options influences the business object export and has default value.
    
    :var optionName: Export option name for remote export.
    :var optionValue: Values for remote export option (can be multi-valued strings).
    """
    optionName: str = ''
    optionValue: List[str] = ()


@dataclass
class RemoteExportInfo(TcBaseObj):
    """
    The 'RemoteExportInfo' holds the business object and related information meant for remote export.
    
    :var object: Business object for remote export operation.
    :var reason: Reason for exporting business object. Its not mandatory to pass any reason, empty string can be passed.
    :var targetSites: List of sites, where business object export will be performed.
    :var remoteCheckout: Along with remote export, if the remote check out needs to be performed, pass true. Only one
    target site should be provided with true value.
    :var checkoutId: Checkout identifier(empty string can be passed).
    :var exportOptions: List of options to influence the business object export.
    """
    object: BusinessObject = None
    reason: str = ''
    targetSites: List[str] = ()
    remoteCheckout: bool = False
    checkoutId: str = ''
    exportOptions: List[ImportExportOptionsInfo] = ()
