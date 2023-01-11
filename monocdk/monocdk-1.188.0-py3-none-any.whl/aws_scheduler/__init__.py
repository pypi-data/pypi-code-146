'''
# AWS::Scheduler Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as scheduler
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Scheduler construct libraries](https://constructs.dev/search?q=scheduler)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Scheduler resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Scheduler.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Scheduler](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Scheduler.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/master/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
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

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnSchedule(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_scheduler.CfnSchedule",
):
    '''A CloudFormation ``AWS::Scheduler::Schedule``.

    Creates the specified schedule.

    :cloudformationResource: AWS::Scheduler::Schedule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_scheduler as scheduler
        
        # tags: Any
        
        cfn_schedule = scheduler.CfnSchedule(self, "MyCfnSchedule",
            flexible_time_window=scheduler.CfnSchedule.FlexibleTimeWindowProperty(
                mode="mode",
        
                # the properties below are optional
                maximum_window_in_minutes=123
            ),
            schedule_expression="scheduleExpression",
            target=scheduler.CfnSchedule.TargetProperty(
                arn="arn",
                role_arn="roleArn",
        
                # the properties below are optional
                dead_letter_config=scheduler.CfnSchedule.DeadLetterConfigProperty(
                    arn="arn"
                ),
                ecs_parameters=scheduler.CfnSchedule.EcsParametersProperty(
                    task_definition_arn="taskDefinitionArn",
        
                    # the properties below are optional
                    capacity_provider_strategy=[scheduler.CfnSchedule.CapacityProviderStrategyItemProperty(
                        capacity_provider="capacityProvider",
        
                        # the properties below are optional
                        base=123,
                        weight=123
                    )],
                    enable_ecs_managed_tags=False,
                    enable_execute_command=False,
                    group="group",
                    launch_type="launchType",
                    network_configuration=scheduler.CfnSchedule.NetworkConfigurationProperty(
                        awsvpc_configuration=scheduler.CfnSchedule.AwsVpcConfigurationProperty(
                            subnets=["subnets"],
        
                            # the properties below are optional
                            assign_public_ip="assignPublicIp",
                            security_groups=["securityGroups"]
                        )
                    ),
                    placement_constraints=[scheduler.CfnSchedule.PlacementConstraintProperty(
                        expression="expression",
                        type="type"
                    )],
                    placement_strategy=[scheduler.CfnSchedule.PlacementStrategyProperty(
                        field="field",
                        type="type"
                    )],
                    platform_version="platformVersion",
                    propagate_tags="propagateTags",
                    reference_id="referenceId",
                    tags=tags,
                    task_count=123
                ),
                event_bridge_parameters=scheduler.CfnSchedule.EventBridgeParametersProperty(
                    detail_type="detailType",
                    source="source"
                ),
                input="input",
                kinesis_parameters=scheduler.CfnSchedule.KinesisParametersProperty(
                    partition_key="partitionKey"
                ),
                retry_policy=scheduler.CfnSchedule.RetryPolicyProperty(
                    maximum_event_age_in_seconds=123,
                    maximum_retry_attempts=123
                ),
                sage_maker_pipeline_parameters=scheduler.CfnSchedule.SageMakerPipelineParametersProperty(
                    pipeline_parameter_list=[scheduler.CfnSchedule.SageMakerPipelineParameterProperty(
                        name="name",
                        value="value"
                    )]
                ),
                sqs_parameters=scheduler.CfnSchedule.SqsParametersProperty(
                    message_group_id="messageGroupId"
                )
            ),
        
            # the properties below are optional
            description="description",
            end_date="endDate",
            group_name="groupName",
            kms_key_arn="kmsKeyArn",
            name="name",
            schedule_expression_timezone="scheduleExpressionTimezone",
            start_date="startDate",
            state="state"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        flexible_time_window: typing.Union[typing.Union["CfnSchedule.FlexibleTimeWindowProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        schedule_expression: builtins.str,
        target: typing.Union[typing.Union["CfnSchedule.TargetProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        end_date: typing.Optional[builtins.str] = None,
        group_name: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        schedule_expression_timezone: typing.Optional[builtins.str] = None,
        start_date: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Scheduler::Schedule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param flexible_time_window: Allows you to configure a time window during which EventBridge Scheduler invokes the schedule.
        :param schedule_expression: The expression that defines when the schedule runs. The following formats are supported. - ``at`` expression - ``at(yyyy-mm-ddThh:mm:ss)`` - ``rate`` expression - ``rate(unit value)`` - ``cron`` expression - ``cron(fields)`` You can use ``at`` expressions to create one-time schedules that invoke a target once, at the time and in the time zone, that you specify. You can use ``rate`` and ``cron`` expressions to create recurring schedules. Rate-based schedules are useful when you want to invoke a target at regular intervals, such as every 15 minutes or every five days. Cron-based schedules are useful when you want to invoke a target periodically at a specific time, such as at 8:00 am (UTC+0) every 1st day of the month. A ``cron`` expression consists of six fields separated by white spaces: ``(minutes hours day_of_month month day_of_week year)`` . A ``rate`` expression consists of a *value* as a positive integer, and a *unit* with the following options: ``minute`` | ``minutes`` | ``hour`` | ``hours`` | ``day`` | ``days`` For more information and examples, see `Schedule types on EventBridge Scheduler <https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html>`_ in the *EventBridge Scheduler User Guide* .
        :param target: The schedule's target details.
        :param description: The description you specify for the schedule.
        :param end_date: The date, in UTC, before which the schedule can invoke its target. Depending on the schedule's recurrence expression, invocations might stop on, or before, the ``EndDate`` you specify. EventBridge Scheduler ignores ``EndDate`` for one-time schedules.
        :param group_name: The name of the schedule group associated with this schedule.
        :param kms_key_arn: The Amazon Resource Name (ARN) for the customer managed KMS key that EventBridge Scheduler will use to encrypt and decrypt your data.
        :param name: The name of the schedule.
        :param schedule_expression_timezone: The timezone in which the scheduling expression is evaluated.
        :param start_date: The date, in UTC, after which the schedule can begin invoking its target. Depending on the schedule's recurrence expression, invocations might occur on, or after, the ``StartDate`` you specify. EventBridge Scheduler ignores ``StartDate`` for one-time schedules.
        :param state: Specifies whether the schedule is enabled or disabled.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba25e64f746f8fa7a5d1e2d04f5f19027a8b4c994f38b48f449140a19f9372f6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnScheduleProps(
            flexible_time_window=flexible_time_window,
            schedule_expression=schedule_expression,
            target=target,
            description=description,
            end_date=end_date,
            group_name=group_name,
            kms_key_arn=kms_key_arn,
            name=name,
            schedule_expression_timezone=schedule_expression_timezone,
            start_date=start_date,
            state=state,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d9deb64c974ffc04efce7eb9c9ef983ea4725dfd8add3f7cbea81bfa7d4b404)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e4dae299315aa379226601968701041339a2dd79d8be34e07fa0833029784d8)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for the Amazon EventBridge Scheduler schedule.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="flexibleTimeWindow")
    def flexible_time_window(
        self,
    ) -> typing.Union["CfnSchedule.FlexibleTimeWindowProperty", _IResolvable_a771d0ef]:
        '''Allows you to configure a time window during which EventBridge Scheduler invokes the schedule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-flexibletimewindow
        '''
        return typing.cast(typing.Union["CfnSchedule.FlexibleTimeWindowProperty", _IResolvable_a771d0ef], jsii.get(self, "flexibleTimeWindow"))

    @flexible_time_window.setter
    def flexible_time_window(
        self,
        value: typing.Union["CfnSchedule.FlexibleTimeWindowProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b66cde60fa736ec009451b701de99a70b871d6c1ffa14f8c8bc073efa21ff1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flexibleTimeWindow", value)

    @builtins.property
    @jsii.member(jsii_name="scheduleExpression")
    def schedule_expression(self) -> builtins.str:
        '''The expression that defines when the schedule runs. The following formats are supported.

        - ``at`` expression - ``at(yyyy-mm-ddThh:mm:ss)``
        - ``rate`` expression - ``rate(unit value)``
        - ``cron`` expression - ``cron(fields)``

        You can use ``at`` expressions to create one-time schedules that invoke a target once, at the time and in the time zone, that you specify. You can use ``rate`` and ``cron`` expressions to create recurring schedules. Rate-based schedules are useful when you want to invoke a target at regular intervals, such as every 15 minutes or every five days. Cron-based schedules are useful when you want to invoke a target periodically at a specific time, such as at 8:00 am (UTC+0) every 1st day of the month.

        A ``cron`` expression consists of six fields separated by white spaces: ``(minutes hours day_of_month month day_of_week year)`` .

        A ``rate`` expression consists of a *value* as a positive integer, and a *unit* with the following options: ``minute`` | ``minutes`` | ``hour`` | ``hours`` | ``day`` | ``days``

        For more information and examples, see `Schedule types on EventBridge Scheduler <https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html>`_ in the *EventBridge Scheduler User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-scheduleexpression
        '''
        return typing.cast(builtins.str, jsii.get(self, "scheduleExpression"))

    @schedule_expression.setter
    def schedule_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44621d34d7b55afbbcf96371376065aadced9f702bf3204b4cef26fed2dacbda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleExpression", value)

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(
        self,
    ) -> typing.Union["CfnSchedule.TargetProperty", _IResolvable_a771d0ef]:
        '''The schedule's target details.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-target
        '''
        return typing.cast(typing.Union["CfnSchedule.TargetProperty", _IResolvable_a771d0ef], jsii.get(self, "target"))

    @target.setter
    def target(
        self,
        value: typing.Union["CfnSchedule.TargetProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__960d5d92b33ff31984b675c8627c63acd9cc031cb346220fc03103b6c83cb601)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description you specify for the schedule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6ca13b10d05e657b7573272b277c975aba40ef419b7dc6f2414bb071606bbe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="endDate")
    def end_date(self) -> typing.Optional[builtins.str]:
        '''The date, in UTC, before which the schedule can invoke its target.

        Depending on the schedule's recurrence expression, invocations might stop on, or before, the ``EndDate`` you specify.
        EventBridge Scheduler ignores ``EndDate`` for one-time schedules.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-enddate
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endDate"))

    @end_date.setter
    def end_date(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a989f59f2bfd6b56fd707171ad3e9bdcf955ea09768d930c6bb6e17bf45b1a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endDate", value)

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the schedule group associated with this schedule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-groupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupName"))

    @group_name.setter
    def group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb4b0b36ba92f25d07fa92f9ef85d0c7370bacc3b782806cc3d7e3e3bf229195)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupName", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) for the customer managed KMS key that EventBridge Scheduler will use to encrypt and decrypt your data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-kmskeyarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e074b998485064e1aa888150b0198fd0d15409c0ad990d00ac32c66c5e7403b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the schedule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__625a6b22966549274dd26f07bcfa0ec61b5a5304809967f04a4dd865e59080f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="scheduleExpressionTimezone")
    def schedule_expression_timezone(self) -> typing.Optional[builtins.str]:
        '''The timezone in which the scheduling expression is evaluated.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-scheduleexpressiontimezone
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleExpressionTimezone"))

    @schedule_expression_timezone.setter
    def schedule_expression_timezone(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9cfd9bcb214d49f0cfc1ce8b9de30755fd7874c752292ff81fc2c364b443cc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleExpressionTimezone", value)

    @builtins.property
    @jsii.member(jsii_name="startDate")
    def start_date(self) -> typing.Optional[builtins.str]:
        '''The date, in UTC, after which the schedule can begin invoking its target.

        Depending on the schedule's recurrence expression, invocations might occur on, or after, the ``StartDate`` you specify.
        EventBridge Scheduler ignores ``StartDate`` for one-time schedules.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-startdate
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startDate"))

    @start_date.setter
    def start_date(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b2c8f214c451833198ae5f74c7c53a850209f0601339becb1bf0ce8c5e03a3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startDate", value)

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the schedule is enabled or disabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-state
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "state"))

    @state.setter
    def state(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7971622377d5a373004c4cc2e327711e8125760a902e916a419b40d4b96e6aed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_scheduler.CfnSchedule.AwsVpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "subnets": "subnets",
            "assign_public_ip": "assignPublicIp",
            "security_groups": "securityGroups",
        },
    )
    class AwsVpcConfigurationProperty:
        def __init__(
            self,
            *,
            subnets: typing.Sequence[builtins.str],
            assign_public_ip: typing.Optional[builtins.str] = None,
            security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''This structure specifies the VPC subnets and security groups for the task, and whether a public IP address is to be used.

            This structure is relevant only for ECS tasks that use the awsvpc network mode.

            :param subnets: Specifies the subnets associated with the task. These subnets must all be in the same VPC. You can specify as many as 16 subnets.
            :param assign_public_ip: Specifies whether the task's elastic network interface receives a public IP address. You can specify ``ENABLED`` only when ``LaunchType`` in ``EcsParameters`` is set to ``FARGATE`` .
            :param security_groups: Specifies the security groups associated with the task. These security groups must all be in the same VPC. You can specify as many as five security groups. If you do not specify a security group, the default security group for the VPC is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-awsvpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_scheduler as scheduler
                
                aws_vpc_configuration_property = scheduler.CfnSchedule.AwsVpcConfigurationProperty(
                    subnets=["subnets"],
                
                    # the properties below are optional
                    assign_public_ip="assignPublicIp",
                    security_groups=["securityGroups"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8396c06a348956ed63f98299f89742fcd10b456cf5223802a1b0b9e5528042ca)
                check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
                check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
                check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "subnets": subnets,
            }
            if assign_public_ip is not None:
                self._values["assign_public_ip"] = assign_public_ip
            if security_groups is not None:
                self._values["security_groups"] = security_groups

        @builtins.property
        def subnets(self) -> typing.List[builtins.str]:
            '''Specifies the subnets associated with the task.

            These subnets must all be in the same VPC. You can specify as many as 16 subnets.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-awsvpcconfiguration.html#cfn-scheduler-schedule-awsvpcconfiguration-subnets
            '''
            result = self._values.get("subnets")
            assert result is not None, "Required property 'subnets' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def assign_public_ip(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the task's elastic network interface receives a public IP address.

            You can specify ``ENABLED`` only when ``LaunchType`` in ``EcsParameters`` is set to ``FARGATE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-awsvpcconfiguration.html#cfn-scheduler-schedule-awsvpcconfiguration-assignpublicip
            '''
            result = self._values.get("assign_public_ip")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the security groups associated with the task.

            These security groups must all be in the same VPC. You can specify as many as five security groups. If you do not specify a security group, the default security group for the VPC is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-awsvpcconfiguration.html#cfn-scheduler-schedule-awsvpcconfiguration-securitygroups
            '''
            result = self._values.get("security_groups")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsVpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_scheduler.CfnSchedule.CapacityProviderStrategyItemProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capacity_provider": "capacityProvider",
            "base": "base",
            "weight": "weight",
        },
    )
    class CapacityProviderStrategyItemProperty:
        def __init__(
            self,
            *,
            capacity_provider: builtins.str,
            base: typing.Optional[jsii.Number] = None,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The details of a capacity provider strategy.

            :param capacity_provider: The short name of the capacity provider.
            :param base: The base value designates how many tasks, at a minimum, to run on the specified capacity provider. Only one capacity provider in a capacity provider strategy can have a base defined. If no value is specified, the default value of ``0`` is used.
            :param weight: The weight value designates the relative percentage of the total number of tasks launched that should use the specified capacity provider. The weight value is taken into consideration after the base value, if defined, is satisfied.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-capacityproviderstrategyitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_scheduler as scheduler
                
                capacity_provider_strategy_item_property = scheduler.CfnSchedule.CapacityProviderStrategyItemProperty(
                    capacity_provider="capacityProvider",
                
                    # the properties below are optional
                    base=123,
                    weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d87a256e51d8558d5c79a90737f7c86d03718da9e44a6199f6613a03ae5dae23)
                check_type(argname="argument capacity_provider", value=capacity_provider, expected_type=type_hints["capacity_provider"])
                check_type(argname="argument base", value=base, expected_type=type_hints["base"])
                check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "capacity_provider": capacity_provider,
            }
            if base is not None:
                self._values["base"] = base
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def capacity_provider(self) -> builtins.str:
            '''The short name of the capacity provider.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-capacityproviderstrategyitem.html#cfn-scheduler-schedule-capacityproviderstrategyitem-capacityprovider
            '''
            result = self._values.get("capacity_provider")
            assert result is not None, "Required property 'capacity_provider' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def base(self) -> typing.Optional[jsii.Number]:
            '''The base value designates how many tasks, at a minimum, to run on the specified capacity provider.

            Only one capacity provider in a capacity provider strategy can have a base defined. If no value is specified, the default value of ``0`` is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-capacityproviderstrategyitem.html#cfn-scheduler-schedule-capacityproviderstrategyitem-base
            '''
            result = self._values.get("base")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''The weight value designates the relative percentage of the total number of tasks launched that should use the specified capacity provider.

            The weight value is taken into consideration after the base value, if defined, is satisfied.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-capacityproviderstrategyitem.html#cfn-scheduler-schedule-capacityproviderstrategyitem-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityProviderStrategyItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_scheduler.CfnSchedule.DeadLetterConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class DeadLetterConfigProperty:
        def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
            '''An object that contains information about an Amazon SQS queue that EventBridge Scheduler uses as a dead-letter queue for your schedule.

            If specified, EventBridge Scheduler delivers failed events that could not be successfully delivered to a target to the queue.

            :param arn: The Amazon Resource Name (ARN) of the SQS queue specified as the destination for the dead-letter queue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-deadletterconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_scheduler as scheduler
                
                dead_letter_config_property = scheduler.CfnSchedule.DeadLetterConfigProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3f172d16ccf6e4cea837a6343e2aecbdcaee91af772f18fc4e8f393c92261310)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the SQS queue specified as the destination for the dead-letter queue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-deadletterconfig.html#cfn-scheduler-schedule-deadletterconfig-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeadLetterConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_scheduler.CfnSchedule.EcsParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "task_definition_arn": "taskDefinitionArn",
            "capacity_provider_strategy": "capacityProviderStrategy",
            "enable_ecs_managed_tags": "enableEcsManagedTags",
            "enable_execute_command": "enableExecuteCommand",
            "group": "group",
            "launch_type": "launchType",
            "network_configuration": "networkConfiguration",
            "placement_constraints": "placementConstraints",
            "placement_strategy": "placementStrategy",
            "platform_version": "platformVersion",
            "propagate_tags": "propagateTags",
            "reference_id": "referenceId",
            "tags": "tags",
            "task_count": "taskCount",
        },
    )
    class EcsParametersProperty:
        def __init__(
            self,
            *,
            task_definition_arn: builtins.str,
            capacity_provider_strategy: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnSchedule.CapacityProviderStrategyItemProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            enable_ecs_managed_tags: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            enable_execute_command: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            group: typing.Optional[builtins.str] = None,
            launch_type: typing.Optional[builtins.str] = None,
            network_configuration: typing.Optional[typing.Union[typing.Union["CfnSchedule.NetworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            placement_constraints: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnSchedule.PlacementConstraintProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            placement_strategy: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnSchedule.PlacementStrategyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            platform_version: typing.Optional[builtins.str] = None,
            propagate_tags: typing.Optional[builtins.str] = None,
            reference_id: typing.Optional[builtins.str] = None,
            tags: typing.Any = None,
            task_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The templated target type for the Amazon ECS ```RunTask`` <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RunTask.html>`_ API operation.

            :param task_definition_arn: The Amazon Resource Name (ARN) of the task definition to use if the event target is an Amazon ECS task.
            :param capacity_provider_strategy: The capacity provider strategy to use for the task.
            :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the task. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ in the *Amazon ECS Developer Guide* .
            :param enable_execute_command: Whether or not to enable the execute command functionality for the containers in this task. If true, this enables execute command functionality on all containers in the task.
            :param group: Specifies an ECS task group for the task. The maximum length is 255 characters.
            :param launch_type: Specifies the launch type on which your task is running. The launch type that you specify here must match one of the launch type (compatibilities) of the target task. The ``FARGATE`` value is supported only in the Regions where Fargate with Amazon ECS is supported. For more information, see `AWS Fargate on Amazon ECS <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html>`_ in the *Amazon ECS Developer Guide* .
            :param network_configuration: This structure specifies the network configuration for an ECS task.
            :param placement_constraints: An array of placement constraint objects to use for the task. You can specify up to 10 constraints per task (including constraints in the task definition and those specified at runtime).
            :param placement_strategy: The task placement strategy for a task or service.
            :param platform_version: Specifies the platform version for the task. Specify only the numeric portion of the platform version, such as ``1.1.0`` .
            :param propagate_tags: Specifies whether to propagate the tags from the task definition to the task. If no value is specified, the tags are not propagated. Tags can only be propagated to the task during task creation. To add tags to a task after task creation, use Amazon ECS's ```TagResource`` <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_TagResource.html>`_ API action.
            :param reference_id: The reference ID to use for the task.
            :param tags: The metadata that you apply to the task to help you categorize and organize them. Each tag consists of a key and an optional value, both of which you define. For more information, see ```RunTask`` <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RunTask.html>`_ in the *Amazon ECS API Reference* .
            :param task_count: The number of tasks to create based on ``TaskDefinition`` . The default is ``1`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_scheduler as scheduler
                
                # tags: Any
                
                ecs_parameters_property = scheduler.CfnSchedule.EcsParametersProperty(
                    task_definition_arn="taskDefinitionArn",
                
                    # the properties below are optional
                    capacity_provider_strategy=[scheduler.CfnSchedule.CapacityProviderStrategyItemProperty(
                        capacity_provider="capacityProvider",
                
                        # the properties below are optional
                        base=123,
                        weight=123
                    )],
                    enable_ecs_managed_tags=False,
                    enable_execute_command=False,
                    group="group",
                    launch_type="launchType",
                    network_configuration=scheduler.CfnSchedule.NetworkConfigurationProperty(
                        awsvpc_configuration=scheduler.CfnSchedule.AwsVpcConfigurationProperty(
                            subnets=["subnets"],
                
                            # the properties below are optional
                            assign_public_ip="assignPublicIp",
                            security_groups=["securityGroups"]
                        )
                    ),
                    placement_constraints=[scheduler.CfnSchedule.PlacementConstraintProperty(
                        expression="expression",
                        type="type"
                    )],
                    placement_strategy=[scheduler.CfnSchedule.PlacementStrategyProperty(
                        field="field",
                        type="type"
                    )],
                    platform_version="platformVersion",
                    propagate_tags="propagateTags",
                    reference_id="referenceId",
                    tags=tags,
                    task_count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bee2b77d2eede76b62c7d9fd6ecaff48ad9a378da5b76824ccb60ada39e79d19)
                check_type(argname="argument task_definition_arn", value=task_definition_arn, expected_type=type_hints["task_definition_arn"])
                check_type(argname="argument capacity_provider_strategy", value=capacity_provider_strategy, expected_type=type_hints["capacity_provider_strategy"])
                check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
                check_type(argname="argument enable_execute_command", value=enable_execute_command, expected_type=type_hints["enable_execute_command"])
                check_type(argname="argument group", value=group, expected_type=type_hints["group"])
                check_type(argname="argument launch_type", value=launch_type, expected_type=type_hints["launch_type"])
                check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
                check_type(argname="argument placement_constraints", value=placement_constraints, expected_type=type_hints["placement_constraints"])
                check_type(argname="argument placement_strategy", value=placement_strategy, expected_type=type_hints["placement_strategy"])
                check_type(argname="argument platform_version", value=platform_version, expected_type=type_hints["platform_version"])
                check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
                check_type(argname="argument reference_id", value=reference_id, expected_type=type_hints["reference_id"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                check_type(argname="argument task_count", value=task_count, expected_type=type_hints["task_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "task_definition_arn": task_definition_arn,
            }
            if capacity_provider_strategy is not None:
                self._values["capacity_provider_strategy"] = capacity_provider_strategy
            if enable_ecs_managed_tags is not None:
                self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
            if enable_execute_command is not None:
                self._values["enable_execute_command"] = enable_execute_command
            if group is not None:
                self._values["group"] = group
            if launch_type is not None:
                self._values["launch_type"] = launch_type
            if network_configuration is not None:
                self._values["network_configuration"] = network_configuration
            if placement_constraints is not None:
                self._values["placement_constraints"] = placement_constraints
            if placement_strategy is not None:
                self._values["placement_strategy"] = placement_strategy
            if platform_version is not None:
                self._values["platform_version"] = platform_version
            if propagate_tags is not None:
                self._values["propagate_tags"] = propagate_tags
            if reference_id is not None:
                self._values["reference_id"] = reference_id
            if tags is not None:
                self._values["tags"] = tags
            if task_count is not None:
                self._values["task_count"] = task_count

        @builtins.property
        def task_definition_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the task definition to use if the event target is an Amazon ECS task.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-taskdefinitionarn
            '''
            result = self._values.get("task_definition_arn")
            assert result is not None, "Required property 'task_definition_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def capacity_provider_strategy(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSchedule.CapacityProviderStrategyItemProperty", _IResolvable_a771d0ef]]]]:
            '''The capacity provider strategy to use for the task.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-capacityproviderstrategy
            '''
            result = self._values.get("capacity_provider_strategy")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSchedule.CapacityProviderStrategyItemProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def enable_ecs_managed_tags(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether to enable Amazon ECS managed tags for the task.

            For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ in the *Amazon ECS Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-enableecsmanagedtags
            '''
            result = self._values.get("enable_ecs_managed_tags")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def enable_execute_command(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Whether or not to enable the execute command functionality for the containers in this task.

            If true, this enables execute command functionality on all containers in the task.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-enableexecutecommand
            '''
            result = self._values.get("enable_execute_command")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def group(self) -> typing.Optional[builtins.str]:
            '''Specifies an ECS task group for the task.

            The maximum length is 255 characters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-group
            '''
            result = self._values.get("group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def launch_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the launch type on which your task is running.

            The launch type that you specify here must match one of the launch type (compatibilities) of the target task. The ``FARGATE`` value is supported only in the Regions where Fargate with Amazon ECS is supported. For more information, see `AWS Fargate on Amazon ECS <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html>`_ in the *Amazon ECS Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-launchtype
            '''
            result = self._values.get("launch_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def network_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnSchedule.NetworkConfigurationProperty", _IResolvable_a771d0ef]]:
            '''This structure specifies the network configuration for an ECS task.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-networkconfiguration
            '''
            result = self._values.get("network_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnSchedule.NetworkConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def placement_constraints(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSchedule.PlacementConstraintProperty", _IResolvable_a771d0ef]]]]:
            '''An array of placement constraint objects to use for the task.

            You can specify up to 10 constraints per task (including constraints in the task definition and those specified at runtime).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-placementconstraints
            '''
            result = self._values.get("placement_constraints")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSchedule.PlacementConstraintProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def placement_strategy(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSchedule.PlacementStrategyProperty", _IResolvable_a771d0ef]]]]:
            '''The task placement strategy for a task or service.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-placementstrategy
            '''
            result = self._values.get("placement_strategy")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSchedule.PlacementStrategyProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def platform_version(self) -> typing.Optional[builtins.str]:
            '''Specifies the platform version for the task.

            Specify only the numeric portion of the platform version, such as ``1.1.0`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-platformversion
            '''
            result = self._values.get("platform_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def propagate_tags(self) -> typing.Optional[builtins.str]:
            '''Specifies whether to propagate the tags from the task definition to the task.

            If no value is specified, the tags are not propagated. Tags can only be propagated to the task during task creation. To add tags to a task after task creation, use Amazon ECS's ```TagResource`` <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_TagResource.html>`_ API action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-propagatetags
            '''
            result = self._values.get("propagate_tags")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def reference_id(self) -> typing.Optional[builtins.str]:
            '''The reference ID to use for the task.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-referenceid
            '''
            result = self._values.get("reference_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Any:
            '''The metadata that you apply to the task to help you categorize and organize them.

            Each tag consists of a key and an optional value, both of which you define. For more information, see ```RunTask`` <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RunTask.html>`_ in the *Amazon ECS API Reference* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Any, result)

        @builtins.property
        def task_count(self) -> typing.Optional[jsii.Number]:
            '''The number of tasks to create based on ``TaskDefinition`` .

            The default is ``1`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-taskcount
            '''
            result = self._values.get("task_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EcsParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_scheduler.CfnSchedule.EventBridgeParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"detail_type": "detailType", "source": "source"},
    )
    class EventBridgeParametersProperty:
        def __init__(self, *, detail_type: builtins.str, source: builtins.str) -> None:
            '''The templated target type for the EventBridge ```PutEvents`` <https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_PutEvents.html>`_ API operation.

            :param detail_type: A free-form string, with a maximum of 128 characters, used to decide what fields to expect in the event detail.
            :param source: The source of the event.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-eventbridgeparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_scheduler as scheduler
                
                event_bridge_parameters_property = scheduler.CfnSchedule.EventBridgeParametersProperty(
                    detail_type="detailType",
                    source="source"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8ee4e46b7639be7337b8bd2fb7592eb7839f4b6e0e79eb8589a174e966fb1ca7)
                check_type(argname="argument detail_type", value=detail_type, expected_type=type_hints["detail_type"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "detail_type": detail_type,
                "source": source,
            }

        @builtins.property
        def detail_type(self) -> builtins.str:
            '''A free-form string, with a maximum of 128 characters, used to decide what fields to expect in the event detail.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-eventbridgeparameters.html#cfn-scheduler-schedule-eventbridgeparameters-detailtype
            '''
            result = self._values.get("detail_type")
            assert result is not None, "Required property 'detail_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def source(self) -> builtins.str:
            '''The source of the event.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-eventbridgeparameters.html#cfn-scheduler-schedule-eventbridgeparameters-source
            '''
            result = self._values.get("source")
            assert result is not None, "Required property 'source' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventBridgeParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_scheduler.CfnSchedule.FlexibleTimeWindowProperty",
        jsii_struct_bases=[],
        name_mapping={
            "mode": "mode",
            "maximum_window_in_minutes": "maximumWindowInMinutes",
        },
    )
    class FlexibleTimeWindowProperty:
        def __init__(
            self,
            *,
            mode: builtins.str,
            maximum_window_in_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Allows you to configure a time window during which EventBridge Scheduler invokes the schedule.

            :param mode: Determines whether the schedule is invoked within a flexible time window.
            :param maximum_window_in_minutes: The maximum time window during which a schedule can be invoked.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-flexibletimewindow.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_scheduler as scheduler
                
                flexible_time_window_property = scheduler.CfnSchedule.FlexibleTimeWindowProperty(
                    mode="mode",
                
                    # the properties below are optional
                    maximum_window_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5d25303acf371eef953fcb4ea616ae40fec667a390dc1d497c07297bf5b5ccb2)
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument maximum_window_in_minutes", value=maximum_window_in_minutes, expected_type=type_hints["maximum_window_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "mode": mode,
            }
            if maximum_window_in_minutes is not None:
                self._values["maximum_window_in_minutes"] = maximum_window_in_minutes

        @builtins.property
        def mode(self) -> builtins.str:
            '''Determines whether the schedule is invoked within a flexible time window.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-flexibletimewindow.html#cfn-scheduler-schedule-flexibletimewindow-mode
            '''
            result = self._values.get("mode")
            assert result is not None, "Required property 'mode' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def maximum_window_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''The maximum time window during which a schedule can be invoked.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-flexibletimewindow.html#cfn-scheduler-schedule-flexibletimewindow-maximumwindowinminutes
            '''
            result = self._values.get("maximum_window_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FlexibleTimeWindowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_scheduler.CfnSchedule.KinesisParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"partition_key": "partitionKey"},
    )
    class KinesisParametersProperty:
        def __init__(self, *, partition_key: builtins.str) -> None:
            '''The templated target type for the Amazon Kinesis ```PutRecord`` <https://docs.aws.amazon.com/kinesis/latest/APIReference/API_PutRecord.html>`_ API operation.

            :param partition_key: Specifies the shard to which EventBridge Scheduler sends the event. For more information, see `Amazon Kinesis Data Streams terminology and concepts <https://docs.aws.amazon.com/streams/latest/dev/key-concepts.html>`_ in the *Amazon Kinesis Streams Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-kinesisparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_scheduler as scheduler
                
                kinesis_parameters_property = scheduler.CfnSchedule.KinesisParametersProperty(
                    partition_key="partitionKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8cdb752470c4493a28f555cd5e2a76b04c31a58ed13ef744a265832a88b2c00e)
                check_type(argname="argument partition_key", value=partition_key, expected_type=type_hints["partition_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "partition_key": partition_key,
            }

        @builtins.property
        def partition_key(self) -> builtins.str:
            '''Specifies the shard to which EventBridge Scheduler sends the event.

            For more information, see `Amazon Kinesis Data Streams terminology and concepts <https://docs.aws.amazon.com/streams/latest/dev/key-concepts.html>`_ in the *Amazon Kinesis Streams Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-kinesisparameters.html#cfn-scheduler-schedule-kinesisparameters-partitionkey
            '''
            result = self._values.get("partition_key")
            assert result is not None, "Required property 'partition_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_scheduler.CfnSchedule.NetworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"awsvpc_configuration": "awsvpcConfiguration"},
    )
    class NetworkConfigurationProperty:
        def __init__(
            self,
            *,
            awsvpc_configuration: typing.Optional[typing.Union[typing.Union["CfnSchedule.AwsVpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Specifies the network configuration for an ECS task.

            :param awsvpc_configuration: Specifies the Amazon VPC subnets and security groups for the task, and whether a public IP address is to be used. This structure is relevant only for ECS tasks that use the awsvpc network mode.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-networkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_scheduler as scheduler
                
                network_configuration_property = scheduler.CfnSchedule.NetworkConfigurationProperty(
                    awsvpc_configuration=scheduler.CfnSchedule.AwsVpcConfigurationProperty(
                        subnets=["subnets"],
                
                        # the properties below are optional
                        assign_public_ip="assignPublicIp",
                        security_groups=["securityGroups"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__00093e1209f3580a829ede9128bbdc04080a9370894bd4a504047c0cad72e827)
                check_type(argname="argument awsvpc_configuration", value=awsvpc_configuration, expected_type=type_hints["awsvpc_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if awsvpc_configuration is not None:
                self._values["awsvpc_configuration"] = awsvpc_configuration

        @builtins.property
        def awsvpc_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnSchedule.AwsVpcConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Specifies the Amazon VPC subnets and security groups for the task, and whether a public IP address is to be used.

            This structure is relevant only for ECS tasks that use the awsvpc network mode.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-networkconfiguration.html#cfn-scheduler-schedule-networkconfiguration-awsvpcconfiguration
            '''
            result = self._values.get("awsvpc_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnSchedule.AwsVpcConfigurationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_scheduler.CfnSchedule.PlacementConstraintProperty",
        jsii_struct_bases=[],
        name_mapping={"expression": "expression", "type": "type"},
    )
    class PlacementConstraintProperty:
        def __init__(
            self,
            *,
            expression: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object representing a constraint on task placement.

            :param expression: A cluster query language expression to apply to the constraint. You cannot specify an expression if the constraint type is ``distinctInstance`` . For more information, see `Cluster query language <https://docs.aws.amazon.com/latest/developerguide/cluster-query-language.html>`_ in the *Amazon ECS Developer Guide* .
            :param type: The type of constraint. Use ``distinctInstance`` to ensure that each task in a particular group is running on a different container instance. Use ``memberOf`` to restrict the selection to a group of valid candidates.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-placementconstraint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_scheduler as scheduler
                
                placement_constraint_property = scheduler.CfnSchedule.PlacementConstraintProperty(
                    expression="expression",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__81c037f8838131e456502a260915f03019b9605a6e75d659994d1526155e1bd2)
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if expression is not None:
                self._values["expression"] = expression
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''A cluster query language expression to apply to the constraint.

            You cannot specify an expression if the constraint type is ``distinctInstance`` . For more information, see `Cluster query language <https://docs.aws.amazon.com/latest/developerguide/cluster-query-language.html>`_ in the *Amazon ECS Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-placementconstraint.html#cfn-scheduler-schedule-placementconstraint-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of constraint.

            Use ``distinctInstance`` to ensure that each task in a particular group is running on a different container instance. Use ``memberOf`` to restrict the selection to a group of valid candidates.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-placementconstraint.html#cfn-scheduler-schedule-placementconstraint-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PlacementConstraintProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_scheduler.CfnSchedule.PlacementStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={"field": "field", "type": "type"},
    )
    class PlacementStrategyProperty:
        def __init__(
            self,
            *,
            field: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The task placement strategy for a task or service.

            :param field: The field to apply the placement strategy against. For the spread placement strategy, valid values are ``instanceId`` (or ``instanceId`` , which has the same effect), or any platform or custom attribute that is applied to a container instance, such as ``attribute:ecs.availability-zone`` . For the binpack placement strategy, valid values are ``cpu`` and ``memory`` . For the random placement strategy, this field is not used.
            :param type: The type of placement strategy. The random placement strategy randomly places tasks on available candidates. The spread placement strategy spreads placement across available candidates evenly based on the field parameter. The binpack strategy places tasks on available candidates that have the least available amount of the resource that is specified with the field parameter. For example, if you binpack on memory, a task is placed on the instance with the least amount of remaining memory (but still enough to run the task).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-placementstrategy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_scheduler as scheduler
                
                placement_strategy_property = scheduler.CfnSchedule.PlacementStrategyProperty(
                    field="field",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__32c4a7bbcc4688067a1c96a1deab245e332f399229064717b459c7e1335b24cf)
                check_type(argname="argument field", value=field, expected_type=type_hints["field"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if field is not None:
                self._values["field"] = field
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''The field to apply the placement strategy against.

            For the spread placement strategy, valid values are ``instanceId`` (or ``instanceId`` , which has the same effect), or any platform or custom attribute that is applied to a container instance, such as ``attribute:ecs.availability-zone`` . For the binpack placement strategy, valid values are ``cpu`` and ``memory`` . For the random placement strategy, this field is not used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-placementstrategy.html#cfn-scheduler-schedule-placementstrategy-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of placement strategy.

            The random placement strategy randomly places tasks on available candidates. The spread placement strategy spreads placement across available candidates evenly based on the field parameter. The binpack strategy places tasks on available candidates that have the least available amount of the resource that is specified with the field parameter. For example, if you binpack on memory, a task is placed on the instance with the least amount of remaining memory (but still enough to run the task).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-placementstrategy.html#cfn-scheduler-schedule-placementstrategy-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PlacementStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_scheduler.CfnSchedule.RetryPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "maximum_event_age_in_seconds": "maximumEventAgeInSeconds",
            "maximum_retry_attempts": "maximumRetryAttempts",
        },
    )
    class RetryPolicyProperty:
        def __init__(
            self,
            *,
            maximum_event_age_in_seconds: typing.Optional[jsii.Number] = None,
            maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A ``RetryPolicy`` object that includes information about the retry policy settings, including the maximum age of an event, and the maximum number of times EventBridge Scheduler will try to deliver the event to a target.

            :param maximum_event_age_in_seconds: The maximum amount of time, in seconds, to continue to make retry attempts.
            :param maximum_retry_attempts: The maximum number of retry attempts to make before the request fails. Retry attempts with exponential backoff continue until either the maximum number of attempts is made or until the duration of the ``MaximumEventAgeInSeconds`` is reached.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-retrypolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_scheduler as scheduler
                
                retry_policy_property = scheduler.CfnSchedule.RetryPolicyProperty(
                    maximum_event_age_in_seconds=123,
                    maximum_retry_attempts=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dfb0667ad24dd6235b5f2ed312caa77e1f701ec45ef9ede29e44392f15aac03c)
                check_type(argname="argument maximum_event_age_in_seconds", value=maximum_event_age_in_seconds, expected_type=type_hints["maximum_event_age_in_seconds"])
                check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if maximum_event_age_in_seconds is not None:
                self._values["maximum_event_age_in_seconds"] = maximum_event_age_in_seconds
            if maximum_retry_attempts is not None:
                self._values["maximum_retry_attempts"] = maximum_retry_attempts

        @builtins.property
        def maximum_event_age_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of time, in seconds, to continue to make retry attempts.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-retrypolicy.html#cfn-scheduler-schedule-retrypolicy-maximumeventageinseconds
            '''
            result = self._values.get("maximum_event_age_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of retry attempts to make before the request fails.

            Retry attempts with exponential backoff continue until either the maximum number of attempts is made or until the duration of the ``MaximumEventAgeInSeconds`` is reached.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-retrypolicy.html#cfn-scheduler-schedule-retrypolicy-maximumretryattempts
            '''
            result = self._values.get("maximum_retry_attempts")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetryPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_scheduler.CfnSchedule.SageMakerPipelineParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class SageMakerPipelineParameterProperty:
        def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
            '''The name and value pair of a parameter to use to start execution of a SageMaker Model Building Pipeline.

            :param name: Name of parameter to start execution of a SageMaker Model Building Pipeline.
            :param value: Value of parameter to start execution of a SageMaker Model Building Pipeline.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-sagemakerpipelineparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_scheduler as scheduler
                
                sage_maker_pipeline_parameter_property = scheduler.CfnSchedule.SageMakerPipelineParameterProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__26cf77be3f215b6615f2fb1468417b3d4d349010bdd2e944d2328e29ca7e1a6d)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''Name of parameter to start execution of a SageMaker Model Building Pipeline.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-sagemakerpipelineparameter.html#cfn-scheduler-schedule-sagemakerpipelineparameter-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''Value of parameter to start execution of a SageMaker Model Building Pipeline.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-sagemakerpipelineparameter.html#cfn-scheduler-schedule-sagemakerpipelineparameter-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SageMakerPipelineParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_scheduler.CfnSchedule.SageMakerPipelineParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"pipeline_parameter_list": "pipelineParameterList"},
    )
    class SageMakerPipelineParametersProperty:
        def __init__(
            self,
            *,
            pipeline_parameter_list: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnSchedule.SageMakerPipelineParameterProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''The templated target type for the Amazon SageMaker ```StartPipelineExecution`` <https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_StartPipelineExecution.html>`_ API operation.

            :param pipeline_parameter_list: List of parameter names and values to use when executing the SageMaker Model Building Pipeline.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-sagemakerpipelineparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_scheduler as scheduler
                
                sage_maker_pipeline_parameters_property = scheduler.CfnSchedule.SageMakerPipelineParametersProperty(
                    pipeline_parameter_list=[scheduler.CfnSchedule.SageMakerPipelineParameterProperty(
                        name="name",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__581d39e5eac9471e9771cc9718d3cd5dd71491fa62429a05fb92fb135366f23d)
                check_type(argname="argument pipeline_parameter_list", value=pipeline_parameter_list, expected_type=type_hints["pipeline_parameter_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if pipeline_parameter_list is not None:
                self._values["pipeline_parameter_list"] = pipeline_parameter_list

        @builtins.property
        def pipeline_parameter_list(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSchedule.SageMakerPipelineParameterProperty", _IResolvable_a771d0ef]]]]:
            '''List of parameter names and values to use when executing the SageMaker Model Building Pipeline.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-sagemakerpipelineparameters.html#cfn-scheduler-schedule-sagemakerpipelineparameters-pipelineparameterlist
            '''
            result = self._values.get("pipeline_parameter_list")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSchedule.SageMakerPipelineParameterProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SageMakerPipelineParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_scheduler.CfnSchedule.SqsParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"message_group_id": "messageGroupId"},
    )
    class SqsParametersProperty:
        def __init__(
            self,
            *,
            message_group_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The templated target type for the Amazon SQS ```SendMessage`` <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SendMessage.html>`_ API operation. Contains the message group ID to use when the target is a FIFO queue. If you specify an Amazon SQS FIFO queue as a target, the queue must have content-based deduplication enabled. For more information, see `Using the Amazon SQS message deduplication ID <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/using-messagededuplicationid-property.html>`_ in the *Amazon SQS Developer Guide* .

            :param message_group_id: The FIFO message group ID to use as the target.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-sqsparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_scheduler as scheduler
                
                sqs_parameters_property = scheduler.CfnSchedule.SqsParametersProperty(
                    message_group_id="messageGroupId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a0c054234ca511d7dbcef12644289d5976f2ed75dae77cf2a2b7cd56bd83f609)
                check_type(argname="argument message_group_id", value=message_group_id, expected_type=type_hints["message_group_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if message_group_id is not None:
                self._values["message_group_id"] = message_group_id

        @builtins.property
        def message_group_id(self) -> typing.Optional[builtins.str]:
            '''The FIFO message group ID to use as the target.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-sqsparameters.html#cfn-scheduler-schedule-sqsparameters-messagegroupid
            '''
            result = self._values.get("message_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SqsParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_scheduler.CfnSchedule.TargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "role_arn": "roleArn",
            "dead_letter_config": "deadLetterConfig",
            "ecs_parameters": "ecsParameters",
            "event_bridge_parameters": "eventBridgeParameters",
            "input": "input",
            "kinesis_parameters": "kinesisParameters",
            "retry_policy": "retryPolicy",
            "sage_maker_pipeline_parameters": "sageMakerPipelineParameters",
            "sqs_parameters": "sqsParameters",
        },
    )
    class TargetProperty:
        def __init__(
            self,
            *,
            arn: builtins.str,
            role_arn: builtins.str,
            dead_letter_config: typing.Optional[typing.Union[typing.Union["CfnSchedule.DeadLetterConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            ecs_parameters: typing.Optional[typing.Union[typing.Union["CfnSchedule.EcsParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            event_bridge_parameters: typing.Optional[typing.Union[typing.Union["CfnSchedule.EventBridgeParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            input: typing.Optional[builtins.str] = None,
            kinesis_parameters: typing.Optional[typing.Union[typing.Union["CfnSchedule.KinesisParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            retry_policy: typing.Optional[typing.Union[typing.Union["CfnSchedule.RetryPolicyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sage_maker_pipeline_parameters: typing.Optional[typing.Union[typing.Union["CfnSchedule.SageMakerPipelineParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sqs_parameters: typing.Optional[typing.Union[typing.Union["CfnSchedule.SqsParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The schedule's target.

            EventBridge Scheduler supports templated target that invoke common API operations, as well as universal targets that you can customize to invoke over 6,000 API operations across more than 270 services. You can only specify one templated or universal target for a schedule.

            :param arn: The Amazon Resource Name (ARN) of the target.
            :param role_arn: The Amazon Resource Name (ARN) of the IAM role that EventBridge Scheduler will use for this target when the schedule is invoked.
            :param dead_letter_config: An object that contains information about an Amazon SQS queue that EventBridge Scheduler uses as a dead-letter queue for your schedule. If specified, EventBridge Scheduler delivers failed events that could not be successfully delivered to a target to the queue.
            :param ecs_parameters: The templated target type for the Amazon ECS ```RunTask`` <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RunTask.html>`_ API operation.
            :param event_bridge_parameters: The templated target type for the EventBridge ```PutEvents`` <https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_PutEvents.html>`_ API operation.
            :param input: The text, or well-formed JSON, passed to the target. If you are configuring a templated Lambda , AWS Step Functions , or Amazon EventBridge target, the input must be a well-formed JSON. For all other target types, a JSON is not required. If you do not specify anything for this field, Amazon EventBridge Scheduler delivers a default notification to the target.
            :param kinesis_parameters: The templated target type for the Amazon Kinesis ```PutRecord`` <https://docs.aws.amazon.com/kinesis/latest/APIReference/API_PutRecord.html>`_ API operation.
            :param retry_policy: A ``RetryPolicy`` object that includes information about the retry policy settings, including the maximum age of an event, and the maximum number of times EventBridge Scheduler will try to deliver the event to a target.
            :param sage_maker_pipeline_parameters: The templated target type for the Amazon SageMaker ```StartPipelineExecution`` <https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_StartPipelineExecution.html>`_ API operation.
            :param sqs_parameters: The templated target type for the Amazon SQS ```SendMessage`` <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SendMessage.html>`_ API operation. Contains the message group ID to use when the target is a FIFO queue. If you specify an Amazon SQS FIFO queue as a target, the queue must have content-based deduplication enabled. For more information, see `Using the Amazon SQS message deduplication ID <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/using-messagededuplicationid-property.html>`_ in the *Amazon SQS Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_scheduler as scheduler
                
                # tags: Any
                
                target_property = scheduler.CfnSchedule.TargetProperty(
                    arn="arn",
                    role_arn="roleArn",
                
                    # the properties below are optional
                    dead_letter_config=scheduler.CfnSchedule.DeadLetterConfigProperty(
                        arn="arn"
                    ),
                    ecs_parameters=scheduler.CfnSchedule.EcsParametersProperty(
                        task_definition_arn="taskDefinitionArn",
                
                        # the properties below are optional
                        capacity_provider_strategy=[scheduler.CfnSchedule.CapacityProviderStrategyItemProperty(
                            capacity_provider="capacityProvider",
                
                            # the properties below are optional
                            base=123,
                            weight=123
                        )],
                        enable_ecs_managed_tags=False,
                        enable_execute_command=False,
                        group="group",
                        launch_type="launchType",
                        network_configuration=scheduler.CfnSchedule.NetworkConfigurationProperty(
                            awsvpc_configuration=scheduler.CfnSchedule.AwsVpcConfigurationProperty(
                                subnets=["subnets"],
                
                                # the properties below are optional
                                assign_public_ip="assignPublicIp",
                                security_groups=["securityGroups"]
                            )
                        ),
                        placement_constraints=[scheduler.CfnSchedule.PlacementConstraintProperty(
                            expression="expression",
                            type="type"
                        )],
                        placement_strategy=[scheduler.CfnSchedule.PlacementStrategyProperty(
                            field="field",
                            type="type"
                        )],
                        platform_version="platformVersion",
                        propagate_tags="propagateTags",
                        reference_id="referenceId",
                        tags=tags,
                        task_count=123
                    ),
                    event_bridge_parameters=scheduler.CfnSchedule.EventBridgeParametersProperty(
                        detail_type="detailType",
                        source="source"
                    ),
                    input="input",
                    kinesis_parameters=scheduler.CfnSchedule.KinesisParametersProperty(
                        partition_key="partitionKey"
                    ),
                    retry_policy=scheduler.CfnSchedule.RetryPolicyProperty(
                        maximum_event_age_in_seconds=123,
                        maximum_retry_attempts=123
                    ),
                    sage_maker_pipeline_parameters=scheduler.CfnSchedule.SageMakerPipelineParametersProperty(
                        pipeline_parameter_list=[scheduler.CfnSchedule.SageMakerPipelineParameterProperty(
                            name="name",
                            value="value"
                        )]
                    ),
                    sqs_parameters=scheduler.CfnSchedule.SqsParametersProperty(
                        message_group_id="messageGroupId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e9918e491b65b371b1f7d9ebb0db09163f31e22e918415c531618993961d2c05)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument dead_letter_config", value=dead_letter_config, expected_type=type_hints["dead_letter_config"])
                check_type(argname="argument ecs_parameters", value=ecs_parameters, expected_type=type_hints["ecs_parameters"])
                check_type(argname="argument event_bridge_parameters", value=event_bridge_parameters, expected_type=type_hints["event_bridge_parameters"])
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument kinesis_parameters", value=kinesis_parameters, expected_type=type_hints["kinesis_parameters"])
                check_type(argname="argument retry_policy", value=retry_policy, expected_type=type_hints["retry_policy"])
                check_type(argname="argument sage_maker_pipeline_parameters", value=sage_maker_pipeline_parameters, expected_type=type_hints["sage_maker_pipeline_parameters"])
                check_type(argname="argument sqs_parameters", value=sqs_parameters, expected_type=type_hints["sqs_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "arn": arn,
                "role_arn": role_arn,
            }
            if dead_letter_config is not None:
                self._values["dead_letter_config"] = dead_letter_config
            if ecs_parameters is not None:
                self._values["ecs_parameters"] = ecs_parameters
            if event_bridge_parameters is not None:
                self._values["event_bridge_parameters"] = event_bridge_parameters
            if input is not None:
                self._values["input"] = input
            if kinesis_parameters is not None:
                self._values["kinesis_parameters"] = kinesis_parameters
            if retry_policy is not None:
                self._values["retry_policy"] = retry_policy
            if sage_maker_pipeline_parameters is not None:
                self._values["sage_maker_pipeline_parameters"] = sage_maker_pipeline_parameters
            if sqs_parameters is not None:
                self._values["sqs_parameters"] = sqs_parameters

        @builtins.property
        def arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the target.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html#cfn-scheduler-schedule-target-arn
            '''
            result = self._values.get("arn")
            assert result is not None, "Required property 'arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def role_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the IAM role that EventBridge Scheduler will use for this target when the schedule is invoked.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html#cfn-scheduler-schedule-target-rolearn
            '''
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def dead_letter_config(
            self,
        ) -> typing.Optional[typing.Union["CfnSchedule.DeadLetterConfigProperty", _IResolvable_a771d0ef]]:
            '''An object that contains information about an Amazon SQS queue that EventBridge Scheduler uses as a dead-letter queue for your schedule.

            If specified, EventBridge Scheduler delivers failed events that could not be successfully delivered to a target to the queue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html#cfn-scheduler-schedule-target-deadletterconfig
            '''
            result = self._values.get("dead_letter_config")
            return typing.cast(typing.Optional[typing.Union["CfnSchedule.DeadLetterConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def ecs_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnSchedule.EcsParametersProperty", _IResolvable_a771d0ef]]:
            '''The templated target type for the Amazon ECS ```RunTask`` <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RunTask.html>`_ API operation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html#cfn-scheduler-schedule-target-ecsparameters
            '''
            result = self._values.get("ecs_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnSchedule.EcsParametersProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def event_bridge_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnSchedule.EventBridgeParametersProperty", _IResolvable_a771d0ef]]:
            '''The templated target type for the EventBridge ```PutEvents`` <https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_PutEvents.html>`_ API operation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html#cfn-scheduler-schedule-target-eventbridgeparameters
            '''
            result = self._values.get("event_bridge_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnSchedule.EventBridgeParametersProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''The text, or well-formed JSON, passed to the target.

            If you are configuring a templated Lambda , AWS Step Functions , or Amazon EventBridge target, the input must be a well-formed JSON. For all other target types, a JSON is not required. If you do not specify anything for this field, Amazon EventBridge Scheduler delivers a default notification to the target.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html#cfn-scheduler-schedule-target-input
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kinesis_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnSchedule.KinesisParametersProperty", _IResolvable_a771d0ef]]:
            '''The templated target type for the Amazon Kinesis ```PutRecord`` <https://docs.aws.amazon.com/kinesis/latest/APIReference/API_PutRecord.html>`_ API operation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html#cfn-scheduler-schedule-target-kinesisparameters
            '''
            result = self._values.get("kinesis_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnSchedule.KinesisParametersProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def retry_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnSchedule.RetryPolicyProperty", _IResolvable_a771d0ef]]:
            '''A ``RetryPolicy`` object that includes information about the retry policy settings, including the maximum age of an event, and the maximum number of times EventBridge Scheduler will try to deliver the event to a target.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html#cfn-scheduler-schedule-target-retrypolicy
            '''
            result = self._values.get("retry_policy")
            return typing.cast(typing.Optional[typing.Union["CfnSchedule.RetryPolicyProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sage_maker_pipeline_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnSchedule.SageMakerPipelineParametersProperty", _IResolvable_a771d0ef]]:
            '''The templated target type for the Amazon SageMaker ```StartPipelineExecution`` <https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_StartPipelineExecution.html>`_ API operation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html#cfn-scheduler-schedule-target-sagemakerpipelineparameters
            '''
            result = self._values.get("sage_maker_pipeline_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnSchedule.SageMakerPipelineParametersProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sqs_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnSchedule.SqsParametersProperty", _IResolvable_a771d0ef]]:
            '''The templated target type for the Amazon SQS ```SendMessage`` <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SendMessage.html>`_ API operation. Contains the message group ID to use when the target is a FIFO queue. If you specify an Amazon SQS FIFO queue as a target, the queue must have content-based deduplication enabled. For more information, see `Using the Amazon SQS message deduplication ID <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/using-messagededuplicationid-property.html>`_ in the *Amazon SQS Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html#cfn-scheduler-schedule-target-sqsparameters
            '''
            result = self._values.get("sqs_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnSchedule.SqsParametersProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnScheduleGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_scheduler.CfnScheduleGroup",
):
    '''A CloudFormation ``AWS::Scheduler::ScheduleGroup``.

    Creates the specified schedule group.

    :cloudformationResource: AWS::Scheduler::ScheduleGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedulegroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_scheduler as scheduler
        
        cfn_schedule_group = scheduler.CfnScheduleGroup(self, "MyCfnScheduleGroup",
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Scheduler::ScheduleGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the schedule group.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__007dc3664db15a99a7704fb24b138d5b020e0cad6dba4713c2dadc85c55780a7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnScheduleGroupProps(name=name, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b58e44d39f54fd63a80956274e514a5b974a169fcdd7311df1f9e7548b4a5e7f)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__603fe8a75d7fe90e5c37ad9fbfeff0a8b70b875298175cbd8e16368ac0dbb3e3)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the schedule group.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationDate")
    def attr_creation_date(self) -> builtins.str:
        '''The date and time at which the schedule group was created.

        :cloudformationAttribute: CreationDate
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationDate"))

    @builtins.property
    @jsii.member(jsii_name="attrLastModificationDate")
    def attr_last_modification_date(self) -> builtins.str:
        '''The time at which the schedule group was last modified.

        :cloudformationAttribute: LastModificationDate
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastModificationDate"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''Specifies the state of the schedule group.

        Valid values are ``ACTIVE`` and ``DELETING`` .

        :cloudformationAttribute: State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedulegroup.html#cfn-scheduler-schedulegroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the schedule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedulegroup.html#cfn-scheduler-schedulegroup-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4932fd926bbd5b6075bfedde89c72142666d1e2b5582f33be7627d57f70995be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="monocdk.aws_scheduler.CfnScheduleGroupProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "tags": "tags"},
)
class CfnScheduleGroupProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnScheduleGroup``.

        :param name: The name of the schedule group.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedulegroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_scheduler as scheduler
            
            cfn_schedule_group_props = scheduler.CfnScheduleGroupProps(
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d506b86484dae30ae1d28b8b9594c2d074240e93001d7bb706d2bd4e9e58cf6)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the schedule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedulegroup.html#cfn-scheduler-schedulegroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedulegroup.html#cfn-scheduler-schedulegroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnScheduleGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_scheduler.CfnScheduleProps",
    jsii_struct_bases=[],
    name_mapping={
        "flexible_time_window": "flexibleTimeWindow",
        "schedule_expression": "scheduleExpression",
        "target": "target",
        "description": "description",
        "end_date": "endDate",
        "group_name": "groupName",
        "kms_key_arn": "kmsKeyArn",
        "name": "name",
        "schedule_expression_timezone": "scheduleExpressionTimezone",
        "start_date": "startDate",
        "state": "state",
    },
)
class CfnScheduleProps:
    def __init__(
        self,
        *,
        flexible_time_window: typing.Union[typing.Union[CfnSchedule.FlexibleTimeWindowProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        schedule_expression: builtins.str,
        target: typing.Union[typing.Union[CfnSchedule.TargetProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        end_date: typing.Optional[builtins.str] = None,
        group_name: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        schedule_expression_timezone: typing.Optional[builtins.str] = None,
        start_date: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnSchedule``.

        :param flexible_time_window: Allows you to configure a time window during which EventBridge Scheduler invokes the schedule.
        :param schedule_expression: The expression that defines when the schedule runs. The following formats are supported. - ``at`` expression - ``at(yyyy-mm-ddThh:mm:ss)`` - ``rate`` expression - ``rate(unit value)`` - ``cron`` expression - ``cron(fields)`` You can use ``at`` expressions to create one-time schedules that invoke a target once, at the time and in the time zone, that you specify. You can use ``rate`` and ``cron`` expressions to create recurring schedules. Rate-based schedules are useful when you want to invoke a target at regular intervals, such as every 15 minutes or every five days. Cron-based schedules are useful when you want to invoke a target periodically at a specific time, such as at 8:00 am (UTC+0) every 1st day of the month. A ``cron`` expression consists of six fields separated by white spaces: ``(minutes hours day_of_month month day_of_week year)`` . A ``rate`` expression consists of a *value* as a positive integer, and a *unit* with the following options: ``minute`` | ``minutes`` | ``hour`` | ``hours`` | ``day`` | ``days`` For more information and examples, see `Schedule types on EventBridge Scheduler <https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html>`_ in the *EventBridge Scheduler User Guide* .
        :param target: The schedule's target details.
        :param description: The description you specify for the schedule.
        :param end_date: The date, in UTC, before which the schedule can invoke its target. Depending on the schedule's recurrence expression, invocations might stop on, or before, the ``EndDate`` you specify. EventBridge Scheduler ignores ``EndDate`` for one-time schedules.
        :param group_name: The name of the schedule group associated with this schedule.
        :param kms_key_arn: The Amazon Resource Name (ARN) for the customer managed KMS key that EventBridge Scheduler will use to encrypt and decrypt your data.
        :param name: The name of the schedule.
        :param schedule_expression_timezone: The timezone in which the scheduling expression is evaluated.
        :param start_date: The date, in UTC, after which the schedule can begin invoking its target. Depending on the schedule's recurrence expression, invocations might occur on, or after, the ``StartDate`` you specify. EventBridge Scheduler ignores ``StartDate`` for one-time schedules.
        :param state: Specifies whether the schedule is enabled or disabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_scheduler as scheduler
            
            # tags: Any
            
            cfn_schedule_props = scheduler.CfnScheduleProps(
                flexible_time_window=scheduler.CfnSchedule.FlexibleTimeWindowProperty(
                    mode="mode",
            
                    # the properties below are optional
                    maximum_window_in_minutes=123
                ),
                schedule_expression="scheduleExpression",
                target=scheduler.CfnSchedule.TargetProperty(
                    arn="arn",
                    role_arn="roleArn",
            
                    # the properties below are optional
                    dead_letter_config=scheduler.CfnSchedule.DeadLetterConfigProperty(
                        arn="arn"
                    ),
                    ecs_parameters=scheduler.CfnSchedule.EcsParametersProperty(
                        task_definition_arn="taskDefinitionArn",
            
                        # the properties below are optional
                        capacity_provider_strategy=[scheduler.CfnSchedule.CapacityProviderStrategyItemProperty(
                            capacity_provider="capacityProvider",
            
                            # the properties below are optional
                            base=123,
                            weight=123
                        )],
                        enable_ecs_managed_tags=False,
                        enable_execute_command=False,
                        group="group",
                        launch_type="launchType",
                        network_configuration=scheduler.CfnSchedule.NetworkConfigurationProperty(
                            awsvpc_configuration=scheduler.CfnSchedule.AwsVpcConfigurationProperty(
                                subnets=["subnets"],
            
                                # the properties below are optional
                                assign_public_ip="assignPublicIp",
                                security_groups=["securityGroups"]
                            )
                        ),
                        placement_constraints=[scheduler.CfnSchedule.PlacementConstraintProperty(
                            expression="expression",
                            type="type"
                        )],
                        placement_strategy=[scheduler.CfnSchedule.PlacementStrategyProperty(
                            field="field",
                            type="type"
                        )],
                        platform_version="platformVersion",
                        propagate_tags="propagateTags",
                        reference_id="referenceId",
                        tags=tags,
                        task_count=123
                    ),
                    event_bridge_parameters=scheduler.CfnSchedule.EventBridgeParametersProperty(
                        detail_type="detailType",
                        source="source"
                    ),
                    input="input",
                    kinesis_parameters=scheduler.CfnSchedule.KinesisParametersProperty(
                        partition_key="partitionKey"
                    ),
                    retry_policy=scheduler.CfnSchedule.RetryPolicyProperty(
                        maximum_event_age_in_seconds=123,
                        maximum_retry_attempts=123
                    ),
                    sage_maker_pipeline_parameters=scheduler.CfnSchedule.SageMakerPipelineParametersProperty(
                        pipeline_parameter_list=[scheduler.CfnSchedule.SageMakerPipelineParameterProperty(
                            name="name",
                            value="value"
                        )]
                    ),
                    sqs_parameters=scheduler.CfnSchedule.SqsParametersProperty(
                        message_group_id="messageGroupId"
                    )
                ),
            
                # the properties below are optional
                description="description",
                end_date="endDate",
                group_name="groupName",
                kms_key_arn="kmsKeyArn",
                name="name",
                schedule_expression_timezone="scheduleExpressionTimezone",
                start_date="startDate",
                state="state"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe5eb4a72b188be355dfc3ddc2c89f9906481853bea2d9ba379098c193072ca6)
            check_type(argname="argument flexible_time_window", value=flexible_time_window, expected_type=type_hints["flexible_time_window"])
            check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument end_date", value=end_date, expected_type=type_hints["end_date"])
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schedule_expression_timezone", value=schedule_expression_timezone, expected_type=type_hints["schedule_expression_timezone"])
            check_type(argname="argument start_date", value=start_date, expected_type=type_hints["start_date"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "flexible_time_window": flexible_time_window,
            "schedule_expression": schedule_expression,
            "target": target,
        }
        if description is not None:
            self._values["description"] = description
        if end_date is not None:
            self._values["end_date"] = end_date
        if group_name is not None:
            self._values["group_name"] = group_name
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if name is not None:
            self._values["name"] = name
        if schedule_expression_timezone is not None:
            self._values["schedule_expression_timezone"] = schedule_expression_timezone
        if start_date is not None:
            self._values["start_date"] = start_date
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def flexible_time_window(
        self,
    ) -> typing.Union[CfnSchedule.FlexibleTimeWindowProperty, _IResolvable_a771d0ef]:
        '''Allows you to configure a time window during which EventBridge Scheduler invokes the schedule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-flexibletimewindow
        '''
        result = self._values.get("flexible_time_window")
        assert result is not None, "Required property 'flexible_time_window' is missing"
        return typing.cast(typing.Union[CfnSchedule.FlexibleTimeWindowProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def schedule_expression(self) -> builtins.str:
        '''The expression that defines when the schedule runs. The following formats are supported.

        - ``at`` expression - ``at(yyyy-mm-ddThh:mm:ss)``
        - ``rate`` expression - ``rate(unit value)``
        - ``cron`` expression - ``cron(fields)``

        You can use ``at`` expressions to create one-time schedules that invoke a target once, at the time and in the time zone, that you specify. You can use ``rate`` and ``cron`` expressions to create recurring schedules. Rate-based schedules are useful when you want to invoke a target at regular intervals, such as every 15 minutes or every five days. Cron-based schedules are useful when you want to invoke a target periodically at a specific time, such as at 8:00 am (UTC+0) every 1st day of the month.

        A ``cron`` expression consists of six fields separated by white spaces: ``(minutes hours day_of_month month day_of_week year)`` .

        A ``rate`` expression consists of a *value* as a positive integer, and a *unit* with the following options: ``minute`` | ``minutes`` | ``hour`` | ``hours`` | ``day`` | ``days``

        For more information and examples, see `Schedule types on EventBridge Scheduler <https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html>`_ in the *EventBridge Scheduler User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-scheduleexpression
        '''
        result = self._values.get("schedule_expression")
        assert result is not None, "Required property 'schedule_expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> typing.Union[CfnSchedule.TargetProperty, _IResolvable_a771d0ef]:
        '''The schedule's target details.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-target
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(typing.Union[CfnSchedule.TargetProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description you specify for the schedule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def end_date(self) -> typing.Optional[builtins.str]:
        '''The date, in UTC, before which the schedule can invoke its target.

        Depending on the schedule's recurrence expression, invocations might stop on, or before, the ``EndDate`` you specify.
        EventBridge Scheduler ignores ``EndDate`` for one-time schedules.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-enddate
        '''
        result = self._values.get("end_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the schedule group associated with this schedule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-groupname
        '''
        result = self._values.get("group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) for the customer managed KMS key that EventBridge Scheduler will use to encrypt and decrypt your data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-kmskeyarn
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the schedule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_expression_timezone(self) -> typing.Optional[builtins.str]:
        '''The timezone in which the scheduling expression is evaluated.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-scheduleexpressiontimezone
        '''
        result = self._values.get("schedule_expression_timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_date(self) -> typing.Optional[builtins.str]:
        '''The date, in UTC, after which the schedule can begin invoking its target.

        Depending on the schedule's recurrence expression, invocations might occur on, or after, the ``StartDate`` you specify.
        EventBridge Scheduler ignores ``StartDate`` for one-time schedules.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-startdate
        '''
        result = self._values.get("start_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the schedule is enabled or disabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnScheduleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnSchedule",
    "CfnScheduleGroup",
    "CfnScheduleGroupProps",
    "CfnScheduleProps",
]

publication.publish()

def _typecheckingstub__ba25e64f746f8fa7a5d1e2d04f5f19027a8b4c994f38b48f449140a19f9372f6(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    flexible_time_window: typing.Union[typing.Union[CfnSchedule.FlexibleTimeWindowProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    schedule_expression: builtins.str,
    target: typing.Union[typing.Union[CfnSchedule.TargetProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    description: typing.Optional[builtins.str] = None,
    end_date: typing.Optional[builtins.str] = None,
    group_name: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    schedule_expression_timezone: typing.Optional[builtins.str] = None,
    start_date: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d9deb64c974ffc04efce7eb9c9ef983ea4725dfd8add3f7cbea81bfa7d4b404(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e4dae299315aa379226601968701041339a2dd79d8be34e07fa0833029784d8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b66cde60fa736ec009451b701de99a70b871d6c1ffa14f8c8bc073efa21ff1b(
    value: typing.Union[CfnSchedule.FlexibleTimeWindowProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44621d34d7b55afbbcf96371376065aadced9f702bf3204b4cef26fed2dacbda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__960d5d92b33ff31984b675c8627c63acd9cc031cb346220fc03103b6c83cb601(
    value: typing.Union[CfnSchedule.TargetProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ca13b10d05e657b7573272b277c975aba40ef419b7dc6f2414bb071606bbe3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a989f59f2bfd6b56fd707171ad3e9bdcf955ea09768d930c6bb6e17bf45b1a3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb4b0b36ba92f25d07fa92f9ef85d0c7370bacc3b782806cc3d7e3e3bf229195(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e074b998485064e1aa888150b0198fd0d15409c0ad990d00ac32c66c5e7403b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__625a6b22966549274dd26f07bcfa0ec61b5a5304809967f04a4dd865e59080f9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9cfd9bcb214d49f0cfc1ce8b9de30755fd7874c752292ff81fc2c364b443cc5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b2c8f214c451833198ae5f74c7c53a850209f0601339becb1bf0ce8c5e03a3d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7971622377d5a373004c4cc2e327711e8125760a902e916a419b40d4b96e6aed(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8396c06a348956ed63f98299f89742fcd10b456cf5223802a1b0b9e5528042ca(
    *,
    subnets: typing.Sequence[builtins.str],
    assign_public_ip: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87a256e51d8558d5c79a90737f7c86d03718da9e44a6199f6613a03ae5dae23(
    *,
    capacity_provider: builtins.str,
    base: typing.Optional[jsii.Number] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f172d16ccf6e4cea837a6343e2aecbdcaee91af772f18fc4e8f393c92261310(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee2b77d2eede76b62c7d9fd6ecaff48ad9a378da5b76824ccb60ada39e79d19(
    *,
    task_definition_arn: builtins.str,
    capacity_provider_strategy: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnSchedule.CapacityProviderStrategyItemProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    enable_ecs_managed_tags: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    enable_execute_command: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    group: typing.Optional[builtins.str] = None,
    launch_type: typing.Optional[builtins.str] = None,
    network_configuration: typing.Optional[typing.Union[typing.Union[CfnSchedule.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    placement_constraints: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnSchedule.PlacementConstraintProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    placement_strategy: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnSchedule.PlacementStrategyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    platform_version: typing.Optional[builtins.str] = None,
    propagate_tags: typing.Optional[builtins.str] = None,
    reference_id: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    task_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee4e46b7639be7337b8bd2fb7592eb7839f4b6e0e79eb8589a174e966fb1ca7(
    *,
    detail_type: builtins.str,
    source: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d25303acf371eef953fcb4ea616ae40fec667a390dc1d497c07297bf5b5ccb2(
    *,
    mode: builtins.str,
    maximum_window_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cdb752470c4493a28f555cd5e2a76b04c31a58ed13ef744a265832a88b2c00e(
    *,
    partition_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00093e1209f3580a829ede9128bbdc04080a9370894bd4a504047c0cad72e827(
    *,
    awsvpc_configuration: typing.Optional[typing.Union[typing.Union[CfnSchedule.AwsVpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c037f8838131e456502a260915f03019b9605a6e75d659994d1526155e1bd2(
    *,
    expression: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32c4a7bbcc4688067a1c96a1deab245e332f399229064717b459c7e1335b24cf(
    *,
    field: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfb0667ad24dd6235b5f2ed312caa77e1f701ec45ef9ede29e44392f15aac03c(
    *,
    maximum_event_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26cf77be3f215b6615f2fb1468417b3d4d349010bdd2e944d2328e29ca7e1a6d(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__581d39e5eac9471e9771cc9718d3cd5dd71491fa62429a05fb92fb135366f23d(
    *,
    pipeline_parameter_list: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnSchedule.SageMakerPipelineParameterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c054234ca511d7dbcef12644289d5976f2ed75dae77cf2a2b7cd56bd83f609(
    *,
    message_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9918e491b65b371b1f7d9ebb0db09163f31e22e918415c531618993961d2c05(
    *,
    arn: builtins.str,
    role_arn: builtins.str,
    dead_letter_config: typing.Optional[typing.Union[typing.Union[CfnSchedule.DeadLetterConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ecs_parameters: typing.Optional[typing.Union[typing.Union[CfnSchedule.EcsParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    event_bridge_parameters: typing.Optional[typing.Union[typing.Union[CfnSchedule.EventBridgeParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    input: typing.Optional[builtins.str] = None,
    kinesis_parameters: typing.Optional[typing.Union[typing.Union[CfnSchedule.KinesisParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    retry_policy: typing.Optional[typing.Union[typing.Union[CfnSchedule.RetryPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sage_maker_pipeline_parameters: typing.Optional[typing.Union[typing.Union[CfnSchedule.SageMakerPipelineParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sqs_parameters: typing.Optional[typing.Union[typing.Union[CfnSchedule.SqsParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__007dc3664db15a99a7704fb24b138d5b020e0cad6dba4713c2dadc85c55780a7(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58e44d39f54fd63a80956274e514a5b974a169fcdd7311df1f9e7548b4a5e7f(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__603fe8a75d7fe90e5c37ad9fbfeff0a8b70b875298175cbd8e16368ac0dbb3e3(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4932fd926bbd5b6075bfedde89c72142666d1e2b5582f33be7627d57f70995be(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d506b86484dae30ae1d28b8b9594c2d074240e93001d7bb706d2bd4e9e58cf6(
    *,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe5eb4a72b188be355dfc3ddc2c89f9906481853bea2d9ba379098c193072ca6(
    *,
    flexible_time_window: typing.Union[typing.Union[CfnSchedule.FlexibleTimeWindowProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    schedule_expression: builtins.str,
    target: typing.Union[typing.Union[CfnSchedule.TargetProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    description: typing.Optional[builtins.str] = None,
    end_date: typing.Optional[builtins.str] = None,
    group_name: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    schedule_expression_timezone: typing.Optional[builtins.str] = None,
    start_date: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
