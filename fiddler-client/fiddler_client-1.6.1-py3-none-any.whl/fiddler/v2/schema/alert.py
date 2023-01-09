import enum
from typing import Any, Dict, List, Optional

from pydantic import Field, root_validator

from fiddler.v2.schema.base import BaseDataSchema


@enum.unique
class AlertType(str, enum.Enum):
    """Supported Alert types"""

    PERFORMANCE = 'performance'
    DATA_INTEGRITY = 'data_integrity'
    DATA_DRIFT = 'drift'
    SERVICE_METRICS = 'service_metrics'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}.{self.name}'


@enum.unique
class Metric(str, enum.Enum):
    """Supported metrics for Alerts."""

    # Drift metrics
    JSD = 'jsd'
    PSI = 'psi'

    ## Data Integrity Metrics
    MISSING_VALUE = 'missing_value'
    RANGE_VIOLATION = 'range_violation'
    TYPE_VIOLATION = 'type_violation'

    ## Performance metrics
    # Binary Classification
    ACCURACY = 'accuracy'
    RECALL = 'recall'
    FPR = 'fpr'
    PRECISION = 'precision'
    TPR = 'tpr'
    AUC = 'auc'
    F1_SCORE = 'f1_score'
    ECE = 'expected_callibration_error'

    # Regression
    R2 = 'r2'
    MSE = 'mse'
    MAPE = 'mape'
    WMAPE = 'wmape'
    MAE = 'mae'

    # Multiclass Classification
    LOG_LOSS = 'log_loss'

    # Ranking
    MAP = 'map'
    MEAN_NDCG = 'mean_ndcg'

    ## Service Metrics
    TRAFFIC = 'Traffic'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}.{self.name}'


@enum.unique
class BinSize(enum.IntEnum):
    """Bin Size values Alerts can be set on"""

    ONE_HOUR = 3600000
    ONE_DAY = 86400000
    SEVEN_DAYS = 604800000

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}.{self.name}'

    @classmethod
    def keys(cls) -> List[str]:
        return list(cls.__members__.values())


@enum.unique
class ComparePeriod(enum.IntEnum):
    """Time period values for comparison with previous window"""

    ONE_DAY = 86400000
    SEVEN_DAYS = 604800000
    ONE_MONTH = 2629743000
    THREE_MONTHS = 7776000000

    @classmethod
    def keys(cls) -> List[str]:
        return list(cls.__members__.values())

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}.{self.name}'


@enum.unique
class CompareTo(str, enum.Enum):
    """Comparison with Absolute(raw_value) or Relative(time_period)"""

    TIME_PERIOD = 'time_period'
    RAW_VALUE = 'raw_value'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}.{self.name}'


@enum.unique
class AlertCondition(str, enum.Enum):
    GREATER = 'greater'
    LESSER = 'lesser'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}.{self.name}'


@enum.unique
class Priority(str, enum.Enum):
    HIGH = 'HIGH'
    MEDIUM = 'MEDIUM'
    LOW = 'LOW'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}.{self.name}'


class AlertRulePayload(BaseDataSchema):
    organization_name: str
    project_name: str
    model_name: str
    name: str
    alert_type: AlertType
    metric: Metric
    feature_name: Optional[str]
    priority: Priority
    compare_to: CompareTo
    baseline_name: Optional[str]
    compare_period: Optional[ComparePeriod]
    warning_threshold: Optional[float]
    critical_threshold: float
    condition: AlertCondition
    time_bucket: BinSize
    notifications: Optional[Dict[str, Dict[str, Any]]]


class AlertRule(BaseDataSchema):
    alert_rule_uuid: str = Field(alias='uuid')
    organization_name: str
    project_id: str = Field(alias='project_name')
    model_id: str = Field(alias='model_name')
    name: Optional[str]
    alert_type: AlertType
    metric: Metric
    column: str = Field(alias='feature_name')
    baseline_id: Optional[str] = Field(alias='baseline_name')
    priority: Priority
    compare_to: CompareTo
    compare_period: Optional[ComparePeriod]
    warning_threshold: Optional[float]
    critical_threshold: float
    condition: AlertCondition
    bin_size: BinSize = Field(alias='time_bucket')

    @root_validator(pre=True)
    def set_compare_period(cls, values) -> Optional[ComparePeriod]:

        if values['compare_period'] == 0:
            values['compare_period'] = None
        return values


class TriggeredAlerts(BaseDataSchema):
    id: int
    triggered_alert_id: str = Field(alias='uuid')
    alert_rule_uuid: str = Field(alias='alert_config_uuid')
    alert_run_start_time: int
    alert_time_bucket: int
    alert_value: float
    baseline_time_bucket: Optional[int]
    baseline_value: Optional[float]
    is_alert: bool
    severity: Optional[str]
    failure_reason: str
    message: str
