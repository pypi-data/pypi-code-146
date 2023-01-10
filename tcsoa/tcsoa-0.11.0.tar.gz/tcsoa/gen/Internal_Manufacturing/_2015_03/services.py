from __future__ import annotations

from tcsoa.gen.Internal.Manufacturing._2015_03.StructureManagement import SearchForClusters, CreateReuseAssembly, SearchForClustersResponse, ConfigureMultipleStructuresResponse, AlignAssemblyData, GetClusterDetails, ConfigurationsInfo, CreateReuseAssemblyResp
from tcsoa.gen.Internal.Manufacturing._2015_03.Attachments import AttachmentsInput, CreateAttachmentsInput, AttachmentResponse, AttachmentLines
from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.Manufacturing._2015_03.StructureSearch import GetSearchCrieriaFromRecipeResp
from tcsoa.gen.Internal.Manufacturing._2015_03.ResourceManagement import ImportStepP21Files3Response, MapClassificationObjectResponse, ImportStep3DModels2Response, UnzipGtcPackageResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class StructureSearchService(TcService):

    @classmethod
    def getSearchCriteriaFromRecipe(cls, recipes: List[BusinessObject]) -> GetSearchCrieriaFromRecipeResp:
        """
        This operation retrieves the search criteria stored in a recipe on a Manufacturing BOM (MBOM) node. The
        returned search critieria will be used to automatically resolve Engineering BOM (EBOM) lines under the MBOM
        node.
        
        Exceptions:
        >This operation will throw a ServiceException if the Teamcenter database schema does not have the recipe
        constructs.
        - 300376 The schema element Mfg0MEMBOMRecipe is missing, and is needed to be able to store the recipe. Please
        contact your system administrator to ensure that the Foundation template is properly installed.
        
        """
        return cls.execute_soa_method(
            method_name='getSearchCriteriaFromRecipe',
            library='Internal-Manufacturing',
            service_date='2015_03',
            service_name='StructureSearch',
            params={'recipes': recipes},
            response_cls=GetSearchCrieriaFromRecipeResp,
        )


class ResourceManagementService(TcService):

    @classmethod
    def importStep3DModels2(cls, icoIds: List[str]) -> ImportStep3DModels2Response:
        """
        This operation imports STEP 3D model files for Generic Tool Catalog (GTC) Packages. The STEP files are
        converted to NX part and to JT file format and imported into Teamcenter. If needed, items are created for the
        Classification objects (ICO). One UGMaster dataset for the NX part file and one DirectModel dataset for the JT
        file is created below the (new) item. 
        
        
        Use cases:
        There are two different use case s:
            A) The specified ICO is classified in a vendor catalog class
        (the ICO has an attribute -159003 "3D Model file name")
            B) The specified ICO is classified in an MRL MyComponents class
        (the ICO does not have an attribute -159003 "3D Model file name")
        
        In use case A, this operation retrieves the file name of the 3D model directly from GTC attribute 
        -159003 "3D Model file name".
        (Another attribute ID instead of -159003 can be defined in the "MRMGTC3DModelAttributeID" preference.)
        
        In use case B, the SOA operation checks if there is an Manufacturing Resource Library (MRL) attribute -40930
        "Vendor Reference Object ID" in the given ICO. This attribute is used to store the reference from the MRL
        MyComponents ICO to the GTC vendor catalog ICO. If this attribute exists in the ICO's class and has a valid ICO
        ID as value, the 3D model file name will be retrieved from the referenced ICO. (see use case A)
        (Another attribute ID instead of -40930 can be defined in the "MRMGTCReferenceObjectAttributeID"preference.)
        
        The SOA operation retrieves the information about the server-sided directory, where all STEP 3D models of the
        catalog are stored, based on the class of the GTC vendor catalog ICO.
        
        If there is a problem during importing one of the 3D models, the operation will continue importing the 3D
        models of the following ICOs.
        
        This operation is very similar to importStep3DModels(). The difference is that this new operation returns in
        addition to the service data also information about the ICO and the newly created item.
        
        Note: The Graphics Builder has to be configured properly for this operation to work.
        """
        return cls.execute_soa_method(
            method_name='importStep3DModels2',
            library='Internal-Manufacturing',
            service_date='2015_03',
            service_name='ResourceManagement',
            params={'icoIds': icoIds},
            response_cls=ImportStep3DModels2Response,
        )

    @classmethod
    def importStepP21Files3(cls, classId: str, catalogRootDirectory: str, importOption: int) -> ImportStepP21Files3Response:
        """
        This operation imports STEP P21 files containing product data pertaining to Generic Tool Catalog (GTC) Packages
        into the Classification classes that represent vendor catalogs inside the Teamcenter database. It creates
        Internal Classification objects (ICOs) in those classes, and associated data that represents the products.
        Depending on the contents of the GTC Package, it may also create associated items, item revisions, datasets,
        and associated files to store drawings and images that further describe those tool components.
        """
        return cls.execute_soa_method(
            method_name='importStepP21Files3',
            library='Internal-Manufacturing',
            service_date='2015_03',
            service_name='ResourceManagement',
            params={'classId': classId, 'catalogRootDirectory': catalogRootDirectory, 'importOption': importOption},
            response_cls=ImportStepP21Files3Response,
        )

    @classmethod
    def mapClassificationObject(cls, sourceIcoId: str, targetItemId: str, targetItemName: str, targetItemTypeName: str, targetItemRevId: str, targetItemDescription: str, targetClassId: str, options: int) -> MapClassificationObjectResponse:
        """
        This operation maps an Internal Classification Object  (ICO)  from its Classification class into the class
        identified by the provided targetClassId. It will also create an item of the provided item type, having the
        provided IDs, name, and description created. This operation maps the attribute values from the source ICO into
        the target ICO based on the mapping rules defined in Classification Admin. Using the options parameter the user
        can decide if datasets from a source item should be copied to the tartget item.
        
        Use cases:
        A typical use case when this operation can be used is the mapping of ICOs from the Generic Tool Catalog (GTC)
        classes into the Manufacturing Resource Library's (MRL) tool component classes. The GTC classes contain catalog
        tool components. In the MRL tool component classes are those tool components that are actively used in the
        customer's shopfloor.
        In the Classification Admin application are mapping rules (Mapping Views) defined that control which GTC class
        is mapped on what MRL class and which GTC attribute is mapped on what MRL attribute.
        During the mapping operation a new item and ICO are created in the MRL class and the attribute values from the
        source ICO are transferred into the target ICO. If the source component has a dataset attached, this operation
        allows to copy the dataset to the new target component. 
        """
        return cls.execute_soa_method(
            method_name='mapClassificationObject',
            library='Internal-Manufacturing',
            service_date='2015_03',
            service_name='ResourceManagement',
            params={'sourceIcoId': sourceIcoId, 'targetItemId': targetItemId, 'targetItemName': targetItemName, 'targetItemTypeName': targetItemTypeName, 'targetItemRevId': targetItemRevId, 'targetItemDescription': targetItemDescription, 'targetClassId': targetClassId, 'options': options},
            response_cls=MapClassificationObjectResponse,
        )

    @classmethod
    def unzipGtcPackage(cls, transientFmsZipFileTicket: str) -> UnzipGtcPackageResponse:
        """
        This operation uses the File Management Service (FMS) transient file ticket provided to unzip an uploaded
        Generic Tool Catalog (GTC) package ZIP file on the Teamcenter server. The ZIP file will be extracted to:
        $TC_DATA/offset-directory-specified-in-the-MRMGTCPackageServerDir-system-preference
        In that directory, a new directory with the ZIP file name is created. If this directory already exists, a new
        directory with the ZIP file name and an appended timestamp is created.
        
        Example:
        Environment Variable TC_DATA:        $TC_DATA
        Preference MRMGTCPackageServerDir:    ResourceManagement\GTCPackages
        GTC Package ZIP Filename:            sampleGTCPackage.zip
        Resulting Directory:        
        $TC_DATA\ResourceManagement\GTCPackages\sampleGTCPackage  
        
        """
        return cls.execute_soa_method(
            method_name='unzipGtcPackage',
            library='Internal-Manufacturing',
            service_date='2015_03',
            service_name='ResourceManagement',
            params={'transientFmsZipFileTicket': transientFmsZipFileTicket},
            response_cls=UnzipGtcPackageResponse,
        )


class StructureManagementService(TcService):

    @classmethod
    def configureMultipleStructures(cls, configurationsInfo: List[ConfigurationsInfo]) -> ConfigureMultipleStructuresResponse:
        """
        The operation applies the input configurations to each input BOMWindow and its root BOMLine or BOPLine object
        of the structure. The type of BOPLine object can be Mfg0BvrProcess. The configurations those are applicable to
        a BOMWindow in a Teamcenter session are used as input to configure the structures. The input configuration
        rules supported by the operation are as follows -
        a)    Variant rule 
        b)    Revision rule
        c)    Effectivity 
        d)    Show or hide the BOMLine or BOPLine objects configured-out by variant rule configuration on the BOMWindow.
        e)    Show or hide the BOMLine or BOPLine objects configured-out by the occurrence effectivity configuration on
        the BOMWindow.
        f)    Show or hide the suppressed BOMLine or BOPLine objects in the BOMWindow.
        g)    Show or hide the BOMLine or BOPLine objects configured-out by the incremental changes configuration on
        the BOMWindow.
        h)    Show or hide BOPLine objects configured-out by the assigned occurrences in the BOMWindow.
        """
        return cls.execute_soa_method(
            method_name='configureMultipleStructures',
            library='Internal-Manufacturing',
            service_date='2015_03',
            service_name='StructureManagement',
            params={'configurationsInfo': configurationsInfo},
            response_cls=ConfigureMultipleStructuresResponse,
        )

    @classmethod
    def searchForClusters(cls, input: List[SearchForClusters]) -> SearchForClustersResponse:
        """
        This operation creates clusters(groups) of objects (currently, BOMLine objects) from an Engineering BOM (EBOM )
        matching the pattern of currently assigned objects from the same EBOM under a given Model assembly (currently
        represented by a BOMLine object) in a Manufacturing BOM (MBOM)). The pattern to create the clusters is based on
        combination of item id and relative transform differences betweeen the assigned objects in the model assembly.
        If the transforms do not uniquely identify the patterns (example: all transforms are Identity) the operation
        may identify a very large set as pattern. The normal usage for this operation should be when the transforms
        form well defined patterns. It is assumed that the properties of BOMLine objects that form the cluster are not
        used after this operation returns. Calling this operation itself will not return the properties of the BOMLine
        objects that are contained in the clusters. It is imperative that the response of this operation will be used
        as input to another subsequent operation getClusterDetails to get the properties for the BOMLine objects found
        in each cluster.
        """
        return cls.execute_soa_method(
            method_name='searchForClusters',
            library='Internal-Manufacturing',
            service_date='2015_03',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=SearchForClustersResponse,
        )

    @classmethod
    def createReuseAssemblies(cls, input: List[CreateReuseAssembly]) -> CreateReuseAssemblyResp:
        """
        This operation creates reuse  assemblies based on BOMLine objects under a template model assembly defined in
        the Manufacturing BOM (MBOM) and the cluster of BOMLine objects returned from the operation searchForClusters.
        Each of the assemblies created can be reused as a model assembly. The searchForClusters operation returns 
        collections of BOMLine objects from Engineering BOM (EBOM) based on the template model assembly.
        """
        return cls.execute_soa_method(
            method_name='createReuseAssemblies',
            library='Internal-Manufacturing',
            service_date='2015_03',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=CreateReuseAssemblyResp,
        )

    @classmethod
    def alignAssemblies(cls, input: List[AlignAssemblyData]) -> ServiceData:
        """
        This operation aligns the "bl_abs_occ_id" property and the absolute transform of a BOMLine object in source
        structure to a BOMLine object in a target structure. In addition, if alignMode is not specified, any lines with
        matching relative transforms to these aligned lines in their respective structures will have the
        "bl_abs_occ_id" property aligned too. The operation also allows for aligning only "bl_abs_occ_id" property
        without changing the transform or aligning BOMLine properties based on the preference "MEAlignedPropertiesList".
        """
        return cls.execute_soa_method(
            method_name='alignAssemblies',
            library='Internal-Manufacturing',
            service_date='2015_03',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def getClusterDetails(cls, input: List[GetClusterDetails]) -> ServiceData:
        """
        This operation gets the properties for the BOMLine objects returned from a previous call to  searchForClusters.
        It is imperative that the response of this operation will be used as input to this operation to get the
        properties for the BOMLine objects found in each cluster.
        """
        return cls.execute_soa_method(
            method_name='getClusterDetails',
            library='Internal-Manufacturing',
            service_date='2015_03',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=ServiceData,
        )


class AttachmentsService(TcService):

    @classmethod
    def createAttachmentLines(cls, attachmentsInputList: List[CreateAttachmentsInput]) -> AttachmentResponse:
        """
        This service operation creates attachment line representing a form or dataset. The operation takes place in
        multiple steps as below.
        - Dataset  is created.
        - Highest revision of the newly created Dataset is fetched.
        - The write file ticket for the file to be associated with the Dataset  iis fetched.
        - The file is committed with the Dataset.
        - An attachment line is created for the Dataset.
        
        
        The attachment line created by this operation is a run time business object. In client use case scenario this
        object should be used with precaution as it gets destroyed when another BOMLine is selected in BOMWindow.
        Note that this operation doesn't take care of uploading the write file ticket to FMS server thus preventing any
        edit of the file.
        
        Use cases:
        Use Case 1: Creating new dataset line in attachment view.
        This operation can be used to create a new dataset line in the attachment window. The newly created dataset
        will be related to the ItemRevision of the BOMLine with the specified relation.
        
        Use Case 2: Creating new form line in attachment view.
        This operation can be used to create a new attachment line representing a Form. The newly created form will be
        related to the ItemRevision of the BOMLine with a default relation like IMAN_specifications.
        """
        return cls.execute_soa_method(
            method_name='createAttachmentLines',
            library='Internal-Manufacturing',
            service_date='2015_03',
            service_name='Attachments',
            params={'attachmentsInputList': attachmentsInputList},
            response_cls=AttachmentResponse,
        )

    @classmethod
    def getAttachmentLines(cls, inputList: List[AttachmentsInput]) -> AttachmentLines:
        """
        This service operation fetches all the attachment lines for the given BOMLine object.  Using this operation
        saves at least 3 server calls in case of attachment window use cases. 
        
        Use cases:
        Use Case 1: User opens the attachment window/panel.
        This operation can be used to get the attachment lines for the selected BOMLine object  and display in
        attachment window/panel. In this case only the BOMLine object is to be sent to the operation without any
        attachment window objects. A new attachment window is created in this case.
        
        Use Case 2: User selects another BOMLine while the attachment window/panel is opened.
        While the attachment panel is open, this operation can be used to get the attachment lines on change of
        selection to other BOMLine. In this case the CfgAttachmentWindow objects of the opened attachment window(s)
        is(are) to be sent to the operation along with the BOMLine object. No new attachment window is created in this
        case. The given BOMLine is used to set the top line(s) of the attachment window(s) provided to the operation.
        """
        return cls.execute_soa_method(
            method_name='getAttachmentLines',
            library='Internal-Manufacturing',
            service_date='2015_03',
            service_name='Attachments',
            params={'inputList': inputList},
            response_cls=AttachmentLines,
        )
