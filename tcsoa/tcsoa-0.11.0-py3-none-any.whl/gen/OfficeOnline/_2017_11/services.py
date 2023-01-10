from __future__ import annotations

from tcsoa.gen.OfficeOnline._2017_11.OfficeOnline import LaunchInfoOutputResponse, LaunchInfoInput
from typing import List
from tcsoa.base import TcService


class OfficeOnlineService(TcService):

    @classmethod
    def getLaunchInfo(cls, inputs: List[LaunchInfoInput]) -> LaunchInfoOutputResponse:
        """
        This operation retrieves the launch information for a Teamcenter Dataset that a client can use to access Office
        Online to view or edit a Microsoft document. The launch URL is the address to use to connect to the Office
        Online Server (OOS) to open a Microsoft Office file in Office Online.
        
        Integration with Office Online requires implementation of the Web Application Open Platform Interface (WOPI)
        protocol.  For this protocol, the OOS is called the WOPI client and the Teamcenter component that OOS
        communications with is called the WOPI host.  The Teamcenter WOPI host implements REST based APIs specific to
        the WOPI protocol for the Office Online WOPI client to use to work with files stored in Teamcenter.
        
        Use cases:
        A Teamcenter client finds and selects a Dataset for a Microsoft Office document and chooses to view or edit the
        document.  The client calls this operation to retrieve the launch URL to access Office Online to view or edit
        the Microsoft Office document.
        """
        return cls.execute_soa_method(
            method_name='getLaunchInfo',
            library='OfficeOnline',
            service_date='2017_11',
            service_name='OfficeOnline',
            params={'inputs': inputs},
            response_cls=LaunchInfoOutputResponse,
        )
