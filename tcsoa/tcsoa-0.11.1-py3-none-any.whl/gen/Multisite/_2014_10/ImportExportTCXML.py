from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ImportExportOptionsInfo(TcBaseObj):
    """
    The ImportExportOptionsInfo structure holds the name-value pairs of import/export option(s). Value can be single or
    multiple valued. The import/export options influence the business object import/export and has default value.
    
    :var optionName: The name of the option. Valid values are as per below table.
    
    Supported ImportExportOptionsInfo options:  
    
                  Option Name                  Description                                                             
    Default value
    opt_exp_prot_obj        Set this option to False so process will stop when exporting import 
                            or export protected workspace objects.                                                  
    False
    opt_do_struct           Set this option to TRUE to Transfer site ownership of the Top-Level
                            item only and export all components with no site ownership transfer. 
                            Applicable only if transfer_ownership is true.                                          
    False 
    opt_trans_prot_comp     Set this option to TRUE to exclude all components that have no 
                            TRANSFER_OUT/TRANSFER_IN privilege at owning site 
                            for site ownership transfer.
                            Applicable only if transfer_ownership is true.                                          
    False 
    opt_exp_prot_comp       Set this option to TRUE to exclude all components that have no export
                            and/or import privileges granted at the owning site.                                    
    False
            
    opt_entire_bom             Set this option to TRUE to export all components if the item selected is an assembly.   
      False 
    opt_all_ds_files         Set this option to TRUE to export all dataset files.                                    
    True 
    opt_all_ds_vers         Set this option to TRUE to export all dataset versions                                     
    True 
    opt_folder_contents     Set this option to TRUE to export objects in folder.                                     
    False 
    opt_de_rlz_item         Set this option to TRUE to send BOM structure and CPD structure together                 
    False 
    opt_workset_rlz_de         Set this option to TRUE to send Design Element with Workset and subset                  
       False 
    opt_cpd_p2s_skip         Set this option to True to exclude all Reference Geometry/Connected Element 
                            relations from Cpd0DesignElement.                                                        
    True 
    transfer_ownership      Set this option to True to transfer site ownership of selected objects.                    
    False 
    owning_user                Set the owning user for objects at remote site                                          
      None
    owning_group            Set the owning group for objects at the remote site                                        
    None
    include_modified_only     Include only objects that have been modified since the last transfer are exported.
                            Mutually exclusive with the  transfer_ownership option.                                 
    False
    include_relations       List of relations which will be included in export. 
                            The relation must be passed by Teamcenter relation name 
                            and be supported for include processing by the option set.                                
    None
    exclude_relations        List of relations which will be excluded in export. 
                            The relation must be passed by Teamcenter relation name 
                            and be supported for exclude processing by the option set.                                
    None
            
    
    Item Options, only one may be passed. 
    Option Name                              Description                                                               
                                                                         Value(s)
    opt_rev_select                           Process all revisions.                                                    
                                                                         allItemRevisions   
    opt_rev_select                              Process only the latest revision regardless of release status.         
                                                               latestRevisionOnly
    opt_rev_select                           Process only the latest revision regardless of release status.            
                                                            latestWorkingRevisionOnly
    opt_rev_select                           Process only the latest working revision. If there is none, then process
    the latest released                                 latestWorkingAnyOnly
    opt_rev_select                           Process only the latest released revision.                                
                                                                    latestReleasedRevisionOnly
    opt_rev_select                           Process only the selected revision. Applicable only if an ItemRevision is
    the target.                                         selectedRevisionsOnly
    opt_rev_select                           Process only revisions with a specific release status. Supported release
    statuses are defined in the option set.       First value=specificStatusOnly Second value=Release Status Name 
    :var optionValue: A list of values for the optionName.
    """
    optionName: str = ''
    optionValue: List[str] = ()


@dataclass
class RemoteExportFailurePerOperation(TcBaseObj):
    """
    Returns failures from all sites during export of objects.
    
    :var sites: A list of sites by name for this operation.
    :var failuresPerOperation: A list of failure information from sites.
    """
    sites: List[str] = ()
    failuresPerOperation: List[RemoteExportFailurePerSite] = ()


@dataclass
class RemoteExportFailurePerSite(TcBaseObj):
    """
    This structure returns failures encountered during export to a site.
    
    The following errors may be returned in the RemoteExportFailurePerSite structure.
    
    96001 - The bulk "Iman Export Record" (IXR) creation or update has failed during the TC XML based multisite
    operation. 
    96002 - The "Export Commit" process has failed during the TC XML based multisite operation. 
    96003 - The processing callback function is not set for the TC XML based multisite operation.
    96004 - The "Export Record" could not be created during the TC XML based multisite operation. 
    96005 - The "Export Record" could not be created during the TC XML based multisite operation due to an invalid
    value for the attribute 
    96023 - An error has been encountered during the access of the volume during the TC XML based operation. 
    96024 - An invalid input data was found while updating the fast synchronization tables during the TC XML based
    operation. Please refer to the log files for details.
    96025 - The save of "Iman Export Record" (IXR) has encountered partial errors during the TC XML based multisite
    operation. Please refer to the log files for details.
    96026 - The conversion of the input parameters of the utility to its representative Option Set has failed.
    
    
    :var failureCodes: A list of failure codes for this operation.
    :var failureObjects: A list of objects that have failed to export.
    :var failureStrings: A list of error strings for this operation.
    """
    failureCodes: List[int] = ()
    failureObjects: List[BusinessObject] = ()
    failureStrings: List[str] = ()


@dataclass
class RemoteExportInfo(TcBaseObj):
    """
    The RemoteExportInfo structure takes an option set name and export options as input. The option set and options
    will affect the final state of the exported objects at the target sites. There is system default option set and
    additional option sets may be created by the administrator.  When the option set and options are not specified in
    the RemoteExportInfo structure, the system default option set and default options will be used.
    
    :var objects: A list of target objects.
    :var targetSites: A list of target sites by site name.
    :var optionSetName: Name of option set used for export.
    :var reason: The reason for export. It may be empty.
    :var exportOptions: A list of export options.
    """
    objects: List[BusinessObject] = ()
    targetSites: List[str] = ()
    optionSetName: str = ''
    reason: str = ''
    exportOptions: List[ImportExportOptionsInfo] = ()


@dataclass
class RemoteExportResponse(TcBaseObj):
    """
    The RemoteExportResponse returns detailed partial failure information in RemoteExportFailurePerOperation structures
    along with a ServiceData.
    
    This operation can return errors from different sites and each target object may have different errors. The
    RemoteExportFailurePerOperation structure will be used to report failures instead of the ServiceData to allow for
    the detailed reporting of site specific errors.  The RemoteExportFailurePerOperation structure will report what
    which site the errors are returned from. The list RemoteExportFailurePerSite structures will return errors for a
    specific target object(s). 
    
    
    :var failureInfo: The partial failure information specfic to site.
    :var serviceData: The Service Data return. The objects sucessfully exported are added to the Plain objects list.  
    """
    failureInfo: List[RemoteExportFailurePerOperation] = ()
    serviceData: ServiceData = None


@dataclass
class RemoteImportFailurePerOperation(TcBaseObj):
    """
    This structure returns all the failures during import for a set of objects
    
    :var sites: A list of sites by name for this set of failure data.
    :var failuresPerOperation: A list of failure information from sites.
    """
    sites: List[str] = ()
    failuresPerOperation: List[RemoteImportFailurePerSite] = ()


@dataclass
class RemoteImportFailurePerSite(TcBaseObj):
    """
    following errors may be returned in the RemoteImportFailurePerSite structure.
    
    96001 - The bulk "Iman Export Record" (IXR) creation or update has failed during the TC XML based multisite
    operation. 
    96002 - The "Export Commit" process has failed during the TC XML based multisite operation. 
    96003 - The processing callback function is not set for the TC XML based multisite operation.
    96004 - The "Export Record" could not be created during the TC XML based multisite operation. 
    96005 - The "Export Record" could not be created during the TC XML based multisite operation due to an invalid
    value for the attribute 
    96023 - An error has been encountered during the access of the volume during the TC XML based operation. 
    96024 - An invalid input data  was found while updating the fast synchronization tables during the TC XML based
    operation. Please refer to the log files for details.
    96025 - The save of "Iman Export Record" (IXR) has encountered partial errors during the TC XML based multisite
    operation. Please refer to the log files for details.
    96026 - The conversion of the input parameters of the utility to its representative Option Set has failed.
    
    
    :var failureCodes: A list of failure codes for this operation.
    :var failureObjects: A list of objects that have failed to import
    :var failureStrings: A list of error strings for this operation.
    """
    failureCodes: List[int] = ()
    failureObjects: List[BusinessObject] = ()
    failureStrings: List[str] = ()


@dataclass
class RemoteImportInfo(TcBaseObj):
    """
    The RemoteImportInfo structure takes an option set name and export options as input. The option set and options
    will affect the final state of the exported objects at the target sites. There is system default option set and
    additional option sets may be created by the administrator. When the option set and options are not specified in
    the RemoteExportInfo structure, the system default option set and default options will be used. Please find the
    default option values in the list of supported options below. 
    The targeted objects can be of two types.
    1.    A replica PomObject which has been previously imported into the local site
    2.    A PublishedObject which is proxy for remote object. This object must minimally contain UID and the owning
    site information. 
    
    
    :var objects: A list of target objects.
    :var optionSetName: Name of option set used for import.
    :var reason: The reason for this import. It may be empty.
    :var importOptions: A list of import options.
    """
    objects: List[BusinessObject] = ()
    optionSetName: str = ''
    reason: str = ''
    importOptions: List[ImportExportOptionsInfo] = ()


@dataclass
class RemoteImportResponse(TcBaseObj):
    """
    The RemoteImportResponse returns detailed partial failure information in RemoteImportFailurePerOperation structures
    along with a ServiceData. 
    This operation can return errors from different sites and each target object may have different errors per site. 
    The RemoteImportFailurePerOperation structure will be used to report failures instead of the ServiceData to allow
    for the detailed reporting of site specific errors.  The RemoteImportFailurePerOperation structure will report what
    which site the errors are returned from. The list RemoteImportFailurePerSite structures will return errors for a
    specific target object(s). 
    
    
    :var failureInfo: The partial failure information specfic to site.
    :var serviceData: The Service Data return. Objects sucessfully imported will be added to the Updated object list.
    """
    failureInfo: List[RemoteImportFailurePerOperation] = ()
    serviceData: ServiceData = None


@dataclass
class RemoteImportUIDInfo(TcBaseObj):
    """
    The RemoteImportUIDInfo structure takes an option set name and export options as input. The option set and options
    will affect the final state of the exported objects at the target sites. There is system default option set and
    additional option sets may be created by the administrator. When the option set and options are not specified in
    the RemoteExportInfo structure, the system default option set and default options will be used. 
    
    :var objectUIDs: A list of target objects in UID form.
    :var owningSiteIds: A list of owning sites by site ids for each object in objectUIDs
    :var optionSetName: Name of option set used for import.
    :var reason: The reason for this import. It may be empty.
    :var importOptions: A list of import options.
    """
    objectUIDs: List[str] = ()
    owningSiteIds: List[int] = ()
    optionSetName: str = ''
    reason: str = ''
    importOptions: List[ImportExportOptionsInfo] = ()
