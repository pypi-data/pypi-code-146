from tcsoa.gen.Internal_GlobalMultiSite._2020_01.services import BriefcaseService as imp0
from tcsoa.gen.Internal_GlobalMultiSite._2018_11.services import BriefcaseService as imp1
from tcsoa.gen.Internal_GlobalMultiSite._2007_06.services import SynchronizerService as imp2
from tcsoa.gen.Internal_GlobalMultiSite._2007_06.services import ImportExportService as imp3
from tcsoa.gen.Internal_GlobalMultiSite._2020_01.services import OwnershipRecoveryService as imp4
from tcsoa.gen.Internal_GlobalMultiSite._2008_06.services import SynchronizerService as imp5
from tcsoa.gen.Internal_GlobalMultiSite._2010_02.services import LowlevelOwnershipTransferService as imp6
from tcsoa.gen.Internal_GlobalMultiSite._2010_09.services import LowlevelOwnershipTransferService as imp7
from tcsoa.gen.Internal_GlobalMultiSite._2007_06.services import DataMigrationService as imp8
from tcsoa.gen.Internal_GlobalMultiSite._2007_06.services import BriefcaseService as imp9
from tcsoa.gen.Internal_GlobalMultiSite._2017_05.services import ImportExportService as imp10
from tcsoa.base import TcService


class BriefcaseService(TcService):
    addMarkOTForCurrentUser = imp0.addMarkOTForCurrentUser
    checkBriefcaseLicense = imp1.checkBriefcaseLicense
    getBriefcasePreviewData = imp1.getBriefcasePreviewData
    getObjectsLockInfo = imp0.getObjectsLockInfo
    packageBriefcaseContents = imp9.packageBriefcaseContents
    queryMarkOT = imp0.queryMarkOT
    removeMarkOTForCurrentUser = imp0.removeMarkOTForCurrentUser
    unpackBriefcaseContents = imp9.unpackBriefcaseContents


class SynchronizerService(TcService):
    checkReplicaSyncState = imp2.checkReplicaSyncState
    createExportRecordOnStubReplication = imp2.createExportRecordOnStubReplication
    getCandidatesForClasseswOpts = imp5.getCandidatesForClasseswOpts
    getCandidatesForObjectswOpts = imp5.getCandidatesForObjectswOpts
    getCandidatesToSynchronizeForListOfClasses = imp2.getCandidatesToSynchronizeForListOfClasses
    getCandidatesToSynchronizeForListOfObjects = imp2.getCandidatesToSynchronizeForListOfObjects
    getExportedObjects = imp5.getExportedObjects
    updateMasterObjectsOnReplicaDeletion = imp2.updateMasterObjectsOnReplicaDeletion
    updateObjectsOnOwnershipChange = imp2.updateObjectsOnOwnershipChange


class ImportExportService(TcService):
    confirmExport = imp3.confirmExport
    dryRunExport = imp3.dryRunExport
    exportObjects = imp3.exportObjects
    importObjects = imp3.importObjects
    requestExportToRemoteSites = imp3.requestExportToRemoteSites
    requestImportFromRemoteSites = imp3.requestImportFromRemoteSites
    transformData = imp10.transformData


class OwnershipRecoveryService(TcService):
    deleteOtTransaction = imp4.deleteOtTransaction
    findOtTransactions = imp4.findOtTransactions
    recoverOwnership = imp4.recoverOwnership
    recoverOwnershipUsingBriefcase = imp4.recoverOwnershipUsingBriefcase


class LowlevelOwnershipTransferService(TcService):
    getObjectsForOwnershipTransfer = imp6.getObjectsForOwnershipTransfer
    getObjectsForOwnershipTransfer2 = imp7.getObjectsForOwnershipTransfer
    transferOwnership = imp6.transferOwnership
    updateOwnershipTransfer = imp6.updateOwnershipTransfer


class DataMigrationService(TcService):
    getRUO = imp8.getRUO
    setRUO = imp8.setRUO
