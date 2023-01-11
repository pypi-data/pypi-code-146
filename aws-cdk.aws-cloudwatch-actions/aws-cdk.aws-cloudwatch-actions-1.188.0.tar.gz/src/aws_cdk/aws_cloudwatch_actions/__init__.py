'''
# CloudWatch Alarm Actions library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

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

from ._jsii import *

import aws_cdk.aws_applicationautoscaling as _aws_cdk_aws_applicationautoscaling_a31e8c21
import aws_cdk.aws_autoscaling as _aws_cdk_aws_autoscaling_92cc07a7
import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_9b88bb94
import aws_cdk.aws_sns as _aws_cdk_aws_sns_889c7272
import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_aws_cloudwatch_9b88bb94.IAlarmAction)
class ApplicationScalingAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudwatch-actions.ApplicationScalingAction",
):
    '''Use an ApplicationAutoScaling StepScalingAction as an Alarm Action.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_applicationautoscaling as appscaling
        import aws_cdk.aws_cloudwatch_actions as cloudwatch_actions
        
        # step_scaling_action: appscaling.StepScalingAction
        
        application_scaling_action = cloudwatch_actions.ApplicationScalingAction(step_scaling_action)
    '''

    def __init__(
        self,
        step_scaling_action: _aws_cdk_aws_applicationautoscaling_a31e8c21.StepScalingAction,
    ) -> None:
        '''
        :param step_scaling_action: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f61bc77f726d897b265015f62cf1c493e2609b8d2b3beaeb45acfa362fc64ed7)
            check_type(argname="argument step_scaling_action", value=step_scaling_action, expected_type=type_hints["step_scaling_action"])
        jsii.create(self.__class__, self, [step_scaling_action])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _aws_cdk_core_f4b25747.Construct,
        _alarm: _aws_cdk_aws_cloudwatch_9b88bb94.IAlarm,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.AlarmActionConfig:
        '''Returns an alarm action configuration to use an ApplicationScaling StepScalingAction as an alarm action.

        :param _scope: -
        :param _alarm: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f1fa70bb50963559d8469488472bcf3daeedc41e1248ead8be14e77f8df4177)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument _alarm", value=_alarm, expected_type=type_hints["_alarm"])
        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.AlarmActionConfig, jsii.invoke(self, "bind", [_scope, _alarm]))


@jsii.implements(_aws_cdk_aws_cloudwatch_9b88bb94.IAlarmAction)
class AutoScalingAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudwatch-actions.AutoScalingAction",
):
    '''Use an AutoScaling StepScalingAction as an Alarm Action.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_autoscaling as autoscaling
        import aws_cdk.aws_cloudwatch_actions as cloudwatch_actions
        
        # step_scaling_action: autoscaling.StepScalingAction
        
        auto_scaling_action = cloudwatch_actions.AutoScalingAction(step_scaling_action)
    '''

    def __init__(
        self,
        step_scaling_action: _aws_cdk_aws_autoscaling_92cc07a7.StepScalingAction,
    ) -> None:
        '''
        :param step_scaling_action: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d59731b16bdf550e1e465769ab30781a3a3ee84a689da09f1590516cf801af2c)
            check_type(argname="argument step_scaling_action", value=step_scaling_action, expected_type=type_hints["step_scaling_action"])
        jsii.create(self.__class__, self, [step_scaling_action])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _aws_cdk_core_f4b25747.Construct,
        _alarm: _aws_cdk_aws_cloudwatch_9b88bb94.IAlarm,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.AlarmActionConfig:
        '''Returns an alarm action configuration to use an AutoScaling StepScalingAction as an alarm action.

        :param _scope: -
        :param _alarm: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b32a6ac2b9cf5e3c28ea1b1d2b22293a43dca8fb3906de73fa4720acb3b2eea9)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument _alarm", value=_alarm, expected_type=type_hints["_alarm"])
        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.AlarmActionConfig, jsii.invoke(self, "bind", [_scope, _alarm]))


@jsii.implements(_aws_cdk_aws_cloudwatch_9b88bb94.IAlarmAction)
class Ec2Action(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudwatch-actions.Ec2Action",
):
    '''Use an EC2 action as an Alarm action.

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
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e400733a92f6c827d0871e2c00c45f54e166a21e774682d4fbfba394aaae8bd)
            check_type(argname="argument instance_action", value=instance_action, expected_type=type_hints["instance_action"])
        jsii.create(self.__class__, self, [instance_action])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _aws_cdk_core_f4b25747.Construct,
        _alarm: _aws_cdk_aws_cloudwatch_9b88bb94.IAlarm,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.AlarmActionConfig:
        '''Returns an alarm action configuration to use an EC2 action as an alarm action.

        :param _scope: -
        :param _alarm: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a3a5306d662cc54e5fc2f4fd30308536de0ad33275c2a8827ed4e3a16f5c24)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument _alarm", value=_alarm, expected_type=type_hints["_alarm"])
        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.AlarmActionConfig, jsii.invoke(self, "bind", [_scope, _alarm]))


@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch-actions.Ec2InstanceAction")
class Ec2InstanceAction(enum.Enum):
    '''Types of EC2 actions available.

    :exampleMetadata: infused

    Example::

        # Alarm must be configured with an EC2 per-instance metric
        # alarm: cloudwatch.Alarm
        
        # Attach a reboot when alarm triggers
        alarm.add_alarm_action(
            actions.Ec2Action(actions.Ec2InstanceAction.REBOOT))
    '''

    STOP = "STOP"
    '''Stop the instance.'''
    TERMINATE = "TERMINATE"
    '''Terminatethe instance.'''
    RECOVER = "RECOVER"
    '''Recover the instance.'''
    REBOOT = "REBOOT"
    '''Reboot the instance.'''


@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch-actions.OpsItemCategory")
class OpsItemCategory(enum.Enum):
    '''Types of OpsItem category available.

    :exampleMetadata: infused

    Example::

        # alarm: cloudwatch.Alarm
        
        # Create an OpsItem with specific severity and category when alarm triggers
        alarm.add_alarm_action(
            actions.SsmAction(actions.OpsItemSeverity.CRITICAL, actions.OpsItemCategory.PERFORMANCE))
    '''

    AVAILABILITY = "AVAILABILITY"
    '''Set the category to availability.'''
    COST = "COST"
    '''Set the category to cost.'''
    PERFORMANCE = "PERFORMANCE"
    '''Set the category to performance.'''
    RECOVERY = "RECOVERY"
    '''Set the category to recovery.'''
    SECURITY = "SECURITY"
    '''Set the category to security.'''


@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch-actions.OpsItemSeverity")
class OpsItemSeverity(enum.Enum):
    '''Types of OpsItem severity available.

    :exampleMetadata: infused

    Example::

        # alarm: cloudwatch.Alarm
        
        # Create an OpsItem with specific severity and category when alarm triggers
        alarm.add_alarm_action(
            actions.SsmAction(actions.OpsItemSeverity.CRITICAL, actions.OpsItemCategory.PERFORMANCE))
    '''

    CRITICAL = "CRITICAL"
    '''Set the severity to critical.'''
    HIGH = "HIGH"
    '''Set the severity to high.'''
    MEDIUM = "MEDIUM"
    '''Set the severity to medium.'''
    LOW = "LOW"
    '''Set the severity to low.'''


@jsii.implements(_aws_cdk_aws_cloudwatch_9b88bb94.IAlarmAction)
class SnsAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudwatch-actions.SnsAction",
):
    '''Use an SNS topic as an alarm action.

    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_cloudwatch_actions as cw_actions
        # alarm: cloudwatch.Alarm
        
        
        topic = sns.Topic(self, "Topic")
        alarm.add_alarm_action(cw_actions.SnsAction(topic))
    '''

    def __init__(self, topic: _aws_cdk_aws_sns_889c7272.ITopic) -> None:
        '''
        :param topic: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f15cb67b42af842688802659fb3ab749731ffe8c1fe0f9004c679ffcd6ddd554)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        jsii.create(self.__class__, self, [topic])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _aws_cdk_core_f4b25747.Construct,
        _alarm: _aws_cdk_aws_cloudwatch_9b88bb94.IAlarm,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.AlarmActionConfig:
        '''Returns an alarm action configuration to use an SNS topic as an alarm action.

        :param _scope: -
        :param _alarm: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86cf1a2137760a4d802e2355d33ca956dbadf3447967aca0b6ff94f8568f257d)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument _alarm", value=_alarm, expected_type=type_hints["_alarm"])
        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.AlarmActionConfig, jsii.invoke(self, "bind", [_scope, _alarm]))


@jsii.implements(_aws_cdk_aws_cloudwatch_9b88bb94.IAlarmAction)
class SsmAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudwatch-actions.SsmAction",
):
    '''Use an SSM OpsItem action as an Alarm action.

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
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d7f6b1dfe737883802e8ba03974b7eaabf30a6df7233887ef046dd63317f21d)
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
        jsii.create(self.__class__, self, [severity, category])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _aws_cdk_core_f4b25747.Construct,
        _alarm: _aws_cdk_aws_cloudwatch_9b88bb94.IAlarm,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.AlarmActionConfig:
        '''Returns an alarm action configuration to use an SSM OpsItem action as an alarm action.

        :param _scope: -
        :param _alarm: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54e273b6c221a708a17a90cbbf7e549b885be6917f27455806735d37d4724996)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument _alarm", value=_alarm, expected_type=type_hints["_alarm"])
        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.AlarmActionConfig, jsii.invoke(self, "bind", [_scope, _alarm]))


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

def _typecheckingstub__f61bc77f726d897b265015f62cf1c493e2609b8d2b3beaeb45acfa362fc64ed7(
    step_scaling_action: _aws_cdk_aws_applicationautoscaling_a31e8c21.StepScalingAction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f1fa70bb50963559d8469488472bcf3daeedc41e1248ead8be14e77f8df4177(
    _scope: _aws_cdk_core_f4b25747.Construct,
    _alarm: _aws_cdk_aws_cloudwatch_9b88bb94.IAlarm,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d59731b16bdf550e1e465769ab30781a3a3ee84a689da09f1590516cf801af2c(
    step_scaling_action: _aws_cdk_aws_autoscaling_92cc07a7.StepScalingAction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b32a6ac2b9cf5e3c28ea1b1d2b22293a43dca8fb3906de73fa4720acb3b2eea9(
    _scope: _aws_cdk_core_f4b25747.Construct,
    _alarm: _aws_cdk_aws_cloudwatch_9b88bb94.IAlarm,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e400733a92f6c827d0871e2c00c45f54e166a21e774682d4fbfba394aaae8bd(
    instance_action: Ec2InstanceAction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a3a5306d662cc54e5fc2f4fd30308536de0ad33275c2a8827ed4e3a16f5c24(
    _scope: _aws_cdk_core_f4b25747.Construct,
    _alarm: _aws_cdk_aws_cloudwatch_9b88bb94.IAlarm,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f15cb67b42af842688802659fb3ab749731ffe8c1fe0f9004c679ffcd6ddd554(
    topic: _aws_cdk_aws_sns_889c7272.ITopic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86cf1a2137760a4d802e2355d33ca956dbadf3447967aca0b6ff94f8568f257d(
    _scope: _aws_cdk_core_f4b25747.Construct,
    _alarm: _aws_cdk_aws_cloudwatch_9b88bb94.IAlarm,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d7f6b1dfe737883802e8ba03974b7eaabf30a6df7233887ef046dd63317f21d(
    severity: OpsItemSeverity,
    category: typing.Optional[OpsItemCategory] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e273b6c221a708a17a90cbbf7e549b885be6917f27455806735d37d4724996(
    _scope: _aws_cdk_core_f4b25747.Construct,
    _alarm: _aws_cdk_aws_cloudwatch_9b88bb94.IAlarm,
) -> None:
    """Type checking stubs"""
    pass
