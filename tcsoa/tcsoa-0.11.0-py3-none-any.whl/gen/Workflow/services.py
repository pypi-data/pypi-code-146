from tcsoa.gen.Workflow._2008_06.services import WorkflowService as imp0
from tcsoa.gen.Workflow._2015_07.services import WorkflowService as imp1
from tcsoa.gen.Workflow._2010_09.services import WorkflowService as imp2
from tcsoa.gen.Workflow._2019_06.services import WorkflowService as imp3
from tcsoa.gen.Workflow._2014_10.services import WorkflowService as imp4
from tcsoa.gen.Workflow._2020_01.services import WorkflowService as imp5
from tcsoa.gen.Workflow._2013_05.services import WorkflowService as imp6
from tcsoa.gen.Workflow._2012_10.services import WorkflowService as imp7
from tcsoa.gen.Workflow._2014_06.services import WorkflowService as imp8
from tcsoa.gen.Workflow._2007_06.services import WorkflowService as imp9
from tcsoa.base import TcService


class WorkflowService(TcService):
    addAttachments = imp0.addAttachments
    addSignoffs = imp0.addSignoffs
    addSignoffs2 = imp1.addSignoffs
    applyTemplateToProcesses = imp2.applyTemplateToProcesses
    applyTemplateToProcessesAsync = imp2.applyTemplateToProcessesAsync
    assignAllTasks = imp0.assignAllTasks
    changeState = imp0.changeState
    createInstance = imp0.createInstance
    createOrUpdateHandler = imp3.createOrUpdateHandler
    createOrUpdatePAL = imp3.createOrUpdatePAL
    createOrUpdateTemplate = imp3.createOrUpdateTemplate
    createRemoteWorkflowAsync = imp4.createRemoteWorkflowAsync
    createWorkflow = imp4.createWorkflow
    delegateSignoff = imp0.delegateSignoff
    getAllTasks = imp0.getAllTasks
    getAssignmentLists = imp0.getAssignmentLists
    getRegisteredHandlers = imp3.getRegisteredHandlers
    getResourcePool = imp0.getResourcePool
    getSupportedHandlerArguments = imp5.getSupportedHandlerArguments
    getWorkflowTemplates = imp0.getWorkflowTemplates
    getWorkflowTemplates2 = imp6.getWorkflowTemplates
    listDefinitions = imp0.listDefinitions
    performAction = imp0.performAction
    performAction2 = imp7.performAction2
    performAction3 = imp8.performAction3
    performActionWithSignature = imp8.performActionWithSignature
    removeAttachments = imp0.removeAttachments
    removeSignoffs = imp0.removeSignoffs
    setActiveSurrogate = imp8.setActiveSurrogate
    setOutOfOffice = imp8.setOutOfOffice
    setReleaseStatus = imp9.setReleaseStatus
    setSurrogate = imp8.setSurrogate
    viewAuditFile = imp0.viewAuditFile
