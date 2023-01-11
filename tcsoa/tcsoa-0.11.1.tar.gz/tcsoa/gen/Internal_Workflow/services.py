from tcsoa.gen.Internal_Workflow._2017_11.services import WorkflowService as imp0
from tcsoa.gen.Internal_Workflow._2013_05.services import WorkflowService as imp1
from tcsoa.base import TcService


class WorkflowService(TcService):
    createWorkflowAsync = imp0.createWorkflowAsync
    performActionAsync = imp1.performActionAsync
