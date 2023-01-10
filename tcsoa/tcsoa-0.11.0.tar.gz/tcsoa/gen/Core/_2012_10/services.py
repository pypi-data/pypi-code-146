from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Core._2012_10.DataManagement import TraceabilityReportOutput1, TraceabilityInfoInput1, GetDatasetTypesWithFileExtensionResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def getTraceReport(cls, input: List[TraceabilityInfoInput1]) -> TraceabilityReportOutput1:
        """
        This operation will generate a Trace Report on the objects selected by user. The report will contain
        information about complying as well as defining objects which are connected to selected object using
        FND_TraceLink, or its subtype. This operation will check if there is any TraceLink relation starting or ending
        from selected object(s). If TraceLink relation exists for selected object(s), then it gets the other end of
        TraceLink relation and generates a trace report.  
        
        Trace links can be between following objects: 
        
        * Between occurrences of an ItemRevision 
        * Between any two WorkspaceObject. 
        
        Following will be added, in addition to existing getTraceReport operation: 
        
        * If scope of search structure is defined for the getting Trace Report in input of this operation by sending
        top lines of BOMWindow instances, then matching TraceLink instances within the scope windows will be returned. 
        * If input of this operation is having list of object type names, then object type filter will be applied to
        target objects of TraceLink. 
        * If input of this operation is having list of TraceLink type names, then those types of TraceLink will be
        returned in Trace Report. 
        * If propertyFilterInput is given in the input of this operation, then the additional filter of property will
        be applied on the output before sending to client. 
        * Trace report tree will be sorted for given property, sort direction can also be defined, if not defined then
        it will get default sorted in ascending direction. 
        * The output of this operation can be either sent to rich client to build the report or to MSExcel application. 
        * User can export this trace report to MSExcel application by sending appropriate exportTo mode in input. If
        the mode of export is "TraceReportMSExcelExport", then trace report will be exported to .xlsm file and this
        file ticket will be sent to rich client. Then rich client will download the file and open MSExcel application. 
        """
        return cls.execute_soa_method(
            method_name='getTraceReport',
            library='Core',
            service_date='2012_10',
            service_name='DataManagement',
            params={'input': input},
            response_cls=TraceabilityReportOutput1,
        )

    @classmethod
    def refreshObjects2(cls, objects: List[BusinessObject], lockObjects: bool) -> ServiceData:
        """
        This operation is used to reload the in-memory representation of the objects from the database.
        Any references to the object will still be valid. Any in-memory changes to the original object will be lost. If
        the object has been changed in the database since it was last loaded, then those changes will not be present in
        memory. 
        The operation updates the in memory representation to reflect database changes. 
        
        If the lockObjects flag is true then it will aquire write lock on objects otherwise operation will release the
        write lock on the business objects. 
        This is useful when client needs to do an in-process lock and unlock for shorter duration that does not require
        checkout or checkin mechanism. Client caling this operation to lock the objects must unlock those objects by
        callng this operation.
        This operation must be used in pairs to lock and unlock the objects.
        
        Use cases:
        Use this operation to do bulk lock & bulk unlock of Input Objects.
        """
        return cls.execute_soa_method(
            method_name='refreshObjects2',
            library='Core',
            service_date='2012_10',
            service_name='DataManagement',
            params={'objects': objects, 'lockObjects': lockObjects},
            response_cls=ServiceData,
        )

    @classmethod
    def getDatasetTypesWithFileExtension(cls, fileExtensions: List[str]) -> GetDatasetTypesWithFileExtensionResponse:
        """
        This operation returns the dataset type and reference information for a set of file extensions. Named
        references are Teamcenter objects that relate to a specific data file. For each file extension, it is possible
        that it belongs to multiple dataset types. For such cases, all matching dataset types will be returned using
        the file extension as the key in the GetDatasetTypesWithFileExtensionOutput structure. The order of file
        extension in the GetDatasetTypesWithFileExtensionOutput structure may be different than the order of file
        extension input. This operation will insert file extensions that match the default dataset type defined in
        AE_default_dataset_type preference at the beginning of the list. This operation uses
        TC_Dataset_Import_Exclude_Wildcard preference to determine if wildcard may be used in file extension input. If
        the preference is set and file extension is set to asterisk, this operation will return all data set types that
        allow wildcards in its name reference in Teamcenter. Details about these two preferences can be found in
        Preferences and Environment (Variables Reference Configuration preferences, under Data management preferences).
        """
        return cls.execute_soa_method(
            method_name='getDatasetTypesWithFileExtension',
            library='Core',
            service_date='2012_10',
            service_name='DataManagement',
            params={'fileExtensions': fileExtensions},
            response_cls=GetDatasetTypesWithFileExtensionResponse,
        )
