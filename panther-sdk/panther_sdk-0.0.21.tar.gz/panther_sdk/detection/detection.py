# Copyright (C) 2022 Panther Labs, Inc.
#
# The Panther SaaS is licensed under the terms of the Panther Enterprise Subscription
# Agreement available at https://panther.com/enterprise-subscription-agreement/.
# All intellectual property rights in and to the Panther SaaS, including any and all
# rights to access the Panther SaaS, are governed by the Panther Enterprise Subscription Agreement.

# coding=utf-8
# *** WARNING: generated file
import typing
import functools
import dataclasses

from panther_core import PantherEvent

"""
The detection module provides classes representing Panther detections: Rules, Policies, Scheduled Rules and more
"""

from .. import _utilities

__all__ = [
    "AnyFilter",
    "AnyUnitTest",
    "DynamicStringField",
    "DynamicStringFieldOverrides",
    "DynamicDestinations",
    "DynamicDestinationsOverrides",
    "AlertGrouping",
    "AlertGroupingOverrides",
    "PythonFilter",
    "PythonFilterOverrides",
    "UnitTestMock",
    "UnitTestMockOverrides",
    "JSONUnitTest",
    "JSONUnitTestOverrides",
    "Policy",
    "PolicyOverrides",
    "Rule",
    "RuleOverrides",
    "ScheduledRule",
    "ScheduledRuleOverrides",
    "SeverityLow",
    "SeverityInfo",
    "SeverityMedium",
    "SeverityHigh",
    "SeverityCritical",
    "ReportKeyMITRE",
]


SeverityLow = "LOW"
SeverityInfo = "INFO"
SeverityMedium = "MEDIUM"
SeverityHigh = "HIGH"
SeverityCritical = "CRITICAL"
ReportKeyMITRE = "MITRE ATT&CK"


class DefaultOverrides:
    pass


def overridable(cls: typing.Callable) -> typing.Callable:
    @functools.wraps(cls)
    def wrapper(
        *args: typing.Any,
        overrides: typing.Optional[
            typing.Union[
                "DynamicStringFieldOverrides",
                "DynamicDestinationsOverrides",
                "AlertGroupingOverrides",
                "PythonFilterOverrides",
                "UnitTestMockOverrides",
                "JSONUnitTestOverrides",
                "PolicyOverrides",
                "RuleOverrides",
                "ScheduledRuleOverrides",
                DefaultOverrides,
            ]
        ] = DefaultOverrides(),
        **kwargs: typing.Any,
    ) -> typing.Any:
        if overrides:  # overrides can be None
            for key, val in overrides.__dict__.items():
                kwargs[key] = val or kwargs.get(key)
        return cls(*args, **kwargs)

    return wrapper


@dataclasses.dataclass
class DynamicStringFieldOverrides:
    """Overrides dataclass for DynamicStringField. All arguments are marked optional.

    - fallback -- Fallback value in case the dynamic handler fails
    - func -- Dynamic handler
    """

    fallback: typing.Optional[str] = None

    func: typing.Optional[typing.Callable[[PantherEvent], str]] = None


@dataclasses.dataclass(frozen=True)
class DynamicStringField(_utilities.SDKNode):
    """Make a field dynamic based on the detection input

    - fallback -- Fallback value in case the dynamic handler fails (optional, default: "")
    - func -- Dynamic handler (optional, default: None)
    """

    # optional
    fallback: str = ""

    # optional
    func: typing.Optional[typing.Callable[[PantherEvent], str]] = None

    # internal private methods
    def _typename(self) -> str:
        return "DynamicStringField"

    def _output_key(self) -> str:
        return ""

    def _fields(self) -> typing.List[str]:
        return ["fallback", "func"]


@dataclasses.dataclass
class DynamicDestinationsOverrides:
    """Overrides dataclass for DynamicDestinations. All arguments are marked optional.

    - func -- Dynamic handler
    - fallback -- Fallback value in case the dynamic handler fails
    """

    func: typing.Optional[typing.Callable[[PantherEvent], typing.List[str]]] = None

    fallback: typing.Optional[typing.List[str]] = None


@dataclasses.dataclass(frozen=True)
class DynamicDestinations(_utilities.SDKNode):
    """Make destinations dynamic based on the detection input

    - func -- Dynamic handler (required)
    - fallback -- Fallback value in case the dynamic handler fails (optional, default: None)
    """

    # required
    func: typing.Callable[[PantherEvent], typing.List[str]]

    # optional
    fallback: typing.Optional[typing.List[str]] = None

    # internal private methods
    def _typename(self) -> str:
        return "DynamicDestinations"

    def _output_key(self) -> str:
        return ""

    def _fields(self) -> typing.List[str]:
        return ["func", "fallback"]


@dataclasses.dataclass
class AlertGroupingOverrides:
    """Overrides dataclass for AlertGrouping. All arguments are marked optional.

    - group_by -- Function to generate a key for grouping matches
    - period_minutes -- How long should matches be grouped into an alert after the first match
    """

    group_by: typing.Optional[typing.Callable[[PantherEvent], str]] = None

    period_minutes: typing.Optional[int] = None


@dataclasses.dataclass(frozen=True)
class AlertGrouping(_utilities.SDKNode):
    """Configuration for how an alert is grouped

    - group_by -- Function to generate a key for grouping matches (optional, default: None)
    - period_minutes -- How long should matches be grouped into an alert after the first match (optional, default: 15)
    """

    # optional
    group_by: typing.Optional[typing.Callable[[PantherEvent], str]] = None

    # optional
    period_minutes: int = 15

    # internal private methods
    def _typename(self) -> str:
        return "AlertGrouping"

    def _output_key(self) -> str:
        return ""

    def _fields(self) -> typing.List[str]:
        return ["group_by", "period_minutes"]


@dataclasses.dataclass
class PythonFilterOverrides:
    """Overrides dataclass for PythonFilter. All arguments are marked optional.

    - func -- Provide a function whose python source will be used as the filter definition
    """

    func: typing.Optional[typing.Callable[[PantherEvent], bool]] = None


@dataclasses.dataclass(frozen=True)
class PythonFilter(_utilities.SDKNode):
    """Create a filter by referencing a python function

    - func -- Provide a function whose python source will be used as the filter definition (required)
    """

    # required
    func: typing.Callable[[PantherEvent], bool]

    # internal private methods
    def _typename(self) -> str:
        return "PythonFilter"

    def _output_key(self) -> str:
        return ""

    def _fields(self) -> typing.List[str]:
        return ["func"]


@dataclasses.dataclass
class UnitTestMockOverrides:
    """Overrides dataclass for UnitTestMock. All arguments are marked optional.

    - name -- name of the object to mock
    - return_value -- string to assign as the return value for the mock
    """

    name: typing.Optional[str] = None

    return_value: typing.Optional[str] = None


@dataclasses.dataclass(frozen=True)
class UnitTestMock(_utilities.SDKNode):
    """Mock for a unit test

    - name -- name of the object to mock (required)
    - return_value -- string to assign as the return value for the mock (required)
    """

    # required
    name: str

    # required
    return_value: str

    # internal private methods
    def _typename(self) -> str:
        return "UnitTestMock"

    def _output_key(self) -> str:
        return ""

    def _fields(self) -> typing.List[str]:
        return ["name", "return_value"]


@dataclasses.dataclass
class JSONUnitTestOverrides:
    """Overrides dataclass for JSONUnitTest. All arguments are marked optional.

    - data -- json string
    - expect_match -- whether the data should match and trigger an alert
    - name -- name of the unit test
    - mocks -- list of mocks to use in the test
    """

    data: typing.Optional[str] = None

    expect_match: typing.Optional[bool] = None

    name: typing.Optional[str] = None

    mocks: typing.Optional[typing.List[UnitTestMock]] = None


@dataclasses.dataclass(frozen=True)
class JSONUnitTest(_utilities.SDKNode):
    """Unit test with json content

    - data -- json string (required)
    - expect_match -- whether the data should match and trigger an alert (required)
    - name -- name of the unit test (required)
    - mocks -- list of mocks to use in the test (optional, default: None)
    """

    # required
    data: str

    # required
    expect_match: bool

    # required
    name: str

    # optional
    mocks: typing.Optional[typing.List[UnitTestMock]] = None

    # internal private methods
    def _typename(self) -> str:
        return "JSONUnitTest"

    def _output_key(self) -> str:
        return ""

    def _fields(self) -> typing.List[str]:
        return ["data", "expect_match", "name", "mocks"]


@dataclasses.dataclass
class PolicyOverrides:
    """Overrides dataclass for Policy. All arguments are marked optional.

    - filters -- Define event filters for the policy
    - policy_id -- ID for the Policy
    - resource_types -- What resource types this policy will apply to
    - severity -- What severity alerts generated from this policy get assigned
    - alert_context -- Optional JSON to attach to alerts generated by this policy
    - alert_grouping -- Configuration for how an alert is grouped
    - alert_title -- Title to use in the alert
    - description -- Description for the policy
    - destinations -- Alert destinations for the policy
    - enabled -- Whether the policy is enabled or not
    - ignore_patterns -- Patterns of resource ids to ignore for the policy
    - name -- What name to display in the UI and alerts. The PolicyID will be displayed if this field is not set.
    - reference -- The reason this policy exists, often a link to documentation
    - reports -- A mapping of framework or report names to values this policy covers for that framework
    - runbook -- The actions to be carried out if this policy fails, often a link to documentation
    - tags -- Tags used to categorize this policy
    - unit_tests -- Unit tests for this policy
    """

    filters: typing.Optional[
        typing.Union[
            typing.Union[PythonFilter], typing.List[typing.Union[PythonFilter]]
        ]
    ] = None

    policy_id: typing.Optional[str] = None

    resource_types: typing.Optional[typing.Union[str, typing.List[str]]] = None

    severity: typing.Optional[typing.Union[str, DynamicStringField]] = None

    alert_context: typing.Optional[
        typing.Callable[[PantherEvent], typing.Dict[str, typing.Any]]
    ] = None

    alert_grouping: typing.Optional[AlertGrouping] = None

    alert_title: typing.Optional[typing.Callable[[PantherEvent], str]] = None

    description: typing.Optional[typing.Union[str, DynamicStringField]] = None

    destinations: typing.Optional[
        typing.Union[str, typing.List[str], DynamicDestinations]
    ] = None

    enabled: typing.Optional[bool] = None

    ignore_patterns: typing.Optional[typing.Union[str, typing.List[str]]] = None

    name: typing.Optional[str] = None

    reference: typing.Optional[typing.Union[str, DynamicStringField]] = None

    reports: typing.Optional[typing.Dict[str, typing.List[str]]] = None

    runbook: typing.Optional[typing.Union[str, DynamicStringField]] = None

    tags: typing.Optional[typing.Union[str, typing.List[str]]] = None

    unit_tests: typing.Optional[
        typing.Union[
            typing.Union[JSONUnitTest], typing.List[typing.Union[JSONUnitTest]]
        ]
    ] = None


@overridable
@dataclasses.dataclass(frozen=True)
class Policy(_utilities.SDKNode):
    """Define a Policy-type detection to execute against log data in your Panther instance

    - filters -- Define event filters for the policy (required)
    - policy_id -- ID for the Policy (required)
    - resource_types -- What resource types this policy will apply to (required)
    - severity -- What severity alerts generated from this policy get assigned (required)
    - alert_context -- Optional JSON to attach to alerts generated by this policy (optional, default: None)
    - alert_grouping -- Configuration for how an alert is grouped (optional, default: None)
    - alert_title -- Title to use in the alert (optional, default: None)
    - description -- Description for the policy (optional, default: "")
    - destinations -- Alert destinations for the policy (optional, default: None)
    - enabled -- Whether the policy is enabled or not (optional, default: True)
    - ignore_patterns -- Patterns of resource ids to ignore for the policy (optional, default: None)
    - name -- What name to display in the UI and alerts. The PolicyID will be displayed if this field is not set. (optional, default: "")
    - reference -- The reason this policy exists, often a link to documentation (optional, default: "")
    - reports -- A mapping of framework or report names to values this policy covers for that framework (optional, default: None)
    - runbook -- The actions to be carried out if this policy fails, often a link to documentation (optional, default: "")
    - tags -- Tags used to categorize this policy (optional, default: None)
    - unit_tests -- Unit tests for this policy (optional, default: None)
    """

    # required
    filters: typing.Union[
        typing.Union[PythonFilter], typing.List[typing.Union[PythonFilter]]
    ]

    # required
    policy_id: str

    # required
    resource_types: typing.Union[str, typing.List[str]]

    # required
    severity: typing.Union[str, DynamicStringField]

    # optional
    alert_context: typing.Optional[
        typing.Callable[[PantherEvent], typing.Dict[str, typing.Any]]
    ] = None

    # optional
    alert_grouping: typing.Optional[AlertGrouping] = None

    # optional
    alert_title: typing.Optional[typing.Callable[[PantherEvent], str]] = None

    # optional
    description: typing.Optional[typing.Union[str, DynamicStringField]] = ""

    # optional
    destinations: typing.Optional[
        typing.Union[str, typing.List[str], DynamicDestinations]
    ] = None

    # optional
    enabled: bool = True

    # optional
    ignore_patterns: typing.Optional[typing.Union[str, typing.List[str]]] = None

    # optional
    name: typing.Optional[str] = ""

    # optional
    reference: typing.Optional[typing.Union[str, DynamicStringField]] = ""

    # optional
    reports: typing.Optional[typing.Dict[str, typing.List[str]]] = None

    # optional
    runbook: typing.Optional[typing.Union[str, DynamicStringField]] = ""

    # optional
    tags: typing.Optional[typing.Union[str, typing.List[str]]] = None

    # optional
    unit_tests: typing.Optional[
        typing.Union[
            typing.Union[JSONUnitTest], typing.List[typing.Union[JSONUnitTest]]
        ]
    ] = None

    # overrides field is used to allow mypy type checking but is not used in Policy functionality
    overrides: PolicyOverrides = dataclasses.field(
        default=PolicyOverrides(), repr=False
    )

    # internal private methods
    def _typename(self) -> str:
        return "Policy"

    def _output_key(self) -> str:
        return "sdk-node:policy"

    def _fields(self) -> typing.List[str]:
        return [
            "filters",
            "policy_id",
            "resource_types",
            "severity",
            "alert_context",
            "alert_grouping",
            "alert_title",
            "description",
            "destinations",
            "enabled",
            "ignore_patterns",
            "name",
            "reference",
            "reports",
            "runbook",
            "tags",
            "unit_tests",
        ]


@dataclasses.dataclass
class RuleOverrides:
    """Overrides dataclass for Rule. All arguments are marked optional.

    - filters -- Define event filters for the rule
    - log_types -- Log Types to associate with this rule
    - rule_id -- ID for the rule
    - severity -- Severity for the rule
    - alert_context -- Optional JSON to attach to alerts generated by this rule
    - alert_grouping -- Configuration for how an alert is grouped
    - alert_title -- Title to use in the alert
    - description -- Description for the rule
    - destinations -- Alert destinations for the rule
    - enabled -- Whether the rule is enabled or not
    - name -- Display name for the rule
    - reference -- Reference for the rule
    - reports -- Report mappings for the rule
    - runbook -- Runbook for the rule
    - summary_attrs -- Summary Attributes for the rule
    - tags -- Tags for the rule
    - threshold -- Number of matches received before an alert is triggered
    - unit_tests -- Define event filters for the rule
    """

    filters: typing.Optional[
        typing.Union[
            typing.Union[PythonFilter], typing.List[typing.Union[PythonFilter]]
        ]
    ] = None

    log_types: typing.Optional[typing.Union[str, typing.List[str]]] = None

    rule_id: typing.Optional[str] = None

    severity: typing.Optional[typing.Union[str, DynamicStringField]] = None

    alert_context: typing.Optional[
        typing.Callable[[PantherEvent], typing.Dict[str, typing.Any]]
    ] = None

    alert_grouping: typing.Optional[AlertGrouping] = None

    alert_title: typing.Optional[typing.Callable[[PantherEvent], str]] = None

    description: typing.Optional[typing.Union[str, DynamicStringField]] = None

    destinations: typing.Optional[
        typing.Union[str, typing.List[str], DynamicDestinations]
    ] = None

    enabled: typing.Optional[bool] = None

    name: typing.Optional[str] = None

    reference: typing.Optional[typing.Union[str, DynamicStringField]] = None

    reports: typing.Optional[typing.Dict[str, typing.List[str]]] = None

    runbook: typing.Optional[typing.Union[str, DynamicStringField]] = None

    summary_attrs: typing.Optional[typing.List[str]] = None

    tags: typing.Optional[typing.Union[str, typing.List[str]]] = None

    threshold: typing.Optional[int] = None

    unit_tests: typing.Optional[
        typing.Union[
            typing.Union[JSONUnitTest], typing.List[typing.Union[JSONUnitTest]]
        ]
    ] = None


@overridable
@dataclasses.dataclass(frozen=True)
class Rule(_utilities.SDKNode):
    """Define a Rule-type detection to execute against log data in your Panther instance

    - filters -- Define event filters for the rule (required)
    - log_types -- Log Types to associate with this rule (required)
    - rule_id -- ID for the rule (required)
    - severity -- Severity for the rule (required)
    - alert_context -- Optional JSON to attach to alerts generated by this rule (optional, default: None)
    - alert_grouping -- Configuration for how an alert is grouped (optional, default: None)
    - alert_title -- Title to use in the alert (optional, default: None)
    - description -- Description for the rule (optional, default: "")
    - destinations -- Alert destinations for the rule (optional, default: None)
    - enabled -- Whether the rule is enabled or not (optional, default: True)
    - name -- Display name for the rule (optional, default: "")
    - reference -- Reference for the rule (optional, default: "")
    - reports -- Report mappings for the rule (optional, default: None)
    - runbook -- Runbook for the rule (optional, default: "")
    - summary_attrs -- Summary Attributes for the rule (optional, default: None)
    - tags -- Tags for the rule (optional, default: None)
    - threshold -- Number of matches received before an alert is triggered (optional, default: 1)
    - unit_tests -- Define event filters for the rule (optional, default: None)
    """

    # required
    filters: typing.Union[
        typing.Union[PythonFilter], typing.List[typing.Union[PythonFilter]]
    ]

    # required
    log_types: typing.Union[str, typing.List[str]]

    # required
    rule_id: str

    # required
    severity: typing.Union[str, DynamicStringField]

    # optional
    alert_context: typing.Optional[
        typing.Callable[[PantherEvent], typing.Dict[str, typing.Any]]
    ] = None

    # optional
    alert_grouping: typing.Optional[AlertGrouping] = None

    # optional
    alert_title: typing.Optional[typing.Callable[[PantherEvent], str]] = None

    # optional
    description: typing.Optional[typing.Union[str, DynamicStringField]] = ""

    # optional
    destinations: typing.Optional[
        typing.Union[str, typing.List[str], DynamicDestinations]
    ] = None

    # optional
    enabled: bool = True

    # optional
    name: typing.Optional[str] = ""

    # optional
    reference: typing.Optional[typing.Union[str, DynamicStringField]] = ""

    # optional
    reports: typing.Optional[typing.Dict[str, typing.List[str]]] = None

    # optional
    runbook: typing.Optional[typing.Union[str, DynamicStringField]] = ""

    # optional
    summary_attrs: typing.Optional[typing.List[str]] = None

    # optional
    tags: typing.Optional[typing.Union[str, typing.List[str]]] = None

    # optional
    threshold: int = 1

    # optional
    unit_tests: typing.Optional[
        typing.Union[
            typing.Union[JSONUnitTest], typing.List[typing.Union[JSONUnitTest]]
        ]
    ] = None

    # overrides field is used to allow mypy type checking but is not used in Rule functionality
    overrides: RuleOverrides = dataclasses.field(default=RuleOverrides(), repr=False)

    # internal private methods
    def _typename(self) -> str:
        return "Rule"

    def _output_key(self) -> str:
        return "sdk-node:rule"

    def _fields(self) -> typing.List[str]:
        return [
            "filters",
            "log_types",
            "rule_id",
            "severity",
            "alert_context",
            "alert_grouping",
            "alert_title",
            "description",
            "destinations",
            "enabled",
            "name",
            "reference",
            "reports",
            "runbook",
            "summary_attrs",
            "tags",
            "threshold",
            "unit_tests",
        ]


@dataclasses.dataclass
class ScheduledRuleOverrides:
    """Overrides dataclass for ScheduledRule. All arguments are marked optional.

    - filters -- Define event filters for the scheduled rule
    - rule_id -- ID for the scheduled rule
    - scheduled_queries -- Scheduled queries to associate with this scheduled rule
    - severity -- What severity alerts generated from this scheduled rule get assigned
    - alert_context -- Optional JSON to attach to alerts generated by this rule
    - alert_grouping -- Configuration for how an alert is grouped
    - alert_title -- Title to use in the alert
    - description -- Description for the scheduled rule
    - destinations -- Alert destinations for the scheduled rule
    - enabled -- Short description for the scheduled rule
    - name -- Display name for the scheduled rule
    - reference -- Reference for the scheduled rule
    - reports -- Report mappings for the scheduled rule
    - runbook -- Runbook for the scheduled rule
    - summary_attrs -- Summary Attributes for the scheduled rule
    - tags -- Tags for the scheduled rule
    - threshold -- Number of matches received before an alert is triggered
    - unit_tests -- Define event filters for the scheduled rule
    """

    filters: typing.Optional[
        typing.Union[
            typing.Union[PythonFilter], typing.List[typing.Union[PythonFilter]]
        ]
    ] = None

    rule_id: typing.Optional[str] = None

    scheduled_queries: typing.Optional[typing.Union[str, typing.List[str]]] = None

    severity: typing.Optional[typing.Union[str, DynamicStringField]] = None

    alert_context: typing.Optional[
        typing.Callable[[PantherEvent], typing.Dict[str, typing.Any]]
    ] = None

    alert_grouping: typing.Optional[AlertGrouping] = None

    alert_title: typing.Optional[typing.Callable[[PantherEvent], str]] = None

    description: typing.Optional[typing.Union[str, DynamicStringField]] = None

    destinations: typing.Optional[
        typing.Union[str, typing.List[str], DynamicDestinations]
    ] = None

    enabled: typing.Optional[bool] = None

    name: typing.Optional[str] = None

    reference: typing.Optional[typing.Union[str, DynamicStringField]] = None

    reports: typing.Optional[typing.Dict[str, typing.List[str]]] = None

    runbook: typing.Optional[typing.Union[str, DynamicStringField]] = None

    summary_attrs: typing.Optional[typing.List[str]] = None

    tags: typing.Optional[typing.Union[str, typing.List[str]]] = None

    threshold: typing.Optional[int] = None

    unit_tests: typing.Optional[
        typing.Union[
            typing.Union[JSONUnitTest], typing.List[typing.Union[JSONUnitTest]]
        ]
    ] = None


@overridable
@dataclasses.dataclass(frozen=True)
class ScheduledRule(_utilities.SDKNode):
    """Define a ScheduledRule-type detection to execute against query results in your Panther instance

    - filters -- Define event filters for the scheduled rule (required)
    - rule_id -- ID for the scheduled rule (required)
    - scheduled_queries -- Scheduled queries to associate with this scheduled rule (required)
    - severity -- What severity alerts generated from this scheduled rule get assigned (required)
    - alert_context -- Optional JSON to attach to alerts generated by this rule (optional, default: None)
    - alert_grouping -- Configuration for how an alert is grouped (optional, default: None)
    - alert_title -- Title to use in the alert (optional, default: None)
    - description -- Description for the scheduled rule (optional, default: "")
    - destinations -- Alert destinations for the scheduled rule (optional, default: None)
    - enabled -- Short description for the scheduled rule (optional, default: True)
    - name -- Display name for the scheduled rule (optional, default: "")
    - reference -- Reference for the scheduled rule (optional, default: "")
    - reports -- Report mappings for the scheduled rule (optional, default: None)
    - runbook -- Runbook for the scheduled rule (optional, default: "")
    - summary_attrs -- Summary Attributes for the scheduled rule (optional, default: None)
    - tags -- Tags for the scheduled rule (optional, default: None)
    - threshold -- Number of matches received before an alert is triggered (optional, default: 1)
    - unit_tests -- Define event filters for the scheduled rule (optional, default: None)
    """

    # required
    filters: typing.Union[
        typing.Union[PythonFilter], typing.List[typing.Union[PythonFilter]]
    ]

    # required
    rule_id: str

    # required
    scheduled_queries: typing.Union[str, typing.List[str]]

    # required
    severity: typing.Union[str, DynamicStringField]

    # optional
    alert_context: typing.Optional[
        typing.Callable[[PantherEvent], typing.Dict[str, typing.Any]]
    ] = None

    # optional
    alert_grouping: typing.Optional[AlertGrouping] = None

    # optional
    alert_title: typing.Optional[typing.Callable[[PantherEvent], str]] = None

    # optional
    description: typing.Optional[typing.Union[str, DynamicStringField]] = ""

    # optional
    destinations: typing.Optional[
        typing.Union[str, typing.List[str], DynamicDestinations]
    ] = None

    # optional
    enabled: bool = True

    # optional
    name: typing.Optional[str] = ""

    # optional
    reference: typing.Optional[typing.Union[str, DynamicStringField]] = ""

    # optional
    reports: typing.Optional[typing.Dict[str, typing.List[str]]] = None

    # optional
    runbook: typing.Optional[typing.Union[str, DynamicStringField]] = ""

    # optional
    summary_attrs: typing.Optional[typing.List[str]] = None

    # optional
    tags: typing.Optional[typing.Union[str, typing.List[str]]] = None

    # optional
    threshold: int = 1

    # optional
    unit_tests: typing.Optional[
        typing.Union[
            typing.Union[JSONUnitTest], typing.List[typing.Union[JSONUnitTest]]
        ]
    ] = None

    # overrides field is used to allow mypy type checking but is not used in ScheduledRule functionality
    overrides: ScheduledRuleOverrides = dataclasses.field(
        default=ScheduledRuleOverrides(), repr=False
    )

    # internal private methods
    def _typename(self) -> str:
        return "ScheduledRule"

    def _output_key(self) -> str:
        return "sdk-node:scheduled-rule"

    def _fields(self) -> typing.List[str]:
        return [
            "filters",
            "rule_id",
            "scheduled_queries",
            "severity",
            "alert_context",
            "alert_grouping",
            "alert_title",
            "description",
            "destinations",
            "enabled",
            "name",
            "reference",
            "reports",
            "runbook",
            "summary_attrs",
            "tags",
            "threshold",
            "unit_tests",
        ]


AnyFilter = typing.Union[PythonFilter]
AnyUnitTest = typing.Union[JSONUnitTest]
