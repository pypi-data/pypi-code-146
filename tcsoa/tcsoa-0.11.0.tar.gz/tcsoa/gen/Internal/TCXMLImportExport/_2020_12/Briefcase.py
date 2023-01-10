from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, POM_imc, TransferOptionSet
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ImportObjectsFromBriefcaseInput(TcBaseObj):
    """
    The struct for defining the input arguments required by the importObjectsFromBriefcase operation.
    
    :var bczFileTicket: The FMS file ticket for the source briefcase file. User needs to upload the briefcase file to
    the FMS transient volume to generate the file ticket.
    :var transferOptionSet: The Transfer Option Set object used for data scoping.
    :var overrideOptions: The name and value pairs of options that will override the same options defined in the input
    Transfer Option Set.
    :var sessionOptions: The name and value pair options to control the export session behavior. The supported options
    are:
    1. dry_run: valid values are True/False, specifies that the briefcase import report is generated which has
    discrepancy if any.
    2. ValidateImport: valid values are True/False, specifies that the TCXML is validated against any discrepancy.
    3. validateXMLBeforeXslt: valid values are True/False, specifies that the TCXML is validated before mapping is done.
    """
    bczFileTicket: str = ''
    transferOptionSet: TransferOptionSet = None
    overrideOptions: List[NameAndValue] = ()
    sessionOptions: List[NameAndValue] = ()


@dataclass
class NameAndValue(TcBaseObj):
    """
    NameAndValue structure represents an option name-value pair.
    
    :var optionName: The name of the option name-value pair.
    :var optionValue: The value of the option name-value pair.
    """
    optionName: str = ''
    optionValue: str = ''


@dataclass
class ExportObjectsToBriefcaseInput(TcBaseObj):
    """
    The struct for defining the input arguments required by the exportObjectsToBriefcase operation.
    
    :var rootObjects: The root objects to be exported.
    :var targetSite: The target site.
    :var transferOptionSet: The Transfer Option Set object used for data scoping.
    :var overrideOptions: The name and value pairs of options that will override the same options defined in the input
    Transfer Option Set.
    :var sessionOptions: The name and value pair options to control the export session behavior. The supported options
    are:
    1. pkgDatasetName: valid values are "Dataset name", specifies the output briefcase Dataset name.
    2. revRule: valid values are "Revision Rule name", specifies the Reivsion Rule that will be applied on the root
    object for configured BOM export.
    3. varRule: valid values are "Variant Rule name", specifies the Variant Rule that associated to the root object for
    configured BOM export.
    4. dry_run: valid values are True/False, specifies that the briefcase export report is generated which has
    discrepancy if any.
    5. validateXML: valid values are True/False, specifies that the TCXML is validated against any discrepancy.
    6. validateXMLBeforeXslt: valid values are True/False, specifies that the TCXML is validated before mapping is done.
    7. modified_objects_only: valid values are True/False, specifies the option for delta export.
    8. opt_sync_previous_delta: valid values are True/False, specifies the option for force re-export.
    9. OwnershipTransfer: valid values are True/False, specifies the option to do ownership transfer.
    10. objsForOwnXfer: valid values are in the format of "<site-id>:<object-uid1,object-uid2&hellip;>", specifies the
    objects for ownership transfer.
    11. processUnconfiguredVariants: valid values are True/False, specifies the option to process the BOMLines that are
    configured out by the Variant Rule.
    12. processUnconfiguredByOccEff: valid values are True/False, specifies the option to process the BOMLines that are
    configured out by Occurrence Effectivity.
    13. processSuppressedOcc: valid values are True/False, specifies the option to process the suppressed BOMLines.
    14. processUnconfiguredChanges: valid values are True/False, specifies the option to process the BOMLines that are
    configured out by Incremental Change.
    15. ContinueOnError: valid values are True/False, specifies the option to continue the export on partial error.
    """
    rootObjects: List[BusinessObject] = ()
    targetSite: POM_imc = None
    transferOptionSet: TransferOptionSet = None
    overrideOptions: List[NameAndValue] = ()
    sessionOptions: List[NameAndValue] = ()
