from tcsoa.gen.Internal_DebugMonitor._2011_06.services import DebugMonitorService as imp0
from tcsoa.gen.Internal_DebugMonitor._2011_06.services import PerformanceMonitorService as imp1
from tcsoa.gen.Internal_DebugMonitor._2011_06.services import DebugLoggingService as imp2
from tcsoa.gen.Internal_DebugMonitor._2015_07.services import DebugLoggingService as imp3
from tcsoa.gen.Internal_DebugMonitor._2014_06.services import JournalBasedTestingService as imp4
from tcsoa.gen.Internal_DebugMonitor._2019_06.services import DebugLoggingService as imp5
from tcsoa.gen.Internal_DebugMonitor._2015_10.services import JournalBasedTestingService as imp6
from tcsoa.base import TcService


class DebugMonitorService(TcService):
    clearAllHistory = imp0.clearAllHistory
    clearHistory = imp0.clearHistory
    getAlertInformation = imp0.getAlertInformation
    getMetricMetaData = imp0.getMetricMetaData
    getOperationalHealthData = imp0.getOperationalHealthData
    getTcServerMonitoringMode = imp0.getTcServerMonitoringMode
    getValidMetrics = imp0.getValidMetrics
    reloadConfiguration = imp0.reloadConfiguration
    setMetricConfig = imp0.setMetricConfig
    setTcServerMonitoringMode = imp0.setTcServerMonitoringMode


class PerformanceMonitorService(TcService):
    clearPerformanceInformation = imp1.clearPerformanceInformation
    getPerformanceInformation = imp1.getPerformanceInformation
    monitorPerformance = imp1.monitorPerformance


class DebugLoggingService(TcService):
    dumpStatistics = imp2.dumpStatistics
    getCheckingLevel = imp2.getCheckingLevel
    getDebugStatus = imp2.getDebugStatus
    getJournalFile = imp2.getJournalFile
    getJournalingStatus = imp2.getJournalingStatus
    getLoggerLevels = imp2.getLoggerLevels
    getModuleJournalStatus = imp2.getModuleJournalStatus
    getPerformanceJournalLevel = imp3.getPerformanceJournalLevel
    getSQLLogging = imp2.getSQLLogging
    getStatisticsStatus = imp2.getStatisticsStatus
    getSyslogFile = imp2.getSyslogFile
    getTAOLogLevel = imp2.getTAOLogLevel
    resetStatistics = imp2.resetStatistics
    setCheckingLevel = imp2.setCheckingLevel
    setJournalEntries = imp2.setJournalEntries
    setLoggerLevels = imp2.setLoggerLevels
    setModuleJournalStatus = imp2.setModuleJournalStatus
    setPerformanceJournalLevel = imp3.setPerformanceJournalLevel
    setSQLLogging = imp2.setSQLLogging
    setStatistics = imp2.setStatistics
    setTAOLogLevel = imp2.setTAOLogLevel
    startLogging = imp5.startLogging
    stopLogging = imp5.stopLogging


class JournalBasedTestingService(TcService):
    initializeJBT = imp4.initializeJBT
    terminateJBT = imp6.terminateJBT
    validatePropertyValues = imp4.validatePropertyValues
