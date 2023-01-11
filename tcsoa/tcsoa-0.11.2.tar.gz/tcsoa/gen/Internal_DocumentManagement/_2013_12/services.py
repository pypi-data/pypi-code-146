from __future__ import annotations

from tcsoa.gen.Internal.DocumentManagement._2013_12.Markup import MarkupResponse
from tcsoa.base import TcService
from tcsoa.gen.BusinessObjects import WorkspaceObject


class MarkupService(TcService):

    @classmethod
    def loadMarkups(cls, baseObject: WorkspaceObject, version: str, message: str) -> MarkupResponse:
        """
        This operation loads the markups visible to the current session user.
        
        Use cases:
        When the user starts Markup tool on the client, the application loads from the server the markups made by other
        users that are visible to this user on the client.
        """
        return cls.execute_soa_method(
            method_name='loadMarkups',
            library='Internal-DocumentManagement',
            service_date='2013_12',
            service_name='Markup',
            params={'baseObject': baseObject, 'version': version, 'message': message},
            response_cls=MarkupResponse,
        )

    @classmethod
    def saveMarkups(cls, baseObject: WorkspaceObject, version: str, message: str, markups: str) -> MarkupResponse:
        """
        This operation saves the markups to the server.
        
        Use cases:
        After the user modified the markups on the client, save them to the server so that other users can read the
        updated markups.
        """
        return cls.execute_soa_method(
            method_name='saveMarkups',
            library='Internal-DocumentManagement',
            service_date='2013_12',
            service_name='Markup',
            params={'baseObject': baseObject, 'version': version, 'message': message, 'markups': markups},
            response_cls=MarkupResponse,
        )
