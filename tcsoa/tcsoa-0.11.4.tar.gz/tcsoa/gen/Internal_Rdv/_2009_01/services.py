from __future__ import annotations

from tcsoa.gen.Internal.Rdv._2009_01.VariantManagement import MetaExprTokens, GetAbeBomlineChildComponentsResponse, GetABandABEResponse, GetAbeMeapnChildComponentsResponse, NVEMetaExpressionResponse, NVEMetaToken, GetABandABEInputInfo, GetAbeChildComponentsInputInfo, ValidateNVEMetaExprResponse, AddDesignToProductResponse
from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class VariantManagementService(TcService):

    @classmethod
    def reapplyNVEMetaExpressions(cls, bomlines: List[BOMLine], validate: bool) -> ServiceData:
        """
        This operation reapplies the MetaExpression to the set of BOMLine objetcs. Meta expressions are used to balance
        the tree structure amongst the variant expressions and validate the input combination of Named Variant
        Expressions (NVEs). MetaExpression is the internal representation of Thought. If input parameter 'validate' is
        true then the MetaExpression will be validated before applying to the BOMLine. This operation gets the
        NVEMetaExpression object from the BOMLine. NVEMetaExpression object get 'validated' if validate flag is true
        after that NVEMetaExpression object reapplied to each BOMLine.
        
        Use cases:
        This operation takes the list of BOMLine objects on which metaexpression needs to be reapplied. Meta expression
        can be validated by setting the 'validate' flag to true.
        """
        return cls.execute_soa_method(
            method_name='reapplyNVEMetaExpressions',
            library='Internal-Rdv',
            service_date='2009_01',
            service_name='VariantManagement',
            params={'bomlines': bomlines, 'validate': validate},
            response_cls=ServiceData,
        )

    @classmethod
    def replaceDesignInProduct(cls, component: BusinessObject, bomlinesToReplace: List[BusinessObject], prodRevs: List[BusinessObject], archApn: BusinessObject, lous: List[BusinessObject], metaExpr: List[NVEMetaToken], validate: bool) -> ServiceData:
        """
        This operation applies the variant data to the occurrence of the already added design solution to the
        Installation Assembly. There is no need to associate the Installation Assembly with the architecture as this
        has already been done. The purpose is simply to apply the appropriate variant data to the occurrence of the
        design solution.
        If the number of 'bomlinesToReplace' is 1, then the input component replaces the Item or ItemRevision  on that
        target BOMLine, and the meta expression is applied. If multiple 'bomlinesToReplace' are provided, no substitute
        occurs, but the meta expression is still applied.
        
        Use cases:
        Use case 1: Replacing a design solution with already added design solution
        User can replace existing design solution with a new one or modify the variant condition by specifying its Item
        or ItemRevision in the 'component' parameter and also specify the new variant condition in 'metaExpr'
        parameter. In this case, size of 'bomlinesToReplace' list should be 1.
        
        Use case 2. Updating variant data of multiple design solutions
        If user needs to modify the variant conditions of multiple design solutions in one go, this can be done by
        specifying variant condition data using 'metaExpr' parameter and the multiple designs Item Revisions in
        'prodRevs' parameter. The number of design solutions whose variant data is to be updates is represented by
        'bomlinesToReplace' parameter and its size should be greater than 1. In this case the 'component' parameter is
        ignored.
        """
        return cls.execute_soa_method(
            method_name='replaceDesignInProduct',
            library='Internal-Rdv',
            service_date='2009_01',
            service_name='VariantManagement',
            params={'component': component, 'bomlinesToReplace': bomlinesToReplace, 'prodRevs': prodRevs, 'archApn': archApn, 'lous': lous, 'metaExpr': metaExpr, 'validate': validate},
            response_cls=ServiceData,
        )

    @classmethod
    def addDesignToProduct(cls, component: BusinessObject, iaRev: BusinessObject, prodRevs: List[BusinessObject], archApn: BusinessObject, lous: List[BusinessObject], noRequestedOccs: int, metaExpr: List[NVEMetaToken], validate: bool) -> AddDesignToProductResponse:
        """
        This operation adds a new design solution to a CAD structure node, referred as Installation Assembly (IA), and
        applies variant conditions on the newly added design assembly. The variant conditions are constructed from the
        Named Variant Expressions (NVE) available to the architecture breakdown element that is associated with the
        Installation Assembly. It is assumed the user has already created the design solution and needs to add it to
        the appropriate parent Installation Assembly. 
        Meta expressions are used to balance the tree structure amongst the variant expressions and validate the input
        combination of NVEs.
        All the parameter values are mandatory, except the 'lous' and 'metaExpr' which are optional.
        
        Use cases:
        Use Case 1: Add Design to Product
        This operation is called whenever a user wants to add a design solution to a CAD structure (referred as
        installation assembly). Prior to calling this operation, user is expected to associate the installation
        assembly to architecture breakdown element. After the operation execution the design assembly ('iaRev'
        parameter) is added to the product structure ('prodRevs' parameter) and the variant conditions if supplied
        (using the 'metaExpr' parameter) is applied on the occurrence of the design solution.
        """
        return cls.execute_soa_method(
            method_name='addDesignToProduct',
            library='Internal-Rdv',
            service_date='2009_01',
            service_name='VariantManagement',
            params={'component': component, 'iaRev': iaRev, 'prodRevs': prodRevs, 'archApn': archApn, 'lous': lous, 'noRequestedOccs': noRequestedOccs, 'metaExpr': metaExpr, 'validate': validate},
            response_cls=AddDesignToProductResponse,
        )

    @classmethod
    def validateNVEMetaExpressions(cls, metaExprs: List[MetaExprTokens]) -> ValidateNVEMetaExprResponse:
        """
        This operation validates the list of 'MetaExprTokens'. 'MetaExprTokens' contains the list of 'NVEMetaToken'.
        'MetaExprTokens' is the internal representation of the Thought.
        
        Meta expressions are used to balance the tree structure amongst the variant expressions and validate the input
        combination of NamedVariantExpressions. This operation creates the NVEMetaExpression object from the list of
        'NVEMetaToken' and then NVEMetaExpression object gets validated.
         
        Validation is the process to check if input meta expression always evaluates to 'true' or 'false', in this case
        validation will fail otherwise it will pass. This operation also fails if metaExprs contains invalid
        'MetaExprTokens' objects.
        
        
        Use cases:
        Validating a Thought
        
        Validation of a Thought is performed by converting the Thought into meta expression which is provided as an
        input to this operation.
        """
        return cls.execute_soa_method(
            method_name='validateNVEMetaExpressions',
            library='Internal-Rdv',
            service_date='2009_01',
            service_name='VariantManagement',
            params={'metaExprs': metaExprs},
            response_cls=ValidateNVEMetaExprResponse,
        )

    @classmethod
    def applyNVEMetaExpression(cls, bomlines: List[BOMLine], metaExpr: List[NVEMetaToken], validate: bool) -> ServiceData:
        """
        This operation applies the given MetaExpression to the set of BOMLine objects. Meta expressions are used to
        balance the tree structure amongst the variant expressions and validate the input combination of Named Variant
        Expressions (NVEs). MetaExpression is the internal representation of the Thought. If the input parameter
        validate is true then the MetaExpression will be validated before applying on the BOMLine. This operation
        creates the NVEMetaExpression object from the list of NVEMetaToken objects. The operation fails if input
        MetaExpression is invalid.
        
        Use cases:
        Applying Thought to set of BOMLine objects with or without validation
        In order to apply Thought with validation user can set input argument 'validate' to true. To apply Thought
        without validation user can set 'validate' to false.
        """
        return cls.execute_soa_method(
            method_name='applyNVEMetaExpression',
            library='Internal-Rdv',
            service_date='2009_01',
            service_name='VariantManagement',
            params={'bomlines': bomlines, 'metaExpr': metaExpr, 'validate': validate},
            response_cls=ServiceData,
        )

    @classmethod
    def askNVEMetaExpression(cls, bomlines: List[BOMLine]) -> NVEMetaExpressionResponse:
        """
        This operation creates the 'MetaExprTokens' object corresponding to the BOMLine. MetaExprTokens contains the
        list of 'NVEMetaToken' which represents a token. Meta expressions are used to balance the tree structure
        amongst the variant expressions and validate the input combination of Named Variant Expressions (NVEs). Meta
        expressions are stored in the variant expression block contained in absoccdata associated with bomline. This
        operation fails if input parameter bomlines contain invalid bomline. It returns the 'NVEMetaExpressionResponse'
        object which encapsulates the list of 'MetaExprTokens' and 'ServiceData' objects.
        
        Use cases:
        Use Case 1: Getting a Thought
        This operation can be used to get the Thought associated with the BOMLine, it returns the MetaExprTokens which
        can be converted into a Thought.
        
        Use Case 2: Validating a Thought
        This operation can also be used to validate a Thought associated with the BOMLine, it returns the
        MetaExprTokens which is the internal representation of the Thought. MetaExprTokens can be validated at the
        server side.
        """
        return cls.execute_soa_method(
            method_name='askNVEMetaExpression',
            library='Internal-Rdv',
            service_date='2009_01',
            service_name='VariantManagement',
            params={'bomlines': bomlines},
            response_cls=NVEMetaExpressionResponse,
        )

    @classmethod
    def getApnComponents(cls, inputs: GetABandABEInputInfo) -> GetABandABEResponse:
        """
        This operation verifies if an Architecture Breakdown Element (ABE) exists in the given Architecture assembly or
        not for the given input generic component ID (could be a wildcard string input). If ABE exists then the
        operation returns the MEAPN(s) of the component(s) in a 'GetABandABEResponse' response object, else the
        response object is empty. Any failure in the operation is returned as a full/partial error added to the
        'ServiceData' object contained in the response object.
        
        Use cases:
        Use Case 1: Search Architecture Breakdown Element with given criteria
        This operation helps user to find ABE(s) by providing the search criteria in 'GetABandABEInputInfo' object,
        only single 'GetABandABEInputInfo' object as an input is supported by this operation. The operation returns one
        or more matching APNs in the resultant 'GetABandABEResponse' object containing the details of each APN.
        """
        return cls.execute_soa_method(
            method_name='getApnComponents',
            library='Internal-Rdv',
            service_date='2009_01',
            service_name='VariantManagement',
            params={'inputs': inputs},
            response_cls=GetABandABEResponse,
        )

    @classmethod
    def getArchbreakdownBomlineChildComponents(cls, inputs: GetAbeChildComponentsInputInfo) -> GetAbeBomlineChildComponentsResponse:
        """
        This operation retrieves the child MEAppearancePathNodes (MEAPN) and their respective BOMLine objects for a
        given parent MEAppearancePathNode. The 'topLevelItem' passed as part of the input structure is the reference to
        Architecture Breakdown which is the topline in Architecture Breakdown structure.
        
        The MEAPN passed as part of the input structure is the MEAppearancePathNode of the parent whose child
        MEAppearancePathNodes are to be retrieved. This operation fails if 'topLevelItem' is not supplied or it is not
        of type ArchitectureImpl. This operation fails if 'bomWindow' in the input structure is not supplied.
        
        
        Use cases:
        This operation can be used to get the child MEAppearancePathNodes and their respective BOMLine objects by
        providing reference to Architecture Breakdown, MEAppearancePathNode of parent and BOMWindow object in the
        'GetAbeChildComponentsInputInfo' structure.
        """
        return cls.execute_soa_method(
            method_name='getArchbreakdownBomlineChildComponents',
            library='Internal-Rdv',
            service_date='2009_01',
            service_name='VariantManagement',
            params={'inputs': inputs},
            response_cls=GetAbeBomlineChildComponentsResponse,
        )

    @classmethod
    def getArchbreakdownMeapnChildComponents(cls, inputs: GetAbeChildComponentsInputInfo) -> GetAbeMeapnChildComponentsResponse:
        """
        This operation retrieves the child MEAppearancePathNodes (MEAPNs), their respective generic component IDs and
        description for a given parent MEAPN. If child components exist, the operation returns the child MEAPNs of the
        parent component in a 'GetAbeMeapnChildComponentsResponse' response object, else the response object is empty.
        Any failure in the operation is returned as a full/partial 'ServiceData' object contained in the response
        object.
        
        Use cases:
        Use Case 1: Get child Architecture Breakdown Element(s) for given top level architecture
        This operation helps user to get all the child ABEs of the given top level Architecture Breakdown structure
        (input provided using 'GetAbeChildComponentsInputInfo' object), only single 'GetAbeChildComponentsInputInfo'
        object as an input is supported by this operation. The operation returns all the child ABEs in the resultant
        'GetAbeMeapnChildComponentsResponse' object containing the details of each ABE.
        """
        return cls.execute_soa_method(
            method_name='getArchbreakdownMeapnChildComponents',
            library='Internal-Rdv',
            service_date='2009_01',
            service_name='VariantManagement',
            params={'inputs': inputs},
            response_cls=GetAbeMeapnChildComponentsResponse,
        )
