from __future__ import annotations

from tcsoa.gen.Internal.DebugMonitor._2011_06.DebugMonitor import MetricMetaData, ValidMetrics, MetricConfigMap, MetricAttributes, OperationalHealthData, AlertEventData
from tcsoa.gen.Internal.DebugMonitor._2011_06.DebugLogging import ModuleStatusResponse, ReturnStatus, ModuleStatus, CheckingLevelResponse, SQLLogInfo, LoggerLevel, SQLLogInfoResponse, TAOLogLevelResponse, LoggerLevelResponse
from typing import List
from tcsoa.gen.Internal.DebugMonitor._2011_06.PerformanceMonitor import PerformanceInfoResponse
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class DebugLoggingService(TcService):

    @classmethod
    def getSQLLogging(cls) -> SQLLogInfoResponse:
        """
        Retrieve the SQL logging options in effect in the current Teamcenter session.
        """
        return cls.execute_soa_method(
            method_name='getSQLLogging',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugLogging',
            params={},
            response_cls=SQLLogInfoResponse,
        )

    @classmethod
    def getStatisticsStatus(cls) -> bool:
        """
        Return the status of whether journal summary statistics are being collected or not in the current Teamcenter
        session.
        """
        return cls.execute_soa_method(
            method_name='getStatisticsStatus',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugLogging',
            params={},
            response_cls=bool,
        )

    @classmethod
    def getSyslogFile(cls, size: int) -> str:
        """
        Retrieves the most recent content of the current session`s active Teamcenter system log file (.syslog) as a
        string.
        """
        return cls.execute_soa_method(
            method_name='getSyslogFile',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugLogging',
            params={'size': size},
            response_cls=str,
        )

    @classmethod
    def getTAOLogLevel(cls) -> TAOLogLevelResponse:
        """
        This operation returns the current value of the TAO logging level for the server.
        A Teamcenter business logic server is a CORBA server, and TAO (The ACE ORB) is its open source CORBA
        implementation software.  TAO is capable of producing a log file, named for example
        'C:\TEMP\tcserver.exe16e001fa.orblog'.  The TAO logging level is an integer 0..10 that controls which type of
        information is logged to the file.  No logging is done at level 0, and maximum logging is done at level 10. 
        Specific details of particular levels can be found in TAO software documentation, and in the TAO open source
        code.
        Unless set otherwise, the log level is 0, and nothing is written to the file.  At the end of a successful
        session, the log file is automatically removed if it is empty.
        """
        return cls.execute_soa_method(
            method_name='getTAOLogLevel',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugLogging',
            params={},
            response_cls=TAOLogLevelResponse,
        )

    @classmethod
    def resetStatistics(cls) -> bool:
        """
        Resets the collected journal summary statistics to an initial zeroed out state.
        
        Use cases:
        The 'resetStatistics'  operation is used to reset the statistics at the current point of execution in order to
        start collecting fresh statistics from this point onwards.  To collect statistics for a segment of program
        execution, an administrator using the Server Manager Administrator interface will: 
        1.    Proceed to the start of the desired functionality to be measured.
        2.    'setStatistics(true)',  to start gathering statistics.
        3.    'resetStatistics ()', to clear any stale accumulated statistics.
        4.    Proceed through the functionality to be measured.
        5.    'setStatistics (false)', to stop gathering statistics.
        6.    'dumpStatistics ()', to capture the information in the system log.
        """
        return cls.execute_soa_method(
            method_name='resetStatistics',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugLogging',
            params={},
            response_cls=bool,
        )

    @classmethod
    def setCheckingLevel(cls, checkingLevel: int) -> bool:
        """
        Set the checking level for the current Teamcenter business logic server.  See getCheckingLevel.
        
        Exceptions:
        >214600   The checking level is not in the range 0 through 2.
        """
        return cls.execute_soa_method(
            method_name='setCheckingLevel',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugLogging',
            params={'checkingLevel': checkingLevel},
            response_cls=bool,
        )

    @classmethod
    def setJournalEntries(cls, journal: bool) -> bool:
        """
        Set whether or not the Teamcenter session will write journal entries to the journal file (.jnl)
        """
        return cls.execute_soa_method(
            method_name='setJournalEntries',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugLogging',
            params={'journal': journal},
            response_cls=bool,
        )

    @classmethod
    def setLoggerLevels(cls, loggerInput: List[LoggerLevel]) -> ServiceData:
        """
        Set the priority level of loggers in the business logic server of the current Teamcenter session.  If a logger
        node with the given name does not yet exist, it will be created.
        """
        return cls.execute_soa_method(
            method_name='setLoggerLevels',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugLogging',
            params={'loggerInput': loggerInput},
            response_cls=ServiceData,
        )

    @classmethod
    def setModuleJournalStatus(cls, journalModule: List[ModuleStatus]) -> ServiceData:
        """
        Set the journaling status of modules.
        
        The journaling subsystem tracks the entry and exit of major Teamcenter ITK routine and other major operations. 
        It writes the routine name, entry input parameter values, exit parameters, and execution time to the journal
        (.jnl) file.  The journal subsystem can be activated for specific modules, and deactivated for others.
        
        If any modules are turned on by this operation, the journal subsystem will be automatically turned on to write
        entries to the journal file.
        """
        return cls.execute_soa_method(
            method_name='setModuleJournalStatus',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugLogging',
            params={'journalModule': journalModule},
            response_cls=ServiceData,
        )

    @classmethod
    def setSQLLogging(cls, sqlLogInfo: SQLLogInfo) -> bool:
        """
        Set SQL Logging settings for the current Teamcenter session .  These control the information written to the
        system log for each executed SQL request to the database.
        """
        return cls.execute_soa_method(
            method_name='setSQLLogging',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugLogging',
            params={'sqlLogInfo': sqlLogInfo},
            response_cls=bool,
        )

    @classmethod
    def setStatistics(cls, stats: bool) -> bool:
        """
        Set whether or not to accumulate summary journal statistics in the current Teamcenter session.
        """
        return cls.execute_soa_method(
            method_name='setStatistics',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugLogging',
            params={'stats': stats},
            response_cls=bool,
        )

    @classmethod
    def setTAOLogLevel(cls, logLevel: int) -> bool:
        """
        Set the logging level for the TAO CORBA server code in the business logic server of the current Teamcenter
        session.  See the documentation of 'getTAOLogLevel' for additional details.
        """
        return cls.execute_soa_method(
            method_name='setTAOLogLevel',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugLogging',
            params={'logLevel': logLevel},
            response_cls=bool,
        )

    @classmethod
    def dumpStatistics(cls) -> bool:
        """
        Write the journal summary statistics to the Teamcenter system log file (.syslog)
        """
        return cls.execute_soa_method(
            method_name='dumpStatistics',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugLogging',
            params={},
            response_cls=bool,
        )

    @classmethod
    def getCheckingLevel(cls) -> CheckingLevelResponse:
        """
        Get the checking level.  The checking level is used in low level libsyss routines to activate additional
        diagnostic and validity checking code.  It is an integer 0,1,or 2, where 0 indicates no extra checking, 1
        indicates moderate checking, and 2 indicates advanced checking.   At checking level 2, performance may be
        significantly degraded.
        """
        return cls.execute_soa_method(
            method_name='getCheckingLevel',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugLogging',
            params={},
            response_cls=CheckingLevelResponse,
        )

    @classmethod
    def getDebugStatus(cls) -> ReturnStatus:
        """
        Retrieves the values of the primary debug statuses from the current Teamcenter session in a single request. 
        These are the Checking Level, Journaling status, Statistics status, TAO log level, and SQL logging settings.
        """
        return cls.execute_soa_method(
            method_name='getDebugStatus',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugLogging',
            params={},
            response_cls=ReturnStatus,
        )

    @classmethod
    def getJournalFile(cls, size: int) -> str:
        """
        Retrieves the most recent content of the current session`s active Teamcenter system journal file (.jnl) as a
        string.
        """
        return cls.execute_soa_method(
            method_name='getJournalFile',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugLogging',
            params={'size': size},
            response_cls=str,
        )

    @classmethod
    def getJournalingStatus(cls) -> bool:
        """
        Return the journaling state of the current Teamcenter session.
        """
        return cls.execute_soa_method(
            method_name='getJournalingStatus',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugLogging',
            params={},
            response_cls=bool,
        )

    @classmethod
    def getLoggerLevels(cls, nodeName: str) -> LoggerLevelResponse:
        """
        Retrieves the names and current priority level setting of loggers in the business logic server of the current
        Teamcenter session.   The name of a logger leaf node or an intermediate node in the logger tree is given, and
        the names and priority levels of each logger node in the given subtree are returned.
        """
        return cls.execute_soa_method(
            method_name='getLoggerLevels',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugLogging',
            params={'nodeName': nodeName},
            response_cls=LoggerLevelResponse,
        )

    @classmethod
    def getModuleJournalStatus(cls) -> ModuleStatusResponse:
        """
        Retrieve the names and journaling status of each defined journaling module. The journaling subsystem tracks the
        entry and exit of major Teamcenter ITK routines and other major operations.  It writes the routine name, entry
        input parameter values, exit parameters, and execution time to the journal (.jnl) file.  The journal subsystem
        can be activated for specific modules, and deactivated for others.
        """
        return cls.execute_soa_method(
            method_name='getModuleJournalStatus',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugLogging',
            params={},
            response_cls=ModuleStatusResponse,
        )


class DebugMonitorService(TcService):

    @classmethod
    def getTcServerMonitoringMode(cls) -> str:
        """
        The Teamcenter Server Monitoring System can operate in either of the three different monitoring modes Off,
        Collect or Alert. This method retrieves the current mode of operation. When in Off mode, the monitoring system
        does not record any monitoring data for the performance metrics. Since, there is no history maintained no
        alerts situation happens. In the  Collect mode,  measurement data is recorded but no alerts are generated when
        thresholds exceed. In the Alert mode, the measurement data is not only collected but alerts are generated when
        thresholds for any of the metrics is exceeded.
        
        Use cases:
        The caller of the operation may want to check the monitoring mode and change it later depending on its current
        value. For example, the user may want to switch off the notifications or alerts if he / she finds them enabled
        and set the system to Collect mode.
        """
        return cls.execute_soa_method(
            method_name='getTcServerMonitoringMode',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugMonitor',
            params={},
            response_cls=str,
        )

    @classmethod
    def clearAllHistory(cls) -> bool:
        """
        The Teamcenter Server Health Monitoring System internally stores data pertinent to the performance metrics such
        as metric measurements and notifications issued by the Monitoring System. this operation deletes this data for
        every metric which is being monitored by the system.
        """
        return cls.execute_soa_method(
            method_name='clearAllHistory',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugMonitor',
            params={},
            response_cls=bool,
        )

    @classmethod
    def clearHistory(cls, metricIds: List[str]) -> bool:
        """
        The Teamcenter Server Health Monitoring System internally stores data pertinent to the performance metrics such
        as metric measurements and notifications issued by the Monitoring System. This operation deletes data for the
        selected metrics.
        """
        return cls.execute_soa_method(
            method_name='clearHistory',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugMonitor',
            params={'metricIds': metricIds},
            response_cls=bool,
        )

    @classmethod
    def getValidMetrics(cls) -> ValidMetrics:
        """
        The Teamcenter Server Health Monitoring System internally maintains a list of metrics for which it can monitor
        performance data. This operation retrieves a list of metric IDs corresponding to these metrics.
        """
        return cls.execute_soa_method(
            method_name='getValidMetrics',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugMonitor',
            params={},
            response_cls=ValidMetrics,
        )

    @classmethod
    def reloadConfiguration(cls) -> bool:
        """
        This operation refreshes the configuration information in the Teamcenter Server Health Monitoring System by
        fresh parsing of serverMonitorConfig.xml file in TC_DATA.
        
        Exceptions:
        >If the file containing configuration information for the Teamcenter Server Health Monitoring
        system(serverMonitorConfig.xml file in TC_DATA folder) is corrupt, it throws exception.
        """
        return cls.execute_soa_method(
            method_name='reloadConfiguration',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugMonitor',
            params={},
            response_cls=bool,
        )

    @classmethod
    def setMetricConfig(cls, configs: MetricConfigMap) -> bool:
        """
        This operation sets the Teamcenter  Server Health Monitoring system's metric configuration.
        """
        return cls.execute_soa_method(
            method_name='setMetricConfig',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugMonitor',
            params={'configs': configs},
            response_cls=bool,
        )

    @classmethod
    def setTcServerMonitoringMode(cls, tcServerMonMode: str) -> bool:
        """
        The Teamcenter Server Monitoring System can operate in three different monitoring modes Off, Collect or Alert.
        This operation sets the current mode of operation. When in Off mode, the monitoring system does not record any
        monitoring data for the performance metrics. Since, there is no history maintained no alerts are generated. In
        the Collect mode,  measurement data is recorded but no alerts are generated even if thresholds are exceeded. In
        the Alert mode, the measurement data is not only collected but alerts are generated when threshold  for any of
        the metrics is exceeded. If an unsupported mode of monitoring is specified, the system is set to Off mode.
        """
        return cls.execute_soa_method(
            method_name='setTcServerMonitoringMode',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugMonitor',
            params={'tcServerMonMode': tcServerMonMode},
            response_cls=bool,
        )

    @classmethod
    def getAlertInformation(cls, metricIds: List[str]) -> AlertEventData:
        """
        When the measurement values show a deviation from the expected behavior of the Teamcenter Server, alerts are
        triggered in the Teamcenter Server Health Monitoring System if they are enabled. For every metric Id there is a
        threshold set which defines the expected behavior. When exceeded, it causes the alerts to be generated and
        relevant data is posted in some in-memory data structure. This operation allows the developer to fetch this
        alert data for the desired metrics.
        
        Use cases:
        The caller of this service operation may want to retrieve detailed information pertaining to generated alerts
        like the set of value(s) that caused the alerts, comparison between the threshold and the set of value(s) that
        caused the alert to occur etc. He/ she can use this operation for retrieving it.
        """
        return cls.execute_soa_method(
            method_name='getAlertInformation',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugMonitor',
            params={'metricIds': metricIds},
            response_cls=AlertEventData,
        )

    @classmethod
    def getMetricMetaData(cls, metricIds: List[str]) -> MetricMetaData:
        """
        This operation retrieves the Meta data for desired metrics.. The Meta data is the information that describes
        the characteristics of the metrics that are being monitored by the Teamcenter Server Health Monitoring System.
        If user passes invalid metricIds on the input, they are simply ignored.
        
        Use cases:
        The user may want to know about the characteristics of various metrics before fetching their actual measurement
        values in order to interpret the information correctly. For example units of measurement for a metric may help
        in knowing if the measured value for a time based metric is seconds or milliseconds.
        """
        return cls.execute_soa_method(
            method_name='getMetricMetaData',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugMonitor',
            params={'metricIds': metricIds},
            response_cls=MetricMetaData,
        )

    @classmethod
    def getOperationalHealthData(cls, metricAttributes: List[MetricAttributes]) -> OperationalHealthData:
        """
        This operation retrieves the measurement information for the desired performance metrics. The data is further
        restricted to only those metrics which were enabled for data collection in the system in the past. If there is,
        no previous measurement data collected for a particular metric id, an empty collection is returned for that
        metric. Some of the valid metric IDs are - POMRetries, Deadlocks, DBConnectionLosses, OmAllocations,
        OsBsmUndoPool and PomLocks. The entire list of valid metric IDs can be found in serverMonitorConfig.xml in
        TC_DATA folder. All invalid metric IDs are ignored.
        
        Use cases:
        User can fetch the measurement information based on performance metric IDs (unique identifiers for metrics) and
        the time interval. In order to interpret the measurement information correctly, user may want to call the
        getMetricMetaData operation prior to this operation. It would give information about the characteristics of
        measurements such as the units of measurement.
        """
        return cls.execute_soa_method(
            method_name='getOperationalHealthData',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='DebugMonitor',
            params={'metricAttributes': metricAttributes},
            response_cls=OperationalHealthData,
        )


class PerformanceMonitorService(TcService):

    @classmethod
    def clearPerformanceInformation(cls) -> ServiceData:
        """
        This operation clears the stored performance and resource utilization data on the server and frees any memory
        allocated for such data.
        """
        return cls.execute_soa_method(
            method_name='clearPerformanceInformation',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='PerformanceMonitor',
            params={},
            response_cls=ServiceData,
        )

    @classmethod
    def monitorPerformance(cls, modes: str) -> ServiceData:
        """
        This operations sets performance parameter collection mode. The modes argument can be set to the following
        values:
        - Off    Turn off all instrumentation.
        - SoaOnly    All stored performance data is returned to the caller via the  'getPerformanceInformation' service
        operation call.
        - ServiceDataOnly    All stored performance data is returned to the caller on each service operation calls via
        the 'Fnd0Profiler'  object added to the 'ServiceData' created list.
        - Both    All stored performance data is returned to the call on the new service operation call and any service
        operations returning 'ServiceData'.
        
        
        If the 'modes' value is an invalid mode then it will be discarded and the profiling mode will be set to its
        default value Off.
        """
        return cls.execute_soa_method(
            method_name='monitorPerformance',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='PerformanceMonitor',
            params={'modes': modes},
            response_cls=ServiceData,
        )

    @classmethod
    def getPerformanceInformation(cls, clear: bool) -> PerformanceInfoResponse:
        """
        This operation fetches the performance parameters from the Teamcenter server. If the clear flag is set the
        stored performance data list is cleared and memory is freed, otherwise the performance data is retained and
        used for subsequent calls.
        """
        return cls.execute_soa_method(
            method_name='getPerformanceInformation',
            library='Internal-DebugMonitor',
            service_date='2011_06',
            service_name='PerformanceMonitor',
            params={'clear': clear},
            response_cls=PerformanceInfoResponse,
        )
