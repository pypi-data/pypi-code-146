from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, EPMTask
from tcsoa.gen.Internal.Workflow._2013_05.Workflow import SoaEPMAction, SoaEPMSupportingValues
from tcsoa.base import TcService


class WorkflowService(TcService):

    @classmethod
    def performActionAsync(cls, task: EPMTask, action: SoaEPMAction, comments: str, password: str, supportingValue: SoaEPMSupportingValues, supportingObject: BusinessObject) -> None:
        """
        The method signature of performActionAsync will be same as the sync performAction except the output is a void
        type. It will be used by the Asynchronous Service. This method performs workflow actions on a task. The actions
        that can be performed using this operation are: assign, start, complete, skip, suspend, resume, undo, perform,
        approve, reject, promote and demote. Note: Special case this operation can be used to set only comments without
        changing the decision for perform signoff task. To do that, use the 'EPM_no_action' as input for action
        argument and use the current decision for the supportingValue argument.
        
        Exceptions:
        >Teamcenter::Soa::Server::ServiceException:
        """
        return cls.execute_soa_method(
            method_name='performActionAsync',
            library='Internal-Workflow',
            service_date='2013_05',
            service_name='Workflow',
            params={'task': task, 'action': action, 'comments': comments, 'password': password, 'supportingValue': supportingValue, 'supportingObject': supportingObject},
            response_cls=None,
        )
