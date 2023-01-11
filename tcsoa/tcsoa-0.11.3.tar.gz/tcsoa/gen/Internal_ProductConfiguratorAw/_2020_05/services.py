from __future__ import annotations

from tcsoa.gen.Internal.ProductConfiguratorAw._2020_05.ConfiguratorManagement import GetConfiguratorDataHierarchyIn, GetConfiguratorDataHierarchyResp
from tcsoa.base import TcService


class ConfiguratorManagementService(TcService):

    @classmethod
    def getConfiguratorDataHierarchy(cls, input: GetConfiguratorDataHierarchyIn) -> GetConfiguratorDataHierarchyResp:
        """
        This operation returns the content of Configurator Context and Dictionary based on UI widget. E.g. the data can
        be Product Line Hierarchy and / or Product Models if "Products" tab is opened and Variability data if
        "Features" tab is opened. The operation allows to sort the result by additional filters and sorting criteria
        that is provided as input.
        
        Exceptions:
        >The following service exception may be returned:
        
        77073    The operation has failed, because an invalid Configurator Perspective was passed.
        77074    The operation must contain a product item or dictionary in the Configurator Perspective.
        333012    The operation has failed because of invalid request type.
        333013    The operation has failed because of invalid parent object.
        333014    The operation has failed because of invalid Expand type.
        333015    The operation has failed because of invalid view type.
        """
        return cls.execute_soa_method(
            method_name='getConfiguratorDataHierarchy',
            library='Internal-ProductConfiguratorAw',
            service_date='2020_05',
            service_name='ConfiguratorManagement',
            params={'input': input},
            response_cls=GetConfiguratorDataHierarchyResp,
        )
