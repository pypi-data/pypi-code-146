'''
# Actions for AWS IoT Rule

This library contains integration classes to send data to any number of
supported AWS Services. Instances of these classes should be passed to
`TopicRule` defined in `@aws-cdk/aws-iot`.

Currently supported are:

* Republish a message to another MQTT topic
* Invoke a Lambda function
* Put objects to a S3 bucket
* Put logs to CloudWatch Logs
* Capture CloudWatch metrics
* Change state for a CloudWatch alarm
* Put records to Kinesis Data stream
* Put records to Kinesis Data Firehose stream
* Send messages to SQS queues
* Publish messages on SNS topics

## Republish a message to another MQTT topic

The code snippet below creates an AWS IoT Rule that republish a message to
another MQTT topic when it is triggered.

```python
iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp, temperature FROM 'device/+/data'"),
    actions=[
        actions.IotRepublishMqttAction("${topic()}/republish",
            quality_of_service=actions.MqttQualityOfService.AT_LEAST_ONCE
        )
    ]
)
```

## Invoke a Lambda function

The code snippet below creates an AWS IoT Rule that invoke a Lambda function
when it is triggered.

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
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp, temperature FROM 'device/+/data'"),
    actions=[actions.LambdaFunctionAction(func)]
)
```

## Put objects to a S3 bucket

The code snippet below creates an AWS IoT Rule that put objects to a S3 bucket
when it is triggered.

```python
bucket = s3.Bucket(self, "MyBucket")

iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id FROM 'device/+/data'"),
    actions=[actions.S3PutObjectAction(bucket)]
)
```

The property `key` of `S3PutObjectAction` is given the value `${topic()}/${timestamp()}` by default. This `${topic()}`
and `${timestamp()}` is called Substitution templates. For more information see
[this documentation](https://docs.aws.amazon.com/iot/latest/developerguide/iot-substitution-templates.html).
In above sample, `${topic()}` is replaced by a given MQTT topic as `device/001/data`. And `${timestamp()}` is replaced
by the number of the current timestamp in milliseconds as `1636289461203`. So if the MQTT broker receives an MQTT topic
`device/001/data` on `2021-11-07T00:00:00.000Z`, the S3 bucket object will be put to `device/001/data/1636243200000`.

You can also set specific `key` as following:

```python
bucket = s3.Bucket(self, "MyBucket")

iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
    actions=[
        actions.S3PutObjectAction(bucket,
            key="${year}/${month}/${day}/${topic(2)}"
        )
    ]
)
```

If you wanna set access control to the S3 bucket object, you can specify `accessControl` as following:

```python
bucket = s3.Bucket(self, "MyBucket")

iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
    actions=[
        actions.S3PutObjectAction(bucket,
            access_control=s3.BucketAccessControl.PUBLIC_READ
        )
    ]
)
```

## Put logs to CloudWatch Logs

The code snippet below creates an AWS IoT Rule that put logs to CloudWatch Logs
when it is triggered.

```python
import monocdk as logs


log_group = logs.LogGroup(self, "MyLogGroup")

iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id FROM 'device/+/data'"),
    actions=[actions.CloudWatchLogsAction(log_group)]
)
```

## Capture CloudWatch metrics

The code snippet below creates an AWS IoT Rule that capture CloudWatch metrics
when it is triggered.

```python
topic_rule = iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, namespace, unit, value, timestamp FROM 'device/+/data'"),
    actions=[
        actions.CloudWatchPutMetricAction(
            metric_name="${topic(2)}",
            metric_namespace="${namespace}",
            metric_unit="${unit}",
            metric_value="${value}",
            metric_timestamp="${timestamp}"
        )
    ]
)
```

## Change the state of an Amazon CloudWatch alarm

The code snippet below creates an AWS IoT Rule that changes the state of an Amazon CloudWatch alarm when it is triggered:

```python
import monocdk as cloudwatch


metric = cloudwatch.Metric(
    namespace="MyNamespace",
    metric_name="MyMetric",
    dimensions={"MyDimension": "MyDimensionValue"}
)
alarm = cloudwatch.Alarm(self, "MyAlarm",
    metric=metric,
    threshold=100,
    evaluation_periods=3,
    datapoints_to_alarm=2
)

topic_rule = iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id FROM 'device/+/data'"),
    actions=[
        actions.CloudWatchSetAlarmStateAction(alarm,
            reason="AWS Iot Rule action is triggered",
            alarm_state_to_set=cloudwatch.AlarmState.ALARM
        )
    ]
)
```

## Put records to Kinesis Data stream

The code snippet below creates an AWS IoT Rule that put records to Kinesis Data
stream when it is triggered.

```python
import monocdk as kinesis


stream = kinesis.Stream(self, "MyStream")

topic_rule = iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
    actions=[
        actions.KinesisPutRecordAction(stream,
            partition_key="${newuuid()}"
        )
    ]
)
```

## Put records to Kinesis Data Firehose stream

The code snippet below creates an AWS IoT Rule that put records to Put records
to Kinesis Data Firehose stream when it is triggered.

```python
import monocdk as firehose
import monocdk as destinations


bucket = s3.Bucket(self, "MyBucket")
stream = firehose.DeliveryStream(self, "MyStream",
    destinations=[destinations.S3Bucket(bucket)]
)

topic_rule = iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
    actions=[
        actions.FirehosePutRecordAction(stream,
            batch_mode=True,
            record_separator=actions.FirehoseRecordSeparator.NEWLINE
        )
    ]
)
```

## Send messages to an SQS queue

The code snippet below creates an AWS IoT Rule that send messages
to an SQS queue when it is triggered:

```python
import monocdk as sqs


queue = sqs.Queue(self, "MyQueue")

topic_rule = iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
    actions=[
        actions.SqsQueueAction(queue,
            use_base64=True
        )
    ]
)
```

## Publish messages on an SNS topic

The code snippet below creates and AWS IoT Rule that publishes messages to an SNS topic when it is triggered:

```python
import monocdk as sns


topic = sns.Topic(self, "MyTopic")

topic_rule = iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
    actions=[
        actions.SnsTopicAction(topic,
            message_format=actions.SnsActionMessageFormat.JSON
        )
    ]
)
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

from ..aws_cloudwatch import (
    AlarmState as _AlarmState_ca511f67, IAlarm as _IAlarm_bf66c8d0
)
from ..aws_iam import IRole as _IRole_59af6f50
from ..aws_iot import (
    ActionConfig as _ActionConfig_9dc7cb16,
    IAction as _IAction_25dbea23,
    ITopicRule as _ITopicRule_96d74f80,
)
from ..aws_kinesis import IStream as _IStream_14c6ec7f
from ..aws_kinesisfirehose import IDeliveryStream as _IDeliveryStream_2a44232c
from ..aws_lambda import IFunction as _IFunction_6e14f09e
from ..aws_logs import ILogGroup as _ILogGroup_846e17a0
from ..aws_s3 import (
    BucketAccessControl as _BucketAccessControl_a8cb5bce, IBucket as _IBucket_73486e29
)
from ..aws_sns import ITopic as _ITopic_465e36b9
from ..aws_sqs import IQueue as _IQueue_45a01ab4


@jsii.implements(_IAction_25dbea23)
class CloudWatchLogsAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iot_actions.CloudWatchLogsAction",
):
    '''(experimental) The action to send data to Amazon CloudWatch Logs.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as logs
        
        
        log_group = logs.LogGroup(self, "MyLogGroup")
        
        iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp FROM 'device/+/data'"),
            error_action=actions.CloudWatchLogsAction(log_group)
        )
    '''

    def __init__(
        self,
        log_group: _ILogGroup_846e17a0,
        *,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param log_group: The CloudWatch log group to which the action sends data.
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87739eef01b77c15bee1fe50344c6371f216537035a02ad40e70f2b39c91a575)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        props = CloudWatchLogsActionProps(role=role)

        jsii.create(self.__class__, self, [log_group, props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: _ITopicRule_96d74f80) -> _ActionConfig_9dc7cb16:
        '''(experimental) Returns the topic rule action specification.

        :param rule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd1af313fd18209c754e311e1e9ba3c3301ef6328f8bc4bea30a8d4e6ea193f7)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        return typing.cast(_ActionConfig_9dc7cb16, jsii.invoke(self, "bind", [rule]))


@jsii.implements(_IAction_25dbea23)
class CloudWatchPutMetricAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iot_actions.CloudWatchPutMetricAction",
):
    '''(experimental) The action to capture an Amazon CloudWatch metric.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, namespace, unit, value, timestamp FROM 'device/+/data'"),
            actions=[
                actions.CloudWatchPutMetricAction(
                    metric_name="${topic(2)}",
                    metric_namespace="${namespace}",
                    metric_unit="${unit}",
                    metric_value="${value}",
                    metric_timestamp="${timestamp}"
                )
            ]
        )
    '''

    def __init__(
        self,
        *,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        metric_unit: builtins.str,
        metric_value: builtins.str,
        metric_timestamp: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param metric_name: (experimental) The CloudWatch metric name. Supports substitution templates.
        :param metric_namespace: (experimental) The CloudWatch metric namespace name. Supports substitution templates.
        :param metric_unit: (experimental) The metric unit supported by CloudWatch. Supports substitution templates.
        :param metric_value: (experimental) A string that contains the CloudWatch metric value. Supports substitution templates.
        :param metric_timestamp: (experimental) A string that contains the timestamp, expressed in seconds in Unix epoch time. Supports substitution templates. Default: - none -- Defaults to the current Unix epoch time.
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        props = CloudWatchPutMetricActionProps(
            metric_name=metric_name,
            metric_namespace=metric_namespace,
            metric_unit=metric_unit,
            metric_value=metric_value,
            metric_timestamp=metric_timestamp,
            role=role,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: _ITopicRule_96d74f80) -> _ActionConfig_9dc7cb16:
        '''(experimental) Returns the topic rule action specification.

        :param rule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82ceacb7a32011de54c607f3a599882f97673fbdba4a5a0ae8cfbb18e7440fd5)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        return typing.cast(_ActionConfig_9dc7cb16, jsii.invoke(self, "bind", [rule]))


@jsii.implements(_IAction_25dbea23)
class CloudWatchSetAlarmStateAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iot_actions.CloudWatchSetAlarmStateAction",
):
    '''(experimental) The action to change the state of an Amazon CloudWatch alarm.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as cloudwatch
        
        
        metric = cloudwatch.Metric(
            namespace="MyNamespace",
            metric_name="MyMetric",
            dimensions={"MyDimension": "MyDimensionValue"}
        )
        alarm = cloudwatch.Alarm(self, "MyAlarm",
            metric=metric,
            threshold=100,
            evaluation_periods=3,
            datapoints_to_alarm=2
        )
        
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id FROM 'device/+/data'"),
            actions=[
                actions.CloudWatchSetAlarmStateAction(alarm,
                    reason="AWS Iot Rule action is triggered",
                    alarm_state_to_set=cloudwatch.AlarmState.ALARM
                )
            ]
        )
    '''

    def __init__(
        self,
        alarm: _IAlarm_bf66c8d0,
        *,
        alarm_state_to_set: _AlarmState_ca511f67,
        reason: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param alarm: -
        :param alarm_state_to_set: (experimental) The value of the alarm state to set.
        :param reason: (experimental) The reason for the alarm change. Default: None
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2fc79dbab8bcded2ad4fba7222f2e6e1cd1fdd5d330583de46091ebaa54d93c)
            check_type(argname="argument alarm", value=alarm, expected_type=type_hints["alarm"])
        props = CloudWatchSetAlarmStateActionProps(
            alarm_state_to_set=alarm_state_to_set, reason=reason, role=role
        )

        jsii.create(self.__class__, self, [alarm, props])

    @jsii.member(jsii_name="bind")
    def bind(self, topic_rule: _ITopicRule_96d74f80) -> _ActionConfig_9dc7cb16:
        '''(experimental) Returns the topic rule action specification.

        :param topic_rule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffc4f8a12b806cd15e783bb649e58288bed6ec6a8b04662cb9a897bec71cd87c)
            check_type(argname="argument topic_rule", value=topic_rule, expected_type=type_hints["topic_rule"])
        return typing.cast(_ActionConfig_9dc7cb16, jsii.invoke(self, "bind", [topic_rule]))


@jsii.data_type(
    jsii_type="monocdk.aws_iot_actions.CommonActionProps",
    jsii_struct_bases=[],
    name_mapping={"role": "role"},
)
class CommonActionProps:
    def __init__(self, *, role: typing.Optional[_IRole_59af6f50] = None) -> None:
        '''(experimental) Common properties shared by Actions it access to AWS service.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            from monocdk import aws_iot_actions as iot_actions
            
            # role: iam.Role
            
            common_action_props = iot_actions.CommonActionProps(
                role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78da81fcab19ba02a4107fbedc482da07b12333aa5ec0bf1d16dede359a82dd7)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IAction_25dbea23)
class FirehosePutRecordAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iot_actions.FirehosePutRecordAction",
):
    '''(experimental) The action to put the record from an MQTT message to the Kinesis Data Firehose stream.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as firehose
        import monocdk as destinations
        
        
        bucket = s3.Bucket(self, "MyBucket")
        stream = firehose.DeliveryStream(self, "MyStream",
            destinations=[destinations.S3Bucket(bucket)]
        )
        
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
            actions=[
                actions.FirehosePutRecordAction(stream,
                    batch_mode=True,
                    record_separator=actions.FirehoseRecordSeparator.NEWLINE
                )
            ]
        )
    '''

    def __init__(
        self,
        stream: _IDeliveryStream_2a44232c,
        *,
        batch_mode: typing.Optional[builtins.bool] = None,
        record_separator: typing.Optional["FirehoseRecordSeparator"] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param stream: The Kinesis Data Firehose stream to which to put records.
        :param batch_mode: (experimental) Whether to deliver the Kinesis Data Firehose stream as a batch by using ``PutRecordBatch``. When batchMode is true and the rule's SQL statement evaluates to an Array, each Array element forms one record in the PutRecordBatch request. The resulting array can't have more than 500 records. Default: false
        :param record_separator: (experimental) A character separator that will be used to separate records written to the Kinesis Data Firehose stream. Default: - none -- the stream does not use a separator
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c816cd0b131bc2c820dae90881292c3943bc39eaad02ff9f785d8c8d2eb1c93)
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
        props = FirehosePutRecordActionProps(
            batch_mode=batch_mode, record_separator=record_separator, role=role
        )

        jsii.create(self.__class__, self, [stream, props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: _ITopicRule_96d74f80) -> _ActionConfig_9dc7cb16:
        '''(experimental) Returns the topic rule action specification.

        :param rule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__424abef5c2df04545f50c9b049f492fda417280e317e5bae9b7a11434eb1a00d)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        return typing.cast(_ActionConfig_9dc7cb16, jsii.invoke(self, "bind", [rule]))


@jsii.data_type(
    jsii_type="monocdk.aws_iot_actions.FirehosePutRecordActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={
        "role": "role",
        "batch_mode": "batchMode",
        "record_separator": "recordSeparator",
    },
)
class FirehosePutRecordActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_IRole_59af6f50] = None,
        batch_mode: typing.Optional[builtins.bool] = None,
        record_separator: typing.Optional["FirehoseRecordSeparator"] = None,
    ) -> None:
        '''(experimental) Configuration properties of an action for the Kinesis Data Firehose stream.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param batch_mode: (experimental) Whether to deliver the Kinesis Data Firehose stream as a batch by using ``PutRecordBatch``. When batchMode is true and the rule's SQL statement evaluates to an Array, each Array element forms one record in the PutRecordBatch request. The resulting array can't have more than 500 records. Default: false
        :param record_separator: (experimental) A character separator that will be used to separate records written to the Kinesis Data Firehose stream. Default: - none -- the stream does not use a separator

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as firehose
            import monocdk as destinations
            
            
            bucket = s3.Bucket(self, "MyBucket")
            stream = firehose.DeliveryStream(self, "MyStream",
                destinations=[destinations.S3Bucket(bucket)]
            )
            
            topic_rule = iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
                actions=[
                    actions.FirehosePutRecordAction(stream,
                        batch_mode=True,
                        record_separator=actions.FirehoseRecordSeparator.NEWLINE
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a097a37ccda5f0317a1a063b9cdcf79e643932c61080024b08bcc368d680c28)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument batch_mode", value=batch_mode, expected_type=type_hints["batch_mode"])
            check_type(argname="argument record_separator", value=record_separator, expected_type=type_hints["record_separator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role
        if batch_mode is not None:
            self._values["batch_mode"] = batch_mode
        if record_separator is not None:
            self._values["record_separator"] = record_separator

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def batch_mode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to deliver the Kinesis Data Firehose stream as a batch by using ``PutRecordBatch``.

        When batchMode is true and the rule's SQL statement evaluates to an Array, each Array
        element forms one record in the PutRecordBatch request. The resulting array can't have
        more than 500 records.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("batch_mode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def record_separator(self) -> typing.Optional["FirehoseRecordSeparator"]:
        '''(experimental) A character separator that will be used to separate records written to the Kinesis Data Firehose stream.

        :default: - none -- the stream does not use a separator

        :stability: experimental
        '''
        result = self._values.get("record_separator")
        return typing.cast(typing.Optional["FirehoseRecordSeparator"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirehosePutRecordActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_iot_actions.FirehoseRecordSeparator")
class FirehoseRecordSeparator(enum.Enum):
    '''(experimental) Record Separator to be used to separate records.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as firehose
        import monocdk as destinations
        
        
        bucket = s3.Bucket(self, "MyBucket")
        stream = firehose.DeliveryStream(self, "MyStream",
            destinations=[destinations.S3Bucket(bucket)]
        )
        
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
            actions=[
                actions.FirehosePutRecordAction(stream,
                    batch_mode=True,
                    record_separator=actions.FirehoseRecordSeparator.NEWLINE
                )
            ]
        )
    '''

    NEWLINE = "NEWLINE"
    '''(experimental) Separate by a new line.

    :stability: experimental
    '''
    TAB = "TAB"
    '''(experimental) Separate by a tab.

    :stability: experimental
    '''
    WINDOWS_NEWLINE = "WINDOWS_NEWLINE"
    '''(experimental) Separate by a windows new line.

    :stability: experimental
    '''
    COMMA = "COMMA"
    '''(experimental) Separate by a commma.

    :stability: experimental
    '''


@jsii.implements(_IAction_25dbea23)
class IotRepublishMqttAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iot_actions.IotRepublishMqttAction",
):
    '''(experimental) The action to put the record from an MQTT message to republish another MQTT topic.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp, temperature FROM 'device/+/data'"),
            actions=[
                actions.IotRepublishMqttAction("${topic()}/republish",
                    quality_of_service=actions.MqttQualityOfService.AT_LEAST_ONCE
                )
            ]
        )
    '''

    def __init__(
        self,
        topic: builtins.str,
        *,
        quality_of_service: typing.Optional["MqttQualityOfService"] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param topic: The MQTT topic to which to republish the message.
        :param quality_of_service: (experimental) The Quality of Service (QoS) level to use when republishing messages. Default: MqttQualityOfService.ZERO_OR_MORE_TIMES
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab5088d8665aa51bc2bcd70765b3eaaa2905363cdb92a4b907922779eec3a307)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        props = IotRepublishMqttActionProps(
            quality_of_service=quality_of_service, role=role
        )

        jsii.create(self.__class__, self, [topic, props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: _ITopicRule_96d74f80) -> _ActionConfig_9dc7cb16:
        '''(experimental) Returns the topic rule action specification.

        :param rule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c647a03e7aaca68d037b7af6e4109b15535fcf962e35f78b3ee136f8632e59)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        return typing.cast(_ActionConfig_9dc7cb16, jsii.invoke(self, "bind", [rule]))


@jsii.data_type(
    jsii_type="monocdk.aws_iot_actions.IotRepublishMqttActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={"role": "role", "quality_of_service": "qualityOfService"},
)
class IotRepublishMqttActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_IRole_59af6f50] = None,
        quality_of_service: typing.Optional["MqttQualityOfService"] = None,
    ) -> None:
        '''(experimental) Configuration properties of an action to republish MQTT messages.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param quality_of_service: (experimental) The Quality of Service (QoS) level to use when republishing messages. Default: MqttQualityOfService.ZERO_OR_MORE_TIMES

        :stability: experimental
        :exampleMetadata: infused

        Example::

            iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp, temperature FROM 'device/+/data'"),
                actions=[
                    actions.IotRepublishMqttAction("${topic()}/republish",
                        quality_of_service=actions.MqttQualityOfService.AT_LEAST_ONCE
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__574ad7fccee11d236d44ec006fc3aa4964c7398565c227c1f2b398e99e2cb99c)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument quality_of_service", value=quality_of_service, expected_type=type_hints["quality_of_service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role
        if quality_of_service is not None:
            self._values["quality_of_service"] = quality_of_service

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def quality_of_service(self) -> typing.Optional["MqttQualityOfService"]:
        '''(experimental) The Quality of Service (QoS) level to use when republishing messages.

        :default: MqttQualityOfService.ZERO_OR_MORE_TIMES

        :see: https://docs.aws.amazon.com/iot/latest/developerguide/mqtt.html#mqtt-qos
        :stability: experimental
        '''
        result = self._values.get("quality_of_service")
        return typing.cast(typing.Optional["MqttQualityOfService"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotRepublishMqttActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IAction_25dbea23)
class KinesisPutRecordAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iot_actions.KinesisPutRecordAction",
):
    '''(experimental) The action to put the record from an MQTT message to the Kinesis Data stream.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as kinesis
        
        
        stream = kinesis.Stream(self, "MyStream")
        
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
            actions=[
                actions.KinesisPutRecordAction(stream,
                    partition_key="${newuuid()}"
                )
            ]
        )
    '''

    def __init__(
        self,
        stream: _IStream_14c6ec7f,
        *,
        partition_key: builtins.str,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param stream: The Kinesis Data stream to which to put records.
        :param partition_key: (experimental) The partition key used to determine to which shard the data is written. The partition key is usually composed of an expression (for example, ${topic()} or ${timestamp()}).
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__659bc6328cdbc6f40482b77c11b2462a830cef0aef1e4eca239197d6c604574b)
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
        props = KinesisPutRecordActionProps(partition_key=partition_key, role=role)

        jsii.create(self.__class__, self, [stream, props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: _ITopicRule_96d74f80) -> _ActionConfig_9dc7cb16:
        '''(experimental) Returns the topic rule action specification.

        :param rule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcce390c922e17f34f0eb060a3033500c8803a8d410d54f4308c7c76202ff454)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        return typing.cast(_ActionConfig_9dc7cb16, jsii.invoke(self, "bind", [rule]))


@jsii.data_type(
    jsii_type="monocdk.aws_iot_actions.KinesisPutRecordActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={"role": "role", "partition_key": "partitionKey"},
)
class KinesisPutRecordActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_IRole_59af6f50] = None,
        partition_key: builtins.str,
    ) -> None:
        '''(experimental) Configuration properties of an action for the Kinesis Data stream.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param partition_key: (experimental) The partition key used to determine to which shard the data is written. The partition key is usually composed of an expression (for example, ${topic()} or ${timestamp()}).

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as kinesis
            
            
            stream = kinesis.Stream(self, "MyStream")
            
            topic_rule = iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
                actions=[
                    actions.KinesisPutRecordAction(stream,
                        partition_key="${newuuid()}"
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5233c9271f6a07126937e7cf1391a457b343d32945fa146f908b934e3d3732c)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument partition_key", value=partition_key, expected_type=type_hints["partition_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "partition_key": partition_key,
        }
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def partition_key(self) -> builtins.str:
        '''(experimental) The partition key used to determine to which shard the data is written.

        The partition key is usually composed of an expression (for example, ${topic()} or ${timestamp()}).

        :see: https://docs.aws.amazon.com/kinesis/latest/APIReference/API_PutRecord.html#API_PutRecord_RequestParameters
        :stability: experimental
        '''
        result = self._values.get("partition_key")
        assert result is not None, "Required property 'partition_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisPutRecordActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IAction_25dbea23)
class LambdaFunctionAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iot_actions.LambdaFunctionAction",
):
    '''(experimental) The action to invoke an AWS Lambda function, passing in an MQTT message.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        func = lambda_.Function(self, "MyFunction",
            runtime=lambda_.Runtime.NODEJS_14_X,
            handler="index.handler",
            code=lambda_.Code.from_inline("""
                    exports.handler = (event) => {
                      console.log("It is test for lambda action of AWS IoT Rule.", event);
                    };""")
        )
        
        iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp, temperature FROM 'device/+/data'"),
            actions=[actions.LambdaFunctionAction(func)]
        )
    '''

    def __init__(self, func: _IFunction_6e14f09e) -> None:
        '''
        :param func: The lambda function to be invoked by this action.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cc1848ab9783465ff7f9cce54e608b510bdc8e1e3520d8fe44e6d99855b47eb)
            check_type(argname="argument func", value=func, expected_type=type_hints["func"])
        jsii.create(self.__class__, self, [func])

    @jsii.member(jsii_name="bind")
    def bind(self, topic_rule: _ITopicRule_96d74f80) -> _ActionConfig_9dc7cb16:
        '''(experimental) Returns the topic rule action specification.

        :param topic_rule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8033a5f15d9937e75f94ba46e9e96d829ed804fda5b93f7fd7d26a9320d7582d)
            check_type(argname="argument topic_rule", value=topic_rule, expected_type=type_hints["topic_rule"])
        return typing.cast(_ActionConfig_9dc7cb16, jsii.invoke(self, "bind", [topic_rule]))


@jsii.enum(jsii_type="monocdk.aws_iot_actions.MqttQualityOfService")
class MqttQualityOfService(enum.Enum):
    '''(experimental) MQTT Quality of Service (QoS) indicates the level of assurance for delivery of an MQTT Message.

    :see: https://docs.aws.amazon.com/iot/latest/developerguide/mqtt.html#mqtt-qos
    :stability: experimental
    :exampleMetadata: infused

    Example::

        iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp, temperature FROM 'device/+/data'"),
            actions=[
                actions.IotRepublishMqttAction("${topic()}/republish",
                    quality_of_service=actions.MqttQualityOfService.AT_LEAST_ONCE
                )
            ]
        )
    '''

    ZERO_OR_MORE_TIMES = "ZERO_OR_MORE_TIMES"
    '''(experimental) QoS level 0.

    Sent zero or more times.
    This level should be used for messages that are sent over reliable communication links or that can be missed without a problem.

    :stability: experimental
    '''
    AT_LEAST_ONCE = "AT_LEAST_ONCE"
    '''(experimental) QoS level 1.

    Sent at least one time, and then repeatedly until a PUBACK response is received.
    The message is not considered complete until the sender receives a PUBACK response to indicate successful delivery.

    :stability: experimental
    '''


@jsii.implements(_IAction_25dbea23)
class S3PutObjectAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iot_actions.S3PutObjectAction",
):
    '''(experimental) The action to write the data from an MQTT message to an Amazon S3 bucket.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        bucket = s3.Bucket(self, "MyBucket")
        
        iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
            actions=[
                actions.S3PutObjectAction(bucket,
                    key="${year}/${month}/${day}/${topic(2)}"
                )
            ]
        )
    '''

    def __init__(
        self,
        bucket: _IBucket_73486e29,
        *,
        access_control: typing.Optional[_BucketAccessControl_a8cb5bce] = None,
        key: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param bucket: The Amazon S3 bucket to which to write data.
        :param access_control: (experimental) The Amazon S3 canned ACL that controls access to the object identified by the object key. Default: None
        :param key: (experimental) The path to the file where the data is written. Supports substitution templates. Default: '${topic()}/${timestamp()}'
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eb98179b4ef7114bff3a9d6edd005fb35a86be993ebd0ff127310b95d0fe2fe)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        props = S3PutObjectActionProps(
            access_control=access_control, key=key, role=role
        )

        jsii.create(self.__class__, self, [bucket, props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: _ITopicRule_96d74f80) -> _ActionConfig_9dc7cb16:
        '''(experimental) Returns the topic rule action specification.

        :param rule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42b0788ef11e87e1b56dd9432e2b8b04eefc4be53c446618d11415d987983409)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        return typing.cast(_ActionConfig_9dc7cb16, jsii.invoke(self, "bind", [rule]))


@jsii.data_type(
    jsii_type="monocdk.aws_iot_actions.S3PutObjectActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={"role": "role", "access_control": "accessControl", "key": "key"},
)
class S3PutObjectActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_IRole_59af6f50] = None,
        access_control: typing.Optional[_BucketAccessControl_a8cb5bce] = None,
        key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configuration properties of an action for s3.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param access_control: (experimental) The Amazon S3 canned ACL that controls access to the object identified by the object key. Default: None
        :param key: (experimental) The path to the file where the data is written. Supports substitution templates. Default: '${topic()}/${timestamp()}'

        :stability: experimental
        :exampleMetadata: infused

        Example::

            bucket = s3.Bucket(self, "MyBucket")
            
            iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
                actions=[
                    actions.S3PutObjectAction(bucket,
                        key="${year}/${month}/${day}/${topic(2)}"
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f502dd552d3dd1dfb05696efe167d11d3231930dab1edb9005cb94affe559e1)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument access_control", value=access_control, expected_type=type_hints["access_control"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role
        if access_control is not None:
            self._values["access_control"] = access_control
        if key is not None:
            self._values["key"] = key

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def access_control(self) -> typing.Optional[_BucketAccessControl_a8cb5bce]:
        '''(experimental) The Amazon S3 canned ACL that controls access to the object identified by the object key.

        :default: None

        :see: https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html#canned-acl
        :stability: experimental
        '''
        result = self._values.get("access_control")
        return typing.cast(typing.Optional[_BucketAccessControl_a8cb5bce], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path to the file where the data is written.

        Supports substitution templates.

        :default: '${topic()}/${timestamp()}'

        :see: https://docs.aws.amazon.com/iot/latest/developerguide/iot-substitution-templates.html
        :stability: experimental
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3PutObjectActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_iot_actions.SnsActionMessageFormat")
class SnsActionMessageFormat(enum.Enum):
    '''(experimental) SNS topic action message format options.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as sns
        
        
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

    RAW = "RAW"
    '''(experimental) RAW message format.

    :stability: experimental
    '''
    JSON = "JSON"
    '''(experimental) JSON message format.

    :stability: experimental
    '''


@jsii.implements(_IAction_25dbea23)
class SnsTopicAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iot_actions.SnsTopicAction",
):
    '''(experimental) The action to write the data from an MQTT message to an Amazon SNS topic.

    :see: https://docs.aws.amazon.com/iot/latest/developerguide/sns-rule-action.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as sns
        
        
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
        topic: _ITopic_465e36b9,
        *,
        message_format: typing.Optional[SnsActionMessageFormat] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param topic: The Amazon SNS topic to publish data on. Must not be a FIFO topic.
        :param message_format: (experimental) The message format of the message to publish. SNS uses this setting to determine if the payload should be parsed and relevant platform-specific bits of the payload should be extracted. Default: SnsActionMessageFormat.RAW
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b35e6b32920e3349f48b8cd4c3e9e6a2a7504978922b92a5a287d7852b968e5)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        props = SnsTopicActionProps(message_format=message_format, role=role)

        jsii.create(self.__class__, self, [topic, props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: _ITopicRule_96d74f80) -> _ActionConfig_9dc7cb16:
        '''(experimental) Returns the topic rule action specification.

        :param rule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__286e2f8243a0c069c7c1f179060bc6a13b63a03c6423ce930fc4c200460924ad)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        return typing.cast(_ActionConfig_9dc7cb16, jsii.invoke(self, "bind", [rule]))


@jsii.data_type(
    jsii_type="monocdk.aws_iot_actions.SnsTopicActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={"role": "role", "message_format": "messageFormat"},
)
class SnsTopicActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_IRole_59af6f50] = None,
        message_format: typing.Optional[SnsActionMessageFormat] = None,
    ) -> None:
        '''(experimental) Configuration options for the SNS topic action.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param message_format: (experimental) The message format of the message to publish. SNS uses this setting to determine if the payload should be parsed and relevant platform-specific bits of the payload should be extracted. Default: SnsActionMessageFormat.RAW

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as sns
            
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__06471ff7c10be6179632efbac86e0f22e84cbbfe5e89bbd44d7e196ae05359bd)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument message_format", value=message_format, expected_type=type_hints["message_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role
        if message_format is not None:
            self._values["message_format"] = message_format

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def message_format(self) -> typing.Optional[SnsActionMessageFormat]:
        '''(experimental) The message format of the message to publish.

        SNS uses this setting to determine if the payload should be parsed and relevant platform-specific bits of the payload should be extracted.

        :default: SnsActionMessageFormat.RAW

        :see: https://docs.aws.amazon.com/sns/latest/dg/sns-message-and-json-formats.html
        :stability: experimental
        '''
        result = self._values.get("message_format")
        return typing.cast(typing.Optional[SnsActionMessageFormat], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsTopicActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IAction_25dbea23)
class SqsQueueAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iot_actions.SqsQueueAction",
):
    '''(experimental) The action to write the data from an MQTT message to an Amazon SQS queue.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as sqs
        
        
        queue = sqs.Queue(self, "MyQueue")
        
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
            actions=[
                actions.SqsQueueAction(queue,
                    use_base64=True
                )
            ]
        )
    '''

    def __init__(
        self,
        queue: _IQueue_45a01ab4,
        *,
        use_base64: typing.Optional[builtins.bool] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param queue: The Amazon SQS queue to which to write data.
        :param use_base64: (experimental) Specifies whether to use Base64 encoding. Default: false
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__751ef410a7f9f870ff16f65c6b5f87ef7bbbd114deacc9a951395f910dfc7640)
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        props = SqsQueueActionProps(use_base64=use_base64, role=role)

        jsii.create(self.__class__, self, [queue, props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: _ITopicRule_96d74f80) -> _ActionConfig_9dc7cb16:
        '''(experimental) Returns the topic rule action specification.

        :param rule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbde524684563f76b950d9667106992e7b043c29130c53de10bc15ce58d7a3c7)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        return typing.cast(_ActionConfig_9dc7cb16, jsii.invoke(self, "bind", [rule]))


@jsii.data_type(
    jsii_type="monocdk.aws_iot_actions.SqsQueueActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={"role": "role", "use_base64": "useBase64"},
)
class SqsQueueActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_IRole_59af6f50] = None,
        use_base64: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Configuration properties of an action for SQS.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param use_base64: (experimental) Specifies whether to use Base64 encoding. Default: false

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as sqs
            
            
            queue = sqs.Queue(self, "MyQueue")
            
            topic_rule = iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
                actions=[
                    actions.SqsQueueAction(queue,
                        use_base64=True
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5214bd046c4d6113ff716f0cb431a716c3e3093c6438673b6aa9aa3da3d34d73)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument use_base64", value=use_base64, expected_type=type_hints["use_base64"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role
        if use_base64 is not None:
            self._values["use_base64"] = use_base64

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def use_base64(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether to use Base64 encoding.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("use_base64")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsQueueActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_iot_actions.CloudWatchLogsActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={"role": "role"},
)
class CloudWatchLogsActionProps(CommonActionProps):
    def __init__(self, *, role: typing.Optional[_IRole_59af6f50] = None) -> None:
        '''(experimental) Configuration properties of an action for CloudWatch Logs.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            from monocdk import aws_iot_actions as iot_actions
            
            # role: iam.Role
            
            cloud_watch_logs_action_props = iot_actions.CloudWatchLogsActionProps(
                role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45ff0a822b74f98a16ad4d09902d65feca61f59772ac2f9a986383c4c9405b91)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudWatchLogsActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_iot_actions.CloudWatchPutMetricActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={
        "role": "role",
        "metric_name": "metricName",
        "metric_namespace": "metricNamespace",
        "metric_unit": "metricUnit",
        "metric_value": "metricValue",
        "metric_timestamp": "metricTimestamp",
    },
)
class CloudWatchPutMetricActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_IRole_59af6f50] = None,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        metric_unit: builtins.str,
        metric_value: builtins.str,
        metric_timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configuration properties of an action for CloudWatch metric.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param metric_name: (experimental) The CloudWatch metric name. Supports substitution templates.
        :param metric_namespace: (experimental) The CloudWatch metric namespace name. Supports substitution templates.
        :param metric_unit: (experimental) The metric unit supported by CloudWatch. Supports substitution templates.
        :param metric_value: (experimental) A string that contains the CloudWatch metric value. Supports substitution templates.
        :param metric_timestamp: (experimental) A string that contains the timestamp, expressed in seconds in Unix epoch time. Supports substitution templates. Default: - none -- Defaults to the current Unix epoch time.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            topic_rule = iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, namespace, unit, value, timestamp FROM 'device/+/data'"),
                actions=[
                    actions.CloudWatchPutMetricAction(
                        metric_name="${topic(2)}",
                        metric_namespace="${namespace}",
                        metric_unit="${unit}",
                        metric_value="${value}",
                        metric_timestamp="${timestamp}"
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4b25f6eb9232ba1e58dbe9b09ff09b97fb474e0747764ed1144f24771b42ae2)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument metric_unit", value=metric_unit, expected_type=type_hints["metric_unit"])
            check_type(argname="argument metric_value", value=metric_value, expected_type=type_hints["metric_value"])
            check_type(argname="argument metric_timestamp", value=metric_timestamp, expected_type=type_hints["metric_timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_name": metric_name,
            "metric_namespace": metric_namespace,
            "metric_unit": metric_unit,
            "metric_value": metric_value,
        }
        if role is not None:
            self._values["role"] = role
        if metric_timestamp is not None:
            self._values["metric_timestamp"] = metric_timestamp

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''(experimental) The CloudWatch metric name.

        Supports substitution templates.

        :see: https://docs.aws.amazon.com/iot/latest/developerguide/iot-substitution-templates.html
        :stability: experimental
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_namespace(self) -> builtins.str:
        '''(experimental) The CloudWatch metric namespace name.

        Supports substitution templates.

        :see: https://docs.aws.amazon.com/iot/latest/developerguide/iot-substitution-templates.html
        :stability: experimental
        '''
        result = self._values.get("metric_namespace")
        assert result is not None, "Required property 'metric_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_unit(self) -> builtins.str:
        '''(experimental) The metric unit supported by CloudWatch.

        Supports substitution templates.

        :see: https://docs.aws.amazon.com/iot/latest/developerguide/iot-substitution-templates.html
        :stability: experimental
        '''
        result = self._values.get("metric_unit")
        assert result is not None, "Required property 'metric_unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_value(self) -> builtins.str:
        '''(experimental) A string that contains the CloudWatch metric value.

        Supports substitution templates.

        :see: https://docs.aws.amazon.com/iot/latest/developerguide/iot-substitution-templates.html
        :stability: experimental
        '''
        result = self._values.get("metric_value")
        assert result is not None, "Required property 'metric_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_timestamp(self) -> typing.Optional[builtins.str]:
        '''(experimental) A string that contains the timestamp, expressed in seconds in Unix epoch time.

        Supports substitution templates.

        :default: - none -- Defaults to the current Unix epoch time.

        :see: https://docs.aws.amazon.com/iot/latest/developerguide/iot-substitution-templates.html
        :stability: experimental
        '''
        result = self._values.get("metric_timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudWatchPutMetricActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_iot_actions.CloudWatchSetAlarmStateActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={
        "role": "role",
        "alarm_state_to_set": "alarmStateToSet",
        "reason": "reason",
    },
)
class CloudWatchSetAlarmStateActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_IRole_59af6f50] = None,
        alarm_state_to_set: _AlarmState_ca511f67,
        reason: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configuration properties of an action for CloudWatch alarm.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param alarm_state_to_set: (experimental) The value of the alarm state to set.
        :param reason: (experimental) The reason for the alarm change. Default: None

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as cloudwatch
            
            
            metric = cloudwatch.Metric(
                namespace="MyNamespace",
                metric_name="MyMetric",
                dimensions={"MyDimension": "MyDimensionValue"}
            )
            alarm = cloudwatch.Alarm(self, "MyAlarm",
                metric=metric,
                threshold=100,
                evaluation_periods=3,
                datapoints_to_alarm=2
            )
            
            topic_rule = iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id FROM 'device/+/data'"),
                actions=[
                    actions.CloudWatchSetAlarmStateAction(alarm,
                        reason="AWS Iot Rule action is triggered",
                        alarm_state_to_set=cloudwatch.AlarmState.ALARM
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ff7d107b2d012fb1de6d9f58839420f15f8175329832620822985e9e11646e6)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument alarm_state_to_set", value=alarm_state_to_set, expected_type=type_hints["alarm_state_to_set"])
            check_type(argname="argument reason", value=reason, expected_type=type_hints["reason"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alarm_state_to_set": alarm_state_to_set,
        }
        if role is not None:
            self._values["role"] = role
        if reason is not None:
            self._values["reason"] = reason

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def alarm_state_to_set(self) -> _AlarmState_ca511f67:
        '''(experimental) The value of the alarm state to set.

        :stability: experimental
        '''
        result = self._values.get("alarm_state_to_set")
        assert result is not None, "Required property 'alarm_state_to_set' is missing"
        return typing.cast(_AlarmState_ca511f67, result)

    @builtins.property
    def reason(self) -> typing.Optional[builtins.str]:
        '''(experimental) The reason for the alarm change.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("reason")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudWatchSetAlarmStateActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CloudWatchLogsAction",
    "CloudWatchLogsActionProps",
    "CloudWatchPutMetricAction",
    "CloudWatchPutMetricActionProps",
    "CloudWatchSetAlarmStateAction",
    "CloudWatchSetAlarmStateActionProps",
    "CommonActionProps",
    "FirehosePutRecordAction",
    "FirehosePutRecordActionProps",
    "FirehoseRecordSeparator",
    "IotRepublishMqttAction",
    "IotRepublishMqttActionProps",
    "KinesisPutRecordAction",
    "KinesisPutRecordActionProps",
    "LambdaFunctionAction",
    "MqttQualityOfService",
    "S3PutObjectAction",
    "S3PutObjectActionProps",
    "SnsActionMessageFormat",
    "SnsTopicAction",
    "SnsTopicActionProps",
    "SqsQueueAction",
    "SqsQueueActionProps",
]

publication.publish()

def _typecheckingstub__87739eef01b77c15bee1fe50344c6371f216537035a02ad40e70f2b39c91a575(
    log_group: _ILogGroup_846e17a0,
    *,
    role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd1af313fd18209c754e311e1e9ba3c3301ef6328f8bc4bea30a8d4e6ea193f7(
    rule: _ITopicRule_96d74f80,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82ceacb7a32011de54c607f3a599882f97673fbdba4a5a0ae8cfbb18e7440fd5(
    rule: _ITopicRule_96d74f80,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2fc79dbab8bcded2ad4fba7222f2e6e1cd1fdd5d330583de46091ebaa54d93c(
    alarm: _IAlarm_bf66c8d0,
    *,
    alarm_state_to_set: _AlarmState_ca511f67,
    reason: typing.Optional[builtins.str] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffc4f8a12b806cd15e783bb649e58288bed6ec6a8b04662cb9a897bec71cd87c(
    topic_rule: _ITopicRule_96d74f80,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78da81fcab19ba02a4107fbedc482da07b12333aa5ec0bf1d16dede359a82dd7(
    *,
    role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c816cd0b131bc2c820dae90881292c3943bc39eaad02ff9f785d8c8d2eb1c93(
    stream: _IDeliveryStream_2a44232c,
    *,
    batch_mode: typing.Optional[builtins.bool] = None,
    record_separator: typing.Optional[FirehoseRecordSeparator] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424abef5c2df04545f50c9b049f492fda417280e317e5bae9b7a11434eb1a00d(
    rule: _ITopicRule_96d74f80,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a097a37ccda5f0317a1a063b9cdcf79e643932c61080024b08bcc368d680c28(
    *,
    role: typing.Optional[_IRole_59af6f50] = None,
    batch_mode: typing.Optional[builtins.bool] = None,
    record_separator: typing.Optional[FirehoseRecordSeparator] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5088d8665aa51bc2bcd70765b3eaaa2905363cdb92a4b907922779eec3a307(
    topic: builtins.str,
    *,
    quality_of_service: typing.Optional[MqttQualityOfService] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c647a03e7aaca68d037b7af6e4109b15535fcf962e35f78b3ee136f8632e59(
    rule: _ITopicRule_96d74f80,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574ad7fccee11d236d44ec006fc3aa4964c7398565c227c1f2b398e99e2cb99c(
    *,
    role: typing.Optional[_IRole_59af6f50] = None,
    quality_of_service: typing.Optional[MqttQualityOfService] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__659bc6328cdbc6f40482b77c11b2462a830cef0aef1e4eca239197d6c604574b(
    stream: _IStream_14c6ec7f,
    *,
    partition_key: builtins.str,
    role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcce390c922e17f34f0eb060a3033500c8803a8d410d54f4308c7c76202ff454(
    rule: _ITopicRule_96d74f80,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5233c9271f6a07126937e7cf1391a457b343d32945fa146f908b934e3d3732c(
    *,
    role: typing.Optional[_IRole_59af6f50] = None,
    partition_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc1848ab9783465ff7f9cce54e608b510bdc8e1e3520d8fe44e6d99855b47eb(
    func: _IFunction_6e14f09e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8033a5f15d9937e75f94ba46e9e96d829ed804fda5b93f7fd7d26a9320d7582d(
    topic_rule: _ITopicRule_96d74f80,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb98179b4ef7114bff3a9d6edd005fb35a86be993ebd0ff127310b95d0fe2fe(
    bucket: _IBucket_73486e29,
    *,
    access_control: typing.Optional[_BucketAccessControl_a8cb5bce] = None,
    key: typing.Optional[builtins.str] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42b0788ef11e87e1b56dd9432e2b8b04eefc4be53c446618d11415d987983409(
    rule: _ITopicRule_96d74f80,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f502dd552d3dd1dfb05696efe167d11d3231930dab1edb9005cb94affe559e1(
    *,
    role: typing.Optional[_IRole_59af6f50] = None,
    access_control: typing.Optional[_BucketAccessControl_a8cb5bce] = None,
    key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b35e6b32920e3349f48b8cd4c3e9e6a2a7504978922b92a5a287d7852b968e5(
    topic: _ITopic_465e36b9,
    *,
    message_format: typing.Optional[SnsActionMessageFormat] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286e2f8243a0c069c7c1f179060bc6a13b63a03c6423ce930fc4c200460924ad(
    rule: _ITopicRule_96d74f80,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06471ff7c10be6179632efbac86e0f22e84cbbfe5e89bbd44d7e196ae05359bd(
    *,
    role: typing.Optional[_IRole_59af6f50] = None,
    message_format: typing.Optional[SnsActionMessageFormat] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__751ef410a7f9f870ff16f65c6b5f87ef7bbbd114deacc9a951395f910dfc7640(
    queue: _IQueue_45a01ab4,
    *,
    use_base64: typing.Optional[builtins.bool] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbde524684563f76b950d9667106992e7b043c29130c53de10bc15ce58d7a3c7(
    rule: _ITopicRule_96d74f80,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5214bd046c4d6113ff716f0cb431a716c3e3093c6438673b6aa9aa3da3d34d73(
    *,
    role: typing.Optional[_IRole_59af6f50] = None,
    use_base64: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ff0a822b74f98a16ad4d09902d65feca61f59772ac2f9a986383c4c9405b91(
    *,
    role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4b25f6eb9232ba1e58dbe9b09ff09b97fb474e0747764ed1144f24771b42ae2(
    *,
    role: typing.Optional[_IRole_59af6f50] = None,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    metric_unit: builtins.str,
    metric_value: builtins.str,
    metric_timestamp: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff7d107b2d012fb1de6d9f58839420f15f8175329832620822985e9e11646e6(
    *,
    role: typing.Optional[_IRole_59af6f50] = None,
    alarm_state_to_set: _AlarmState_ca511f67,
    reason: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
