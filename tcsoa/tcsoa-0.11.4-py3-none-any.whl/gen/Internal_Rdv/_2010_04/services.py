from __future__ import annotations

from tcsoa.gen.Internal.Rdv._2010_04.VariantManagement import AddPartSolutionResponse, TargetOccurrences, ReplacePartSolutionResponse, BackgroundOccurrencesResponse, ReplacePartSolutionInputInfo, AddPartSolutionInputInfo
from typing import List
from tcsoa.base import TcService


class VariantManagementService(TcService):

    @classmethod
    def getValidBackgroundOverlays(cls, abortOnError: bool, questions: List[TargetOccurrences]) -> BackgroundOccurrencesResponse:
        """
        This method returns valid background (MEAppearancePathNode or Absocc) UIDs for the respective target (APN or
        Absocc) UID and proximity. Given the top level ItemRevision object tag, RevisionRule name and list of 1:1
        target UIDs and proximity, list of valid background overlays is returned. Proximity search and Valid Overlays
        Only (VOO) filtering is applied on the APN target UIDs to obtain the valid APN background overlays. 
        Please note that the target UIDs provided could be APN or Absocc. If target UID are Absocc, then it is
        converted to APN UID before doing proximity search and Valid Overlay Only processing. Resulting APN background
        overlays are converted to Absocc before being sent to client, if the inputs were Absocc UIDs.
        If the 'abortOnError' flag is set to true, the method would abort even if it finds a single target UID that it
        cannot process. If it is set to false, it would process all the UIDs and return the respective failure codes to
        the client.
        
        Use cases:
        Use case 1: Perform Proximity Search and Valid Overlays Only filtering, for the target MEAPN UIDs, based on the
        proximity distance provided for each of them.
        
        Use case 2: Perform Proximity Search and Valid Overlays Only filtering, for the target Absocc UIDs, based on
        the proximity distance provided for each of them.
        """
        return cls.execute_soa_method(
            method_name='getValidBackgroundOverlays',
            library='Internal-Rdv',
            service_date='2010_04',
            service_name='VariantManagement',
            params={'abortOnError': abortOnError, 'questions': questions},
            response_cls=BackgroundOccurrencesResponse,
        )

    @classmethod
    def replacePartInProduct(cls, inputs: List[ReplacePartSolutionInputInfo]) -> ReplacePartSolutionResponse:
        """
        Replaces a list of existing Part Solutions inside a Product specific Architecture Breakdown Structure with new
        Part Solutions. It also replaces the existing associated part data (Named Variant Expressions and Occurrence
        Notes) corresponding to each part solution with new part data. The new Part solutions and the part data is
        specified through the 'ReplacePartSolutionInputInfo' object. The Part Solution can be replaced with itself (for
        updating) or with a new Part Solution.
        
        Use cases:
        The 'replacePartInProduct' operation is called when user wants to replace existing part solutions and its
        corresponding part data on an Architecture Breakdown Element with new Part Solutions and part data.
        """
        return cls.execute_soa_method(
            method_name='replacePartInProduct',
            library='Internal-Rdv',
            service_date='2010_04',
            service_name='VariantManagement',
            params={'inputs': inputs},
            response_cls=ReplacePartSolutionResponse,
        )

    @classmethod
    def addPartToProduct(cls, inputs: List[AddPartSolutionInputInfo]) -> AddPartSolutionResponse:
        """
        Adds a list of Part Solutions (ERP parts) to an Architecture Breakdown Element (ABE) inside a Product specific
        Architecture Breakdown structure. It also associates the part data (Named Variant Expressions and Occurrence
        Notes) corresponding to each part solution to the architecture breakdown element. The input part solution and
        the part data is specified through the 'AddPartSolutionInputInfo' object.
        
        Use cases:
        The 'addPartToProduct' operation is called when user wants to add part solutions and associate the
        corresponding part data to an Architecture Breakdown Element. The user can specify the input part solution and
        the part data using 'AddPartSolutionInputInfo' object.
        """
        return cls.execute_soa_method(
            method_name='addPartToProduct',
            library='Internal-Rdv',
            service_date='2010_04',
            service_name='VariantManagement',
            params={'inputs': inputs},
            response_cls=AddPartSolutionResponse,
        )
