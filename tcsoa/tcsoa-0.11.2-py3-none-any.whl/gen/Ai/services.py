from tcsoa.gen.Ai._2006_03.services import AiService as imp0
from tcsoa.gen.Ai._2008_06.services import AiService as imp1
from tcsoa.gen.Ai._2014_12.services import AiService as imp2
from tcsoa.gen.Ai._2013_05.services import AiService as imp3
from tcsoa.gen.Ai._2012_09.services import AiService as imp4
from tcsoa.gen.Ai._2013_12.services import AiService as imp5
from tcsoa.gen.Ai._2010_09.services import AiService as imp6
from tcsoa.gen.Ai._2008_05.services import AiService as imp7
from tcsoa.gen.Ai._2007_12.services import AiService as imp8
from tcsoa.gen.Ai._2009_06.services import AiService as imp9
from tcsoa.gen.Ai._2018_06.services import AiService as imp10
from tcsoa.gen.Ai._2009_10.services import AiService as imp11
from tcsoa.base import TcService


class AiService(TcService):
    commitFiles = imp0.commitFiles
    commitStructureFile = imp0.commitStructureFile
    compareConfigurationContexts = imp1.compareConfigurationContexts
    createApplicationInterfaceRecords = imp2.createApplicationInterfaceRecords
    createProjects = imp0.createProjects
    createPublishRequest = imp0.createPublishRequest
    deleteProjects = imp0.deleteProjects
    deleteRequests = imp0.deleteRequests
    endExchange = imp0.endExchange
    findRequestOnAiWithReferences = imp3.findRequestOnAiWithReferences
    findRequests = imp4.findRequests
    findRequestsWithDependencies = imp5.findRequestsWithDependencies
    generateAndEvaluateStructure = imp6.generateAndEvaluateStructure
    generateArrangements = imp7.generateArrangements
    generateFullSyncRequest = imp0.generateFullSyncRequest
    generateScopedMultipleStructure = imp8.generateScopedMultipleStructure
    generateScopedMultipleStructure2 = imp1.generateScopedMultipleStructure2
    generateScopedMultipleStructure3 = imp9.generateScopedMultipleStructure3
    generateScopedSyncRequest = imp8.generateScopedSyncRequest
    generateScopedSyncRequest2 = imp1.generateScopedSyncRequest2
    generateStructure = imp0.generateStructure
    getFileReadTickets = imp0.getFileReadTickets
    getFileWriteTickets = imp0.getFileWriteTickets
    getMappedApplicationRefs = imp2.getMappedApplicationRefs
    getNextApprovedRequest = imp0.getNextApprovedRequest
    getObjectsByApplicationRefs = imp10.getObjectsByApplicationRefs
    getPersistentObjects = imp9.getPersistentObjects
    getProjects = imp0.getProjects
    getProjects2 = imp4.getProjects
    getProjectsInfo = imp0.getProjectsInfo
    getProjectsInfo2 = imp4.getProjectsInfo2
    getPropertiesOfObjects = imp0.getPropertiesOfObjects
    getPropertyValues = imp11.getPropertyValues
    getRequestsForProject = imp0.getRequestsForProject
    getRequestsInfo = imp0.getRequestsInfo
    getRequestsInfo2 = imp4.getRequestsInfo2
    getStructureReadTicket = imp0.getStructureReadTicket
    getStructureWriteTicket = imp0.getStructureWriteTicket
    objectsExist = imp0.objectsExist
    processPublishRequest = imp0.processPublishRequest
    processStructure = imp0.processStructure
    setExchangeMessage = imp0.setExchangeMessage
    setProjectsInfo = imp0.setProjectsInfo
    setProjectsInfo2 = imp4.setProjectsInfo
    setRequestsInfo = imp4.setRequestsInfo
    startExchange = imp0.startExchange
