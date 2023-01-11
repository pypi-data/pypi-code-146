'''
# CloudWatch Alarm Actions library

This library contains a set of classes which can be used as CloudWatch Alarm actions.

The currently implemented actions are: EC2 Actions, SNS Actions, SSM OpsCenter Actions, Autoscaling Actions and Application Autoscaling Actions

## EC2 Action Example

```python
# Alarm must be configured with an EC2 per-instance metric
# alarm: cloudwatch.Alarm

# Attach a reboot when alarm triggers
alarm.add_alarm_action(
    actions.Ec2Action(actions.Ec2InstanceAction.REBOOT))
```

## SSM OpsCenter Action Example

```python
# alarm: cloudwatch.Alarm

# Create an OpsItem with specific severity and category when alarm triggers
alarm.add_alarm_action(
    actions.SsmAction(actions.OpsItemSeverity.CRITICAL, actions.OpsItemCategory.PERFORMANCE))
```

See `@aws-cdk/aws-cloudwatch` for more information.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

from .. import Construct as _Construct_e78e779f
from ..aws_applicationautoscaling import (
    StepScalingAction as _StepScalingAction_20c2d829
)
from ..aws_autoscaling import StepScalingAction as _StepScalingAction_569c9499
from ..aws_cloudwatch import (
    AlarmActionConfig as _AlarmActionConfig_aebdae35,
    IAlarm as _IAlarm_bf66c8d0,
    IAlarmAction as _IAlarmAction_22055cd4,
)
from ..aws_sns import ITopic as _ITopic_465e36b9


@jsii.implements(_IAlarmAction_22055cd4)
class ApplicationScalingAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch_actions.ApplicationScalingAction",
):
    '''(experimental) Use an ApplicationAutoScaling StepScalingAction as an Alarm Action.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_applicationautoscaling as applicationautoscaling
        from monocdk import aws_cloudwatch_actions as cloudwatch_actions
        
        # step_scaling_action: applicationautoscaling.StepScalingAction
        
        application_scaling_action = cloudwatch_actions.ApplicationScalingAction(step_scaling_action)
    '''

    def __init__(self, step_scaling_action: _StepScalingAction_20c2d829) -> None:
        '''
        :param step_scaling_action: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f9819e9200f6acb4bc6dd7807fbb24f6c60f751352372879372ffa76225bde4)
            check_type(argname="argument step_scaling_action", value=step_scaling_action, expected_type=type_hints["step_scaling_action"])
        jsii.create(self.__class__, self, [step_scaling_action])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _Construct_e78e779f,
        _alarm: _IAlarm_bf66c8d0,
    ) -> _AlarmActionConfig_aebdae35:
        '''(experimental) Returns an alarm action configuration to use an ApplicationScaling StepScalingAction as an alarm action.

        :param _scope: -
        :param _alarm: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3fe73bd3412ecb0dd75095e9a344c75702d431abf6ed64ab151f2f0f3eac8c4)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument _alarm", value=_alarm, expected_type=type_hints["_alarm"])
        return typing.cast(_AlarmActionConfig_aebdae35, jsii.invoke(self, "bind", [_scope, _alarm]))


@jsii.implements(_IAlarmAction_22055cd4)
class AutoScalingAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch_actions.AutoScalingAction",
):
    '''(experimental) Use an AutoScaling StepScalingAction as an Alarm Action.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_autoscaling as autoscaling
        from monocdk import aws_cloudwatch_actions as cloudwatch_actions
        
        # step_scaling_action: autoscaling.StepScalingAction
        
        auto_scaling_action = cloudwatch_actions.AutoScalingAction(step_scaling_action)
    '''

    def __init__(self, step_scaling_action: _StepScalingAction_569c9499) -> None:
        '''
        :param step_scaling_action: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25df82c3e2662c2656571fa988a9d85c45e740f34cf1455e7576bf5a6fe20f06)
            check_type(argname="argument step_scaling_action", value=step_scaling_action, expected_type=type_hints["step_scaling_action"])
        jsii.create(self.__class__, self, [step_scaling_action])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _Construct_e78e779f,
        _alarm: _IAlarm_bf66c8d0,
    ) -> _AlarmActionConfig_aebdae35:
        '''(experimental) Returns an alarm action configuration to use an AutoScaling StepScalingAction as an alarm action.

        :param _scope: -
        :param _alarm: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f0f2f6b6f1f1545fbcbee917c205ad6bd818f64d68653a5050a735e62b3df33)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument _alarm", value=_alarm, expected_type=type_hints["_alarm"])
        return typing.cast(_AlarmActionConfig_aebdae35, jsii.invoke(self, "bind", [_scope, _alarm]))


@jsii.implements(_IAlarmAction_22055cd4)
class Ec2Action(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch_actions.Ec2Action",
):
    '''(experimental) Use an EC2 action as an Alarm action.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Alarm must be configured with an EC2 per-instance metric
        # alarm: cloudwatch.Alarm
        
        # Attach a reboot when alarm triggers
        alarm.add_alarm_action(
            actions.Ec2Action(actions.Ec2InstanceAction.REBOOT))
    '''

    def __init__(self, instance_action: "Ec2InstanceAction") -> None:
        '''
        :param instance_action: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2830a9f1fd8ea30bf9ec3772a4a8614f8c92c347aeeaa151e32719fe7920d0e)
            check_type(argname="argument instance_action", value=instance_action, expected_type=type_hints["instance_action"])
        jsii.create(self.__class__, self, [instance_action])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _Construct_e78e779f,
        _alarm: _IAlarm_bf66c8d0,
    ) -> _AlarmActionConfig_aebdae35:
        '''(experimental) Returns an alarm action configuration to use an EC2 action as an alarm action.

        :param _scope: -
        :param _alarm: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ecce9f206b5df0c9239c9c3a8633f65a1d7ba3e088b46ade0b8b64f9fcf799)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument _alarm", value=_alarm, expected_type=type_hints["_alarm"])
        return typing.cast(_AlarmActionConfig_aebdae35, jsii.invoke(self, "bind", [_scope, _alarm]))


@jsii.enum(jsii_type="monocdk.aws_cloudwatch_actions.Ec2InstanceAction")
class Ec2InstanceAction(enum.Enum):
    '''(experimental) Types of EC2 actions available.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Alarm must be configured with an EC2 per-instance metric
        # alarm: cloudwatch.Alarm
        
        # Attach a reboot when alarm triggers
        alarm.add_alarm_action(
            actions.Ec2Action(actions.Ec2InstanceAction.REBOOT))
    '''

    STOP = "STOP"
    '''(experimental) Stop the instance.

    :stability: experimental
    '''
    TERMINATE = "TERMINATE"
    '''(experimental) Terminatethe instance.

    :stability: experimental
    '''
    RECOVER = "RECOVER"
    '''(experimental) Recover the instance.

    :stability: experimental
    '''
    REBOOT = "REBOOT"
    '''(experimental) Reboot the instance.

    :stability: experimental
    '''


@jsii.enum(jsii_type="monocdk.aws_cloudwatch_actions.OpsItemCategory")
class OpsItemCategory(enum.Enum):
    '''(experimental) Types of OpsItem category available.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # alarm: cloudwatch.Alarm
        
        # Create an OpsItem with specific severity and category when alarm triggers
        alarm.add_alarm_action(
            actions.SsmAction(actions.OpsItemSeverity.CRITICAL, actions.OpsItemCategory.PERFORMANCE))
    '''

    AVAILABILITY = "AVAILABILITY"
    '''(experimental) Set the category to availability.

    :stability: experimental
    '''
    COST = "COST"
    '''(experimental) Set the category to cost.

    :stability: experimental
    '''
    PERFORMANCE = "PERFORMANCE"
    '''(experimental) Set the category to performance.

    :stability: experimental
    '''
    RECOVERY = "RECOVERY"
    '''(experimental) Set the category to recovery.

    :stability: experimental
    '''
    SECURITY = "SECURITY"
    '''(experimental) Set the category to security.

    :stability: experimental
    '''


@jsii.enum(jsii_type="monocdk.aws_cloudwatch_actions.OpsItemSeverity")
class OpsItemSeverity(enum.Enum):
    '''(experimental) Types of OpsItem severity available.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # alarm: cloudwatch.Alarm
        
        # Create an OpsItem with specific severity and category when alarm triggers
        alarm.add_alarm_action(
            actions.SsmAction(actions.OpsItemSeverity.CRITICAL, actions.OpsItemCategory.PERFORMANCE))
    '''

    CRITICAL = "CRITICAL"
    '''(experimental) Set the severity to critical.

    :stability: experimental
    '''
    HIGH = "HIGH"
    '''(experimental) Set the severity to high.

    :stability: experimental
    '''
    MEDIUM = "MEDIUM"
    '''(experimental) Set the severity to medium.

    :stability: experimental
    '''
    LOW = "LOW"
    '''(experimental) Set the severity to low.

    :stability: experimental
    '''


@jsii.implements(_IAlarmAction_22055cd4)
class SnsAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch_actions.SnsAction",
):
    '''(experimental) Use an SNS topic as an alarm action.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as cw_actions
        # alarm: cloudwatch.Alarm
        
        
        topic = sns.Topic(self, "Topic")
        alarm.add_alarm_action(cw_actions.SnsAction(topic))
    '''

    def __init__(self, topic: _ITopic_465e36b9) -> None:
        '''
        :param topic: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9f95383ac34b02080a47995670166aa93785761d10d2a4e7457b068b0149f33)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        jsii.create(self.__class__, self, [topic])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _Construct_e78e779f,
        _alarm: _IAlarm_bf66c8d0,
    ) -> _AlarmActionConfig_aebdae35:
        '''(experimental) Returns an alarm action configuration to use an SNS topic as an alarm action.

        :param _scope: -
        :param _alarm: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__267bf0b11dcf1a50304868315363f5cbc7a982ce10b4e0f1214add5419af5e8a)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument _alarm", value=_alarm, expected_type=type_hints["_alarm"])
        return typing.cast(_AlarmActionConfig_aebdae35, jsii.invoke(self, "bind", [_scope, _alarm]))


@jsii.implements(_IAlarmAction_22055cd4)
class SsmAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudwatch_actions.SsmAction",
):
    '''(experimental) Use an SSM OpsItem action as an Alarm action.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # alarm: cloudwatch.Alarm
        
        # Create an OpsItem with specific severity and category when alarm triggers
        alarm.add_alarm_action(
            actions.SsmAction(actions.OpsItemSeverity.CRITICAL, actions.OpsItemCategory.PERFORMANCE))
    '''

    def __init__(
        self,
        severity: OpsItemSeverity,
        category: typing.Optional[OpsItemCategory] = None,
    ) -> None:
        '''
        :param severity: -
        :param category: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d5e20100731a14fc8347a8b6ccc44905d9f64a891ad34563fe7403bea5de71b)
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
        jsii.create(self.__class__, self, [severity, category])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _Construct_e78e779f,
        _alarm: _IAlarm_bf66c8d0,
    ) -> _AlarmActionConfig_aebdae35:
        '''(experimental) Returns an alarm action configuration to use an SSM OpsItem action as an alarm action.

        :param _scope: -
        :param _alarm: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d2b3828adde5855e5144a42e16dfc5f8b50ed903d602d41fda3a0207803d5e8)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument _alarm", value=_alarm, expected_type=type_hints["_alarm"])
        return typing.cast(_AlarmActionConfig_aebdae35, jsii.invoke(self, "bind", [_scope, _alarm]))


__all__ = [
    "ApplicationScalingAction",
    "AutoScalingAction",
    "Ec2Action",
    "Ec2InstanceAction",
    "OpsItemCategory",
    "OpsItemSeverity",
    "SnsAction",
    "SsmAction",
]

publication.publish()

def _typecheckingstub__1f9819e9200f6acb4bc6dd7807fbb24f6c60f751352372879372ffa76225bde4(
    step_scaling_action: _StepScalingAction_20c2d829,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3fe73bd3412ecb0dd75095e9a344c75702d431abf6ed64ab151f2f0f3eac8c4(
    _scope: _Construct_e78e779f,
    _alarm: _IAlarm_bf66c8d0,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25df82c3e2662c2656571fa988a9d85c45e740f34cf1455e7576bf5a6fe20f06(
    step_scaling_action: _StepScalingAction_569c9499,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f0f2f6b6f1f1545fbcbee917c205ad6bd818f64d68653a5050a735e62b3df33(
    _scope: _Construct_e78e779f,
    _alarm: _IAlarm_bf66c8d0,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2830a9f1fd8ea30bf9ec3772a4a8614f8c92c347aeeaa151e32719fe7920d0e(
    instance_action: Ec2InstanceAction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ecce9f206b5df0c9239c9c3a8633f65a1d7ba3e088b46ade0b8b64f9fcf799(
    _scope: _Construct_e78e779f,
    _alarm: _IAlarm_bf66c8d0,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f95383ac34b02080a47995670166aa93785761d10d2a4e7457b068b0149f33(
    topic: _ITopic_465e36b9,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267bf0b11dcf1a50304868315363f5cbc7a982ce10b4e0f1214add5419af5e8a(
    _scope: _Construct_e78e779f,
    _alarm: _IAlarm_bf66c8d0,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d5e20100731a14fc8347a8b6ccc44905d9f64a891ad34563fe7403bea5de71b(
    severity: OpsItemSeverity,
    category: typing.Optional[OpsItemCategory] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2b3828adde5855e5144a42e16dfc5f8b50ed903d602d41fda3a0207803d5e8(
    _scope: _Construct_e78e779f,
    _alarm: _IAlarm_bf66c8d0,
) -> None:
    """Type checking stubs"""
    pass
