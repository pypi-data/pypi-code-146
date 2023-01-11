from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, PSBOMView, AssemblyArrangement, ItemRevision, BOMWindow, Item, ConfigurationContext
from typing import Dict, List
from tcsoa.gen.Cad._2007_01.StructureManagement import RevisionRuleConfigInfo
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CreateWindowsInfo3(TcBaseObj):
    """
    Main input structure that defines Item or ItemRevision of the top line in the BOMWindow. In the input, the
    BOMWindow is mutually exclusive with Item, ItemRevision and PSBOMView. If BOMWindow and Item, ItemRevision and
    PSBOMView objects are sent it will be considered as re-configure with BOMWindow. In the input, either
    revRuleConfigInfo object and objectsForConfigure object (variant rules or saved option set) or configContext object
    is required, the effGrpRevList object is used to re-configure BOMWindow if configContext object is not provided.
    
    :var clientId: Identifier that helps the client to track the objects created.
    :var bomWindow: BOMWindow object to be reconfigured. Must be NULLTAG when creating a new window.
    :var bomWinPropFlagMap: A map (string, string) of property names and respective value that needs to be set on
    window. User need to populate this map with following property string values as key and true or false as value,
    which will be set or unset in the window
    Valid property key values are:
    "show_unconfigured_variants"
    "show_unconfigured_changes"
    "show_suppressed_occurrences"
    "is_packed_by_default"
    "show_out_of_context_lines"
    "fnd0show_uncnf_occ_eff"
    "fnd0bw_in_cv_cfg_to_load_md".
    :var item: Item for top line of new window, or NULLTAG if itemRev is specified. Must be NULLTAG when reconfiguring
    an existing window.
    :var itemRev: ItemRevision for top line of new window, or NULLTAG if item is specified in which case the default
    revision will be used. Must be NULLTAG when reconfiguring an existing window.
    :var bomView: PSBOMView to be used when creating a new window, or NULLTAG to use the default view. Must be NULLTAG
    when reconfiguring an existing window.
    :var revRuleConfigInfo: Structure with information about RevisionRuleConfigInfo.
    :var objectsForConfigure: A list of VariantRule or StoredOptionSet stored option set object to set on this window.
    :var activeAssemblyArrangement: Active AssemblyArrangement of the BOMWindow.
    :var configContext: ConfigurationContext object reference.
    :var effGrpRevList: A list of Fnd0EffectivityGrp  objects, effGrpRevList is used along with BOMwindow and to
    configure or re-configure them.
    """
    clientId: str = ''
    bomWindow: BOMWindow = None
    bomWinPropFlagMap: StringMap2 = None
    item: Item = None
    itemRev: ItemRevision = None
    bomView: PSBOMView = None
    revRuleConfigInfo: RevisionRuleConfigInfo = None
    objectsForConfigure: List[BusinessObject] = ()
    activeAssemblyArrangement: AssemblyArrangement = None
    configContext: ConfigurationContext = None
    effGrpRevList: List[ItemRevision] = ()


"""
This is map of string Key to string Value.
"""
StringMap2 = Dict[str, str]
