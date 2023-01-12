from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2015_10.FullTextSearch import Awp0FullTextSavedSearchInputObject2, Awp0FullTextSavedSearchInputObject, Awp0FullTextSavedSearchResponse
from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.AWS2._2015_10.DataManagement import DatasetTypesWithDefaultRelation
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class FullTextSearchService(TcService):

    @classmethod
    def modifyFullTextSavedSearch(cls, inputs: List[Awp0FullTextSavedSearchInputObject2]) -> Awp0FullTextSavedSearchResponse:
        """
        This operation modifies existing Awp0FullTextSavedSearch objects.
        """
        return cls.execute_soa_method(
            method_name='modifyFullTextSavedSearch',
            library='Internal-AWS2',
            service_date='2015_10',
            service_name='FullTextSearch',
            params={'inputs': inputs},
            response_cls=Awp0FullTextSavedSearchResponse,
        )

    @classmethod
    def createFullTextSavedSearch(cls, inputs: List[Awp0FullTextSavedSearchInputObject]) -> Awp0FullTextSavedSearchResponse:
        """
        This operation creates Awp0FullTextSavedSearch objects. Awp0FullTextSavedSearch objects are used to store
        information about a saved search such as search name, search string, search filters, etc.
        """
        return cls.execute_soa_method(
            method_name='createFullTextSavedSearch',
            library='Internal-AWS2',
            service_date='2015_10',
            service_name='FullTextSearch',
            params={'inputs': inputs},
            response_cls=Awp0FullTextSavedSearchResponse,
        )

    @classmethod
    def deleteFullTextSavedSearch(cls, objects: List[BusinessObject]) -> ServiceData:
        """
        This operation deletes saved searches. The saved search is unpinned before deleted.
        """
        return cls.execute_soa_method(
            method_name='deleteFullTextSavedSearch',
            library='Internal-AWS2',
            service_date='2015_10',
            service_name='FullTextSearch',
            params={'objects': objects},
            response_cls=ServiceData,
        )


class DataManagementService(TcService):

    @classmethod
    def getDatasetTypesWithDefaultRelation(cls, parent: BusinessObject, fileExtensions: List[str]) -> DatasetTypesWithDefaultRelation:
        """
        This operation returns the dataset type and reference information for a set of file extensions. This operation
        also returns the default paste relation for each Dataset type returned for the given input parent. Named
        references are Teamcenter objects that related to a specific data file.
        
        For each file extension, it is possible that it belongs to multiple dataset types. For such cases, all matching
        dataset types will be returned using the file extension as the key in the
        GetDatasetTypesWithDefaultRelationOutput structure.
        
        The order of file extension in the GetDatasetTypesWithDefaultRelationOutput structure may be different than the
        order of file extension input. This operation inserts file extensions that match the default dataset type
        defined in AE_default_dataset_type preference at the beginning of the list.
        
        This operation uses the TC_Dataset_Import_Exclude_Wildcard preference to determine if wildcard may be used in
        file extension input. If the preference is set and file extension is set to asterisk, this operation will
        return all data set types that allow wildcards in its name reference in Teamcenter.
        
        Default paste relation for each Dataset type returned is determined by evaluating preferences
        __default_relation and/or _default_relation. The preference __default_relation takes precedence over
        _default_relation.
        
        Details about these four preferences can be found in Preferences and Environment (Variables Reference
        Configuration preferences, under Data management preferences).
        """
        return cls.execute_soa_method(
            method_name='getDatasetTypesWithDefaultRelation',
            library='Internal-AWS2',
            service_date='2015_10',
            service_name='DataManagement',
            params={'parent': parent, 'fileExtensions': fileExtensions},
            response_cls=DatasetTypesWithDefaultRelation,
        )
