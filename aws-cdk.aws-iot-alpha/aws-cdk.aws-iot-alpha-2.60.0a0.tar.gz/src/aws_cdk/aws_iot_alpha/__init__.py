'''
# AWS IoT Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

AWS IoT Core lets you connect billions of IoT devices and route trillions of
messages to AWS services without managing infrastructure.

## `TopicRule`

Create a topic rule that give your devices the ability to interact with AWS services.
You can create a topic rule with an action that invoke the Lambda action as following:

```python
func = lambda_.Function(self, "MyFunction",
    runtime=lambda_.Runtime.NODEJS_14_X,
    handler="index.handler",
    code=lambda_.Code.from_inline("""
            exports.handler = (event) => {
              console.log("It is test for lambda action of AWS IoT Rule.", event);
            };""")
)

iot.TopicRule(self, "TopicRule",
    topic_rule_name="MyTopicRule",  # optional
    description="invokes the lambda function",  # optional
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp FROM 'device/+/data'"),
    actions=[actions.LambdaFunctionAction(func)]
)
```

Or, you can add an action after constructing the `TopicRule` instance as following:

```python
# func: lambda.Function


topic_rule = iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp FROM 'device/+/data'")
)
topic_rule.add_action(actions.LambdaFunctionAction(func))
```

You can also supply `errorAction` as following,
and the IoT Rule will trigger it if a rule's action is unable to perform:

```python
import aws_cdk.aws_logs as logs


log_group = logs.LogGroup(self, "MyLogGroup")

iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp FROM 'device/+/data'"),
    error_action=actions.CloudWatchLogsAction(log_group)
)
```

If you wanna make the topic rule disable, add property `enabled: false` as following:

```python
iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp FROM 'device/+/data'"),
    enabled=False
)
```

See also [@aws-cdk/aws-iot-actions](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-iot-actions-readme.html) for other actions.
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

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_iot as _aws_cdk_aws_iot_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-alpha.ActionConfig",
    jsii_struct_bases=[],
    name_mapping={"configuration": "configuration"},
)
class ActionConfig:
    def __init__(
        self,
        *,
        configuration: typing.Union[_aws_cdk_aws_iot_ceddda9d.CfnTopicRule.ActionProperty, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''(experimental) Properties for an topic rule action.

        :param configuration: (experimental) The configuration for this action.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iot_alpha as iot_alpha
            
            action_config = iot_alpha.ActionConfig(
                configuration=ActionProperty(
                    cloudwatch_alarm=CloudwatchAlarmActionProperty(
                        alarm_name="alarmName",
                        role_arn="roleArn",
                        state_reason="stateReason",
                        state_value="stateValue"
                    ),
                    cloudwatch_logs=CloudwatchLogsActionProperty(
                        log_group_name="logGroupName",
                        role_arn="roleArn"
                    ),
                    cloudwatch_metric=CloudwatchMetricActionProperty(
                        metric_name="metricName",
                        metric_namespace="metricNamespace",
                        metric_unit="metricUnit",
                        metric_value="metricValue",
                        role_arn="roleArn",
            
                        # the properties below are optional
                        metric_timestamp="metricTimestamp"
                    ),
                    dynamo_db=DynamoDBActionProperty(
                        hash_key_field="hashKeyField",
                        hash_key_value="hashKeyValue",
                        role_arn="roleArn",
                        table_name="tableName",
            
                        # the properties below are optional
                        hash_key_type="hashKeyType",
                        payload_field="payloadField",
                        range_key_field="rangeKeyField",
                        range_key_type="rangeKeyType",
                        range_key_value="rangeKeyValue"
                    ),
                    dynamo_dBv2=DynamoDBv2ActionProperty(
                        put_item=PutItemInputProperty(
                            table_name="tableName"
                        ),
                        role_arn="roleArn"
                    ),
                    elasticsearch=ElasticsearchActionProperty(
                        endpoint="endpoint",
                        id="id",
                        index="index",
                        role_arn="roleArn",
                        type="type"
                    ),
                    firehose=FirehoseActionProperty(
                        delivery_stream_name="deliveryStreamName",
                        role_arn="roleArn",
            
                        # the properties below are optional
                        batch_mode=False,
                        separator="separator"
                    ),
                    http=HttpActionProperty(
                        url="url",
            
                        # the properties below are optional
                        auth=HttpAuthorizationProperty(
                            sigv4=SigV4AuthorizationProperty(
                                role_arn="roleArn",
                                service_name="serviceName",
                                signing_region="signingRegion"
                            )
                        ),
                        confirmation_url="confirmationUrl",
                        headers=[HttpActionHeaderProperty(
                            key="key",
                            value="value"
                        )]
                    ),
                    iot_analytics=IotAnalyticsActionProperty(
                        channel_name="channelName",
                        role_arn="roleArn",
            
                        # the properties below are optional
                        batch_mode=False
                    ),
                    iot_events=IotEventsActionProperty(
                        input_name="inputName",
                        role_arn="roleArn",
            
                        # the properties below are optional
                        batch_mode=False,
                        message_id="messageId"
                    ),
                    iot_site_wise=IotSiteWiseActionProperty(
                        put_asset_property_value_entries=[PutAssetPropertyValueEntryProperty(
                            property_values=[AssetPropertyValueProperty(
                                timestamp=AssetPropertyTimestampProperty(
                                    time_in_seconds="timeInSeconds",
            
                                    # the properties below are optional
                                    offset_in_nanos="offsetInNanos"
                                ),
                                value=AssetPropertyVariantProperty(
                                    boolean_value="booleanValue",
                                    double_value="doubleValue",
                                    integer_value="integerValue",
                                    string_value="stringValue"
                                ),
            
                                # the properties below are optional
                                quality="quality"
                            )],
            
                            # the properties below are optional
                            asset_id="assetId",
                            entry_id="entryId",
                            property_alias="propertyAlias",
                            property_id="propertyId"
                        )],
                        role_arn="roleArn"
                    ),
                    kafka=KafkaActionProperty(
                        client_properties={
                            "client_properties_key": "clientProperties"
                        },
                        destination_arn="destinationArn",
                        topic="topic",
            
                        # the properties below are optional
                        key="key",
                        partition="partition"
                    ),
                    kinesis=KinesisActionProperty(
                        role_arn="roleArn",
                        stream_name="streamName",
            
                        # the properties below are optional
                        partition_key="partitionKey"
                    ),
                    lambda_=LambdaActionProperty(
                        function_arn="functionArn"
                    ),
                    location=LocationActionProperty(
                        device_id="deviceId",
                        latitude="latitude",
                        longitude="longitude",
                        role_arn="roleArn",
                        tracker_name="trackerName",
            
                        # the properties below are optional
                        timestamp=Date()
                    ),
                    open_search=OpenSearchActionProperty(
                        endpoint="endpoint",
                        id="id",
                        index="index",
                        role_arn="roleArn",
                        type="type"
                    ),
                    republish=RepublishActionProperty(
                        role_arn="roleArn",
                        topic="topic",
            
                        # the properties below are optional
                        headers=RepublishActionHeadersProperty(
                            content_type="contentType",
                            correlation_data="correlationData",
                            message_expiry="messageExpiry",
                            payload_format_indicator="payloadFormatIndicator",
                            response_topic="responseTopic",
                            user_properties=[UserPropertyProperty(
                                key="key",
                                value="value"
                            )]
                        ),
                        qos=123
                    ),
                    s3=S3ActionProperty(
                        bucket_name="bucketName",
                        key="key",
                        role_arn="roleArn",
            
                        # the properties below are optional
                        canned_acl="cannedAcl"
                    ),
                    sns=SnsActionProperty(
                        role_arn="roleArn",
                        target_arn="targetArn",
            
                        # the properties below are optional
                        message_format="messageFormat"
                    ),
                    sqs=SqsActionProperty(
                        queue_url="queueUrl",
                        role_arn="roleArn",
            
                        # the properties below are optional
                        use_base64=False
                    ),
                    step_functions=StepFunctionsActionProperty(
                        role_arn="roleArn",
                        state_machine_name="stateMachineName",
            
                        # the properties below are optional
                        execution_name_prefix="executionNamePrefix"
                    ),
                    timestream=TimestreamActionProperty(
                        database_name="databaseName",
                        dimensions=[TimestreamDimensionProperty(
                            name="name",
                            value="value"
                        )],
                        role_arn="roleArn",
                        table_name="tableName",
            
                        # the properties below are optional
                        timestamp=TimestreamTimestampProperty(
                            unit="unit",
                            value="value"
                        )
                    )
                )
            )
        '''
        if isinstance(configuration, dict):
            configuration = _aws_cdk_aws_iot_ceddda9d.CfnTopicRule.ActionProperty(**configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db72c5f97249b79d721bcd6a87436f822fe27caf16ccc0ae7aaa3671a54e7e5f)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration": configuration,
        }

    @builtins.property
    def configuration(self) -> _aws_cdk_aws_iot_ceddda9d.CfnTopicRule.ActionProperty:
        '''(experimental) The configuration for this action.

        :stability: experimental
        '''
        result = self._values.get("configuration")
        assert result is not None, "Required property 'configuration' is missing"
        return typing.cast(_aws_cdk_aws_iot_ceddda9d.CfnTopicRule.ActionProperty, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-iot-alpha.IAction")
class IAction(typing_extensions.Protocol):
    '''(experimental) An abstract action for TopicRule.

    :stability: experimental
    '''

    pass


class _IActionProxy:
    '''(experimental) An abstract action for TopicRule.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iot-alpha.IAction"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAction).__jsii_proxy_class__ = lambda : _IActionProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iot-alpha.ITopicRule")
class ITopicRule(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Represents an AWS IoT Rule.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="topicRuleArn")
    def topic_rule_arn(self) -> builtins.str:
        '''(experimental) The value of the topic rule Amazon Resource Name (ARN), such as arn:aws:iot:us-east-2:123456789012:rule/rule_name.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="topicRuleName")
    def topic_rule_name(self) -> builtins.str:
        '''(experimental) The name topic rule.

        :stability: experimental
        :attribute: true
        '''
        ...


class _ITopicRuleProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents an AWS IoT Rule.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iot-alpha.ITopicRule"

    @builtins.property
    @jsii.member(jsii_name="topicRuleArn")
    def topic_rule_arn(self) -> builtins.str:
        '''(experimental) The value of the topic rule Amazon Resource Name (ARN), such as arn:aws:iot:us-east-2:123456789012:rule/rule_name.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "topicRuleArn"))

    @builtins.property
    @jsii.member(jsii_name="topicRuleName")
    def topic_rule_name(self) -> builtins.str:
        '''(experimental) The name topic rule.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "topicRuleName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITopicRule).__jsii_proxy_class__ = lambda : _ITopicRuleProxy


class IotSql(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-iot-alpha.IotSql",
):
    '''(experimental) Defines AWS IoT SQL.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_sns as sns
        
        
        topic = sns.Topic(self, "MyTopic")
        
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
            actions=[
                actions.SnsTopicAction(topic,
                    message_format=actions.SnsActionMessageFormat.JSON
                )
            ]
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromStringAsVer20151008")
    @builtins.classmethod
    def from_string_as_ver20151008(cls, sql: builtins.str) -> "IotSql":
        '''(experimental) Uses the original SQL version built on 2015-10-08.

        :param sql: The actual SQL-like syntax query.

        :return: Instance of IotSql

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40b60afd6a89f56eb454ee327bd143df85ea1ea9518d995f338ac85c6f9172ef)
            check_type(argname="argument sql", value=sql, expected_type=type_hints["sql"])
        return typing.cast("IotSql", jsii.sinvoke(cls, "fromStringAsVer20151008", [sql]))

    @jsii.member(jsii_name="fromStringAsVer20160323")
    @builtins.classmethod
    def from_string_as_ver20160323(cls, sql: builtins.str) -> "IotSql":
        '''(experimental) Uses the SQL version built on 2016-03-23.

        :param sql: The actual SQL-like syntax query.

        :return: Instance of IotSql

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__246c805677b75001ec2445224c8ee29056b92709ee8d3bb168587a48bc5d0fb5)
            check_type(argname="argument sql", value=sql, expected_type=type_hints["sql"])
        return typing.cast("IotSql", jsii.sinvoke(cls, "fromStringAsVer20160323", [sql]))

    @jsii.member(jsii_name="fromStringAsVerNewestUnstable")
    @builtins.classmethod
    def from_string_as_ver_newest_unstable(cls, sql: builtins.str) -> "IotSql":
        '''(experimental) Uses the most recent beta SQL version.

        If you use this version, it might
        introduce breaking changes to your rules.

        :param sql: The actual SQL-like syntax query.

        :return: Instance of IotSql

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__715467063ed924cc91a9fa5b60c44d4b1b82edbc8eb085d68321fd0014a32067)
            check_type(argname="argument sql", value=sql, expected_type=type_hints["sql"])
        return typing.cast("IotSql", jsii.sinvoke(cls, "fromStringAsVerNewestUnstable", [sql]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, scope: _constructs_77d1e7e8.Construct) -> "IotSqlConfig":
        '''(experimental) Returns the IoT SQL configuration.

        :param scope: -

        :stability: experimental
        '''
        ...


class _IotSqlProxy(IotSql):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: _constructs_77d1e7e8.Construct) -> "IotSqlConfig":
        '''(experimental) Returns the IoT SQL configuration.

        :param scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d3862c5242014e403c7a2af3ffcf5d3a77ce6e5376d651493716a5b5061bd9a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("IotSqlConfig", jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, IotSql).__jsii_proxy_class__ = lambda : _IotSqlProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-alpha.IotSqlConfig",
    jsii_struct_bases=[],
    name_mapping={"aws_iot_sql_version": "awsIotSqlVersion", "sql": "sql"},
)
class IotSqlConfig:
    def __init__(self, *, aws_iot_sql_version: builtins.str, sql: builtins.str) -> None:
        '''(experimental) The type returned from the ``bind()`` method in ``IotSql``.

        :param aws_iot_sql_version: (experimental) The version of the SQL rules engine to use when evaluating the rule.
        :param sql: (experimental) The SQL statement used to query the topic.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iot_alpha as iot_alpha
            
            iot_sql_config = iot_alpha.IotSqlConfig(
                aws_iot_sql_version="awsIotSqlVersion",
                sql="sql"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__887fb9654c4aa0ba71be51a8acf671f0dc89cdb21899f13ebce575d2da566e05)
            check_type(argname="argument aws_iot_sql_version", value=aws_iot_sql_version, expected_type=type_hints["aws_iot_sql_version"])
            check_type(argname="argument sql", value=sql, expected_type=type_hints["sql"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_iot_sql_version": aws_iot_sql_version,
            "sql": sql,
        }

    @builtins.property
    def aws_iot_sql_version(self) -> builtins.str:
        '''(experimental) The version of the SQL rules engine to use when evaluating the rule.

        :stability: experimental
        '''
        result = self._values.get("aws_iot_sql_version")
        assert result is not None, "Required property 'aws_iot_sql_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sql(self) -> builtins.str:
        '''(experimental) The SQL statement used to query the topic.

        :stability: experimental
        '''
        result = self._values.get("sql")
        assert result is not None, "Required property 'sql' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotSqlConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITopicRule)
class TopicRule(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot-alpha.TopicRule",
):
    '''(experimental) Defines an AWS IoT Rule in this stack.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_sns as sns
        
        
        topic = sns.Topic(self, "MyTopic")
        
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
            actions=[
                actions.SnsTopicAction(topic,
                    message_format=actions.SnsActionMessageFormat.JSON
                )
            ]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        sql: IotSql,
        actions: typing.Optional[typing.Sequence[IAction]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        error_action: typing.Optional[IAction] = None,
        topic_rule_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param sql: (experimental) A simplified SQL syntax to filter messages received on an MQTT topic and push the data elsewhere.
        :param actions: (experimental) The actions associated with the topic rule. Default: No actions will be perform
        :param description: (experimental) A textual description of the topic rule. Default: None
        :param enabled: (experimental) Specifies whether the rule is enabled. Default: true
        :param error_action: (experimental) The action AWS IoT performs when it is unable to perform a rule's action. Default: - no action will be performed
        :param topic_rule_name: (experimental) The name of the topic rule. Default: None

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5629ae4086674af1b4cd4c3b55a1d2cd04d194fe7dd7d9a1a08478dc69d9ac5f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TopicRuleProps(
            sql=sql,
            actions=actions,
            description=description,
            enabled=enabled,
            error_action=error_action,
            topic_rule_name=topic_rule_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromTopicRuleArn")
    @builtins.classmethod
    def from_topic_rule_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        topic_rule_arn: builtins.str,
    ) -> ITopicRule:
        '''(experimental) Import an existing AWS IoT Rule provided an ARN.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param topic_rule_arn: AWS IoT Rule ARN (i.e. arn:aws:iot:::rule/MyRule).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a02640c49b9d9e3824df915f05b77c597b5dfd5d900377ada5b2b60b004bbf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument topic_rule_arn", value=topic_rule_arn, expected_type=type_hints["topic_rule_arn"])
        return typing.cast(ITopicRule, jsii.sinvoke(cls, "fromTopicRuleArn", [scope, id, topic_rule_arn]))

    @jsii.member(jsii_name="addAction")
    def add_action(self, action: IAction) -> None:
        '''(experimental) Add a action to the topic rule.

        :param action: the action to associate with the topic rule.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e6d84c555ae6d88e9f422f5418183ec42014991c6a48af643a3d0341a35a73a)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
        return typing.cast(None, jsii.invoke(self, "addAction", [action]))

    @builtins.property
    @jsii.member(jsii_name="topicRuleArn")
    def topic_rule_arn(self) -> builtins.str:
        '''(experimental) Arn of this topic rule.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "topicRuleArn"))

    @builtins.property
    @jsii.member(jsii_name="topicRuleName")
    def topic_rule_name(self) -> builtins.str:
        '''(experimental) Name of this topic rule.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "topicRuleName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-alpha.TopicRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "sql": "sql",
        "actions": "actions",
        "description": "description",
        "enabled": "enabled",
        "error_action": "errorAction",
        "topic_rule_name": "topicRuleName",
    },
)
class TopicRuleProps:
    def __init__(
        self,
        *,
        sql: IotSql,
        actions: typing.Optional[typing.Sequence[IAction]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        error_action: typing.Optional[IAction] = None,
        topic_rule_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for defining an AWS IoT Rule.

        :param sql: (experimental) A simplified SQL syntax to filter messages received on an MQTT topic and push the data elsewhere.
        :param actions: (experimental) The actions associated with the topic rule. Default: No actions will be perform
        :param description: (experimental) A textual description of the topic rule. Default: None
        :param enabled: (experimental) Specifies whether the rule is enabled. Default: true
        :param error_action: (experimental) The action AWS IoT performs when it is unable to perform a rule's action. Default: - no action will be performed
        :param topic_rule_name: (experimental) The name of the topic rule. Default: None

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_sns as sns
            
            
            topic = sns.Topic(self, "MyTopic")
            
            topic_rule = iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
                actions=[
                    actions.SnsTopicAction(topic,
                        message_format=actions.SnsActionMessageFormat.JSON
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__590edde80b67943632c721759786da252d24ea6e116cd451e3e93bb968888414)
            check_type(argname="argument sql", value=sql, expected_type=type_hints["sql"])
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument error_action", value=error_action, expected_type=type_hints["error_action"])
            check_type(argname="argument topic_rule_name", value=topic_rule_name, expected_type=type_hints["topic_rule_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sql": sql,
        }
        if actions is not None:
            self._values["actions"] = actions
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if error_action is not None:
            self._values["error_action"] = error_action
        if topic_rule_name is not None:
            self._values["topic_rule_name"] = topic_rule_name

    @builtins.property
    def sql(self) -> IotSql:
        '''(experimental) A simplified SQL syntax to filter messages received on an MQTT topic and push the data elsewhere.

        :see: https://docs.aws.amazon.com/iot/latest/developerguide/iot-sql-reference.html
        :stability: experimental
        '''
        result = self._values.get("sql")
        assert result is not None, "Required property 'sql' is missing"
        return typing.cast(IotSql, result)

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[IAction]]:
        '''(experimental) The actions associated with the topic rule.

        :default: No actions will be perform

        :stability: experimental
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[IAction]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A textual description of the topic rule.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether the rule is enabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def error_action(self) -> typing.Optional[IAction]:
        '''(experimental) The action AWS IoT performs when it is unable to perform a rule's action.

        :default: - no action will be performed

        :stability: experimental
        '''
        result = self._values.get("error_action")
        return typing.cast(typing.Optional[IAction], result)

    @builtins.property
    def topic_rule_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the topic rule.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("topic_rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TopicRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ActionConfig",
    "IAction",
    "ITopicRule",
    "IotSql",
    "IotSqlConfig",
    "TopicRule",
    "TopicRuleProps",
]

publication.publish()

def _typecheckingstub__db72c5f97249b79d721bcd6a87436f822fe27caf16ccc0ae7aaa3671a54e7e5f(
    *,
    configuration: typing.Union[_aws_cdk_aws_iot_ceddda9d.CfnTopicRule.ActionProperty, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40b60afd6a89f56eb454ee327bd143df85ea1ea9518d995f338ac85c6f9172ef(
    sql: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__246c805677b75001ec2445224c8ee29056b92709ee8d3bb168587a48bc5d0fb5(
    sql: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__715467063ed924cc91a9fa5b60c44d4b1b82edbc8eb085d68321fd0014a32067(
    sql: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3862c5242014e403c7a2af3ffcf5d3a77ce6e5376d651493716a5b5061bd9a(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887fb9654c4aa0ba71be51a8acf671f0dc89cdb21899f13ebce575d2da566e05(
    *,
    aws_iot_sql_version: builtins.str,
    sql: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5629ae4086674af1b4cd4c3b55a1d2cd04d194fe7dd7d9a1a08478dc69d9ac5f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    sql: IotSql,
    actions: typing.Optional[typing.Sequence[IAction]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    error_action: typing.Optional[IAction] = None,
    topic_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a02640c49b9d9e3824df915f05b77c597b5dfd5d900377ada5b2b60b004bbf(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    topic_rule_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6d84c555ae6d88e9f422f5418183ec42014991c6a48af643a3d0341a35a73a(
    action: IAction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__590edde80b67943632c721759786da252d24ea6e116cd451e3e93bb968888414(
    *,
    sql: IotSql,
    actions: typing.Optional[typing.Sequence[IAction]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    error_action: typing.Optional[IAction] = None,
    topic_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
