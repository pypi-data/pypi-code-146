from __future__ import annotations

from tcsoa.gen.Internal.DocumentManagement._2013_05.DigitalSignature import CheckOutForSignResponse
from tcsoa.gen.BusinessObjects import Dataset
from tcsoa.gen.DocumentManagement._2010_04.DigitalSignature import DigitalSignSaveInput, DigtalSigningSaveResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class DigitalSignatureService(TcService):

    @classmethod
    def isCheckOutForSign(cls, inputDatasets: List[Dataset]) -> CheckOutForSignResponse:
        """
        This operation determines each Dataset (from the provided input list of Dataset objects) is checked out for
        digitally sign. It returns the list of true or false corresponding to order of the input Dataset object list,
        and the ServiceData with any partial errors from the system.
        
        Use cases:
        Use Case 1: Determine a Dataset is checked out for sign
        A user selects a dataset from a client application (for example, Rich Client or Thin Client or Microsoft Office
        client). The Sign action in the client will result in the PDF file being checked out and opened in the signing
        application (for example, Adobe Acrobat or Reader). Internally, the client application initiates this operation
        to determine if the dataset is checked out for digitally sign, if it is true then the client application will
        disable the CheckIn, CheckOut, Transfer Checkout menu.
        """
        return cls.execute_soa_method(
            method_name='isCheckOutForSign',
            library='Internal-DocumentManagement',
            service_date='2013_05',
            service_name='DigitalSignature',
            params={'inputDatasets': inputDatasets},
            response_cls=CheckOutForSignResponse,
        )

    @classmethod
    def digitalSigningSaveTool(cls, saveInput: DigitalSignSaveInput) -> DigtalSigningSaveResponse:
        """
        This operation updates and checks in the input Dataset object (which has the digitally signature named
        reference file). The provided input structure DigitalSignSaveInput (contains Dataset object, File Management
        File (FMS) file ticket, the signing tool name, validation of the signature, the signed user name, and the sign
        time). The signed file must be uploaded to Teamcenter volume prior invoking this operation. The Dataset is
        returned if the update is successful; otherwise, partial error information is returned in the ServiceData.
        
        Use cases:
        Use Case 1: Sign a PDF Dataset
        A user selects a PDF dataset and Sign the dataset from a client application (for example, Rich Client or Thin
        Client or Microsoft Office client). The Sign action in the client will result in the PDF file being checked out
        and opened in the signing application (for example, Adobe Acrobat or Reader). After the user applied the
        digital signature and save the PDF file, this will trigger the signing application to call back to the client
        application, and the client application then initiates this operation to update the PDF datasets named
        reference file (file must be upload to Teamcenter volume first) with the signed PDF file and check in the PDF
        dataset.
        """
        return cls.execute_soa_method(
            method_name='digitalSigningSaveTool',
            library='Internal-DocumentManagement',
            service_date='2013_05',
            service_name='DigitalSignature',
            params={'saveInput': saveInput},
            response_cls=DigtalSigningSaveResponse,
        )

    @classmethod
    def cancelSign(cls, inputDatasets: List[Dataset]) -> ServiceData:
        """
        This operation cancels the previously checked out Dataset objects for digitally sign operation. It returns the
        ServiceData with any partial errors from the system.
        
        Use cases:
        Use Case 1: Cancel Sign a PDF Dataset
        A user selects a PDF dataset and Sign the dataset from a client application (for example, Rich Client or Thin
        Client or Microsoft Office client). The Sign action in the client will result in the PDF file being checked out
        and opened in the signing application (for example, Adobe Acrobat or Reader). The user closes the signing
        application without applying the digital signature. From the client application, the user initiates the Cancel
        Sign action. This will initiates this operation to cancel the checked out of the PDF dataset.
        """
        return cls.execute_soa_method(
            method_name='cancelSign',
            library='Internal-DocumentManagement',
            service_date='2013_05',
            service_name='DigitalSignature',
            params={'inputDatasets': inputDatasets},
            response_cls=ServiceData,
        )
