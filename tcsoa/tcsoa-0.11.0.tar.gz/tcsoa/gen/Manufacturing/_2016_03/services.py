from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Manufacturing._2016_03.ImportExport import NamesAndValuesMap, MfgExportToBriefcaseResponse, ImportManufaturingFeaturesInput
from tcsoa.gen.Manufacturing._2015_10.ImportExport import ImportManufaturingFeaturesResponse
from typing import List
from tcsoa.base import TcService


class ImportExportService(TcService):

    @classmethod
    def importManufacturingFeatures(cls, input: ImportManufaturingFeaturesInput) -> ImportManufaturingFeaturesResponse:
        """
        The PLMXML contains the data about the MFGs. The data contains the name of the MFGs. Their transform, their
        parts' connection, and their form attributes. There are two types of manufacturing features. Continuous MFG
        like arcweld ( Mfg0BVRArcWeld) and discrete MFGs like weld point (Mfg0BVRWeldPoint) and datum point
        (Mfg0BVRDatumPoint).
        For continuous MFGs, the PLMXML also contains the JT information.
        """
        return cls.execute_soa_method(
            method_name='importManufacturingFeatures',
            library='Manufacturing',
            service_date='2016_03',
            service_name='ImportExport',
            params={'input': input},
            response_cls=ImportManufaturingFeaturesResponse,
        )

    @classmethod
    def exportToBriefcase(cls, reason: str, sites: List[BusinessObject], objects: List[BusinessObject], transferOptionSet: BusinessObject, optionNameAndValues: NamesAndValuesMap, sessionOptionNamesAndValues: NamesAndValuesMap) -> MfgExportToBriefcaseResponse:
        """
        This operation is applicable specifically for Manufacturing Process Planner MPP  application.
        This operation combines following two operations.
        Teamcenter::Soa::GlobalMultiSite::_2008_06::ImportExport exportObjectsToOfflinePackage 
        Teamcenter::Soa::GlobalMultiSite::_2008_06::ImportExport requestExportToRemoteSites 
        In addition, it creates internal objects which are helpful in supplier collaboration use cases for
        manufacturing objects. Details in the use case section.
        
        Use cases:
        Use Case 1:  Exporting objects to the briefcase by transferring the ownership to the supplier.
        User wants to export Collaboration Context (CC) object in MPP to the briefcase to be used by the supplier at
        remote site. 
        The CC may contain product structure(s), bill of processes (BOP) such as plant BOP, plant structure etc.
        While exporting, the user wants to transfer ownership of few objects in the CC to the supplier so that the
        supplier can make changes to those objects on the other site.
        The user selects the CC and uses the menu option Tools, Export To, Briefcase...
        he menu option opens a dialog that allows user to set a destination site, a transfer option set, a list of
        traverse options and a list of session options. 
        In this case, all the objects which can be traversed by the transfer option set and session options will be
        exported into an output TC XML file. 
        The files and datasets related to exported objects will be downloaded and packed into the briefcase file along
        with the TC XML file.
        
        In addition, the internal object, Appearance Path Node (APN) will be created for the identified BOMLine objects
        in the CC. The BOMLine objects are identified based on the preference MERuleForBriefcaseExport.
        """
        return cls.execute_soa_method(
            method_name='exportToBriefcase',
            library='Manufacturing',
            service_date='2016_03',
            service_name='ImportExport',
            params={'reason': reason, 'sites': sites, 'objects': objects, 'transferOptionSet': transferOptionSet, 'optionNameAndValues': optionNameAndValues, 'sessionOptionNamesAndValues': sessionOptionNamesAndValues},
            response_cls=MfgExportToBriefcaseResponse,
        )
