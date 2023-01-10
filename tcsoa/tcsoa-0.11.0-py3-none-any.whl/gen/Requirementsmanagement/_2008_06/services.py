from __future__ import annotations

from tcsoa.gen.Requirementsmanagement._2008_06.RequirementsManagement import GetContentInput1
from tcsoa.gen.Requirementsmanagement._2007_01.RequirementsManagement import GetRichContentResponse
from typing import List
from tcsoa.base import TcService


class RequirementsManagementService(TcService):

    @classmethod
    def getRichContent(cls, inputs: List[GetContentInput1]) -> GetRichContentResponse:
        """
        The SOA operation is responsible for retrieving contents of objects of type SpecElement. It can be used to view
        content of SpecElement in word. SOA also provides capability to view contents by applying default templates.
        
        Use cases:
        User can open requirements in word using default templates or they can open content (body text) in word for
        view and edit purpose.
        
        Exceptions:
        >If there is any error during generating transient file read ticket due to a configuration issue at the server,
        then the operation throws a service exception. Example- If the transient volume directory is not configured at
        the server then the FMS fails to generate a file at the server and subsequent file download operation fails. In
        such situation a service exception is thrown.
        """
        return cls.execute_soa_method(
            method_name='getRichContent',
            library='Requirementsmanagement',
            service_date='2008_06',
            service_name='RequirementsManagement',
            params={'inputs': inputs},
            response_cls=GetRichContentResponse,
        )
