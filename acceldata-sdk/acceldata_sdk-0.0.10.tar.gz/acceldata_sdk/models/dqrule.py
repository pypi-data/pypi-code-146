from acceldata_sdk.models.ruleExecutionResult import RuleExecutionResult, RuleItemResult, RuleResult, RuleExecutionSummary
from enum import Enum
from dataclasses import dataclass
from typing import List
from acceldata_sdk.models.rule import ShortSegment, Label, BackingAsset, RuleThresholdLevel, RuleTag, PolicyGroup, RuleResource, RuleExecution

from acceldata_sdk.models.ruleExecutionResult import ExecutorConfig
from acceldata_sdk.constants import FailureStrategy, PolicyType


class RootCauseAnalysis:
    def __init__(self, key, bad, good, badFraction, goodFraction, *args, **kwargs):
        self.key = key
        self.bad = bad
        self.good = good
        self.badFraction = badFraction
        self.goodFraction = goodFraction

    def __repr__(self):
        return f"RootCauseAnalysis({self.__dict__})"


class DataQualityRuleExecutionResult(RuleExecutionResult):
    def __init__(self, status, description=None, successCount=None, failureCount=None, rows=None, failedRows=None,
                 qualityScore=None, rca=None, *args, **kwargs):
        super().__init__(status, description, successCount, failureCount, qualityScore)
        self.failedRows = failedRows
        self.rows = rows
        if isinstance(rca, dict):
            self.rca = RootCauseAnalysis(**rca)
        else:
            self.rca = rca
    
    def __repr__(self):
        return f"DataQualityRuleExecutionResult({self.__dict__})"


class DataQualityRuleItemResult(RuleItemResult):
    def __init__(self, id, ruleItemId, threshold, weightage, isWarning, resultPercent=None, businessItemId=None,
                 success=None, error=None, *args, **kwargs):
        super().__init__(id, ruleItemId, threshold, weightage, isWarning, resultPercent, success, error)
        self.businessItemId = businessItemId

    def __repr__(self):
        return f"DataQualityRuleItemResult({self.__dict__})"


class DataQualityExecutionResult(RuleResult):
    def __init__(self, execution, items, meta=None, result=None, *args, **kwargs):
        if isinstance(execution, dict):
            self.execution = RuleExecutionSummary(**execution)
        else:
            self.execution = execution
        if isinstance(result, dict):
            self.result = DataQualityRuleExecutionResult(**result)
        else:
            self.result = result
        self.items = list()
        for obj in items:
            if isinstance(obj, dict):
                self.items.append(DataQualityRuleItemResult(**obj))
            else:
                self.items.append(obj)
        self.meta = meta
        self.executionId = self.execution.id

    def __repr__(self):
        return f"DataQualityExecutionResult({self.__dict__})"


class DataQualityMeasurementType(Enum):
    MISSING_VALUES = 'MISSING_VALUES'
    DATATYPE_MATCH = 'DATATYPE_MATCH'
    REGEX_MATCH = 'REGEX_MATCH'
    VALUES_IN_LIST = 'VALUES_IN_LIST'
    DISTINCTNESS_CHECK = 'DISTINCTNESS_CHECK'
    DUPLICATE_ROWS_CHECK = 'DUPLICATE_ROWS_CHECK'
    PRECISION_SCALE_CHECK = 'PRECISION_SCALE_CHECK'
    BUSINESS_MEASURE = 'BUSINESS_MEASURE'
    TAG_MATCH = 'TAG_MATCH'
    RANGE_MATCH = 'RANGE_MATCH'
    SIZE_CHECK = 'SIZE_CHECK'
    CUSTOM = 'CUSTOM'
    UDF_PREDICATE = 'UDF_PREDICATE'


@dataclass
class Item:
    id = None
    ruleId = None
    measurementType = None
    executionOrder = None
    columnName = None
    value = None
    ruleExpression = None
    resultThreshold = None
    weightage = None
    ruleVersion = None
    businessExplanation = None
    labels = None
    isWarning = None

    def __init__(self,
                 id=None,
                 ruleId=None,
                 measurementType=None,
                 executionOrder=None,
                 columnName=None,
                 value=None,
                 ruleExpression=None,
                 resultThreshold=None,
                 weightage=None,
                 ruleVersion=None,
                 businessExplanation=None,
                 labels=None,
                 isWarning=None,
                 *args, **kwargs):
        self.ruleId = ruleId
        self.id = id
        if isinstance(measurementType, dict):
            self.measurementType = DataQualityMeasurementType(**measurementType)
        else:
            self.measurementType = measurementType
        self.executionOrder = executionOrder
        self.columnName = columnName
        self.value = value
        self.ruleExpression = ruleExpression
        self.resultThreshold = resultThreshold
        self.weightage = weightage
        self.ruleVersion = ruleVersion
        self.businessExplanation = businessExplanation
        self.labels = list()
        for obj in labels:
            if isinstance(obj, dict):
                self.labels.append(Label(**obj))
            else:
                self.labels.append(obj)
        self.isWarning = isWarning

    def __repr__(self):
        return f"Item({self.__dict__})"


class DataQualityRuleDetails:
    def __init__(self, ruleId, backingAssetId,
                 items, isSegmented, segments, id=None, *args, **kwargs):
        self.id = id
        self.ruleId = ruleId
        self.backingAssetId = backingAssetId
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

    def __repr__(self):
        return f"DataQualityRuleDetails({self.__dict__})"


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


class DataQualityRule:
    def __init__(self, name=None, description=None, type=None, enabled=None, schedule=None, scheduled=None,
                 notificationChannels=None, backingAssets=None, createdAt=None, updatedAt=None, thresholdLevel=None,
                 archived=None, archivalReason=None, tenantId=None, createdBy=None, lastUpdatedBy=None, tags=None,
                 segments=None, version=None, executorConfig=None, labels=None, isProtectedResource=None,
                 policyGroups=None, id=None, *args, **kwargs):
        self.id = id
        self.name = name
        self.description = description
        self.type = type
        self.enabled = enabled
        self.schedule = schedule
        self.scheduled = scheduled
        self.notificationChannels = notificationChannels
        self.backingAssets = list()
        if backingAssets is not None:
            for obj in backingAssets:
                if isinstance(obj, dict):
                    self.backingAssets.append(BackingAsset(**obj))
                else:
                    self.backingAssets.append(obj)
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
        self.segments = list()
        if segments is not None:
            for obj in segments:
                if isinstance(obj, dict):
                    self.segments.append(ShortSegment(**obj))
                else:
                    self.segments.append(obj)
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
        return f"DataQualityRule({self.__dict__})"


class DataQualityRuleResource(RuleResource):
    def __init__(self, rule, details, client=None, *args, **kwargs):
        if isinstance(rule, dict):
            self.rule = DataQualityRule(**rule)
        else:
            self.rule = rule
        if isinstance(details, dict):
            self.details = DataQualityRuleDetails(**details)
        else:
            self.details = details
        self.client = client

    def execute(self, sync=True, incremental=False, failure_strategy: FailureStrategy = FailureStrategy.DoNotFail) -> RuleExecution:
        return self.client.execute_rule(PolicyType.DATA_QUALITY, self.rule.id, sync, incremental, failure_strategy)

    def get_executions(self, page=0, size=25, sortBy='finishedAt:DESC'):
        return self.client.policy_executions(self.rule.id, PolicyType.DATA_QUALITY, page, size, sortBy)

    def __repr__(self):
        return f"DataQualityRuleResource({self.__dict__})"
