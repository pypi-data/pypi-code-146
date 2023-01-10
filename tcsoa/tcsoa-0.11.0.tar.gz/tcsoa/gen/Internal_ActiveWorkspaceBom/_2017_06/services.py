from __future__ import annotations

from tcsoa.gen.Internal.ActiveWorkspaceBom._2017_06.OccurrenceConfiguration import ConfigRuleInput, ConfigRuleResponse
from tcsoa.gen.Internal.ActiveWorkspaceBom._2017_06.OccurrenceManagement import EffectivityCreateInput, EffectivityEditInput, UserContextState
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class OccurrenceManagementService(TcService):

    @classmethod
    def createAndAddElementEffectivity(cls, input: EffectivityCreateInput) -> ServiceData:
        """
        This operation creates and adds Effectivity to the input Awb0Element. The impacted Awb0Element(s) are
        reconfigured with new effectivity.
        
        Exceptions:
        >This operation may raise a ServiceException containing following   
        errors:
        
        - 126002 No Adapter could be found to handle the request.
        - 126225 The effectivities cannot be updated on Awb0Element.
        - 126228 The effectivity cannot be created.
        
        """
        return cls.execute_soa_method(
            method_name='createAndAddElementEffectivity',
            library='Internal-ActiveWorkspaceBom',
            service_date='2017_06',
            service_name='OccurrenceManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def editElementEffectivity(cls, input: EffectivityEditInput) -> ServiceData:
        """
        This operation updates Effectivity of the input Awb0Element. The impacted Awb0Element(s) are reconfigured with
        the updated effectivity
        
        Exceptions:
        >This operation may raise a ServiceException containing following 
        errors:
        - 126002 No Adapter could be found to handle the request.
        - 126225 The effectivity cannot be updated on Awb0Element.
        
        """
        return cls.execute_soa_method(
            method_name='editElementEffectivity',
            library='Internal-ActiveWorkspaceBom',
            service_date='2017_06',
            service_name='OccurrenceManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def saveUserWorkingContextState(cls, contextState: UserContextState) -> ServiceData:
        """
        This operation saves current user's client state information for the opened object. The saved information is
        used to establish user's working state while opening the object again.
        """
        return cls.execute_soa_method(
            method_name='saveUserWorkingContextState',
            library='Internal-ActiveWorkspaceBom',
            service_date='2017_06',
            service_name='OccurrenceManagement',
            params={'contextState': contextState},
            response_cls=ServiceData,
        )


class OccurrenceConfigurationService(TcService):

    @classmethod
    def getConfigurationRules(cls, input: ConfigRuleInput) -> ConfigRuleResponse:
        """
        This operation returns a list of RevisionRule or VariantRule based on the input product context information.
        The number of RevisionRule or VariantRule in the response depends on the page size.
        """
        return cls.execute_soa_method(
            method_name='getConfigurationRules',
            library='Internal-ActiveWorkspaceBom',
            service_date='2017_06',
            service_name='OccurrenceConfiguration',
            params={'input': input},
            response_cls=ConfigRuleResponse,
        )
