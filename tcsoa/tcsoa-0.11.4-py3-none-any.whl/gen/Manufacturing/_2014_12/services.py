from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Manufacturing._2014_12.StructureSearch import ResolveAssignmentRecipeInputElement, CreateOrUpdateAssignmentRecipeResp, ResolveAssignmentRecipeResp, GetAssignmentRecipesResp, CreateOrUpdateAssignmentRecipeInputElem
from tcsoa.gen.Manufacturing._2014_12.IPAManagement import RepopulateDynamicIPAsResponse, RepopulateDynamicIPAsData, FindAndRepopulateDynamicIPAsResponse
from typing import List
from tcsoa.gen.Manufacturing._2014_12.Validation import MaturityReportResponse, MaturityReportRequest
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService
from tcsoa.gen.Manufacturing._2014_12.Model import ValidateScopeFlowsConsistencyResponse


class IPAManagementService(TcService):

    @classmethod
    def repopulateDynamicIPAs(cls, input: RepopulateDynamicIPAsData) -> RepopulateDynamicIPAsResponse:
        """
        The operation converts the given input list of absolute occurrence IDs to a list of objects (ImanItemBOPLine)
        and calculates/regenerates & returns dynamic in-process assembly nodes and its related information. The input
        object contains the top BOPLine and a list of absolute occurrence IDs of processes(Mfg0BvrProcess) or shared
        studies(Mfg0BvrShdStudy).
        
        For every given absolute occurrence IDs
        - If the object doesn't have any dynamic in-process-assembly (IPA)  as children, the operation issues an error.
        - If the dynamic IPA nodes (that belong to the given object) are empty, the operation re-calculates them. 
        - The response of the operation includes the dynamic IPA nodes that belongs to the object. For each dynamic
        IPA, the response includes its content (i.e. parts underneath) and occurrence information. Both the consumed
        part object (BOPLine) and referenced part object (BOMLine) are returned along with their related occurrence
        information. 
        
        
        
        This data is returned for every given object, no matter whether its dynamic IPA nodes were originally empty or
        not.
        """
        return cls.execute_soa_method(
            method_name='repopulateDynamicIPAs',
            library='Manufacturing',
            service_date='2014_12',
            service_name='IPAManagement',
            params={'input': input},
            response_cls=RepopulateDynamicIPAsResponse,
        )

    @classmethod
    def findAndRepopulateDynamicIPAs(cls, inputBOPLines: List[BusinessObject]) -> FindAndRepopulateDynamicIPAsResponse:
        """
        This operation recieves a list of ImanItemBOPLine as an input.
        (The type of of the bop line objects can be either Mfg0BvrProcess or Mfg0BvrShdStudy).
        
        For every given object:
        1. If the object does not have any dynamic IPAs, the operation issues an error.
        
        2. If the dynamic IPAs (that belong to the given object) are empty, the operation re-calculates them.
        """
        return cls.execute_soa_method(
            method_name='findAndRepopulateDynamicIPAs',
            library='Manufacturing',
            service_date='2014_12',
            service_name='IPAManagement',
            params={'inputBOPLines': inputBOPLines},
            response_cls=FindAndRepopulateDynamicIPAsResponse,
        )


class StructureSearchService(TcService):

    @classmethod
    def resolveAssignmentRecipe(cls, input: List[ResolveAssignmentRecipeInputElement]) -> ResolveAssignmentRecipeResp:
        """
        This operation resolves the saved search recipe on a Manufacturing BOM (MBOM) node. The recipe is used to
        automatically resolve Engineering BOM (EBOM) lines under the MBOM node with the recipe. The operation will
        throw an ServiceException if the Teamcenter database schema does not have the recipe constructs.
        
        Exceptions:
        >If the schema for the AssignmentRecipe is not available an exception is thrown.
        """
        return cls.execute_soa_method(
            method_name='resolveAssignmentRecipe',
            library='Manufacturing',
            service_date='2014_12',
            service_name='StructureSearch',
            params={'input': input},
            response_cls=ResolveAssignmentRecipeResp,
        )

    @classmethod
    def createOrUpdateAssignmentRecipe(cls, input: List[CreateOrUpdateAssignmentRecipeInputElem]) -> CreateOrUpdateAssignmentRecipeResp:
        """
        This operation creates or updates the search recipe on a Manufacturing BOM (MBOM) node. The recipe is used to
        automatically resolve Engineering BOM (EBOM) lines under the MBOM node with the recipe. If recipe is updated
        after a prior resolve there must be a subsequent call to resolve the new recipe using the
        resolveAssignmentRecipe. The operation will throw an ServiceException if the Teamcenter database schema does
        not have the recipe constructs. It requires the recipe to be provided as a SearchStructureContext object
        (capturing structure search parameters) and/or key-value pairs of AbsOccurrence attributes.
        
        Use cases:
        There is a need to automatically consume Engineering BOM (EBOM) nodes under a phantom Manufacturing BOM (MBOM)
        node based on search criteria provided by Structure Search.
        
        Exceptions:
        >If the schema for the Mfg0MEMBOMRecipe is not found, an exception will be thrown.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateAssignmentRecipe',
            library='Manufacturing',
            service_date='2014_12',
            service_name='StructureSearch',
            params={'input': input},
            response_cls=CreateOrUpdateAssignmentRecipeResp,
        )

    @classmethod
    def deleteAssignmentRecipes(cls, recipes: List[BusinessObject], recipeAnchors: List[BusinessObject], contextForRemovingResolvedObjs: BusinessObject, appKey: str) -> ServiceData:
        """
        This operation deletes the given explit recipe (Mfg0MEMBOMRecipe) objects. Optionally, can delete all recipe
        objects attached to the recipeAnchors ( BOMLine Objects). If the contextForRemovingResolvedObjs is provided,
        the resolved lines will be removed unless those are resolved by other recipes too. Pass NULL for this parameter
        if resolved lines are not to be cleaned up.
        
        Exceptions:
        >If the schema for the recipe is not installed, service will throw an exception.
        """
        return cls.execute_soa_method(
            method_name='deleteAssignmentRecipes',
            library='Manufacturing',
            service_date='2014_12',
            service_name='StructureSearch',
            params={'recipes': recipes, 'recipeAnchors': recipeAnchors, 'contextForRemovingResolvedObjs': contextForRemovingResolvedObjs, 'appKey': appKey},
            response_cls=ServiceData,
        )

    @classmethod
    def getAssignmentRecipes(cls, recipeAnchors: List[BusinessObject], recipeNames: List[str], appKey: str) -> GetAssignmentRecipesResp:
        """
        This operation get the recipe (Mfg0MEMBOMRecipe) objects attached to the underlying ItemRevisions of the
        recipeAnchors. Currently, only BOMLine objects can be specified as recipeAnchors.
        
        Exceptions:
        >If the schema for Manufacturing BOM (MBOM) does not exist the service exception is thrown.
        """
        return cls.execute_soa_method(
            method_name='getAssignmentRecipes',
            library='Manufacturing',
            service_date='2014_12',
            service_name='StructureSearch',
            params={'recipeAnchors': recipeAnchors, 'recipeNames': recipeNames, 'appKey': appKey},
            response_cls=GetAssignmentRecipesResp,
        )


class ModelService(TcService):

    @classmethod
    def validateScopeFlowsConsistency(cls, rootLines: List[BusinessObject]) -> ValidateScopeFlowsConsistencyResponse:
        """
        This operation will be used to identify scope flows created under the given input line are acyclic or not. This
        operation recieves a list of ImanItemBOPLine as an input.  (The type of the BOP line objects can be either
        Mfg0BvrProcess or Mfg0BvrOperation). For each input scope, the operation checks whether the scope-flows
        (defined in this scope), create a cycle of processes or operations. 
        
        If a cycle is indentified during this operation, the relevant information for the cycle is returned in the
        response.
        """
        return cls.execute_soa_method(
            method_name='validateScopeFlowsConsistency',
            library='Manufacturing',
            service_date='2014_12',
            service_name='Model',
            params={'rootLines': rootLines},
            response_cls=ValidateScopeFlowsConsistencyResponse,
        )


class ValidationService(TcService):

    @classmethod
    def getMaturityReport(cls, maturityReportRequest: MaturityReportRequest) -> MaturityReportResponse:
        """
        This service operation evaluates the maturity of the structure based on certain rules. The operation executes 
        specified rules on objects of the structure and returns if the rules are fulfilled or not. The operation takes 
        BOMLine as a scope to evaluate the maturity of objects under it, the list of rules to evaluate the maturity,
        and supporting information. In response the operation returns the objects and their maturity status along with
        other relevant information.
        
        Use cases:
        Use Case 1 - User checks maturity of a structure.
            User can check the maturity of structure by right clicking on root or topline of the structure. Consider a
        Logistic structure consisting of logistics bill of process (LBOP), part family, parts under the part family and
        in-plant supply chain. User needs to know if all part families have part specified or if all part families have
        at least one in-plant supply chain or if all parts have at least one in-bound supply chain. User can choose the
        predefined rules and use this operation to evaluate the rules on part family and in response see a maturity
        report.
        """
        return cls.execute_soa_method(
            method_name='getMaturityReport',
            library='Manufacturing',
            service_date='2014_12',
            service_name='Validation',
            params={'maturityReportRequest': maturityReportRequest},
            response_cls=MaturityReportResponse,
        )
