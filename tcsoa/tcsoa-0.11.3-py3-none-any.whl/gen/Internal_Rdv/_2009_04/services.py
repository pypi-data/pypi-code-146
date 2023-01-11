from __future__ import annotations

from tcsoa.gen.Internal.Rdv._2009_04.VariantManagement import DeleteNamedVariantExpressions, GetSVRResponse, GetSVRInfo, GetMultipleNVEResponse, MultipleNamedVariantExpressions
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class VariantManagementService(TcService):

    @classmethod
    def createMultipleNamedVariantExpressions(cls, input: MultipleNamedVariantExpressions) -> GetMultipleNVEResponse:
        """
        Creates a list of Named Variant Expressions (NVEs) based on the input structure. When Architecture Breakdown is
        using shared NVEs, the NVE gets created on the Architecture Breakdown. Architecture Breakdown is the topline in
        Architecture Breakdown structure. The payload variant expression passed as part of the input structure is used
        to create the NVE. The code is used as the name of the NVE. When using the shared NVEs, if the Architecture
        object or variant expression is not supplied then this operation will fail. It is required that applicable
        variability is assigned to the toplevel Architecture Breakdown before creating the NVE. When shared NVEs is
        used, all NVEs with in Architecture Breakdown must have a unique name. Each NVE should have a unique variant
        condition. When not using the shared NVEs, NVEs get created on the selected Architecture Breakdown Element.
        
        Use cases:
        The NVEs are created in the Architecture Breakdown structure as raw material for constructing the final variant
        condition on the design assembly. NVEs are applied on the design assembly during Replace Design in Product
        process.
        """
        return cls.execute_soa_method(
            method_name='createMultipleNamedVariantExpressions',
            library='Internal-Rdv',
            service_date='2009_04',
            service_name='VariantManagement',
            params={'input': input},
            response_cls=GetMultipleNVEResponse,
        )

    @classmethod
    def createSavedVariantRules(cls, input: GetSVRInfo) -> GetSVRResponse:
        """
        This operation creates multiple Saved Variant Rules (SVR) in order to configure a particular variant of a
        structure. The variant rule presents all the options that are used in the structure for which user can then set
        values as required. User does not have to specify values for all option, they can remain unset.
        SVRs created for configuring the part solutions are saved under the top level architecture item. If SVR already
        exists for the provided ItemRevision object, the operation will modify existing SVR with the default variant
        rule on which the option values are set.
        The values needed for creating SVR(s) is provided through the 'GetSVRInfo' object which is passed as a
        parameter input to this operation.
        
        Use cases:
        Use Case 1: Creating Saved Variant Rule(s)
        This operation is used when a user needs to create/modify one or more Saved Variant Rules in one go. All the
        details need to be specified in a list of 'GetSVRInfo' objects. The operation first attempts to find the
        existence of supplied SVR name, if it exists then SVR is modified otherwise new one is created. It is to be
        noted that only those 'SVRData' objects are processed whose both attributes option and value are set, failing
        to supply either of them will ignore the SVR processing.
        """
        return cls.execute_soa_method(
            method_name='createSavedVariantRules',
            library='Internal-Rdv',
            service_date='2009_04',
            service_name='VariantManagement',
            params={'input': input},
            response_cls=GetSVRResponse,
        )

    @classmethod
    def deleteMultipleNamedVariantExpressions(cls, input: DeleteNamedVariantExpressions) -> ServiceData:
        """
        Deletes the Named Variant Expressions (NVEs). When NVEs get deleted its reference from Architecture breakdown
        also gets deleted. NVE is owned by the Architecture Breakdown object. Input object contains the information of
        the NVEs that need to be deleted. If Architecture Breakdown object is not supplied then this operation will
        fail.
        
        Use cases:
        This operation can be used to delete the unused or wrongly created NamedVariantExpressions by passing the
        Architecture Breakdown object which owns the Named Variant Expression and list of NamedVariantExpression
        objects as a part of DeleteNamedVariantExpressions object.
        """
        return cls.execute_soa_method(
            method_name='deleteMultipleNamedVariantExpressions',
            library='Internal-Rdv',
            service_date='2009_04',
            service_name='VariantManagement',
            params={'input': input},
            response_cls=ServiceData,
        )
