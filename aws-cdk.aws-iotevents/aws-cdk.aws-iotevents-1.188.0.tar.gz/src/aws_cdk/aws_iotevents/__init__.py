'''
# AWS::IoTEvents Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

AWS IoT Events enables you to monitor your equipment or device fleets for
failures or changes in operation, and to trigger actions when such events
occur.

## Installation

Install the module:

```console
$ npm i @aws-cdk/aws-iotevents
```

Import it into your code:

```python
import aws_cdk.aws_iotevents as iotevents
```

## `DetectorModel`

The following example creates an AWS IoT Events detector model to your stack.
The detector model need a reference to at least one AWS IoT Events input.
AWS IoT Events inputs enable the detector to get MQTT payload values from IoT Core rules.

You can define built-in actions to use a timer or set a variable, or send data to other AWS resources.
See also [@aws-cdk/aws-iotevents-actions](https://docs.aws.amazon.com/cdk/api/v1/docs/aws-iotevents-actions-readme.html) for other actions.

```python
import aws_cdk.aws_iotevents as iotevents
import aws_cdk.aws_iotevents_actions as actions
import aws_cdk.aws_lambda as lambda_

# func: lambda.IFunction


input = iotevents.Input(self, "MyInput",
    input_name="my_input",  # optional
    attribute_json_paths=["payload.deviceId", "payload.temperature"]
)

warm_state = iotevents.State(
    state_name="warm",
    on_enter=[iotevents.Event(
        event_name="test-enter-event",
        condition=iotevents.Expression.current_input(input),
        actions=[actions.LambdaInvokeAction(func)]
    )],
    on_input=[iotevents.Event( # optional
        event_name="test-input-event",
        actions=[actions.LambdaInvokeAction(func)])],
    on_exit=[iotevents.Event( # optional
        event_name="test-exit-event",
        actions=[actions.LambdaInvokeAction(func)])]
)
cold_state = iotevents.State(
    state_name="cold"
)

# transit to coldState when temperature is less than 15
warm_state.transition_to(cold_state,
    event_name="to_coldState",  # optional property, default by combining the names of the States
    when=iotevents.Expression.lt(
        iotevents.Expression.input_attribute(input, "payload.temperature"),
        iotevents.Expression.from_string("15")),
    executing=[actions.LambdaInvokeAction(func)]
)
# transit to warmState when temperature is greater than or equal to 15
cold_state.transition_to(warm_state,
    when=iotevents.Expression.gte(
        iotevents.Expression.input_attribute(input, "payload.temperature"),
        iotevents.Expression.from_string("15"))
)

iotevents.DetectorModel(self, "MyDetectorModel",
    detector_model_name="test-detector-model",  # optional
    description="test-detector-model-description",  # optional property, default is none
    evaluation_method=iotevents.EventEvaluation.SERIAL,  # optional property, default is iotevents.EventEvaluation.BATCH
    detector_key="payload.deviceId",  # optional property, default is none and single detector instance will be created and all inputs will be routed to it
    initial_state=warm_state
)
```

To grant permissions to put messages in the input,
you can use the `grantWrite()` method:

```python
import aws_cdk.aws_iam as iam
import aws_cdk.aws_iotevents as iotevents

# grantable: iam.IGrantable

input = iotevents.Input.from_input_name(self, "MyInput", "my_input")

input.grant_write(grantable)
```
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

import aws_cdk.aws_iam as _aws_cdk_aws_iam_940a1ce0
import aws_cdk.core as _aws_cdk_core_f4b25747
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iotevents.ActionBindOptions",
    jsii_struct_bases=[],
    name_mapping={"role": "role"},
)
class ActionBindOptions:
    def __init__(self, *, role: _aws_cdk_aws_iam_940a1ce0.IRole) -> None:
        '''(experimental) Options when binding a Action to a detector model.

        :param role: (experimental) The IAM role assumed by IoT Events to perform the action.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            import aws_cdk.aws_iotevents as iotevents
            
            # role: iam.Role
            
            action_bind_options = iotevents.ActionBindOptions(
                role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6e4e20ba363e3582ad4c70accbecdc3e65a61c102b483e5f244eb6757edb282)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role": role,
        }

    @builtins.property
    def role(self) -> _aws_cdk_aws_iam_940a1ce0.IRole:
        '''(experimental) The IAM role assumed by IoT Events to perform the action.

        :stability: experimental
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.IRole, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iotevents.ActionConfig",
    jsii_struct_bases=[],
    name_mapping={"configuration": "configuration"},
)
class ActionConfig:
    def __init__(
        self,
        *,
        configuration: typing.Union["CfnDetectorModel.ActionProperty", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''(experimental) Properties for a AWS IoT Events action.

        :param configuration: (experimental) The configuration for this action.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iotevents as iotevents
            
            action_config = iotevents.ActionConfig(
                configuration=iotevents.CfnDetectorModel.ActionProperty(
                    clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                        timer_name="timerName"
                    ),
                    dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                        hash_key_field="hashKeyField",
                        hash_key_value="hashKeyValue",
                        table_name="tableName",
            
                        # the properties below are optional
                        hash_key_type="hashKeyType",
                        operation="operation",
                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        payload_field="payloadField",
                        range_key_field="rangeKeyField",
                        range_key_type="rangeKeyType",
                        range_key_value="rangeKeyValue"
                    ),
                    dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                        table_name="tableName",
            
                        # the properties below are optional
                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                        delivery_stream_name="deliveryStreamName",
            
                        # the properties below are optional
                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        separator="separator"
                    ),
                    iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                        input_name="inputName",
            
                        # the properties below are optional
                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                        property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                            value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                boolean_value="booleanValue",
                                double_value="doubleValue",
                                integer_value="integerValue",
                                string_value="stringValue"
                            ),
            
                            # the properties below are optional
                            quality="quality",
                            timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                time_in_seconds="timeInSeconds",
            
                                # the properties below are optional
                                offset_in_nanos="offsetInNanos"
                            )
                        ),
            
                        # the properties below are optional
                        asset_id="assetId",
                        entry_id="entryId",
                        property_alias="propertyAlias",
                        property_id="propertyId"
                    ),
                    iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                        mqtt_topic="mqttTopic",
            
                        # the properties below are optional
                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                        function_arn="functionArn",
            
                        # the properties below are optional
                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                        timer_name="timerName"
                    ),
                    set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                        timer_name="timerName",
            
                        # the properties below are optional
                        duration_expression="durationExpression",
                        seconds=123
                    ),
                    set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                        value="value",
                        variable_name="variableName"
                    ),
                    sns=iotevents.CfnDetectorModel.SnsProperty(
                        target_arn="targetArn",
            
                        # the properties below are optional
                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    sqs=iotevents.CfnDetectorModel.SqsProperty(
                        queue_url="queueUrl",
            
                        # the properties below are optional
                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        use_base64=False
                    )
                )
            )
        '''
        if isinstance(configuration, dict):
            configuration = CfnDetectorModel.ActionProperty(**configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d439f5f4716bead9be50e1122600ed3b2d5603d310a4523ce577b254c0f1fa37)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration": configuration,
        }

    @builtins.property
    def configuration(self) -> "CfnDetectorModel.ActionProperty":
        '''(experimental) The configuration for this action.

        :stability: experimental
        '''
        result = self._values.get("configuration")
        assert result is not None, "Required property 'configuration' is missing"
        return typing.cast("CfnDetectorModel.ActionProperty", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnAlarmModel(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModel",
):
    '''A CloudFormation ``AWS::IoTEvents::AlarmModel``.

    Represents an alarm model to monitor an AWS IoT Events input attribute. You can use the alarm to get notified when the value is outside a specified range. For more information, see `Create an alarm model <https://docs.aws.amazon.com/iotevents/latest/developerguide/create-alarms.html>`_ in the *AWS IoT Events Developer Guide* .

    :cloudformationResource: AWS::IoTEvents::AlarmModel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iotevents as iotevents
        
        cfn_alarm_model = iotevents.CfnAlarmModel(self, "MyCfnAlarmModel",
            alarm_rule=iotevents.CfnAlarmModel.AlarmRuleProperty(
                simple_rule=iotevents.CfnAlarmModel.SimpleRuleProperty(
                    comparison_operator="comparisonOperator",
                    input_property="inputProperty",
                    threshold="threshold"
                )
            ),
            role_arn="roleArn",
        
            # the properties below are optional
            alarm_capabilities=iotevents.CfnAlarmModel.AlarmCapabilitiesProperty(
                acknowledge_flow=iotevents.CfnAlarmModel.AcknowledgeFlowProperty(
                    enabled=False
                ),
                initialization_configuration=iotevents.CfnAlarmModel.InitializationConfigurationProperty(
                    disabled_on_initialization=False
                )
            ),
            alarm_event_actions=iotevents.CfnAlarmModel.AlarmEventActionsProperty(
                alarm_actions=[iotevents.CfnAlarmModel.AlarmActionProperty(
                    dynamo_db=iotevents.CfnAlarmModel.DynamoDBProperty(
                        hash_key_field="hashKeyField",
                        hash_key_value="hashKeyValue",
                        table_name="tableName",
        
                        # the properties below are optional
                        hash_key_type="hashKeyType",
                        operation="operation",
                        payload=iotevents.CfnAlarmModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        payload_field="payloadField",
                        range_key_field="rangeKeyField",
                        range_key_type="rangeKeyType",
                        range_key_value="rangeKeyValue"
                    ),
                    dynamo_dBv2=iotevents.CfnAlarmModel.DynamoDBv2Property(
                        table_name="tableName",
        
                        # the properties below are optional
                        payload=iotevents.CfnAlarmModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    firehose=iotevents.CfnAlarmModel.FirehoseProperty(
                        delivery_stream_name="deliveryStreamName",
        
                        # the properties below are optional
                        payload=iotevents.CfnAlarmModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        separator="separator"
                    ),
                    iot_events=iotevents.CfnAlarmModel.IotEventsProperty(
                        input_name="inputName",
        
                        # the properties below are optional
                        payload=iotevents.CfnAlarmModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    iot_site_wise=iotevents.CfnAlarmModel.IotSiteWiseProperty(
                        asset_id="assetId",
                        entry_id="entryId",
                        property_alias="propertyAlias",
                        property_id="propertyId",
                        property_value=iotevents.CfnAlarmModel.AssetPropertyValueProperty(
                            value=iotevents.CfnAlarmModel.AssetPropertyVariantProperty(
                                boolean_value="booleanValue",
                                double_value="doubleValue",
                                integer_value="integerValue",
                                string_value="stringValue"
                            ),
        
                            # the properties below are optional
                            quality="quality",
                            timestamp=iotevents.CfnAlarmModel.AssetPropertyTimestampProperty(
                                time_in_seconds="timeInSeconds",
        
                                # the properties below are optional
                                offset_in_nanos="offsetInNanos"
                            )
                        )
                    ),
                    iot_topic_publish=iotevents.CfnAlarmModel.IotTopicPublishProperty(
                        mqtt_topic="mqttTopic",
        
                        # the properties below are optional
                        payload=iotevents.CfnAlarmModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    lambda_=iotevents.CfnAlarmModel.LambdaProperty(
                        function_arn="functionArn",
        
                        # the properties below are optional
                        payload=iotevents.CfnAlarmModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    sns=iotevents.CfnAlarmModel.SnsProperty(
                        target_arn="targetArn",
        
                        # the properties below are optional
                        payload=iotevents.CfnAlarmModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    sqs=iotevents.CfnAlarmModel.SqsProperty(
                        queue_url="queueUrl",
        
                        # the properties below are optional
                        payload=iotevents.CfnAlarmModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        use_base64=False
                    )
                )]
            ),
            alarm_model_description="alarmModelDescription",
            alarm_model_name="alarmModelName",
            key="key",
            severity=123,
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        alarm_rule: typing.Union[typing.Union["CfnAlarmModel.AlarmRuleProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        role_arn: builtins.str,
        alarm_capabilities: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.AlarmCapabilitiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        alarm_event_actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.AlarmEventActionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        alarm_model_description: typing.Optional[builtins.str] = None,
        alarm_model_name: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        severity: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTEvents::AlarmModel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param alarm_rule: Defines when your alarm is invoked.
        :param role_arn: The ARN of the IAM role that allows the alarm to perform actions and access AWS resources. For more information, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param alarm_capabilities: Contains the configuration information of alarm state changes.
        :param alarm_event_actions: Contains information about one or more alarm actions.
        :param alarm_model_description: The description of the alarm model.
        :param alarm_model_name: The name of the alarm model.
        :param key: An input attribute used as a key to create an alarm. AWS IoT Events routes `inputs <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Input.html>`_ associated with this key to the alarm.
        :param severity: A non-negative integer that reflects the severity level of the alarm.
        :param tags: A list of key-value pairs that contain metadata for the alarm model. The tags help you manage the alarm model. For more information, see `Tagging your AWS IoT Events resources <https://docs.aws.amazon.com/iotevents/latest/developerguide/tagging-iotevents.html>`_ in the *AWS IoT Events Developer Guide* . You can create up to 50 tags for one alarm model.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b865a8f80af7952b8b1b2e5849ec961ae5136962021870e5072b51e705cf71ef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAlarmModelProps(
            alarm_rule=alarm_rule,
            role_arn=role_arn,
            alarm_capabilities=alarm_capabilities,
            alarm_event_actions=alarm_event_actions,
            alarm_model_description=alarm_model_description,
            alarm_model_name=alarm_model_name,
            key=key,
            severity=severity,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b35ceb8f84eb5605375dab910268d296f60c1bacd5c30be3f3c804581abb2f35)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc3f2c8a584a104362374c79e0614db42489b5f4d282595b5545d4d35721bddd)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''A list of key-value pairs that contain metadata for the alarm model.

        The tags help you manage the alarm model. For more information, see `Tagging your AWS IoT Events resources <https://docs.aws.amazon.com/iotevents/latest/developerguide/tagging-iotevents.html>`_ in the *AWS IoT Events Developer Guide* .

        You can create up to 50 tags for one alarm model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="alarmRule")
    def alarm_rule(
        self,
    ) -> typing.Union["CfnAlarmModel.AlarmRuleProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''Defines when your alarm is invoked.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-alarmrule
        '''
        return typing.cast(typing.Union["CfnAlarmModel.AlarmRuleProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "alarmRule"))

    @alarm_rule.setter
    def alarm_rule(
        self,
        value: typing.Union["CfnAlarmModel.AlarmRuleProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d16e53e3e055183bb3ecc8468e38382f6396c1cffd5d1b5467111f42e7d950c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmRule", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The ARN of the IAM role that allows the alarm to perform actions and access AWS resources.

        For more information, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-rolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97c6b18b8c6f64d6c959f437aaab99054154b1f300e33c2d1164a00f407c3726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="alarmCapabilities")
    def alarm_capabilities(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.AlarmCapabilitiesProperty"]]:
        '''Contains the configuration information of alarm state changes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-alarmcapabilities
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.AlarmCapabilitiesProperty"]], jsii.get(self, "alarmCapabilities"))

    @alarm_capabilities.setter
    def alarm_capabilities(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.AlarmCapabilitiesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa9c01884d5e6b0057d9c603574a54e99207049299f60210b611434af9cc7d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmCapabilities", value)

    @builtins.property
    @jsii.member(jsii_name="alarmEventActions")
    def alarm_event_actions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.AlarmEventActionsProperty"]]:
        '''Contains information about one or more alarm actions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-alarmeventactions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.AlarmEventActionsProperty"]], jsii.get(self, "alarmEventActions"))

    @alarm_event_actions.setter
    def alarm_event_actions(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.AlarmEventActionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a39551781ab30e8b75606d2c5480da65aa186cc5117af8aab7f8dae053433470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmEventActions", value)

    @builtins.property
    @jsii.member(jsii_name="alarmModelDescription")
    def alarm_model_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-alarmmodeldescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alarmModelDescription"))

    @alarm_model_description.setter
    def alarm_model_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4375f5713256be0f6ff946e4da30f1dfc1af932546d6e6156fd5b0a468a81b31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmModelDescription", value)

    @builtins.property
    @jsii.member(jsii_name="alarmModelName")
    def alarm_model_name(self) -> typing.Optional[builtins.str]:
        '''The name of the alarm model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-alarmmodelname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alarmModelName"))

    @alarm_model_name.setter
    def alarm_model_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d98a56666e8c2c8fff01ce6a5abd1646f39abde73d1942dfb1c7e6d756a677a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmModelName", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> typing.Optional[builtins.str]:
        '''An input attribute used as a key to create an alarm.

        AWS IoT Events routes `inputs <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Input.html>`_ associated with this key to the alarm.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-key
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "key"))

    @key.setter
    def key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fdcae76ae679f4116866637a98a9e464d81b04c811f22eb028532f15f40116c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> typing.Optional[jsii.Number]:
        '''A non-negative integer that reflects the severity level of the alarm.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-severity
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6c550c17eb7ac3d503af21342bb28e717a8c5570860a6309d46833545ce5e35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModel.AcknowledgeFlowProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class AcknowledgeFlowProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Specifies whether to get notified for alarm state changes.

            :param enabled: The value must be ``TRUE`` or ``FALSE`` . If ``TRUE`` , you receive a notification when the alarm state changes. You must choose to acknowledge the notification before the alarm state can return to ``NORMAL`` . If ``FALSE`` , you won't receive notifications. The alarm automatically changes to the ``NORMAL`` state when the input property value returns to the specified range.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-acknowledgeflow.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                acknowledge_flow_property = iotevents.CfnAlarmModel.AcknowledgeFlowProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d4ce31ee5e28212451cf6e2ef3b9a0baadab9bccf136ddf92fb50b5a01d66e40)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''The value must be ``TRUE`` or ``FALSE`` .

            If ``TRUE`` , you receive a notification when the alarm state changes. You must choose to acknowledge the notification before the alarm state can return to ``NORMAL`` . If ``FALSE`` , you won't receive notifications. The alarm automatically changes to the ``NORMAL`` state when the input property value returns to the specified range.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-acknowledgeflow.html#cfn-iotevents-alarmmodel-acknowledgeflow-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AcknowledgeFlowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModel.AlarmActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dynamo_db": "dynamoDb",
            "dynamo_d_bv2": "dynamoDBv2",
            "firehose": "firehose",
            "iot_events": "iotEvents",
            "iot_site_wise": "iotSiteWise",
            "iot_topic_publish": "iotTopicPublish",
            "lambda_": "lambda",
            "sns": "sns",
            "sqs": "sqs",
        },
    )
    class AlarmActionProperty:
        def __init__(
            self,
            *,
            dynamo_db: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.DynamoDBProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dynamo_d_bv2: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.DynamoDBv2Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            firehose: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.FirehoseProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            iot_events: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.IotEventsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            iot_site_wise: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.IotSiteWiseProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            iot_topic_publish: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.IotTopicPublishProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            lambda_: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.LambdaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sns: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.SnsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sqs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.SqsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies one of the following actions to receive notifications when the alarm state changes.

            :param dynamo_db: Defines an action to write to the Amazon DynamoDB table that you created. The standard action payload contains all the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . One column of the DynamoDB table receives all attribute-value pairs in the payload that you specify. You must use expressions for all parameters in ``DynamoDBAction`` . The expressions accept literals, operators, functions, references, and substitution templates. **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``hashKeyType`` parameter can be ``'STRING'`` . - For references, you must specify either variables or input values. For example, the value for the ``hashKeyField`` parameter can be ``$input.GreenhouseInput.name`` . - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates. In the following example, the value for the ``hashKeyValue`` parameter uses a substitution template. ``'${$input.GreenhouseInput.temperature * 6 / 5 + 32} in Fahrenheit'`` - For a string concatenation, you must use ``+`` . A string concatenation can also contain a combination of literals, operators, functions, references, and substitution templates. In the following example, the value for the ``tableName`` parameter uses a string concatenation. ``'GreenhouseTemperatureTable ' + $input.GreenhouseInput.date`` For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* . If the defined payload type is a string, ``DynamoDBAction`` writes non-JSON data to the DynamoDB table as binary data. The DynamoDB console displays the data as Base64-encoded text. The value for the ``payloadField`` parameter is ``<payload-field>_raw`` .
            :param dynamo_d_bv2: Defines an action to write to the Amazon DynamoDB table that you created. The default action payload contains all the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . A separate column of the DynamoDB table receives one attribute-value pair in the payload that you specify. You must use expressions for all parameters in ``DynamoDBv2Action`` . The expressions accept literals, operators, functions, references, and substitution templates. **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``tableName`` parameter can be ``'GreenhouseTemperatureTable'`` . - For references, you must specify either variables or input values. For example, the value for the ``tableName`` parameter can be ``$variable.ddbtableName`` . - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates. In the following example, the value for the ``contentExpression`` parameter in ``Payload`` uses a substitution template. ``'{\\"sensorID\\": \\"${$input.GreenhouseInput.sensor_id}\\", \\"temperature\\": \\"${$input.GreenhouseInput.temperature * 9 / 5 + 32}\\"}'`` - For a string concatenation, you must use ``+`` . A string concatenation can also contain a combination of literals, operators, functions, references, and substitution templates. In the following example, the value for the ``tableName`` parameter uses a string concatenation. ``'GreenhouseTemperatureTable ' + $input.GreenhouseInput.date`` For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* . The value for the ``type`` parameter in ``Payload`` must be ``JSON`` .
            :param firehose: Sends information about the detector model instance and the event that triggered the action to an Amazon Kinesis Data Firehose delivery stream.
            :param iot_events: Sends an AWS IoT Events input, passing in information about the detector model instance and the event that triggered the action.
            :param iot_site_wise: Sends information about the detector model instance and the event that triggered the action to a specified asset property in AWS IoT SiteWise . You must use expressions for all parameters in ``IotSiteWiseAction`` . The expressions accept literals, operators, functions, references, and substitutions templates. **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``propertyAlias`` parameter can be ``'/company/windfarm/3/turbine/7/temperature'`` . - For references, you must specify either variables or input values. For example, the value for the ``assetId`` parameter can be ``$input.TurbineInput.assetId1`` . - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates. In the following example, the value for the ``propertyAlias`` parameter uses a substitution template. ``'company/windfarm/${$input.TemperatureInput.sensorData.windfarmID}/turbine/ ${$input.TemperatureInput.sensorData.turbineID}/temperature'`` You must specify either ``propertyAlias`` or both ``assetId`` and ``propertyId`` to identify the target asset property in AWS IoT SiteWise . For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .
            :param iot_topic_publish: Information required to publish the MQTT message through the AWS IoT message broker.
            :param lambda_: Calls a Lambda function, passing in information about the detector model instance and the event that triggered the action.
            :param sns: ``CfnAlarmModel.AlarmActionProperty.Sns``.
            :param sqs: Sends information about the detector model instance and the event that triggered the action to an Amazon SQS queue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                alarm_action_property = iotevents.CfnAlarmModel.AlarmActionProperty(
                    dynamo_db=iotevents.CfnAlarmModel.DynamoDBProperty(
                        hash_key_field="hashKeyField",
                        hash_key_value="hashKeyValue",
                        table_name="tableName",
                
                        # the properties below are optional
                        hash_key_type="hashKeyType",
                        operation="operation",
                        payload=iotevents.CfnAlarmModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        payload_field="payloadField",
                        range_key_field="rangeKeyField",
                        range_key_type="rangeKeyType",
                        range_key_value="rangeKeyValue"
                    ),
                    dynamo_dBv2=iotevents.CfnAlarmModel.DynamoDBv2Property(
                        table_name="tableName",
                
                        # the properties below are optional
                        payload=iotevents.CfnAlarmModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    firehose=iotevents.CfnAlarmModel.FirehoseProperty(
                        delivery_stream_name="deliveryStreamName",
                
                        # the properties below are optional
                        payload=iotevents.CfnAlarmModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        separator="separator"
                    ),
                    iot_events=iotevents.CfnAlarmModel.IotEventsProperty(
                        input_name="inputName",
                
                        # the properties below are optional
                        payload=iotevents.CfnAlarmModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    iot_site_wise=iotevents.CfnAlarmModel.IotSiteWiseProperty(
                        asset_id="assetId",
                        entry_id="entryId",
                        property_alias="propertyAlias",
                        property_id="propertyId",
                        property_value=iotevents.CfnAlarmModel.AssetPropertyValueProperty(
                            value=iotevents.CfnAlarmModel.AssetPropertyVariantProperty(
                                boolean_value="booleanValue",
                                double_value="doubleValue",
                                integer_value="integerValue",
                                string_value="stringValue"
                            ),
                
                            # the properties below are optional
                            quality="quality",
                            timestamp=iotevents.CfnAlarmModel.AssetPropertyTimestampProperty(
                                time_in_seconds="timeInSeconds",
                
                                # the properties below are optional
                                offset_in_nanos="offsetInNanos"
                            )
                        )
                    ),
                    iot_topic_publish=iotevents.CfnAlarmModel.IotTopicPublishProperty(
                        mqtt_topic="mqttTopic",
                
                        # the properties below are optional
                        payload=iotevents.CfnAlarmModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    lambda_=iotevents.CfnAlarmModel.LambdaProperty(
                        function_arn="functionArn",
                
                        # the properties below are optional
                        payload=iotevents.CfnAlarmModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    sns=iotevents.CfnAlarmModel.SnsProperty(
                        target_arn="targetArn",
                
                        # the properties below are optional
                        payload=iotevents.CfnAlarmModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    sqs=iotevents.CfnAlarmModel.SqsProperty(
                        queue_url="queueUrl",
                
                        # the properties below are optional
                        payload=iotevents.CfnAlarmModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        use_base64=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ca2d49aa4bc7249874260ab9616b9866ce9e315a0ed5f31faeb171b9e25ac74f)
                check_type(argname="argument dynamo_db", value=dynamo_db, expected_type=type_hints["dynamo_db"])
                check_type(argname="argument dynamo_d_bv2", value=dynamo_d_bv2, expected_type=type_hints["dynamo_d_bv2"])
                check_type(argname="argument firehose", value=firehose, expected_type=type_hints["firehose"])
                check_type(argname="argument iot_events", value=iot_events, expected_type=type_hints["iot_events"])
                check_type(argname="argument iot_site_wise", value=iot_site_wise, expected_type=type_hints["iot_site_wise"])
                check_type(argname="argument iot_topic_publish", value=iot_topic_publish, expected_type=type_hints["iot_topic_publish"])
                check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
                check_type(argname="argument sns", value=sns, expected_type=type_hints["sns"])
                check_type(argname="argument sqs", value=sqs, expected_type=type_hints["sqs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dynamo_db is not None:
                self._values["dynamo_db"] = dynamo_db
            if dynamo_d_bv2 is not None:
                self._values["dynamo_d_bv2"] = dynamo_d_bv2
            if firehose is not None:
                self._values["firehose"] = firehose
            if iot_events is not None:
                self._values["iot_events"] = iot_events
            if iot_site_wise is not None:
                self._values["iot_site_wise"] = iot_site_wise
            if iot_topic_publish is not None:
                self._values["iot_topic_publish"] = iot_topic_publish
            if lambda_ is not None:
                self._values["lambda_"] = lambda_
            if sns is not None:
                self._values["sns"] = sns
            if sqs is not None:
                self._values["sqs"] = sqs

        @builtins.property
        def dynamo_db(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.DynamoDBProperty"]]:
            '''Defines an action to write to the Amazon DynamoDB table that you created.

            The standard action payload contains all the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . One column of the DynamoDB table receives all attribute-value pairs in the payload that you specify.

            You must use expressions for all parameters in ``DynamoDBAction`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``hashKeyType`` parameter can be ``'STRING'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``hashKeyField`` parameter can be ``$input.GreenhouseInput.name`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``hashKeyValue`` parameter uses a substitution template.

            ``'${$input.GreenhouseInput.temperature * 6 / 5 + 32} in Fahrenheit'``

            - For a string concatenation, you must use ``+`` . A string concatenation can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``tableName`` parameter uses a string concatenation.

            ``'GreenhouseTemperatureTable ' + $input.GreenhouseInput.date``

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            If the defined payload type is a string, ``DynamoDBAction`` writes non-JSON data to the DynamoDB table as binary data. The DynamoDB console displays the data as Base64-encoded text. The value for the ``payloadField`` parameter is ``<payload-field>_raw`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-dynamodb
            '''
            result = self._values.get("dynamo_db")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.DynamoDBProperty"]], result)

        @builtins.property
        def dynamo_d_bv2(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.DynamoDBv2Property"]]:
            '''Defines an action to write to the Amazon DynamoDB table that you created.

            The default action payload contains all the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . A separate column of the DynamoDB table receives one attribute-value pair in the payload that you specify.

            You must use expressions for all parameters in ``DynamoDBv2Action`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``tableName`` parameter can be ``'GreenhouseTemperatureTable'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``tableName`` parameter can be ``$variable.ddbtableName`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``contentExpression`` parameter in ``Payload`` uses a substitution template.

            ``'{\\"sensorID\\": \\"${$input.GreenhouseInput.sensor_id}\\", \\"temperature\\": \\"${$input.GreenhouseInput.temperature * 9 / 5 + 32}\\"}'``

            - For a string concatenation, you must use ``+`` . A string concatenation can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``tableName`` parameter uses a string concatenation.

            ``'GreenhouseTemperatureTable ' + $input.GreenhouseInput.date``

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            The value for the ``type`` parameter in ``Payload`` must be ``JSON`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-dynamodbv2
            '''
            result = self._values.get("dynamo_d_bv2")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.DynamoDBv2Property"]], result)

        @builtins.property
        def firehose(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.FirehoseProperty"]]:
            '''Sends information about the detector model instance and the event that triggered the action to an Amazon Kinesis Data Firehose delivery stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-firehose
            '''
            result = self._values.get("firehose")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.FirehoseProperty"]], result)

        @builtins.property
        def iot_events(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.IotEventsProperty"]]:
            '''Sends an AWS IoT Events input, passing in information about the detector model instance and the event that triggered the action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-iotevents
            '''
            result = self._values.get("iot_events")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.IotEventsProperty"]], result)

        @builtins.property
        def iot_site_wise(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.IotSiteWiseProperty"]]:
            '''Sends information about the detector model instance and the event that triggered the action to a specified asset property in AWS IoT SiteWise .

            You must use expressions for all parameters in ``IotSiteWiseAction`` . The expressions accept literals, operators, functions, references, and substitutions templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``propertyAlias`` parameter can be ``'/company/windfarm/3/turbine/7/temperature'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``assetId`` parameter can be ``$input.TurbineInput.assetId1`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``propertyAlias`` parameter uses a substitution template.

            ``'company/windfarm/${$input.TemperatureInput.sensorData.windfarmID}/turbine/ ${$input.TemperatureInput.sensorData.turbineID}/temperature'``

            You must specify either ``propertyAlias`` or both ``assetId`` and ``propertyId`` to identify the target asset property in AWS IoT SiteWise .

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-iotsitewise
            '''
            result = self._values.get("iot_site_wise")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.IotSiteWiseProperty"]], result)

        @builtins.property
        def iot_topic_publish(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.IotTopicPublishProperty"]]:
            '''Information required to publish the MQTT message through the AWS IoT message broker.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-iottopicpublish
            '''
            result = self._values.get("iot_topic_publish")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.IotTopicPublishProperty"]], result)

        @builtins.property
        def lambda_(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.LambdaProperty"]]:
            '''Calls a Lambda function, passing in information about the detector model instance and the event that triggered the action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-lambda
            '''
            result = self._values.get("lambda_")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.LambdaProperty"]], result)

        @builtins.property
        def sns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.SnsProperty"]]:
            '''``CfnAlarmModel.AlarmActionProperty.Sns``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-sns
            '''
            result = self._values.get("sns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.SnsProperty"]], result)

        @builtins.property
        def sqs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.SqsProperty"]]:
            '''Sends information about the detector model instance and the event that triggered the action to an Amazon SQS queue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-sqs
            '''
            result = self._values.get("sqs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.SqsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModel.AlarmCapabilitiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "acknowledge_flow": "acknowledgeFlow",
            "initialization_configuration": "initializationConfiguration",
        },
    )
    class AlarmCapabilitiesProperty:
        def __init__(
            self,
            *,
            acknowledge_flow: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.AcknowledgeFlowProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            initialization_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.InitializationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains the configuration information of alarm state changes.

            :param acknowledge_flow: Specifies whether to get notified for alarm state changes.
            :param initialization_configuration: Specifies the default alarm state. The configuration applies to all alarms that were created based on this alarm model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmcapabilities.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                alarm_capabilities_property = iotevents.CfnAlarmModel.AlarmCapabilitiesProperty(
                    acknowledge_flow=iotevents.CfnAlarmModel.AcknowledgeFlowProperty(
                        enabled=False
                    ),
                    initialization_configuration=iotevents.CfnAlarmModel.InitializationConfigurationProperty(
                        disabled_on_initialization=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f8ecf1907f94be4f65cd1ef05ff98d984d1db1a5610d54694b32330e12379d4c)
                check_type(argname="argument acknowledge_flow", value=acknowledge_flow, expected_type=type_hints["acknowledge_flow"])
                check_type(argname="argument initialization_configuration", value=initialization_configuration, expected_type=type_hints["initialization_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if acknowledge_flow is not None:
                self._values["acknowledge_flow"] = acknowledge_flow
            if initialization_configuration is not None:
                self._values["initialization_configuration"] = initialization_configuration

        @builtins.property
        def acknowledge_flow(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.AcknowledgeFlowProperty"]]:
            '''Specifies whether to get notified for alarm state changes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmcapabilities.html#cfn-iotevents-alarmmodel-alarmcapabilities-acknowledgeflow
            '''
            result = self._values.get("acknowledge_flow")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.AcknowledgeFlowProperty"]], result)

        @builtins.property
        def initialization_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.InitializationConfigurationProperty"]]:
            '''Specifies the default alarm state.

            The configuration applies to all alarms that were created based on this alarm model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmcapabilities.html#cfn-iotevents-alarmmodel-alarmcapabilities-initializationconfiguration
            '''
            result = self._values.get("initialization_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.InitializationConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmCapabilitiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModel.AlarmEventActionsProperty",
        jsii_struct_bases=[],
        name_mapping={"alarm_actions": "alarmActions"},
    )
    class AlarmEventActionsProperty:
        def __init__(
            self,
            *,
            alarm_actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.AlarmActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains information about one or more alarm actions.

            :param alarm_actions: Specifies one or more supported actions to receive notifications when the alarm state changes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmeventactions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                alarm_event_actions_property = iotevents.CfnAlarmModel.AlarmEventActionsProperty(
                    alarm_actions=[iotevents.CfnAlarmModel.AlarmActionProperty(
                        dynamo_db=iotevents.CfnAlarmModel.DynamoDBProperty(
                            hash_key_field="hashKeyField",
                            hash_key_value="hashKeyValue",
                            table_name="tableName",
                
                            # the properties below are optional
                            hash_key_type="hashKeyType",
                            operation="operation",
                            payload=iotevents.CfnAlarmModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            payload_field="payloadField",
                            range_key_field="rangeKeyField",
                            range_key_type="rangeKeyType",
                            range_key_value="rangeKeyValue"
                        ),
                        dynamo_dBv2=iotevents.CfnAlarmModel.DynamoDBv2Property(
                            table_name="tableName",
                
                            # the properties below are optional
                            payload=iotevents.CfnAlarmModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        firehose=iotevents.CfnAlarmModel.FirehoseProperty(
                            delivery_stream_name="deliveryStreamName",
                
                            # the properties below are optional
                            payload=iotevents.CfnAlarmModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            separator="separator"
                        ),
                        iot_events=iotevents.CfnAlarmModel.IotEventsProperty(
                            input_name="inputName",
                
                            # the properties below are optional
                            payload=iotevents.CfnAlarmModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        iot_site_wise=iotevents.CfnAlarmModel.IotSiteWiseProperty(
                            asset_id="assetId",
                            entry_id="entryId",
                            property_alias="propertyAlias",
                            property_id="propertyId",
                            property_value=iotevents.CfnAlarmModel.AssetPropertyValueProperty(
                                value=iotevents.CfnAlarmModel.AssetPropertyVariantProperty(
                                    boolean_value="booleanValue",
                                    double_value="doubleValue",
                                    integer_value="integerValue",
                                    string_value="stringValue"
                                ),
                
                                # the properties below are optional
                                quality="quality",
                                timestamp=iotevents.CfnAlarmModel.AssetPropertyTimestampProperty(
                                    time_in_seconds="timeInSeconds",
                
                                    # the properties below are optional
                                    offset_in_nanos="offsetInNanos"
                                )
                            )
                        ),
                        iot_topic_publish=iotevents.CfnAlarmModel.IotTopicPublishProperty(
                            mqtt_topic="mqttTopic",
                
                            # the properties below are optional
                            payload=iotevents.CfnAlarmModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        lambda_=iotevents.CfnAlarmModel.LambdaProperty(
                            function_arn="functionArn",
                
                            # the properties below are optional
                            payload=iotevents.CfnAlarmModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        sns=iotevents.CfnAlarmModel.SnsProperty(
                            target_arn="targetArn",
                
                            # the properties below are optional
                            payload=iotevents.CfnAlarmModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        sqs=iotevents.CfnAlarmModel.SqsProperty(
                            queue_url="queueUrl",
                
                            # the properties below are optional
                            payload=iotevents.CfnAlarmModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            use_base64=False
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__de40a95f07bb0f0039395959b5963380ad4d6e9b2f30e8fce314408d58db484d)
                check_type(argname="argument alarm_actions", value=alarm_actions, expected_type=type_hints["alarm_actions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alarm_actions is not None:
                self._values["alarm_actions"] = alarm_actions

        @builtins.property
        def alarm_actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.AlarmActionProperty"]]]]:
            '''Specifies one or more supported actions to receive notifications when the alarm state changes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmeventactions.html#cfn-iotevents-alarmmodel-alarmeventactions-alarmactions
            '''
            result = self._values.get("alarm_actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.AlarmActionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmEventActionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModel.AlarmRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"simple_rule": "simpleRule"},
    )
    class AlarmRuleProperty:
        def __init__(
            self,
            *,
            simple_rule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.SimpleRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Defines when your alarm is invoked.

            :param simple_rule: A rule that compares an input property value to a threshold value with a comparison operator.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                alarm_rule_property = iotevents.CfnAlarmModel.AlarmRuleProperty(
                    simple_rule=iotevents.CfnAlarmModel.SimpleRuleProperty(
                        comparison_operator="comparisonOperator",
                        input_property="inputProperty",
                        threshold="threshold"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1996cc62c11a58432f39f15e1f2d262e684403bad70d61c8c9feff2a563ea07d)
                check_type(argname="argument simple_rule", value=simple_rule, expected_type=type_hints["simple_rule"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if simple_rule is not None:
                self._values["simple_rule"] = simple_rule

        @builtins.property
        def simple_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.SimpleRuleProperty"]]:
            '''A rule that compares an input property value to a threshold value with a comparison operator.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmrule.html#cfn-iotevents-alarmmodel-alarmrule-simplerule
            '''
            result = self._values.get("simple_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.SimpleRuleProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModel.AssetPropertyTimestampProperty",
        jsii_struct_bases=[],
        name_mapping={
            "time_in_seconds": "timeInSeconds",
            "offset_in_nanos": "offsetInNanos",
        },
    )
    class AssetPropertyTimestampProperty:
        def __init__(
            self,
            *,
            time_in_seconds: builtins.str,
            offset_in_nanos: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that contains timestamp information. For more information, see `TimeInNanos <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_TimeInNanos.html>`_ in the *AWS IoT SiteWise API Reference* .

            You must use expressions for all parameters in ``AssetPropertyTimestamp`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``timeInSeconds`` parameter can be ``'1586400675'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``offsetInNanos`` parameter can be ``$variable.time`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``timeInSeconds`` parameter uses a substitution template.

            ``'${$input.TemperatureInput.sensorData.timestamp / 1000}'``

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            :param time_in_seconds: The timestamp, in seconds, in the Unix epoch format. The valid range is between 1-31556889864403199.
            :param offset_in_nanos: The nanosecond offset converted from ``timeInSeconds`` . The valid range is between 0-999999999.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertytimestamp.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                asset_property_timestamp_property = iotevents.CfnAlarmModel.AssetPropertyTimestampProperty(
                    time_in_seconds="timeInSeconds",
                
                    # the properties below are optional
                    offset_in_nanos="offsetInNanos"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__da7b4d62e42583bff1c92d47c9b4ec10cd620ef140852f206980d2244ef5cf3b)
                check_type(argname="argument time_in_seconds", value=time_in_seconds, expected_type=type_hints["time_in_seconds"])
                check_type(argname="argument offset_in_nanos", value=offset_in_nanos, expected_type=type_hints["offset_in_nanos"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "time_in_seconds": time_in_seconds,
            }
            if offset_in_nanos is not None:
                self._values["offset_in_nanos"] = offset_in_nanos

        @builtins.property
        def time_in_seconds(self) -> builtins.str:
            '''The timestamp, in seconds, in the Unix epoch format.

            The valid range is between 1-31556889864403199.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertytimestamp.html#cfn-iotevents-alarmmodel-assetpropertytimestamp-timeinseconds
            '''
            result = self._values.get("time_in_seconds")
            assert result is not None, "Required property 'time_in_seconds' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def offset_in_nanos(self) -> typing.Optional[builtins.str]:
            '''The nanosecond offset converted from ``timeInSeconds`` .

            The valid range is between 0-999999999.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertytimestamp.html#cfn-iotevents-alarmmodel-assetpropertytimestamp-offsetinnanos
            '''
            result = self._values.get("offset_in_nanos")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetPropertyTimestampProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModel.AssetPropertyValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "value": "value",
            "quality": "quality",
            "timestamp": "timestamp",
        },
    )
    class AssetPropertyValueProperty:
        def __init__(
            self,
            *,
            value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.AssetPropertyVariantProperty", typing.Dict[builtins.str, typing.Any]]],
            quality: typing.Optional[builtins.str] = None,
            timestamp: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.AssetPropertyTimestampProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A structure that contains value information. For more information, see `AssetPropertyValue <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_AssetPropertyValue.html>`_ in the *AWS IoT SiteWise API Reference* .

            You must use expressions for all parameters in ``AssetPropertyValue`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``quality`` parameter can be ``'GOOD'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``quality`` parameter can be ``$input.TemperatureInput.sensorData.quality`` .

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            :param value: The value to send to an asset property.
            :param quality: The quality of the asset property value. The value must be ``'GOOD'`` , ``'BAD'`` , or ``'UNCERTAIN'`` .
            :param timestamp: The timestamp associated with the asset property value. The default is the current event time.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertyvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                asset_property_value_property = iotevents.CfnAlarmModel.AssetPropertyValueProperty(
                    value=iotevents.CfnAlarmModel.AssetPropertyVariantProperty(
                        boolean_value="booleanValue",
                        double_value="doubleValue",
                        integer_value="integerValue",
                        string_value="stringValue"
                    ),
                
                    # the properties below are optional
                    quality="quality",
                    timestamp=iotevents.CfnAlarmModel.AssetPropertyTimestampProperty(
                        time_in_seconds="timeInSeconds",
                
                        # the properties below are optional
                        offset_in_nanos="offsetInNanos"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0e6d4ab6b1ff6d5770977fead02aba27fb717ede46cdd9e6a6ca6c3b77afd4d5)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                check_type(argname="argument quality", value=quality, expected_type=type_hints["quality"])
                check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "value": value,
            }
            if quality is not None:
                self._values["quality"] = quality
            if timestamp is not None:
                self._values["timestamp"] = timestamp

        @builtins.property
        def value(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.AssetPropertyVariantProperty"]:
            '''The value to send to an asset property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertyvalue.html#cfn-iotevents-alarmmodel-assetpropertyvalue-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.AssetPropertyVariantProperty"], result)

        @builtins.property
        def quality(self) -> typing.Optional[builtins.str]:
            '''The quality of the asset property value.

            The value must be ``'GOOD'`` , ``'BAD'`` , or ``'UNCERTAIN'`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertyvalue.html#cfn-iotevents-alarmmodel-assetpropertyvalue-quality
            '''
            result = self._values.get("quality")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timestamp(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.AssetPropertyTimestampProperty"]]:
            '''The timestamp associated with the asset property value.

            The default is the current event time.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertyvalue.html#cfn-iotevents-alarmmodel-assetpropertyvalue-timestamp
            '''
            result = self._values.get("timestamp")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.AssetPropertyTimestampProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetPropertyValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModel.AssetPropertyVariantProperty",
        jsii_struct_bases=[],
        name_mapping={
            "boolean_value": "booleanValue",
            "double_value": "doubleValue",
            "integer_value": "integerValue",
            "string_value": "stringValue",
        },
    )
    class AssetPropertyVariantProperty:
        def __init__(
            self,
            *,
            boolean_value: typing.Optional[builtins.str] = None,
            double_value: typing.Optional[builtins.str] = None,
            integer_value: typing.Optional[builtins.str] = None,
            string_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that contains an asset property value.

            For more information, see `Variant <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_Variant.html>`_ in the *AWS IoT SiteWise API Reference* .

            You must use expressions for all parameters in ``AssetPropertyVariant`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``integerValue`` parameter can be ``'100'`` .

            - For references, you must specify either variables or parameters. For example, the value for the ``booleanValue`` parameter can be ``$variable.offline`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``doubleValue`` parameter uses a substitution template.

            ``'${$input.TemperatureInput.sensorData.temperature * 6 / 5 + 32}'``

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            You must specify one of the following value types, depending on the ``dataType`` of the specified asset property. For more information, see `AssetProperty <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_AssetProperty.html>`_ in the *AWS IoT SiteWise API Reference* .

            :param boolean_value: The asset property value is a Boolean value that must be ``'TRUE'`` or ``'FALSE'`` . You must use an expression, and the evaluated result should be a Boolean value.
            :param double_value: The asset property value is a double. You must use an expression, and the evaluated result should be a double.
            :param integer_value: The asset property value is an integer. You must use an expression, and the evaluated result should be an integer.
            :param string_value: The asset property value is a string. You must use an expression, and the evaluated result should be a string.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertyvariant.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                asset_property_variant_property = iotevents.CfnAlarmModel.AssetPropertyVariantProperty(
                    boolean_value="booleanValue",
                    double_value="doubleValue",
                    integer_value="integerValue",
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a3dff3482581c0d7b7f1f373a6939726703984e4cd432dda6ff5e5905986fc81)
                check_type(argname="argument boolean_value", value=boolean_value, expected_type=type_hints["boolean_value"])
                check_type(argname="argument double_value", value=double_value, expected_type=type_hints["double_value"])
                check_type(argname="argument integer_value", value=integer_value, expected_type=type_hints["integer_value"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if boolean_value is not None:
                self._values["boolean_value"] = boolean_value
            if double_value is not None:
                self._values["double_value"] = double_value
            if integer_value is not None:
                self._values["integer_value"] = integer_value
            if string_value is not None:
                self._values["string_value"] = string_value

        @builtins.property
        def boolean_value(self) -> typing.Optional[builtins.str]:
            '''The asset property value is a Boolean value that must be ``'TRUE'`` or ``'FALSE'`` .

            You must use an expression, and the evaluated result should be a Boolean value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertyvariant.html#cfn-iotevents-alarmmodel-assetpropertyvariant-booleanvalue
            '''
            result = self._values.get("boolean_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def double_value(self) -> typing.Optional[builtins.str]:
            '''The asset property value is a double.

            You must use an expression, and the evaluated result should be a double.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertyvariant.html#cfn-iotevents-alarmmodel-assetpropertyvariant-doublevalue
            '''
            result = self._values.get("double_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def integer_value(self) -> typing.Optional[builtins.str]:
            '''The asset property value is an integer.

            You must use an expression, and the evaluated result should be an integer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertyvariant.html#cfn-iotevents-alarmmodel-assetpropertyvariant-integervalue
            '''
            result = self._values.get("integer_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''The asset property value is a string.

            You must use an expression, and the evaluated result should be a string.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertyvariant.html#cfn-iotevents-alarmmodel-assetpropertyvariant-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetPropertyVariantProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModel.DynamoDBProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hash_key_field": "hashKeyField",
            "hash_key_value": "hashKeyValue",
            "table_name": "tableName",
            "hash_key_type": "hashKeyType",
            "operation": "operation",
            "payload": "payload",
            "payload_field": "payloadField",
            "range_key_field": "rangeKeyField",
            "range_key_type": "rangeKeyType",
            "range_key_value": "rangeKeyValue",
        },
    )
    class DynamoDBProperty:
        def __init__(
            self,
            *,
            hash_key_field: builtins.str,
            hash_key_value: builtins.str,
            table_name: builtins.str,
            hash_key_type: typing.Optional[builtins.str] = None,
            operation: typing.Optional[builtins.str] = None,
            payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            payload_field: typing.Optional[builtins.str] = None,
            range_key_field: typing.Optional[builtins.str] = None,
            range_key_type: typing.Optional[builtins.str] = None,
            range_key_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines an action to write to the Amazon DynamoDB table that you created.

            The standard action payload contains all the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . One column of the DynamoDB table receives all attribute-value pairs in the payload that you specify.

            You must use expressions for all parameters in ``DynamoDBAction`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``hashKeyType`` parameter can be ``'STRING'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``hashKeyField`` parameter can be ``$input.GreenhouseInput.name`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``hashKeyValue`` parameter uses a substitution template.

            ``'${$input.GreenhouseInput.temperature * 6 / 5 + 32} in Fahrenheit'``

            - For a string concatenation, you must use ``+`` . A string concatenation can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``tableName`` parameter uses a string concatenation.

            ``'GreenhouseTemperatureTable ' + $input.GreenhouseInput.date``

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            If the defined payload type is a string, ``DynamoDBAction`` writes non-JSON data to the DynamoDB table as binary data. The DynamoDB console displays the data as Base64-encoded text. The value for the ``payloadField`` parameter is ``<payload-field>_raw`` .

            :param hash_key_field: The name of the hash key (also called the partition key). The ``hashKeyField`` value must match the partition key of the target DynamoDB table.
            :param hash_key_value: The value of the hash key (also called the partition key).
            :param table_name: The name of the DynamoDB table. The ``tableName`` value must match the table name of the target DynamoDB table.
            :param hash_key_type: The data type for the hash key (also called the partition key). You can specify the following values:. - ``'STRING'`` - The hash key is a string. - ``'NUMBER'`` - The hash key is a number. If you don't specify ``hashKeyType`` , the default value is ``'STRING'`` .
            :param operation: The type of operation to perform. You can specify the following values:. - ``'INSERT'`` - Insert data as a new item into the DynamoDB table. This item uses the specified hash key as a partition key. If you specified a range key, the item uses the range key as a sort key. - ``'UPDATE'`` - Update an existing item of the DynamoDB table with new data. This item's partition key must match the specified hash key. If you specified a range key, the range key must match the item's sort key. - ``'DELETE'`` - Delete an existing item of the DynamoDB table. This item's partition key must match the specified hash key. If you specified a range key, the range key must match the item's sort key. If you don't specify this parameter, AWS IoT Events triggers the ``'INSERT'`` operation.
            :param payload: Information needed to configure the payload. By default, AWS IoT Events generates a standard payload in JSON for any action. This action payload contains all attribute-value pairs that have the information about the detector model instance and the event triggered the action. To configure the action payload, you can use ``contentExpression`` .
            :param payload_field: The name of the DynamoDB column that receives the action payload. If you don't specify this parameter, the name of the DynamoDB column is ``payload`` .
            :param range_key_field: The name of the range key (also called the sort key). The ``rangeKeyField`` value must match the sort key of the target DynamoDB table.
            :param range_key_type: The data type for the range key (also called the sort key), You can specify the following values:. - ``'STRING'`` - The range key is a string. - ``'NUMBER'`` - The range key is number. If you don't specify ``rangeKeyField`` , the default value is ``'STRING'`` .
            :param range_key_value: The value of the range key (also called the sort key).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                dynamo_dBProperty = iotevents.CfnAlarmModel.DynamoDBProperty(
                    hash_key_field="hashKeyField",
                    hash_key_value="hashKeyValue",
                    table_name="tableName",
                
                    # the properties below are optional
                    hash_key_type="hashKeyType",
                    operation="operation",
                    payload=iotevents.CfnAlarmModel.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    ),
                    payload_field="payloadField",
                    range_key_field="rangeKeyField",
                    range_key_type="rangeKeyType",
                    range_key_value="rangeKeyValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1f81c4293cf593a2baa751af6dce60d7ff55bc34f6b1a9698bd2ad03b3f7e7e4)
                check_type(argname="argument hash_key_field", value=hash_key_field, expected_type=type_hints["hash_key_field"])
                check_type(argname="argument hash_key_value", value=hash_key_value, expected_type=type_hints["hash_key_value"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
                check_type(argname="argument hash_key_type", value=hash_key_type, expected_type=type_hints["hash_key_type"])
                check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
                check_type(argname="argument payload_field", value=payload_field, expected_type=type_hints["payload_field"])
                check_type(argname="argument range_key_field", value=range_key_field, expected_type=type_hints["range_key_field"])
                check_type(argname="argument range_key_type", value=range_key_type, expected_type=type_hints["range_key_type"])
                check_type(argname="argument range_key_value", value=range_key_value, expected_type=type_hints["range_key_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "hash_key_field": hash_key_field,
                "hash_key_value": hash_key_value,
                "table_name": table_name,
            }
            if hash_key_type is not None:
                self._values["hash_key_type"] = hash_key_type
            if operation is not None:
                self._values["operation"] = operation
            if payload is not None:
                self._values["payload"] = payload
            if payload_field is not None:
                self._values["payload_field"] = payload_field
            if range_key_field is not None:
                self._values["range_key_field"] = range_key_field
            if range_key_type is not None:
                self._values["range_key_type"] = range_key_type
            if range_key_value is not None:
                self._values["range_key_value"] = range_key_value

        @builtins.property
        def hash_key_field(self) -> builtins.str:
            '''The name of the hash key (also called the partition key).

            The ``hashKeyField`` value must match the partition key of the target DynamoDB table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html#cfn-iotevents-alarmmodel-dynamodb-hashkeyfield
            '''
            result = self._values.get("hash_key_field")
            assert result is not None, "Required property 'hash_key_field' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def hash_key_value(self) -> builtins.str:
            '''The value of the hash key (also called the partition key).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html#cfn-iotevents-alarmmodel-dynamodb-hashkeyvalue
            '''
            result = self._values.get("hash_key_value")
            assert result is not None, "Required property 'hash_key_value' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def table_name(self) -> builtins.str:
            '''The name of the DynamoDB table.

            The ``tableName`` value must match the table name of the target DynamoDB table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html#cfn-iotevents-alarmmodel-dynamodb-tablename
            '''
            result = self._values.get("table_name")
            assert result is not None, "Required property 'table_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def hash_key_type(self) -> typing.Optional[builtins.str]:
            '''The data type for the hash key (also called the partition key). You can specify the following values:.

            - ``'STRING'`` - The hash key is a string.
            - ``'NUMBER'`` - The hash key is a number.

            If you don't specify ``hashKeyType`` , the default value is ``'STRING'`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html#cfn-iotevents-alarmmodel-dynamodb-hashkeytype
            '''
            result = self._values.get("hash_key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operation(self) -> typing.Optional[builtins.str]:
            '''The type of operation to perform. You can specify the following values:.

            - ``'INSERT'`` - Insert data as a new item into the DynamoDB table. This item uses the specified hash key as a partition key. If you specified a range key, the item uses the range key as a sort key.
            - ``'UPDATE'`` - Update an existing item of the DynamoDB table with new data. This item's partition key must match the specified hash key. If you specified a range key, the range key must match the item's sort key.
            - ``'DELETE'`` - Delete an existing item of the DynamoDB table. This item's partition key must match the specified hash key. If you specified a range key, the range key must match the item's sort key.

            If you don't specify this parameter, AWS IoT Events triggers the ``'INSERT'`` operation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html#cfn-iotevents-alarmmodel-dynamodb-operation
            '''
            result = self._values.get("operation")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.PayloadProperty"]]:
            '''Information needed to configure the payload.

            By default, AWS IoT Events generates a standard payload in JSON for any action. This action payload contains all attribute-value pairs that have the information about the detector model instance and the event triggered the action. To configure the action payload, you can use ``contentExpression`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html#cfn-iotevents-alarmmodel-dynamodb-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.PayloadProperty"]], result)

        @builtins.property
        def payload_field(self) -> typing.Optional[builtins.str]:
            '''The name of the DynamoDB column that receives the action payload.

            If you don't specify this parameter, the name of the DynamoDB column is ``payload`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html#cfn-iotevents-alarmmodel-dynamodb-payloadfield
            '''
            result = self._values.get("payload_field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def range_key_field(self) -> typing.Optional[builtins.str]:
            '''The name of the range key (also called the sort key).

            The ``rangeKeyField`` value must match the sort key of the target DynamoDB table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html#cfn-iotevents-alarmmodel-dynamodb-rangekeyfield
            '''
            result = self._values.get("range_key_field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def range_key_type(self) -> typing.Optional[builtins.str]:
            '''The data type for the range key (also called the sort key), You can specify the following values:.

            - ``'STRING'`` - The range key is a string.
            - ``'NUMBER'`` - The range key is number.

            If you don't specify ``rangeKeyField`` , the default value is ``'STRING'`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html#cfn-iotevents-alarmmodel-dynamodb-rangekeytype
            '''
            result = self._values.get("range_key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def range_key_value(self) -> typing.Optional[builtins.str]:
            '''The value of the range key (also called the sort key).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html#cfn-iotevents-alarmmodel-dynamodb-rangekeyvalue
            '''
            result = self._values.get("range_key_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamoDBProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModel.DynamoDBv2Property",
        jsii_struct_bases=[],
        name_mapping={"table_name": "tableName", "payload": "payload"},
    )
    class DynamoDBv2Property:
        def __init__(
            self,
            *,
            table_name: builtins.str,
            payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Defines an action to write to the Amazon DynamoDB table that you created.

            The default action payload contains all the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . A separate column of the DynamoDB table receives one attribute-value pair in the payload that you specify.

            You must use expressions for all parameters in ``DynamoDBv2Action`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``tableName`` parameter can be ``'GreenhouseTemperatureTable'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``tableName`` parameter can be ``$variable.ddbtableName`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``contentExpression`` parameter in ``Payload`` uses a substitution template.

            ``'{\\"sensorID\\": \\"${$input.GreenhouseInput.sensor_id}\\", \\"temperature\\": \\"${$input.GreenhouseInput.temperature * 9 / 5 + 32}\\"}'``

            - For a string concatenation, you must use ``+`` . A string concatenation can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``tableName`` parameter uses a string concatenation.

            ``'GreenhouseTemperatureTable ' + $input.GreenhouseInput.date``

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            The value for the ``type`` parameter in ``Payload`` must be ``JSON`` .

            :param table_name: The name of the DynamoDB table.
            :param payload: ``CfnAlarmModel.DynamoDBv2Property.Payload``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodbv2.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                dynamo_dBv2_property = iotevents.CfnAlarmModel.DynamoDBv2Property(
                    table_name="tableName",
                
                    # the properties below are optional
                    payload=iotevents.CfnAlarmModel.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a2bbd9176a2096155ec8c0b345254a576eefa26b05268c411a5b4e56f972eaf9)
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "table_name": table_name,
            }
            if payload is not None:
                self._values["payload"] = payload

        @builtins.property
        def table_name(self) -> builtins.str:
            '''The name of the DynamoDB table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodbv2.html#cfn-iotevents-alarmmodel-dynamodbv2-tablename
            '''
            result = self._values.get("table_name")
            assert result is not None, "Required property 'table_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.PayloadProperty"]]:
            '''``CfnAlarmModel.DynamoDBv2Property.Payload``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodbv2.html#cfn-iotevents-alarmmodel-dynamodbv2-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.PayloadProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamoDBv2Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModel.FirehoseProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delivery_stream_name": "deliveryStreamName",
            "payload": "payload",
            "separator": "separator",
        },
    )
    class FirehoseProperty:
        def __init__(
            self,
            *,
            delivery_stream_name: builtins.str,
            payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            separator: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Sends information about the detector model instance and the event that triggered the action to an Amazon Kinesis Data Firehose delivery stream.

            :param delivery_stream_name: The name of the Kinesis Data Firehose delivery stream where the data is written.
            :param payload: You can configure the action payload when you send a message to an Amazon Kinesis Data Firehose delivery stream.
            :param separator: A character separator that is used to separate records written to the Kinesis Data Firehose delivery stream. Valid values are: '\\n' (newline), '\\t' (tab), '\\r\\n' (Windows newline), ',' (comma).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-firehose.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                firehose_property = iotevents.CfnAlarmModel.FirehoseProperty(
                    delivery_stream_name="deliveryStreamName",
                
                    # the properties below are optional
                    payload=iotevents.CfnAlarmModel.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    ),
                    separator="separator"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__97c1dc45e15d1d1de750460f656506de609e77b9f5db1e68ae9dc159c6ff274c)
                check_type(argname="argument delivery_stream_name", value=delivery_stream_name, expected_type=type_hints["delivery_stream_name"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
                check_type(argname="argument separator", value=separator, expected_type=type_hints["separator"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "delivery_stream_name": delivery_stream_name,
            }
            if payload is not None:
                self._values["payload"] = payload
            if separator is not None:
                self._values["separator"] = separator

        @builtins.property
        def delivery_stream_name(self) -> builtins.str:
            '''The name of the Kinesis Data Firehose delivery stream where the data is written.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-firehose.html#cfn-iotevents-alarmmodel-firehose-deliverystreamname
            '''
            result = self._values.get("delivery_stream_name")
            assert result is not None, "Required property 'delivery_stream_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.PayloadProperty"]]:
            '''You can configure the action payload when you send a message to an Amazon Kinesis Data Firehose delivery stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-firehose.html#cfn-iotevents-alarmmodel-firehose-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.PayloadProperty"]], result)

        @builtins.property
        def separator(self) -> typing.Optional[builtins.str]:
            '''A character separator that is used to separate records written to the Kinesis Data Firehose delivery stream.

            Valid values are: '\\n' (newline), '\\t' (tab), '\\r\\n' (Windows newline), ',' (comma).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-firehose.html#cfn-iotevents-alarmmodel-firehose-separator
            '''
            result = self._values.get("separator")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FirehoseProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModel.InitializationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"disabled_on_initialization": "disabledOnInitialization"},
    )
    class InitializationConfigurationProperty:
        def __init__(
            self,
            *,
            disabled_on_initialization: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        ) -> None:
            '''Specifies the default alarm state.

            The configuration applies to all alarms that were created based on this alarm model.

            :param disabled_on_initialization: The value must be ``TRUE`` or ``FALSE`` . If ``FALSE`` , all alarm instances created based on the alarm model are activated. The default value is ``TRUE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-initializationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                initialization_configuration_property = iotevents.CfnAlarmModel.InitializationConfigurationProperty(
                    disabled_on_initialization=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__95837c1c4560c728492c3735f77080263999005659248c85ab38116efe8c98f1)
                check_type(argname="argument disabled_on_initialization", value=disabled_on_initialization, expected_type=type_hints["disabled_on_initialization"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "disabled_on_initialization": disabled_on_initialization,
            }

        @builtins.property
        def disabled_on_initialization(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''The value must be ``TRUE`` or ``FALSE`` .

            If ``FALSE`` , all alarm instances created based on the alarm model are activated. The default value is ``TRUE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-initializationconfiguration.html#cfn-iotevents-alarmmodel-initializationconfiguration-disabledoninitialization
            '''
            result = self._values.get("disabled_on_initialization")
            assert result is not None, "Required property 'disabled_on_initialization' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InitializationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModel.IotEventsProperty",
        jsii_struct_bases=[],
        name_mapping={"input_name": "inputName", "payload": "payload"},
    )
    class IotEventsProperty:
        def __init__(
            self,
            *,
            input_name: builtins.str,
            payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Sends an AWS IoT Events input, passing in information about the detector model instance and the event that triggered the action.

            :param input_name: The name of the AWS IoT Events input where the data is sent.
            :param payload: You can configure the action payload when you send a message to an AWS IoT Events input.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iotevents.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                iot_events_property = iotevents.CfnAlarmModel.IotEventsProperty(
                    input_name="inputName",
                
                    # the properties below are optional
                    payload=iotevents.CfnAlarmModel.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__87a4b97990788585da844a043b73294f787a5e2a0dd55e480c1f4ea48e904549)
                check_type(argname="argument input_name", value=input_name, expected_type=type_hints["input_name"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "input_name": input_name,
            }
            if payload is not None:
                self._values["payload"] = payload

        @builtins.property
        def input_name(self) -> builtins.str:
            '''The name of the AWS IoT Events input where the data is sent.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iotevents.html#cfn-iotevents-alarmmodel-iotevents-inputname
            '''
            result = self._values.get("input_name")
            assert result is not None, "Required property 'input_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.PayloadProperty"]]:
            '''You can configure the action payload when you send a message to an AWS IoT Events input.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iotevents.html#cfn-iotevents-alarmmodel-iotevents-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.PayloadProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IotEventsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModel.IotSiteWiseProperty",
        jsii_struct_bases=[],
        name_mapping={
            "asset_id": "assetId",
            "entry_id": "entryId",
            "property_alias": "propertyAlias",
            "property_id": "propertyId",
            "property_value": "propertyValue",
        },
    )
    class IotSiteWiseProperty:
        def __init__(
            self,
            *,
            asset_id: typing.Optional[builtins.str] = None,
            entry_id: typing.Optional[builtins.str] = None,
            property_alias: typing.Optional[builtins.str] = None,
            property_id: typing.Optional[builtins.str] = None,
            property_value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.AssetPropertyValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Sends information about the detector model instance and the event that triggered the action to a specified asset property in AWS IoT SiteWise .

            You must use expressions for all parameters in ``IotSiteWiseAction`` . The expressions accept literals, operators, functions, references, and substitutions templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``propertyAlias`` parameter can be ``'/company/windfarm/3/turbine/7/temperature'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``assetId`` parameter can be ``$input.TurbineInput.assetId1`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``propertyAlias`` parameter uses a substitution template.

            ``'company/windfarm/${$input.TemperatureInput.sensorData.windfarmID}/turbine/ ${$input.TemperatureInput.sensorData.turbineID}/temperature'``

            You must specify either ``propertyAlias`` or both ``assetId`` and ``propertyId`` to identify the target asset property in AWS IoT SiteWise .

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            :param asset_id: The ID of the asset that has the specified property.
            :param entry_id: A unique identifier for this entry. You can use the entry ID to track which data entry causes an error in case of failure. The default is a new unique identifier.
            :param property_alias: The alias of the asset property.
            :param property_id: The ID of the asset property.
            :param property_value: The value to send to the asset property. This value contains timestamp, quality, and value (TQV) information.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iotsitewise.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                iot_site_wise_property = iotevents.CfnAlarmModel.IotSiteWiseProperty(
                    asset_id="assetId",
                    entry_id="entryId",
                    property_alias="propertyAlias",
                    property_id="propertyId",
                    property_value=iotevents.CfnAlarmModel.AssetPropertyValueProperty(
                        value=iotevents.CfnAlarmModel.AssetPropertyVariantProperty(
                            boolean_value="booleanValue",
                            double_value="doubleValue",
                            integer_value="integerValue",
                            string_value="stringValue"
                        ),
                
                        # the properties below are optional
                        quality="quality",
                        timestamp=iotevents.CfnAlarmModel.AssetPropertyTimestampProperty(
                            time_in_seconds="timeInSeconds",
                
                            # the properties below are optional
                            offset_in_nanos="offsetInNanos"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cfa1d4e0b76e794ba751e7417e9d24ad51b6e74bbe555ee58e958f52351df9ac)
                check_type(argname="argument asset_id", value=asset_id, expected_type=type_hints["asset_id"])
                check_type(argname="argument entry_id", value=entry_id, expected_type=type_hints["entry_id"])
                check_type(argname="argument property_alias", value=property_alias, expected_type=type_hints["property_alias"])
                check_type(argname="argument property_id", value=property_id, expected_type=type_hints["property_id"])
                check_type(argname="argument property_value", value=property_value, expected_type=type_hints["property_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if asset_id is not None:
                self._values["asset_id"] = asset_id
            if entry_id is not None:
                self._values["entry_id"] = entry_id
            if property_alias is not None:
                self._values["property_alias"] = property_alias
            if property_id is not None:
                self._values["property_id"] = property_id
            if property_value is not None:
                self._values["property_value"] = property_value

        @builtins.property
        def asset_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the asset that has the specified property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iotsitewise.html#cfn-iotevents-alarmmodel-iotsitewise-assetid
            '''
            result = self._values.get("asset_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def entry_id(self) -> typing.Optional[builtins.str]:
            '''A unique identifier for this entry.

            You can use the entry ID to track which data entry causes an error in case of failure. The default is a new unique identifier.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iotsitewise.html#cfn-iotevents-alarmmodel-iotsitewise-entryid
            '''
            result = self._values.get("entry_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_alias(self) -> typing.Optional[builtins.str]:
            '''The alias of the asset property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iotsitewise.html#cfn-iotevents-alarmmodel-iotsitewise-propertyalias
            '''
            result = self._values.get("property_alias")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the asset property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iotsitewise.html#cfn-iotevents-alarmmodel-iotsitewise-propertyid
            '''
            result = self._values.get("property_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.AssetPropertyValueProperty"]]:
            '''The value to send to the asset property.

            This value contains timestamp, quality, and value (TQV) information.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iotsitewise.html#cfn-iotevents-alarmmodel-iotsitewise-propertyvalue
            '''
            result = self._values.get("property_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.AssetPropertyValueProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IotSiteWiseProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModel.IotTopicPublishProperty",
        jsii_struct_bases=[],
        name_mapping={"mqtt_topic": "mqttTopic", "payload": "payload"},
    )
    class IotTopicPublishProperty:
        def __init__(
            self,
            *,
            mqtt_topic: builtins.str,
            payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information required to publish the MQTT message through the AWS IoT message broker.

            :param mqtt_topic: The MQTT topic of the message. You can use a string expression that includes variables ( ``$variable.<variable-name>`` ) and input values ( ``$input.<input-name>.<path-to-datum>`` ) as the topic string.
            :param payload: You can configure the action payload when you publish a message to an AWS IoT Core topic.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iottopicpublish.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                iot_topic_publish_property = iotevents.CfnAlarmModel.IotTopicPublishProperty(
                    mqtt_topic="mqttTopic",
                
                    # the properties below are optional
                    payload=iotevents.CfnAlarmModel.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__211c4f79f8cc0420aac5fd9faee1d93e51d8e055861a16ba062be2824488d4ce)
                check_type(argname="argument mqtt_topic", value=mqtt_topic, expected_type=type_hints["mqtt_topic"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "mqtt_topic": mqtt_topic,
            }
            if payload is not None:
                self._values["payload"] = payload

        @builtins.property
        def mqtt_topic(self) -> builtins.str:
            '''The MQTT topic of the message.

            You can use a string expression that includes variables ( ``$variable.<variable-name>`` ) and input values ( ``$input.<input-name>.<path-to-datum>`` ) as the topic string.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iottopicpublish.html#cfn-iotevents-alarmmodel-iottopicpublish-mqtttopic
            '''
            result = self._values.get("mqtt_topic")
            assert result is not None, "Required property 'mqtt_topic' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.PayloadProperty"]]:
            '''You can configure the action payload when you publish a message to an AWS IoT Core topic.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iottopicpublish.html#cfn-iotevents-alarmmodel-iottopicpublish-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.PayloadProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IotTopicPublishProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModel.LambdaProperty",
        jsii_struct_bases=[],
        name_mapping={"function_arn": "functionArn", "payload": "payload"},
    )
    class LambdaProperty:
        def __init__(
            self,
            *,
            function_arn: builtins.str,
            payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Calls a Lambda function, passing in information about the detector model instance and the event that triggered the action.

            :param function_arn: The ARN of the Lambda function that is executed.
            :param payload: You can configure the action payload when you send a message to a Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-lambda.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                lambda_property = iotevents.CfnAlarmModel.LambdaProperty(
                    function_arn="functionArn",
                
                    # the properties below are optional
                    payload=iotevents.CfnAlarmModel.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dca9296bdd50c0b157abb60b919efee87de8d50dfa3ddb183568f6f79ded785a)
                check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "function_arn": function_arn,
            }
            if payload is not None:
                self._values["payload"] = payload

        @builtins.property
        def function_arn(self) -> builtins.str:
            '''The ARN of the Lambda function that is executed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-lambda.html#cfn-iotevents-alarmmodel-lambda-functionarn
            '''
            result = self._values.get("function_arn")
            assert result is not None, "Required property 'function_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.PayloadProperty"]]:
            '''You can configure the action payload when you send a message to a Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-lambda.html#cfn-iotevents-alarmmodel-lambda-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.PayloadProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModel.PayloadProperty",
        jsii_struct_bases=[],
        name_mapping={"content_expression": "contentExpression", "type": "type"},
    )
    class PayloadProperty:
        def __init__(
            self,
            *,
            content_expression: builtins.str,
            type: builtins.str,
        ) -> None:
            '''Information needed to configure the payload.

            By default, AWS IoT Events generates a standard payload in JSON for any action. This action payload contains all attribute-value pairs that have the information about the detector model instance and the event triggered the action. To configure the action payload, you can use ``contentExpression`` .

            :param content_expression: The content of the payload. You can use a string expression that includes quoted strings ( ``'<string>'`` ), variables ( ``$variable.<variable-name>`` ), input values ( ``$input.<input-name>.<path-to-datum>`` ), string concatenations, and quoted strings that contain ``${}`` as the content. The recommended maximum size of a content expression is 1 KB.
            :param type: The value of the payload type can be either ``STRING`` or ``JSON`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-payload.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                payload_property = iotevents.CfnAlarmModel.PayloadProperty(
                    content_expression="contentExpression",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a87051e63342027aa5b09d2eef106ab646561f61a6373d55f1ad3c76d0f5135d)
                check_type(argname="argument content_expression", value=content_expression, expected_type=type_hints["content_expression"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "content_expression": content_expression,
                "type": type,
            }

        @builtins.property
        def content_expression(self) -> builtins.str:
            '''The content of the payload.

            You can use a string expression that includes quoted strings ( ``'<string>'`` ), variables ( ``$variable.<variable-name>`` ), input values ( ``$input.<input-name>.<path-to-datum>`` ), string concatenations, and quoted strings that contain ``${}`` as the content. The recommended maximum size of a content expression is 1 KB.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-payload.html#cfn-iotevents-alarmmodel-payload-contentexpression
            '''
            result = self._values.get("content_expression")
            assert result is not None, "Required property 'content_expression' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def type(self) -> builtins.str:
            '''The value of the payload type can be either ``STRING`` or ``JSON`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-payload.html#cfn-iotevents-alarmmodel-payload-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PayloadProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModel.SimpleRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "comparison_operator": "comparisonOperator",
            "input_property": "inputProperty",
            "threshold": "threshold",
        },
    )
    class SimpleRuleProperty:
        def __init__(
            self,
            *,
            comparison_operator: builtins.str,
            input_property: builtins.str,
            threshold: builtins.str,
        ) -> None:
            '''A rule that compares an input property value to a threshold value with a comparison operator.

            :param comparison_operator: The comparison operator.
            :param input_property: The value on the left side of the comparison operator. You can specify an AWS IoT Events input attribute as an input property.
            :param threshold: The value on the right side of the comparison operator. You can enter a number or specify an AWS IoT Events input attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-simplerule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                simple_rule_property = iotevents.CfnAlarmModel.SimpleRuleProperty(
                    comparison_operator="comparisonOperator",
                    input_property="inputProperty",
                    threshold="threshold"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bf82e9fa5c332ee501ab6e3f649c8952741ec85ee7790640a9f0ac469ba86556)
                check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
                check_type(argname="argument input_property", value=input_property, expected_type=type_hints["input_property"])
                check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "comparison_operator": comparison_operator,
                "input_property": input_property,
                "threshold": threshold,
            }

        @builtins.property
        def comparison_operator(self) -> builtins.str:
            '''The comparison operator.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-simplerule.html#cfn-iotevents-alarmmodel-simplerule-comparisonoperator
            '''
            result = self._values.get("comparison_operator")
            assert result is not None, "Required property 'comparison_operator' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def input_property(self) -> builtins.str:
            '''The value on the left side of the comparison operator.

            You can specify an AWS IoT Events input attribute as an input property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-simplerule.html#cfn-iotevents-alarmmodel-simplerule-inputproperty
            '''
            result = self._values.get("input_property")
            assert result is not None, "Required property 'input_property' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def threshold(self) -> builtins.str:
            '''The value on the right side of the comparison operator.

            You can enter a number or specify an AWS IoT Events input attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-simplerule.html#cfn-iotevents-alarmmodel-simplerule-threshold
            '''
            result = self._values.get("threshold")
            assert result is not None, "Required property 'threshold' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SimpleRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModel.SnsProperty",
        jsii_struct_bases=[],
        name_mapping={"target_arn": "targetArn", "payload": "payload"},
    )
    class SnsProperty:
        def __init__(
            self,
            *,
            target_arn: builtins.str,
            payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information required to publish the Amazon SNS message.

            :param target_arn: The ARN of the Amazon SNS target where the message is sent.
            :param payload: You can configure the action payload when you send a message as an Amazon SNS push notification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-sns.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                sns_property = iotevents.CfnAlarmModel.SnsProperty(
                    target_arn="targetArn",
                
                    # the properties below are optional
                    payload=iotevents.CfnAlarmModel.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__de8f1c762e8184bc32d3df2aaa983a732404d12720e10ee361b3db524b73bf59)
                check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "target_arn": target_arn,
            }
            if payload is not None:
                self._values["payload"] = payload

        @builtins.property
        def target_arn(self) -> builtins.str:
            '''The ARN of the Amazon SNS target where the message is sent.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-sns.html#cfn-iotevents-alarmmodel-sns-targetarn
            '''
            result = self._values.get("target_arn")
            assert result is not None, "Required property 'target_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.PayloadProperty"]]:
            '''You can configure the action payload when you send a message as an Amazon SNS push notification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-sns.html#cfn-iotevents-alarmmodel-sns-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.PayloadProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModel.SqsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "queue_url": "queueUrl",
            "payload": "payload",
            "use_base64": "useBase64",
        },
    )
    class SqsProperty:
        def __init__(
            self,
            *,
            queue_url: builtins.str,
            payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAlarmModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            use_base64: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Sends information about the detector model instance and the event that triggered the action to an Amazon SQS queue.

            :param queue_url: The URL of the SQS queue where the data is written.
            :param payload: You can configure the action payload when you send a message to an Amazon SQS queue.
            :param use_base64: Set this to TRUE if you want the data to be base-64 encoded before it is written to the queue. Otherwise, set this to FALSE.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-sqs.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                sqs_property = iotevents.CfnAlarmModel.SqsProperty(
                    queue_url="queueUrl",
                
                    # the properties below are optional
                    payload=iotevents.CfnAlarmModel.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    ),
                    use_base64=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b518d32ae21e79224630c149b5b9ddab07513e3db392536b138607d09e3ad55)
                check_type(argname="argument queue_url", value=queue_url, expected_type=type_hints["queue_url"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
                check_type(argname="argument use_base64", value=use_base64, expected_type=type_hints["use_base64"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "queue_url": queue_url,
            }
            if payload is not None:
                self._values["payload"] = payload
            if use_base64 is not None:
                self._values["use_base64"] = use_base64

        @builtins.property
        def queue_url(self) -> builtins.str:
            '''The URL of the SQS queue where the data is written.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-sqs.html#cfn-iotevents-alarmmodel-sqs-queueurl
            '''
            result = self._values.get("queue_url")
            assert result is not None, "Required property 'queue_url' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.PayloadProperty"]]:
            '''You can configure the action payload when you send a message to an Amazon SQS queue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-sqs.html#cfn-iotevents-alarmmodel-sqs-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAlarmModel.PayloadProperty"]], result)

        @builtins.property
        def use_base64(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Set this to TRUE if you want the data to be base-64 encoded before it is written to the queue.

            Otherwise, set this to FALSE.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-sqs.html#cfn-iotevents-alarmmodel-sqs-usebase64
            '''
            result = self._values.get("use_base64")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SqsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iotevents.CfnAlarmModelProps",
    jsii_struct_bases=[],
    name_mapping={
        "alarm_rule": "alarmRule",
        "role_arn": "roleArn",
        "alarm_capabilities": "alarmCapabilities",
        "alarm_event_actions": "alarmEventActions",
        "alarm_model_description": "alarmModelDescription",
        "alarm_model_name": "alarmModelName",
        "key": "key",
        "severity": "severity",
        "tags": "tags",
    },
)
class CfnAlarmModelProps:
    def __init__(
        self,
        *,
        alarm_rule: typing.Union[typing.Union[CfnAlarmModel.AlarmRuleProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        role_arn: builtins.str,
        alarm_capabilities: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.AlarmCapabilitiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        alarm_event_actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.AlarmEventActionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        alarm_model_description: typing.Optional[builtins.str] = None,
        alarm_model_name: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        severity: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAlarmModel``.

        :param alarm_rule: Defines when your alarm is invoked.
        :param role_arn: The ARN of the IAM role that allows the alarm to perform actions and access AWS resources. For more information, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param alarm_capabilities: Contains the configuration information of alarm state changes.
        :param alarm_event_actions: Contains information about one or more alarm actions.
        :param alarm_model_description: The description of the alarm model.
        :param alarm_model_name: The name of the alarm model.
        :param key: An input attribute used as a key to create an alarm. AWS IoT Events routes `inputs <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Input.html>`_ associated with this key to the alarm.
        :param severity: A non-negative integer that reflects the severity level of the alarm.
        :param tags: A list of key-value pairs that contain metadata for the alarm model. The tags help you manage the alarm model. For more information, see `Tagging your AWS IoT Events resources <https://docs.aws.amazon.com/iotevents/latest/developerguide/tagging-iotevents.html>`_ in the *AWS IoT Events Developer Guide* . You can create up to 50 tags for one alarm model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iotevents as iotevents
            
            cfn_alarm_model_props = iotevents.CfnAlarmModelProps(
                alarm_rule=iotevents.CfnAlarmModel.AlarmRuleProperty(
                    simple_rule=iotevents.CfnAlarmModel.SimpleRuleProperty(
                        comparison_operator="comparisonOperator",
                        input_property="inputProperty",
                        threshold="threshold"
                    )
                ),
                role_arn="roleArn",
            
                # the properties below are optional
                alarm_capabilities=iotevents.CfnAlarmModel.AlarmCapabilitiesProperty(
                    acknowledge_flow=iotevents.CfnAlarmModel.AcknowledgeFlowProperty(
                        enabled=False
                    ),
                    initialization_configuration=iotevents.CfnAlarmModel.InitializationConfigurationProperty(
                        disabled_on_initialization=False
                    )
                ),
                alarm_event_actions=iotevents.CfnAlarmModel.AlarmEventActionsProperty(
                    alarm_actions=[iotevents.CfnAlarmModel.AlarmActionProperty(
                        dynamo_db=iotevents.CfnAlarmModel.DynamoDBProperty(
                            hash_key_field="hashKeyField",
                            hash_key_value="hashKeyValue",
                            table_name="tableName",
            
                            # the properties below are optional
                            hash_key_type="hashKeyType",
                            operation="operation",
                            payload=iotevents.CfnAlarmModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            payload_field="payloadField",
                            range_key_field="rangeKeyField",
                            range_key_type="rangeKeyType",
                            range_key_value="rangeKeyValue"
                        ),
                        dynamo_dBv2=iotevents.CfnAlarmModel.DynamoDBv2Property(
                            table_name="tableName",
            
                            # the properties below are optional
                            payload=iotevents.CfnAlarmModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        firehose=iotevents.CfnAlarmModel.FirehoseProperty(
                            delivery_stream_name="deliveryStreamName",
            
                            # the properties below are optional
                            payload=iotevents.CfnAlarmModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            separator="separator"
                        ),
                        iot_events=iotevents.CfnAlarmModel.IotEventsProperty(
                            input_name="inputName",
            
                            # the properties below are optional
                            payload=iotevents.CfnAlarmModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        iot_site_wise=iotevents.CfnAlarmModel.IotSiteWiseProperty(
                            asset_id="assetId",
                            entry_id="entryId",
                            property_alias="propertyAlias",
                            property_id="propertyId",
                            property_value=iotevents.CfnAlarmModel.AssetPropertyValueProperty(
                                value=iotevents.CfnAlarmModel.AssetPropertyVariantProperty(
                                    boolean_value="booleanValue",
                                    double_value="doubleValue",
                                    integer_value="integerValue",
                                    string_value="stringValue"
                                ),
            
                                # the properties below are optional
                                quality="quality",
                                timestamp=iotevents.CfnAlarmModel.AssetPropertyTimestampProperty(
                                    time_in_seconds="timeInSeconds",
            
                                    # the properties below are optional
                                    offset_in_nanos="offsetInNanos"
                                )
                            )
                        ),
                        iot_topic_publish=iotevents.CfnAlarmModel.IotTopicPublishProperty(
                            mqtt_topic="mqttTopic",
            
                            # the properties below are optional
                            payload=iotevents.CfnAlarmModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        lambda_=iotevents.CfnAlarmModel.LambdaProperty(
                            function_arn="functionArn",
            
                            # the properties below are optional
                            payload=iotevents.CfnAlarmModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        sns=iotevents.CfnAlarmModel.SnsProperty(
                            target_arn="targetArn",
            
                            # the properties below are optional
                            payload=iotevents.CfnAlarmModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        sqs=iotevents.CfnAlarmModel.SqsProperty(
                            queue_url="queueUrl",
            
                            # the properties below are optional
                            payload=iotevents.CfnAlarmModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            use_base64=False
                        )
                    )]
                ),
                alarm_model_description="alarmModelDescription",
                alarm_model_name="alarmModelName",
                key="key",
                severity=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__858c6d54605adf535894fac594bf100a6ec4bdd7a972ce9162352f95b9934e09)
            check_type(argname="argument alarm_rule", value=alarm_rule, expected_type=type_hints["alarm_rule"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument alarm_capabilities", value=alarm_capabilities, expected_type=type_hints["alarm_capabilities"])
            check_type(argname="argument alarm_event_actions", value=alarm_event_actions, expected_type=type_hints["alarm_event_actions"])
            check_type(argname="argument alarm_model_description", value=alarm_model_description, expected_type=type_hints["alarm_model_description"])
            check_type(argname="argument alarm_model_name", value=alarm_model_name, expected_type=type_hints["alarm_model_name"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alarm_rule": alarm_rule,
            "role_arn": role_arn,
        }
        if alarm_capabilities is not None:
            self._values["alarm_capabilities"] = alarm_capabilities
        if alarm_event_actions is not None:
            self._values["alarm_event_actions"] = alarm_event_actions
        if alarm_model_description is not None:
            self._values["alarm_model_description"] = alarm_model_description
        if alarm_model_name is not None:
            self._values["alarm_model_name"] = alarm_model_name
        if key is not None:
            self._values["key"] = key
        if severity is not None:
            self._values["severity"] = severity
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def alarm_rule(
        self,
    ) -> typing.Union[CfnAlarmModel.AlarmRuleProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''Defines when your alarm is invoked.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-alarmrule
        '''
        result = self._values.get("alarm_rule")
        assert result is not None, "Required property 'alarm_rule' is missing"
        return typing.cast(typing.Union[CfnAlarmModel.AlarmRuleProperty, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''The ARN of the IAM role that allows the alarm to perform actions and access AWS resources.

        For more information, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-rolearn
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alarm_capabilities(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAlarmModel.AlarmCapabilitiesProperty]]:
        '''Contains the configuration information of alarm state changes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-alarmcapabilities
        '''
        result = self._values.get("alarm_capabilities")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAlarmModel.AlarmCapabilitiesProperty]], result)

    @builtins.property
    def alarm_event_actions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAlarmModel.AlarmEventActionsProperty]]:
        '''Contains information about one or more alarm actions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-alarmeventactions
        '''
        result = self._values.get("alarm_event_actions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAlarmModel.AlarmEventActionsProperty]], result)

    @builtins.property
    def alarm_model_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-alarmmodeldescription
        '''
        result = self._values.get("alarm_model_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_model_name(self) -> typing.Optional[builtins.str]:
        '''The name of the alarm model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-alarmmodelname
        '''
        result = self._values.get("alarm_model_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''An input attribute used as a key to create an alarm.

        AWS IoT Events routes `inputs <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Input.html>`_ associated with this key to the alarm.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-key
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def severity(self) -> typing.Optional[jsii.Number]:
        '''A non-negative integer that reflects the severity level of the alarm.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-severity
        '''
        result = self._values.get("severity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A list of key-value pairs that contain metadata for the alarm model.

        The tags help you manage the alarm model. For more information, see `Tagging your AWS IoT Events resources <https://docs.aws.amazon.com/iotevents/latest/developerguide/tagging-iotevents.html>`_ in the *AWS IoT Events Developer Guide* .

        You can create up to 50 tags for one alarm model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAlarmModelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnDetectorModel(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel",
):
    '''A CloudFormation ``AWS::IoTEvents::DetectorModel``.

    The AWS::IoTEvents::DetectorModel resource creates a detector model. You create a *detector model* (a model of your equipment or process) using *states* . For each state, you define conditional (Boolean) logic that evaluates the incoming inputs to detect significant events. When an event is detected, it can change the state or trigger custom-built or predefined actions using other AWS services. You can define additional events that trigger actions when entering or exiting a state and, optionally, when a condition is met. For more information, see `How to Use AWS IoT Events <https://docs.aws.amazon.com/iotevents/latest/developerguide/how-to-use-iotevents.html>`_ in the *AWS IoT Events Developer Guide* .
    .. epigraph::

       When you successfully update a detector model (using the AWS IoT Events console, AWS IoT Events API or CLI commands, or AWS CloudFormation ) all detector instances created by the model are reset to their initial states. (The detector's ``state`` , and the values of any variables and timers are reset.)

       When you successfully update a detector model (using the AWS IoT Events console, AWS IoT Events API or CLI commands, or AWS CloudFormation ) the version number of the detector model is incremented. (A detector model with version number 1 before the update has version number 2 after the update succeeds.)

       If you attempt to update a detector model using AWS CloudFormation and the update does not succeed, the system may, in some cases, restore the original detector model. When this occurs, the detector model's version is incremented twice (for example, from version 1 to version 3) and the detector instances are reset.

       Also, be aware that if you attempt to update several detector models at once using AWS CloudFormation , some updates may succeed and others fail. In this case, the effects on each detector model's detector instances and version number depend on whether the update succeeded or failed, with the results as stated.

    :cloudformationResource: AWS::IoTEvents::DetectorModel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iotevents as iotevents
        
        cfn_detector_model = iotevents.CfnDetectorModel(self, "MyCfnDetectorModel",
            detector_model_definition=iotevents.CfnDetectorModel.DetectorModelDefinitionProperty(
                initial_state_name="initialStateName",
                states=[iotevents.CfnDetectorModel.StateProperty(
                    state_name="stateName",
        
                    # the properties below are optional
                    on_enter=iotevents.CfnDetectorModel.OnEnterProperty(
                        events=[iotevents.CfnDetectorModel.EventProperty(
                            event_name="eventName",
        
                            # the properties below are optional
                            actions=[iotevents.CfnDetectorModel.ActionProperty(
                                clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                                    timer_name="timerName"
                                ),
                                dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                                    hash_key_field="hashKeyField",
                                    hash_key_value="hashKeyValue",
                                    table_name="tableName",
        
                                    # the properties below are optional
                                    hash_key_type="hashKeyType",
                                    operation="operation",
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    payload_field="payloadField",
                                    range_key_field="rangeKeyField",
                                    range_key_type="rangeKeyType",
                                    range_key_value="rangeKeyValue"
                                ),
                                dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                                    table_name="tableName",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                                    delivery_stream_name="deliveryStreamName",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    separator="separator"
                                ),
                                iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                                    input_name="inputName",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                                    property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                        value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                            boolean_value="booleanValue",
                                            double_value="doubleValue",
                                            integer_value="integerValue",
                                            string_value="stringValue"
                                        ),
        
                                        # the properties below are optional
                                        quality="quality",
                                        timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                            time_in_seconds="timeInSeconds",
        
                                            # the properties below are optional
                                            offset_in_nanos="offsetInNanos"
                                        )
                                    ),
        
                                    # the properties below are optional
                                    asset_id="assetId",
                                    entry_id="entryId",
                                    property_alias="propertyAlias",
                                    property_id="propertyId"
                                ),
                                iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                                    mqtt_topic="mqttTopic",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                                    function_arn="functionArn",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                                    timer_name="timerName"
                                ),
                                set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                                    timer_name="timerName",
        
                                    # the properties below are optional
                                    duration_expression="durationExpression",
                                    seconds=123
                                ),
                                set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                                    value="value",
                                    variable_name="variableName"
                                ),
                                sns=iotevents.CfnDetectorModel.SnsProperty(
                                    target_arn="targetArn",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                sqs=iotevents.CfnDetectorModel.SqsProperty(
                                    queue_url="queueUrl",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    use_base64=False
                                )
                            )],
                            condition="condition"
                        )]
                    ),
                    on_exit=iotevents.CfnDetectorModel.OnExitProperty(
                        events=[iotevents.CfnDetectorModel.EventProperty(
                            event_name="eventName",
        
                            # the properties below are optional
                            actions=[iotevents.CfnDetectorModel.ActionProperty(
                                clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                                    timer_name="timerName"
                                ),
                                dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                                    hash_key_field="hashKeyField",
                                    hash_key_value="hashKeyValue",
                                    table_name="tableName",
        
                                    # the properties below are optional
                                    hash_key_type="hashKeyType",
                                    operation="operation",
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    payload_field="payloadField",
                                    range_key_field="rangeKeyField",
                                    range_key_type="rangeKeyType",
                                    range_key_value="rangeKeyValue"
                                ),
                                dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                                    table_name="tableName",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                                    delivery_stream_name="deliveryStreamName",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    separator="separator"
                                ),
                                iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                                    input_name="inputName",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                                    property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                        value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                            boolean_value="booleanValue",
                                            double_value="doubleValue",
                                            integer_value="integerValue",
                                            string_value="stringValue"
                                        ),
        
                                        # the properties below are optional
                                        quality="quality",
                                        timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                            time_in_seconds="timeInSeconds",
        
                                            # the properties below are optional
                                            offset_in_nanos="offsetInNanos"
                                        )
                                    ),
        
                                    # the properties below are optional
                                    asset_id="assetId",
                                    entry_id="entryId",
                                    property_alias="propertyAlias",
                                    property_id="propertyId"
                                ),
                                iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                                    mqtt_topic="mqttTopic",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                                    function_arn="functionArn",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                                    timer_name="timerName"
                                ),
                                set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                                    timer_name="timerName",
        
                                    # the properties below are optional
                                    duration_expression="durationExpression",
                                    seconds=123
                                ),
                                set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                                    value="value",
                                    variable_name="variableName"
                                ),
                                sns=iotevents.CfnDetectorModel.SnsProperty(
                                    target_arn="targetArn",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                sqs=iotevents.CfnDetectorModel.SqsProperty(
                                    queue_url="queueUrl",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    use_base64=False
                                )
                            )],
                            condition="condition"
                        )]
                    ),
                    on_input=iotevents.CfnDetectorModel.OnInputProperty(
                        events=[iotevents.CfnDetectorModel.EventProperty(
                            event_name="eventName",
        
                            # the properties below are optional
                            actions=[iotevents.CfnDetectorModel.ActionProperty(
                                clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                                    timer_name="timerName"
                                ),
                                dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                                    hash_key_field="hashKeyField",
                                    hash_key_value="hashKeyValue",
                                    table_name="tableName",
        
                                    # the properties below are optional
                                    hash_key_type="hashKeyType",
                                    operation="operation",
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    payload_field="payloadField",
                                    range_key_field="rangeKeyField",
                                    range_key_type="rangeKeyType",
                                    range_key_value="rangeKeyValue"
                                ),
                                dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                                    table_name="tableName",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                                    delivery_stream_name="deliveryStreamName",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    separator="separator"
                                ),
                                iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                                    input_name="inputName",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                                    property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                        value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                            boolean_value="booleanValue",
                                            double_value="doubleValue",
                                            integer_value="integerValue",
                                            string_value="stringValue"
                                        ),
        
                                        # the properties below are optional
                                        quality="quality",
                                        timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                            time_in_seconds="timeInSeconds",
        
                                            # the properties below are optional
                                            offset_in_nanos="offsetInNanos"
                                        )
                                    ),
        
                                    # the properties below are optional
                                    asset_id="assetId",
                                    entry_id="entryId",
                                    property_alias="propertyAlias",
                                    property_id="propertyId"
                                ),
                                iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                                    mqtt_topic="mqttTopic",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                                    function_arn="functionArn",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                                    timer_name="timerName"
                                ),
                                set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                                    timer_name="timerName",
        
                                    # the properties below are optional
                                    duration_expression="durationExpression",
                                    seconds=123
                                ),
                                set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                                    value="value",
                                    variable_name="variableName"
                                ),
                                sns=iotevents.CfnDetectorModel.SnsProperty(
                                    target_arn="targetArn",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                sqs=iotevents.CfnDetectorModel.SqsProperty(
                                    queue_url="queueUrl",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    use_base64=False
                                )
                            )],
                            condition="condition"
                        )],
                        transition_events=[iotevents.CfnDetectorModel.TransitionEventProperty(
                            condition="condition",
                            event_name="eventName",
                            next_state="nextState",
        
                            # the properties below are optional
                            actions=[iotevents.CfnDetectorModel.ActionProperty(
                                clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                                    timer_name="timerName"
                                ),
                                dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                                    hash_key_field="hashKeyField",
                                    hash_key_value="hashKeyValue",
                                    table_name="tableName",
        
                                    # the properties below are optional
                                    hash_key_type="hashKeyType",
                                    operation="operation",
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    payload_field="payloadField",
                                    range_key_field="rangeKeyField",
                                    range_key_type="rangeKeyType",
                                    range_key_value="rangeKeyValue"
                                ),
                                dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                                    table_name="tableName",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                                    delivery_stream_name="deliveryStreamName",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    separator="separator"
                                ),
                                iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                                    input_name="inputName",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                                    property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                        value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                            boolean_value="booleanValue",
                                            double_value="doubleValue",
                                            integer_value="integerValue",
                                            string_value="stringValue"
                                        ),
        
                                        # the properties below are optional
                                        quality="quality",
                                        timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                            time_in_seconds="timeInSeconds",
        
                                            # the properties below are optional
                                            offset_in_nanos="offsetInNanos"
                                        )
                                    ),
        
                                    # the properties below are optional
                                    asset_id="assetId",
                                    entry_id="entryId",
                                    property_alias="propertyAlias",
                                    property_id="propertyId"
                                ),
                                iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                                    mqtt_topic="mqttTopic",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                                    function_arn="functionArn",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                                    timer_name="timerName"
                                ),
                                set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                                    timer_name="timerName",
        
                                    # the properties below are optional
                                    duration_expression="durationExpression",
                                    seconds=123
                                ),
                                set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                                    value="value",
                                    variable_name="variableName"
                                ),
                                sns=iotevents.CfnDetectorModel.SnsProperty(
                                    target_arn="targetArn",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                sqs=iotevents.CfnDetectorModel.SqsProperty(
                                    queue_url="queueUrl",
        
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    use_base64=False
                                )
                            )]
                        )]
                    )
                )]
            ),
            role_arn="roleArn",
        
            # the properties below are optional
            detector_model_description="detectorModelDescription",
            detector_model_name="detectorModelName",
            evaluation_method="evaluationMethod",
            key="key",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        detector_model_definition: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.DetectorModelDefinitionProperty", typing.Dict[builtins.str, typing.Any]]],
        role_arn: builtins.str,
        detector_model_description: typing.Optional[builtins.str] = None,
        detector_model_name: typing.Optional[builtins.str] = None,
        evaluation_method: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTEvents::DetectorModel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param detector_model_definition: Information that defines how a detector operates.
        :param role_arn: The ARN of the role that grants permission to AWS IoT Events to perform its operations.
        :param detector_model_description: A brief description of the detector model.
        :param detector_model_name: The name of the detector model.
        :param evaluation_method: Information about the order in which events are evaluated and how actions are executed.
        :param key: The value used to identify a detector instance. When a device or system sends input, a new detector instance with a unique key value is created. AWS IoT Events can continue to route input to its corresponding detector instance based on this identifying information. This parameter uses a JSON-path expression to select the attribute-value pair in the message payload that is used for identification. To route the message to the correct detector instance, the device must send a message payload that contains the same attribute-value.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f2aaacccbdf39fc3ae6cb97fa81518a278625a9848665d3760abe14bf34e3af)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDetectorModelProps(
            detector_model_definition=detector_model_definition,
            role_arn=role_arn,
            detector_model_description=detector_model_description,
            detector_model_name=detector_model_name,
            evaluation_method=evaluation_method,
            key=key,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac63b00f89aa5a4bbeede8c1f17ef03e6f7d729c47716c4b0627a146856d85a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52d165955426f30a9de317a9cf94ee1324774376cc6cbe1954de34f10ffa6157)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="detectorModelDefinition")
    def detector_model_definition(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.DetectorModelDefinitionProperty"]:
        '''Information that defines how a detector operates.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-detectormodeldefinition
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.DetectorModelDefinitionProperty"], jsii.get(self, "detectorModelDefinition"))

    @detector_model_definition.setter
    def detector_model_definition(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.DetectorModelDefinitionProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d455d74c1be301e4f5070c18fd43a70a6b9868591d7d7e0d8b98dd262ed8540c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectorModelDefinition", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The ARN of the role that grants permission to AWS IoT Events to perform its operations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-rolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9bba1ba0b474c50c03e97436648c1c52de0dcea2084553e505e21e12a6c8cb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="detectorModelDescription")
    def detector_model_description(self) -> typing.Optional[builtins.str]:
        '''A brief description of the detector model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-detectormodeldescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "detectorModelDescription"))

    @detector_model_description.setter
    def detector_model_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1befb4a024f9773e0245579b01128449e3f7e867bdbebddd82c744ee5cc58fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectorModelDescription", value)

    @builtins.property
    @jsii.member(jsii_name="detectorModelName")
    def detector_model_name(self) -> typing.Optional[builtins.str]:
        '''The name of the detector model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-detectormodelname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "detectorModelName"))

    @detector_model_name.setter
    def detector_model_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__364dd7d50a8269617f57ef27267f8115ed950958b98f2d6715bef12a45652df2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectorModelName", value)

    @builtins.property
    @jsii.member(jsii_name="evaluationMethod")
    def evaluation_method(self) -> typing.Optional[builtins.str]:
        '''Information about the order in which events are evaluated and how actions are executed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-evaluationmethod
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "evaluationMethod"))

    @evaluation_method.setter
    def evaluation_method(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9caa2ed3026f19cd12ac5bb6aeabe66388ba53d49111a0f158481b5c588e861c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationMethod", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> typing.Optional[builtins.str]:
        '''The value used to identify a detector instance.

        When a device or system sends input, a new detector instance with a unique key value is created. AWS IoT Events can continue to route input to its corresponding detector instance based on this identifying information.

        This parameter uses a JSON-path expression to select the attribute-value pair in the message payload that is used for identification. To route the message to the correct detector instance, the device must send a message payload that contains the same attribute-value.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-key
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "key"))

    @key.setter
    def key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f1c312faffd330b8198e3a0e32b8a2729b80ca99188128373022dd98399e4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "clear_timer": "clearTimer",
            "dynamo_db": "dynamoDb",
            "dynamo_d_bv2": "dynamoDBv2",
            "firehose": "firehose",
            "iot_events": "iotEvents",
            "iot_site_wise": "iotSiteWise",
            "iot_topic_publish": "iotTopicPublish",
            "lambda_": "lambda",
            "reset_timer": "resetTimer",
            "set_timer": "setTimer",
            "set_variable": "setVariable",
            "sns": "sns",
            "sqs": "sqs",
        },
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            clear_timer: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.ClearTimerProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dynamo_db: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.DynamoDBProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dynamo_d_bv2: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.DynamoDBv2Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            firehose: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.FirehoseProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            iot_events: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.IotEventsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            iot_site_wise: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.IotSiteWiseProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            iot_topic_publish: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.IotTopicPublishProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            lambda_: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.LambdaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            reset_timer: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.ResetTimerProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            set_timer: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.SetTimerProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            set_variable: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.SetVariableProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sns: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.SnsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sqs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.SqsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An action to be performed when the ``condition`` is TRUE.

            :param clear_timer: Information needed to clear the timer.
            :param dynamo_db: Writes to the DynamoDB table that you created. The default action payload contains all attribute-value pairs that have the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . One column of the DynamoDB table receives all attribute-value pairs in the payload that you specify. For more information, see `Actions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-event-actions.html>`_ in *AWS IoT Events Developer Guide* .
            :param dynamo_d_bv2: Writes to the DynamoDB table that you created. The default action payload contains all attribute-value pairs that have the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . A separate column of the DynamoDB table receives one attribute-value pair in the payload that you specify. For more information, see `Actions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-event-actions.html>`_ in *AWS IoT Events Developer Guide* .
            :param firehose: Sends information about the detector model instance and the event that triggered the action to an Amazon Kinesis Data Firehose delivery stream.
            :param iot_events: Sends AWS IoT Events input, which passes information about the detector model instance and the event that triggered the action.
            :param iot_site_wise: Sends information about the detector model instance and the event that triggered the action to an asset property in AWS IoT SiteWise .
            :param iot_topic_publish: Publishes an MQTT message with the given topic to the AWS IoT message broker.
            :param lambda_: Calls a Lambda function, passing in information about the detector model instance and the event that triggered the action.
            :param reset_timer: Information needed to reset the timer.
            :param set_timer: Information needed to set the timer.
            :param set_variable: Sets a variable to a specified value.
            :param sns: Sends an Amazon SNS message.
            :param sqs: Sends an Amazon SNS message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                action_property = iotevents.CfnDetectorModel.ActionProperty(
                    clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                        timer_name="timerName"
                    ),
                    dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                        hash_key_field="hashKeyField",
                        hash_key_value="hashKeyValue",
                        table_name="tableName",
                
                        # the properties below are optional
                        hash_key_type="hashKeyType",
                        operation="operation",
                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        payload_field="payloadField",
                        range_key_field="rangeKeyField",
                        range_key_type="rangeKeyType",
                        range_key_value="rangeKeyValue"
                    ),
                    dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                        table_name="tableName",
                
                        # the properties below are optional
                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                        delivery_stream_name="deliveryStreamName",
                
                        # the properties below are optional
                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        separator="separator"
                    ),
                    iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                        input_name="inputName",
                
                        # the properties below are optional
                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                        property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                            value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                boolean_value="booleanValue",
                                double_value="doubleValue",
                                integer_value="integerValue",
                                string_value="stringValue"
                            ),
                
                            # the properties below are optional
                            quality="quality",
                            timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                time_in_seconds="timeInSeconds",
                
                                # the properties below are optional
                                offset_in_nanos="offsetInNanos"
                            )
                        ),
                
                        # the properties below are optional
                        asset_id="assetId",
                        entry_id="entryId",
                        property_alias="propertyAlias",
                        property_id="propertyId"
                    ),
                    iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                        mqtt_topic="mqttTopic",
                
                        # the properties below are optional
                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                        function_arn="functionArn",
                
                        # the properties below are optional
                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                        timer_name="timerName"
                    ),
                    set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                        timer_name="timerName",
                
                        # the properties below are optional
                        duration_expression="durationExpression",
                        seconds=123
                    ),
                    set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                        value="value",
                        variable_name="variableName"
                    ),
                    sns=iotevents.CfnDetectorModel.SnsProperty(
                        target_arn="targetArn",
                
                        # the properties below are optional
                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    sqs=iotevents.CfnDetectorModel.SqsProperty(
                        queue_url="queueUrl",
                
                        # the properties below are optional
                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        use_base64=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__941e688a554b35e3d59da041d715f16e37c14bd53b92e2ecee7cab3c8cf5b910)
                check_type(argname="argument clear_timer", value=clear_timer, expected_type=type_hints["clear_timer"])
                check_type(argname="argument dynamo_db", value=dynamo_db, expected_type=type_hints["dynamo_db"])
                check_type(argname="argument dynamo_d_bv2", value=dynamo_d_bv2, expected_type=type_hints["dynamo_d_bv2"])
                check_type(argname="argument firehose", value=firehose, expected_type=type_hints["firehose"])
                check_type(argname="argument iot_events", value=iot_events, expected_type=type_hints["iot_events"])
                check_type(argname="argument iot_site_wise", value=iot_site_wise, expected_type=type_hints["iot_site_wise"])
                check_type(argname="argument iot_topic_publish", value=iot_topic_publish, expected_type=type_hints["iot_topic_publish"])
                check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
                check_type(argname="argument reset_timer", value=reset_timer, expected_type=type_hints["reset_timer"])
                check_type(argname="argument set_timer", value=set_timer, expected_type=type_hints["set_timer"])
                check_type(argname="argument set_variable", value=set_variable, expected_type=type_hints["set_variable"])
                check_type(argname="argument sns", value=sns, expected_type=type_hints["sns"])
                check_type(argname="argument sqs", value=sqs, expected_type=type_hints["sqs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if clear_timer is not None:
                self._values["clear_timer"] = clear_timer
            if dynamo_db is not None:
                self._values["dynamo_db"] = dynamo_db
            if dynamo_d_bv2 is not None:
                self._values["dynamo_d_bv2"] = dynamo_d_bv2
            if firehose is not None:
                self._values["firehose"] = firehose
            if iot_events is not None:
                self._values["iot_events"] = iot_events
            if iot_site_wise is not None:
                self._values["iot_site_wise"] = iot_site_wise
            if iot_topic_publish is not None:
                self._values["iot_topic_publish"] = iot_topic_publish
            if lambda_ is not None:
                self._values["lambda_"] = lambda_
            if reset_timer is not None:
                self._values["reset_timer"] = reset_timer
            if set_timer is not None:
                self._values["set_timer"] = set_timer
            if set_variable is not None:
                self._values["set_variable"] = set_variable
            if sns is not None:
                self._values["sns"] = sns
            if sqs is not None:
                self._values["sqs"] = sqs

        @builtins.property
        def clear_timer(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.ClearTimerProperty"]]:
            '''Information needed to clear the timer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-cleartimer
            '''
            result = self._values.get("clear_timer")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.ClearTimerProperty"]], result)

        @builtins.property
        def dynamo_db(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.DynamoDBProperty"]]:
            '''Writes to the DynamoDB table that you created.

            The default action payload contains all attribute-value pairs that have the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . One column of the DynamoDB table receives all attribute-value pairs in the payload that you specify. For more information, see `Actions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-event-actions.html>`_ in *AWS IoT Events Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-dynamodb
            '''
            result = self._values.get("dynamo_db")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.DynamoDBProperty"]], result)

        @builtins.property
        def dynamo_d_bv2(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.DynamoDBv2Property"]]:
            '''Writes to the DynamoDB table that you created.

            The default action payload contains all attribute-value pairs that have the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . A separate column of the DynamoDB table receives one attribute-value pair in the payload that you specify. For more information, see `Actions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-event-actions.html>`_ in *AWS IoT Events Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-dynamodbv2
            '''
            result = self._values.get("dynamo_d_bv2")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.DynamoDBv2Property"]], result)

        @builtins.property
        def firehose(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.FirehoseProperty"]]:
            '''Sends information about the detector model instance and the event that triggered the action to an Amazon Kinesis Data Firehose delivery stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-firehose
            '''
            result = self._values.get("firehose")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.FirehoseProperty"]], result)

        @builtins.property
        def iot_events(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.IotEventsProperty"]]:
            '''Sends AWS IoT Events input, which passes information about the detector model instance and the event that triggered the action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-iotevents
            '''
            result = self._values.get("iot_events")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.IotEventsProperty"]], result)

        @builtins.property
        def iot_site_wise(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.IotSiteWiseProperty"]]:
            '''Sends information about the detector model instance and the event that triggered the action to an asset property in AWS IoT SiteWise .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-iotsitewise
            '''
            result = self._values.get("iot_site_wise")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.IotSiteWiseProperty"]], result)

        @builtins.property
        def iot_topic_publish(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.IotTopicPublishProperty"]]:
            '''Publishes an MQTT message with the given topic to the AWS IoT message broker.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-iottopicpublish
            '''
            result = self._values.get("iot_topic_publish")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.IotTopicPublishProperty"]], result)

        @builtins.property
        def lambda_(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.LambdaProperty"]]:
            '''Calls a Lambda function, passing in information about the detector model instance and the event that triggered the action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-lambda
            '''
            result = self._values.get("lambda_")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.LambdaProperty"]], result)

        @builtins.property
        def reset_timer(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.ResetTimerProperty"]]:
            '''Information needed to reset the timer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-resettimer
            '''
            result = self._values.get("reset_timer")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.ResetTimerProperty"]], result)

        @builtins.property
        def set_timer(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.SetTimerProperty"]]:
            '''Information needed to set the timer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-settimer
            '''
            result = self._values.get("set_timer")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.SetTimerProperty"]], result)

        @builtins.property
        def set_variable(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.SetVariableProperty"]]:
            '''Sets a variable to a specified value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-setvariable
            '''
            result = self._values.get("set_variable")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.SetVariableProperty"]], result)

        @builtins.property
        def sns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.SnsProperty"]]:
            '''Sends an Amazon SNS message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-sns
            '''
            result = self._values.get("sns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.SnsProperty"]], result)

        @builtins.property
        def sqs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.SqsProperty"]]:
            '''Sends an Amazon SNS message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-sqs
            '''
            result = self._values.get("sqs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.SqsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.AssetPropertyTimestampProperty",
        jsii_struct_bases=[],
        name_mapping={
            "time_in_seconds": "timeInSeconds",
            "offset_in_nanos": "offsetInNanos",
        },
    )
    class AssetPropertyTimestampProperty:
        def __init__(
            self,
            *,
            time_in_seconds: builtins.str,
            offset_in_nanos: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that contains timestamp information. For more information, see `TimeInNanos <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_TimeInNanos.html>`_ in the *AWS IoT SiteWise API Reference* .

            You must use expressions for all parameters in ``AssetPropertyTimestamp`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``timeInSeconds`` parameter can be ``'1586400675'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``offsetInNanos`` parameter can be ``$variable.time`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``timeInSeconds`` parameter uses a substitution template.

            ``'${$input.TemperatureInput.sensorData.timestamp / 1000}'``

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            :param time_in_seconds: The timestamp, in seconds, in the Unix epoch format. The valid range is between 1-31556889864403199.
            :param offset_in_nanos: The nanosecond offset converted from ``timeInSeconds`` . The valid range is between 0-999999999.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertytimestamp.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                asset_property_timestamp_property = iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                    time_in_seconds="timeInSeconds",
                
                    # the properties below are optional
                    offset_in_nanos="offsetInNanos"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0dd4ed56d59949f5787f4680c51797508688338e21a8271708094f1ab9b7a74f)
                check_type(argname="argument time_in_seconds", value=time_in_seconds, expected_type=type_hints["time_in_seconds"])
                check_type(argname="argument offset_in_nanos", value=offset_in_nanos, expected_type=type_hints["offset_in_nanos"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "time_in_seconds": time_in_seconds,
            }
            if offset_in_nanos is not None:
                self._values["offset_in_nanos"] = offset_in_nanos

        @builtins.property
        def time_in_seconds(self) -> builtins.str:
            '''The timestamp, in seconds, in the Unix epoch format.

            The valid range is between 1-31556889864403199.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertytimestamp.html#cfn-iotevents-detectormodel-assetpropertytimestamp-timeinseconds
            '''
            result = self._values.get("time_in_seconds")
            assert result is not None, "Required property 'time_in_seconds' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def offset_in_nanos(self) -> typing.Optional[builtins.str]:
            '''The nanosecond offset converted from ``timeInSeconds`` .

            The valid range is between 0-999999999.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertytimestamp.html#cfn-iotevents-detectormodel-assetpropertytimestamp-offsetinnanos
            '''
            result = self._values.get("offset_in_nanos")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetPropertyTimestampProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.AssetPropertyValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "value": "value",
            "quality": "quality",
            "timestamp": "timestamp",
        },
    )
    class AssetPropertyValueProperty:
        def __init__(
            self,
            *,
            value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.AssetPropertyVariantProperty", typing.Dict[builtins.str, typing.Any]]],
            quality: typing.Optional[builtins.str] = None,
            timestamp: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.AssetPropertyTimestampProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A structure that contains value information. For more information, see `AssetPropertyValue <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_AssetPropertyValue.html>`_ in the *AWS IoT SiteWise API Reference* .

            You must use expressions for all parameters in ``AssetPropertyValue`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``quality`` parameter can be ``'GOOD'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``quality`` parameter can be ``$input.TemperatureInput.sensorData.quality`` .

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            :param value: The value to send to an asset property.
            :param quality: The quality of the asset property value. The value must be ``'GOOD'`` , ``'BAD'`` , or ``'UNCERTAIN'`` .
            :param timestamp: The timestamp associated with the asset property value. The default is the current event time.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                asset_property_value_property = iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                    value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                        boolean_value="booleanValue",
                        double_value="doubleValue",
                        integer_value="integerValue",
                        string_value="stringValue"
                    ),
                
                    # the properties below are optional
                    quality="quality",
                    timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                        time_in_seconds="timeInSeconds",
                
                        # the properties below are optional
                        offset_in_nanos="offsetInNanos"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__14f43e0e57626c7d6b69a42bb377d37552b8ccef973a097c6a4e0d39810862e5)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                check_type(argname="argument quality", value=quality, expected_type=type_hints["quality"])
                check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "value": value,
            }
            if quality is not None:
                self._values["quality"] = quality
            if timestamp is not None:
                self._values["timestamp"] = timestamp

        @builtins.property
        def value(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.AssetPropertyVariantProperty"]:
            '''The value to send to an asset property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvalue.html#cfn-iotevents-detectormodel-assetpropertyvalue-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.AssetPropertyVariantProperty"], result)

        @builtins.property
        def quality(self) -> typing.Optional[builtins.str]:
            '''The quality of the asset property value.

            The value must be ``'GOOD'`` , ``'BAD'`` , or ``'UNCERTAIN'`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvalue.html#cfn-iotevents-detectormodel-assetpropertyvalue-quality
            '''
            result = self._values.get("quality")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timestamp(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.AssetPropertyTimestampProperty"]]:
            '''The timestamp associated with the asset property value.

            The default is the current event time.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvalue.html#cfn-iotevents-detectormodel-assetpropertyvalue-timestamp
            '''
            result = self._values.get("timestamp")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.AssetPropertyTimestampProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetPropertyValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.AssetPropertyVariantProperty",
        jsii_struct_bases=[],
        name_mapping={
            "boolean_value": "booleanValue",
            "double_value": "doubleValue",
            "integer_value": "integerValue",
            "string_value": "stringValue",
        },
    )
    class AssetPropertyVariantProperty:
        def __init__(
            self,
            *,
            boolean_value: typing.Optional[builtins.str] = None,
            double_value: typing.Optional[builtins.str] = None,
            integer_value: typing.Optional[builtins.str] = None,
            string_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that contains an asset property value.

            For more information, see `Variant <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_Variant.html>`_ in the *AWS IoT SiteWise API Reference* .

            You must use expressions for all parameters in ``AssetPropertyVariant`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``integerValue`` parameter can be ``'100'`` .

            - For references, you must specify either variables or parameters. For example, the value for the ``booleanValue`` parameter can be ``$variable.offline`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``doubleValue`` parameter uses a substitution template.

            ``'${$input.TemperatureInput.sensorData.temperature * 6 / 5 + 32}'``

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            You must specify one of the following value types, depending on the ``dataType`` of the specified asset property. For more information, see `AssetProperty <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_AssetProperty.html>`_ in the *AWS IoT SiteWise API Reference* .

            :param boolean_value: The asset property value is a Boolean value that must be ``'TRUE'`` or ``'FALSE'`` . You must use an expression, and the evaluated result should be a Boolean value.
            :param double_value: The asset property value is a double. You must use an expression, and the evaluated result should be a double.
            :param integer_value: The asset property value is an integer. You must use an expression, and the evaluated result should be an integer.
            :param string_value: The asset property value is a string. You must use an expression, and the evaluated result should be a string.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvariant.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                asset_property_variant_property = iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                    boolean_value="booleanValue",
                    double_value="doubleValue",
                    integer_value="integerValue",
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5a99f6659005b765e75663adbdb672e127e821885f889825750025173b5f4a99)
                check_type(argname="argument boolean_value", value=boolean_value, expected_type=type_hints["boolean_value"])
                check_type(argname="argument double_value", value=double_value, expected_type=type_hints["double_value"])
                check_type(argname="argument integer_value", value=integer_value, expected_type=type_hints["integer_value"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if boolean_value is not None:
                self._values["boolean_value"] = boolean_value
            if double_value is not None:
                self._values["double_value"] = double_value
            if integer_value is not None:
                self._values["integer_value"] = integer_value
            if string_value is not None:
                self._values["string_value"] = string_value

        @builtins.property
        def boolean_value(self) -> typing.Optional[builtins.str]:
            '''The asset property value is a Boolean value that must be ``'TRUE'`` or ``'FALSE'`` .

            You must use an expression, and the evaluated result should be a Boolean value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvariant.html#cfn-iotevents-detectormodel-assetpropertyvariant-booleanvalue
            '''
            result = self._values.get("boolean_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def double_value(self) -> typing.Optional[builtins.str]:
            '''The asset property value is a double.

            You must use an expression, and the evaluated result should be a double.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvariant.html#cfn-iotevents-detectormodel-assetpropertyvariant-doublevalue
            '''
            result = self._values.get("double_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def integer_value(self) -> typing.Optional[builtins.str]:
            '''The asset property value is an integer.

            You must use an expression, and the evaluated result should be an integer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvariant.html#cfn-iotevents-detectormodel-assetpropertyvariant-integervalue
            '''
            result = self._values.get("integer_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''The asset property value is a string.

            You must use an expression, and the evaluated result should be a string.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvariant.html#cfn-iotevents-detectormodel-assetpropertyvariant-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetPropertyVariantProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.ClearTimerProperty",
        jsii_struct_bases=[],
        name_mapping={"timer_name": "timerName"},
    )
    class ClearTimerProperty:
        def __init__(self, *, timer_name: builtins.str) -> None:
            '''Information needed to clear the timer.

            :param timer_name: The name of the timer to clear.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-cleartimer.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                clear_timer_property = iotevents.CfnDetectorModel.ClearTimerProperty(
                    timer_name="timerName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4416a7142280a8194936287914e2d3f4e3e95032a15849dca1b6dcc3a9581178)
                check_type(argname="argument timer_name", value=timer_name, expected_type=type_hints["timer_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "timer_name": timer_name,
            }

        @builtins.property
        def timer_name(self) -> builtins.str:
            '''The name of the timer to clear.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-cleartimer.html#cfn-iotevents-detectormodel-cleartimer-timername
            '''
            result = self._values.get("timer_name")
            assert result is not None, "Required property 'timer_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ClearTimerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.DetectorModelDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"initial_state_name": "initialStateName", "states": "states"},
    )
    class DetectorModelDefinitionProperty:
        def __init__(
            self,
            *,
            initial_state_name: builtins.str,
            states: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.StateProperty", typing.Dict[builtins.str, typing.Any]]]]],
        ) -> None:
            '''Information that defines how a detector operates.

            :param initial_state_name: The state that is entered at the creation of each detector (instance).
            :param states: Information about the states of the detector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-detectormodeldefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                detector_model_definition_property = iotevents.CfnDetectorModel.DetectorModelDefinitionProperty(
                    initial_state_name="initialStateName",
                    states=[iotevents.CfnDetectorModel.StateProperty(
                        state_name="stateName",
                
                        # the properties below are optional
                        on_enter=iotevents.CfnDetectorModel.OnEnterProperty(
                            events=[iotevents.CfnDetectorModel.EventProperty(
                                event_name="eventName",
                
                                # the properties below are optional
                                actions=[iotevents.CfnDetectorModel.ActionProperty(
                                    clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                                        hash_key_field="hashKeyField",
                                        hash_key_value="hashKeyValue",
                                        table_name="tableName",
                
                                        # the properties below are optional
                                        hash_key_type="hashKeyType",
                                        operation="operation",
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        payload_field="payloadField",
                                        range_key_field="rangeKeyField",
                                        range_key_type="rangeKeyType",
                                        range_key_value="rangeKeyValue"
                                    ),
                                    dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                                        table_name="tableName",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                                        delivery_stream_name="deliveryStreamName",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        separator="separator"
                                    ),
                                    iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                                        input_name="inputName",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                                        property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                            value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                                boolean_value="booleanValue",
                                                double_value="doubleValue",
                                                integer_value="integerValue",
                                                string_value="stringValue"
                                            ),
                
                                            # the properties below are optional
                                            quality="quality",
                                            timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                                time_in_seconds="timeInSeconds",
                
                                                # the properties below are optional
                                                offset_in_nanos="offsetInNanos"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        asset_id="assetId",
                                        entry_id="entryId",
                                        property_alias="propertyAlias",
                                        property_id="propertyId"
                                    ),
                                    iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                                        mqtt_topic="mqttTopic",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                                        function_arn="functionArn",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                                        timer_name="timerName",
                
                                        # the properties below are optional
                                        duration_expression="durationExpression",
                                        seconds=123
                                    ),
                                    set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                                        value="value",
                                        variable_name="variableName"
                                    ),
                                    sns=iotevents.CfnDetectorModel.SnsProperty(
                                        target_arn="targetArn",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    sqs=iotevents.CfnDetectorModel.SqsProperty(
                                        queue_url="queueUrl",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        use_base64=False
                                    )
                                )],
                                condition="condition"
                            )]
                        ),
                        on_exit=iotevents.CfnDetectorModel.OnExitProperty(
                            events=[iotevents.CfnDetectorModel.EventProperty(
                                event_name="eventName",
                
                                # the properties below are optional
                                actions=[iotevents.CfnDetectorModel.ActionProperty(
                                    clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                                        hash_key_field="hashKeyField",
                                        hash_key_value="hashKeyValue",
                                        table_name="tableName",
                
                                        # the properties below are optional
                                        hash_key_type="hashKeyType",
                                        operation="operation",
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        payload_field="payloadField",
                                        range_key_field="rangeKeyField",
                                        range_key_type="rangeKeyType",
                                        range_key_value="rangeKeyValue"
                                    ),
                                    dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                                        table_name="tableName",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                                        delivery_stream_name="deliveryStreamName",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        separator="separator"
                                    ),
                                    iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                                        input_name="inputName",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                                        property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                            value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                                boolean_value="booleanValue",
                                                double_value="doubleValue",
                                                integer_value="integerValue",
                                                string_value="stringValue"
                                            ),
                
                                            # the properties below are optional
                                            quality="quality",
                                            timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                                time_in_seconds="timeInSeconds",
                
                                                # the properties below are optional
                                                offset_in_nanos="offsetInNanos"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        asset_id="assetId",
                                        entry_id="entryId",
                                        property_alias="propertyAlias",
                                        property_id="propertyId"
                                    ),
                                    iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                                        mqtt_topic="mqttTopic",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                                        function_arn="functionArn",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                                        timer_name="timerName",
                
                                        # the properties below are optional
                                        duration_expression="durationExpression",
                                        seconds=123
                                    ),
                                    set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                                        value="value",
                                        variable_name="variableName"
                                    ),
                                    sns=iotevents.CfnDetectorModel.SnsProperty(
                                        target_arn="targetArn",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    sqs=iotevents.CfnDetectorModel.SqsProperty(
                                        queue_url="queueUrl",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        use_base64=False
                                    )
                                )],
                                condition="condition"
                            )]
                        ),
                        on_input=iotevents.CfnDetectorModel.OnInputProperty(
                            events=[iotevents.CfnDetectorModel.EventProperty(
                                event_name="eventName",
                
                                # the properties below are optional
                                actions=[iotevents.CfnDetectorModel.ActionProperty(
                                    clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                                        hash_key_field="hashKeyField",
                                        hash_key_value="hashKeyValue",
                                        table_name="tableName",
                
                                        # the properties below are optional
                                        hash_key_type="hashKeyType",
                                        operation="operation",
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        payload_field="payloadField",
                                        range_key_field="rangeKeyField",
                                        range_key_type="rangeKeyType",
                                        range_key_value="rangeKeyValue"
                                    ),
                                    dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                                        table_name="tableName",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                                        delivery_stream_name="deliveryStreamName",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        separator="separator"
                                    ),
                                    iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                                        input_name="inputName",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                                        property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                            value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                                boolean_value="booleanValue",
                                                double_value="doubleValue",
                                                integer_value="integerValue",
                                                string_value="stringValue"
                                            ),
                
                                            # the properties below are optional
                                            quality="quality",
                                            timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                                time_in_seconds="timeInSeconds",
                
                                                # the properties below are optional
                                                offset_in_nanos="offsetInNanos"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        asset_id="assetId",
                                        entry_id="entryId",
                                        property_alias="propertyAlias",
                                        property_id="propertyId"
                                    ),
                                    iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                                        mqtt_topic="mqttTopic",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                                        function_arn="functionArn",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                                        timer_name="timerName",
                
                                        # the properties below are optional
                                        duration_expression="durationExpression",
                                        seconds=123
                                    ),
                                    set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                                        value="value",
                                        variable_name="variableName"
                                    ),
                                    sns=iotevents.CfnDetectorModel.SnsProperty(
                                        target_arn="targetArn",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    sqs=iotevents.CfnDetectorModel.SqsProperty(
                                        queue_url="queueUrl",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        use_base64=False
                                    )
                                )],
                                condition="condition"
                            )],
                            transition_events=[iotevents.CfnDetectorModel.TransitionEventProperty(
                                condition="condition",
                                event_name="eventName",
                                next_state="nextState",
                
                                # the properties below are optional
                                actions=[iotevents.CfnDetectorModel.ActionProperty(
                                    clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                                        hash_key_field="hashKeyField",
                                        hash_key_value="hashKeyValue",
                                        table_name="tableName",
                
                                        # the properties below are optional
                                        hash_key_type="hashKeyType",
                                        operation="operation",
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        payload_field="payloadField",
                                        range_key_field="rangeKeyField",
                                        range_key_type="rangeKeyType",
                                        range_key_value="rangeKeyValue"
                                    ),
                                    dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                                        table_name="tableName",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                                        delivery_stream_name="deliveryStreamName",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        separator="separator"
                                    ),
                                    iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                                        input_name="inputName",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                                        property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                            value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                                boolean_value="booleanValue",
                                                double_value="doubleValue",
                                                integer_value="integerValue",
                                                string_value="stringValue"
                                            ),
                
                                            # the properties below are optional
                                            quality="quality",
                                            timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                                time_in_seconds="timeInSeconds",
                
                                                # the properties below are optional
                                                offset_in_nanos="offsetInNanos"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        asset_id="assetId",
                                        entry_id="entryId",
                                        property_alias="propertyAlias",
                                        property_id="propertyId"
                                    ),
                                    iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                                        mqtt_topic="mqttTopic",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                                        function_arn="functionArn",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                                        timer_name="timerName",
                
                                        # the properties below are optional
                                        duration_expression="durationExpression",
                                        seconds=123
                                    ),
                                    set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                                        value="value",
                                        variable_name="variableName"
                                    ),
                                    sns=iotevents.CfnDetectorModel.SnsProperty(
                                        target_arn="targetArn",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    sqs=iotevents.CfnDetectorModel.SqsProperty(
                                        queue_url="queueUrl",
                
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        use_base64=False
                                    )
                                )]
                            )]
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a25afe04c9b8dd7d53a71a1d933ad80cc386085ea5f9fe135c68adee6f6ea4ae)
                check_type(argname="argument initial_state_name", value=initial_state_name, expected_type=type_hints["initial_state_name"])
                check_type(argname="argument states", value=states, expected_type=type_hints["states"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "initial_state_name": initial_state_name,
                "states": states,
            }

        @builtins.property
        def initial_state_name(self) -> builtins.str:
            '''The state that is entered at the creation of each detector (instance).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-detectormodeldefinition.html#cfn-iotevents-detectormodel-detectormodeldefinition-initialstatename
            '''
            result = self._values.get("initial_state_name")
            assert result is not None, "Required property 'initial_state_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def states(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.StateProperty"]]]:
            '''Information about the states of the detector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-detectormodeldefinition.html#cfn-iotevents-detectormodel-detectormodeldefinition-states
            '''
            result = self._values.get("states")
            assert result is not None, "Required property 'states' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.StateProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DetectorModelDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.DynamoDBProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hash_key_field": "hashKeyField",
            "hash_key_value": "hashKeyValue",
            "table_name": "tableName",
            "hash_key_type": "hashKeyType",
            "operation": "operation",
            "payload": "payload",
            "payload_field": "payloadField",
            "range_key_field": "rangeKeyField",
            "range_key_type": "rangeKeyType",
            "range_key_value": "rangeKeyValue",
        },
    )
    class DynamoDBProperty:
        def __init__(
            self,
            *,
            hash_key_field: builtins.str,
            hash_key_value: builtins.str,
            table_name: builtins.str,
            hash_key_type: typing.Optional[builtins.str] = None,
            operation: typing.Optional[builtins.str] = None,
            payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            payload_field: typing.Optional[builtins.str] = None,
            range_key_field: typing.Optional[builtins.str] = None,
            range_key_type: typing.Optional[builtins.str] = None,
            range_key_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines an action to write to the Amazon DynamoDB table that you created.

            The standard action payload contains all the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . One column of the DynamoDB table receives all attribute-value pairs in the payload that you specify.

            You must use expressions for all parameters in ``DynamoDBAction`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``hashKeyType`` parameter can be ``'STRING'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``hashKeyField`` parameter can be ``$input.GreenhouseInput.name`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``hashKeyValue`` parameter uses a substitution template.

            ``'${$input.GreenhouseInput.temperature * 6 / 5 + 32} in Fahrenheit'``

            - For a string concatenation, you must use ``+`` . A string concatenation can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``tableName`` parameter uses a string concatenation.

            ``'GreenhouseTemperatureTable ' + $input.GreenhouseInput.date``

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            If the defined payload type is a string, ``DynamoDBAction`` writes non-JSON data to the DynamoDB table as binary data. The DynamoDB console displays the data as Base64-encoded text. The value for the ``payloadField`` parameter is ``<payload-field>_raw`` .

            :param hash_key_field: The name of the hash key (also called the partition key). The ``hashKeyField`` value must match the partition key of the target DynamoDB table.
            :param hash_key_value: The value of the hash key (also called the partition key).
            :param table_name: The name of the DynamoDB table. The ``tableName`` value must match the table name of the target DynamoDB table.
            :param hash_key_type: The data type for the hash key (also called the partition key). You can specify the following values:. - ``'STRING'`` - The hash key is a string. - ``'NUMBER'`` - The hash key is a number. If you don't specify ``hashKeyType`` , the default value is ``'STRING'`` .
            :param operation: The type of operation to perform. You can specify the following values:. - ``'INSERT'`` - Insert data as a new item into the DynamoDB table. This item uses the specified hash key as a partition key. If you specified a range key, the item uses the range key as a sort key. - ``'UPDATE'`` - Update an existing item of the DynamoDB table with new data. This item's partition key must match the specified hash key. If you specified a range key, the range key must match the item's sort key. - ``'DELETE'`` - Delete an existing item of the DynamoDB table. This item's partition key must match the specified hash key. If you specified a range key, the range key must match the item's sort key. If you don't specify this parameter, AWS IoT Events triggers the ``'INSERT'`` operation.
            :param payload: Information needed to configure the payload. By default, AWS IoT Events generates a standard payload in JSON for any action. This action payload contains all attribute-value pairs that have the information about the detector model instance and the event triggered the action. To configure the action payload, you can use ``contentExpression`` .
            :param payload_field: The name of the DynamoDB column that receives the action payload. If you don't specify this parameter, the name of the DynamoDB column is ``payload`` .
            :param range_key_field: The name of the range key (also called the sort key). The ``rangeKeyField`` value must match the sort key of the target DynamoDB table.
            :param range_key_type: The data type for the range key (also called the sort key), You can specify the following values:. - ``'STRING'`` - The range key is a string. - ``'NUMBER'`` - The range key is number. If you don't specify ``rangeKeyField`` , the default value is ``'STRING'`` .
            :param range_key_value: The value of the range key (also called the sort key).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                dynamo_dBProperty = iotevents.CfnDetectorModel.DynamoDBProperty(
                    hash_key_field="hashKeyField",
                    hash_key_value="hashKeyValue",
                    table_name="tableName",
                
                    # the properties below are optional
                    hash_key_type="hashKeyType",
                    operation="operation",
                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    ),
                    payload_field="payloadField",
                    range_key_field="rangeKeyField",
                    range_key_type="rangeKeyType",
                    range_key_value="rangeKeyValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f31d1c7d374d5e831a3813fd7c0cfdf95eb7ddfdb3c86f207b90cfc7207002e9)
                check_type(argname="argument hash_key_field", value=hash_key_field, expected_type=type_hints["hash_key_field"])
                check_type(argname="argument hash_key_value", value=hash_key_value, expected_type=type_hints["hash_key_value"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
                check_type(argname="argument hash_key_type", value=hash_key_type, expected_type=type_hints["hash_key_type"])
                check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
                check_type(argname="argument payload_field", value=payload_field, expected_type=type_hints["payload_field"])
                check_type(argname="argument range_key_field", value=range_key_field, expected_type=type_hints["range_key_field"])
                check_type(argname="argument range_key_type", value=range_key_type, expected_type=type_hints["range_key_type"])
                check_type(argname="argument range_key_value", value=range_key_value, expected_type=type_hints["range_key_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "hash_key_field": hash_key_field,
                "hash_key_value": hash_key_value,
                "table_name": table_name,
            }
            if hash_key_type is not None:
                self._values["hash_key_type"] = hash_key_type
            if operation is not None:
                self._values["operation"] = operation
            if payload is not None:
                self._values["payload"] = payload
            if payload_field is not None:
                self._values["payload_field"] = payload_field
            if range_key_field is not None:
                self._values["range_key_field"] = range_key_field
            if range_key_type is not None:
                self._values["range_key_type"] = range_key_type
            if range_key_value is not None:
                self._values["range_key_value"] = range_key_value

        @builtins.property
        def hash_key_field(self) -> builtins.str:
            '''The name of the hash key (also called the partition key).

            The ``hashKeyField`` value must match the partition key of the target DynamoDB table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-hashkeyfield
            '''
            result = self._values.get("hash_key_field")
            assert result is not None, "Required property 'hash_key_field' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def hash_key_value(self) -> builtins.str:
            '''The value of the hash key (also called the partition key).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-hashkeyvalue
            '''
            result = self._values.get("hash_key_value")
            assert result is not None, "Required property 'hash_key_value' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def table_name(self) -> builtins.str:
            '''The name of the DynamoDB table.

            The ``tableName`` value must match the table name of the target DynamoDB table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-tablename
            '''
            result = self._values.get("table_name")
            assert result is not None, "Required property 'table_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def hash_key_type(self) -> typing.Optional[builtins.str]:
            '''The data type for the hash key (also called the partition key). You can specify the following values:.

            - ``'STRING'`` - The hash key is a string.
            - ``'NUMBER'`` - The hash key is a number.

            If you don't specify ``hashKeyType`` , the default value is ``'STRING'`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-hashkeytype
            '''
            result = self._values.get("hash_key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operation(self) -> typing.Optional[builtins.str]:
            '''The type of operation to perform. You can specify the following values:.

            - ``'INSERT'`` - Insert data as a new item into the DynamoDB table. This item uses the specified hash key as a partition key. If you specified a range key, the item uses the range key as a sort key.
            - ``'UPDATE'`` - Update an existing item of the DynamoDB table with new data. This item's partition key must match the specified hash key. If you specified a range key, the range key must match the item's sort key.
            - ``'DELETE'`` - Delete an existing item of the DynamoDB table. This item's partition key must match the specified hash key. If you specified a range key, the range key must match the item's sort key.

            If you don't specify this parameter, AWS IoT Events triggers the ``'INSERT'`` operation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-operation
            '''
            result = self._values.get("operation")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.PayloadProperty"]]:
            '''Information needed to configure the payload.

            By default, AWS IoT Events generates a standard payload in JSON for any action. This action payload contains all attribute-value pairs that have the information about the detector model instance and the event triggered the action. To configure the action payload, you can use ``contentExpression`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.PayloadProperty"]], result)

        @builtins.property
        def payload_field(self) -> typing.Optional[builtins.str]:
            '''The name of the DynamoDB column that receives the action payload.

            If you don't specify this parameter, the name of the DynamoDB column is ``payload`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-payloadfield
            '''
            result = self._values.get("payload_field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def range_key_field(self) -> typing.Optional[builtins.str]:
            '''The name of the range key (also called the sort key).

            The ``rangeKeyField`` value must match the sort key of the target DynamoDB table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-rangekeyfield
            '''
            result = self._values.get("range_key_field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def range_key_type(self) -> typing.Optional[builtins.str]:
            '''The data type for the range key (also called the sort key), You can specify the following values:.

            - ``'STRING'`` - The range key is a string.
            - ``'NUMBER'`` - The range key is number.

            If you don't specify ``rangeKeyField`` , the default value is ``'STRING'`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-rangekeytype
            '''
            result = self._values.get("range_key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def range_key_value(self) -> typing.Optional[builtins.str]:
            '''The value of the range key (also called the sort key).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-rangekeyvalue
            '''
            result = self._values.get("range_key_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamoDBProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.DynamoDBv2Property",
        jsii_struct_bases=[],
        name_mapping={"table_name": "tableName", "payload": "payload"},
    )
    class DynamoDBv2Property:
        def __init__(
            self,
            *,
            table_name: builtins.str,
            payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Defines an action to write to the Amazon DynamoDB table that you created.

            The default action payload contains all the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . A separate column of the DynamoDB table receives one attribute-value pair in the payload that you specify.

            You must use expressions for all parameters in ``DynamoDBv2Action`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``tableName`` parameter can be ``'GreenhouseTemperatureTable'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``tableName`` parameter can be ``$variable.ddbtableName`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``contentExpression`` parameter in ``Payload`` uses a substitution template.

            ``'{\\"sensorID\\": \\"${$input.GreenhouseInput.sensor_id}\\", \\"temperature\\": \\"${$input.GreenhouseInput.temperature * 9 / 5 + 32}\\"}'``

            - For a string concatenation, you must use ``+`` . A string concatenation can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``tableName`` parameter uses a string concatenation.

            ``'GreenhouseTemperatureTable ' + $input.GreenhouseInput.date``

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            The value for the ``type`` parameter in ``Payload`` must be ``JSON`` .

            :param table_name: The name of the DynamoDB table.
            :param payload: Information needed to configure the payload. By default, AWS IoT Events generates a standard payload in JSON for any action. This action payload contains all attribute-value pairs that have the information about the detector model instance and the event triggered the action. To configure the action payload, you can use ``contentExpression`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodbv2.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                dynamo_dBv2_property = iotevents.CfnDetectorModel.DynamoDBv2Property(
                    table_name="tableName",
                
                    # the properties below are optional
                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9a888ed429a92d938952ca9d54c1845e5339696b77a967c76e5169847f0d8a1e)
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "table_name": table_name,
            }
            if payload is not None:
                self._values["payload"] = payload

        @builtins.property
        def table_name(self) -> builtins.str:
            '''The name of the DynamoDB table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodbv2.html#cfn-iotevents-detectormodel-dynamodbv2-tablename
            '''
            result = self._values.get("table_name")
            assert result is not None, "Required property 'table_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.PayloadProperty"]]:
            '''Information needed to configure the payload.

            By default, AWS IoT Events generates a standard payload in JSON for any action. This action payload contains all attribute-value pairs that have the information about the detector model instance and the event triggered the action. To configure the action payload, you can use ``contentExpression`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodbv2.html#cfn-iotevents-detectormodel-dynamodbv2-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.PayloadProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamoDBv2Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.EventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "event_name": "eventName",
            "actions": "actions",
            "condition": "condition",
        },
    )
    class EventProperty:
        def __init__(
            self,
            *,
            event_name: builtins.str,
            actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union["CfnDetectorModel.ActionProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
            condition: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the ``actions`` to be performed when the ``condition`` evaluates to TRUE.

            :param event_name: The name of the event.
            :param actions: The actions to be performed.
            :param condition: Optional. The Boolean expression that, when TRUE, causes the ``actions`` to be performed. If not present, the actions are performed (=TRUE). If the expression result is not a Boolean value, the actions are not performed (=FALSE).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-event.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                event_property = iotevents.CfnDetectorModel.EventProperty(
                    event_name="eventName",
                
                    # the properties below are optional
                    actions=[iotevents.CfnDetectorModel.ActionProperty(
                        clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                            timer_name="timerName"
                        ),
                        dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                            hash_key_field="hashKeyField",
                            hash_key_value="hashKeyValue",
                            table_name="tableName",
                
                            # the properties below are optional
                            hash_key_type="hashKeyType",
                            operation="operation",
                            payload=iotevents.CfnDetectorModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            payload_field="payloadField",
                            range_key_field="rangeKeyField",
                            range_key_type="rangeKeyType",
                            range_key_value="rangeKeyValue"
                        ),
                        dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                            table_name="tableName",
                
                            # the properties below are optional
                            payload=iotevents.CfnDetectorModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                            delivery_stream_name="deliveryStreamName",
                
                            # the properties below are optional
                            payload=iotevents.CfnDetectorModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            separator="separator"
                        ),
                        iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                            input_name="inputName",
                
                            # the properties below are optional
                            payload=iotevents.CfnDetectorModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                            property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                    boolean_value="booleanValue",
                                    double_value="doubleValue",
                                    integer_value="integerValue",
                                    string_value="stringValue"
                                ),
                
                                # the properties below are optional
                                quality="quality",
                                timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                    time_in_seconds="timeInSeconds",
                
                                    # the properties below are optional
                                    offset_in_nanos="offsetInNanos"
                                )
                            ),
                
                            # the properties below are optional
                            asset_id="assetId",
                            entry_id="entryId",
                            property_alias="propertyAlias",
                            property_id="propertyId"
                        ),
                        iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                            mqtt_topic="mqttTopic",
                
                            # the properties below are optional
                            payload=iotevents.CfnDetectorModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                            function_arn="functionArn",
                
                            # the properties below are optional
                            payload=iotevents.CfnDetectorModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                            timer_name="timerName"
                        ),
                        set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                            timer_name="timerName",
                
                            # the properties below are optional
                            duration_expression="durationExpression",
                            seconds=123
                        ),
                        set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                            value="value",
                            variable_name="variableName"
                        ),
                        sns=iotevents.CfnDetectorModel.SnsProperty(
                            target_arn="targetArn",
                
                            # the properties below are optional
                            payload=iotevents.CfnDetectorModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        sqs=iotevents.CfnDetectorModel.SqsProperty(
                            queue_url="queueUrl",
                
                            # the properties below are optional
                            payload=iotevents.CfnDetectorModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            use_base64=False
                        )
                    )],
                    condition="condition"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b61761053338e03f2fcf818c1bf2130b57529b93342d9fb78c881fbc864df019)
                check_type(argname="argument event_name", value=event_name, expected_type=type_hints["event_name"])
                check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
                check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "event_name": event_name,
            }
            if actions is not None:
                self._values["actions"] = actions
            if condition is not None:
                self._values["condition"] = condition

        @builtins.property
        def event_name(self) -> builtins.str:
            '''The name of the event.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-event.html#cfn-iotevents-detectormodel-event-eventname
            '''
            result = self._values.get("event_name")
            assert result is not None, "Required property 'event_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnDetectorModel.ActionProperty", _aws_cdk_core_f4b25747.IResolvable]]]]:
            '''The actions to be performed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-event.html#cfn-iotevents-detectormodel-event-actions
            '''
            result = self._values.get("actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnDetectorModel.ActionProperty", _aws_cdk_core_f4b25747.IResolvable]]]], result)

        @builtins.property
        def condition(self) -> typing.Optional[builtins.str]:
            '''Optional.

            The Boolean expression that, when TRUE, causes the ``actions`` to be performed. If not present, the actions are performed (=TRUE). If the expression result is not a Boolean value, the actions are not performed (=FALSE).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-event.html#cfn-iotevents-detectormodel-event-condition
            '''
            result = self._values.get("condition")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.FirehoseProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delivery_stream_name": "deliveryStreamName",
            "payload": "payload",
            "separator": "separator",
        },
    )
    class FirehoseProperty:
        def __init__(
            self,
            *,
            delivery_stream_name: builtins.str,
            payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            separator: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Sends information about the detector model instance and the event that triggered the action to an Amazon Kinesis Data Firehose delivery stream.

            :param delivery_stream_name: The name of the Kinesis Data Firehose delivery stream where the data is written.
            :param payload: You can configure the action payload when you send a message to an Amazon Kinesis Data Firehose delivery stream.
            :param separator: A character separator that is used to separate records written to the Kinesis Data Firehose delivery stream. Valid values are: '\\n' (newline), '\\t' (tab), '\\r\\n' (Windows newline), ',' (comma).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-firehose.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                firehose_property = iotevents.CfnDetectorModel.FirehoseProperty(
                    delivery_stream_name="deliveryStreamName",
                
                    # the properties below are optional
                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    ),
                    separator="separator"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ba3b4ec59ca7a6d232da9b1730f785ec202ec42fe148cc714809748830f07de8)
                check_type(argname="argument delivery_stream_name", value=delivery_stream_name, expected_type=type_hints["delivery_stream_name"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
                check_type(argname="argument separator", value=separator, expected_type=type_hints["separator"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "delivery_stream_name": delivery_stream_name,
            }
            if payload is not None:
                self._values["payload"] = payload
            if separator is not None:
                self._values["separator"] = separator

        @builtins.property
        def delivery_stream_name(self) -> builtins.str:
            '''The name of the Kinesis Data Firehose delivery stream where the data is written.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-firehose.html#cfn-iotevents-detectormodel-firehose-deliverystreamname
            '''
            result = self._values.get("delivery_stream_name")
            assert result is not None, "Required property 'delivery_stream_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.PayloadProperty"]]:
            '''You can configure the action payload when you send a message to an Amazon Kinesis Data Firehose delivery stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-firehose.html#cfn-iotevents-detectormodel-firehose-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.PayloadProperty"]], result)

        @builtins.property
        def separator(self) -> typing.Optional[builtins.str]:
            '''A character separator that is used to separate records written to the Kinesis Data Firehose delivery stream.

            Valid values are: '\\n' (newline), '\\t' (tab), '\\r\\n' (Windows newline), ',' (comma).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-firehose.html#cfn-iotevents-detectormodel-firehose-separator
            '''
            result = self._values.get("separator")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FirehoseProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.IotEventsProperty",
        jsii_struct_bases=[],
        name_mapping={"input_name": "inputName", "payload": "payload"},
    )
    class IotEventsProperty:
        def __init__(
            self,
            *,
            input_name: builtins.str,
            payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Sends an AWS IoT Events input, passing in information about the detector model instance and the event that triggered the action.

            :param input_name: The name of the AWS IoT Events input where the data is sent.
            :param payload: You can configure the action payload when you send a message to an AWS IoT Events input.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotevents.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                iot_events_property = iotevents.CfnDetectorModel.IotEventsProperty(
                    input_name="inputName",
                
                    # the properties below are optional
                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6738bafd08f099889eaa028bcdd7d23d8f2f3a581a23f5f9b9010743ba140300)
                check_type(argname="argument input_name", value=input_name, expected_type=type_hints["input_name"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "input_name": input_name,
            }
            if payload is not None:
                self._values["payload"] = payload

        @builtins.property
        def input_name(self) -> builtins.str:
            '''The name of the AWS IoT Events input where the data is sent.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotevents.html#cfn-iotevents-detectormodel-iotevents-inputname
            '''
            result = self._values.get("input_name")
            assert result is not None, "Required property 'input_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.PayloadProperty"]]:
            '''You can configure the action payload when you send a message to an AWS IoT Events input.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotevents.html#cfn-iotevents-detectormodel-iotevents-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.PayloadProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IotEventsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.IotSiteWiseProperty",
        jsii_struct_bases=[],
        name_mapping={
            "property_value": "propertyValue",
            "asset_id": "assetId",
            "entry_id": "entryId",
            "property_alias": "propertyAlias",
            "property_id": "propertyId",
        },
    )
    class IotSiteWiseProperty:
        def __init__(
            self,
            *,
            property_value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.AssetPropertyValueProperty", typing.Dict[builtins.str, typing.Any]]],
            asset_id: typing.Optional[builtins.str] = None,
            entry_id: typing.Optional[builtins.str] = None,
            property_alias: typing.Optional[builtins.str] = None,
            property_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Sends information about the detector model instance and the event that triggered the action to a specified asset property in AWS IoT SiteWise .

            You must use expressions for all parameters in ``IotSiteWiseAction`` . The expressions accept literals, operators, functions, references, and substitutions templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``propertyAlias`` parameter can be ``'/company/windfarm/3/turbine/7/temperature'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``assetId`` parameter can be ``$input.TurbineInput.assetId1`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``propertyAlias`` parameter uses a substitution template.

            ``'company/windfarm/${$input.TemperatureInput.sensorData.windfarmID}/turbine/ ${$input.TemperatureInput.sensorData.turbineID}/temperature'``

            You must specify either ``propertyAlias`` or both ``assetId`` and ``propertyId`` to identify the target asset property in AWS IoT SiteWise .

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            :param property_value: The value to send to the asset property. This value contains timestamp, quality, and value (TQV) information.
            :param asset_id: The ID of the asset that has the specified property.
            :param entry_id: A unique identifier for this entry. You can use the entry ID to track which data entry causes an error in case of failure. The default is a new unique identifier.
            :param property_alias: The alias of the asset property.
            :param property_id: The ID of the asset property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotsitewise.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                iot_site_wise_property = iotevents.CfnDetectorModel.IotSiteWiseProperty(
                    property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                        value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                            boolean_value="booleanValue",
                            double_value="doubleValue",
                            integer_value="integerValue",
                            string_value="stringValue"
                        ),
                
                        # the properties below are optional
                        quality="quality",
                        timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                            time_in_seconds="timeInSeconds",
                
                            # the properties below are optional
                            offset_in_nanos="offsetInNanos"
                        )
                    ),
                
                    # the properties below are optional
                    asset_id="assetId",
                    entry_id="entryId",
                    property_alias="propertyAlias",
                    property_id="propertyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d0ea319e3419ecaaed81e94d4acc411e0f85ad42445d3174eeb741f3186fb0c9)
                check_type(argname="argument property_value", value=property_value, expected_type=type_hints["property_value"])
                check_type(argname="argument asset_id", value=asset_id, expected_type=type_hints["asset_id"])
                check_type(argname="argument entry_id", value=entry_id, expected_type=type_hints["entry_id"])
                check_type(argname="argument property_alias", value=property_alias, expected_type=type_hints["property_alias"])
                check_type(argname="argument property_id", value=property_id, expected_type=type_hints["property_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "property_value": property_value,
            }
            if asset_id is not None:
                self._values["asset_id"] = asset_id
            if entry_id is not None:
                self._values["entry_id"] = entry_id
            if property_alias is not None:
                self._values["property_alias"] = property_alias
            if property_id is not None:
                self._values["property_id"] = property_id

        @builtins.property
        def property_value(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.AssetPropertyValueProperty"]:
            '''The value to send to the asset property.

            This value contains timestamp, quality, and value (TQV) information.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotsitewise.html#cfn-iotevents-detectormodel-iotsitewise-propertyvalue
            '''
            result = self._values.get("property_value")
            assert result is not None, "Required property 'property_value' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.AssetPropertyValueProperty"], result)

        @builtins.property
        def asset_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the asset that has the specified property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotsitewise.html#cfn-iotevents-detectormodel-iotsitewise-assetid
            '''
            result = self._values.get("asset_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def entry_id(self) -> typing.Optional[builtins.str]:
            '''A unique identifier for this entry.

            You can use the entry ID to track which data entry causes an error in case of failure. The default is a new unique identifier.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotsitewise.html#cfn-iotevents-detectormodel-iotsitewise-entryid
            '''
            result = self._values.get("entry_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_alias(self) -> typing.Optional[builtins.str]:
            '''The alias of the asset property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotsitewise.html#cfn-iotevents-detectormodel-iotsitewise-propertyalias
            '''
            result = self._values.get("property_alias")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the asset property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotsitewise.html#cfn-iotevents-detectormodel-iotsitewise-propertyid
            '''
            result = self._values.get("property_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IotSiteWiseProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.IotTopicPublishProperty",
        jsii_struct_bases=[],
        name_mapping={"mqtt_topic": "mqttTopic", "payload": "payload"},
    )
    class IotTopicPublishProperty:
        def __init__(
            self,
            *,
            mqtt_topic: builtins.str,
            payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information required to publish the MQTT message through the AWS IoT message broker.

            :param mqtt_topic: The MQTT topic of the message. You can use a string expression that includes variables ( ``$variable.<variable-name>`` ) and input values ( ``$input.<input-name>.<path-to-datum>`` ) as the topic string.
            :param payload: You can configure the action payload when you publish a message to an AWS IoT Core topic.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iottopicpublish.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                iot_topic_publish_property = iotevents.CfnDetectorModel.IotTopicPublishProperty(
                    mqtt_topic="mqttTopic",
                
                    # the properties below are optional
                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3920e2a00706daf32dace0a6ea7dbe9aed3e387cc5d0dea3ef7767ef876fd325)
                check_type(argname="argument mqtt_topic", value=mqtt_topic, expected_type=type_hints["mqtt_topic"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "mqtt_topic": mqtt_topic,
            }
            if payload is not None:
                self._values["payload"] = payload

        @builtins.property
        def mqtt_topic(self) -> builtins.str:
            '''The MQTT topic of the message.

            You can use a string expression that includes variables ( ``$variable.<variable-name>`` ) and input values ( ``$input.<input-name>.<path-to-datum>`` ) as the topic string.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iottopicpublish.html#cfn-iotevents-detectormodel-iottopicpublish-mqtttopic
            '''
            result = self._values.get("mqtt_topic")
            assert result is not None, "Required property 'mqtt_topic' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.PayloadProperty"]]:
            '''You can configure the action payload when you publish a message to an AWS IoT Core topic.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iottopicpublish.html#cfn-iotevents-detectormodel-iottopicpublish-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.PayloadProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IotTopicPublishProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.LambdaProperty",
        jsii_struct_bases=[],
        name_mapping={"function_arn": "functionArn", "payload": "payload"},
    )
    class LambdaProperty:
        def __init__(
            self,
            *,
            function_arn: builtins.str,
            payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Calls a Lambda function, passing in information about the detector model instance and the event that triggered the action.

            :param function_arn: The ARN of the Lambda function that is executed.
            :param payload: You can configure the action payload when you send a message to a Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-lambda.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                lambda_property = iotevents.CfnDetectorModel.LambdaProperty(
                    function_arn="functionArn",
                
                    # the properties below are optional
                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__293a086a49c67b3204fd673189de27386c912f033ae6bc74d43463e58c9d0725)
                check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "function_arn": function_arn,
            }
            if payload is not None:
                self._values["payload"] = payload

        @builtins.property
        def function_arn(self) -> builtins.str:
            '''The ARN of the Lambda function that is executed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-lambda.html#cfn-iotevents-detectormodel-lambda-functionarn
            '''
            result = self._values.get("function_arn")
            assert result is not None, "Required property 'function_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.PayloadProperty"]]:
            '''You can configure the action payload when you send a message to a Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-lambda.html#cfn-iotevents-detectormodel-lambda-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.PayloadProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.OnEnterProperty",
        jsii_struct_bases=[],
        name_mapping={"events": "events"},
    )
    class OnEnterProperty:
        def __init__(
            self,
            *,
            events: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.EventProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''When entering this state, perform these ``actions`` if the ``condition`` is TRUE.

            :param events: Specifies the actions that are performed when the state is entered and the ``condition`` is ``TRUE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-onenter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                on_enter_property = iotevents.CfnDetectorModel.OnEnterProperty(
                    events=[iotevents.CfnDetectorModel.EventProperty(
                        event_name="eventName",
                
                        # the properties below are optional
                        actions=[iotevents.CfnDetectorModel.ActionProperty(
                            clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                                timer_name="timerName"
                            ),
                            dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                                hash_key_field="hashKeyField",
                                hash_key_value="hashKeyValue",
                                table_name="tableName",
                
                                # the properties below are optional
                                hash_key_type="hashKeyType",
                                operation="operation",
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                payload_field="payloadField",
                                range_key_field="rangeKeyField",
                                range_key_type="rangeKeyType",
                                range_key_value="rangeKeyValue"
                            ),
                            dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                                table_name="tableName",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                                delivery_stream_name="deliveryStreamName",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                separator="separator"
                            ),
                            iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                                input_name="inputName",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                                property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                    value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                        boolean_value="booleanValue",
                                        double_value="doubleValue",
                                        integer_value="integerValue",
                                        string_value="stringValue"
                                    ),
                
                                    # the properties below are optional
                                    quality="quality",
                                    timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                        time_in_seconds="timeInSeconds",
                
                                        # the properties below are optional
                                        offset_in_nanos="offsetInNanos"
                                    )
                                ),
                
                                # the properties below are optional
                                asset_id="assetId",
                                entry_id="entryId",
                                property_alias="propertyAlias",
                                property_id="propertyId"
                            ),
                            iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                                mqtt_topic="mqttTopic",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                                function_arn="functionArn",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                                timer_name="timerName"
                            ),
                            set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                                timer_name="timerName",
                
                                # the properties below are optional
                                duration_expression="durationExpression",
                                seconds=123
                            ),
                            set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                                value="value",
                                variable_name="variableName"
                            ),
                            sns=iotevents.CfnDetectorModel.SnsProperty(
                                target_arn="targetArn",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            sqs=iotevents.CfnDetectorModel.SqsProperty(
                                queue_url="queueUrl",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                use_base64=False
                            )
                        )],
                        condition="condition"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__05dba8292b91c490e5a24d386248dbb0280b4500201cbc3055bd83e4a417ce1d)
                check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if events is not None:
                self._values["events"] = events

        @builtins.property
        def events(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.EventProperty"]]]]:
            '''Specifies the actions that are performed when the state is entered and the ``condition`` is ``TRUE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-onenter.html#cfn-iotevents-detectormodel-onenter-events
            '''
            result = self._values.get("events")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.EventProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnEnterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.OnExitProperty",
        jsii_struct_bases=[],
        name_mapping={"events": "events"},
    )
    class OnExitProperty:
        def __init__(
            self,
            *,
            events: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.EventProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''When exiting this state, perform these ``actions`` if the specified ``condition`` is ``TRUE`` .

            :param events: Specifies the ``actions`` that are performed when the state is exited and the ``condition`` is ``TRUE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-onexit.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                on_exit_property = iotevents.CfnDetectorModel.OnExitProperty(
                    events=[iotevents.CfnDetectorModel.EventProperty(
                        event_name="eventName",
                
                        # the properties below are optional
                        actions=[iotevents.CfnDetectorModel.ActionProperty(
                            clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                                timer_name="timerName"
                            ),
                            dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                                hash_key_field="hashKeyField",
                                hash_key_value="hashKeyValue",
                                table_name="tableName",
                
                                # the properties below are optional
                                hash_key_type="hashKeyType",
                                operation="operation",
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                payload_field="payloadField",
                                range_key_field="rangeKeyField",
                                range_key_type="rangeKeyType",
                                range_key_value="rangeKeyValue"
                            ),
                            dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                                table_name="tableName",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                                delivery_stream_name="deliveryStreamName",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                separator="separator"
                            ),
                            iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                                input_name="inputName",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                                property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                    value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                        boolean_value="booleanValue",
                                        double_value="doubleValue",
                                        integer_value="integerValue",
                                        string_value="stringValue"
                                    ),
                
                                    # the properties below are optional
                                    quality="quality",
                                    timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                        time_in_seconds="timeInSeconds",
                
                                        # the properties below are optional
                                        offset_in_nanos="offsetInNanos"
                                    )
                                ),
                
                                # the properties below are optional
                                asset_id="assetId",
                                entry_id="entryId",
                                property_alias="propertyAlias",
                                property_id="propertyId"
                            ),
                            iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                                mqtt_topic="mqttTopic",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                                function_arn="functionArn",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                                timer_name="timerName"
                            ),
                            set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                                timer_name="timerName",
                
                                # the properties below are optional
                                duration_expression="durationExpression",
                                seconds=123
                            ),
                            set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                                value="value",
                                variable_name="variableName"
                            ),
                            sns=iotevents.CfnDetectorModel.SnsProperty(
                                target_arn="targetArn",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            sqs=iotevents.CfnDetectorModel.SqsProperty(
                                queue_url="queueUrl",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                use_base64=False
                            )
                        )],
                        condition="condition"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9afa050392906e9434389b9edae26edb2762c0e869f1aa4ff0dc3006750de422)
                check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if events is not None:
                self._values["events"] = events

        @builtins.property
        def events(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.EventProperty"]]]]:
            '''Specifies the ``actions`` that are performed when the state is exited and the ``condition`` is ``TRUE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-onexit.html#cfn-iotevents-detectormodel-onexit-events
            '''
            result = self._values.get("events")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.EventProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnExitProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.OnInputProperty",
        jsii_struct_bases=[],
        name_mapping={"events": "events", "transition_events": "transitionEvents"},
    )
    class OnInputProperty:
        def __init__(
            self,
            *,
            events: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.EventProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            transition_events: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.TransitionEventProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies the actions performed when the ``condition`` evaluates to TRUE.

            :param events: Specifies the actions performed when the ``condition`` evaluates to TRUE.
            :param transition_events: Specifies the actions performed, and the next state entered, when a ``condition`` evaluates to TRUE.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-oninput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                on_input_property = iotevents.CfnDetectorModel.OnInputProperty(
                    events=[iotevents.CfnDetectorModel.EventProperty(
                        event_name="eventName",
                
                        # the properties below are optional
                        actions=[iotevents.CfnDetectorModel.ActionProperty(
                            clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                                timer_name="timerName"
                            ),
                            dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                                hash_key_field="hashKeyField",
                                hash_key_value="hashKeyValue",
                                table_name="tableName",
                
                                # the properties below are optional
                                hash_key_type="hashKeyType",
                                operation="operation",
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                payload_field="payloadField",
                                range_key_field="rangeKeyField",
                                range_key_type="rangeKeyType",
                                range_key_value="rangeKeyValue"
                            ),
                            dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                                table_name="tableName",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                                delivery_stream_name="deliveryStreamName",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                separator="separator"
                            ),
                            iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                                input_name="inputName",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                                property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                    value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                        boolean_value="booleanValue",
                                        double_value="doubleValue",
                                        integer_value="integerValue",
                                        string_value="stringValue"
                                    ),
                
                                    # the properties below are optional
                                    quality="quality",
                                    timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                        time_in_seconds="timeInSeconds",
                
                                        # the properties below are optional
                                        offset_in_nanos="offsetInNanos"
                                    )
                                ),
                
                                # the properties below are optional
                                asset_id="assetId",
                                entry_id="entryId",
                                property_alias="propertyAlias",
                                property_id="propertyId"
                            ),
                            iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                                mqtt_topic="mqttTopic",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                                function_arn="functionArn",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                                timer_name="timerName"
                            ),
                            set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                                timer_name="timerName",
                
                                # the properties below are optional
                                duration_expression="durationExpression",
                                seconds=123
                            ),
                            set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                                value="value",
                                variable_name="variableName"
                            ),
                            sns=iotevents.CfnDetectorModel.SnsProperty(
                                target_arn="targetArn",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            sqs=iotevents.CfnDetectorModel.SqsProperty(
                                queue_url="queueUrl",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                use_base64=False
                            )
                        )],
                        condition="condition"
                    )],
                    transition_events=[iotevents.CfnDetectorModel.TransitionEventProperty(
                        condition="condition",
                        event_name="eventName",
                        next_state="nextState",
                
                        # the properties below are optional
                        actions=[iotevents.CfnDetectorModel.ActionProperty(
                            clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                                timer_name="timerName"
                            ),
                            dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                                hash_key_field="hashKeyField",
                                hash_key_value="hashKeyValue",
                                table_name="tableName",
                
                                # the properties below are optional
                                hash_key_type="hashKeyType",
                                operation="operation",
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                payload_field="payloadField",
                                range_key_field="rangeKeyField",
                                range_key_type="rangeKeyType",
                                range_key_value="rangeKeyValue"
                            ),
                            dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                                table_name="tableName",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                                delivery_stream_name="deliveryStreamName",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                separator="separator"
                            ),
                            iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                                input_name="inputName",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                                property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                    value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                        boolean_value="booleanValue",
                                        double_value="doubleValue",
                                        integer_value="integerValue",
                                        string_value="stringValue"
                                    ),
                
                                    # the properties below are optional
                                    quality="quality",
                                    timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                        time_in_seconds="timeInSeconds",
                
                                        # the properties below are optional
                                        offset_in_nanos="offsetInNanos"
                                    )
                                ),
                
                                # the properties below are optional
                                asset_id="assetId",
                                entry_id="entryId",
                                property_alias="propertyAlias",
                                property_id="propertyId"
                            ),
                            iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                                mqtt_topic="mqttTopic",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                                function_arn="functionArn",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                                timer_name="timerName"
                            ),
                            set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                                timer_name="timerName",
                
                                # the properties below are optional
                                duration_expression="durationExpression",
                                seconds=123
                            ),
                            set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                                value="value",
                                variable_name="variableName"
                            ),
                            sns=iotevents.CfnDetectorModel.SnsProperty(
                                target_arn="targetArn",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            sqs=iotevents.CfnDetectorModel.SqsProperty(
                                queue_url="queueUrl",
                
                                # the properties below are optional
                                payload=iotevents.CfnDetectorModel.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                use_base64=False
                            )
                        )]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2e1f51bf4a7f70eed01fd39b1db9e0dc17066d5cf08a553a091cfa0a6c0d4d5f)
                check_type(argname="argument events", value=events, expected_type=type_hints["events"])
                check_type(argname="argument transition_events", value=transition_events, expected_type=type_hints["transition_events"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if events is not None:
                self._values["events"] = events
            if transition_events is not None:
                self._values["transition_events"] = transition_events

        @builtins.property
        def events(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.EventProperty"]]]]:
            '''Specifies the actions performed when the ``condition`` evaluates to TRUE.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-oninput.html#cfn-iotevents-detectormodel-oninput-events
            '''
            result = self._values.get("events")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.EventProperty"]]]], result)

        @builtins.property
        def transition_events(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.TransitionEventProperty"]]]]:
            '''Specifies the actions performed, and the next state entered, when a ``condition`` evaluates to TRUE.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-oninput.html#cfn-iotevents-detectormodel-oninput-transitionevents
            '''
            result = self._values.get("transition_events")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.TransitionEventProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.PayloadProperty",
        jsii_struct_bases=[],
        name_mapping={"content_expression": "contentExpression", "type": "type"},
    )
    class PayloadProperty:
        def __init__(
            self,
            *,
            content_expression: builtins.str,
            type: builtins.str,
        ) -> None:
            '''Information needed to configure the payload.

            By default, AWS IoT Events generates a standard payload in JSON for any action. This action payload contains all attribute-value pairs that have the information about the detector model instance and the event triggered the action. To configure the action payload, you can use ``contentExpression`` .

            :param content_expression: The content of the payload. You can use a string expression that includes quoted strings ( ``'<string>'`` ), variables ( ``$variable.<variable-name>`` ), input values ( ``$input.<input-name>.<path-to-datum>`` ), string concatenations, and quoted strings that contain ``${}`` as the content. The recommended maximum size of a content expression is 1 KB.
            :param type: The value of the payload type can be either ``STRING`` or ``JSON`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-payload.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                payload_property = iotevents.CfnDetectorModel.PayloadProperty(
                    content_expression="contentExpression",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c78c1e0ebddc06eb1d8f94cd4699159bcbf6a62da73d5b2c579414e407737b4)
                check_type(argname="argument content_expression", value=content_expression, expected_type=type_hints["content_expression"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "content_expression": content_expression,
                "type": type,
            }

        @builtins.property
        def content_expression(self) -> builtins.str:
            '''The content of the payload.

            You can use a string expression that includes quoted strings ( ``'<string>'`` ), variables ( ``$variable.<variable-name>`` ), input values ( ``$input.<input-name>.<path-to-datum>`` ), string concatenations, and quoted strings that contain ``${}`` as the content. The recommended maximum size of a content expression is 1 KB.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-payload.html#cfn-iotevents-detectormodel-payload-contentexpression
            '''
            result = self._values.get("content_expression")
            assert result is not None, "Required property 'content_expression' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def type(self) -> builtins.str:
            '''The value of the payload type can be either ``STRING`` or ``JSON`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-payload.html#cfn-iotevents-detectormodel-payload-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PayloadProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.ResetTimerProperty",
        jsii_struct_bases=[],
        name_mapping={"timer_name": "timerName"},
    )
    class ResetTimerProperty:
        def __init__(self, *, timer_name: builtins.str) -> None:
            '''Information required to reset the timer.

            The timer is reset to the previously evaluated result of the duration. The duration expression isn't reevaluated when you reset the timer.

            :param timer_name: The name of the timer to reset.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-resettimer.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                reset_timer_property = iotevents.CfnDetectorModel.ResetTimerProperty(
                    timer_name="timerName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0135145118d95eda2e4ebc894b6ea9648f4fe9dafc0bd12979bc95803e71ae2c)
                check_type(argname="argument timer_name", value=timer_name, expected_type=type_hints["timer_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "timer_name": timer_name,
            }

        @builtins.property
        def timer_name(self) -> builtins.str:
            '''The name of the timer to reset.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-resettimer.html#cfn-iotevents-detectormodel-resettimer-timername
            '''
            result = self._values.get("timer_name")
            assert result is not None, "Required property 'timer_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResetTimerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.SetTimerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "timer_name": "timerName",
            "duration_expression": "durationExpression",
            "seconds": "seconds",
        },
    )
    class SetTimerProperty:
        def __init__(
            self,
            *,
            timer_name: builtins.str,
            duration_expression: typing.Optional[builtins.str] = None,
            seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information needed to set the timer.

            :param timer_name: The name of the timer.
            :param duration_expression: The duration of the timer, in seconds. You can use a string expression that includes numbers, variables ( ``$variable.<variable-name>`` ), and input values ( ``$input.<input-name>.<path-to-datum>`` ) as the duration. The range of the duration is 1-31622400 seconds. To ensure accuracy, the minimum duration is 60 seconds. The evaluated result of the duration is rounded down to the nearest whole number.
            :param seconds: The number of seconds until the timer expires. The minimum value is 60 seconds to ensure accuracy. The maximum value is 31622400 seconds.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-settimer.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                set_timer_property = iotevents.CfnDetectorModel.SetTimerProperty(
                    timer_name="timerName",
                
                    # the properties below are optional
                    duration_expression="durationExpression",
                    seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0917589c4b566176b94107f82e1799155dc39252113d78103c0b1b4e0514af7d)
                check_type(argname="argument timer_name", value=timer_name, expected_type=type_hints["timer_name"])
                check_type(argname="argument duration_expression", value=duration_expression, expected_type=type_hints["duration_expression"])
                check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "timer_name": timer_name,
            }
            if duration_expression is not None:
                self._values["duration_expression"] = duration_expression
            if seconds is not None:
                self._values["seconds"] = seconds

        @builtins.property
        def timer_name(self) -> builtins.str:
            '''The name of the timer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-settimer.html#cfn-iotevents-detectormodel-settimer-timername
            '''
            result = self._values.get("timer_name")
            assert result is not None, "Required property 'timer_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def duration_expression(self) -> typing.Optional[builtins.str]:
            '''The duration of the timer, in seconds.

            You can use a string expression that includes numbers, variables ( ``$variable.<variable-name>`` ), and input values ( ``$input.<input-name>.<path-to-datum>`` ) as the duration. The range of the duration is 1-31622400 seconds. To ensure accuracy, the minimum duration is 60 seconds. The evaluated result of the duration is rounded down to the nearest whole number.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-settimer.html#cfn-iotevents-detectormodel-settimer-durationexpression
            '''
            result = self._values.get("duration_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def seconds(self) -> typing.Optional[jsii.Number]:
            '''The number of seconds until the timer expires.

            The minimum value is 60 seconds to ensure accuracy. The maximum value is 31622400 seconds.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-settimer.html#cfn-iotevents-detectormodel-settimer-seconds
            '''
            result = self._values.get("seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SetTimerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.SetVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value", "variable_name": "variableName"},
    )
    class SetVariableProperty:
        def __init__(self, *, value: builtins.str, variable_name: builtins.str) -> None:
            '''Information about the variable and its new value.

            :param value: The new value of the variable.
            :param variable_name: The name of the variable.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-setvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                set_variable_property = iotevents.CfnDetectorModel.SetVariableProperty(
                    value="value",
                    variable_name="variableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7f166d174dbdec15ea523e0d5e5673a6cee715c762ca23b1ff9b1b0e5a94c90c)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                check_type(argname="argument variable_name", value=variable_name, expected_type=type_hints["variable_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "value": value,
                "variable_name": variable_name,
            }

        @builtins.property
        def value(self) -> builtins.str:
            '''The new value of the variable.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-setvariable.html#cfn-iotevents-detectormodel-setvariable-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def variable_name(self) -> builtins.str:
            '''The name of the variable.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-setvariable.html#cfn-iotevents-detectormodel-setvariable-variablename
            '''
            result = self._values.get("variable_name")
            assert result is not None, "Required property 'variable_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SetVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.SnsProperty",
        jsii_struct_bases=[],
        name_mapping={"target_arn": "targetArn", "payload": "payload"},
    )
    class SnsProperty:
        def __init__(
            self,
            *,
            target_arn: builtins.str,
            payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information required to publish the Amazon SNS message.

            :param target_arn: The ARN of the Amazon SNS target where the message is sent.
            :param payload: You can configure the action payload when you send a message as an Amazon SNS push notification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sns.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                sns_property = iotevents.CfnDetectorModel.SnsProperty(
                    target_arn="targetArn",
                
                    # the properties below are optional
                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6e5c8988e7bc1074899c099b5589c681ce7e914462ad5133869d72104c97f034)
                check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "target_arn": target_arn,
            }
            if payload is not None:
                self._values["payload"] = payload

        @builtins.property
        def target_arn(self) -> builtins.str:
            '''The ARN of the Amazon SNS target where the message is sent.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sns.html#cfn-iotevents-detectormodel-sns-targetarn
            '''
            result = self._values.get("target_arn")
            assert result is not None, "Required property 'target_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.PayloadProperty"]]:
            '''You can configure the action payload when you send a message as an Amazon SNS push notification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sns.html#cfn-iotevents-detectormodel-sns-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.PayloadProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.SqsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "queue_url": "queueUrl",
            "payload": "payload",
            "use_base64": "useBase64",
        },
    )
    class SqsProperty:
        def __init__(
            self,
            *,
            queue_url: builtins.str,
            payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            use_base64: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Sends information about the detector model instance and the event that triggered the action to an Amazon SQS queue.

            :param queue_url: The URL of the SQS queue where the data is written.
            :param payload: You can configure the action payload when you send a message to an Amazon SQS queue.
            :param use_base64: Set this to TRUE if you want the data to be base-64 encoded before it is written to the queue. Otherwise, set this to FALSE.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sqs.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                sqs_property = iotevents.CfnDetectorModel.SqsProperty(
                    queue_url="queueUrl",
                
                    # the properties below are optional
                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    ),
                    use_base64=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__61f4b00db15cec4d0e31cd3ae94cde0fe4240511b1191fbf746ae165a36538fd)
                check_type(argname="argument queue_url", value=queue_url, expected_type=type_hints["queue_url"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
                check_type(argname="argument use_base64", value=use_base64, expected_type=type_hints["use_base64"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "queue_url": queue_url,
            }
            if payload is not None:
                self._values["payload"] = payload
            if use_base64 is not None:
                self._values["use_base64"] = use_base64

        @builtins.property
        def queue_url(self) -> builtins.str:
            '''The URL of the SQS queue where the data is written.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sqs.html#cfn-iotevents-detectormodel-sqs-queueurl
            '''
            result = self._values.get("queue_url")
            assert result is not None, "Required property 'queue_url' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.PayloadProperty"]]:
            '''You can configure the action payload when you send a message to an Amazon SQS queue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sqs.html#cfn-iotevents-detectormodel-sqs-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.PayloadProperty"]], result)

        @builtins.property
        def use_base64(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Set this to TRUE if you want the data to be base-64 encoded before it is written to the queue.

            Otherwise, set this to FALSE.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sqs.html#cfn-iotevents-detectormodel-sqs-usebase64
            '''
            result = self._values.get("use_base64")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SqsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.StateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "state_name": "stateName",
            "on_enter": "onEnter",
            "on_exit": "onExit",
            "on_input": "onInput",
        },
    )
    class StateProperty:
        def __init__(
            self,
            *,
            state_name: builtins.str,
            on_enter: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.OnEnterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            on_exit: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.OnExitProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            on_input: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetectorModel.OnInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information that defines a state of a detector.

            :param state_name: The name of the state.
            :param on_enter: When entering this state, perform these ``actions`` if the ``condition`` is TRUE.
            :param on_exit: When exiting this state, perform these ``actions`` if the specified ``condition`` is ``TRUE`` .
            :param on_input: When an input is received and the ``condition`` is TRUE, perform the specified ``actions`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-state.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                state_property = iotevents.CfnDetectorModel.StateProperty(
                    state_name="stateName",
                
                    # the properties below are optional
                    on_enter=iotevents.CfnDetectorModel.OnEnterProperty(
                        events=[iotevents.CfnDetectorModel.EventProperty(
                            event_name="eventName",
                
                            # the properties below are optional
                            actions=[iotevents.CfnDetectorModel.ActionProperty(
                                clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                                    timer_name="timerName"
                                ),
                                dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                                    hash_key_field="hashKeyField",
                                    hash_key_value="hashKeyValue",
                                    table_name="tableName",
                
                                    # the properties below are optional
                                    hash_key_type="hashKeyType",
                                    operation="operation",
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    payload_field="payloadField",
                                    range_key_field="rangeKeyField",
                                    range_key_type="rangeKeyType",
                                    range_key_value="rangeKeyValue"
                                ),
                                dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                                    table_name="tableName",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                                    delivery_stream_name="deliveryStreamName",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    separator="separator"
                                ),
                                iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                                    input_name="inputName",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                                    property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                        value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                            boolean_value="booleanValue",
                                            double_value="doubleValue",
                                            integer_value="integerValue",
                                            string_value="stringValue"
                                        ),
                
                                        # the properties below are optional
                                        quality="quality",
                                        timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                            time_in_seconds="timeInSeconds",
                
                                            # the properties below are optional
                                            offset_in_nanos="offsetInNanos"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    asset_id="assetId",
                                    entry_id="entryId",
                                    property_alias="propertyAlias",
                                    property_id="propertyId"
                                ),
                                iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                                    mqtt_topic="mqttTopic",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                                    function_arn="functionArn",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                                    timer_name="timerName"
                                ),
                                set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                                    timer_name="timerName",
                
                                    # the properties below are optional
                                    duration_expression="durationExpression",
                                    seconds=123
                                ),
                                set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                                    value="value",
                                    variable_name="variableName"
                                ),
                                sns=iotevents.CfnDetectorModel.SnsProperty(
                                    target_arn="targetArn",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                sqs=iotevents.CfnDetectorModel.SqsProperty(
                                    queue_url="queueUrl",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    use_base64=False
                                )
                            )],
                            condition="condition"
                        )]
                    ),
                    on_exit=iotevents.CfnDetectorModel.OnExitProperty(
                        events=[iotevents.CfnDetectorModel.EventProperty(
                            event_name="eventName",
                
                            # the properties below are optional
                            actions=[iotevents.CfnDetectorModel.ActionProperty(
                                clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                                    timer_name="timerName"
                                ),
                                dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                                    hash_key_field="hashKeyField",
                                    hash_key_value="hashKeyValue",
                                    table_name="tableName",
                
                                    # the properties below are optional
                                    hash_key_type="hashKeyType",
                                    operation="operation",
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    payload_field="payloadField",
                                    range_key_field="rangeKeyField",
                                    range_key_type="rangeKeyType",
                                    range_key_value="rangeKeyValue"
                                ),
                                dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                                    table_name="tableName",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                                    delivery_stream_name="deliveryStreamName",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    separator="separator"
                                ),
                                iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                                    input_name="inputName",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                                    property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                        value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                            boolean_value="booleanValue",
                                            double_value="doubleValue",
                                            integer_value="integerValue",
                                            string_value="stringValue"
                                        ),
                
                                        # the properties below are optional
                                        quality="quality",
                                        timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                            time_in_seconds="timeInSeconds",
                
                                            # the properties below are optional
                                            offset_in_nanos="offsetInNanos"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    asset_id="assetId",
                                    entry_id="entryId",
                                    property_alias="propertyAlias",
                                    property_id="propertyId"
                                ),
                                iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                                    mqtt_topic="mqttTopic",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                                    function_arn="functionArn",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                                    timer_name="timerName"
                                ),
                                set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                                    timer_name="timerName",
                
                                    # the properties below are optional
                                    duration_expression="durationExpression",
                                    seconds=123
                                ),
                                set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                                    value="value",
                                    variable_name="variableName"
                                ),
                                sns=iotevents.CfnDetectorModel.SnsProperty(
                                    target_arn="targetArn",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                sqs=iotevents.CfnDetectorModel.SqsProperty(
                                    queue_url="queueUrl",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    use_base64=False
                                )
                            )],
                            condition="condition"
                        )]
                    ),
                    on_input=iotevents.CfnDetectorModel.OnInputProperty(
                        events=[iotevents.CfnDetectorModel.EventProperty(
                            event_name="eventName",
                
                            # the properties below are optional
                            actions=[iotevents.CfnDetectorModel.ActionProperty(
                                clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                                    timer_name="timerName"
                                ),
                                dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                                    hash_key_field="hashKeyField",
                                    hash_key_value="hashKeyValue",
                                    table_name="tableName",
                
                                    # the properties below are optional
                                    hash_key_type="hashKeyType",
                                    operation="operation",
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    payload_field="payloadField",
                                    range_key_field="rangeKeyField",
                                    range_key_type="rangeKeyType",
                                    range_key_value="rangeKeyValue"
                                ),
                                dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                                    table_name="tableName",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                                    delivery_stream_name="deliveryStreamName",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    separator="separator"
                                ),
                                iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                                    input_name="inputName",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                                    property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                        value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                            boolean_value="booleanValue",
                                            double_value="doubleValue",
                                            integer_value="integerValue",
                                            string_value="stringValue"
                                        ),
                
                                        # the properties below are optional
                                        quality="quality",
                                        timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                            time_in_seconds="timeInSeconds",
                
                                            # the properties below are optional
                                            offset_in_nanos="offsetInNanos"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    asset_id="assetId",
                                    entry_id="entryId",
                                    property_alias="propertyAlias",
                                    property_id="propertyId"
                                ),
                                iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                                    mqtt_topic="mqttTopic",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                                    function_arn="functionArn",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                                    timer_name="timerName"
                                ),
                                set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                                    timer_name="timerName",
                
                                    # the properties below are optional
                                    duration_expression="durationExpression",
                                    seconds=123
                                ),
                                set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                                    value="value",
                                    variable_name="variableName"
                                ),
                                sns=iotevents.CfnDetectorModel.SnsProperty(
                                    target_arn="targetArn",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                sqs=iotevents.CfnDetectorModel.SqsProperty(
                                    queue_url="queueUrl",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    use_base64=False
                                )
                            )],
                            condition="condition"
                        )],
                        transition_events=[iotevents.CfnDetectorModel.TransitionEventProperty(
                            condition="condition",
                            event_name="eventName",
                            next_state="nextState",
                
                            # the properties below are optional
                            actions=[iotevents.CfnDetectorModel.ActionProperty(
                                clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                                    timer_name="timerName"
                                ),
                                dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                                    hash_key_field="hashKeyField",
                                    hash_key_value="hashKeyValue",
                                    table_name="tableName",
                
                                    # the properties below are optional
                                    hash_key_type="hashKeyType",
                                    operation="operation",
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    payload_field="payloadField",
                                    range_key_field="rangeKeyField",
                                    range_key_type="rangeKeyType",
                                    range_key_value="rangeKeyValue"
                                ),
                                dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                                    table_name="tableName",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                                    delivery_stream_name="deliveryStreamName",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    separator="separator"
                                ),
                                iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                                    input_name="inputName",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                                    property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                        value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                            boolean_value="booleanValue",
                                            double_value="doubleValue",
                                            integer_value="integerValue",
                                            string_value="stringValue"
                                        ),
                
                                        # the properties below are optional
                                        quality="quality",
                                        timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                            time_in_seconds="timeInSeconds",
                
                                            # the properties below are optional
                                            offset_in_nanos="offsetInNanos"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    asset_id="assetId",
                                    entry_id="entryId",
                                    property_alias="propertyAlias",
                                    property_id="propertyId"
                                ),
                                iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                                    mqtt_topic="mqttTopic",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                                    function_arn="functionArn",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                                    timer_name="timerName"
                                ),
                                set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                                    timer_name="timerName",
                
                                    # the properties below are optional
                                    duration_expression="durationExpression",
                                    seconds=123
                                ),
                                set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                                    value="value",
                                    variable_name="variableName"
                                ),
                                sns=iotevents.CfnDetectorModel.SnsProperty(
                                    target_arn="targetArn",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                sqs=iotevents.CfnDetectorModel.SqsProperty(
                                    queue_url="queueUrl",
                
                                    # the properties below are optional
                                    payload=iotevents.CfnDetectorModel.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    use_base64=False
                                )
                            )]
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ad72a224aee928a149d5a9da9a562a5f111b31203a328cc4a8fed15dc8c90f32)
                check_type(argname="argument state_name", value=state_name, expected_type=type_hints["state_name"])
                check_type(argname="argument on_enter", value=on_enter, expected_type=type_hints["on_enter"])
                check_type(argname="argument on_exit", value=on_exit, expected_type=type_hints["on_exit"])
                check_type(argname="argument on_input", value=on_input, expected_type=type_hints["on_input"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "state_name": state_name,
            }
            if on_enter is not None:
                self._values["on_enter"] = on_enter
            if on_exit is not None:
                self._values["on_exit"] = on_exit
            if on_input is not None:
                self._values["on_input"] = on_input

        @builtins.property
        def state_name(self) -> builtins.str:
            '''The name of the state.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-state.html#cfn-iotevents-detectormodel-state-statename
            '''
            result = self._values.get("state_name")
            assert result is not None, "Required property 'state_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def on_enter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.OnEnterProperty"]]:
            '''When entering this state, perform these ``actions`` if the ``condition`` is TRUE.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-state.html#cfn-iotevents-detectormodel-state-onenter
            '''
            result = self._values.get("on_enter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.OnEnterProperty"]], result)

        @builtins.property
        def on_exit(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.OnExitProperty"]]:
            '''When exiting this state, perform these ``actions`` if the specified ``condition`` is ``TRUE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-state.html#cfn-iotevents-detectormodel-state-onexit
            '''
            result = self._values.get("on_exit")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.OnExitProperty"]], result)

        @builtins.property
        def on_input(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.OnInputProperty"]]:
            '''When an input is received and the ``condition`` is TRUE, perform the specified ``actions`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-state.html#cfn-iotevents-detectormodel-state-oninput
            '''
            result = self._values.get("on_input")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetectorModel.OnInputProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModel.TransitionEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "condition": "condition",
            "event_name": "eventName",
            "next_state": "nextState",
            "actions": "actions",
        },
    )
    class TransitionEventProperty:
        def __init__(
            self,
            *,
            condition: builtins.str,
            event_name: builtins.str,
            next_state: builtins.str,
            actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union["CfnDetectorModel.ActionProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
        ) -> None:
            '''Specifies the actions performed and the next state entered when a ``condition`` evaluates to TRUE.

            :param condition: Required. A Boolean expression that when TRUE causes the actions to be performed and the ``nextState`` to be entered.
            :param event_name: The name of the transition event.
            :param next_state: The next state to enter.
            :param actions: The actions to be performed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-transitionevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                transition_event_property = iotevents.CfnDetectorModel.TransitionEventProperty(
                    condition="condition",
                    event_name="eventName",
                    next_state="nextState",
                
                    # the properties below are optional
                    actions=[iotevents.CfnDetectorModel.ActionProperty(
                        clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                            timer_name="timerName"
                        ),
                        dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                            hash_key_field="hashKeyField",
                            hash_key_value="hashKeyValue",
                            table_name="tableName",
                
                            # the properties below are optional
                            hash_key_type="hashKeyType",
                            operation="operation",
                            payload=iotevents.CfnDetectorModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            payload_field="payloadField",
                            range_key_field="rangeKeyField",
                            range_key_type="rangeKeyType",
                            range_key_value="rangeKeyValue"
                        ),
                        dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                            table_name="tableName",
                
                            # the properties below are optional
                            payload=iotevents.CfnDetectorModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                            delivery_stream_name="deliveryStreamName",
                
                            # the properties below are optional
                            payload=iotevents.CfnDetectorModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            separator="separator"
                        ),
                        iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                            input_name="inputName",
                
                            # the properties below are optional
                            payload=iotevents.CfnDetectorModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                            property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                    boolean_value="booleanValue",
                                    double_value="doubleValue",
                                    integer_value="integerValue",
                                    string_value="stringValue"
                                ),
                
                                # the properties below are optional
                                quality="quality",
                                timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                    time_in_seconds="timeInSeconds",
                
                                    # the properties below are optional
                                    offset_in_nanos="offsetInNanos"
                                )
                            ),
                
                            # the properties below are optional
                            asset_id="assetId",
                            entry_id="entryId",
                            property_alias="propertyAlias",
                            property_id="propertyId"
                        ),
                        iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                            mqtt_topic="mqttTopic",
                
                            # the properties below are optional
                            payload=iotevents.CfnDetectorModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                            function_arn="functionArn",
                
                            # the properties below are optional
                            payload=iotevents.CfnDetectorModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                            timer_name="timerName"
                        ),
                        set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                            timer_name="timerName",
                
                            # the properties below are optional
                            duration_expression="durationExpression",
                            seconds=123
                        ),
                        set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                            value="value",
                            variable_name="variableName"
                        ),
                        sns=iotevents.CfnDetectorModel.SnsProperty(
                            target_arn="targetArn",
                
                            # the properties below are optional
                            payload=iotevents.CfnDetectorModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        sqs=iotevents.CfnDetectorModel.SqsProperty(
                            queue_url="queueUrl",
                
                            # the properties below are optional
                            payload=iotevents.CfnDetectorModel.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            use_base64=False
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8c559f87f0cd942e9bcd26f6e591d9ad45420f38a707a30b3f6818f33e08af2d)
                check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
                check_type(argname="argument event_name", value=event_name, expected_type=type_hints["event_name"])
                check_type(argname="argument next_state", value=next_state, expected_type=type_hints["next_state"])
                check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "condition": condition,
                "event_name": event_name,
                "next_state": next_state,
            }
            if actions is not None:
                self._values["actions"] = actions

        @builtins.property
        def condition(self) -> builtins.str:
            '''Required.

            A Boolean expression that when TRUE causes the actions to be performed and the ``nextState`` to be entered.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-transitionevent.html#cfn-iotevents-detectormodel-transitionevent-condition
            '''
            result = self._values.get("condition")
            assert result is not None, "Required property 'condition' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def event_name(self) -> builtins.str:
            '''The name of the transition event.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-transitionevent.html#cfn-iotevents-detectormodel-transitionevent-eventname
            '''
            result = self._values.get("event_name")
            assert result is not None, "Required property 'event_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def next_state(self) -> builtins.str:
            '''The next state to enter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-transitionevent.html#cfn-iotevents-detectormodel-transitionevent-nextstate
            '''
            result = self._values.get("next_state")
            assert result is not None, "Required property 'next_state' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnDetectorModel.ActionProperty", _aws_cdk_core_f4b25747.IResolvable]]]]:
            '''The actions to be performed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-transitionevent.html#cfn-iotevents-detectormodel-transitionevent-actions
            '''
            result = self._values.get("actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnDetectorModel.ActionProperty", _aws_cdk_core_f4b25747.IResolvable]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TransitionEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iotevents.CfnDetectorModelProps",
    jsii_struct_bases=[],
    name_mapping={
        "detector_model_definition": "detectorModelDefinition",
        "role_arn": "roleArn",
        "detector_model_description": "detectorModelDescription",
        "detector_model_name": "detectorModelName",
        "evaluation_method": "evaluationMethod",
        "key": "key",
        "tags": "tags",
    },
)
class CfnDetectorModelProps:
    def __init__(
        self,
        *,
        detector_model_definition: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.DetectorModelDefinitionProperty, typing.Dict[builtins.str, typing.Any]]],
        role_arn: builtins.str,
        detector_model_description: typing.Optional[builtins.str] = None,
        detector_model_name: typing.Optional[builtins.str] = None,
        evaluation_method: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDetectorModel``.

        :param detector_model_definition: Information that defines how a detector operates.
        :param role_arn: The ARN of the role that grants permission to AWS IoT Events to perform its operations.
        :param detector_model_description: A brief description of the detector model.
        :param detector_model_name: The name of the detector model.
        :param evaluation_method: Information about the order in which events are evaluated and how actions are executed.
        :param key: The value used to identify a detector instance. When a device or system sends input, a new detector instance with a unique key value is created. AWS IoT Events can continue to route input to its corresponding detector instance based on this identifying information. This parameter uses a JSON-path expression to select the attribute-value pair in the message payload that is used for identification. To route the message to the correct detector instance, the device must send a message payload that contains the same attribute-value.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iotevents as iotevents
            
            cfn_detector_model_props = iotevents.CfnDetectorModelProps(
                detector_model_definition=iotevents.CfnDetectorModel.DetectorModelDefinitionProperty(
                    initial_state_name="initialStateName",
                    states=[iotevents.CfnDetectorModel.StateProperty(
                        state_name="stateName",
            
                        # the properties below are optional
                        on_enter=iotevents.CfnDetectorModel.OnEnterProperty(
                            events=[iotevents.CfnDetectorModel.EventProperty(
                                event_name="eventName",
            
                                # the properties below are optional
                                actions=[iotevents.CfnDetectorModel.ActionProperty(
                                    clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                                        hash_key_field="hashKeyField",
                                        hash_key_value="hashKeyValue",
                                        table_name="tableName",
            
                                        # the properties below are optional
                                        hash_key_type="hashKeyType",
                                        operation="operation",
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        payload_field="payloadField",
                                        range_key_field="rangeKeyField",
                                        range_key_type="rangeKeyType",
                                        range_key_value="rangeKeyValue"
                                    ),
                                    dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                                        table_name="tableName",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                                        delivery_stream_name="deliveryStreamName",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        separator="separator"
                                    ),
                                    iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                                        input_name="inputName",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                                        property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                            value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                                boolean_value="booleanValue",
                                                double_value="doubleValue",
                                                integer_value="integerValue",
                                                string_value="stringValue"
                                            ),
            
                                            # the properties below are optional
                                            quality="quality",
                                            timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                                time_in_seconds="timeInSeconds",
            
                                                # the properties below are optional
                                                offset_in_nanos="offsetInNanos"
                                            )
                                        ),
            
                                        # the properties below are optional
                                        asset_id="assetId",
                                        entry_id="entryId",
                                        property_alias="propertyAlias",
                                        property_id="propertyId"
                                    ),
                                    iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                                        mqtt_topic="mqttTopic",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                                        function_arn="functionArn",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                                        timer_name="timerName",
            
                                        # the properties below are optional
                                        duration_expression="durationExpression",
                                        seconds=123
                                    ),
                                    set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                                        value="value",
                                        variable_name="variableName"
                                    ),
                                    sns=iotevents.CfnDetectorModel.SnsProperty(
                                        target_arn="targetArn",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    sqs=iotevents.CfnDetectorModel.SqsProperty(
                                        queue_url="queueUrl",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        use_base64=False
                                    )
                                )],
                                condition="condition"
                            )]
                        ),
                        on_exit=iotevents.CfnDetectorModel.OnExitProperty(
                            events=[iotevents.CfnDetectorModel.EventProperty(
                                event_name="eventName",
            
                                # the properties below are optional
                                actions=[iotevents.CfnDetectorModel.ActionProperty(
                                    clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                                        hash_key_field="hashKeyField",
                                        hash_key_value="hashKeyValue",
                                        table_name="tableName",
            
                                        # the properties below are optional
                                        hash_key_type="hashKeyType",
                                        operation="operation",
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        payload_field="payloadField",
                                        range_key_field="rangeKeyField",
                                        range_key_type="rangeKeyType",
                                        range_key_value="rangeKeyValue"
                                    ),
                                    dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                                        table_name="tableName",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                                        delivery_stream_name="deliveryStreamName",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        separator="separator"
                                    ),
                                    iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                                        input_name="inputName",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                                        property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                            value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                                boolean_value="booleanValue",
                                                double_value="doubleValue",
                                                integer_value="integerValue",
                                                string_value="stringValue"
                                            ),
            
                                            # the properties below are optional
                                            quality="quality",
                                            timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                                time_in_seconds="timeInSeconds",
            
                                                # the properties below are optional
                                                offset_in_nanos="offsetInNanos"
                                            )
                                        ),
            
                                        # the properties below are optional
                                        asset_id="assetId",
                                        entry_id="entryId",
                                        property_alias="propertyAlias",
                                        property_id="propertyId"
                                    ),
                                    iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                                        mqtt_topic="mqttTopic",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                                        function_arn="functionArn",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                                        timer_name="timerName",
            
                                        # the properties below are optional
                                        duration_expression="durationExpression",
                                        seconds=123
                                    ),
                                    set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                                        value="value",
                                        variable_name="variableName"
                                    ),
                                    sns=iotevents.CfnDetectorModel.SnsProperty(
                                        target_arn="targetArn",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    sqs=iotevents.CfnDetectorModel.SqsProperty(
                                        queue_url="queueUrl",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        use_base64=False
                                    )
                                )],
                                condition="condition"
                            )]
                        ),
                        on_input=iotevents.CfnDetectorModel.OnInputProperty(
                            events=[iotevents.CfnDetectorModel.EventProperty(
                                event_name="eventName",
            
                                # the properties below are optional
                                actions=[iotevents.CfnDetectorModel.ActionProperty(
                                    clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                                        hash_key_field="hashKeyField",
                                        hash_key_value="hashKeyValue",
                                        table_name="tableName",
            
                                        # the properties below are optional
                                        hash_key_type="hashKeyType",
                                        operation="operation",
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        payload_field="payloadField",
                                        range_key_field="rangeKeyField",
                                        range_key_type="rangeKeyType",
                                        range_key_value="rangeKeyValue"
                                    ),
                                    dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                                        table_name="tableName",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                                        delivery_stream_name="deliveryStreamName",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        separator="separator"
                                    ),
                                    iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                                        input_name="inputName",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                                        property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                            value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                                boolean_value="booleanValue",
                                                double_value="doubleValue",
                                                integer_value="integerValue",
                                                string_value="stringValue"
                                            ),
            
                                            # the properties below are optional
                                            quality="quality",
                                            timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                                time_in_seconds="timeInSeconds",
            
                                                # the properties below are optional
                                                offset_in_nanos="offsetInNanos"
                                            )
                                        ),
            
                                        # the properties below are optional
                                        asset_id="assetId",
                                        entry_id="entryId",
                                        property_alias="propertyAlias",
                                        property_id="propertyId"
                                    ),
                                    iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                                        mqtt_topic="mqttTopic",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                                        function_arn="functionArn",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                                        timer_name="timerName",
            
                                        # the properties below are optional
                                        duration_expression="durationExpression",
                                        seconds=123
                                    ),
                                    set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                                        value="value",
                                        variable_name="variableName"
                                    ),
                                    sns=iotevents.CfnDetectorModel.SnsProperty(
                                        target_arn="targetArn",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    sqs=iotevents.CfnDetectorModel.SqsProperty(
                                        queue_url="queueUrl",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        use_base64=False
                                    )
                                )],
                                condition="condition"
                            )],
                            transition_events=[iotevents.CfnDetectorModel.TransitionEventProperty(
                                condition="condition",
                                event_name="eventName",
                                next_state="nextState",
            
                                # the properties below are optional
                                actions=[iotevents.CfnDetectorModel.ActionProperty(
                                    clear_timer=iotevents.CfnDetectorModel.ClearTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    dynamo_db=iotevents.CfnDetectorModel.DynamoDBProperty(
                                        hash_key_field="hashKeyField",
                                        hash_key_value="hashKeyValue",
                                        table_name="tableName",
            
                                        # the properties below are optional
                                        hash_key_type="hashKeyType",
                                        operation="operation",
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        payload_field="payloadField",
                                        range_key_field="rangeKeyField",
                                        range_key_type="rangeKeyType",
                                        range_key_value="rangeKeyValue"
                                    ),
                                    dynamo_dBv2=iotevents.CfnDetectorModel.DynamoDBv2Property(
                                        table_name="tableName",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    firehose=iotevents.CfnDetectorModel.FirehoseProperty(
                                        delivery_stream_name="deliveryStreamName",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        separator="separator"
                                    ),
                                    iot_events=iotevents.CfnDetectorModel.IotEventsProperty(
                                        input_name="inputName",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    iot_site_wise=iotevents.CfnDetectorModel.IotSiteWiseProperty(
                                        property_value=iotevents.CfnDetectorModel.AssetPropertyValueProperty(
                                            value=iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                                                boolean_value="booleanValue",
                                                double_value="doubleValue",
                                                integer_value="integerValue",
                                                string_value="stringValue"
                                            ),
            
                                            # the properties below are optional
                                            quality="quality",
                                            timestamp=iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                                                time_in_seconds="timeInSeconds",
            
                                                # the properties below are optional
                                                offset_in_nanos="offsetInNanos"
                                            )
                                        ),
            
                                        # the properties below are optional
                                        asset_id="assetId",
                                        entry_id="entryId",
                                        property_alias="propertyAlias",
                                        property_id="propertyId"
                                    ),
                                    iot_topic_publish=iotevents.CfnDetectorModel.IotTopicPublishProperty(
                                        mqtt_topic="mqttTopic",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    lambda_=iotevents.CfnDetectorModel.LambdaProperty(
                                        function_arn="functionArn",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    reset_timer=iotevents.CfnDetectorModel.ResetTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    set_timer=iotevents.CfnDetectorModel.SetTimerProperty(
                                        timer_name="timerName",
            
                                        # the properties below are optional
                                        duration_expression="durationExpression",
                                        seconds=123
                                    ),
                                    set_variable=iotevents.CfnDetectorModel.SetVariableProperty(
                                        value="value",
                                        variable_name="variableName"
                                    ),
                                    sns=iotevents.CfnDetectorModel.SnsProperty(
                                        target_arn="targetArn",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    sqs=iotevents.CfnDetectorModel.SqsProperty(
                                        queue_url="queueUrl",
            
                                        # the properties below are optional
                                        payload=iotevents.CfnDetectorModel.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        use_base64=False
                                    )
                                )]
                            )]
                        )
                    )]
                ),
                role_arn="roleArn",
            
                # the properties below are optional
                detector_model_description="detectorModelDescription",
                detector_model_name="detectorModelName",
                evaluation_method="evaluationMethod",
                key="key",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8e30ba23b6ecb962d840a1a1201e65ae6f2c8f187561a7cf44d5fd8eade4512)
            check_type(argname="argument detector_model_definition", value=detector_model_definition, expected_type=type_hints["detector_model_definition"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument detector_model_description", value=detector_model_description, expected_type=type_hints["detector_model_description"])
            check_type(argname="argument detector_model_name", value=detector_model_name, expected_type=type_hints["detector_model_name"])
            check_type(argname="argument evaluation_method", value=evaluation_method, expected_type=type_hints["evaluation_method"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "detector_model_definition": detector_model_definition,
            "role_arn": role_arn,
        }
        if detector_model_description is not None:
            self._values["detector_model_description"] = detector_model_description
        if detector_model_name is not None:
            self._values["detector_model_name"] = detector_model_name
        if evaluation_method is not None:
            self._values["evaluation_method"] = evaluation_method
        if key is not None:
            self._values["key"] = key
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def detector_model_definition(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDetectorModel.DetectorModelDefinitionProperty]:
        '''Information that defines how a detector operates.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-detectormodeldefinition
        '''
        result = self._values.get("detector_model_definition")
        assert result is not None, "Required property 'detector_model_definition' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDetectorModel.DetectorModelDefinitionProperty], result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''The ARN of the role that grants permission to AWS IoT Events to perform its operations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-rolearn
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def detector_model_description(self) -> typing.Optional[builtins.str]:
        '''A brief description of the detector model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-detectormodeldescription
        '''
        result = self._values.get("detector_model_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def detector_model_name(self) -> typing.Optional[builtins.str]:
        '''The name of the detector model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-detectormodelname
        '''
        result = self._values.get("detector_model_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def evaluation_method(self) -> typing.Optional[builtins.str]:
        '''Information about the order in which events are evaluated and how actions are executed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-evaluationmethod
        '''
        result = self._values.get("evaluation_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''The value used to identify a detector instance.

        When a device or system sends input, a new detector instance with a unique key value is created. AWS IoT Events can continue to route input to its corresponding detector instance based on this identifying information.

        This parameter uses a JSON-path expression to select the attribute-value pair in the message payload that is used for identification. To route the message to the correct detector instance, the device must send a message payload that contains the same attribute-value.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-key
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDetectorModelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnInput(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iotevents.CfnInput",
):
    '''A CloudFormation ``AWS::IoTEvents::Input``.

    The AWS::IoTEvents::Input resource creates an input. To monitor your devices and processes, they must have a way to get telemetry data into AWS IoT Events . This is done by sending messages as *inputs* to AWS IoT Events . For more information, see `How to Use AWS IoT Events <https://docs.aws.amazon.com/iotevents/latest/developerguide/how-to-use-iotevents.html>`_ in the *AWS IoT Events Developer Guide* .

    :cloudformationResource: AWS::IoTEvents::Input
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iotevents as iotevents
        
        cfn_input = iotevents.CfnInput(self, "MyCfnInput",
            input_definition=iotevents.CfnInput.InputDefinitionProperty(
                attributes=[iotevents.CfnInput.AttributeProperty(
                    json_path="jsonPath"
                )]
            ),
        
            # the properties below are optional
            input_description="inputDescription",
            input_name="inputName",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        input_definition: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnInput.InputDefinitionProperty", typing.Dict[builtins.str, typing.Any]]],
        input_description: typing.Optional[builtins.str] = None,
        input_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTEvents::Input``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param input_definition: The definition of the input.
        :param input_description: A brief description of the input.
        :param input_name: The name of the input.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70f2fc6b7bbe4b1f65d243c1ff89e3fe75af14aff4158f940416fef97a826473)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnInputProps(
            input_definition=input_definition,
            input_description=input_description,
            input_name=input_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be7cd0224d183e31f465309b8c9de028c5b329736d5aae2ce176a96362f15d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0898d278a67b758da0fcd9827fa251ad877a952c928f8b5295c8c6581b8cd6ce)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="inputDefinition")
    def input_definition(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInput.InputDefinitionProperty"]:
        '''The definition of the input.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-inputdefinition
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInput.InputDefinitionProperty"], jsii.get(self, "inputDefinition"))

    @input_definition.setter
    def input_definition(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInput.InputDefinitionProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b0ec99a885e850e67e0a41ec8b9fc6520cb5c34018435cf6c68ce7278f4697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputDefinition", value)

    @builtins.property
    @jsii.member(jsii_name="inputDescription")
    def input_description(self) -> typing.Optional[builtins.str]:
        '''A brief description of the input.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-inputdescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputDescription"))

    @input_description.setter
    def input_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b50766aa7996de8fcd48f6adea2158fd4c0b50fa06126bc624cc9e2506e8b56e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputDescription", value)

    @builtins.property
    @jsii.member(jsii_name="inputName")
    def input_name(self) -> typing.Optional[builtins.str]:
        '''The name of the input.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-inputname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputName"))

    @input_name.setter
    def input_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a86f17a4a4eac005742143149464fee2507fcdea27264ecb7c977152aa37b2ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnInput.AttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"json_path": "jsonPath"},
    )
    class AttributeProperty:
        def __init__(self, *, json_path: builtins.str) -> None:
            '''The attributes from the JSON payload that are made available by the input.

            Inputs are derived from messages sent to the AWS IoT Events system using ``BatchPutMessage`` . Each such message contains a JSON payload. Those attributes (and their paired values) specified here are available for use in the ``condition`` expressions used by detectors.

            :param json_path: An expression that specifies an attribute-value pair in a JSON structure. Use this to specify an attribute from the JSON payload that is made available by the input. Inputs are derived from messages sent to AWS IoT Events ( ``BatchPutMessage`` ). Each such message contains a JSON payload. The attribute (and its paired value) specified here are available for use in the ``condition`` expressions used by detectors. Syntax: ``<field-name>.<field-name>...``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-input-attribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                attribute_property = iotevents.CfnInput.AttributeProperty(
                    json_path="jsonPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c50352623d6e3bb9331a191ceae3166443a9ee8b20e7d1efa1295ac2b597fe0f)
                check_type(argname="argument json_path", value=json_path, expected_type=type_hints["json_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "json_path": json_path,
            }

        @builtins.property
        def json_path(self) -> builtins.str:
            '''An expression that specifies an attribute-value pair in a JSON structure.

            Use this to specify an attribute from the JSON payload that is made available by the input. Inputs are derived from messages sent to AWS IoT Events ( ``BatchPutMessage`` ). Each such message contains a JSON payload. The attribute (and its paired value) specified here are available for use in the ``condition`` expressions used by detectors.

            Syntax: ``<field-name>.<field-name>...``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-input-attribute.html#cfn-iotevents-input-attribute-jsonpath
            '''
            result = self._values.get("json_path")
            assert result is not None, "Required property 'json_path' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iotevents.CfnInput.InputDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"attributes": "attributes"},
    )
    class InputDefinitionProperty:
        def __init__(
            self,
            *,
            attributes: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnInput.AttributeProperty", typing.Dict[builtins.str, typing.Any]]]]],
        ) -> None:
            '''The definition of the input.

            :param attributes: The attributes from the JSON payload that are made available by the input. Inputs are derived from messages sent to the AWS IoT Events system using ``BatchPutMessage`` . Each such message contains a JSON payload, and those attributes (and their paired values) specified here are available for use in the ``condition`` expressions used by detectors that monitor this input.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-input-inputdefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iotevents as iotevents
                
                input_definition_property = iotevents.CfnInput.InputDefinitionProperty(
                    attributes=[iotevents.CfnInput.AttributeProperty(
                        json_path="jsonPath"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c3e938ad00c56449b1b3cda4b57d66c9d89c38fc2b44fe72c5681e2b13f1f63)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "attributes": attributes,
            }

        @builtins.property
        def attributes(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInput.AttributeProperty"]]]:
            '''The attributes from the JSON payload that are made available by the input.

            Inputs are derived from messages sent to the AWS IoT Events system using ``BatchPutMessage`` . Each such message contains a JSON payload, and those attributes (and their paired values) specified here are available for use in the ``condition`` expressions used by detectors that monitor this input.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-input-inputdefinition.html#cfn-iotevents-input-inputdefinition-attributes
            '''
            result = self._values.get("attributes")
            assert result is not None, "Required property 'attributes' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInput.AttributeProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iotevents.CfnInputProps",
    jsii_struct_bases=[],
    name_mapping={
        "input_definition": "inputDefinition",
        "input_description": "inputDescription",
        "input_name": "inputName",
        "tags": "tags",
    },
)
class CfnInputProps:
    def __init__(
        self,
        *,
        input_definition: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInput.InputDefinitionProperty, typing.Dict[builtins.str, typing.Any]]],
        input_description: typing.Optional[builtins.str] = None,
        input_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnInput``.

        :param input_definition: The definition of the input.
        :param input_description: A brief description of the input.
        :param input_name: The name of the input.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iotevents as iotevents
            
            cfn_input_props = iotevents.CfnInputProps(
                input_definition=iotevents.CfnInput.InputDefinitionProperty(
                    attributes=[iotevents.CfnInput.AttributeProperty(
                        json_path="jsonPath"
                    )]
                ),
            
                # the properties below are optional
                input_description="inputDescription",
                input_name="inputName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6444f69e6a66f8069a5a2c1c9e2ecc3a008795bd121adb8032245553f620ff09)
            check_type(argname="argument input_definition", value=input_definition, expected_type=type_hints["input_definition"])
            check_type(argname="argument input_description", value=input_description, expected_type=type_hints["input_description"])
            check_type(argname="argument input_name", value=input_name, expected_type=type_hints["input_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "input_definition": input_definition,
        }
        if input_description is not None:
            self._values["input_description"] = input_description
        if input_name is not None:
            self._values["input_name"] = input_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def input_definition(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnInput.InputDefinitionProperty]:
        '''The definition of the input.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-inputdefinition
        '''
        result = self._values.get("input_definition")
        assert result is not None, "Required property 'input_definition' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnInput.InputDefinitionProperty], result)

    @builtins.property
    def input_description(self) -> typing.Optional[builtins.str]:
        '''A brief description of the input.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-inputdescription
        '''
        result = self._values.get("input_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_name(self) -> typing.Optional[builtins.str]:
        '''The name of the input.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-inputname
        '''
        result = self._values.get("input_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInputProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iotevents.DetectorModelProps",
    jsii_struct_bases=[],
    name_mapping={
        "initial_state": "initialState",
        "description": "description",
        "detector_key": "detectorKey",
        "detector_model_name": "detectorModelName",
        "evaluation_method": "evaluationMethod",
        "role": "role",
    },
)
class DetectorModelProps:
    def __init__(
        self,
        *,
        initial_state: "State",
        description: typing.Optional[builtins.str] = None,
        detector_key: typing.Optional[builtins.str] = None,
        detector_model_name: typing.Optional[builtins.str] = None,
        evaluation_method: typing.Optional["EventEvaluation"] = None,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''(experimental) Properties for defining an AWS IoT Events detector model.

        :param initial_state: (experimental) The state that is entered at the creation of each detector.
        :param description: (experimental) A brief description of the detector model. Default: none
        :param detector_key: (experimental) The value used to identify a detector instance. When a device or system sends input, a new detector instance with a unique key value is created. AWS IoT Events can continue to route input to its corresponding detector instance based on this identifying information. This parameter uses a JSON-path expression to select the attribute-value pair in the message payload that is used for identification. To route the message to the correct detector instance, the device must send a message payload that contains the same attribute-value. Default: - none (single detector instance will be created and all inputs will be routed to it)
        :param detector_model_name: (experimental) The name of the detector model. Default: - CloudFormation will generate a unique name of the detector model
        :param evaluation_method: (experimental) Information about the order in which events are evaluated and how actions are executed. When setting to SERIAL, variables are updated and event conditions are evaluated in the order that the events are defined. When setting to BATCH, variables within a state are updated and events within a state are performed only after all event conditions are evaluated. Default: EventEvaluation.BATCH
        :param role: (experimental) The role that grants permission to AWS IoT Events to perform its operations. Default: - a role will be created with default permissions

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_iotevents as iotevents
            import aws_cdk.aws_iotevents_actions as actions
            import aws_cdk.aws_lambda as lambda_
            
            # func: lambda.IFunction
            
            
            input = iotevents.Input(self, "MyInput",
                input_name="my_input",  # optional
                attribute_json_paths=["payload.deviceId", "payload.temperature"]
            )
            
            warm_state = iotevents.State(
                state_name="warm",
                on_enter=[iotevents.Event(
                    event_name="test-enter-event",
                    condition=iotevents.Expression.current_input(input),
                    actions=[actions.LambdaInvokeAction(func)]
                )],
                on_input=[iotevents.Event( # optional
                    event_name="test-input-event",
                    actions=[actions.LambdaInvokeAction(func)])],
                on_exit=[iotevents.Event( # optional
                    event_name="test-exit-event",
                    actions=[actions.LambdaInvokeAction(func)])]
            )
            cold_state = iotevents.State(
                state_name="cold"
            )
            
            # transit to coldState when temperature is less than 15
            warm_state.transition_to(cold_state,
                event_name="to_coldState",  # optional property, default by combining the names of the States
                when=iotevents.Expression.lt(
                    iotevents.Expression.input_attribute(input, "payload.temperature"),
                    iotevents.Expression.from_string("15")),
                executing=[actions.LambdaInvokeAction(func)]
            )
            # transit to warmState when temperature is greater than or equal to 15
            cold_state.transition_to(warm_state,
                when=iotevents.Expression.gte(
                    iotevents.Expression.input_attribute(input, "payload.temperature"),
                    iotevents.Expression.from_string("15"))
            )
            
            iotevents.DetectorModel(self, "MyDetectorModel",
                detector_model_name="test-detector-model",  # optional
                description="test-detector-model-description",  # optional property, default is none
                evaluation_method=iotevents.EventEvaluation.SERIAL,  # optional property, default is iotevents.EventEvaluation.BATCH
                detector_key="payload.deviceId",  # optional property, default is none and single detector instance will be created and all inputs will be routed to it
                initial_state=warm_state
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aebf79fa1acd81efa906913f1ca96fcc710f16e945a27c388d9af35ff61f965a)
            check_type(argname="argument initial_state", value=initial_state, expected_type=type_hints["initial_state"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument detector_key", value=detector_key, expected_type=type_hints["detector_key"])
            check_type(argname="argument detector_model_name", value=detector_model_name, expected_type=type_hints["detector_model_name"])
            check_type(argname="argument evaluation_method", value=evaluation_method, expected_type=type_hints["evaluation_method"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "initial_state": initial_state,
        }
        if description is not None:
            self._values["description"] = description
        if detector_key is not None:
            self._values["detector_key"] = detector_key
        if detector_model_name is not None:
            self._values["detector_model_name"] = detector_model_name
        if evaluation_method is not None:
            self._values["evaluation_method"] = evaluation_method
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def initial_state(self) -> "State":
        '''(experimental) The state that is entered at the creation of each detector.

        :stability: experimental
        '''
        result = self._values.get("initial_state")
        assert result is not None, "Required property 'initial_state' is missing"
        return typing.cast("State", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A brief description of the detector model.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def detector_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) The value used to identify a detector instance.

        When a device or system sends input, a new
        detector instance with a unique key value is created. AWS IoT Events can continue to route
        input to its corresponding detector instance based on this identifying information.

        This parameter uses a JSON-path expression to select the attribute-value pair in the message
        payload that is used for identification. To route the message to the correct detector instance,
        the device must send a message payload that contains the same attribute-value.

        :default: - none (single detector instance will be created and all inputs will be routed to it)

        :stability: experimental
        '''
        result = self._values.get("detector_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def detector_model_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the detector model.

        :default: - CloudFormation will generate a unique name of the detector model

        :stability: experimental
        '''
        result = self._values.get("detector_model_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def evaluation_method(self) -> typing.Optional["EventEvaluation"]:
        '''(experimental) Information about the order in which events are evaluated and how actions are executed.

        When setting to SERIAL, variables are updated and event conditions are evaluated in the order
        that the events are defined.
        When setting to BATCH, variables within a state are updated and events within a state are
        performed only after all event conditions are evaluated.

        :default: EventEvaluation.BATCH

        :stability: experimental
        '''
        result = self._values.get("evaluation_method")
        return typing.cast(typing.Optional["EventEvaluation"], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''(experimental) The role that grants permission to AWS IoT Events to perform its operations.

        :default: - a role will be created with default permissions

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DetectorModelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iotevents.Event",
    jsii_struct_bases=[],
    name_mapping={
        "event_name": "eventName",
        "actions": "actions",
        "condition": "condition",
    },
)
class Event:
    def __init__(
        self,
        *,
        event_name: builtins.str,
        actions: typing.Optional[typing.Sequence["IAction"]] = None,
        condition: typing.Optional["Expression"] = None,
    ) -> None:
        '''(experimental) Specifies the actions to be performed when the condition evaluates to ``true``.

        :param event_name: (experimental) The name of the event.
        :param actions: (experimental) The actions to be performed. Default: - no actions will be performed
        :param condition: (experimental) The Boolean expression that, when ``true``, causes the actions to be performed. Default: - none (the actions are always executed)

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iotevents as iotevents
            
            # action: iotevents.IAction
            # expression: iotevents.Expression
            
            event = iotevents.Event(
                event_name="eventName",
            
                # the properties below are optional
                actions=[action],
                condition=expression
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd0180524e458ab33b60171fbad3530ccee1c10edfdbf0481caf1a82c210486f)
            check_type(argname="argument event_name", value=event_name, expected_type=type_hints["event_name"])
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_name": event_name,
        }
        if actions is not None:
            self._values["actions"] = actions
        if condition is not None:
            self._values["condition"] = condition

    @builtins.property
    def event_name(self) -> builtins.str:
        '''(experimental) The name of the event.

        :stability: experimental
        '''
        result = self._values.get("event_name")
        assert result is not None, "Required property 'event_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def actions(self) -> typing.Optional[typing.List["IAction"]]:
        '''(experimental) The actions to be performed.

        :default: - no actions will be performed

        :stability: experimental
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List["IAction"]], result)

    @builtins.property
    def condition(self) -> typing.Optional["Expression"]:
        '''(experimental) The Boolean expression that, when ``true``, causes the actions to be performed.

        :default: - none (the actions are always executed)

        :stability: experimental
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional["Expression"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Event(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-iotevents.EventEvaluation")
class EventEvaluation(enum.Enum):
    '''(experimental) Information about the order in which events are evaluated and how actions are executed.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_iotevents as iotevents
        import aws_cdk.aws_iotevents_actions as actions
        import aws_cdk.aws_lambda as lambda_
        
        # func: lambda.IFunction
        
        
        input = iotevents.Input(self, "MyInput",
            input_name="my_input",  # optional
            attribute_json_paths=["payload.deviceId", "payload.temperature"]
        )
        
        warm_state = iotevents.State(
            state_name="warm",
            on_enter=[iotevents.Event(
                event_name="test-enter-event",
                condition=iotevents.Expression.current_input(input),
                actions=[actions.LambdaInvokeAction(func)]
            )],
            on_input=[iotevents.Event( # optional
                event_name="test-input-event",
                actions=[actions.LambdaInvokeAction(func)])],
            on_exit=[iotevents.Event( # optional
                event_name="test-exit-event",
                actions=[actions.LambdaInvokeAction(func)])]
        )
        cold_state = iotevents.State(
            state_name="cold"
        )
        
        # transit to coldState when temperature is less than 15
        warm_state.transition_to(cold_state,
            event_name="to_coldState",  # optional property, default by combining the names of the States
            when=iotevents.Expression.lt(
                iotevents.Expression.input_attribute(input, "payload.temperature"),
                iotevents.Expression.from_string("15")),
            executing=[actions.LambdaInvokeAction(func)]
        )
        # transit to warmState when temperature is greater than or equal to 15
        cold_state.transition_to(warm_state,
            when=iotevents.Expression.gte(
                iotevents.Expression.input_attribute(input, "payload.temperature"),
                iotevents.Expression.from_string("15"))
        )
        
        iotevents.DetectorModel(self, "MyDetectorModel",
            detector_model_name="test-detector-model",  # optional
            description="test-detector-model-description",  # optional property, default is none
            evaluation_method=iotevents.EventEvaluation.SERIAL,  # optional property, default is iotevents.EventEvaluation.BATCH
            detector_key="payload.deviceId",  # optional property, default is none and single detector instance will be created and all inputs will be routed to it
            initial_state=warm_state
        )
    '''

    BATCH = "BATCH"
    '''(experimental) When setting to BATCH, variables within a state are updated and events within a state are performed only after all event conditions are evaluated.

    :stability: experimental
    '''
    SERIAL = "SERIAL"
    '''(experimental) When setting to SERIAL, variables are updated and event conditions are evaluated in the order that the events are defined.

    :stability: experimental
    '''


class Expression(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-iotevents.Expression",
):
    '''(experimental) Expression for events in Detector Model state.

    :see: https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Example automatically generated from non-compiling source. May contain errors.
        import aws_cdk.aws_iotevents as iotevents
        import aws_cdk.aws_iotevents_actions as actions
        
        # input: iotevents.IInput
        
        state = iotevents.State(
            state_name="MyState",
            on_enter=[iotevents.Event(
                event_name="test-event",
                condition=iotevents.Expression.current_input(input),
                actions=[actions, [
                    actions.SetVariableAction("MyVariable",
                        iotevents.Expression.input_attribute(input, "payload.temperature"))
                ]
                ]
            )]
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="and")
    @builtins.classmethod
    def and_(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the AND operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2adcde9e1aebb67e309495c4f283992f6ccabb7e286dcabe4f22b090bcb8bc5)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "and", [left, right]))

    @jsii.member(jsii_name="currentInput")
    @builtins.classmethod
    def current_input(cls, input: "IInput") -> "Expression":
        '''(experimental) Create a expression for function ``currentInput()``.

        It is evaluated to true if the specified input message was received.

        :param input: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4d6a7ee8eaf2af8cc2ce00f5f45a096d449737ef5febf0eb43c4de8553e9887)
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
        return typing.cast("Expression", jsii.sinvoke(cls, "currentInput", [input]))

    @jsii.member(jsii_name="eq")
    @builtins.classmethod
    def eq(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the Equal operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e788239ae3d00dc07f530a4d7550e25061eb786f9887575c410982eba92ba23)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "eq", [left, right]))

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(cls, value: builtins.str) -> "Expression":
        '''(experimental) Create a expression from the given string.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2fd1fc181e89b3f9bc2752a8edfe83152cb302a735eb499b99dac4bac5be833)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("Expression", jsii.sinvoke(cls, "fromString", [value]))

    @jsii.member(jsii_name="gt")
    @builtins.classmethod
    def gt(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the Greater Than operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c3465200c7a77486f40a69a0c1764c941011e8a6729fcc6399137960de5a0f)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "gt", [left, right]))

    @jsii.member(jsii_name="gte")
    @builtins.classmethod
    def gte(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the Greater Than Or Equal operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1a73c08d7ba9b2a565b147391bb1877a2a30a3022387df82fb210cefea9079f)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "gte", [left, right]))

    @jsii.member(jsii_name="inputAttribute")
    @builtins.classmethod
    def input_attribute(cls, input: "IInput", path: builtins.str) -> "Expression":
        '''(experimental) Create a expression for get an input attribute as ``$input.TemperatureInput.temperatures[2]``.

        :param input: -
        :param path: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4bec8a9359e40c38e34ef4a1fc146e79316e9ecfde950f3ce2bd2919f64c361)
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("Expression", jsii.sinvoke(cls, "inputAttribute", [input, path]))

    @jsii.member(jsii_name="lt")
    @builtins.classmethod
    def lt(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the Less Than operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81973e05d8a74cf3bba291907eb803f6572fce4e3e65e48b39520a9be752e805)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "lt", [left, right]))

    @jsii.member(jsii_name="lte")
    @builtins.classmethod
    def lte(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the Less Than Or Equal operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__380acac5d46e88d6de66fa90bc47875d578d6cc3f7f88918512f8f802112e5ac)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "lte", [left, right]))

    @jsii.member(jsii_name="neq")
    @builtins.classmethod
    def neq(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the Not Equal operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aea6f40d0b21c36128d79b156f8890a1a79f4939257981ebbadd73b3da35651c)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "neq", [left, right]))

    @jsii.member(jsii_name="or")
    @builtins.classmethod
    def or_(cls, left: "Expression", right: "Expression") -> "Expression":
        '''(experimental) Create a expression for the OR operator.

        :param left: -
        :param right: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a76ed3f4df1e48a1164ff439b9c922b766aefb3f57e223f5a398fe3b491a9bd9)
            check_type(argname="argument left", value=left, expected_type=type_hints["left"])
            check_type(argname="argument right", value=right, expected_type=type_hints["right"])
        return typing.cast("Expression", jsii.sinvoke(cls, "or", [left, right]))

    @jsii.member(jsii_name="evaluate")
    @abc.abstractmethod
    def evaluate(
        self,
        parent_priority: typing.Optional[jsii.Number] = None,
    ) -> builtins.str:
        '''(experimental) This is called to evaluate the expression.

        :param parent_priority: priority of the parent of this expression, used for determining whether or not to add parenthesis around the expression. This is intended to be set according to MDN rules, see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Operator_Precedence#table for details

        :stability: experimental
        '''
        ...


class _ExpressionProxy(Expression):
    @jsii.member(jsii_name="evaluate")
    def evaluate(
        self,
        parent_priority: typing.Optional[jsii.Number] = None,
    ) -> builtins.str:
        '''(experimental) This is called to evaluate the expression.

        :param parent_priority: priority of the parent of this expression, used for determining whether or not to add parenthesis around the expression. This is intended to be set according to MDN rules, see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Operator_Precedence#table for details

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d24971e1624fc3946b3b95ccb83a848ead0f9d5d5b6b4ca5257af445b89ab730)
            check_type(argname="argument parent_priority", value=parent_priority, expected_type=type_hints["parent_priority"])
        return typing.cast(builtins.str, jsii.invoke(self, "evaluate", [parent_priority]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Expression).__jsii_proxy_class__ = lambda : _ExpressionProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iotevents.IAction")
class IAction(typing_extensions.Protocol):
    '''(experimental) An abstract action for DetectorModel.

    :stability: experimental
    '''

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        role: _aws_cdk_aws_iam_940a1ce0.IRole,
    ) -> ActionConfig:
        '''(experimental) Returns the AWS IoT Events action specification.

        :param scope: -
        :param role: (experimental) The IAM role assumed by IoT Events to perform the action.

        :stability: experimental
        '''
        ...


class _IActionProxy:
    '''(experimental) An abstract action for DetectorModel.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iotevents.IAction"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        role: _aws_cdk_aws_iam_940a1ce0.IRole,
    ) -> ActionConfig:
        '''(experimental) Returns the AWS IoT Events action specification.

        :param scope: -
        :param role: (experimental) The IAM role assumed by IoT Events to perform the action.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__959e6c5f02243a49a319d90bf3843c8e380e497782132de964e8f331b4cabed1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        options = ActionBindOptions(role=role)

        return typing.cast(ActionConfig, jsii.invoke(self, "bind", [scope, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAction).__jsii_proxy_class__ = lambda : _IActionProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iotevents.IDetectorModel")
class IDetectorModel(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''(experimental) Represents an AWS IoT Events detector model.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="detectorModelName")
    def detector_model_name(self) -> builtins.str:
        '''(experimental) The name of the detector model.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IDetectorModelProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''(experimental) Represents an AWS IoT Events detector model.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iotevents.IDetectorModel"

    @builtins.property
    @jsii.member(jsii_name="detectorModelName")
    def detector_model_name(self) -> builtins.str:
        '''(experimental) The name of the detector model.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "detectorModelName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDetectorModel).__jsii_proxy_class__ = lambda : _IDetectorModelProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iotevents.IInput")
class IInput(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''(experimental) Represents an AWS IoT Events input.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="inputArn")
    def input_arn(self) -> builtins.str:
        '''(experimental) The ARN of the input.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="inputName")
    def input_name(self) -> builtins.str:
        '''(experimental) The name of the input.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''(experimental) Grant the indicated permissions on this input to the given IAM principal (Role/Group/User).

        :param grantee: the principal.
        :param actions: the set of actions to allow (i.e. "iotevents:BatchPutMessage").

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''(experimental) Grant write permissions on this input and its contents to an IAM principal (Role/Group/User).

        :param grantee: the principal.

        :stability: experimental
        '''
        ...


class _IInputProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''(experimental) Represents an AWS IoT Events input.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iotevents.IInput"

    @builtins.property
    @jsii.member(jsii_name="inputArn")
    def input_arn(self) -> builtins.str:
        '''(experimental) The ARN of the input.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "inputArn"))

    @builtins.property
    @jsii.member(jsii_name="inputName")
    def input_name(self) -> builtins.str:
        '''(experimental) The name of the input.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "inputName"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''(experimental) Grant the indicated permissions on this input to the given IAM principal (Role/Group/User).

        :param grantee: the principal.
        :param actions: the set of actions to allow (i.e. "iotevents:BatchPutMessage").

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c52069038289e50f95bd000409f6f17da5d7907c98d4f9d3259f864e530326ce)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''(experimental) Grant write permissions on this input and its contents to an IAM principal (Role/Group/User).

        :param grantee: the principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce1acfc0d062982b612615a9c24decdb9823156576d760781192cc0025e404d8)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantWrite", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IInput).__jsii_proxy_class__ = lambda : _IInputProxy


@jsii.implements(IInput)
class Input(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iotevents.Input",
):
    '''(experimental) Defines an AWS IoT Events input in this stack.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_iotevents as iotevents
        import aws_cdk.aws_iotevents_actions as actions
        import aws_cdk.aws_lambda as lambda_
        
        # func: lambda.IFunction
        
        
        input = iotevents.Input(self, "MyInput",
            input_name="my_input",  # optional
            attribute_json_paths=["payload.deviceId", "payload.temperature"]
        )
        
        warm_state = iotevents.State(
            state_name="warm",
            on_enter=[iotevents.Event(
                event_name="test-enter-event",
                condition=iotevents.Expression.current_input(input),
                actions=[actions.LambdaInvokeAction(func)]
            )],
            on_input=[iotevents.Event( # optional
                event_name="test-input-event",
                actions=[actions.LambdaInvokeAction(func)])],
            on_exit=[iotevents.Event( # optional
                event_name="test-exit-event",
                actions=[actions.LambdaInvokeAction(func)])]
        )
        cold_state = iotevents.State(
            state_name="cold"
        )
        
        # transit to coldState when temperature is less than 15
        warm_state.transition_to(cold_state,
            event_name="to_coldState",  # optional property, default by combining the names of the States
            when=iotevents.Expression.lt(
                iotevents.Expression.input_attribute(input, "payload.temperature"),
                iotevents.Expression.from_string("15")),
            executing=[actions.LambdaInvokeAction(func)]
        )
        # transit to warmState when temperature is greater than or equal to 15
        cold_state.transition_to(warm_state,
            when=iotevents.Expression.gte(
                iotevents.Expression.input_attribute(input, "payload.temperature"),
                iotevents.Expression.from_string("15"))
        )
        
        iotevents.DetectorModel(self, "MyDetectorModel",
            detector_model_name="test-detector-model",  # optional
            description="test-detector-model-description",  # optional property, default is none
            evaluation_method=iotevents.EventEvaluation.SERIAL,  # optional property, default is iotevents.EventEvaluation.BATCH
            detector_key="payload.deviceId",  # optional property, default is none and single detector instance will be created and all inputs will be routed to it
            initial_state=warm_state
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        attribute_json_paths: typing.Sequence[builtins.str],
        input_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param attribute_json_paths: (experimental) An expression that specifies an attribute-value pair in a JSON structure. Use this to specify an attribute from the JSON payload that is made available by the input. Inputs are derived from messages sent to AWS IoT Events (BatchPutMessage). Each such message contains a JSON payload. The attribute (and its paired value) specified here are available for use in the condition expressions used by detectors.
        :param input_name: (experimental) The name of the input. Default: - CloudFormation will generate a unique name of the input

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a1c9709d4b03fe647971258a1dff1507db076ca85d7e1f62d8a23088c287b84)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = InputProps(
            attribute_json_paths=attribute_json_paths, input_name=input_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromInputName")
    @builtins.classmethod
    def from_input_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        input_name: builtins.str,
    ) -> IInput:
        '''(experimental) Import an existing input.

        :param scope: -
        :param id: -
        :param input_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5b7aa94617b1c8e737a91c26218670dc64ccf90bface1c544bbdb5a77245aa1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument input_name", value=input_name, expected_type=type_hints["input_name"])
        return typing.cast(IInput, jsii.sinvoke(cls, "fromInputName", [scope, id, input_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''(experimental) Grant the indicated permissions on this input to the given IAM principal (Role/Group/User).

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da87756126d61843b6c456f0dbc4fdfc488feb35744c4c18f99ccdd59240e9d8)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''(experimental) Grant write permissions on this input and its contents to an IAM principal (Role/Group/User).

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc61510051b3f2625a09b308b69a0d3f8f1f46e1224c41d297af9e9087b485fc)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantWrite", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="inputArn")
    def input_arn(self) -> builtins.str:
        '''(experimental) The ARN of the input.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "inputArn"))

    @builtins.property
    @jsii.member(jsii_name="inputName")
    def input_name(self) -> builtins.str:
        '''(experimental) The name of the input.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "inputName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iotevents.InputProps",
    jsii_struct_bases=[],
    name_mapping={
        "attribute_json_paths": "attributeJsonPaths",
        "input_name": "inputName",
    },
)
class InputProps:
    def __init__(
        self,
        *,
        attribute_json_paths: typing.Sequence[builtins.str],
        input_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for defining an AWS IoT Events input.

        :param attribute_json_paths: (experimental) An expression that specifies an attribute-value pair in a JSON structure. Use this to specify an attribute from the JSON payload that is made available by the input. Inputs are derived from messages sent to AWS IoT Events (BatchPutMessage). Each such message contains a JSON payload. The attribute (and its paired value) specified here are available for use in the condition expressions used by detectors.
        :param input_name: (experimental) The name of the input. Default: - CloudFormation will generate a unique name of the input

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_iotevents as iotevents
            import aws_cdk.aws_iotevents_actions as actions
            import aws_cdk.aws_lambda as lambda_
            
            # func: lambda.IFunction
            
            
            input = iotevents.Input(self, "MyInput",
                input_name="my_input",  # optional
                attribute_json_paths=["payload.deviceId", "payload.temperature"]
            )
            
            warm_state = iotevents.State(
                state_name="warm",
                on_enter=[iotevents.Event(
                    event_name="test-enter-event",
                    condition=iotevents.Expression.current_input(input),
                    actions=[actions.LambdaInvokeAction(func)]
                )],
                on_input=[iotevents.Event( # optional
                    event_name="test-input-event",
                    actions=[actions.LambdaInvokeAction(func)])],
                on_exit=[iotevents.Event( # optional
                    event_name="test-exit-event",
                    actions=[actions.LambdaInvokeAction(func)])]
            )
            cold_state = iotevents.State(
                state_name="cold"
            )
            
            # transit to coldState when temperature is less than 15
            warm_state.transition_to(cold_state,
                event_name="to_coldState",  # optional property, default by combining the names of the States
                when=iotevents.Expression.lt(
                    iotevents.Expression.input_attribute(input, "payload.temperature"),
                    iotevents.Expression.from_string("15")),
                executing=[actions.LambdaInvokeAction(func)]
            )
            # transit to warmState when temperature is greater than or equal to 15
            cold_state.transition_to(warm_state,
                when=iotevents.Expression.gte(
                    iotevents.Expression.input_attribute(input, "payload.temperature"),
                    iotevents.Expression.from_string("15"))
            )
            
            iotevents.DetectorModel(self, "MyDetectorModel",
                detector_model_name="test-detector-model",  # optional
                description="test-detector-model-description",  # optional property, default is none
                evaluation_method=iotevents.EventEvaluation.SERIAL,  # optional property, default is iotevents.EventEvaluation.BATCH
                detector_key="payload.deviceId",  # optional property, default is none and single detector instance will be created and all inputs will be routed to it
                initial_state=warm_state
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b774f8902bf22c53aa4307c5d30820bdb0c75c7502a06096f34802b338980af5)
            check_type(argname="argument attribute_json_paths", value=attribute_json_paths, expected_type=type_hints["attribute_json_paths"])
            check_type(argname="argument input_name", value=input_name, expected_type=type_hints["input_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attribute_json_paths": attribute_json_paths,
        }
        if input_name is not None:
            self._values["input_name"] = input_name

    @builtins.property
    def attribute_json_paths(self) -> typing.List[builtins.str]:
        '''(experimental) An expression that specifies an attribute-value pair in a JSON structure.

        Use this to specify an attribute from the JSON payload that is made available
        by the input. Inputs are derived from messages sent to AWS IoT Events (BatchPutMessage).
        Each such message contains a JSON payload. The attribute (and its paired value)
        specified here are available for use in the condition expressions used by detectors.

        :stability: experimental
        '''
        result = self._values.get("attribute_json_paths")
        assert result is not None, "Required property 'attribute_json_paths' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def input_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the input.

        :default: - CloudFormation will generate a unique name of the input

        :stability: experimental
        '''
        result = self._values.get("input_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InputProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class State(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iotevents.State"):
    '''(experimental) Defines a state of a detector.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Example automatically generated from non-compiling source. May contain errors.
        import aws_cdk.aws_iotevents as iotevents
        import aws_cdk.aws_iotevents_actions as actions
        
        # input: iotevents.IInput
        
        state = iotevents.State(
            state_name="MyState",
            on_enter=[iotevents.Event(
                event_name="test-event",
                condition=iotevents.Expression.current_input(input),
                actions=[actions, [
                    actions.SetVariableAction("MyVariable",
                        iotevents.Expression.input_attribute(input, "payload.temperature"))
                ]
                ]
            )]
        )
    '''

    def __init__(
        self,
        *,
        state_name: builtins.str,
        on_enter: typing.Optional[typing.Sequence[typing.Union[Event, typing.Dict[builtins.str, typing.Any]]]] = None,
        on_exit: typing.Optional[typing.Sequence[typing.Union[Event, typing.Dict[builtins.str, typing.Any]]]] = None,
        on_input: typing.Optional[typing.Sequence[typing.Union[Event, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param state_name: (experimental) The name of the state.
        :param on_enter: (experimental) Specifies the events on enter. The conditions of the events will be evaluated when entering this state. If the condition of the event evaluates to ``true``, the actions of the event will be executed. Default: - no events will trigger on entering this state
        :param on_exit: (experimental) Specifies the events on exit. The conditions of the events are evaluated when an exiting this state. If the condition evaluates to ``true``, the actions of the event will be executed. Default: - no events will trigger on exiting this state
        :param on_input: (experimental) Specifies the events on input. The conditions of the events will be evaluated when any input is received. If the condition of the event evaluates to ``true``, the actions of the event will be executed. Default: - no events will trigger on input in this state

        :stability: experimental
        '''
        props = StateProps(
            state_name=state_name,
            on_enter=on_enter,
            on_exit=on_exit,
            on_input=on_input,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="transitionTo")
    def transition_to(
        self,
        target_state: "State",
        *,
        when: Expression,
        event_name: typing.Optional[builtins.str] = None,
        executing: typing.Optional[typing.Sequence[IAction]] = None,
    ) -> None:
        '''(experimental) Add a transition event to the state.

        The transition event will be triggered if condition is evaluated to ``true``.

        :param target_state: the state that will be transit to when the event triggered.
        :param when: (experimental) The condition that is used to determine to cause the state transition and the actions. When this was evaluated to ``true``, the state transition and the actions are triggered.
        :param event_name: (experimental) The name of the event. Default: string combining the names of the States as ``${originStateName}_to_${targetStateName}``
        :param executing: (experimental) The actions to be performed with the transition. Default: - no actions will be performed

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c2c4af4f894c4c9f5b579fc93e0c943f72ee49a862e3e605002c42a8eae323)
            check_type(argname="argument target_state", value=target_state, expected_type=type_hints["target_state"])
        options = TransitionOptions(
            when=when, event_name=event_name, executing=executing
        )

        return typing.cast(None, jsii.invoke(self, "transitionTo", [target_state, options]))

    @builtins.property
    @jsii.member(jsii_name="stateName")
    def state_name(self) -> builtins.str:
        '''(experimental) The name of the state.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "stateName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iotevents.StateProps",
    jsii_struct_bases=[],
    name_mapping={
        "state_name": "stateName",
        "on_enter": "onEnter",
        "on_exit": "onExit",
        "on_input": "onInput",
    },
)
class StateProps:
    def __init__(
        self,
        *,
        state_name: builtins.str,
        on_enter: typing.Optional[typing.Sequence[typing.Union[Event, typing.Dict[builtins.str, typing.Any]]]] = None,
        on_exit: typing.Optional[typing.Sequence[typing.Union[Event, typing.Dict[builtins.str, typing.Any]]]] = None,
        on_input: typing.Optional[typing.Sequence[typing.Union[Event, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Properties for defining a state of a detector.

        :param state_name: (experimental) The name of the state.
        :param on_enter: (experimental) Specifies the events on enter. The conditions of the events will be evaluated when entering this state. If the condition of the event evaluates to ``true``, the actions of the event will be executed. Default: - no events will trigger on entering this state
        :param on_exit: (experimental) Specifies the events on exit. The conditions of the events are evaluated when an exiting this state. If the condition evaluates to ``true``, the actions of the event will be executed. Default: - no events will trigger on exiting this state
        :param on_input: (experimental) Specifies the events on input. The conditions of the events will be evaluated when any input is received. If the condition of the event evaluates to ``true``, the actions of the event will be executed. Default: - no events will trigger on input in this state

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # Example automatically generated from non-compiling source. May contain errors.
            import aws_cdk.aws_iotevents as iotevents
            import aws_cdk.aws_iotevents_actions as actions
            
            # input: iotevents.IInput
            
            state = iotevents.State(
                state_name="MyState",
                on_enter=[iotevents.Event(
                    event_name="test-event",
                    condition=iotevents.Expression.current_input(input),
                    actions=[actions, [
                        actions.SetVariableAction("MyVariable",
                            iotevents.Expression.input_attribute(input, "payload.temperature"))
                    ]
                    ]
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a97c297f459a4463d79fda8f2b6ad0f5a33fcc278b799fe34f674e2205dedca)
            check_type(argname="argument state_name", value=state_name, expected_type=type_hints["state_name"])
            check_type(argname="argument on_enter", value=on_enter, expected_type=type_hints["on_enter"])
            check_type(argname="argument on_exit", value=on_exit, expected_type=type_hints["on_exit"])
            check_type(argname="argument on_input", value=on_input, expected_type=type_hints["on_input"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "state_name": state_name,
        }
        if on_enter is not None:
            self._values["on_enter"] = on_enter
        if on_exit is not None:
            self._values["on_exit"] = on_exit
        if on_input is not None:
            self._values["on_input"] = on_input

    @builtins.property
    def state_name(self) -> builtins.str:
        '''(experimental) The name of the state.

        :stability: experimental
        '''
        result = self._values.get("state_name")
        assert result is not None, "Required property 'state_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def on_enter(self) -> typing.Optional[typing.List[Event]]:
        '''(experimental) Specifies the events on enter.

        The conditions of the events will be evaluated when entering this state.
        If the condition of the event evaluates to ``true``, the actions of the event will be executed.

        :default: - no events will trigger on entering this state

        :stability: experimental
        '''
        result = self._values.get("on_enter")
        return typing.cast(typing.Optional[typing.List[Event]], result)

    @builtins.property
    def on_exit(self) -> typing.Optional[typing.List[Event]]:
        '''(experimental) Specifies the events on exit.

        The conditions of the events are evaluated when an exiting this state.
        If the condition evaluates to ``true``, the actions of the event will be executed.

        :default: - no events will trigger on exiting this state

        :stability: experimental
        '''
        result = self._values.get("on_exit")
        return typing.cast(typing.Optional[typing.List[Event]], result)

    @builtins.property
    def on_input(self) -> typing.Optional[typing.List[Event]]:
        '''(experimental) Specifies the events on input.

        The conditions of the events will be evaluated when any input is received.
        If the condition of the event evaluates to ``true``, the actions of the event will be executed.

        :default: - no events will trigger on input in this state

        :stability: experimental
        '''
        result = self._values.get("on_input")
        return typing.cast(typing.Optional[typing.List[Event]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iotevents.TransitionOptions",
    jsii_struct_bases=[],
    name_mapping={"when": "when", "event_name": "eventName", "executing": "executing"},
)
class TransitionOptions:
    def __init__(
        self,
        *,
        when: Expression,
        event_name: typing.Optional[builtins.str] = None,
        executing: typing.Optional[typing.Sequence[IAction]] = None,
    ) -> None:
        '''(experimental) Properties for options of state transition.

        :param when: (experimental) The condition that is used to determine to cause the state transition and the actions. When this was evaluated to ``true``, the state transition and the actions are triggered.
        :param event_name: (experimental) The name of the event. Default: string combining the names of the States as ``${originStateName}_to_${targetStateName}``
        :param executing: (experimental) The actions to be performed with the transition. Default: - no actions will be performed

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_iotevents as iotevents
            import aws_cdk.aws_iotevents_actions as actions
            import aws_cdk.aws_lambda as lambda_
            
            # func: lambda.IFunction
            
            
            input = iotevents.Input(self, "MyInput",
                input_name="my_input",  # optional
                attribute_json_paths=["payload.deviceId", "payload.temperature"]
            )
            
            warm_state = iotevents.State(
                state_name="warm",
                on_enter=[iotevents.Event(
                    event_name="test-enter-event",
                    condition=iotevents.Expression.current_input(input),
                    actions=[actions.LambdaInvokeAction(func)]
                )],
                on_input=[iotevents.Event( # optional
                    event_name="test-input-event",
                    actions=[actions.LambdaInvokeAction(func)])],
                on_exit=[iotevents.Event( # optional
                    event_name="test-exit-event",
                    actions=[actions.LambdaInvokeAction(func)])]
            )
            cold_state = iotevents.State(
                state_name="cold"
            )
            
            # transit to coldState when temperature is less than 15
            warm_state.transition_to(cold_state,
                event_name="to_coldState",  # optional property, default by combining the names of the States
                when=iotevents.Expression.lt(
                    iotevents.Expression.input_attribute(input, "payload.temperature"),
                    iotevents.Expression.from_string("15")),
                executing=[actions.LambdaInvokeAction(func)]
            )
            # transit to warmState when temperature is greater than or equal to 15
            cold_state.transition_to(warm_state,
                when=iotevents.Expression.gte(
                    iotevents.Expression.input_attribute(input, "payload.temperature"),
                    iotevents.Expression.from_string("15"))
            )
            
            iotevents.DetectorModel(self, "MyDetectorModel",
                detector_model_name="test-detector-model",  # optional
                description="test-detector-model-description",  # optional property, default is none
                evaluation_method=iotevents.EventEvaluation.SERIAL,  # optional property, default is iotevents.EventEvaluation.BATCH
                detector_key="payload.deviceId",  # optional property, default is none and single detector instance will be created and all inputs will be routed to it
                initial_state=warm_state
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bacaa8d88dbb67842d4a6ecc3d8d12890fc663d23331e415273a40dcf6d11c79)
            check_type(argname="argument when", value=when, expected_type=type_hints["when"])
            check_type(argname="argument event_name", value=event_name, expected_type=type_hints["event_name"])
            check_type(argname="argument executing", value=executing, expected_type=type_hints["executing"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "when": when,
        }
        if event_name is not None:
            self._values["event_name"] = event_name
        if executing is not None:
            self._values["executing"] = executing

    @builtins.property
    def when(self) -> Expression:
        '''(experimental) The condition that is used to determine to cause the state transition and the actions.

        When this was evaluated to ``true``, the state transition and the actions are triggered.

        :stability: experimental
        '''
        result = self._values.get("when")
        assert result is not None, "Required property 'when' is missing"
        return typing.cast(Expression, result)

    @builtins.property
    def event_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the event.

        :default: string combining the names of the States as ``${originStateName}_to_${targetStateName}``

        :stability: experimental
        '''
        result = self._values.get("event_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def executing(self) -> typing.Optional[typing.List[IAction]]:
        '''(experimental) The actions to be performed with the transition.

        :default: - no actions will be performed

        :stability: experimental
        '''
        result = self._values.get("executing")
        return typing.cast(typing.Optional[typing.List[IAction]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransitionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IDetectorModel)
class DetectorModel(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iotevents.DetectorModel",
):
    '''(experimental) Defines an AWS IoT Events detector model in this stack.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_iotevents as iotevents
        import aws_cdk.aws_iotevents_actions as actions
        import aws_cdk.aws_lambda as lambda_
        
        # func: lambda.IFunction
        
        
        input = iotevents.Input(self, "MyInput",
            input_name="my_input",  # optional
            attribute_json_paths=["payload.deviceId", "payload.temperature"]
        )
        
        warm_state = iotevents.State(
            state_name="warm",
            on_enter=[iotevents.Event(
                event_name="test-enter-event",
                condition=iotevents.Expression.current_input(input),
                actions=[actions.LambdaInvokeAction(func)]
            )],
            on_input=[iotevents.Event( # optional
                event_name="test-input-event",
                actions=[actions.LambdaInvokeAction(func)])],
            on_exit=[iotevents.Event( # optional
                event_name="test-exit-event",
                actions=[actions.LambdaInvokeAction(func)])]
        )
        cold_state = iotevents.State(
            state_name="cold"
        )
        
        # transit to coldState when temperature is less than 15
        warm_state.transition_to(cold_state,
            event_name="to_coldState",  # optional property, default by combining the names of the States
            when=iotevents.Expression.lt(
                iotevents.Expression.input_attribute(input, "payload.temperature"),
                iotevents.Expression.from_string("15")),
            executing=[actions.LambdaInvokeAction(func)]
        )
        # transit to warmState when temperature is greater than or equal to 15
        cold_state.transition_to(warm_state,
            when=iotevents.Expression.gte(
                iotevents.Expression.input_attribute(input, "payload.temperature"),
                iotevents.Expression.from_string("15"))
        )
        
        iotevents.DetectorModel(self, "MyDetectorModel",
            detector_model_name="test-detector-model",  # optional
            description="test-detector-model-description",  # optional property, default is none
            evaluation_method=iotevents.EventEvaluation.SERIAL,  # optional property, default is iotevents.EventEvaluation.BATCH
            detector_key="payload.deviceId",  # optional property, default is none and single detector instance will be created and all inputs will be routed to it
            initial_state=warm_state
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        initial_state: State,
        description: typing.Optional[builtins.str] = None,
        detector_key: typing.Optional[builtins.str] = None,
        detector_model_name: typing.Optional[builtins.str] = None,
        evaluation_method: typing.Optional[EventEvaluation] = None,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param initial_state: (experimental) The state that is entered at the creation of each detector.
        :param description: (experimental) A brief description of the detector model. Default: none
        :param detector_key: (experimental) The value used to identify a detector instance. When a device or system sends input, a new detector instance with a unique key value is created. AWS IoT Events can continue to route input to its corresponding detector instance based on this identifying information. This parameter uses a JSON-path expression to select the attribute-value pair in the message payload that is used for identification. To route the message to the correct detector instance, the device must send a message payload that contains the same attribute-value. Default: - none (single detector instance will be created and all inputs will be routed to it)
        :param detector_model_name: (experimental) The name of the detector model. Default: - CloudFormation will generate a unique name of the detector model
        :param evaluation_method: (experimental) Information about the order in which events are evaluated and how actions are executed. When setting to SERIAL, variables are updated and event conditions are evaluated in the order that the events are defined. When setting to BATCH, variables within a state are updated and events within a state are performed only after all event conditions are evaluated. Default: EventEvaluation.BATCH
        :param role: (experimental) The role that grants permission to AWS IoT Events to perform its operations. Default: - a role will be created with default permissions

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f3e10a1c887b5f87239de26ae67a6c44346bbc98a046fe7f890f98ab3d0381)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DetectorModelProps(
            initial_state=initial_state,
            description=description,
            detector_key=detector_key,
            detector_model_name=detector_model_name,
            evaluation_method=evaluation_method,
            role=role,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromDetectorModelName")
    @builtins.classmethod
    def from_detector_model_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        detector_model_name: builtins.str,
    ) -> IDetectorModel:
        '''(experimental) Import an existing detector model.

        :param scope: -
        :param id: -
        :param detector_model_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__989b908a98c6e576bf49e96d046639d93daf5e6ebd22861b446b27fd74e0b45b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument detector_model_name", value=detector_model_name, expected_type=type_hints["detector_model_name"])
        return typing.cast(IDetectorModel, jsii.sinvoke(cls, "fromDetectorModelName", [scope, id, detector_model_name]))

    @builtins.property
    @jsii.member(jsii_name="detectorModelName")
    def detector_model_name(self) -> builtins.str:
        '''(experimental) The name of the detector model.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "detectorModelName"))


__all__ = [
    "ActionBindOptions",
    "ActionConfig",
    "CfnAlarmModel",
    "CfnAlarmModelProps",
    "CfnDetectorModel",
    "CfnDetectorModelProps",
    "CfnInput",
    "CfnInputProps",
    "DetectorModel",
    "DetectorModelProps",
    "Event",
    "EventEvaluation",
    "Expression",
    "IAction",
    "IDetectorModel",
    "IInput",
    "Input",
    "InputProps",
    "State",
    "StateProps",
    "TransitionOptions",
]

publication.publish()

def _typecheckingstub__a6e4e20ba363e3582ad4c70accbecdc3e65a61c102b483e5f244eb6757edb282(
    *,
    role: _aws_cdk_aws_iam_940a1ce0.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d439f5f4716bead9be50e1122600ed3b2d5603d310a4523ce577b254c0f1fa37(
    *,
    configuration: typing.Union[CfnDetectorModel.ActionProperty, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b865a8f80af7952b8b1b2e5849ec961ae5136962021870e5072b51e705cf71ef(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    alarm_rule: typing.Union[typing.Union[CfnAlarmModel.AlarmRuleProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    role_arn: builtins.str,
    alarm_capabilities: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.AlarmCapabilitiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    alarm_event_actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.AlarmEventActionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    alarm_model_description: typing.Optional[builtins.str] = None,
    alarm_model_name: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    severity: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b35ceb8f84eb5605375dab910268d296f60c1bacd5c30be3f3c804581abb2f35(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc3f2c8a584a104362374c79e0614db42489b5f4d282595b5545d4d35721bddd(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d16e53e3e055183bb3ecc8468e38382f6396c1cffd5d1b5467111f42e7d950c6(
    value: typing.Union[CfnAlarmModel.AlarmRuleProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97c6b18b8c6f64d6c959f437aaab99054154b1f300e33c2d1164a00f407c3726(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa9c01884d5e6b0057d9c603574a54e99207049299f60210b611434af9cc7d0(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAlarmModel.AlarmCapabilitiesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39551781ab30e8b75606d2c5480da65aa186cc5117af8aab7f8dae053433470(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAlarmModel.AlarmEventActionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4375f5713256be0f6ff946e4da30f1dfc1af932546d6e6156fd5b0a468a81b31(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d98a56666e8c2c8fff01ce6a5abd1646f39abde73d1942dfb1c7e6d756a677a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fdcae76ae679f4116866637a98a9e464d81b04c811f22eb028532f15f40116c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c550c17eb7ac3d503af21342bb28e717a8c5570860a6309d46833545ce5e35(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ce31ee5e28212451cf6e2ef3b9a0baadab9bccf136ddf92fb50b5a01d66e40(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2d49aa4bc7249874260ab9616b9866ce9e315a0ed5f31faeb171b9e25ac74f(
    *,
    dynamo_db: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.DynamoDBProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynamo_d_bv2: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.DynamoDBv2Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    firehose: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.FirehoseProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    iot_events: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.IotEventsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    iot_site_wise: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.IotSiteWiseProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    iot_topic_publish: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.IotTopicPublishProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lambda_: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.LambdaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sns: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.SnsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sqs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.SqsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8ecf1907f94be4f65cd1ef05ff98d984d1db1a5610d54694b32330e12379d4c(
    *,
    acknowledge_flow: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.AcknowledgeFlowProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    initialization_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.InitializationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de40a95f07bb0f0039395959b5963380ad4d6e9b2f30e8fce314408d58db484d(
    *,
    alarm_actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.AlarmActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1996cc62c11a58432f39f15e1f2d262e684403bad70d61c8c9feff2a563ea07d(
    *,
    simple_rule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.SimpleRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da7b4d62e42583bff1c92d47c9b4ec10cd620ef140852f206980d2244ef5cf3b(
    *,
    time_in_seconds: builtins.str,
    offset_in_nanos: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6d4ab6b1ff6d5770977fead02aba27fb717ede46cdd9e6a6ca6c3b77afd4d5(
    *,
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.AssetPropertyVariantProperty, typing.Dict[builtins.str, typing.Any]]],
    quality: typing.Optional[builtins.str] = None,
    timestamp: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.AssetPropertyTimestampProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3dff3482581c0d7b7f1f373a6939726703984e4cd432dda6ff5e5905986fc81(
    *,
    boolean_value: typing.Optional[builtins.str] = None,
    double_value: typing.Optional[builtins.str] = None,
    integer_value: typing.Optional[builtins.str] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f81c4293cf593a2baa751af6dce60d7ff55bc34f6b1a9698bd2ad03b3f7e7e4(
    *,
    hash_key_field: builtins.str,
    hash_key_value: builtins.str,
    table_name: builtins.str,
    hash_key_type: typing.Optional[builtins.str] = None,
    operation: typing.Optional[builtins.str] = None,
    payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    payload_field: typing.Optional[builtins.str] = None,
    range_key_field: typing.Optional[builtins.str] = None,
    range_key_type: typing.Optional[builtins.str] = None,
    range_key_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2bbd9176a2096155ec8c0b345254a576eefa26b05268c411a5b4e56f972eaf9(
    *,
    table_name: builtins.str,
    payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97c1dc45e15d1d1de750460f656506de609e77b9f5db1e68ae9dc159c6ff274c(
    *,
    delivery_stream_name: builtins.str,
    payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    separator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95837c1c4560c728492c3735f77080263999005659248c85ab38116efe8c98f1(
    *,
    disabled_on_initialization: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a4b97990788585da844a043b73294f787a5e2a0dd55e480c1f4ea48e904549(
    *,
    input_name: builtins.str,
    payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfa1d4e0b76e794ba751e7417e9d24ad51b6e74bbe555ee58e958f52351df9ac(
    *,
    asset_id: typing.Optional[builtins.str] = None,
    entry_id: typing.Optional[builtins.str] = None,
    property_alias: typing.Optional[builtins.str] = None,
    property_id: typing.Optional[builtins.str] = None,
    property_value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.AssetPropertyValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211c4f79f8cc0420aac5fd9faee1d93e51d8e055861a16ba062be2824488d4ce(
    *,
    mqtt_topic: builtins.str,
    payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca9296bdd50c0b157abb60b919efee87de8d50dfa3ddb183568f6f79ded785a(
    *,
    function_arn: builtins.str,
    payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87051e63342027aa5b09d2eef106ab646561f61a6373d55f1ad3c76d0f5135d(
    *,
    content_expression: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf82e9fa5c332ee501ab6e3f649c8952741ec85ee7790640a9f0ac469ba86556(
    *,
    comparison_operator: builtins.str,
    input_property: builtins.str,
    threshold: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8f1c762e8184bc32d3df2aaa983a732404d12720e10ee361b3db524b73bf59(
    *,
    target_arn: builtins.str,
    payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b518d32ae21e79224630c149b5b9ddab07513e3db392536b138607d09e3ad55(
    *,
    queue_url: builtins.str,
    payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    use_base64: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__858c6d54605adf535894fac594bf100a6ec4bdd7a972ce9162352f95b9934e09(
    *,
    alarm_rule: typing.Union[typing.Union[CfnAlarmModel.AlarmRuleProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    role_arn: builtins.str,
    alarm_capabilities: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.AlarmCapabilitiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    alarm_event_actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAlarmModel.AlarmEventActionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    alarm_model_description: typing.Optional[builtins.str] = None,
    alarm_model_name: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    severity: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f2aaacccbdf39fc3ae6cb97fa81518a278625a9848665d3760abe14bf34e3af(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    detector_model_definition: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.DetectorModelDefinitionProperty, typing.Dict[builtins.str, typing.Any]]],
    role_arn: builtins.str,
    detector_model_description: typing.Optional[builtins.str] = None,
    detector_model_name: typing.Optional[builtins.str] = None,
    evaluation_method: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac63b00f89aa5a4bbeede8c1f17ef03e6f7d729c47716c4b0627a146856d85a6(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52d165955426f30a9de317a9cf94ee1324774376cc6cbe1954de34f10ffa6157(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d455d74c1be301e4f5070c18fd43a70a6b9868591d7d7e0d8b98dd262ed8540c(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDetectorModel.DetectorModelDefinitionProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9bba1ba0b474c50c03e97436648c1c52de0dcea2084553e505e21e12a6c8cb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1befb4a024f9773e0245579b01128449e3f7e867bdbebddd82c744ee5cc58fb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__364dd7d50a8269617f57ef27267f8115ed950958b98f2d6715bef12a45652df2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9caa2ed3026f19cd12ac5bb6aeabe66388ba53d49111a0f158481b5c588e861c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f1c312faffd330b8198e3a0e32b8a2729b80ca99188128373022dd98399e4d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__941e688a554b35e3d59da041d715f16e37c14bd53b92e2ecee7cab3c8cf5b910(
    *,
    clear_timer: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.ClearTimerProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynamo_db: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.DynamoDBProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynamo_d_bv2: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.DynamoDBv2Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    firehose: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.FirehoseProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    iot_events: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.IotEventsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    iot_site_wise: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.IotSiteWiseProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    iot_topic_publish: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.IotTopicPublishProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lambda_: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.LambdaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    reset_timer: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.ResetTimerProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    set_timer: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.SetTimerProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    set_variable: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.SetVariableProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sns: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.SnsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sqs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.SqsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd4ed56d59949f5787f4680c51797508688338e21a8271708094f1ab9b7a74f(
    *,
    time_in_seconds: builtins.str,
    offset_in_nanos: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14f43e0e57626c7d6b69a42bb377d37552b8ccef973a097c6a4e0d39810862e5(
    *,
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.AssetPropertyVariantProperty, typing.Dict[builtins.str, typing.Any]]],
    quality: typing.Optional[builtins.str] = None,
    timestamp: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.AssetPropertyTimestampProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a99f6659005b765e75663adbdb672e127e821885f889825750025173b5f4a99(
    *,
    boolean_value: typing.Optional[builtins.str] = None,
    double_value: typing.Optional[builtins.str] = None,
    integer_value: typing.Optional[builtins.str] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4416a7142280a8194936287914e2d3f4e3e95032a15849dca1b6dcc3a9581178(
    *,
    timer_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a25afe04c9b8dd7d53a71a1d933ad80cc386085ea5f9fe135c68adee6f6ea4ae(
    *,
    initial_state_name: builtins.str,
    states: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.StateProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31d1c7d374d5e831a3813fd7c0cfdf95eb7ddfdb3c86f207b90cfc7207002e9(
    *,
    hash_key_field: builtins.str,
    hash_key_value: builtins.str,
    table_name: builtins.str,
    hash_key_type: typing.Optional[builtins.str] = None,
    operation: typing.Optional[builtins.str] = None,
    payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    payload_field: typing.Optional[builtins.str] = None,
    range_key_field: typing.Optional[builtins.str] = None,
    range_key_type: typing.Optional[builtins.str] = None,
    range_key_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a888ed429a92d938952ca9d54c1845e5339696b77a967c76e5169847f0d8a1e(
    *,
    table_name: builtins.str,
    payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61761053338e03f2fcf818c1bf2130b57529b93342d9fb78c881fbc864df019(
    *,
    event_name: builtins.str,
    actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnDetectorModel.ActionProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
    condition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba3b4ec59ca7a6d232da9b1730f785ec202ec42fe148cc714809748830f07de8(
    *,
    delivery_stream_name: builtins.str,
    payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    separator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6738bafd08f099889eaa028bcdd7d23d8f2f3a581a23f5f9b9010743ba140300(
    *,
    input_name: builtins.str,
    payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ea319e3419ecaaed81e94d4acc411e0f85ad42445d3174eeb741f3186fb0c9(
    *,
    property_value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.AssetPropertyValueProperty, typing.Dict[builtins.str, typing.Any]]],
    asset_id: typing.Optional[builtins.str] = None,
    entry_id: typing.Optional[builtins.str] = None,
    property_alias: typing.Optional[builtins.str] = None,
    property_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3920e2a00706daf32dace0a6ea7dbe9aed3e387cc5d0dea3ef7767ef876fd325(
    *,
    mqtt_topic: builtins.str,
    payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__293a086a49c67b3204fd673189de27386c912f033ae6bc74d43463e58c9d0725(
    *,
    function_arn: builtins.str,
    payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05dba8292b91c490e5a24d386248dbb0280b4500201cbc3055bd83e4a417ce1d(
    *,
    events: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.EventProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9afa050392906e9434389b9edae26edb2762c0e869f1aa4ff0dc3006750de422(
    *,
    events: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.EventProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e1f51bf4a7f70eed01fd39b1db9e0dc17066d5cf08a553a091cfa0a6c0d4d5f(
    *,
    events: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.EventProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    transition_events: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.TransitionEventProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c78c1e0ebddc06eb1d8f94cd4699159bcbf6a62da73d5b2c579414e407737b4(
    *,
    content_expression: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0135145118d95eda2e4ebc894b6ea9648f4fe9dafc0bd12979bc95803e71ae2c(
    *,
    timer_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0917589c4b566176b94107f82e1799155dc39252113d78103c0b1b4e0514af7d(
    *,
    timer_name: builtins.str,
    duration_expression: typing.Optional[builtins.str] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f166d174dbdec15ea523e0d5e5673a6cee715c762ca23b1ff9b1b0e5a94c90c(
    *,
    value: builtins.str,
    variable_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e5c8988e7bc1074899c099b5589c681ce7e914462ad5133869d72104c97f034(
    *,
    target_arn: builtins.str,
    payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f4b00db15cec4d0e31cd3ae94cde0fe4240511b1191fbf746ae165a36538fd(
    *,
    queue_url: builtins.str,
    payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    use_base64: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad72a224aee928a149d5a9da9a562a5f111b31203a328cc4a8fed15dc8c90f32(
    *,
    state_name: builtins.str,
    on_enter: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.OnEnterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    on_exit: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.OnExitProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    on_input: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.OnInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c559f87f0cd942e9bcd26f6e591d9ad45420f38a707a30b3f6818f33e08af2d(
    *,
    condition: builtins.str,
    event_name: builtins.str,
    next_state: builtins.str,
    actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnDetectorModel.ActionProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8e30ba23b6ecb962d840a1a1201e65ae6f2c8f187561a7cf44d5fd8eade4512(
    *,
    detector_model_definition: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetectorModel.DetectorModelDefinitionProperty, typing.Dict[builtins.str, typing.Any]]],
    role_arn: builtins.str,
    detector_model_description: typing.Optional[builtins.str] = None,
    detector_model_name: typing.Optional[builtins.str] = None,
    evaluation_method: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f2fc6b7bbe4b1f65d243c1ff89e3fe75af14aff4158f940416fef97a826473(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    input_definition: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInput.InputDefinitionProperty, typing.Dict[builtins.str, typing.Any]]],
    input_description: typing.Optional[builtins.str] = None,
    input_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be7cd0224d183e31f465309b8c9de028c5b329736d5aae2ce176a96362f15d0(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0898d278a67b758da0fcd9827fa251ad877a952c928f8b5295c8c6581b8cd6ce(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b0ec99a885e850e67e0a41ec8b9fc6520cb5c34018435cf6c68ce7278f4697(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnInput.InputDefinitionProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50766aa7996de8fcd48f6adea2158fd4c0b50fa06126bc624cc9e2506e8b56e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a86f17a4a4eac005742143149464fee2507fcdea27264ecb7c977152aa37b2ce(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c50352623d6e3bb9331a191ceae3166443a9ee8b20e7d1efa1295ac2b597fe0f(
    *,
    json_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3e938ad00c56449b1b3cda4b57d66c9d89c38fc2b44fe72c5681e2b13f1f63(
    *,
    attributes: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInput.AttributeProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6444f69e6a66f8069a5a2c1c9e2ecc3a008795bd121adb8032245553f620ff09(
    *,
    input_definition: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInput.InputDefinitionProperty, typing.Dict[builtins.str, typing.Any]]],
    input_description: typing.Optional[builtins.str] = None,
    input_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aebf79fa1acd81efa906913f1ca96fcc710f16e945a27c388d9af35ff61f965a(
    *,
    initial_state: State,
    description: typing.Optional[builtins.str] = None,
    detector_key: typing.Optional[builtins.str] = None,
    detector_model_name: typing.Optional[builtins.str] = None,
    evaluation_method: typing.Optional[EventEvaluation] = None,
    role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd0180524e458ab33b60171fbad3530ccee1c10edfdbf0481caf1a82c210486f(
    *,
    event_name: builtins.str,
    actions: typing.Optional[typing.Sequence[IAction]] = None,
    condition: typing.Optional[Expression] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2adcde9e1aebb67e309495c4f283992f6ccabb7e286dcabe4f22b090bcb8bc5(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d6a7ee8eaf2af8cc2ce00f5f45a096d449737ef5febf0eb43c4de8553e9887(
    input: IInput,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e788239ae3d00dc07f530a4d7550e25061eb786f9887575c410982eba92ba23(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2fd1fc181e89b3f9bc2752a8edfe83152cb302a735eb499b99dac4bac5be833(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c3465200c7a77486f40a69a0c1764c941011e8a6729fcc6399137960de5a0f(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a73c08d7ba9b2a565b147391bb1877a2a30a3022387df82fb210cefea9079f(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4bec8a9359e40c38e34ef4a1fc146e79316e9ecfde950f3ce2bd2919f64c361(
    input: IInput,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81973e05d8a74cf3bba291907eb803f6572fce4e3e65e48b39520a9be752e805(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380acac5d46e88d6de66fa90bc47875d578d6cc3f7f88918512f8f802112e5ac(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea6f40d0b21c36128d79b156f8890a1a79f4939257981ebbadd73b3da35651c(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a76ed3f4df1e48a1164ff439b9c922b766aefb3f57e223f5a398fe3b491a9bd9(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d24971e1624fc3946b3b95ccb83a848ead0f9d5d5b6b4ca5257af445b89ab730(
    parent_priority: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__959e6c5f02243a49a319d90bf3843c8e380e497782132de964e8f331b4cabed1(
    scope: _constructs_77d1e7e8.Construct,
    *,
    role: _aws_cdk_aws_iam_940a1ce0.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52069038289e50f95bd000409f6f17da5d7907c98d4f9d3259f864e530326ce(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce1acfc0d062982b612615a9c24decdb9823156576d760781192cc0025e404d8(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1c9709d4b03fe647971258a1dff1507db076ca85d7e1f62d8a23088c287b84(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    attribute_json_paths: typing.Sequence[builtins.str],
    input_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5b7aa94617b1c8e737a91c26218670dc64ccf90bface1c544bbdb5a77245aa1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    input_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da87756126d61843b6c456f0dbc4fdfc488feb35744c4c18f99ccdd59240e9d8(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc61510051b3f2625a09b308b69a0d3f8f1f46e1224c41d297af9e9087b485fc(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b774f8902bf22c53aa4307c5d30820bdb0c75c7502a06096f34802b338980af5(
    *,
    attribute_json_paths: typing.Sequence[builtins.str],
    input_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c2c4af4f894c4c9f5b579fc93e0c943f72ee49a862e3e605002c42a8eae323(
    target_state: State,
    *,
    when: Expression,
    event_name: typing.Optional[builtins.str] = None,
    executing: typing.Optional[typing.Sequence[IAction]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a97c297f459a4463d79fda8f2b6ad0f5a33fcc278b799fe34f674e2205dedca(
    *,
    state_name: builtins.str,
    on_enter: typing.Optional[typing.Sequence[typing.Union[Event, typing.Dict[builtins.str, typing.Any]]]] = None,
    on_exit: typing.Optional[typing.Sequence[typing.Union[Event, typing.Dict[builtins.str, typing.Any]]]] = None,
    on_input: typing.Optional[typing.Sequence[typing.Union[Event, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bacaa8d88dbb67842d4a6ecc3d8d12890fc663d23331e415273a40dcf6d11c79(
    *,
    when: Expression,
    event_name: typing.Optional[builtins.str] = None,
    executing: typing.Optional[typing.Sequence[IAction]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f3e10a1c887b5f87239de26ae67a6c44346bbc98a046fe7f890f98ab3d0381(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    initial_state: State,
    description: typing.Optional[builtins.str] = None,
    detector_key: typing.Optional[builtins.str] = None,
    detector_model_name: typing.Optional[builtins.str] = None,
    evaluation_method: typing.Optional[EventEvaluation] = None,
    role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__989b908a98c6e576bf49e96d046639d93daf5e6ebd22861b446b27fd74e0b45b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    detector_model_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
