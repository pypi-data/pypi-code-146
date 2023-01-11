from __future__ import annotations

from enum import Enum
from typing import Dict, List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MeasuredValue(TcBaseObj):
    """
    The measurement value for a metric and some associated information.
    
    :var dType: The data type of the value.
    :var value: Measurement value in a measurement unit relevant to the metric.
    """
    dType: str = ''
    value: str = ''


@dataclass
class MeasurementInfo(TcBaseObj):
    """
    Measurement data for each requested performance metric.
    
    :var timeStamp: The time at which the measurement was recorded.
    :var measvals: The measurement value and some associated information.
    :var additionalInfo: A place holder for data recorded in addition to measurement value. For example, the name of
    operation may be recorded as additional information with the SqlTotalTime metric.
    """
    timeStamp: datetime = None
    measvals: MeasuredValue = None
    additionalInfo: List[str] = ()


@dataclass
class MetaData(TcBaseObj):
    """
    It represents the vector containing list of meta data for various metrics. A collection of characteristics or
    properties of metrics.
    
    :var metricId: A unique identifier that can identify a particular metric from a list of performance metrics.
    :var dType: The data type for the measured value. The valid values are MetricDataType_Integer and
    MetricDataType_Double.
    :var displayName: User friendly name for display on UI.
    :var metricMode: The metric monitoring mode. Possible values are - Off, Collect or Alert.
    :var unitOfMeasurement: The measurement unit for the values being measured. For a time based metric it could be
    "seconds".
    :var maxEntriesToKeep: The total number of measurement values to be kept in history for a particular metric. If the
    numbers of values exceed this value the less important measured value is deleted first.
    :var metricThreshold: Collected values exceeding this threshold will result in the Teamcenter Server Health
    Monitoring System generating an Alert for this metric.
    :var monStartTime: The time at which the monitoring is started for the particular metric.
    :var metricType: Metrics can be classified based on the method of monitoring. 'metricType' denotes which method is
    adopted for monitoring.
    """
    metricId: str = ''
    dType: str = ''
    displayName: str = ''
    metricMode: MetricMode = None
    unitOfMeasurement: str = ''
    maxEntriesToKeep: int = 0
    metricThreshold: Threshold = None
    monStartTime: datetime = None
    metricType: MetricType = None


@dataclass
class MetricAttributes(TcBaseObj):
    """
    A performance metric identifier and the time interval for which the data should be collected.
    
    :var metricId: Uniquely identifies a particular metric from a list of performance metrics. The entire list of valid
    metric IDs can be found in serverMonitorConfig.xml in TC_DATA folder.
    :var timeInterval: The time duration(seconds) for which measurements will be collected. A value of 30 would collect
    the last 30 seconds of measurement data. A value of 0 results in the full measurement history being returned.
    """
    metricId: str = ''
    timeInterval: int = 0


@dataclass
class MetricConfig(TcBaseObj):
    """
    It holds the characteristics relevant to a metric. These include the monitoring mode of metric, the maximum number
    of measurements to be kept for the metric, the threshold value and the threshold period.
    
    :var mode: It signifies the mode of monitoring i. e. Off, Collect or Alert.
    :var numMaxEntriesToKeep: Maximum number of measurements to be stored for this metric.
    :var thresholdValue: The value exceeding which the Teamcenter Health Monitoring System will generate alert if it is
    in Alert mode.
    :var thresholdPeriod: The period during which the threshold value needs to be monitored for generating alerts.
    """
    mode: MetricMode = None
    numMaxEntriesToKeep: int = 0
    thresholdValue: str = ''
    thresholdPeriod: int = 0


@dataclass
class MetricMetaData(TcBaseObj):
    """
    It represents the vector containing list of meta data for various metrics. A collection of characteristics or
    properties of metrics.
    
    :var metaData: A collection of characteristics or properties of metrics.
    """
    metaData: List[MetaData] = ()


@dataclass
class OperationalHealthData(TcBaseObj):
    """
    Measurement data for each requested performance metric.
    
    :var measurementInfoMap: A map which holds the list of measurements monitored associated with the metric. A map of
    metric IDs and measurement data ( string / EventStatistics ).
    """
    measurementInfoMap: MeasurementInfoMap = None


@dataclass
class Threshold(TcBaseObj):
    """
    It holds the threshold information of Teamcenter Server Health metrics.  When a threshold is exceeded for a metric
    the Teamcenter Health Monitoring System may generate alerts.
    
    :var thresholdValue: The boundary value for which the Teamcenter Server Health Monitoring System may generate
    alerts for this metric.
    :var hasPeriod: A true value signifies that the threshold has a time period associated with it.
    :var thresholdPeriod: The time period (seconds) associated with threshold. It is meaningful for those metrics which
    also consider time period for monitoring like CountableMetricWithTimePeriod.
    """
    thresholdValue: str = ''
    hasPeriod: bool = False
    thresholdPeriod: int = 0


@dataclass
class ValidMetrics(TcBaseObj):
    """
    A list of valid metric IDs.
    
    :var metricIds: List of all metricIds.
    """
    metricIds: List[str] = ()


@dataclass
class AlertData(TcBaseObj):
    """
    This holds the alert data associated with the metric. The information includes the subject of generated alert, the
    summary of the alert and event data causing the alert.
    
    :var subject: Subject line that contains information regarding which metric generated alert etc.
    :var summary: A summary containing information about the set threshold and the value that exceeded threshold.
    :var eventData: Measured event values for the metric.
    """
    subject: str = ''
    summary: str = ''
    eventData: List[EventData] = ()


@dataclass
class AlertEventData(TcBaseObj):
    """
    Measurement data for each requested metric.
    
    :var alertData: A map of metric IDs and alert data ( string / AlertData ).
    """
    alertData: AlertDataMap = None


@dataclass
class EventData(TcBaseObj):
    """
    This holds the information about one event which includes date and time, value of the measurement, and vector of
    additional information. Measured event values for the metric.
    
    :var time: The time at which the measurement was taken.
    :var value: Measurement value recorded.
    :var additionalInfo: A place holder for data recorded in addition to measurement value. For example, the name of
    operation may be recorded as additional information with the SqlTotalTime metric
    """
    time: str = ''
    value: str = ''
    additionalInfo: List[str] = ()


@dataclass
class EventStatistics(TcBaseObj):
    """
    It holds the event data associated with the given metrics for the specified time interval. The information includes
    a list of measurements and event statistics.
    
    :var measInfo: The measurement statistics for the given time period.
    :var eventStats: Some statistics based on the type of metric. 
    - For a CountableMetric or CountableMetricWithTimePeriod this would be number of events that have taken place since
    monitoring started. 
    - For VariableMetric or AvgVariableWithTimePeriod  it would be average value of measurements recorded so far. 
    - In case of MaxVariableWithTimePeriod, it would be the maximum measurement value recorded in the measurement
    history of that metric.
    -  For DetailedMetric, it would be average time taken per SQL call for an operation.
    
    """
    measInfo: List[MeasurementInfo] = ()
    eventStats: str = ''


class MetricMode(Enum):
    """
    A metric can operate in any of the three different monitoring modes Off, Collect or Alert. This method retrieves
    the current mode of operation. When in Off mode, the monitoring system does not record any monitoring data for the
    performance metrics. Since, there is no history maintained no alerts situation happens. In the Collect mode, 
    measurement data is recorded but no alerts are generated when thresholds exceed. In the Alert mode, the measurement
    data is not only collected but alerts are generated when thresholds for any of the metrics is exceeded
    """
    Off = 'Off'
    Collect = 'Collect'
    Alert = 'Alert'


class MetricType(Enum):
    """
    Type of the metric.
    - CountableMetric A metric for which the number or count of events is of importance and is considered for alert
    generation. If the threshold value is 'n' it means the alert will be generated if event has occurred 'n' number of 
        times or more since its monitoring started.
    - CountableMetricWithTimePeriod     Same as CountableMetric, but the count is over an elapsed period of time.
    - VariableMetric     For a VariableMetric, the measured value is of significance and an alert will be triggered if
    the measured value for a metric equals or exceeds the threshold value. An alert is triggered when a measured value
    is equal to or exceeds the threshold.
    - AvgVariableWithTimePeriod    An Alert is triggered when the running average of the measured value is equal to or
    exceeds the threshold.
    - MaxVariableWithTimePeriod    An alert is triggered when the measured value is equal to or exceeds the threshold
    value over a given time period.    
    - DetailedMetric    This is a special type of metric specific to SQL statistics which does not result in any alert
    generation by Teamcenter Server Health Monitoring System. The average time taken per SQL call is of significance in
    its context.
    
    """
    CountableMetric = 'CountableMetric'
    CountableMetricWithTimePeriod = 'CountableMetricWithTimePeriod'
    VariableMetric = 'VariableMetric'
    AvgVariableWithTimePeriod = 'AvgVariableWithTimePeriod'
    MaxVariableWithTimePeriod = 'MaxVariableWithTimePeriod'
    DetailedMetric = 'DetailedMetric'


"""
A Map which holds the list of measurements monitored associated with the metric. A map of metric IDs and measurement data ( string / EventStatistics ).
"""
MeasurementInfoMap = Dict[str, List[EventStatistics]]


"""
A Map that holds metric Configuration information. A map of metric IDs and metric configuration data ( string / MetricConfig ).
"""
MetricConfigMap = Dict[str, MetricConfig]


"""
A Map which holds the alert data associated with the metric. A map of metric IDs and alert data ( string / AlertData ).
"""
AlertDataMap = Dict[str, AlertData]
