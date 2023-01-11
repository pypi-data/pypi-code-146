from typing import Dict
from txp.common.reports.section import ReportSection
from txp.common.reports.mock_double_line import MockDoubleLine
from txp.common.reports.forecasting import *
from txp.common.reports.anomaly_detection import *
from txp.common.reports.transitions import *
from txp.common.reports.distribution import *
from txp.common.reports.states_sunburst import *
from txp.common.reports.transitions_lines import *


SECTIONS_REGISTRY: Dict[str, ReportSection] = {
    MockDoubleLine.__name__: MockDoubleLine,
    StatesForecasting.__name__: StatesForecasting,
    EventsForecasting.__name__: EventsForecasting,
    AnomalyDetectionStates.__name__: AnomalyDetectionStates,
    AnomalyDetectionEvents.__name__: AnomalyDetectionEvents,
    RawDataForecasting.__name__: RawDataForecasting,
    AnomalyDetectionRawData.__name__: AnomalyDetectionRawData,
    StatesTransitions.__name__: StatesTransitions,
    EventsTransitions.__name__: EventsTransitions,
    StatesDistribution.__name__: StatesDistribution,
    EventsDistribution.__name__: EventsDistribution,
    StatesSunburst.__name__: StatesSunburst,
    StatesTransitionsLines.__name__: StatesTransitionsLines,
    EventsTransitionsLines.__name__: EventsTransitionsLines
}
