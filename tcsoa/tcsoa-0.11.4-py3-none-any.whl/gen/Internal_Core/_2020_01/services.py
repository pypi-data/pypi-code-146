from __future__ import annotations

from tcsoa.gen.Internal.Core._2020_01.ActiveModeler import AddPropsOnTypeInput, TypeInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ActiveModelerService(TcService):

    @classmethod
    def addPropertiesOnTypes(cls, addPropsOnTypeInputs: List[AddPropsOnTypeInput]) -> ServiceData:
        """
        This method adds new properties on existing Business object types. This method validates the inputs, creates
        the new properties and updates a dataset with the inputs. This dataset will be later used by BMIDE client to
        sync the custom template.
        
        Use cases:
        Add properties on type.
        """
        return cls.execute_soa_method(
            method_name='addPropertiesOnTypes',
            library='Internal-Core',
            service_date='2020_01',
            service_name='ActiveModeler',
            params={'addPropsOnTypeInputs': addPropsOnTypeInputs},
            response_cls=ServiceData,
        )

    @classmethod
    def createTypes(cls, typeInput: List[TypeInput]) -> ServiceData:
        """
        This method creates new business object types. This method will validate the inputs, create the business object
        type and create datasets with input information. The dataset will be used to sync up changes into an existing
        Business Modeler IDE (BMIDE) project.
        
        Use cases:
        Create Teamcenter Type.
        """
        return cls.execute_soa_method(
            method_name='createTypes',
            library='Internal-Core',
            service_date='2020_01',
            service_name='ActiveModeler',
            params={'typeInput': typeInput},
            response_cls=ServiceData,
        )
