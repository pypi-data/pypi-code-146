from __future__ import annotations

from tcsoa.gen.Manufacturing._2013_12.Model import AppearancePathInput, ComputeAppearancePathResponse
from tcsoa.gen.Manufacturing._2013_12.ResourceManagement import GetVendorCatalogInfoResponse, ImportVendorCatalogHierarchyResponse, GetStepP21FileCountsResponse, ImportStepP21FilesResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ResourceManagementService(TcService):

    @classmethod
    def getStepP21FileCounts(cls, classIDs: List[str]) -> GetStepP21FileCountsResponse:
        """
        This operation retrieves the count of STEP P21 product files that are available in a GTC vendor catalog in and
        below the specified classes.
        """
        return cls.execute_soa_method(
            method_name='getStepP21FileCounts',
            library='Manufacturing',
            service_date='2013_12',
            service_name='ResourceManagement',
            params={'classIDs': classIDs},
            response_cls=GetStepP21FileCountsResponse,
        )

    @classmethod
    def getVendorCatalogInfo(cls) -> GetVendorCatalogInfoResponse:
        """
        This operation retrieves information about the GTC vendor catalogs that are available on the Teamcenter server
        machine. The multi-value preference "MRMGTCVendorCatalogRootDir" allows you to specify one or multiple root
        directories where those catalogs can be stored. This operation scans the given directories for GTC vendor
        catalogs and returns detailed information for each catalog.
        """
        return cls.execute_soa_method(
            method_name='getVendorCatalogInfo',
            library='Manufacturing',
            service_date='2013_12',
            service_name='ResourceManagement',
            params={},
            response_cls=GetVendorCatalogInfoResponse,
        )

    @classmethod
    def importStep3DModels(cls, icoIDs: List[str]) -> ServiceData:
        """
        This operation imports STEP 3D model files for Generic Tool Catalog (GTC) vendor catalog components. The STEP
        files are converted to NX part and to JT file format and imported into Teamcenter. If needed, items are created
        for the Classification objects (ICO). One UGMaster dataset for the NX part file and one DirectModel dataset for
        the JT file is created below the (new) item.
        
        Use cases:
        There are two different use cases:
            A) The specified ICO is classified in a GTC vendor catalog class
        (the ICO has an attribute -159003 "3D Model file name")
            B) The specified ICO is classified in an MRL MyComponents class
        (the ICO does not have an attribute -159003 "3D Model file name")
        
        In use case A, this operation retrieves the file name of the 3D model directly from GTC attribute 
        -159003 "3D Model file name".
        (Another attribute ID instead of -159003 can be defined in the "MRMGTC3DModelAttributeID" preference.)
        
        In use case B, the SOA operation checks if there is an Manufacturing Resource Libraray (MRL) attribute -40930
        "Vendor Reference Object ID" in the given ICO. This attribute is used to store the reference from the MRL
        MyComponents ICO to the GTC vendor catalog ICO. If this attribute exists in the ICO's class and has a valid ICO
        ID as value, the 3D model file name will be retrieved from the referenced ICO. (see use case A)
        (Another attribute ID instead of -40930 can be defined in the "MRMGTCReferenceObjectAttributeID"preference.)
        
        The SOA operation retrieves the information about the server-sided directory, where all STEP 3D models of the
        catalog are stored, based on the class of the GTC vendor catalog ICO.
        
        If there is a problem during importing one of the 3D models, the operation will continue importing the 3D
        models of the following ICOs.
        
        Note: The Graphics Builder has to be configured properly for this operation to work.
        """
        return cls.execute_soa_method(
            method_name='importStep3DModels',
            library='Manufacturing',
            service_date='2013_12',
            service_name='ResourceManagement',
            params={'icoIDs': icoIDs},
            response_cls=ServiceData,
        )

    @classmethod
    def importStepP21Files(cls, classID: str, importOptions: int) -> ImportStepP21FilesResponse:
        """
        This operation imports STEP P21 files containing the attributes values of manufacturing components (vendor
        product data) into the vendor catalog Classification classes. 
        It creates Classification objects (ICOs) and associated data. Depending on the available data in the input
        directory, the associated items might be created to store drawing files and/or images.
        """
        return cls.execute_soa_method(
            method_name='importStepP21Files',
            library='Manufacturing',
            service_date='2013_12',
            service_name='ResourceManagement',
            params={'classID': classID, 'importOptions': importOptions},
            response_cls=ImportStepP21FilesResponse,
        )

    @classmethod
    def importVendorCatalogHierarchy(cls, vendorCatalogRootDir: str, importOptions: int) -> ImportVendorCatalogHierarchyResponse:
        """
        This operation imports the Classification class hierarchy (including class icons and images) of a GTC (Generic
        Tool Catalog) vendor catalog. The catalog hierarchy will be imported below the Manufacturing Resource Library
        (MRL) "Vendor Catalogs" class. The vendor catalog root directory that is needed as input parameter can be
        retrieved using the service operation getVendorCatalogInfo().
        """
        return cls.execute_soa_method(
            method_name='importVendorCatalogHierarchy',
            library='Manufacturing',
            service_date='2013_12',
            service_name='ResourceManagement',
            params={'vendorCatalogRootDir': vendorCatalogRootDir, 'importOptions': importOptions},
            response_cls=ImportVendorCatalogHierarchyResponse,
        )

    @classmethod
    def updateNXToolAssemblies(cls, icoIDs: List[str], identifyCutAndNoCut: bool, generateSpinning: bool, setToolJunctions: bool, writePartAttributes: bool) -> ServiceData:
        """
        This operation triggers specific actions on the NX side to update one or mutliple tool assemblies for use in NX
        CAM. The tool assemblies are identified by their Classification object (ICO) IDs. Initially, the tool
        assemblies are created in the Resource Manager in Teamcenter. Then this operation uses the Graphics Builder and
        calls some NX user functions. UGMaster datasets and an NX part files are created for the tool assemblies. The
        different input parameters trigger more actions.  To ensure that this operation works properly, the "NX Tool
        Type" (MRL attribute -45110) has to be defined in the tool assemblies. Turning tool assemblies have to have a
        "Tracking Point" (MRL attribute -45015) specified. This operation works only for tool assemblies that are
        classified using the Manufacturing Resource Library (MRL).
        Note: The Graphics Builder has to be configured properly for this operation to work.
        """
        return cls.execute_soa_method(
            method_name='updateNXToolAssemblies',
            library='Manufacturing',
            service_date='2013_12',
            service_name='ResourceManagement',
            params={'icoIDs': icoIDs, 'identifyCutAndNoCut': identifyCutAndNoCut, 'generateSpinning': generateSpinning, 'setToolJunctions': setToolJunctions, 'writePartAttributes': writePartAttributes},
            response_cls=ServiceData,
        )


class ModelService(TcService):

    @classmethod
    def computeAppearancePath(cls, input: AppearancePathInput) -> ComputeAppearancePathResponse:
        """
        This service computes and returns the values for APNUID and AbsOccUID propertis.
        
        APN - bl_apn_uid_in_topline_context
        AbsOccUID - bl_absocc_uid_in_topline_context
        
        Input: parent object and a list of paths.
                 Each path starts reletively from the parent object.
                   In case the parent does not have APN, the service will calculate it to the parent as well.
        Response : vector of values of the adove propeties according to each path.
        
        If the input is BOMLine (and not Fnd0BOMLineLite) there might be performance issue due to the fact that the
        modified obejct would be put in the serviceData and the properties that will be brought for this object would
        be according to the PolicyFile (in this case the best practice is to use Dymanic Policy).
        
        Fnd0BOMLineLite does not have as much properties as BOMLine and therefore even if the input is large, not many
        properties would be calculated in the Policy File.
        
        """
        return cls.execute_soa_method(
            method_name='computeAppearancePath',
            library='Manufacturing',
            service_date='2013_12',
            service_name='Model',
            params={'input': input},
            response_cls=ComputeAppearancePathResponse,
        )
