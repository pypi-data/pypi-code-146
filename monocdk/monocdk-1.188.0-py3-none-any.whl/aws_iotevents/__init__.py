'''
# AWS::IoTEvents Construct Library

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
import monocdk as iotevents
```

## `DetectorModel`

The following example creates an AWS IoT Events detector model to your stack.
The detector model need a reference to at least one AWS IoT Events input.
AWS IoT Events inputs enable the detector to get MQTT payload values from IoT Core rules.

You can define built-in actions to use a timer or set a variable, or send data to other AWS resources.
See also [@aws-cdk/aws-iotevents-actions](https://docs.aws.amazon.com/cdk/api/v1/docs/aws-iotevents-actions-readme.html) for other actions.

```python
import monocdk as iotevents
import monocdk as actions
import monocdk as lambda_

# func: lambda.IFunction


input = iotevents.Input(self, "MyInput",
    input_name="my_input",  # optional
    attribute_json_paths=["payload.deviceId", "payload.temperature"]
)

warm_state = iotevents.State(
    state_name="warm",
    on_enter=[iotevents.aws_iotevents.Event(
        event_name="test-enter-event",
        condition=iotevents.Expression.current_input(input),
        actions=[actions.LambdaInvokeAction(func)]
    )],
    on_input=[iotevents.aws_iotevents.Event( # optional
        event_name="test-input-event",
        actions=[actions.LambdaInvokeAction(func)])],
    on_exit=[iotevents.aws_iotevents.Event( # optional
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
import monocdk as iam
import monocdk as iotevents

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

from .._jsii import *

import constructs as _constructs_77d1e7e8
from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    Resource as _Resource_abff4495,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_iam import (
    Grant as _Grant_bcb5eae7,
    IGrantable as _IGrantable_4c5a91d1,
    IRole as _IRole_59af6f50,
)


@jsii.data_type(
    jsii_type="monocdk.aws_iotevents.ActionBindOptions",
    jsii_struct_bases=[],
    name_mapping={"role": "role"},
)
class ActionBindOptions:
    def __init__(self, *, role: _IRole_59af6f50) -> None:
        '''(experimental) Options when binding a Action to a detector model.

        :param role: (experimental) The IAM role assumed by IoT Events to perform the action.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            from monocdk import aws_iotevents as iotevents
            
            # role: iam.Role
            
            action_bind_options = iotevents.ActionBindOptions(
                role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f505628cd6253804a698aab6faedb360100aea82b67ccb476052748e631702a)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role": role,
        }

    @builtins.property
    def role(self) -> _IRole_59af6f50:
        '''(experimental) The IAM role assumed by IoT Events to perform the action.

        :stability: experimental
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(_IRole_59af6f50, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_iotevents.ActionConfig",
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
            from monocdk import aws_iotevents as iotevents
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__79b4b2fdb4ca2ca770997c81df82d8d663d25bfc54d96c4d146d045a297e3b64)
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


@jsii.implements(_IInspectable_82c04a63)
class CfnAlarmModel(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iotevents.CfnAlarmModel",
):
    '''A CloudFormation ``AWS::IoTEvents::AlarmModel``.

    Represents an alarm model to monitor an AWS IoT Events input attribute. You can use the alarm to get notified when the value is outside a specified range. For more information, see `Create an alarm model <https://docs.aws.amazon.com/iotevents/latest/developerguide/create-alarms.html>`_ in the *AWS IoT Events Developer Guide* .

    :cloudformationResource: AWS::IoTEvents::AlarmModel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iotevents as iotevents
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        alarm_rule: typing.Union[typing.Union["CfnAlarmModel.AlarmRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        role_arn: builtins.str,
        alarm_capabilities: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.AlarmCapabilitiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        alarm_event_actions: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.AlarmEventActionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        alarm_model_description: typing.Optional[builtins.str] = None,
        alarm_model_name: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        severity: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7534c9d68936e1c392dfb05008475157f303eea28ecb6c22480714aaa7892bf)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8259b996358635cc0c2736e4ea45cb49188380c97914087547bfeb7cf6b60185)
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
            type_hints = typing.get_type_hints(_typecheckingstub__446fdcf1fbc6ce4e83f9368f59cb3d103c24467c788c19129de2e51b5867a5c8)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of key-value pairs that contain metadata for the alarm model.

        The tags help you manage the alarm model. For more information, see `Tagging your AWS IoT Events resources <https://docs.aws.amazon.com/iotevents/latest/developerguide/tagging-iotevents.html>`_ in the *AWS IoT Events Developer Guide* .

        You can create up to 50 tags for one alarm model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="alarmRule")
    def alarm_rule(
        self,
    ) -> typing.Union["CfnAlarmModel.AlarmRuleProperty", _IResolvable_a771d0ef]:
        '''Defines when your alarm is invoked.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-alarmrule
        '''
        return typing.cast(typing.Union["CfnAlarmModel.AlarmRuleProperty", _IResolvable_a771d0ef], jsii.get(self, "alarmRule"))

    @alarm_rule.setter
    def alarm_rule(
        self,
        value: typing.Union["CfnAlarmModel.AlarmRuleProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5a7944cb33d7dce7e34ed9c94ed425f2e91a2ef2f3ed78b7bda59bc90a0ef0e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33b7c40804a7e6801af108eaadb7c60cfdef4b74344ba3233b326b7a163268c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="alarmCapabilities")
    def alarm_capabilities(
        self,
    ) -> typing.Optional[typing.Union["CfnAlarmModel.AlarmCapabilitiesProperty", _IResolvable_a771d0ef]]:
        '''Contains the configuration information of alarm state changes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-alarmcapabilities
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.AlarmCapabilitiesProperty", _IResolvable_a771d0ef]], jsii.get(self, "alarmCapabilities"))

    @alarm_capabilities.setter
    def alarm_capabilities(
        self,
        value: typing.Optional[typing.Union["CfnAlarmModel.AlarmCapabilitiesProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b878d772bd0873b3f2cd2483fe5c0ff9fbbb63afcfab434ea07ccefd836ef43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmCapabilities", value)

    @builtins.property
    @jsii.member(jsii_name="alarmEventActions")
    def alarm_event_actions(
        self,
    ) -> typing.Optional[typing.Union["CfnAlarmModel.AlarmEventActionsProperty", _IResolvable_a771d0ef]]:
        '''Contains information about one or more alarm actions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-alarmeventactions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.AlarmEventActionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "alarmEventActions"))

    @alarm_event_actions.setter
    def alarm_event_actions(
        self,
        value: typing.Optional[typing.Union["CfnAlarmModel.AlarmEventActionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46684fade78a3ded88581d5c9450e50431e0e31b9502dbb9063f4b68c17a2450)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8dc6aa08419411ed0c2b4c6559168d4c5bf3ef72edb80da33a2c6aa1c1523a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b85508bcdc7953fa9de42f96203bf90c0f422f1f4184f9d7a76abeecacf48871)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0e5fd02e299f8621a7f87089115c6cfecd55c2993a2dd8879d9d15ffbaeb7c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a348df024311f52e40b249d0481a418788788239c0a73f00aa04bb49710a10d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnAlarmModel.AcknowledgeFlowProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class AcknowledgeFlowProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Specifies whether to get notified for alarm state changes.

            :param enabled: The value must be ``TRUE`` or ``FALSE`` . If ``TRUE`` , you receive a notification when the alarm state changes. You must choose to acknowledge the notification before the alarm state can return to ``NORMAL`` . If ``FALSE`` , you won't receive notifications. The alarm automatically changes to the ``NORMAL`` state when the input property value returns to the specified range.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-acknowledgeflow.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotevents as iotevents
                
                acknowledge_flow_property = iotevents.CfnAlarmModel.AcknowledgeFlowProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8d9e888195d965759839d49913adbff9999e0139d138df3e53d2427d2c5adc98)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''The value must be ``TRUE`` or ``FALSE`` .

            If ``TRUE`` , you receive a notification when the alarm state changes. You must choose to acknowledge the notification before the alarm state can return to ``NORMAL`` . If ``FALSE`` , you won't receive notifications. The alarm automatically changes to the ``NORMAL`` state when the input property value returns to the specified range.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-acknowledgeflow.html#cfn-iotevents-alarmmodel-acknowledgeflow-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AcknowledgeFlowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnAlarmModel.AlarmActionProperty",
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
            dynamo_db: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.DynamoDBProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            dynamo_d_bv2: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.DynamoDBv2Property", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            firehose: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.FirehoseProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            iot_events: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.IotEventsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            iot_site_wise: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.IotSiteWiseProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            iot_topic_publish: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.IotTopicPublishProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            lambda_: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.LambdaProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sns: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.SnsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sqs: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.SqsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__0ee1d6f8df8dba71c094c18cde82ecf0c2a33baa4e6846ceca64a316c2ad2b2c)
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
        ) -> typing.Optional[typing.Union["CfnAlarmModel.DynamoDBProperty", _IResolvable_a771d0ef]]:
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
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.DynamoDBProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def dynamo_d_bv2(
            self,
        ) -> typing.Optional[typing.Union["CfnAlarmModel.DynamoDBv2Property", _IResolvable_a771d0ef]]:
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
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.DynamoDBv2Property", _IResolvable_a771d0ef]], result)

        @builtins.property
        def firehose(
            self,
        ) -> typing.Optional[typing.Union["CfnAlarmModel.FirehoseProperty", _IResolvable_a771d0ef]]:
            '''Sends information about the detector model instance and the event that triggered the action to an Amazon Kinesis Data Firehose delivery stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-firehose
            '''
            result = self._values.get("firehose")
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.FirehoseProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def iot_events(
            self,
        ) -> typing.Optional[typing.Union["CfnAlarmModel.IotEventsProperty", _IResolvable_a771d0ef]]:
            '''Sends an AWS IoT Events input, passing in information about the detector model instance and the event that triggered the action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-iotevents
            '''
            result = self._values.get("iot_events")
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.IotEventsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def iot_site_wise(
            self,
        ) -> typing.Optional[typing.Union["CfnAlarmModel.IotSiteWiseProperty", _IResolvable_a771d0ef]]:
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
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.IotSiteWiseProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def iot_topic_publish(
            self,
        ) -> typing.Optional[typing.Union["CfnAlarmModel.IotTopicPublishProperty", _IResolvable_a771d0ef]]:
            '''Information required to publish the MQTT message through the AWS IoT message broker.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-iottopicpublish
            '''
            result = self._values.get("iot_topic_publish")
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.IotTopicPublishProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def lambda_(
            self,
        ) -> typing.Optional[typing.Union["CfnAlarmModel.LambdaProperty", _IResolvable_a771d0ef]]:
            '''Calls a Lambda function, passing in information about the detector model instance and the event that triggered the action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-lambda
            '''
            result = self._values.get("lambda_")
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.LambdaProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sns(
            self,
        ) -> typing.Optional[typing.Union["CfnAlarmModel.SnsProperty", _IResolvable_a771d0ef]]:
            '''``CfnAlarmModel.AlarmActionProperty.Sns``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-sns
            '''
            result = self._values.get("sns")
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.SnsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sqs(
            self,
        ) -> typing.Optional[typing.Union["CfnAlarmModel.SqsProperty", _IResolvable_a771d0ef]]:
            '''Sends information about the detector model instance and the event that triggered the action to an Amazon SQS queue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-sqs
            '''
            result = self._values.get("sqs")
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.SqsProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnAlarmModel.AlarmCapabilitiesProperty",
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
            acknowledge_flow: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.AcknowledgeFlowProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            initialization_configuration: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.InitializationConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Contains the configuration information of alarm state changes.

            :param acknowledge_flow: Specifies whether to get notified for alarm state changes.
            :param initialization_configuration: Specifies the default alarm state. The configuration applies to all alarms that were created based on this alarm model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmcapabilities.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__af8cba49d23702bc0fd211ed9fa32dc62c91496b424333554331a0476f082d55)
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
        ) -> typing.Optional[typing.Union["CfnAlarmModel.AcknowledgeFlowProperty", _IResolvable_a771d0ef]]:
            '''Specifies whether to get notified for alarm state changes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmcapabilities.html#cfn-iotevents-alarmmodel-alarmcapabilities-acknowledgeflow
            '''
            result = self._values.get("acknowledge_flow")
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.AcknowledgeFlowProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def initialization_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnAlarmModel.InitializationConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Specifies the default alarm state.

            The configuration applies to all alarms that were created based on this alarm model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmcapabilities.html#cfn-iotevents-alarmmodel-alarmcapabilities-initializationconfiguration
            '''
            result = self._values.get("initialization_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.InitializationConfigurationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmCapabilitiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnAlarmModel.AlarmEventActionsProperty",
        jsii_struct_bases=[],
        name_mapping={"alarm_actions": "alarmActions"},
    )
    class AlarmEventActionsProperty:
        def __init__(
            self,
            *,
            alarm_actions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAlarmModel.AlarmActionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''Contains information about one or more alarm actions.

            :param alarm_actions: Specifies one or more supported actions to receive notifications when the alarm state changes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmeventactions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__42dbc3d1726f37254888dc63d800917aeb2ea78249e87c5007e30b8d4bb932d9)
                check_type(argname="argument alarm_actions", value=alarm_actions, expected_type=type_hints["alarm_actions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alarm_actions is not None:
                self._values["alarm_actions"] = alarm_actions

        @builtins.property
        def alarm_actions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAlarmModel.AlarmActionProperty", _IResolvable_a771d0ef]]]]:
            '''Specifies one or more supported actions to receive notifications when the alarm state changes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmeventactions.html#cfn-iotevents-alarmmodel-alarmeventactions-alarmactions
            '''
            result = self._values.get("alarm_actions")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAlarmModel.AlarmActionProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmEventActionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnAlarmModel.AlarmRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"simple_rule": "simpleRule"},
    )
    class AlarmRuleProperty:
        def __init__(
            self,
            *,
            simple_rule: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.SimpleRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Defines when your alarm is invoked.

            :param simple_rule: A rule that compares an input property value to a threshold value with a comparison operator.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotevents as iotevents
                
                alarm_rule_property = iotevents.CfnAlarmModel.AlarmRuleProperty(
                    simple_rule=iotevents.CfnAlarmModel.SimpleRuleProperty(
                        comparison_operator="comparisonOperator",
                        input_property="inputProperty",
                        threshold="threshold"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4c3d326845bfad3fde5a49c444ebfcb275ef393654b1373eea5e9d2629c3ecc0)
                check_type(argname="argument simple_rule", value=simple_rule, expected_type=type_hints["simple_rule"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if simple_rule is not None:
                self._values["simple_rule"] = simple_rule

        @builtins.property
        def simple_rule(
            self,
        ) -> typing.Optional[typing.Union["CfnAlarmModel.SimpleRuleProperty", _IResolvable_a771d0ef]]:
            '''A rule that compares an input property value to a threshold value with a comparison operator.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmrule.html#cfn-iotevents-alarmmodel-alarmrule-simplerule
            '''
            result = self._values.get("simple_rule")
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.SimpleRuleProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnAlarmModel.AssetPropertyTimestampProperty",
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
                from monocdk import aws_iotevents as iotevents
                
                asset_property_timestamp_property = iotevents.CfnAlarmModel.AssetPropertyTimestampProperty(
                    time_in_seconds="timeInSeconds",
                
                    # the properties below are optional
                    offset_in_nanos="offsetInNanos"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2c8697800c5a0580751eeae7f3cb2dd86767b37d250cb22cdce580eb1bc01100)
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
        jsii_type="monocdk.aws_iotevents.CfnAlarmModel.AssetPropertyValueProperty",
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
            value: typing.Union[typing.Union["CfnAlarmModel.AssetPropertyVariantProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            quality: typing.Optional[builtins.str] = None,
            timestamp: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.AssetPropertyTimestampProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__e4d29bba68e1311bdcaedc8caa6b95a96f6e6c5836463aaa71257003e009a792)
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
        ) -> typing.Union["CfnAlarmModel.AssetPropertyVariantProperty", _IResolvable_a771d0ef]:
            '''The value to send to an asset property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertyvalue.html#cfn-iotevents-alarmmodel-assetpropertyvalue-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(typing.Union["CfnAlarmModel.AssetPropertyVariantProperty", _IResolvable_a771d0ef], result)

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
        ) -> typing.Optional[typing.Union["CfnAlarmModel.AssetPropertyTimestampProperty", _IResolvable_a771d0ef]]:
            '''The timestamp associated with the asset property value.

            The default is the current event time.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertyvalue.html#cfn-iotevents-alarmmodel-assetpropertyvalue-timestamp
            '''
            result = self._values.get("timestamp")
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.AssetPropertyTimestampProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetPropertyValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnAlarmModel.AssetPropertyVariantProperty",
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
                from monocdk import aws_iotevents as iotevents
                
                asset_property_variant_property = iotevents.CfnAlarmModel.AssetPropertyVariantProperty(
                    boolean_value="booleanValue",
                    double_value="doubleValue",
                    integer_value="integerValue",
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7ff5d722da871984b1680dd373c312d836657e3bc72e6f954d79077542c56d60)
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
        jsii_type="monocdk.aws_iotevents.CfnAlarmModel.DynamoDBProperty",
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
            payload: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__ec5c92107587ba507361d1202e1bd17939a41d35cd1190095f495ad6d372e34e)
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
        ) -> typing.Optional[typing.Union["CfnAlarmModel.PayloadProperty", _IResolvable_a771d0ef]]:
            '''Information needed to configure the payload.

            By default, AWS IoT Events generates a standard payload in JSON for any action. This action payload contains all attribute-value pairs that have the information about the detector model instance and the event triggered the action. To configure the action payload, you can use ``contentExpression`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html#cfn-iotevents-alarmmodel-dynamodb-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.PayloadProperty", _IResolvable_a771d0ef]], result)

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
        jsii_type="monocdk.aws_iotevents.CfnAlarmModel.DynamoDBv2Property",
        jsii_struct_bases=[],
        name_mapping={"table_name": "tableName", "payload": "payload"},
    )
    class DynamoDBv2Property:
        def __init__(
            self,
            *,
            table_name: builtins.str,
            payload: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__56ac3206b191c481daeab544a1cb989799865da2e1881ea4883c07875b3aa95b)
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
        ) -> typing.Optional[typing.Union["CfnAlarmModel.PayloadProperty", _IResolvable_a771d0ef]]:
            '''``CfnAlarmModel.DynamoDBv2Property.Payload``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodbv2.html#cfn-iotevents-alarmmodel-dynamodbv2-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.PayloadProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamoDBv2Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnAlarmModel.FirehoseProperty",
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
            payload: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__5eda6a59407afd6eea06bd6e8603e6aa58281533dc1146fd1412be66d877f2fc)
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
        ) -> typing.Optional[typing.Union["CfnAlarmModel.PayloadProperty", _IResolvable_a771d0ef]]:
            '''You can configure the action payload when you send a message to an Amazon Kinesis Data Firehose delivery stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-firehose.html#cfn-iotevents-alarmmodel-firehose-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.PayloadProperty", _IResolvable_a771d0ef]], result)

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
        jsii_type="monocdk.aws_iotevents.CfnAlarmModel.InitializationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"disabled_on_initialization": "disabledOnInitialization"},
    )
    class InitializationConfigurationProperty:
        def __init__(
            self,
            *,
            disabled_on_initialization: typing.Union[builtins.bool, _IResolvable_a771d0ef],
        ) -> None:
            '''Specifies the default alarm state.

            The configuration applies to all alarms that were created based on this alarm model.

            :param disabled_on_initialization: The value must be ``TRUE`` or ``FALSE`` . If ``FALSE`` , all alarm instances created based on the alarm model are activated. The default value is ``TRUE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-initializationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotevents as iotevents
                
                initialization_configuration_property = iotevents.CfnAlarmModel.InitializationConfigurationProperty(
                    disabled_on_initialization=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4c58a201ea33c5bd1bb42192a2a04450f00c7a00f5d57cf7aa961cf10d966112)
                check_type(argname="argument disabled_on_initialization", value=disabled_on_initialization, expected_type=type_hints["disabled_on_initialization"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "disabled_on_initialization": disabled_on_initialization,
            }

        @builtins.property
        def disabled_on_initialization(
            self,
        ) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''The value must be ``TRUE`` or ``FALSE`` .

            If ``FALSE`` , all alarm instances created based on the alarm model are activated. The default value is ``TRUE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-initializationconfiguration.html#cfn-iotevents-alarmmodel-initializationconfiguration-disabledoninitialization
            '''
            result = self._values.get("disabled_on_initialization")
            assert result is not None, "Required property 'disabled_on_initialization' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InitializationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnAlarmModel.IotEventsProperty",
        jsii_struct_bases=[],
        name_mapping={"input_name": "inputName", "payload": "payload"},
    )
    class IotEventsProperty:
        def __init__(
            self,
            *,
            input_name: builtins.str,
            payload: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Sends an AWS IoT Events input, passing in information about the detector model instance and the event that triggered the action.

            :param input_name: The name of the AWS IoT Events input where the data is sent.
            :param payload: You can configure the action payload when you send a message to an AWS IoT Events input.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iotevents.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__a4a7222cab72c17189d6a4599f1d66740b90f8f11ef80faa8a4c69fc613c00f6)
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
        ) -> typing.Optional[typing.Union["CfnAlarmModel.PayloadProperty", _IResolvable_a771d0ef]]:
            '''You can configure the action payload when you send a message to an AWS IoT Events input.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iotevents.html#cfn-iotevents-alarmmodel-iotevents-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.PayloadProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IotEventsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnAlarmModel.IotSiteWiseProperty",
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
            property_value: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.AssetPropertyValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__62ff5536e20d1cad7b1e02121aa4f26d58de6cddb7d9f693d44a6b39ddea8008)
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
        ) -> typing.Optional[typing.Union["CfnAlarmModel.AssetPropertyValueProperty", _IResolvable_a771d0ef]]:
            '''The value to send to the asset property.

            This value contains timestamp, quality, and value (TQV) information.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iotsitewise.html#cfn-iotevents-alarmmodel-iotsitewise-propertyvalue
            '''
            result = self._values.get("property_value")
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.AssetPropertyValueProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IotSiteWiseProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnAlarmModel.IotTopicPublishProperty",
        jsii_struct_bases=[],
        name_mapping={"mqtt_topic": "mqttTopic", "payload": "payload"},
    )
    class IotTopicPublishProperty:
        def __init__(
            self,
            *,
            mqtt_topic: builtins.str,
            payload: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Information required to publish the MQTT message through the AWS IoT message broker.

            :param mqtt_topic: The MQTT topic of the message. You can use a string expression that includes variables ( ``$variable.<variable-name>`` ) and input values ( ``$input.<input-name>.<path-to-datum>`` ) as the topic string.
            :param payload: You can configure the action payload when you publish a message to an AWS IoT Core topic.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iottopicpublish.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__d30f4f6153ab4d01554da299b5bfd08270ccbb3f4d5f2e10a8876f708adb8daf)
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
        ) -> typing.Optional[typing.Union["CfnAlarmModel.PayloadProperty", _IResolvable_a771d0ef]]:
            '''You can configure the action payload when you publish a message to an AWS IoT Core topic.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iottopicpublish.html#cfn-iotevents-alarmmodel-iottopicpublish-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.PayloadProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IotTopicPublishProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnAlarmModel.LambdaProperty",
        jsii_struct_bases=[],
        name_mapping={"function_arn": "functionArn", "payload": "payload"},
    )
    class LambdaProperty:
        def __init__(
            self,
            *,
            function_arn: builtins.str,
            payload: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Calls a Lambda function, passing in information about the detector model instance and the event that triggered the action.

            :param function_arn: The ARN of the Lambda function that is executed.
            :param payload: You can configure the action payload when you send a message to a Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-lambda.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__9bc617ea5eecc7c2f870f30ed590c15b8cfb7e30a871b8722320a009d74bf19d)
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
        ) -> typing.Optional[typing.Union["CfnAlarmModel.PayloadProperty", _IResolvable_a771d0ef]]:
            '''You can configure the action payload when you send a message to a Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-lambda.html#cfn-iotevents-alarmmodel-lambda-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.PayloadProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnAlarmModel.PayloadProperty",
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
                from monocdk import aws_iotevents as iotevents
                
                payload_property = iotevents.CfnAlarmModel.PayloadProperty(
                    content_expression="contentExpression",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e83f0bcba645b576e8b0f679bf8eb120b894cb26f6bd57c6b31a416eaaa55c68)
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
        jsii_type="monocdk.aws_iotevents.CfnAlarmModel.SimpleRuleProperty",
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
                from monocdk import aws_iotevents as iotevents
                
                simple_rule_property = iotevents.CfnAlarmModel.SimpleRuleProperty(
                    comparison_operator="comparisonOperator",
                    input_property="inputProperty",
                    threshold="threshold"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__38238b114d571c07a0278ac74c9927826577a307612915d912b10c53eb8e48a0)
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
        jsii_type="monocdk.aws_iotevents.CfnAlarmModel.SnsProperty",
        jsii_struct_bases=[],
        name_mapping={"target_arn": "targetArn", "payload": "payload"},
    )
    class SnsProperty:
        def __init__(
            self,
            *,
            target_arn: builtins.str,
            payload: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Information required to publish the Amazon SNS message.

            :param target_arn: The ARN of the Amazon SNS target where the message is sent.
            :param payload: You can configure the action payload when you send a message as an Amazon SNS push notification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-sns.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__37525278edd4b9720989e6018b5b4fe53472869326ab48f2d2d1167861e0a870)
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
        ) -> typing.Optional[typing.Union["CfnAlarmModel.PayloadProperty", _IResolvable_a771d0ef]]:
            '''You can configure the action payload when you send a message as an Amazon SNS push notification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-sns.html#cfn-iotevents-alarmmodel-sns-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.PayloadProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnAlarmModel.SqsProperty",
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
            payload: typing.Optional[typing.Union[typing.Union["CfnAlarmModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            use_base64: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__e42920d9c69b06500829d02b9b6156b2a6b606f35b89b6d9cf66bd6bc2264559)
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
        ) -> typing.Optional[typing.Union["CfnAlarmModel.PayloadProperty", _IResolvable_a771d0ef]]:
            '''You can configure the action payload when you send a message to an Amazon SQS queue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-sqs.html#cfn-iotevents-alarmmodel-sqs-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union["CfnAlarmModel.PayloadProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def use_base64(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Set this to TRUE if you want the data to be base-64 encoded before it is written to the queue.

            Otherwise, set this to FALSE.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-sqs.html#cfn-iotevents-alarmmodel-sqs-usebase64
            '''
            result = self._values.get("use_base64")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SqsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_iotevents.CfnAlarmModelProps",
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
        alarm_rule: typing.Union[typing.Union[CfnAlarmModel.AlarmRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        role_arn: builtins.str,
        alarm_capabilities: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.AlarmCapabilitiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        alarm_event_actions: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.AlarmEventActionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        alarm_model_description: typing.Optional[builtins.str] = None,
        alarm_model_name: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        severity: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            from monocdk import aws_iotevents as iotevents
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbda50935840a9092dc02e74659d967b56b7cafe139501d66a69d3b36de77890)
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
    ) -> typing.Union[CfnAlarmModel.AlarmRuleProperty, _IResolvable_a771d0ef]:
        '''Defines when your alarm is invoked.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-alarmrule
        '''
        result = self._values.get("alarm_rule")
        assert result is not None, "Required property 'alarm_rule' is missing"
        return typing.cast(typing.Union[CfnAlarmModel.AlarmRuleProperty, _IResolvable_a771d0ef], result)

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
    ) -> typing.Optional[typing.Union[CfnAlarmModel.AlarmCapabilitiesProperty, _IResolvable_a771d0ef]]:
        '''Contains the configuration information of alarm state changes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-alarmcapabilities
        '''
        result = self._values.get("alarm_capabilities")
        return typing.cast(typing.Optional[typing.Union[CfnAlarmModel.AlarmCapabilitiesProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def alarm_event_actions(
        self,
    ) -> typing.Optional[typing.Union[CfnAlarmModel.AlarmEventActionsProperty, _IResolvable_a771d0ef]]:
        '''Contains information about one or more alarm actions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-alarmeventactions
        '''
        result = self._values.get("alarm_event_actions")
        return typing.cast(typing.Optional[typing.Union[CfnAlarmModel.AlarmEventActionsProperty, _IResolvable_a771d0ef]], result)

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
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of key-value pairs that contain metadata for the alarm model.

        The tags help you manage the alarm model. For more information, see `Tagging your AWS IoT Events resources <https://docs.aws.amazon.com/iotevents/latest/developerguide/tagging-iotevents.html>`_ in the *AWS IoT Events Developer Guide* .

        You can create up to 50 tags for one alarm model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAlarmModelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnDetectorModel(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iotevents.CfnDetectorModel",
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
        from monocdk import aws_iotevents as iotevents
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        detector_model_definition: typing.Union[typing.Union["CfnDetectorModel.DetectorModelDefinitionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        role_arn: builtins.str,
        detector_model_description: typing.Optional[builtins.str] = None,
        detector_model_name: typing.Optional[builtins.str] = None,
        evaluation_method: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbdb1289d0fb5f082d64616bc7675cc0f446f19d2268dcd3151b55ab400db9c0)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba5ff28e61e446ec636e269b07d2b274f1ec2740651842382f757a64050a330b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f71b348d5b864eec84da0b6a0e2f3c29d6afd6a9314e1d12159f3719b060dc3d)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="detectorModelDefinition")
    def detector_model_definition(
        self,
    ) -> typing.Union["CfnDetectorModel.DetectorModelDefinitionProperty", _IResolvable_a771d0ef]:
        '''Information that defines how a detector operates.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-detectormodeldefinition
        '''
        return typing.cast(typing.Union["CfnDetectorModel.DetectorModelDefinitionProperty", _IResolvable_a771d0ef], jsii.get(self, "detectorModelDefinition"))

    @detector_model_definition.setter
    def detector_model_definition(
        self,
        value: typing.Union["CfnDetectorModel.DetectorModelDefinitionProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1884a4c2dc8139ac71fce533b53ce11f50a8d454d5ae3b76b25015b6b75d92c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbaa93d99534f7704e22958d063ef4153ac3cb9d266e87fb9f6e761303bc3c64)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8342c966991619769a329fd3eda4f8dc6a61626057274e5c2445da0a6544cba7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efcfa1c4f4dad1fa43c85a945e5158c870b5028d8e72786003d91b15597fda4b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fb412275cb971c101dd7e211a3221f17b9efbff11c3c9f0aa270b41c5a19ab0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__541d636b65115810770a71349f195d6f0f950cb98134c2d075eab92dfb19ecb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.ActionProperty",
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
            clear_timer: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.ClearTimerProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            dynamo_db: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.DynamoDBProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            dynamo_d_bv2: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.DynamoDBv2Property", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            firehose: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.FirehoseProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            iot_events: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.IotEventsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            iot_site_wise: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.IotSiteWiseProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            iot_topic_publish: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.IotTopicPublishProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            lambda_: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.LambdaProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            reset_timer: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.ResetTimerProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            set_timer: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.SetTimerProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            set_variable: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.SetVariableProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sns: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.SnsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sqs: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.SqsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__30e2bce1fe0cd77aae0a1e6fc46b095a511402771d452eb1e9e864867a4dea8e)
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
        ) -> typing.Optional[typing.Union["CfnDetectorModel.ClearTimerProperty", _IResolvable_a771d0ef]]:
            '''Information needed to clear the timer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-cleartimer
            '''
            result = self._values.get("clear_timer")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.ClearTimerProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def dynamo_db(
            self,
        ) -> typing.Optional[typing.Union["CfnDetectorModel.DynamoDBProperty", _IResolvable_a771d0ef]]:
            '''Writes to the DynamoDB table that you created.

            The default action payload contains all attribute-value pairs that have the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . One column of the DynamoDB table receives all attribute-value pairs in the payload that you specify. For more information, see `Actions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-event-actions.html>`_ in *AWS IoT Events Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-dynamodb
            '''
            result = self._values.get("dynamo_db")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.DynamoDBProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def dynamo_d_bv2(
            self,
        ) -> typing.Optional[typing.Union["CfnDetectorModel.DynamoDBv2Property", _IResolvable_a771d0ef]]:
            '''Writes to the DynamoDB table that you created.

            The default action payload contains all attribute-value pairs that have the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . A separate column of the DynamoDB table receives one attribute-value pair in the payload that you specify. For more information, see `Actions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-event-actions.html>`_ in *AWS IoT Events Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-dynamodbv2
            '''
            result = self._values.get("dynamo_d_bv2")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.DynamoDBv2Property", _IResolvable_a771d0ef]], result)

        @builtins.property
        def firehose(
            self,
        ) -> typing.Optional[typing.Union["CfnDetectorModel.FirehoseProperty", _IResolvable_a771d0ef]]:
            '''Sends information about the detector model instance and the event that triggered the action to an Amazon Kinesis Data Firehose delivery stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-firehose
            '''
            result = self._values.get("firehose")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.FirehoseProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def iot_events(
            self,
        ) -> typing.Optional[typing.Union["CfnDetectorModel.IotEventsProperty", _IResolvable_a771d0ef]]:
            '''Sends AWS IoT Events input, which passes information about the detector model instance and the event that triggered the action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-iotevents
            '''
            result = self._values.get("iot_events")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.IotEventsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def iot_site_wise(
            self,
        ) -> typing.Optional[typing.Union["CfnDetectorModel.IotSiteWiseProperty", _IResolvable_a771d0ef]]:
            '''Sends information about the detector model instance and the event that triggered the action to an asset property in AWS IoT SiteWise .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-iotsitewise
            '''
            result = self._values.get("iot_site_wise")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.IotSiteWiseProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def iot_topic_publish(
            self,
        ) -> typing.Optional[typing.Union["CfnDetectorModel.IotTopicPublishProperty", _IResolvable_a771d0ef]]:
            '''Publishes an MQTT message with the given topic to the AWS IoT message broker.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-iottopicpublish
            '''
            result = self._values.get("iot_topic_publish")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.IotTopicPublishProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def lambda_(
            self,
        ) -> typing.Optional[typing.Union["CfnDetectorModel.LambdaProperty", _IResolvable_a771d0ef]]:
            '''Calls a Lambda function, passing in information about the detector model instance and the event that triggered the action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-lambda
            '''
            result = self._values.get("lambda_")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.LambdaProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def reset_timer(
            self,
        ) -> typing.Optional[typing.Union["CfnDetectorModel.ResetTimerProperty", _IResolvable_a771d0ef]]:
            '''Information needed to reset the timer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-resettimer
            '''
            result = self._values.get("reset_timer")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.ResetTimerProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def set_timer(
            self,
        ) -> typing.Optional[typing.Union["CfnDetectorModel.SetTimerProperty", _IResolvable_a771d0ef]]:
            '''Information needed to set the timer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-settimer
            '''
            result = self._values.get("set_timer")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.SetTimerProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def set_variable(
            self,
        ) -> typing.Optional[typing.Union["CfnDetectorModel.SetVariableProperty", _IResolvable_a771d0ef]]:
            '''Sets a variable to a specified value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-setvariable
            '''
            result = self._values.get("set_variable")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.SetVariableProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sns(
            self,
        ) -> typing.Optional[typing.Union["CfnDetectorModel.SnsProperty", _IResolvable_a771d0ef]]:
            '''Sends an Amazon SNS message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-sns
            '''
            result = self._values.get("sns")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.SnsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sqs(
            self,
        ) -> typing.Optional[typing.Union["CfnDetectorModel.SqsProperty", _IResolvable_a771d0ef]]:
            '''Sends an Amazon SNS message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-sqs
            '''
            result = self._values.get("sqs")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.SqsProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.AssetPropertyTimestampProperty",
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
                from monocdk import aws_iotevents as iotevents
                
                asset_property_timestamp_property = iotevents.CfnDetectorModel.AssetPropertyTimestampProperty(
                    time_in_seconds="timeInSeconds",
                
                    # the properties below are optional
                    offset_in_nanos="offsetInNanos"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__58415476f4e5211c17a67b819b8192c4b4e1a7e6b591b7e25bab106c901ac1c8)
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
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.AssetPropertyValueProperty",
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
            value: typing.Union[typing.Union["CfnDetectorModel.AssetPropertyVariantProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            quality: typing.Optional[builtins.str] = None,
            timestamp: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.AssetPropertyTimestampProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__91dbd97594cd581829c75fadfa1039ecb4ce505f3e8c54d3e7e254c8df7163a1)
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
        ) -> typing.Union["CfnDetectorModel.AssetPropertyVariantProperty", _IResolvable_a771d0ef]:
            '''The value to send to an asset property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvalue.html#cfn-iotevents-detectormodel-assetpropertyvalue-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(typing.Union["CfnDetectorModel.AssetPropertyVariantProperty", _IResolvable_a771d0ef], result)

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
        ) -> typing.Optional[typing.Union["CfnDetectorModel.AssetPropertyTimestampProperty", _IResolvable_a771d0ef]]:
            '''The timestamp associated with the asset property value.

            The default is the current event time.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvalue.html#cfn-iotevents-detectormodel-assetpropertyvalue-timestamp
            '''
            result = self._values.get("timestamp")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.AssetPropertyTimestampProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetPropertyValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.AssetPropertyVariantProperty",
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
                from monocdk import aws_iotevents as iotevents
                
                asset_property_variant_property = iotevents.CfnDetectorModel.AssetPropertyVariantProperty(
                    boolean_value="booleanValue",
                    double_value="doubleValue",
                    integer_value="integerValue",
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__46daa12fc1ae4d34be03fce2ae8fbb3a96f7aef48bdd9477389f36b6bd44d945)
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
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.ClearTimerProperty",
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
                from monocdk import aws_iotevents as iotevents
                
                clear_timer_property = iotevents.CfnDetectorModel.ClearTimerProperty(
                    timer_name="timerName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db2e7f4fda95e3c7fbc0d9376950212cfb83c322970fc2fa38a216d63e26f1cb)
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
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.DetectorModelDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"initial_state_name": "initialStateName", "states": "states"},
    )
    class DetectorModelDefinitionProperty:
        def __init__(
            self,
            *,
            initial_state_name: builtins.str,
            states: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnDetectorModel.StateProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        ) -> None:
            '''Information that defines how a detector operates.

            :param initial_state_name: The state that is entered at the creation of each detector (instance).
            :param states: Information about the states of the detector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-detectormodeldefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__66859f5359ee29b1078fb1fc8c4404969ca38476d5ed6404cc4fe88fd67f2a8f)
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
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDetectorModel.StateProperty", _IResolvable_a771d0ef]]]:
            '''Information about the states of the detector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-detectormodeldefinition.html#cfn-iotevents-detectormodel-detectormodeldefinition-states
            '''
            result = self._values.get("states")
            assert result is not None, "Required property 'states' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDetectorModel.StateProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DetectorModelDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.DynamoDBProperty",
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
            payload: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__765b650dd5ee90a7c750be55b537c3bbe23bf921f158c5a2fe3c46eaf669ebc3)
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
        ) -> typing.Optional[typing.Union["CfnDetectorModel.PayloadProperty", _IResolvable_a771d0ef]]:
            '''Information needed to configure the payload.

            By default, AWS IoT Events generates a standard payload in JSON for any action. This action payload contains all attribute-value pairs that have the information about the detector model instance and the event triggered the action. To configure the action payload, you can use ``contentExpression`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.PayloadProperty", _IResolvable_a771d0ef]], result)

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
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.DynamoDBv2Property",
        jsii_struct_bases=[],
        name_mapping={"table_name": "tableName", "payload": "payload"},
    )
    class DynamoDBv2Property:
        def __init__(
            self,
            *,
            table_name: builtins.str,
            payload: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__0e02e819491bf01b0ae2af9b97e4c47198d13014a402c8a7375cc54e275f9a1a)
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
        ) -> typing.Optional[typing.Union["CfnDetectorModel.PayloadProperty", _IResolvable_a771d0ef]]:
            '''Information needed to configure the payload.

            By default, AWS IoT Events generates a standard payload in JSON for any action. This action payload contains all attribute-value pairs that have the information about the detector model instance and the event triggered the action. To configure the action payload, you can use ``contentExpression`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodbv2.html#cfn-iotevents-detectormodel-dynamodbv2-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.PayloadProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamoDBv2Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.EventProperty",
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
            actions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnDetectorModel.ActionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
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
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__b14d56b59ca224936868097631f52f49fd345a9ba63e01375bbf3903250ce495)
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
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDetectorModel.ActionProperty", _IResolvable_a771d0ef]]]]:
            '''The actions to be performed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-event.html#cfn-iotevents-detectormodel-event-actions
            '''
            result = self._values.get("actions")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDetectorModel.ActionProperty", _IResolvable_a771d0ef]]]], result)

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
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.FirehoseProperty",
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
            payload: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__de720b5e4aa44f00c3480d9d6fa7b92efc58bf123d8a17d540dd1677b6adfd84)
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
        ) -> typing.Optional[typing.Union["CfnDetectorModel.PayloadProperty", _IResolvable_a771d0ef]]:
            '''You can configure the action payload when you send a message to an Amazon Kinesis Data Firehose delivery stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-firehose.html#cfn-iotevents-detectormodel-firehose-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.PayloadProperty", _IResolvable_a771d0ef]], result)

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
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.IotEventsProperty",
        jsii_struct_bases=[],
        name_mapping={"input_name": "inputName", "payload": "payload"},
    )
    class IotEventsProperty:
        def __init__(
            self,
            *,
            input_name: builtins.str,
            payload: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Sends an AWS IoT Events input, passing in information about the detector model instance and the event that triggered the action.

            :param input_name: The name of the AWS IoT Events input where the data is sent.
            :param payload: You can configure the action payload when you send a message to an AWS IoT Events input.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotevents.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__1c18b4bbf49aeafd47c5103d506ba087f7bb55d3a2d92cc73b56b5ed3f418111)
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
        ) -> typing.Optional[typing.Union["CfnDetectorModel.PayloadProperty", _IResolvable_a771d0ef]]:
            '''You can configure the action payload when you send a message to an AWS IoT Events input.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotevents.html#cfn-iotevents-detectormodel-iotevents-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.PayloadProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IotEventsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.IotSiteWiseProperty",
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
            property_value: typing.Union[typing.Union["CfnDetectorModel.AssetPropertyValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
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
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__e314dec90319ab6330fdf50d0cd36560054ccc5b8f0c75173d108c91622ec5bb)
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
        ) -> typing.Union["CfnDetectorModel.AssetPropertyValueProperty", _IResolvable_a771d0ef]:
            '''The value to send to the asset property.

            This value contains timestamp, quality, and value (TQV) information.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotsitewise.html#cfn-iotevents-detectormodel-iotsitewise-propertyvalue
            '''
            result = self._values.get("property_value")
            assert result is not None, "Required property 'property_value' is missing"
            return typing.cast(typing.Union["CfnDetectorModel.AssetPropertyValueProperty", _IResolvable_a771d0ef], result)

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
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.IotTopicPublishProperty",
        jsii_struct_bases=[],
        name_mapping={"mqtt_topic": "mqttTopic", "payload": "payload"},
    )
    class IotTopicPublishProperty:
        def __init__(
            self,
            *,
            mqtt_topic: builtins.str,
            payload: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Information required to publish the MQTT message through the AWS IoT message broker.

            :param mqtt_topic: The MQTT topic of the message. You can use a string expression that includes variables ( ``$variable.<variable-name>`` ) and input values ( ``$input.<input-name>.<path-to-datum>`` ) as the topic string.
            :param payload: You can configure the action payload when you publish a message to an AWS IoT Core topic.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iottopicpublish.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__c2c3ebb624c99aef373f04785e49a31de2f9e416a494acaac4292bba694d6de1)
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
        ) -> typing.Optional[typing.Union["CfnDetectorModel.PayloadProperty", _IResolvable_a771d0ef]]:
            '''You can configure the action payload when you publish a message to an AWS IoT Core topic.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iottopicpublish.html#cfn-iotevents-detectormodel-iottopicpublish-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.PayloadProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IotTopicPublishProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.LambdaProperty",
        jsii_struct_bases=[],
        name_mapping={"function_arn": "functionArn", "payload": "payload"},
    )
    class LambdaProperty:
        def __init__(
            self,
            *,
            function_arn: builtins.str,
            payload: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Calls a Lambda function, passing in information about the detector model instance and the event that triggered the action.

            :param function_arn: The ARN of the Lambda function that is executed.
            :param payload: You can configure the action payload when you send a message to a Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-lambda.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__9684c316eefbb054da20f62b47b3364ef10d33add40011256966aecab149d513)
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
        ) -> typing.Optional[typing.Union["CfnDetectorModel.PayloadProperty", _IResolvable_a771d0ef]]:
            '''You can configure the action payload when you send a message to a Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-lambda.html#cfn-iotevents-detectormodel-lambda-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.PayloadProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.OnEnterProperty",
        jsii_struct_bases=[],
        name_mapping={"events": "events"},
    )
    class OnEnterProperty:
        def __init__(
            self,
            *,
            events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnDetectorModel.EventProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''When entering this state, perform these ``actions`` if the ``condition`` is TRUE.

            :param events: Specifies the actions that are performed when the state is entered and the ``condition`` is ``TRUE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-onenter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__1f20db8cfce173ff75e3f8322eb91b32cc1401b580d9c2e12dfb0747992351fa)
                check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if events is not None:
                self._values["events"] = events

        @builtins.property
        def events(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDetectorModel.EventProperty", _IResolvable_a771d0ef]]]]:
            '''Specifies the actions that are performed when the state is entered and the ``condition`` is ``TRUE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-onenter.html#cfn-iotevents-detectormodel-onenter-events
            '''
            result = self._values.get("events")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDetectorModel.EventProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnEnterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.OnExitProperty",
        jsii_struct_bases=[],
        name_mapping={"events": "events"},
    )
    class OnExitProperty:
        def __init__(
            self,
            *,
            events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnDetectorModel.EventProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''When exiting this state, perform these ``actions`` if the specified ``condition`` is ``TRUE`` .

            :param events: Specifies the ``actions`` that are performed when the state is exited and the ``condition`` is ``TRUE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-onexit.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__12722923002267c0c006cf1c8063f0f263a521ab1fd1b9bfec62d920b7989b4e)
                check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if events is not None:
                self._values["events"] = events

        @builtins.property
        def events(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDetectorModel.EventProperty", _IResolvable_a771d0ef]]]]:
            '''Specifies the ``actions`` that are performed when the state is exited and the ``condition`` is ``TRUE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-onexit.html#cfn-iotevents-detectormodel-onexit-events
            '''
            result = self._values.get("events")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDetectorModel.EventProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnExitProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.OnInputProperty",
        jsii_struct_bases=[],
        name_mapping={"events": "events", "transition_events": "transitionEvents"},
    )
    class OnInputProperty:
        def __init__(
            self,
            *,
            events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnDetectorModel.EventProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            transition_events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnDetectorModel.TransitionEventProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''Specifies the actions performed when the ``condition`` evaluates to TRUE.

            :param events: Specifies the actions performed when the ``condition`` evaluates to TRUE.
            :param transition_events: Specifies the actions performed, and the next state entered, when a ``condition`` evaluates to TRUE.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-oninput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__d58ace0464a2b6c8630a01e1b4a9c04c8ba7db2b33d3e6163924c90fbdbd0c5b)
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
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDetectorModel.EventProperty", _IResolvable_a771d0ef]]]]:
            '''Specifies the actions performed when the ``condition`` evaluates to TRUE.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-oninput.html#cfn-iotevents-detectormodel-oninput-events
            '''
            result = self._values.get("events")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDetectorModel.EventProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def transition_events(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDetectorModel.TransitionEventProperty", _IResolvable_a771d0ef]]]]:
            '''Specifies the actions performed, and the next state entered, when a ``condition`` evaluates to TRUE.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-oninput.html#cfn-iotevents-detectormodel-oninput-transitionevents
            '''
            result = self._values.get("transition_events")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDetectorModel.TransitionEventProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.PayloadProperty",
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
                from monocdk import aws_iotevents as iotevents
                
                payload_property = iotevents.CfnDetectorModel.PayloadProperty(
                    content_expression="contentExpression",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c0cd0cb3751a1ce11cd3d2c57c970046b10f9ce423d08422465e44f50ffb3492)
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
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.ResetTimerProperty",
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
                from monocdk import aws_iotevents as iotevents
                
                reset_timer_property = iotevents.CfnDetectorModel.ResetTimerProperty(
                    timer_name="timerName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ec125d7211fff7aa0b7d0e338fc5491087d617575057ade2be2ec02eeedcf8b4)
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
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.SetTimerProperty",
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
                from monocdk import aws_iotevents as iotevents
                
                set_timer_property = iotevents.CfnDetectorModel.SetTimerProperty(
                    timer_name="timerName",
                
                    # the properties below are optional
                    duration_expression="durationExpression",
                    seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a29889c1ace504dbdcdba1eddc8628ce3811416fdde5123ad8ff3020fc633f08)
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
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.SetVariableProperty",
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
                from monocdk import aws_iotevents as iotevents
                
                set_variable_property = iotevents.CfnDetectorModel.SetVariableProperty(
                    value="value",
                    variable_name="variableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__39f8a7a8dff4c1ef4cac00bc3936710a995692c474b569e64ab27f53a78e53ec)
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
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.SnsProperty",
        jsii_struct_bases=[],
        name_mapping={"target_arn": "targetArn", "payload": "payload"},
    )
    class SnsProperty:
        def __init__(
            self,
            *,
            target_arn: builtins.str,
            payload: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Information required to publish the Amazon SNS message.

            :param target_arn: The ARN of the Amazon SNS target where the message is sent.
            :param payload: You can configure the action payload when you send a message as an Amazon SNS push notification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sns.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__7681907fa4aee84717d34242c6974c4b260b29efa77afcf913470b8e46634ae8)
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
        ) -> typing.Optional[typing.Union["CfnDetectorModel.PayloadProperty", _IResolvable_a771d0ef]]:
            '''You can configure the action payload when you send a message as an Amazon SNS push notification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sns.html#cfn-iotevents-detectormodel-sns-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.PayloadProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.SqsProperty",
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
            payload: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.PayloadProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            use_base64: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__f1b04f3c8765ad06a75c0ba0d367b24368e06453fc5c477c240b01dad7c0a4a5)
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
        ) -> typing.Optional[typing.Union["CfnDetectorModel.PayloadProperty", _IResolvable_a771d0ef]]:
            '''You can configure the action payload when you send a message to an Amazon SQS queue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sqs.html#cfn-iotevents-detectormodel-sqs-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.PayloadProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def use_base64(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Set this to TRUE if you want the data to be base-64 encoded before it is written to the queue.

            Otherwise, set this to FALSE.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sqs.html#cfn-iotevents-detectormodel-sqs-usebase64
            '''
            result = self._values.get("use_base64")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SqsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.StateProperty",
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
            on_enter: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.OnEnterProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            on_exit: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.OnExitProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            on_input: typing.Optional[typing.Union[typing.Union["CfnDetectorModel.OnInputProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__1fcd1a66b115ad806079e97994b07e7b3411e1dacb5fa008409f8ce443f1cc71)
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
        ) -> typing.Optional[typing.Union["CfnDetectorModel.OnEnterProperty", _IResolvable_a771d0ef]]:
            '''When entering this state, perform these ``actions`` if the ``condition`` is TRUE.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-state.html#cfn-iotevents-detectormodel-state-onenter
            '''
            result = self._values.get("on_enter")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.OnEnterProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def on_exit(
            self,
        ) -> typing.Optional[typing.Union["CfnDetectorModel.OnExitProperty", _IResolvable_a771d0ef]]:
            '''When exiting this state, perform these ``actions`` if the specified ``condition`` is ``TRUE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-state.html#cfn-iotevents-detectormodel-state-onexit
            '''
            result = self._values.get("on_exit")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.OnExitProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def on_input(
            self,
        ) -> typing.Optional[typing.Union["CfnDetectorModel.OnInputProperty", _IResolvable_a771d0ef]]:
            '''When an input is received and the ``condition`` is TRUE, perform the specified ``actions`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-state.html#cfn-iotevents-detectormodel-state-oninput
            '''
            result = self._values.get("on_input")
            return typing.cast(typing.Optional[typing.Union["CfnDetectorModel.OnInputProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnDetectorModel.TransitionEventProperty",
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
            actions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnDetectorModel.ActionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
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
                from monocdk import aws_iotevents as iotevents
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__162c185f80f628eee71fedbdb51893ff66e9e6baa28040b9e84fe25264f89e2a)
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
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDetectorModel.ActionProperty", _IResolvable_a771d0ef]]]]:
            '''The actions to be performed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-transitionevent.html#cfn-iotevents-detectormodel-transitionevent-actions
            '''
            result = self._values.get("actions")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDetectorModel.ActionProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TransitionEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_iotevents.CfnDetectorModelProps",
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
        detector_model_definition: typing.Union[typing.Union[CfnDetectorModel.DetectorModelDefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        role_arn: builtins.str,
        detector_model_description: typing.Optional[builtins.str] = None,
        detector_model_name: typing.Optional[builtins.str] = None,
        evaluation_method: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            from monocdk import aws_iotevents as iotevents
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbf081acf6d5045fabb59bf7f5e0ae811e32d3091782126a2322417af75f5c62)
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
    ) -> typing.Union[CfnDetectorModel.DetectorModelDefinitionProperty, _IResolvable_a771d0ef]:
        '''Information that defines how a detector operates.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-detectormodeldefinition
        '''
        result = self._values.get("detector_model_definition")
        assert result is not None, "Required property 'detector_model_definition' is missing"
        return typing.cast(typing.Union[CfnDetectorModel.DetectorModelDefinitionProperty, _IResolvable_a771d0ef], result)

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
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDetectorModelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnInput(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iotevents.CfnInput",
):
    '''A CloudFormation ``AWS::IoTEvents::Input``.

    The AWS::IoTEvents::Input resource creates an input. To monitor your devices and processes, they must have a way to get telemetry data into AWS IoT Events . This is done by sending messages as *inputs* to AWS IoT Events . For more information, see `How to Use AWS IoT Events <https://docs.aws.amazon.com/iotevents/latest/developerguide/how-to-use-iotevents.html>`_ in the *AWS IoT Events Developer Guide* .

    :cloudformationResource: AWS::IoTEvents::Input
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iotevents as iotevents
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        input_definition: typing.Union[typing.Union["CfnInput.InputDefinitionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        input_description: typing.Optional[builtins.str] = None,
        input_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef5aa809de55ed0610206e2d687545885d6443313a73b31e379f28180f074a0a)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a1d74b79c7f1aec3ad406b8f26c8da50d7066110d302446345d370f948bb3ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ac1ab2d9f1b39d6982f7072f46fd62820a25e06d90430a7ad194c204629ecf8)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="inputDefinition")
    def input_definition(
        self,
    ) -> typing.Union["CfnInput.InputDefinitionProperty", _IResolvable_a771d0ef]:
        '''The definition of the input.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-inputdefinition
        '''
        return typing.cast(typing.Union["CfnInput.InputDefinitionProperty", _IResolvable_a771d0ef], jsii.get(self, "inputDefinition"))

    @input_definition.setter
    def input_definition(
        self,
        value: typing.Union["CfnInput.InputDefinitionProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a22cc2052ecb63941a580f1063be2b0dfd0ff197af9b0b9191c11f4d68c87f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1252aa877157bbd7049243ad7caa78d4fdd6dc3c5283ad2e542a98da212e359)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97fd2c1c7e85c7c649ce55fbde52fc60471612e5a6f65f54fc79c41aff9d6df2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_iotevents.CfnInput.AttributeProperty",
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
                from monocdk import aws_iotevents as iotevents
                
                attribute_property = iotevents.CfnInput.AttributeProperty(
                    json_path="jsonPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b57031c3f18bcbb8d7f6ca6f09445c05bc7e256c370371e129e8e47616faec2c)
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
        jsii_type="monocdk.aws_iotevents.CfnInput.InputDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"attributes": "attributes"},
    )
    class InputDefinitionProperty:
        def __init__(
            self,
            *,
            attributes: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnInput.AttributeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        ) -> None:
            '''The definition of the input.

            :param attributes: The attributes from the JSON payload that are made available by the input. Inputs are derived from messages sent to the AWS IoT Events system using ``BatchPutMessage`` . Each such message contains a JSON payload, and those attributes (and their paired values) specified here are available for use in the ``condition`` expressions used by detectors that monitor this input.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-input-inputdefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotevents as iotevents
                
                input_definition_property = iotevents.CfnInput.InputDefinitionProperty(
                    attributes=[iotevents.CfnInput.AttributeProperty(
                        json_path="jsonPath"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4d756e737a6a9bdaaf2819b9c6c86e67820ea6c7bf81b0cfc354dd3ae4eacf4a)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "attributes": attributes,
            }

        @builtins.property
        def attributes(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnInput.AttributeProperty", _IResolvable_a771d0ef]]]:
            '''The attributes from the JSON payload that are made available by the input.

            Inputs are derived from messages sent to the AWS IoT Events system using ``BatchPutMessage`` . Each such message contains a JSON payload, and those attributes (and their paired values) specified here are available for use in the ``condition`` expressions used by detectors that monitor this input.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-input-inputdefinition.html#cfn-iotevents-input-inputdefinition-attributes
            '''
            result = self._values.get("attributes")
            assert result is not None, "Required property 'attributes' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnInput.AttributeProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_iotevents.CfnInputProps",
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
        input_definition: typing.Union[typing.Union[CfnInput.InputDefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        input_description: typing.Optional[builtins.str] = None,
        input_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            from monocdk import aws_iotevents as iotevents
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__65f89c1939fb85ff5429362c39134351a5602b07057ac791fba1e816fed71c25)
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
    ) -> typing.Union[CfnInput.InputDefinitionProperty, _IResolvable_a771d0ef]:
        '''The definition of the input.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-inputdefinition
        '''
        result = self._values.get("input_definition")
        assert result is not None, "Required property 'input_definition' is missing"
        return typing.cast(typing.Union[CfnInput.InputDefinitionProperty, _IResolvable_a771d0ef], result)

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
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInputProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_iotevents.DetectorModelProps",
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
        role: typing.Optional[_IRole_59af6f50] = None,
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

            import monocdk as iotevents
            import monocdk as actions
            import monocdk as lambda_
            
            # func: lambda.IFunction
            
            
            input = iotevents.Input(self, "MyInput",
                input_name="my_input",  # optional
                attribute_json_paths=["payload.deviceId", "payload.temperature"]
            )
            
            warm_state = iotevents.State(
                state_name="warm",
                on_enter=[iotevents.aws_iotevents.Event(
                    event_name="test-enter-event",
                    condition=iotevents.Expression.current_input(input),
                    actions=[actions.LambdaInvokeAction(func)]
                )],
                on_input=[iotevents.aws_iotevents.Event( # optional
                    event_name="test-input-event",
                    actions=[actions.LambdaInvokeAction(func)])],
                on_exit=[iotevents.aws_iotevents.Event( # optional
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdd48144b7dc9569116a2fa81f4c10b4cf4192ce4390fa794b4301e87f5e767f)
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
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The role that grants permission to AWS IoT Events to perform its operations.

        :default: - a role will be created with default permissions

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DetectorModelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_iotevents.Event",
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
            from monocdk import aws_iotevents as iotevents
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__92b79b241c7a064cd0939d018c3b7d72a8999872d686b40bc0d7810ff341efc4)
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


@jsii.enum(jsii_type="monocdk.aws_iotevents.EventEvaluation")
class EventEvaluation(enum.Enum):
    '''(experimental) Information about the order in which events are evaluated and how actions are executed.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as iotevents
        import monocdk as actions
        import monocdk as lambda_
        
        # func: lambda.IFunction
        
        
        input = iotevents.Input(self, "MyInput",
            input_name="my_input",  # optional
            attribute_json_paths=["payload.deviceId", "payload.temperature"]
        )
        
        warm_state = iotevents.State(
            state_name="warm",
            on_enter=[iotevents.aws_iotevents.Event(
                event_name="test-enter-event",
                condition=iotevents.Expression.current_input(input),
                actions=[actions.LambdaInvokeAction(func)]
            )],
            on_input=[iotevents.aws_iotevents.Event( # optional
                event_name="test-input-event",
                actions=[actions.LambdaInvokeAction(func)])],
            on_exit=[iotevents.aws_iotevents.Event( # optional
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
    jsii_type="monocdk.aws_iotevents.Expression",
):
    '''(experimental) Expression for events in Detector Model state.

    :see: https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Example automatically generated from non-compiling source. May contain errors.
        import monocdk as iotevents
        import monocdk as actions
        
        # input: iotevents.IInput
        
        
        state = iotevents.State(
            state_name="MyState",
            on_enter=[iotevents.aws_iotevents.Event(
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bc712dc3dba960b89e11dd0be43d835de974be4ffbb38a03f1a30ad60592bb9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05fb7b5983e5cac7e39ec81cb0b77596494d0fbd002d2697f8ef7b3b1af44999)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79718ac5cbbe2ce56ca114b4f4157f3beef320a29fe1805cd832d23ac09e8675)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecc11603296f80d784d556c14ce2090443676b1a71b8ffc29b1a7dd415b78f44)
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
            type_hints = typing.get_type_hints(_typecheckingstub__448cf29e4d4d89e9746a4ea0bf4b8d4dea6a9083ef7910b5583d50d5b909f0b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ecb4a311a64e667a4982c94996e1944b499e2488dd5a1081b6ca54a76003552)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3b9c08f86c74455b35cc063f0c558a292da6c5f047e8b3a87f273961921e026)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09df8314ad56ef37f0e1827de7ee4f2d96c7a00c979f59db686d648c675669bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90dc25a15be155be64d350bb2af87284608b16917b3455e2522613ee0778dd1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__700901c21f28bf8aa913e84b37d9dad894697f809ad1f180e5cb9e197d806fdc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d747908502a1ad500cb271688f0c5e0297f1261c92f4ab16ed1f4610fc7940f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73ba300fa422c65f84f188db530fe6f69af2040f046d7c1378173bd4a134eea3)
            check_type(argname="argument parent_priority", value=parent_priority, expected_type=type_hints["parent_priority"])
        return typing.cast(builtins.str, jsii.invoke(self, "evaluate", [parent_priority]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Expression).__jsii_proxy_class__ = lambda : _ExpressionProxy


@jsii.interface(jsii_type="monocdk.aws_iotevents.IAction")
class IAction(typing_extensions.Protocol):
    '''(experimental) An abstract action for DetectorModel.

    :stability: experimental
    '''

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        role: _IRole_59af6f50,
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

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_iotevents.IAction"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        role: _IRole_59af6f50,
    ) -> ActionConfig:
        '''(experimental) Returns the AWS IoT Events action specification.

        :param scope: -
        :param role: (experimental) The IAM role assumed by IoT Events to perform the action.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ce27fdc532b62829b75239b068a8ef8fbfdd2ae9d377bcbe3df3d4274f450e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        options = ActionBindOptions(role=role)

        return typing.cast(ActionConfig, jsii.invoke(self, "bind", [scope, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAction).__jsii_proxy_class__ = lambda : _IActionProxy


@jsii.interface(jsii_type="monocdk.aws_iotevents.IDetectorModel")
class IDetectorModel(_IResource_8c1dbbbd, typing_extensions.Protocol):
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
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) Represents an AWS IoT Events detector model.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_iotevents.IDetectorModel"

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


@jsii.interface(jsii_type="monocdk.aws_iotevents.IInput")
class IInput(_IResource_8c1dbbbd, typing_extensions.Protocol):
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
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the indicated permissions on this input to the given IAM principal (Role/Group/User).

        :param grantee: the principal.
        :param actions: the set of actions to allow (i.e. "iotevents:BatchPutMessage").

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions on this input and its contents to an IAM principal (Role/Group/User).

        :param grantee: the principal.

        :stability: experimental
        '''
        ...


class _IInputProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) Represents an AWS IoT Events input.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_iotevents.IInput"

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
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the indicated permissions on this input to the given IAM principal (Role/Group/User).

        :param grantee: the principal.
        :param actions: the set of actions to allow (i.e. "iotevents:BatchPutMessage").

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00e34bff62550c821f4a102db7c420193f1d8ed154c3e2be8e302d1b90ec0843)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions on this input and its contents to an IAM principal (Role/Group/User).

        :param grantee: the principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1f27802114bc2027bc73d322322e8b25260fe0ea37914db7553da801936ccf3)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantWrite", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IInput).__jsii_proxy_class__ = lambda : _IInputProxy


@jsii.implements(IInput)
class Input(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iotevents.Input",
):
    '''(experimental) Defines an AWS IoT Events input in this stack.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as iotevents
        import monocdk as actions
        import monocdk as lambda_
        
        # func: lambda.IFunction
        
        
        input = iotevents.Input(self, "MyInput",
            input_name="my_input",  # optional
            attribute_json_paths=["payload.deviceId", "payload.temperature"]
        )
        
        warm_state = iotevents.State(
            state_name="warm",
            on_enter=[iotevents.aws_iotevents.Event(
                event_name="test-enter-event",
                condition=iotevents.Expression.current_input(input),
                actions=[actions.LambdaInvokeAction(func)]
            )],
            on_input=[iotevents.aws_iotevents.Event( # optional
                event_name="test-input-event",
                actions=[actions.LambdaInvokeAction(func)])],
            on_exit=[iotevents.aws_iotevents.Event( # optional
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed3031091c350af10609eaf9f4a82e69341836842aa0f2497ec90ac221859d96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5eed37747b2db6d63ffcd446457d2d0f38d1fd74645612af86a24365d61c9f43)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument input_name", value=input_name, expected_type=type_hints["input_name"])
        return typing.cast(IInput, jsii.sinvoke(cls, "fromInputName", [scope, id, input_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the indicated permissions on this input to the given IAM principal (Role/Group/User).

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8456138490e1818a90738f49544ad45a6321144a3ffcc0a99e6ecfb6a49855ae)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions on this input and its contents to an IAM principal (Role/Group/User).

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__823afcc1a49d2bb91fdd24f35c5d10fa7a2cab840c8868f14886ae03bd4fbbaa)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantWrite", [grantee]))

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
    jsii_type="monocdk.aws_iotevents.InputProps",
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

            import monocdk as iotevents
            import monocdk as actions
            import monocdk as lambda_
            
            # func: lambda.IFunction
            
            
            input = iotevents.Input(self, "MyInput",
                input_name="my_input",  # optional
                attribute_json_paths=["payload.deviceId", "payload.temperature"]
            )
            
            warm_state = iotevents.State(
                state_name="warm",
                on_enter=[iotevents.aws_iotevents.Event(
                    event_name="test-enter-event",
                    condition=iotevents.Expression.current_input(input),
                    actions=[actions.LambdaInvokeAction(func)]
                )],
                on_input=[iotevents.aws_iotevents.Event( # optional
                    event_name="test-input-event",
                    actions=[actions.LambdaInvokeAction(func)])],
                on_exit=[iotevents.aws_iotevents.Event( # optional
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
            type_hints = typing.get_type_hints(_typecheckingstub__7afd2074a55c65cbb7010d5b3bd086844fe5a1793d2999178949958925278cb5)
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


class State(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_iotevents.State"):
    '''(experimental) Defines a state of a detector.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Example automatically generated from non-compiling source. May contain errors.
        import monocdk as iotevents
        import monocdk as actions
        
        # input: iotevents.IInput
        
        
        state = iotevents.State(
            state_name="MyState",
            on_enter=[iotevents.aws_iotevents.Event(
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd2c4054123c78e6661909d294ab8615528818d1b07fbcbcac927b51d554d81a)
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
    jsii_type="monocdk.aws_iotevents.StateProps",
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
            import monocdk as iotevents
            import monocdk as actions
            
            # input: iotevents.IInput
            
            
            state = iotevents.State(
                state_name="MyState",
                on_enter=[iotevents.aws_iotevents.Event(
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9fdde7f3a019c1bac662f35db5759679d5df06cdb9b54ebbbcd16e6e73f3235)
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
    jsii_type="monocdk.aws_iotevents.TransitionOptions",
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

            import monocdk as iotevents
            import monocdk as actions
            import monocdk as lambda_
            
            # func: lambda.IFunction
            
            
            input = iotevents.Input(self, "MyInput",
                input_name="my_input",  # optional
                attribute_json_paths=["payload.deviceId", "payload.temperature"]
            )
            
            warm_state = iotevents.State(
                state_name="warm",
                on_enter=[iotevents.aws_iotevents.Event(
                    event_name="test-enter-event",
                    condition=iotevents.Expression.current_input(input),
                    actions=[actions.LambdaInvokeAction(func)]
                )],
                on_input=[iotevents.aws_iotevents.Event( # optional
                    event_name="test-input-event",
                    actions=[actions.LambdaInvokeAction(func)])],
                on_exit=[iotevents.aws_iotevents.Event( # optional
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
            type_hints = typing.get_type_hints(_typecheckingstub__80b1676412ccaf7f3a15c9e7b613d67687a991510c21f8c803f754e1c507957b)
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
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iotevents.DetectorModel",
):
    '''(experimental) Defines an AWS IoT Events detector model in this stack.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as iotevents
        import monocdk as actions
        import monocdk as lambda_
        
        # func: lambda.IFunction
        
        
        input = iotevents.Input(self, "MyInput",
            input_name="my_input",  # optional
            attribute_json_paths=["payload.deviceId", "payload.temperature"]
        )
        
        warm_state = iotevents.State(
            state_name="warm",
            on_enter=[iotevents.aws_iotevents.Event(
                event_name="test-enter-event",
                condition=iotevents.Expression.current_input(input),
                actions=[actions.LambdaInvokeAction(func)]
            )],
            on_input=[iotevents.aws_iotevents.Event( # optional
                event_name="test-input-event",
                actions=[actions.LambdaInvokeAction(func)])],
            on_exit=[iotevents.aws_iotevents.Event( # optional
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
        role: typing.Optional[_IRole_59af6f50] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a658a6836e212adc207ef6570785abc2804ca86e25dc97ba0912b6a03448154)
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
            type_hints = typing.get_type_hints(_typecheckingstub__202a828c7cf6b9f83a91661d04229cc70e3f8e1810585590ab17556eccfbe7fa)
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

def _typecheckingstub__5f505628cd6253804a698aab6faedb360100aea82b67ccb476052748e631702a(
    *,
    role: _IRole_59af6f50,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79b4b2fdb4ca2ca770997c81df82d8d663d25bfc54d96c4d146d045a297e3b64(
    *,
    configuration: typing.Union[CfnDetectorModel.ActionProperty, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7534c9d68936e1c392dfb05008475157f303eea28ecb6c22480714aaa7892bf(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    alarm_rule: typing.Union[typing.Union[CfnAlarmModel.AlarmRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    role_arn: builtins.str,
    alarm_capabilities: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.AlarmCapabilitiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    alarm_event_actions: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.AlarmEventActionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    alarm_model_description: typing.Optional[builtins.str] = None,
    alarm_model_name: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    severity: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8259b996358635cc0c2736e4ea45cb49188380c97914087547bfeb7cf6b60185(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__446fdcf1fbc6ce4e83f9368f59cb3d103c24467c788c19129de2e51b5867a5c8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5a7944cb33d7dce7e34ed9c94ed425f2e91a2ef2f3ed78b7bda59bc90a0ef0e(
    value: typing.Union[CfnAlarmModel.AlarmRuleProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b7c40804a7e6801af108eaadb7c60cfdef4b74344ba3233b326b7a163268c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b878d772bd0873b3f2cd2483fe5c0ff9fbbb63afcfab434ea07ccefd836ef43(
    value: typing.Optional[typing.Union[CfnAlarmModel.AlarmCapabilitiesProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46684fade78a3ded88581d5c9450e50431e0e31b9502dbb9063f4b68c17a2450(
    value: typing.Optional[typing.Union[CfnAlarmModel.AlarmEventActionsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8dc6aa08419411ed0c2b4c6559168d4c5bf3ef72edb80da33a2c6aa1c1523a8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85508bcdc7953fa9de42f96203bf90c0f422f1f4184f9d7a76abeecacf48871(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e5fd02e299f8621a7f87089115c6cfecd55c2993a2dd8879d9d15ffbaeb7c1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a348df024311f52e40b249d0481a418788788239c0a73f00aa04bb49710a10d(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d9e888195d965759839d49913adbff9999e0139d138df3e53d2427d2c5adc98(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee1d6f8df8dba71c094c18cde82ecf0c2a33baa4e6846ceca64a316c2ad2b2c(
    *,
    dynamo_db: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.DynamoDBProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    dynamo_d_bv2: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.DynamoDBv2Property, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    firehose: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.FirehoseProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    iot_events: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.IotEventsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    iot_site_wise: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.IotSiteWiseProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    iot_topic_publish: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.IotTopicPublishProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    lambda_: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.LambdaProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sns: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.SnsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sqs: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.SqsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af8cba49d23702bc0fd211ed9fa32dc62c91496b424333554331a0476f082d55(
    *,
    acknowledge_flow: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.AcknowledgeFlowProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    initialization_configuration: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.InitializationConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42dbc3d1726f37254888dc63d800917aeb2ea78249e87c5007e30b8d4bb932d9(
    *,
    alarm_actions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAlarmModel.AlarmActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c3d326845bfad3fde5a49c444ebfcb275ef393654b1373eea5e9d2629c3ecc0(
    *,
    simple_rule: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.SimpleRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c8697800c5a0580751eeae7f3cb2dd86767b37d250cb22cdce580eb1bc01100(
    *,
    time_in_seconds: builtins.str,
    offset_in_nanos: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d29bba68e1311bdcaedc8caa6b95a96f6e6c5836463aaa71257003e009a792(
    *,
    value: typing.Union[typing.Union[CfnAlarmModel.AssetPropertyVariantProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    quality: typing.Optional[builtins.str] = None,
    timestamp: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.AssetPropertyTimestampProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ff5d722da871984b1680dd373c312d836657e3bc72e6f954d79077542c56d60(
    *,
    boolean_value: typing.Optional[builtins.str] = None,
    double_value: typing.Optional[builtins.str] = None,
    integer_value: typing.Optional[builtins.str] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec5c92107587ba507361d1202e1bd17939a41d35cd1190095f495ad6d372e34e(
    *,
    hash_key_field: builtins.str,
    hash_key_value: builtins.str,
    table_name: builtins.str,
    hash_key_type: typing.Optional[builtins.str] = None,
    operation: typing.Optional[builtins.str] = None,
    payload: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    payload_field: typing.Optional[builtins.str] = None,
    range_key_field: typing.Optional[builtins.str] = None,
    range_key_type: typing.Optional[builtins.str] = None,
    range_key_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56ac3206b191c481daeab544a1cb989799865da2e1881ea4883c07875b3aa95b(
    *,
    table_name: builtins.str,
    payload: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eda6a59407afd6eea06bd6e8603e6aa58281533dc1146fd1412be66d877f2fc(
    *,
    delivery_stream_name: builtins.str,
    payload: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    separator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c58a201ea33c5bd1bb42192a2a04450f00c7a00f5d57cf7aa961cf10d966112(
    *,
    disabled_on_initialization: typing.Union[builtins.bool, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a7222cab72c17189d6a4599f1d66740b90f8f11ef80faa8a4c69fc613c00f6(
    *,
    input_name: builtins.str,
    payload: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62ff5536e20d1cad7b1e02121aa4f26d58de6cddb7d9f693d44a6b39ddea8008(
    *,
    asset_id: typing.Optional[builtins.str] = None,
    entry_id: typing.Optional[builtins.str] = None,
    property_alias: typing.Optional[builtins.str] = None,
    property_id: typing.Optional[builtins.str] = None,
    property_value: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.AssetPropertyValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30f4f6153ab4d01554da299b5bfd08270ccbb3f4d5f2e10a8876f708adb8daf(
    *,
    mqtt_topic: builtins.str,
    payload: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bc617ea5eecc7c2f870f30ed590c15b8cfb7e30a871b8722320a009d74bf19d(
    *,
    function_arn: builtins.str,
    payload: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e83f0bcba645b576e8b0f679bf8eb120b894cb26f6bd57c6b31a416eaaa55c68(
    *,
    content_expression: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38238b114d571c07a0278ac74c9927826577a307612915d912b10c53eb8e48a0(
    *,
    comparison_operator: builtins.str,
    input_property: builtins.str,
    threshold: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37525278edd4b9720989e6018b5b4fe53472869326ab48f2d2d1167861e0a870(
    *,
    target_arn: builtins.str,
    payload: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e42920d9c69b06500829d02b9b6156b2a6b606f35b89b6d9cf66bd6bc2264559(
    *,
    queue_url: builtins.str,
    payload: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    use_base64: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbda50935840a9092dc02e74659d967b56b7cafe139501d66a69d3b36de77890(
    *,
    alarm_rule: typing.Union[typing.Union[CfnAlarmModel.AlarmRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    role_arn: builtins.str,
    alarm_capabilities: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.AlarmCapabilitiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    alarm_event_actions: typing.Optional[typing.Union[typing.Union[CfnAlarmModel.AlarmEventActionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    alarm_model_description: typing.Optional[builtins.str] = None,
    alarm_model_name: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    severity: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbdb1289d0fb5f082d64616bc7675cc0f446f19d2268dcd3151b55ab400db9c0(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    detector_model_definition: typing.Union[typing.Union[CfnDetectorModel.DetectorModelDefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    role_arn: builtins.str,
    detector_model_description: typing.Optional[builtins.str] = None,
    detector_model_name: typing.Optional[builtins.str] = None,
    evaluation_method: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba5ff28e61e446ec636e269b07d2b274f1ec2740651842382f757a64050a330b(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71b348d5b864eec84da0b6a0e2f3c29d6afd6a9314e1d12159f3719b060dc3d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1884a4c2dc8139ac71fce533b53ce11f50a8d454d5ae3b76b25015b6b75d92c8(
    value: typing.Union[CfnDetectorModel.DetectorModelDefinitionProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbaa93d99534f7704e22958d063ef4153ac3cb9d266e87fb9f6e761303bc3c64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8342c966991619769a329fd3eda4f8dc6a61626057274e5c2445da0a6544cba7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efcfa1c4f4dad1fa43c85a945e5158c870b5028d8e72786003d91b15597fda4b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb412275cb971c101dd7e211a3221f17b9efbff11c3c9f0aa270b41c5a19ab0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__541d636b65115810770a71349f195d6f0f950cb98134c2d075eab92dfb19ecb6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e2bce1fe0cd77aae0a1e6fc46b095a511402771d452eb1e9e864867a4dea8e(
    *,
    clear_timer: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.ClearTimerProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    dynamo_db: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.DynamoDBProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    dynamo_d_bv2: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.DynamoDBv2Property, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    firehose: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.FirehoseProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    iot_events: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.IotEventsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    iot_site_wise: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.IotSiteWiseProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    iot_topic_publish: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.IotTopicPublishProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    lambda_: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.LambdaProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    reset_timer: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.ResetTimerProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    set_timer: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.SetTimerProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    set_variable: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.SetVariableProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sns: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.SnsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sqs: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.SqsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58415476f4e5211c17a67b819b8192c4b4e1a7e6b591b7e25bab106c901ac1c8(
    *,
    time_in_seconds: builtins.str,
    offset_in_nanos: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91dbd97594cd581829c75fadfa1039ecb4ce505f3e8c54d3e7e254c8df7163a1(
    *,
    value: typing.Union[typing.Union[CfnDetectorModel.AssetPropertyVariantProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    quality: typing.Optional[builtins.str] = None,
    timestamp: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.AssetPropertyTimestampProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46daa12fc1ae4d34be03fce2ae8fbb3a96f7aef48bdd9477389f36b6bd44d945(
    *,
    boolean_value: typing.Optional[builtins.str] = None,
    double_value: typing.Optional[builtins.str] = None,
    integer_value: typing.Optional[builtins.str] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db2e7f4fda95e3c7fbc0d9376950212cfb83c322970fc2fa38a216d63e26f1cb(
    *,
    timer_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66859f5359ee29b1078fb1fc8c4404969ca38476d5ed6404cc4fe88fd67f2a8f(
    *,
    initial_state_name: builtins.str,
    states: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnDetectorModel.StateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__765b650dd5ee90a7c750be55b537c3bbe23bf921f158c5a2fe3c46eaf669ebc3(
    *,
    hash_key_field: builtins.str,
    hash_key_value: builtins.str,
    table_name: builtins.str,
    hash_key_type: typing.Optional[builtins.str] = None,
    operation: typing.Optional[builtins.str] = None,
    payload: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    payload_field: typing.Optional[builtins.str] = None,
    range_key_field: typing.Optional[builtins.str] = None,
    range_key_type: typing.Optional[builtins.str] = None,
    range_key_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e02e819491bf01b0ae2af9b97e4c47198d13014a402c8a7375cc54e275f9a1a(
    *,
    table_name: builtins.str,
    payload: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14d56b59ca224936868097631f52f49fd345a9ba63e01375bbf3903250ce495(
    *,
    event_name: builtins.str,
    actions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnDetectorModel.ActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    condition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de720b5e4aa44f00c3480d9d6fa7b92efc58bf123d8a17d540dd1677b6adfd84(
    *,
    delivery_stream_name: builtins.str,
    payload: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    separator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c18b4bbf49aeafd47c5103d506ba087f7bb55d3a2d92cc73b56b5ed3f418111(
    *,
    input_name: builtins.str,
    payload: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e314dec90319ab6330fdf50d0cd36560054ccc5b8f0c75173d108c91622ec5bb(
    *,
    property_value: typing.Union[typing.Union[CfnDetectorModel.AssetPropertyValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    asset_id: typing.Optional[builtins.str] = None,
    entry_id: typing.Optional[builtins.str] = None,
    property_alias: typing.Optional[builtins.str] = None,
    property_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c3ebb624c99aef373f04785e49a31de2f9e416a494acaac4292bba694d6de1(
    *,
    mqtt_topic: builtins.str,
    payload: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9684c316eefbb054da20f62b47b3364ef10d33add40011256966aecab149d513(
    *,
    function_arn: builtins.str,
    payload: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f20db8cfce173ff75e3f8322eb91b32cc1401b580d9c2e12dfb0747992351fa(
    *,
    events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnDetectorModel.EventProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12722923002267c0c006cf1c8063f0f263a521ab1fd1b9bfec62d920b7989b4e(
    *,
    events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnDetectorModel.EventProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58ace0464a2b6c8630a01e1b4a9c04c8ba7db2b33d3e6163924c90fbdbd0c5b(
    *,
    events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnDetectorModel.EventProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    transition_events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnDetectorModel.TransitionEventProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0cd0cb3751a1ce11cd3d2c57c970046b10f9ce423d08422465e44f50ffb3492(
    *,
    content_expression: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec125d7211fff7aa0b7d0e338fc5491087d617575057ade2be2ec02eeedcf8b4(
    *,
    timer_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a29889c1ace504dbdcdba1eddc8628ce3811416fdde5123ad8ff3020fc633f08(
    *,
    timer_name: builtins.str,
    duration_expression: typing.Optional[builtins.str] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39f8a7a8dff4c1ef4cac00bc3936710a995692c474b569e64ab27f53a78e53ec(
    *,
    value: builtins.str,
    variable_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7681907fa4aee84717d34242c6974c4b260b29efa77afcf913470b8e46634ae8(
    *,
    target_arn: builtins.str,
    payload: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b04f3c8765ad06a75c0ba0d367b24368e06453fc5c477c240b01dad7c0a4a5(
    *,
    queue_url: builtins.str,
    payload: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.PayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    use_base64: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fcd1a66b115ad806079e97994b07e7b3411e1dacb5fa008409f8ce443f1cc71(
    *,
    state_name: builtins.str,
    on_enter: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.OnEnterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    on_exit: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.OnExitProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    on_input: typing.Optional[typing.Union[typing.Union[CfnDetectorModel.OnInputProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__162c185f80f628eee71fedbdb51893ff66e9e6baa28040b9e84fe25264f89e2a(
    *,
    condition: builtins.str,
    event_name: builtins.str,
    next_state: builtins.str,
    actions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnDetectorModel.ActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbf081acf6d5045fabb59bf7f5e0ae811e32d3091782126a2322417af75f5c62(
    *,
    detector_model_definition: typing.Union[typing.Union[CfnDetectorModel.DetectorModelDefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    role_arn: builtins.str,
    detector_model_description: typing.Optional[builtins.str] = None,
    detector_model_name: typing.Optional[builtins.str] = None,
    evaluation_method: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef5aa809de55ed0610206e2d687545885d6443313a73b31e379f28180f074a0a(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    input_definition: typing.Union[typing.Union[CfnInput.InputDefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    input_description: typing.Optional[builtins.str] = None,
    input_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a1d74b79c7f1aec3ad406b8f26c8da50d7066110d302446345d370f948bb3ea(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac1ab2d9f1b39d6982f7072f46fd62820a25e06d90430a7ad194c204629ecf8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a22cc2052ecb63941a580f1063be2b0dfd0ff197af9b0b9191c11f4d68c87f9(
    value: typing.Union[CfnInput.InputDefinitionProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1252aa877157bbd7049243ad7caa78d4fdd6dc3c5283ad2e542a98da212e359(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97fd2c1c7e85c7c649ce55fbde52fc60471612e5a6f65f54fc79c41aff9d6df2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b57031c3f18bcbb8d7f6ca6f09445c05bc7e256c370371e129e8e47616faec2c(
    *,
    json_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d756e737a6a9bdaaf2819b9c6c86e67820ea6c7bf81b0cfc354dd3ae4eacf4a(
    *,
    attributes: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnInput.AttributeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65f89c1939fb85ff5429362c39134351a5602b07057ac791fba1e816fed71c25(
    *,
    input_definition: typing.Union[typing.Union[CfnInput.InputDefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    input_description: typing.Optional[builtins.str] = None,
    input_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd48144b7dc9569116a2fa81f4c10b4cf4192ce4390fa794b4301e87f5e767f(
    *,
    initial_state: State,
    description: typing.Optional[builtins.str] = None,
    detector_key: typing.Optional[builtins.str] = None,
    detector_model_name: typing.Optional[builtins.str] = None,
    evaluation_method: typing.Optional[EventEvaluation] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b79b241c7a064cd0939d018c3b7d72a8999872d686b40bc0d7810ff341efc4(
    *,
    event_name: builtins.str,
    actions: typing.Optional[typing.Sequence[IAction]] = None,
    condition: typing.Optional[Expression] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc712dc3dba960b89e11dd0be43d835de974be4ffbb38a03f1a30ad60592bb9(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05fb7b5983e5cac7e39ec81cb0b77596494d0fbd002d2697f8ef7b3b1af44999(
    input: IInput,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79718ac5cbbe2ce56ca114b4f4157f3beef320a29fe1805cd832d23ac09e8675(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecc11603296f80d784d556c14ce2090443676b1a71b8ffc29b1a7dd415b78f44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448cf29e4d4d89e9746a4ea0bf4b8d4dea6a9083ef7910b5583d50d5b909f0b2(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ecb4a311a64e667a4982c94996e1944b499e2488dd5a1081b6ca54a76003552(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b9c08f86c74455b35cc063f0c558a292da6c5f047e8b3a87f273961921e026(
    input: IInput,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09df8314ad56ef37f0e1827de7ee4f2d96c7a00c979f59db686d648c675669bb(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90dc25a15be155be64d350bb2af87284608b16917b3455e2522613ee0778dd1a(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__700901c21f28bf8aa913e84b37d9dad894697f809ad1f180e5cb9e197d806fdc(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d747908502a1ad500cb271688f0c5e0297f1261c92f4ab16ed1f4610fc7940f(
    left: Expression,
    right: Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ba300fa422c65f84f188db530fe6f69af2040f046d7c1378173bd4a134eea3(
    parent_priority: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ce27fdc532b62829b75239b068a8ef8fbfdd2ae9d377bcbe3df3d4274f450e(
    scope: _constructs_77d1e7e8.Construct,
    *,
    role: _IRole_59af6f50,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00e34bff62550c821f4a102db7c420193f1d8ed154c3e2be8e302d1b90ec0843(
    grantee: _IGrantable_4c5a91d1,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1f27802114bc2027bc73d322322e8b25260fe0ea37914db7553da801936ccf3(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed3031091c350af10609eaf9f4a82e69341836842aa0f2497ec90ac221859d96(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    attribute_json_paths: typing.Sequence[builtins.str],
    input_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eed37747b2db6d63ffcd446457d2d0f38d1fd74645612af86a24365d61c9f43(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    input_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8456138490e1818a90738f49544ad45a6321144a3ffcc0a99e6ecfb6a49855ae(
    grantee: _IGrantable_4c5a91d1,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__823afcc1a49d2bb91fdd24f35c5d10fa7a2cab840c8868f14886ae03bd4fbbaa(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7afd2074a55c65cbb7010d5b3bd086844fe5a1793d2999178949958925278cb5(
    *,
    attribute_json_paths: typing.Sequence[builtins.str],
    input_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd2c4054123c78e6661909d294ab8615528818d1b07fbcbcac927b51d554d81a(
    target_state: State,
    *,
    when: Expression,
    event_name: typing.Optional[builtins.str] = None,
    executing: typing.Optional[typing.Sequence[IAction]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fdde7f3a019c1bac662f35db5759679d5df06cdb9b54ebbbcd16e6e73f3235(
    *,
    state_name: builtins.str,
    on_enter: typing.Optional[typing.Sequence[typing.Union[Event, typing.Dict[builtins.str, typing.Any]]]] = None,
    on_exit: typing.Optional[typing.Sequence[typing.Union[Event, typing.Dict[builtins.str, typing.Any]]]] = None,
    on_input: typing.Optional[typing.Sequence[typing.Union[Event, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b1676412ccaf7f3a15c9e7b613d67687a991510c21f8c803f754e1c507957b(
    *,
    when: Expression,
    event_name: typing.Optional[builtins.str] = None,
    executing: typing.Optional[typing.Sequence[IAction]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a658a6836e212adc207ef6570785abc2804ca86e25dc97ba0912b6a03448154(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    initial_state: State,
    description: typing.Optional[builtins.str] = None,
    detector_key: typing.Optional[builtins.str] = None,
    detector_model_name: typing.Optional[builtins.str] = None,
    evaluation_method: typing.Optional[EventEvaluation] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__202a828c7cf6b9f83a91661d04229cc70e3f8e1810585590ab17556eccfbe7fa(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    detector_model_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
