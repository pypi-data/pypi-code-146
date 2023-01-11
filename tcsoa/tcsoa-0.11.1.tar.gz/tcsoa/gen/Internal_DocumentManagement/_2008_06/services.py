from __future__ import annotations

from tcsoa.gen.Internal.DocumentManagement._2008_06.DispatcherManagement import ConfigInput, ConfigOutput
from tcsoa.gen.Internal.DocumentManagement._2008_06.DocumentControl import IRDCResponse
from tcsoa.gen.BusinessObjects import ItemRevision
from typing import List
from tcsoa.base import TcService


class DispatcherManagementService(TcService):

    @classmethod
    def getConfigurations(cls, svcConfigInput: List[ConfigInput]) -> ConfigOutput:
        """
        The Document Management Render system uses the DispatcherServiceConfig business object to determine what
        Dispatcher Service to invoke for performing the file translation for a given source dataset type to derived
        dataset type.  This operation returns a list of DispatcherServiceConfig business objects deployed in the
        Teamcenter system based on the 'ConfigInput' list structure (contains source data set type, derived dataset
        type and service available).  The 'ConfigInput' structure is used to filter for source dataset type, derived
        dataset type, and service available for the DispatcherServiceConfig business object retrieval.  To retrieve all
        DispatcherServiceConfig business objects, set 'ConfigInput' structure source dataset type name and derived
        dataset type name set to empty string (use double quotes to specify empty string),  and service available set
        to negative or minus 1.  There is no default.
        
        The 'DocumentControl' service 'getIRDCs' operation normally invoke first to obtain the Item Revision Definition
        Configure (IRDC) setting of source dataset type and derived dataset type dataset associated to the ItemRevision
        in order to determine the derived dataset to be generated for the specify source dataset type.
        
        Use cases:
        Use case 1: Retrieve a specific DispatcherServiceConfig business object
        The following example has a DispatcherServiceConfig  business object defining previewservice to be used to
        translate MSWordX (its named reference file .docx) dataset to PDF (the generated .pdf file will be stored as
        named reference file) dataset type:
        - DispatcherServiceConfig  Name=MSWordXTo_PDF_previewservice, Source dataset type name=MSWordX, Derived dataset
        type name=PDF, Dispatcher service=previewservice, Sort Order=1, Service Available=true
        
        
        
        The Document Management Render system (Teamcenter RenderMgtTranslator) can retrieve an instance of
        DispatcherServiceConfig business object filter for source dataset type=MSWordX, derived dataset type=PDF and
        service available=1.  This will return a single list of DispatcherServiceConfig business object containing a
        single object defined in the above example.
        
        Use case 2: Retrieve DispatcherServiceConfig business objects contains service available set to true
        The following example has two DispatcherServiceConfig business objects defining pdfgenerator or previewservice
        to be used to translate MSWordX (its named reference file .docx) dataset to PDF (the generated .pdf file will
        be stored as named reference file) dataset type:
        - DispatcherServiceConfig  Name=MSWordXTo_PDF_pdfgenerator, Source dataset type name=MSWordX, Derived dataset
        type name=PDF, Dispatcher service=pdfgenerator, Sort Order=2, Service Available=true
        
        
        
        - DispatcherServiceConfig  Name=MSWordXTo_PDF_previewservice, Source dataset type name=MSWordX, Derived dataset
        type name=PDF, Dispatcher service=previewservice, Sort Order=1, Service Available=true
        
        
        
        The Document Management Render system (Teamcenter RenderMgtTranslator) can retrieve DispatcherServiceConfig
        business objects filter for source dataset type=MSWordX, derived dataset type=PDF and service available=1. 
        This will return a single list of DispatcherServiceConfig business object containing two business objects
        (DispatcherServiceConfig Name=MSWordXTo_PDF_pdfgenerator, and MSWordXTo_PDF_previewservice) defined in the
        above example.  The Document Management Render system will select the DispatcherServiceConfig business object
        with higher sort order value if there are duplicate objects with the same values specified for the combination
        of source dataset type and derived dataset type.
          
        The system allows defining multiple DispatcherServiceConfig business objects for the same types so the
        Administrator can have backup translators available and select which one to be used without deleting and
        creating the DispatcherServicConfig business objects.
        
        Use case 3: Retrieve all DispatcherServiceConfig business objects
        The following example has three DispatcherServiceConfig business objects defining pdfgenerator or
        previewservice to be used to translate MSWordX (its named reference file .docx) dataset to PDF (the generated
        .pdf file will be stored as named reference file) dataset type. Previewsevice to be used to translate MSExcelX
        (its named reference file .xlsx) dataset type to PDF dataset type:
        
        - DispatcherServiceConfig  Name= MSWordXTo_PDF_pdfgenerator, Source dataset type name= MSWordX, Derived dataset
        type name=PDF, Dispatcher service= pdfgenerator, Sort Order=2, Service Available=true
        
        
        
        - DispatcherServiceConfig  Name= MSWordXTo_PDF_previewservice, Source dataset type name= MSWordX, Derived
        dataset type name=PDF, Dispatcher service= previewservice, Sort Order=1, Service Available=false
        
        
        
        - DispatcherServiceConfig  Name= MSWordXTo_PDF_previewservice, Source dataset type name= MSExcelX, Derived
        dataset type name=PDF, Dispatcher service= previewservice, Sort Order=1, Service Available=true
        
        
        
        The Document Management Render system (Teamcenter RenderMgtTranslator) can retrieve all DispatcherServiceConfig
        objects by filtering for source dataset type=empty string, derived dataset type=empty string and service
        available=negative or minus 1.  This will return a single list of DispatcherServiceConfig business object
        containing all three business objects as defined in the above example.
        """
        return cls.execute_soa_method(
            method_name='getConfigurations',
            library='Internal-DocumentManagement',
            service_date='2008_06',
            service_name='DispatcherManagement',
            params={'svcConfigInput': svcConfigInput},
            response_cls=ConfigOutput,
        )


class DocumentControlService(TcService):

    @classmethod
    def getIRDCs(cls, itemRevs: List[ItemRevision]) -> IRDCResponse:
        """
        This operation is used by the Document Management Render system (Teamcenter RenderMgtTranslator) prior to
        performing a render of the given ItemRevision objects. In order to perform the render of an ItemRevision, the
        system needs to obtain the Item Revision Definition Configuration (IRDC) settings for the ItemRevision first.
        The IRDC object specifies necessary information for the render, such as the source and derived dataset types.
        
        There is only a single IRDC object returned per ItemRevision. The return vector is the same length as the input
        vector, with a 1 to 1 relation between the two lists.
        
        This operation is internal and only intended to be used by the Document Management Render system. The IRDC
        object should be treated as read only. Only the Business Modeler IDE (BMIDE) application is allowed to create
        or modify IRDC settings.
        
        Use cases:
        Retrieve render data for one or more ItemRevision business objects.
        
        The Document Management Render system is given a list of ItemRevision objects for rendering. First it must
        invoke the getIRDCs operation in order to determine what the source and derived dataset types are for each
        ItemRevision. Once the system has the IRDC objects, it can use the getConfigurations operation to get the
        DispatcherServiceConfig object for each translation, and then perform the translation.
        """
        return cls.execute_soa_method(
            method_name='getIRDCs',
            library='Internal-DocumentManagement',
            service_date='2008_06',
            service_name='DocumentControl',
            params={'itemRevs': itemRevs},
            response_cls=IRDCResponse,
        )
