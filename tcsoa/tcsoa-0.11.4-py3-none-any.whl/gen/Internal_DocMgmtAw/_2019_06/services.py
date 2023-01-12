from __future__ import annotations

from tcsoa.gen.Internal.DocMgmtAw._2019_06.DocMgmt import MarkupResponse, MarkupProperties
from tcsoa.base import TcService
from tcsoa.gen.BusinessObjects import WorkspaceObject


class DocMgmtService(TcService):

    @classmethod
    def processMarkups(cls, baseObject: WorkspaceObject, version: str, properties: MarkupProperties, markups: str) -> MarkupResponse:
        """
        Description:
        This operation processes the markups on the server. 
        Use Cases:
        - Load all the existing markups from the server.
        - Save the user created or modified markups to the server.
        
        """
        return cls.execute_soa_method(
            method_name='processMarkups',
            library='Internal-DocMgmtAw',
            service_date='2019_06',
            service_name='DocMgmt',
            params={'baseObject': baseObject, 'version': version, 'properties': properties, 'markups': markups},
            response_cls=MarkupResponse,
        )
