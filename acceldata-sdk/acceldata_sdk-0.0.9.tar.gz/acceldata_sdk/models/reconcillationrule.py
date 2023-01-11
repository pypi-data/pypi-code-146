from enum import Enum, auto
from dataclasses import dataclass, asdict
from typing import List

from acceldata_sdk.models.ruleExecutionResult import RuleExecutionResult, RuleItemResult, RuleExecutionSummary, RuleResult
from acceldata_sdk.models.ruleExecutionResult import ExecutorConfig
from acceldata_sdk.models.rule import ShortSegment, Label, BackingAsset, RuleThresholdLevel, RuleTag, PolicyGroup, RuleResource, RuleExecution
from acceldata_sdk.constants import FailureStrategy, PolicyType


class ReconRuleExecutionSummary(RuleExecutionSummary):
    def __init__(self, ruleId, executionMode, executionStatus, resultStatus, startedAt, executionType,
                 isProtectedResource, thresholdLevel, ruleVersion, id=None, ruleName=None, ruleType=None,
                 lastMarker=None, leftLastMarker=None, rightLastMarker=None, executionError=None, finishedAt=None,
                 resetPoint=None, persistencePath=None, resultPersistencePath=None, executorConfig=None,
                 markerConfig=None, leftMarkerConfig=None, rightMarkerConfig=None, dataPersistenceEnabled=None,
                 *args, **kwargs):
        super().__init__(ruleId, executionMode, executionStatus, resultStatus, startedAt,executionType, thresholdLevel,
                         ruleVersion, id, ruleName, ruleType, lastMarker, leftLastMarker, rightLastMarker,
                         executionError, finishedAt, resetPoint, persistencePath, resultPersistencePath, executorConfig,
                         markerConfig, leftMarkerConfig, rightMarkerConfig, dataPersistenceEnabled, isProtectedResource)

    def __repr__(self):
        return f"ReconRuleExecutionSummary({self.__dict__})"


class ReconcillationRuleExecutionResult(RuleExecutionResult):
    def __init__(self, status, description=None, successCount=None, failureCount=None, leftRows=None, rightRows=None,
                 qualityScore=None, *args, **kwargs):
        super().__init__(status, description, successCount, failureCount, qualityScore)
        self.leftRows = leftRows
        self.rightRows = rightRows

    def __repr__(self):
        return f"ReconcillationRuleExecutionResult({self.__dict__})"


class MappingOperation(Enum):
    EQ = auto()
    NOT_EQ = auto()
    GTE = auto()
    GT = auto()
    LTE = auto()
    LT = auto()


class ColumnMapping:
    def __init__(self, leftColumnName, operation, rightColumnName, useForJoining, isJoinColumnUsedForMeasure,
                 ignoreNullValues, weightage, ruleVersion,isWarning, businessExplanation=None, id=None,
                 reconciliationRuleId=None, deletedAt=None, labels=None, *args, **kwargs):
        self.id = id
        self.leftColumnName = leftColumnName
        if isinstance(operation, dict):
            self.operation = MappingOperation(**operation)
        else:
            self.operation = operation
        self.rightColumnName = rightColumnName
        self.useForJoining = useForJoining
        self.isJoinColumnUsedForMeasure = isJoinColumnUsedForMeasure
        self.ignoreNullValues = ignoreNullValues
        self.weightage = weightage
        self.ruleVersion = ruleVersion
        self.isWarning = isWarning
        self.businessExplanation = businessExplanation
        self.reconciliationRuleId = reconciliationRuleId
        self.deletedAt = deletedAt
        self.labels = list()
        for obj in labels:
            if isinstance(obj, dict):
                self.labels.append(Label(**obj))
            else:
                self.labels.append(obj)

    def __repr__(self):
        return f"ColumnMapping({self.__dict__})"


class ReconcillationRuleItemResult(RuleItemResult):
    def __init__(self, id, ruleItemId, threshold, weightage, isRowMatchMeasure, isWarning, columnMapping=None,
                 resultPercent=None, success=None, error=None, *args, **kwargs):
        super().__init__(id, ruleItemId, threshold, weightage, isWarning, resultPercent, success, error)
        self.isRowMatchMeasure = isRowMatchMeasure
        if isinstance(columnMapping, dict):
            self.columnMapping = ColumnMapping(**columnMapping)
        else:
            self.columnMapping = columnMapping

    def __repr__(self):
        return f"ReconcillationRuleItemResult({self.__dict__})"


class ReconcillationExecutionResult(RuleResult):
    def __init__(self, execution, items, meta=None, result=None, *args, **kwargs):
        if isinstance(execution, dict):
            self.execution = ReconRuleExecutionSummary(**execution)
        else:
            self.execution = execution
        if isinstance(result, dict):
            self.result = ReconcillationRuleExecutionResult(**result)
        else:
            self.result = result
        self.items = list()
        for obj in items:
            if isinstance(obj, dict):
                self.items.append(ReconcillationRuleItemResult(**obj))
            else:
                self.items.append(obj)
        self.meta = meta
        self.executionId = self.execution.id

    def __repr__(self):
        return f"ReconcillationExecutionResult({self.__dict__})"


class ReconciliationMeasurementType(Enum):
    EQUALITY = 'EQUALITY'
    COUNT = 'COUNT'
    PROFILE_EQUALITY = 'PROFILE_EQUALITY'
    HASHED_EQUALITY = 'HASHED_EQUALITY'
    TIMELINESS = 'TIMELINESS'
    CUSTOM = 'CUSTOM'


@dataclass
class Item:
    id = None
    ruleId = None
    measurementType = None
    executionOrder = None
    version = None

    def __init__(self,
                 id=None,
                 ruleId=None,
                 measurementType = None,
                 executionOrder = None,
                 version = None, *args, **kwargs
                 ):
        self.ruleId = ruleId
        self.id = id
        self.executionOrder = executionOrder
        self.version = version
        if isinstance(measurementType, dict):
            self.measurementType = ReconciliationMeasurementType(**measurementType)
        else:
            self.measurementType = measurementType


class ReconciliationRuleDetails:
    def __init__(self, ruleId, leftBackingAssetId, rightBackingAssetId, columnMappings, timeSecondsOffset,
                 items, isSegmented, segments, id=None, *args, **kwargs):
        self.id = id
        self.ruleId = ruleId
        self.leftBackingAssetId = leftBackingAssetId
        self.rightBackingAssetId = rightBackingAssetId
        self.timeSecondsOffset = timeSecondsOffset
        self.items = list()
        for obj in items:
            if isinstance(obj, dict):
                self.items.append(Item(**obj))
            else:
                self.items.append(obj)
        self.isSegmented = isSegmented
        self.segments = list()
        if segments is not None:
            for obj in segments:
                if isinstance(obj, dict):
                    self.segments.append(ShortSegment(**obj))
                else:
                    self.segments.append(obj)
        self.columnMappings = list()
        if columnMappings is not None:
            for obj in columnMappings:
                if isinstance(obj, dict):
                    self.columnMappings.append(ColumnMapping(**obj))
                else:
                    self.columnMappings.append(obj)

    def __repr__(self):
        return f"ReconciliationRuleDetails({self.__dict__})"


class ChannelType(Enum):
    JIRA = 'JIRA'
    EMAIL = 'EMAIL'
    SLACK = 'SLACK'
    HANGOUT = 'HANGOUT'
    WEBHOOK = 'WEBHOOK'


class NotifyOn(Enum):
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    SUCCESS = 'SUCCESS'
    ALL = 'ALL'


@dataclass
class NotificationPayload:
    configuredList: List
    notifyOn: List[NotifyOn]
    tags: List[str] = None


class ReconciliationRule:
    def __init__(self, name, description, type, enabled, schedule,scheduled,notificationChannels, leftBackingAsset,
                 rightBackingAsset,timeSecondsOffset, createdAt, updatedAt, thresholdLevel, archived, archivalReason,
                 tenantId, createdBy, lastUpdatedBy, tags, version, executorConfig, labels, isProtectedResource,
                 policyGroups, id=None, *args, **kwargs):
        self.id = id
        self.name = name
        self.description = description
        self.type = type
        self.enabled = enabled
        self.schedule = schedule
        self.scheduled = scheduled
        self.notificationChannels = notificationChannels
        if isinstance(leftBackingAsset, dict):
            self.leftBackingAsset = BackingAsset(**leftBackingAsset)
        else:
            self.leftBackingAsset = leftBackingAsset
        if isinstance(rightBackingAsset, dict):
            self.rightBackingAsset = BackingAsset(**rightBackingAsset)
        else:
            self.rightBackingAsset = rightBackingAsset
        self.timeSecondsOffset = timeSecondsOffset
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        if isinstance(thresholdLevel, dict):
            self.thresholdLevel = RuleThresholdLevel(**thresholdLevel)
        else:
            self.thresholdLevel = thresholdLevel
        self.archived = archived
        self.archivalReason = archivalReason
        self.tenantId = tenantId
        self.createdBy = createdBy
        self.lastUpdatedBy = lastUpdatedBy

        self.tags = list()
        if tags is not None:
            for obj in tags:
                if isinstance(obj, dict):
                    self.tags.append(RuleTag(**obj))
                else:
                    self.tags.append(obj)
        self.version = version
        if isinstance(executorConfig, dict):
            self.executorConfig = ExecutorConfig(**executorConfig)
        else:
            self.executorConfig = executorConfig
        self.labels = list()
        if labels is not None:
            for obj in labels:
                if isinstance(obj, dict):
                    self.labels.append(Label(**obj))
                else:
                    self.labels.append(obj)
        self.isProtectedResource = isProtectedResource

        self.policyGroups = list()
        if policyGroups is not None:
            for obj in policyGroups:
                if isinstance(obj, dict):
                    self.policyGroups.append(PolicyGroup(**obj))
                else:
                    self.policyGroups.append(obj)

    def __repr__(self):
        return f"ReconciliationRule({self.__dict__})"


class ReconciliationRuleResource(RuleResource):
    def __init__(self, rule, details, client=None, *args, **kwargs):
        if isinstance(rule, dict):
            self.rule = ReconciliationRule(**rule)
        else:
            self.rule = rule
        if isinstance(details, dict):
            self.details = ReconciliationRuleDetails(**details)
        else:
            self.details = details
        self.client = client

    def execute(self, sync=True, incremental=False, failure_strategy: FailureStrategy = FailureStrategy.DoNotFail) -> RuleExecution:
        return self.client.execute_rule(PolicyType.RECONCILIATION, self.rule.id, sync, incremental, failure_strategy)

    def get_executions(self, page=0, size=25, sortBy='finishedAt:DESC'):
        return self.client.policy_executions(self.rule.id, PolicyType.RECONCILIATION, page, size, sortBy)

    def __repr__(self):
        return f"ReconciliationRuleResource({self.__dict__})"
