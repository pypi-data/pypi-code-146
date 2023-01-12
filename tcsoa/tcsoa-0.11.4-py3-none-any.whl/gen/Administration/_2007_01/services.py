from __future__ import annotations

from tcsoa.gen.Administration._2007_01.UserManagement import CreateDisciplinesResponse, CreateDisciplinesIn
from typing import List
from tcsoa.base import TcService


class UserManagementService(TcService):

    @classmethod
    def createDisciplines(cls, disciplines: List[CreateDisciplinesIn]) -> CreateDisciplinesResponse:
        """
        This operation creates a list of new Discipline objects based on the list of CreateDisciplineIn objects. If 
        parent group is specified in the CreateDisciplinesIn object, the discipline objects would be added into the
        group. This operation requires system administration or group administration privilege.
        """
        return cls.execute_soa_method(
            method_name='createDisciplines',
            library='Administration',
            service_date='2007_01',
            service_name='UserManagement',
            params={'disciplines': disciplines},
            response_cls=CreateDisciplinesResponse,
        )
