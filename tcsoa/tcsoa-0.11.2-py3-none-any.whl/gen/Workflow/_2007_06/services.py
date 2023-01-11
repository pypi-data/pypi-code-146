from __future__ import annotations

from typing import List
from tcsoa.gen.Workflow._2007_06.Workflow import ReleaseStatusInput, SetReleaseStatusResponse
from tcsoa.base import TcService


class WorkflowService(TcService):

    @classmethod
    def setReleaseStatus(cls, input: List[ReleaseStatusInput]) -> SetReleaseStatusResponse:
        """
        Manages the release status status of an object
        
        The permitted operations are Append, Delete, Rename and Replace
        Currently Append and Delete are supported
        With the delete operation if an empty string is passed in instead of the status name all
        statuses will be cleared for that set of workspace objects
        
        Exceptions:
        >Teamcenter::Soa::Server::ServiceException:
        """
        return cls.execute_soa_method(
            method_name='setReleaseStatus',
            library='Workflow',
            service_date='2007_06',
            service_name='Workflow',
            params={'input': input},
            response_cls=SetReleaseStatusResponse,
        )
