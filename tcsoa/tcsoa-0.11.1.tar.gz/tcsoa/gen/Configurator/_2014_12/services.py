from __future__ import annotations

from tcsoa.gen.BusinessObjects import Cfg0ConfiguratorPerspective
from tcsoa.gen.Configurator._2014_12.ConfiguratorManagement import GetAdmissibilityResponse, GetAdmissibilityInputStruct
from typing import List
from tcsoa.base import TcService


class ConfiguratorManagementService(TcService):

    @classmethod
    def getAdmissibility(cls, operationConfigPerspective: Cfg0ConfiguratorPerspective, admissibilityInputs: List[GetAdmissibilityInputStruct]) -> GetAdmissibilityResponse:
        """
        This operation returns the admissibility statements for the variability data associated with a given set of
        context objects. The instance of Cfg0AbsAdmissibility object represents the relation and state between a
        configurator specific object and a non-configurator specific object. For example, the pair of a partition and
        an family is associated with state "Available". The admissibility states are defined by the LOV
        Cfg0AdmissibilityState. The allowed values for this property are "Available" and "Not Available".
        
        Use cases:
        Consider that following set of the data-
        
        Groups-
        Engine-Box (A Family Group) - It has families "Engine" and "Transmission". 
        1. Engine- Petrol, Diesel
        2. Transmission - Manual, Auto
        Wheel (A Family Group) - It has families "Wheel-drive" and "Suspension". 
        1. Wheel-drive - 2-Wheels, 4-Wheels
        2. Suspension - Full-Thrust, Full-Boom
        For the Engine partition object, the families, Engine &amp; Transmission are "Available" and the families
        Wheel-drive &amp; Suspension are "Not Available".
        The response of the operation for  the Engine partition object will have  the list of  Cfg0AbsAdmissibility
        objects for families Engine and Transmission, 1 for each and those will have admissibility state as "Available"
        and also the Cfg0AbsAdmissibility objects for the families Wheel-drive and Suspension, 1 for each and those
        will have admissibility state as "Not Available".
        
        Exceptions:
        >The operation will return a ServiceException if an unknown error occurs. A possible source for unknown errors
        could be a codeful configurator component customization.
        """
        return cls.execute_soa_method(
            method_name='getAdmissibility',
            library='Configurator',
            service_date='2014_12',
            service_name='ConfiguratorManagement',
            params={'operationConfigPerspective': operationConfigPerspective, 'admissibilityInputs': admissibilityInputs},
            response_cls=GetAdmissibilityResponse,
        )
