from __future__ import annotations

from tcsoa.gen.Ai._2006_03.Ai import ApplicationRef
from tcsoa.gen.Internal.Ai._2008_06.Ai import GenerateMonolithicJtOptions, EndGenerateMonolithicJtResponse, BeginGenerateMonolithicJtResponse
from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Ai._2007_12.Ai import Configuration2
from tcsoa.base import TcService


class AiService(TcService):

    @classmethod
    def invoke(cls, methodName: str, strIn: str) -> str:
        """
        Invoke method that takes a string and outputs a string. This is in place for backward
        compatibility with existing AIWS clients that used this method to call custom hook furnctions.
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='invoke',
            library='Internal-Ai',
            service_date='2008_06',
            service_name='Ai',
            params={'methodName': methodName, 'strIn': strIn},
            response_cls=str,
        )

    @classmethod
    def endGenerateMonolithicJt(cls, request: BusinessObject, serverMode: int) -> EndGenerateMonolithicJtResponse:
        """
        Get the status of a TSTK request object. To be used in conjunction with BeginGenerateMonolithicJt.
        """
        return cls.execute_soa_method(
            method_name='endGenerateMonolithicJt',
            library='Internal-Ai',
            service_date='2008_06',
            service_name='Ai',
            params={'request': request, 'serverMode': serverMode},
            response_cls=EndGenerateMonolithicJtResponse,
        )

    @classmethod
    def beginGenerateMonolithicJt(cls, startingNode: ApplicationRef, itemId: str, revId: str, config: Configuration2, options: GenerateMonolithicJtOptions, serverMode: int) -> BeginGenerateMonolithicJtResponse:
        """
        Generates a monolithic jt file given a structure.
        """
        return cls.execute_soa_method(
            method_name='beginGenerateMonolithicJt',
            library='Internal-Ai',
            service_date='2008_06',
            service_name='Ai',
            params={'startingNode': startingNode, 'itemId': itemId, 'revId': revId, 'config': config, 'options': options, 'serverMode': serverMode},
            response_cls=BeginGenerateMonolithicJtResponse,
        )
