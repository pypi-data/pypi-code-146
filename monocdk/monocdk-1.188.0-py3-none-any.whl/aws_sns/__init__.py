'''
# Amazon Simple Notification Service Construct Library

Add an SNS Topic to your stack:

```python
topic = sns.Topic(self, "Topic",
    display_name="Customer subscription topic"
)
```

Add a FIFO SNS topic with content-based de-duplication to your stack:

```python
topic = sns.Topic(self, "Topic",
    content_based_deduplication=True,
    display_name="Customer subscription topic",
    fifo=True,
    topic_name="customerTopic"
)
```

Note that FIFO topics require a topic name to be provided. The required `.fifo` suffix will be automatically added to the topic name if it is not explicitly provided.

## Subscriptions

Various subscriptions can be added to the topic by calling the
`.addSubscription(...)` method on the topic. It accepts a *subscription* object,
default implementations of which can be found in the
`@aws-cdk/aws-sns-subscriptions` package:

Add an HTTPS Subscription to your topic:

```python
my_topic = sns.Topic(self, "MyTopic")

my_topic.add_subscription(subscriptions.UrlSubscription("https://foobar.com/"))
```

Subscribe a queue to the topic:

```python
# queue: sqs.Queue

my_topic = sns.Topic(self, "MyTopic")

my_topic.add_subscription(subscriptions.SqsSubscription(queue))
```

Note that subscriptions of queues in different accounts need to be manually confirmed by
reading the initial message from the queue and visiting the link found in it.

### Filter policy

A filter policy can be specified when subscribing an endpoint to a topic.

Example with a Lambda subscription:

```python
import monocdk as lambda_
# fn: lambda.Function


my_topic = sns.Topic(self, "MyTopic")

# Lambda should receive only message matching the following conditions on attributes:
# color: 'red' or 'orange' or begins with 'bl'
# size: anything but 'small' or 'medium'
# price: between 100 and 200 or greater than 300
# store: attribute must be present
my_topic.add_subscription(subscriptions.LambdaSubscription(fn,
    filter_policy={
        "color": sns.SubscriptionFilter.string_filter(
            allowlist=["red", "orange"],
            match_prefixes=["bl"]
        ),
        "size": sns.SubscriptionFilter.string_filter(
            denylist=["small", "medium"]
        ),
        "price": sns.SubscriptionFilter.numeric_filter(
            between=lambda.aws_sns.BetweenCondition(start=100, stop=200),
            greater_than=300
        ),
        "store": sns.SubscriptionFilter.exists_filter()
    }
))
```

### Example of Firehose Subscription

```python
from monocdk.aws_kinesisfirehose import DeliveryStream
# stream: DeliveryStream


topic = sns.Topic(self, "Topic")

sns.Subscription(self, "Subscription",
    topic=topic,
    endpoint=stream.delivery_stream_arn,
    protocol=sns.SubscriptionProtocol.FIREHOSE,
    subscription_role_arn="SAMPLE_ARN"
)
```

## DLQ setup for SNS Subscription

CDK can attach provided Queue as DLQ for your SNS subscription.
See the [SNS DLQ configuration docs](https://docs.aws.amazon.com/sns/latest/dg/sns-configure-dead-letter-queue.html) for more information about this feature.

Example of usage with user provided DLQ.

```python
topic = sns.Topic(self, "Topic")
dl_queue = sqs.Queue(self, "DeadLetterQueue",
    queue_name="MySubscription_DLQ",
    retention_period=Duration.days(14)
)

sns.Subscription(self, "Subscription",
    endpoint="endpoint",
    protocol=sns.SubscriptionProtocol.LAMBDA,
    topic=topic,
    dead_letter_queue=dl_queue
)
```

## CloudWatch Event Rule Target

SNS topics can be used as targets for CloudWatch event rules.

Use the `@aws-cdk/aws-events-targets.SnsTopic`:

```python
import monocdk as codecommit
import monocdk as targets

# repo: codecommit.Repository

my_topic = sns.Topic(self, "Topic")

repo.on_commit("OnCommit",
    target=targets.SnsTopic(my_topic)
)
```

This will result in adding a target to the event rule and will also modify the
topic resource policy to allow CloudWatch events to publish to the topic.

## Topic Policy

A topic policy is automatically created when `addToResourcePolicy` is called, if
one doesn't already exist. Using `addToResourcePolicy` is the simplest way to
add policies, but a `TopicPolicy` can also be created manually.

```python
topic = sns.Topic(self, "Topic")
topic_policy = sns.TopicPolicy(self, "TopicPolicy",
    topics=[topic]
)

topic_policy.document.add_statements(iam.PolicyStatement(
    actions=["sns:Subscribe"],
    principals=[iam.AnyPrincipal()],
    resources=[topic.topic_arn]
))
```

A policy document can also be passed on `TopicPolicy` construction

```python
topic = sns.Topic(self, "Topic")
policy_document = iam.PolicyDocument(
    assign_sids=True,
    statements=[
        iam.PolicyStatement(
            actions=["sns:Subscribe"],
            principals=[iam.AnyPrincipal()],
            resources=[topic.topic_arn]
        )
    ]
)

topic_policy = sns.TopicPolicy(self, "Policy",
    topics=[topic],
    policy_document=policy_document
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

import constructs as _constructs_77d1e7e8
from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    Duration as _Duration_070aa057,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    Resource as _Resource_abff4495,
    ResourceProps as _ResourceProps_9b554c0f,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_cloudwatch import (
    Metric as _Metric_5b2b8e58,
    MetricOptions as _MetricOptions_1c185ae8,
    Unit as _Unit_113c79f9,
)
from ..aws_codestarnotifications import (
    INotificationRuleTarget as _INotificationRuleTarget_31f512df,
    NotificationRuleTargetConfig as _NotificationRuleTargetConfig_a582558e,
)
from ..aws_iam import (
    AddToResourcePolicyResult as _AddToResourcePolicyResult_0fd9d2a9,
    Grant as _Grant_bcb5eae7,
    IGrantable as _IGrantable_4c5a91d1,
    PolicyDocument as _PolicyDocument_b5de5177,
    PolicyStatement as _PolicyStatement_296fe8a3,
)
from ..aws_kms import IKey as _IKey_36930160
from ..aws_sqs import IQueue as _IQueue_45a01ab4


@jsii.data_type(
    jsii_type="monocdk.aws_sns.BetweenCondition",
    jsii_struct_bases=[],
    name_mapping={"start": "start", "stop": "stop"},
)
class BetweenCondition:
    def __init__(self, *, start: jsii.Number, stop: jsii.Number) -> None:
        '''(experimental) Between condition for a numeric attribute.

        :param start: (experimental) The start value.
        :param stop: (experimental) The stop value.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as lambda_
            # fn: lambda.Function
            
            
            my_topic = sns.Topic(self, "MyTopic")
            
            # Lambda should receive only message matching the following conditions on attributes:
            # color: 'red' or 'orange' or begins with 'bl'
            # size: anything but 'small' or 'medium'
            # price: between 100 and 200 or greater than 300
            # store: attribute must be present
            my_topic.add_subscription(subscriptions.LambdaSubscription(fn,
                filter_policy={
                    "color": sns.SubscriptionFilter.string_filter(
                        allowlist=["red", "orange"],
                        match_prefixes=["bl"]
                    ),
                    "size": sns.SubscriptionFilter.string_filter(
                        denylist=["small", "medium"]
                    ),
                    "price": sns.SubscriptionFilter.numeric_filter(
                        between=lambda.aws_sns.BetweenCondition(start=100, stop=200),
                        greater_than=300
                    ),
                    "store": sns.SubscriptionFilter.exists_filter()
                }
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bcba6f40d1e40e50e482fae9fd174fa4286f24b64edbcc8abbccff860899bf4)
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            check_type(argname="argument stop", value=stop, expected_type=type_hints["stop"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "start": start,
            "stop": stop,
        }

    @builtins.property
    def start(self) -> jsii.Number:
        '''(experimental) The start value.

        :stability: experimental
        '''
        result = self._values.get("start")
        assert result is not None, "Required property 'start' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def stop(self) -> jsii.Number:
        '''(experimental) The stop value.

        :stability: experimental
        '''
        result = self._values.get("stop")
        assert result is not None, "Required property 'stop' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BetweenCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSubscription(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sns.CfnSubscription",
):
    '''A CloudFormation ``AWS::SNS::Subscription``.

    The ``AWS::SNS::Subscription`` resource subscribes an endpoint to an Amazon SNS topic. For a subscription to be created, the owner of the endpoint must confirm the subscription.

    :cloudformationResource: AWS::SNS::Subscription
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_sns as sns
        
        # delivery_policy: Any
        # filter_policy: Any
        # redrive_policy: Any
        
        cfn_subscription = sns.CfnSubscription(self, "MyCfnSubscription",
            protocol="protocol",
            topic_arn="topicArn",
        
            # the properties below are optional
            delivery_policy=delivery_policy,
            endpoint="endpoint",
            filter_policy=filter_policy,
            filter_policy_scope="filterPolicyScope",
            raw_message_delivery=False,
            redrive_policy=redrive_policy,
            region="region",
            subscription_role_arn="subscriptionRoleArn"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        protocol: builtins.str,
        topic_arn: builtins.str,
        delivery_policy: typing.Any = None,
        endpoint: typing.Optional[builtins.str] = None,
        filter_policy: typing.Any = None,
        filter_policy_scope: typing.Optional[builtins.str] = None,
        raw_message_delivery: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        redrive_policy: typing.Any = None,
        region: typing.Optional[builtins.str] = None,
        subscription_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::SNS::Subscription``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param protocol: The subscription's protocol. For more information, see the ``Protocol`` parameter of the ``[Subscribe](https://docs.aws.amazon.com/sns/latest/api/API_Subscribe.html)`` action in the *Amazon SNS API Reference* .
        :param topic_arn: The ARN of the topic to subscribe to.
        :param delivery_policy: The delivery policy JSON assigned to the subscription. Enables the subscriber to define the message delivery retry strategy in the case of an HTTP/S endpoint subscribed to the topic. For more information, see ``[GetSubscriptionAttributes](https://docs.aws.amazon.com/sns/latest/api/API_GetSubscriptionAttributes.html)`` in the *Amazon SNS API Reference* and `Message delivery retries <https://docs.aws.amazon.com/sns/latest/dg/sns-message-delivery-retries.html>`_ in the *Amazon SNS Developer Guide* .
        :param endpoint: The subscription's endpoint. The endpoint value depends on the protocol that you specify. For more information, see the ``Endpoint`` parameter of the ``[Subscribe](https://docs.aws.amazon.com/sns/latest/api/API_Subscribe.html)`` action in the *Amazon SNS API Reference* .
        :param filter_policy: The filter policy JSON assigned to the subscription. Enables the subscriber to filter out unwanted messages. For more information, see ``[GetSubscriptionAttributes](https://docs.aws.amazon.com/sns/latest/api/API_GetSubscriptionAttributes.html)`` in the *Amazon SNS API Reference* and `Message filtering <https://docs.aws.amazon.com/sns/latest/dg/sns-message-filtering.html>`_ in the *Amazon SNS Developer Guide* . - ``FilterPolicyScope`` - This attribute lets you choose the filtering scope by using one of the following string value types: - ``MessageAttributes`` (default) - The filter is applied on the message attributes. - ``MessageBody`` - The filter is applied on the message body.
        :param filter_policy_scope: ``AWS::SNS::Subscription.FilterPolicyScope``.
        :param raw_message_delivery: When set to ``true`` , enables raw message delivery. Raw messages don't contain any JSON formatting and can be sent to Amazon SQS and HTTP/S endpoints. For more information, see ``[GetSubscriptionAttributes](https://docs.aws.amazon.com/sns/latest/api/API_GetSubscriptionAttributes.html)`` in the *Amazon SNS API Reference* .
        :param redrive_policy: When specified, sends undeliverable messages to the specified Amazon SQS dead-letter queue. Messages that can't be delivered due to client errors (for example, when the subscribed endpoint is unreachable) or server errors (for example, when the service that powers the subscribed endpoint becomes unavailable) are held in the dead-letter queue for further analysis or reprocessing. For more information about the redrive policy and dead-letter queues, see `Amazon SQS dead-letter queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html>`_ in the *Amazon SQS Developer Guide* .
        :param region: For cross-region subscriptions, the region in which the topic resides. If no region is specified, AWS CloudFormation uses the region of the caller as the default. If you perform an update operation that only updates the ``Region`` property of a ``AWS::SNS::Subscription`` resource, that operation will fail unless you are either: - Updating the ``Region`` from ``NULL`` to the caller region. - Updating the ``Region`` from the caller region to ``NULL`` .
        :param subscription_role_arn: This property applies only to Amazon Kinesis Data Firehose delivery stream subscriptions. Specify the ARN of the IAM role that has the following: - Permission to write to the Amazon Kinesis Data Firehose delivery stream - Amazon SNS listed as a trusted entity Specifying a valid ARN for this attribute is required for Kinesis Data Firehose delivery stream subscriptions. For more information, see `Fanout to Amazon Kinesis Data Firehose delivery streams <https://docs.aws.amazon.com/sns/latest/dg/sns-firehose-as-subscriber.html>`_ in the *Amazon SNS Developer Guide.*
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__076230a6f834505ef89eb5209456e37c9c0b48214e98c426a20b11b4cb09f04c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSubscriptionProps(
            protocol=protocol,
            topic_arn=topic_arn,
            delivery_policy=delivery_policy,
            endpoint=endpoint,
            filter_policy=filter_policy,
            filter_policy_scope=filter_policy_scope,
            raw_message_delivery=raw_message_delivery,
            redrive_policy=redrive_policy,
            region=region,
            subscription_role_arn=subscription_role_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9885538e2f3d287043ce00f00c636c5005e7cfd167551ca15146c84f36df3e33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac179251a959fc3ad80f532e50aa363fa643e59edb2f224074466159dd1b99f7)
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
    @jsii.member(jsii_name="deliveryPolicy")
    def delivery_policy(self) -> typing.Any:
        '''The delivery policy JSON assigned to the subscription.

        Enables the subscriber to define the message delivery retry strategy in the case of an HTTP/S endpoint subscribed to the topic. For more information, see ``[GetSubscriptionAttributes](https://docs.aws.amazon.com/sns/latest/api/API_GetSubscriptionAttributes.html)`` in the *Amazon SNS API Reference* and `Message delivery retries <https://docs.aws.amazon.com/sns/latest/dg/sns-message-delivery-retries.html>`_ in the *Amazon SNS Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-deliverypolicy
        '''
        return typing.cast(typing.Any, jsii.get(self, "deliveryPolicy"))

    @delivery_policy.setter
    def delivery_policy(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e50237dff74d5a80e5ab1010dbec724707098cea6f45efdfe548a5e1e224c20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deliveryPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="filterPolicy")
    def filter_policy(self) -> typing.Any:
        '''The filter policy JSON assigned to the subscription.

        Enables the subscriber to filter out unwanted messages. For more information, see ``[GetSubscriptionAttributes](https://docs.aws.amazon.com/sns/latest/api/API_GetSubscriptionAttributes.html)`` in the *Amazon SNS API Reference* and `Message filtering <https://docs.aws.amazon.com/sns/latest/dg/sns-message-filtering.html>`_ in the *Amazon SNS Developer Guide* .

        - ``FilterPolicyScope`` - This attribute lets you choose the filtering scope by using one of the following string value types:
        - ``MessageAttributes`` (default) - The filter is applied on the message attributes.
        - ``MessageBody`` - The filter is applied on the message body.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-filterpolicy
        '''
        return typing.cast(typing.Any, jsii.get(self, "filterPolicy"))

    @filter_policy.setter
    def filter_policy(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fae729db18712337548c7cd5cc81bf6ff3ffc30c0d8999bd6616d6801be589b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        '''The subscription's protocol.

        For more information, see the ``Protocol`` parameter of the ``[Subscribe](https://docs.aws.amazon.com/sns/latest/api/API_Subscribe.html)`` action in the *Amazon SNS API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-protocol
        '''
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bab8bd725e3396d322ea4f2f1993c7e081f97559cc7981b6518d15df59a1ecf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="redrivePolicy")
    def redrive_policy(self) -> typing.Any:
        '''When specified, sends undeliverable messages to the specified Amazon SQS dead-letter queue.

        Messages that can't be delivered due to client errors (for example, when the subscribed endpoint is unreachable) or server errors (for example, when the service that powers the subscribed endpoint becomes unavailable) are held in the dead-letter queue for further analysis or reprocessing.

        For more information about the redrive policy and dead-letter queues, see `Amazon SQS dead-letter queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html>`_ in the *Amazon SQS Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-redrivepolicy
        '''
        return typing.cast(typing.Any, jsii.get(self, "redrivePolicy"))

    @redrive_policy.setter
    def redrive_policy(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1502081a359e821747a81a7d5a46a689dd7dabde478c368d061652c67dfd1789)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redrivePolicy", value)

    @builtins.property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> builtins.str:
        '''The ARN of the topic to subscribe to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#topicarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "topicArn"))

    @topic_arn.setter
    def topic_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6a707e7eac08260016b837817369f151266569f2f65d100c2e8ff45c592d911)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicArn", value)

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''The subscription's endpoint.

        The endpoint value depends on the protocol that you specify. For more information, see the ``Endpoint`` parameter of the ``[Subscribe](https://docs.aws.amazon.com/sns/latest/api/API_Subscribe.html)`` action in the *Amazon SNS API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-endpoint
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cb40c522c000821a88715bb6b991a7fecf77c7cd49bc8fbad68bedbfa0d8f36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value)

    @builtins.property
    @jsii.member(jsii_name="filterPolicyScope")
    def filter_policy_scope(self) -> typing.Optional[builtins.str]:
        '''``AWS::SNS::Subscription.FilterPolicyScope``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-filterpolicyscope
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterPolicyScope"))

    @filter_policy_scope.setter
    def filter_policy_scope(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee7666af622d138685bf401be24b855f77364367065d0986499a21c4b86a21fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterPolicyScope", value)

    @builtins.property
    @jsii.member(jsii_name="rawMessageDelivery")
    def raw_message_delivery(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''When set to ``true`` , enables raw message delivery.

        Raw messages don't contain any JSON formatting and can be sent to Amazon SQS and HTTP/S endpoints. For more information, see ``[GetSubscriptionAttributes](https://docs.aws.amazon.com/sns/latest/api/API_GetSubscriptionAttributes.html)`` in the *Amazon SNS API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-rawmessagedelivery
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "rawMessageDelivery"))

    @raw_message_delivery.setter
    def raw_message_delivery(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09fe21a3620e088f193f51c4eb4d8bed83d898eb8ddf000f7c4b3ec56387b131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawMessageDelivery", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        '''For cross-region subscriptions, the region in which the topic resides.

        If no region is specified, AWS CloudFormation uses the region of the caller as the default.

        If you perform an update operation that only updates the ``Region`` property of a ``AWS::SNS::Subscription`` resource, that operation will fail unless you are either:

        - Updating the ``Region`` from ``NULL`` to the caller region.
        - Updating the ``Region`` from the caller region to ``NULL`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-region
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))

    @region.setter
    def region(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f678797b822d131c0c9439c597fbfc69b2c5828027ac3d240395c836689ba8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="subscriptionRoleArn")
    def subscription_role_arn(self) -> typing.Optional[builtins.str]:
        '''This property applies only to Amazon Kinesis Data Firehose delivery stream subscriptions.

        Specify the ARN of the IAM role that has the following:

        - Permission to write to the Amazon Kinesis Data Firehose delivery stream
        - Amazon SNS listed as a trusted entity

        Specifying a valid ARN for this attribute is required for Kinesis Data Firehose delivery stream subscriptions. For more information, see `Fanout to Amazon Kinesis Data Firehose delivery streams <https://docs.aws.amazon.com/sns/latest/dg/sns-firehose-as-subscriber.html>`_ in the *Amazon SNS Developer Guide.*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-subscriptionrolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subscriptionRoleArn"))

    @subscription_role_arn.setter
    def subscription_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d4e9f25848ff4a63ed6f6a08ec197c226c6f9024dc1bc378a826fe07ba2d8f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscriptionRoleArn", value)


@jsii.data_type(
    jsii_type="monocdk.aws_sns.CfnSubscriptionProps",
    jsii_struct_bases=[],
    name_mapping={
        "protocol": "protocol",
        "topic_arn": "topicArn",
        "delivery_policy": "deliveryPolicy",
        "endpoint": "endpoint",
        "filter_policy": "filterPolicy",
        "filter_policy_scope": "filterPolicyScope",
        "raw_message_delivery": "rawMessageDelivery",
        "redrive_policy": "redrivePolicy",
        "region": "region",
        "subscription_role_arn": "subscriptionRoleArn",
    },
)
class CfnSubscriptionProps:
    def __init__(
        self,
        *,
        protocol: builtins.str,
        topic_arn: builtins.str,
        delivery_policy: typing.Any = None,
        endpoint: typing.Optional[builtins.str] = None,
        filter_policy: typing.Any = None,
        filter_policy_scope: typing.Optional[builtins.str] = None,
        raw_message_delivery: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        redrive_policy: typing.Any = None,
        region: typing.Optional[builtins.str] = None,
        subscription_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnSubscription``.

        :param protocol: The subscription's protocol. For more information, see the ``Protocol`` parameter of the ``[Subscribe](https://docs.aws.amazon.com/sns/latest/api/API_Subscribe.html)`` action in the *Amazon SNS API Reference* .
        :param topic_arn: The ARN of the topic to subscribe to.
        :param delivery_policy: The delivery policy JSON assigned to the subscription. Enables the subscriber to define the message delivery retry strategy in the case of an HTTP/S endpoint subscribed to the topic. For more information, see ``[GetSubscriptionAttributes](https://docs.aws.amazon.com/sns/latest/api/API_GetSubscriptionAttributes.html)`` in the *Amazon SNS API Reference* and `Message delivery retries <https://docs.aws.amazon.com/sns/latest/dg/sns-message-delivery-retries.html>`_ in the *Amazon SNS Developer Guide* .
        :param endpoint: The subscription's endpoint. The endpoint value depends on the protocol that you specify. For more information, see the ``Endpoint`` parameter of the ``[Subscribe](https://docs.aws.amazon.com/sns/latest/api/API_Subscribe.html)`` action in the *Amazon SNS API Reference* .
        :param filter_policy: The filter policy JSON assigned to the subscription. Enables the subscriber to filter out unwanted messages. For more information, see ``[GetSubscriptionAttributes](https://docs.aws.amazon.com/sns/latest/api/API_GetSubscriptionAttributes.html)`` in the *Amazon SNS API Reference* and `Message filtering <https://docs.aws.amazon.com/sns/latest/dg/sns-message-filtering.html>`_ in the *Amazon SNS Developer Guide* . - ``FilterPolicyScope`` - This attribute lets you choose the filtering scope by using one of the following string value types: - ``MessageAttributes`` (default) - The filter is applied on the message attributes. - ``MessageBody`` - The filter is applied on the message body.
        :param filter_policy_scope: ``AWS::SNS::Subscription.FilterPolicyScope``.
        :param raw_message_delivery: When set to ``true`` , enables raw message delivery. Raw messages don't contain any JSON formatting and can be sent to Amazon SQS and HTTP/S endpoints. For more information, see ``[GetSubscriptionAttributes](https://docs.aws.amazon.com/sns/latest/api/API_GetSubscriptionAttributes.html)`` in the *Amazon SNS API Reference* .
        :param redrive_policy: When specified, sends undeliverable messages to the specified Amazon SQS dead-letter queue. Messages that can't be delivered due to client errors (for example, when the subscribed endpoint is unreachable) or server errors (for example, when the service that powers the subscribed endpoint becomes unavailable) are held in the dead-letter queue for further analysis or reprocessing. For more information about the redrive policy and dead-letter queues, see `Amazon SQS dead-letter queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html>`_ in the *Amazon SQS Developer Guide* .
        :param region: For cross-region subscriptions, the region in which the topic resides. If no region is specified, AWS CloudFormation uses the region of the caller as the default. If you perform an update operation that only updates the ``Region`` property of a ``AWS::SNS::Subscription`` resource, that operation will fail unless you are either: - Updating the ``Region`` from ``NULL`` to the caller region. - Updating the ``Region`` from the caller region to ``NULL`` .
        :param subscription_role_arn: This property applies only to Amazon Kinesis Data Firehose delivery stream subscriptions. Specify the ARN of the IAM role that has the following: - Permission to write to the Amazon Kinesis Data Firehose delivery stream - Amazon SNS listed as a trusted entity Specifying a valid ARN for this attribute is required for Kinesis Data Firehose delivery stream subscriptions. For more information, see `Fanout to Amazon Kinesis Data Firehose delivery streams <https://docs.aws.amazon.com/sns/latest/dg/sns-firehose-as-subscriber.html>`_ in the *Amazon SNS Developer Guide.*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sns as sns
            
            # delivery_policy: Any
            # filter_policy: Any
            # redrive_policy: Any
            
            cfn_subscription_props = sns.CfnSubscriptionProps(
                protocol="protocol",
                topic_arn="topicArn",
            
                # the properties below are optional
                delivery_policy=delivery_policy,
                endpoint="endpoint",
                filter_policy=filter_policy,
                filter_policy_scope="filterPolicyScope",
                raw_message_delivery=False,
                redrive_policy=redrive_policy,
                region="region",
                subscription_role_arn="subscriptionRoleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93ce8b6f2cfa476a226137d16d19936b7650ee46a7f8517f06e3889d072bf452)
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            check_type(argname="argument delivery_policy", value=delivery_policy, expected_type=type_hints["delivery_policy"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument filter_policy", value=filter_policy, expected_type=type_hints["filter_policy"])
            check_type(argname="argument filter_policy_scope", value=filter_policy_scope, expected_type=type_hints["filter_policy_scope"])
            check_type(argname="argument raw_message_delivery", value=raw_message_delivery, expected_type=type_hints["raw_message_delivery"])
            check_type(argname="argument redrive_policy", value=redrive_policy, expected_type=type_hints["redrive_policy"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument subscription_role_arn", value=subscription_role_arn, expected_type=type_hints["subscription_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "protocol": protocol,
            "topic_arn": topic_arn,
        }
        if delivery_policy is not None:
            self._values["delivery_policy"] = delivery_policy
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy
        if filter_policy_scope is not None:
            self._values["filter_policy_scope"] = filter_policy_scope
        if raw_message_delivery is not None:
            self._values["raw_message_delivery"] = raw_message_delivery
        if redrive_policy is not None:
            self._values["redrive_policy"] = redrive_policy
        if region is not None:
            self._values["region"] = region
        if subscription_role_arn is not None:
            self._values["subscription_role_arn"] = subscription_role_arn

    @builtins.property
    def protocol(self) -> builtins.str:
        '''The subscription's protocol.

        For more information, see the ``Protocol`` parameter of the ``[Subscribe](https://docs.aws.amazon.com/sns/latest/api/API_Subscribe.html)`` action in the *Amazon SNS API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-protocol
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic_arn(self) -> builtins.str:
        '''The ARN of the topic to subscribe to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#topicarn
        '''
        result = self._values.get("topic_arn")
        assert result is not None, "Required property 'topic_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def delivery_policy(self) -> typing.Any:
        '''The delivery policy JSON assigned to the subscription.

        Enables the subscriber to define the message delivery retry strategy in the case of an HTTP/S endpoint subscribed to the topic. For more information, see ``[GetSubscriptionAttributes](https://docs.aws.amazon.com/sns/latest/api/API_GetSubscriptionAttributes.html)`` in the *Amazon SNS API Reference* and `Message delivery retries <https://docs.aws.amazon.com/sns/latest/dg/sns-message-delivery-retries.html>`_ in the *Amazon SNS Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-deliverypolicy
        '''
        result = self._values.get("delivery_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''The subscription's endpoint.

        The endpoint value depends on the protocol that you specify. For more information, see the ``Endpoint`` parameter of the ``[Subscribe](https://docs.aws.amazon.com/sns/latest/api/API_Subscribe.html)`` action in the *Amazon SNS API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-endpoint
        '''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_policy(self) -> typing.Any:
        '''The filter policy JSON assigned to the subscription.

        Enables the subscriber to filter out unwanted messages. For more information, see ``[GetSubscriptionAttributes](https://docs.aws.amazon.com/sns/latest/api/API_GetSubscriptionAttributes.html)`` in the *Amazon SNS API Reference* and `Message filtering <https://docs.aws.amazon.com/sns/latest/dg/sns-message-filtering.html>`_ in the *Amazon SNS Developer Guide* .

        - ``FilterPolicyScope`` - This attribute lets you choose the filtering scope by using one of the following string value types:
        - ``MessageAttributes`` (default) - The filter is applied on the message attributes.
        - ``MessageBody`` - The filter is applied on the message body.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-filterpolicy
        '''
        result = self._values.get("filter_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def filter_policy_scope(self) -> typing.Optional[builtins.str]:
        '''``AWS::SNS::Subscription.FilterPolicyScope``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-filterpolicyscope
        '''
        result = self._values.get("filter_policy_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_message_delivery(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''When set to ``true`` , enables raw message delivery.

        Raw messages don't contain any JSON formatting and can be sent to Amazon SQS and HTTP/S endpoints. For more information, see ``[GetSubscriptionAttributes](https://docs.aws.amazon.com/sns/latest/api/API_GetSubscriptionAttributes.html)`` in the *Amazon SNS API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-rawmessagedelivery
        '''
        result = self._values.get("raw_message_delivery")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def redrive_policy(self) -> typing.Any:
        '''When specified, sends undeliverable messages to the specified Amazon SQS dead-letter queue.

        Messages that can't be delivered due to client errors (for example, when the subscribed endpoint is unreachable) or server errors (for example, when the service that powers the subscribed endpoint becomes unavailable) are held in the dead-letter queue for further analysis or reprocessing.

        For more information about the redrive policy and dead-letter queues, see `Amazon SQS dead-letter queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html>`_ in the *Amazon SQS Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-redrivepolicy
        '''
        result = self._values.get("redrive_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''For cross-region subscriptions, the region in which the topic resides.

        If no region is specified, AWS CloudFormation uses the region of the caller as the default.

        If you perform an update operation that only updates the ``Region`` property of a ``AWS::SNS::Subscription`` resource, that operation will fail unless you are either:

        - Updating the ``Region`` from ``NULL`` to the caller region.
        - Updating the ``Region`` from the caller region to ``NULL`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-region
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscription_role_arn(self) -> typing.Optional[builtins.str]:
        '''This property applies only to Amazon Kinesis Data Firehose delivery stream subscriptions.

        Specify the ARN of the IAM role that has the following:

        - Permission to write to the Amazon Kinesis Data Firehose delivery stream
        - Amazon SNS listed as a trusted entity

        Specifying a valid ARN for this attribute is required for Kinesis Data Firehose delivery stream subscriptions. For more information, see `Fanout to Amazon Kinesis Data Firehose delivery streams <https://docs.aws.amazon.com/sns/latest/dg/sns-firehose-as-subscriber.html>`_ in the *Amazon SNS Developer Guide.*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-subscriptionrolearn
        '''
        result = self._values.get("subscription_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnTopic(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sns.CfnTopic",
):
    '''A CloudFormation ``AWS::SNS::Topic``.

    The ``AWS::SNS::Topic`` resource creates a topic to which notifications can be published.
    .. epigraph::

       One account can create a maximum of 100,000 standard topics and 1,000 FIFO topics. For more information, see `Amazon SNS endpoints and quotas <https://docs.aws.amazon.com/general/latest/gr/sns.html>`_ in the *AWS General Reference* .

    :cloudformationResource: AWS::SNS::Topic
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_sns as sns
        
        # data_protection_policy: Any
        
        cfn_topic = sns.CfnTopic(self, "MyCfnTopic",
            content_based_deduplication=False,
            data_protection_policy=data_protection_policy,
            display_name="displayName",
            fifo_topic=False,
            kms_master_key_id="kmsMasterKeyId",
            signature_version="signatureVersion",
            subscription=[sns.CfnTopic.SubscriptionProperty(
                endpoint="endpoint",
                protocol="protocol"
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            topic_name="topicName"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        content_based_deduplication: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        data_protection_policy: typing.Any = None,
        display_name: typing.Optional[builtins.str] = None,
        fifo_topic: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        kms_master_key_id: typing.Optional[builtins.str] = None,
        signature_version: typing.Optional[builtins.str] = None,
        subscription: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTopic.SubscriptionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        topic_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::SNS::Topic``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param content_based_deduplication: Enables content-based deduplication for FIFO topics. - By default, ``ContentBasedDeduplication`` is set to ``false`` . If you create a FIFO topic and this attribute is ``false`` , you must specify a value for the ``MessageDeduplicationId`` parameter for the `Publish <https://docs.aws.amazon.com/sns/latest/api/API_Publish.html>`_ action. - When you set ``ContentBasedDeduplication`` to ``true`` , Amazon SNS uses a SHA-256 hash to generate the ``MessageDeduplicationId`` using the body of the message (but not the attributes of the message). (Optional) To override the generated value, you can specify a value for the the ``MessageDeduplicationId`` parameter for the ``Publish`` action.
        :param data_protection_policy: The body of the policy document you want to use for this topic. You can only add one policy per topic. The policy must be in JSON string format. Length Constraints: Maximum length of 30,720.
        :param display_name: The display name to use for an Amazon SNS topic with SMS subscriptions. The display name must be maximum 100 characters long, including hyphens (-), underscores (_), spaces, and tabs.
        :param fifo_topic: Set to true to create a FIFO topic.
        :param kms_master_key_id: The ID of an AWS managed customer master key (CMK) for Amazon SNS or a custom CMK. For more information, see `Key terms <https://docs.aws.amazon.com/sns/latest/dg/sns-server-side-encryption.html#sse-key-terms>`_ . For more examples, see ``[KeyId](https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html#API_DescribeKey_RequestParameters)`` in the *AWS Key Management Service API Reference* . This property applies only to `server-side-encryption <https://docs.aws.amazon.com/sns/latest/dg/sns-server-side-encryption.html>`_ .
        :param signature_version: ``AWS::SNS::Topic.SignatureVersion``.
        :param subscription: The Amazon SNS subscriptions (endpoints) for this topic.
        :param tags: The list of tags to add to a new topic. .. epigraph:: To be able to tag a topic on creation, you must have the ``sns:CreateTopic`` and ``sns:TagResource`` permissions.
        :param topic_name: The name of the topic you want to create. Topic names must include only uppercase and lowercase ASCII letters, numbers, underscores, and hyphens, and must be between 1 and 256 characters long. FIFO topic names must end with ``.fifo`` . If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the topic name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e0ee1a44f398c754b0862d012b783ba509399f8773e351a1669d21d5c10fdf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTopicProps(
            content_based_deduplication=content_based_deduplication,
            data_protection_policy=data_protection_policy,
            display_name=display_name,
            fifo_topic=fifo_topic,
            kms_master_key_id=kms_master_key_id,
            signature_version=signature_version,
            subscription=subscription,
            tags=tags,
            topic_name=topic_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3942ff430b75b849487eeaa6a8ccfef3aaecc185a02d36a64745ce0814ec9a8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08e53d41b4fe5c6f27be279f7503efdc21ef14dfc22fc05e0e3e76e5e80b59c8)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrTopicArn")
    def attr_topic_arn(self) -> builtins.str:
        '''Returns the ARN of an Amazon SNS topic.

        :cloudformationAttribute: TopicArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTopicArn"))

    @builtins.property
    @jsii.member(jsii_name="attrTopicName")
    def attr_topic_name(self) -> builtins.str:
        '''Returns the name of an Amazon SNS topic.

        :cloudformationAttribute: TopicName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTopicName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The list of tags to add to a new topic.

        .. epigraph::

           To be able to tag a topic on creation, you must have the ``sns:CreateTopic`` and ``sns:TagResource`` permissions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="dataProtectionPolicy")
    def data_protection_policy(self) -> typing.Any:
        '''The body of the policy document you want to use for this topic.

        You can only add one policy per topic.

        The policy must be in JSON string format.

        Length Constraints: Maximum length of 30,720.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-dataprotectionpolicy
        '''
        return typing.cast(typing.Any, jsii.get(self, "dataProtectionPolicy"))

    @data_protection_policy.setter
    def data_protection_policy(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__995cc9290d5ec332c766a36abeb1695afc60ab299f7553e3ab21c68fb9997216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataProtectionPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="contentBasedDeduplication")
    def content_based_deduplication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Enables content-based deduplication for FIFO topics.

        - By default, ``ContentBasedDeduplication`` is set to ``false`` . If you create a FIFO topic and this attribute is ``false`` , you must specify a value for the ``MessageDeduplicationId`` parameter for the `Publish <https://docs.aws.amazon.com/sns/latest/api/API_Publish.html>`_ action.
        - When you set ``ContentBasedDeduplication`` to ``true`` , Amazon SNS uses a SHA-256 hash to generate the ``MessageDeduplicationId`` using the body of the message (but not the attributes of the message).

        (Optional) To override the generated value, you can specify a value for the the ``MessageDeduplicationId`` parameter for the ``Publish`` action.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-contentbaseddeduplication
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "contentBasedDeduplication"))

    @content_based_deduplication.setter
    def content_based_deduplication(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33e547bf8efb76c461397e84eed7e885bd4e3e4e5262d669f014c88e1e25a991)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentBasedDeduplication", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name to use for an Amazon SNS topic with SMS subscriptions.

        The display name must be maximum 100 characters long, including hyphens (-), underscores (_), spaces, and tabs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-displayname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86605374120923641b3baba4b957cd29c90e96185e3468669caacdd77db9c33f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="fifoTopic")
    def fifo_topic(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Set to true to create a FIFO topic.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-fifotopic
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "fifoTopic"))

    @fifo_topic.setter
    def fifo_topic(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__036f330bdd9a94a17ad14b123e0cbdd57387ec44c73060154a13ce95fb9b9128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fifoTopic", value)

    @builtins.property
    @jsii.member(jsii_name="kmsMasterKeyId")
    def kms_master_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of an AWS managed customer master key (CMK) for Amazon SNS or a custom CMK.

        For more information, see `Key terms <https://docs.aws.amazon.com/sns/latest/dg/sns-server-side-encryption.html#sse-key-terms>`_ . For more examples, see ``[KeyId](https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html#API_DescribeKey_RequestParameters)`` in the *AWS Key Management Service API Reference* .

        This property applies only to `server-side-encryption <https://docs.aws.amazon.com/sns/latest/dg/sns-server-side-encryption.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-kmsmasterkeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsMasterKeyId"))

    @kms_master_key_id.setter
    def kms_master_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb9e5f8b3cf159b99ed685dd542df363801765e8ba858c4ea1dee8d8db46790f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsMasterKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="signatureVersion")
    def signature_version(self) -> typing.Optional[builtins.str]:
        '''``AWS::SNS::Topic.SignatureVersion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-signatureversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signatureVersion"))

    @signature_version.setter
    def signature_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eed72c3e827fd991b83e1e49b8ead0d2b51c870ec4581af935877034f0aa356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signatureVersion", value)

    @builtins.property
    @jsii.member(jsii_name="subscription")
    def subscription(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTopic.SubscriptionProperty", _IResolvable_a771d0ef]]]]:
        '''The Amazon SNS subscriptions (endpoints) for this topic.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-subscription
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTopic.SubscriptionProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "subscription"))

    @subscription.setter
    def subscription(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTopic.SubscriptionProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f324d34beb044d22ca87b6749ae40d4648f0569c39870b42f00ffa8c0d9d7d68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscription", value)

    @builtins.property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> typing.Optional[builtins.str]:
        '''The name of the topic you want to create.

        Topic names must include only uppercase and lowercase ASCII letters, numbers, underscores, and hyphens, and must be between 1 and 256 characters long. FIFO topic names must end with ``.fifo`` .

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the topic name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-topicname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicName"))

    @topic_name.setter
    def topic_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__160e8825570304a6bb299a5a68a0f0585096f755e02fa3adb5384d78dd1875dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_sns.CfnTopic.SubscriptionProperty",
        jsii_struct_bases=[],
        name_mapping={"endpoint": "endpoint", "protocol": "protocol"},
    )
    class SubscriptionProperty:
        def __init__(self, *, endpoint: builtins.str, protocol: builtins.str) -> None:
            '''``Subscription`` is an embedded property that describes the subscription endpoints of an Amazon SNS topic.

            .. epigraph::

               For full control over subscription behavior (for example, delivery policy, filtering, raw message delivery, and cross-region subscriptions), use the `AWS::SNS::Subscription <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html>`_ resource.

            :param endpoint: The endpoint that receives notifications from the Amazon SNS topic. The endpoint value depends on the protocol that you specify. For more information, see the ``Endpoint`` parameter of the ``[Subscribe](https://docs.aws.amazon.com/sns/latest/api/API_Subscribe.html)`` action in the *Amazon SNS API Reference* .
            :param protocol: The subscription's protocol. For more information, see the ``Protocol`` parameter of the ``[Subscribe](https://docs.aws.amazon.com/sns/latest/api/API_Subscribe.html)`` action in the *Amazon SNS API Reference* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic-subscription.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sns as sns
                
                subscription_property = sns.CfnTopic.SubscriptionProperty(
                    endpoint="endpoint",
                    protocol="protocol"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__04d803becc2a4d16646a2d546552c6f13e16d72fef9fdf7fc584605ce8545f0c)
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "endpoint": endpoint,
                "protocol": protocol,
            }

        @builtins.property
        def endpoint(self) -> builtins.str:
            '''The endpoint that receives notifications from the Amazon SNS topic.

            The endpoint value depends on the protocol that you specify. For more information, see the ``Endpoint`` parameter of the ``[Subscribe](https://docs.aws.amazon.com/sns/latest/api/API_Subscribe.html)`` action in the *Amazon SNS API Reference* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic-subscription.html#cfn-sns-topic-subscription-endpoint
            '''
            result = self._values.get("endpoint")
            assert result is not None, "Required property 'endpoint' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def protocol(self) -> builtins.str:
            '''The subscription's protocol.

            For more information, see the ``Protocol`` parameter of the ``[Subscribe](https://docs.aws.amazon.com/sns/latest/api/API_Subscribe.html)`` action in the *Amazon SNS API Reference* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic-subscription.html#cfn-sns-topic-subscription-protocol
            '''
            result = self._values.get("protocol")
            assert result is not None, "Required property 'protocol' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubscriptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnTopicPolicy(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sns.CfnTopicPolicy",
):
    '''A CloudFormation ``AWS::SNS::TopicPolicy``.

    The ``AWS::SNS::TopicPolicy`` resource associates Amazon SNS topics with a policy. For an example snippet, see `Declaring an Amazon SNS policy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-sns-policy>`_ in the *AWS CloudFormation User Guide* .

    :cloudformationResource: AWS::SNS::TopicPolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_sns as sns
        
        # policy_document: Any
        
        cfn_topic_policy = sns.CfnTopicPolicy(self, "MyCfnTopicPolicy",
            policy_document=policy_document,
            topics=["topics"]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        policy_document: typing.Any,
        topics: typing.Sequence[builtins.str],
    ) -> None:
        '''Create a new ``AWS::SNS::TopicPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy_document: A policy document that contains permissions to add to the specified SNS topics.
        :param topics: The Amazon Resource Names (ARN) of the topics to which you want to add the policy. You can use the ``[Ref](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html)`` function to specify an ``[AWS::SNS::Topic](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html)`` resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a0ac65dd92cdd283e93fece57a00ea33ebfabf45144dfa8c11d5c30bed2b325)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTopicPolicyProps(policy_document=policy_document, topics=topics)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9423b268c7453eb12a77fbf95fc7a6a20c1e9ecac20fac2057cf8ef1928d7cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36e1cac98754a36f072ba18a88daa4d0e3e50229a9ee563200d8dbdb70ffbd2e)
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
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> typing.Any:
        '''A policy document that contains permissions to add to the specified SNS topics.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html#cfn-sns-topicpolicy-policydocument
        '''
        return typing.cast(typing.Any, jsii.get(self, "policyDocument"))

    @policy_document.setter
    def policy_document(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__731efe65a5881ad9fbec7bd6dec0412f875b999626e5a760ed488c1c0f199b09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="topics")
    def topics(self) -> typing.List[builtins.str]:
        '''The Amazon Resource Names (ARN) of the topics to which you want to add the policy.

        You can use the ``[Ref](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html)`` function to specify an ``[AWS::SNS::Topic](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html)`` resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html#cfn-sns-topicpolicy-topics
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "topics"))

    @topics.setter
    def topics(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08fc632ba09bfbef7a007383d40997e8795445e1f32a76207b520d48ed41d8c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topics", value)


@jsii.data_type(
    jsii_type="monocdk.aws_sns.CfnTopicPolicyProps",
    jsii_struct_bases=[],
    name_mapping={"policy_document": "policyDocument", "topics": "topics"},
)
class CfnTopicPolicyProps:
    def __init__(
        self,
        *,
        policy_document: typing.Any,
        topics: typing.Sequence[builtins.str],
    ) -> None:
        '''Properties for defining a ``CfnTopicPolicy``.

        :param policy_document: A policy document that contains permissions to add to the specified SNS topics.
        :param topics: The Amazon Resource Names (ARN) of the topics to which you want to add the policy. You can use the ``[Ref](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html)`` function to specify an ``[AWS::SNS::Topic](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html)`` resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sns as sns
            
            # policy_document: Any
            
            cfn_topic_policy_props = sns.CfnTopicPolicyProps(
                policy_document=policy_document,
                topics=["topics"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1287a88f078ff3e3e197070a7223a5a150b4b155b93d6b206e7eed0228f28840)
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument topics", value=topics, expected_type=type_hints["topics"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_document": policy_document,
            "topics": topics,
        }

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''A policy document that contains permissions to add to the specified SNS topics.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html#cfn-sns-topicpolicy-policydocument
        '''
        result = self._values.get("policy_document")
        assert result is not None, "Required property 'policy_document' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def topics(self) -> typing.List[builtins.str]:
        '''The Amazon Resource Names (ARN) of the topics to which you want to add the policy.

        You can use the ``[Ref](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html)`` function to specify an ``[AWS::SNS::Topic](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html)`` resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html#cfn-sns-topicpolicy-topics
        '''
        result = self._values.get("topics")
        assert result is not None, "Required property 'topics' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTopicPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_sns.CfnTopicProps",
    jsii_struct_bases=[],
    name_mapping={
        "content_based_deduplication": "contentBasedDeduplication",
        "data_protection_policy": "dataProtectionPolicy",
        "display_name": "displayName",
        "fifo_topic": "fifoTopic",
        "kms_master_key_id": "kmsMasterKeyId",
        "signature_version": "signatureVersion",
        "subscription": "subscription",
        "tags": "tags",
        "topic_name": "topicName",
    },
)
class CfnTopicProps:
    def __init__(
        self,
        *,
        content_based_deduplication: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        data_protection_policy: typing.Any = None,
        display_name: typing.Optional[builtins.str] = None,
        fifo_topic: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        kms_master_key_id: typing.Optional[builtins.str] = None,
        signature_version: typing.Optional[builtins.str] = None,
        subscription: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTopic.SubscriptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        topic_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnTopic``.

        :param content_based_deduplication: Enables content-based deduplication for FIFO topics. - By default, ``ContentBasedDeduplication`` is set to ``false`` . If you create a FIFO topic and this attribute is ``false`` , you must specify a value for the ``MessageDeduplicationId`` parameter for the `Publish <https://docs.aws.amazon.com/sns/latest/api/API_Publish.html>`_ action. - When you set ``ContentBasedDeduplication`` to ``true`` , Amazon SNS uses a SHA-256 hash to generate the ``MessageDeduplicationId`` using the body of the message (but not the attributes of the message). (Optional) To override the generated value, you can specify a value for the the ``MessageDeduplicationId`` parameter for the ``Publish`` action.
        :param data_protection_policy: The body of the policy document you want to use for this topic. You can only add one policy per topic. The policy must be in JSON string format. Length Constraints: Maximum length of 30,720.
        :param display_name: The display name to use for an Amazon SNS topic with SMS subscriptions. The display name must be maximum 100 characters long, including hyphens (-), underscores (_), spaces, and tabs.
        :param fifo_topic: Set to true to create a FIFO topic.
        :param kms_master_key_id: The ID of an AWS managed customer master key (CMK) for Amazon SNS or a custom CMK. For more information, see `Key terms <https://docs.aws.amazon.com/sns/latest/dg/sns-server-side-encryption.html#sse-key-terms>`_ . For more examples, see ``[KeyId](https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html#API_DescribeKey_RequestParameters)`` in the *AWS Key Management Service API Reference* . This property applies only to `server-side-encryption <https://docs.aws.amazon.com/sns/latest/dg/sns-server-side-encryption.html>`_ .
        :param signature_version: ``AWS::SNS::Topic.SignatureVersion``.
        :param subscription: The Amazon SNS subscriptions (endpoints) for this topic.
        :param tags: The list of tags to add to a new topic. .. epigraph:: To be able to tag a topic on creation, you must have the ``sns:CreateTopic`` and ``sns:TagResource`` permissions.
        :param topic_name: The name of the topic you want to create. Topic names must include only uppercase and lowercase ASCII letters, numbers, underscores, and hyphens, and must be between 1 and 256 characters long. FIFO topic names must end with ``.fifo`` . If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the topic name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sns as sns
            
            # data_protection_policy: Any
            
            cfn_topic_props = sns.CfnTopicProps(
                content_based_deduplication=False,
                data_protection_policy=data_protection_policy,
                display_name="displayName",
                fifo_topic=False,
                kms_master_key_id="kmsMasterKeyId",
                signature_version="signatureVersion",
                subscription=[sns.CfnTopic.SubscriptionProperty(
                    endpoint="endpoint",
                    protocol="protocol"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                topic_name="topicName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20f94fcf9a01a467359b11c49600b39b8c173af7e61631766b3f637d5f67e708)
            check_type(argname="argument content_based_deduplication", value=content_based_deduplication, expected_type=type_hints["content_based_deduplication"])
            check_type(argname="argument data_protection_policy", value=data_protection_policy, expected_type=type_hints["data_protection_policy"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument fifo_topic", value=fifo_topic, expected_type=type_hints["fifo_topic"])
            check_type(argname="argument kms_master_key_id", value=kms_master_key_id, expected_type=type_hints["kms_master_key_id"])
            check_type(argname="argument signature_version", value=signature_version, expected_type=type_hints["signature_version"])
            check_type(argname="argument subscription", value=subscription, expected_type=type_hints["subscription"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument topic_name", value=topic_name, expected_type=type_hints["topic_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if content_based_deduplication is not None:
            self._values["content_based_deduplication"] = content_based_deduplication
        if data_protection_policy is not None:
            self._values["data_protection_policy"] = data_protection_policy
        if display_name is not None:
            self._values["display_name"] = display_name
        if fifo_topic is not None:
            self._values["fifo_topic"] = fifo_topic
        if kms_master_key_id is not None:
            self._values["kms_master_key_id"] = kms_master_key_id
        if signature_version is not None:
            self._values["signature_version"] = signature_version
        if subscription is not None:
            self._values["subscription"] = subscription
        if tags is not None:
            self._values["tags"] = tags
        if topic_name is not None:
            self._values["topic_name"] = topic_name

    @builtins.property
    def content_based_deduplication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Enables content-based deduplication for FIFO topics.

        - By default, ``ContentBasedDeduplication`` is set to ``false`` . If you create a FIFO topic and this attribute is ``false`` , you must specify a value for the ``MessageDeduplicationId`` parameter for the `Publish <https://docs.aws.amazon.com/sns/latest/api/API_Publish.html>`_ action.
        - When you set ``ContentBasedDeduplication`` to ``true`` , Amazon SNS uses a SHA-256 hash to generate the ``MessageDeduplicationId`` using the body of the message (but not the attributes of the message).

        (Optional) To override the generated value, you can specify a value for the the ``MessageDeduplicationId`` parameter for the ``Publish`` action.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-contentbaseddeduplication
        '''
        result = self._values.get("content_based_deduplication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def data_protection_policy(self) -> typing.Any:
        '''The body of the policy document you want to use for this topic.

        You can only add one policy per topic.

        The policy must be in JSON string format.

        Length Constraints: Maximum length of 30,720.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-dataprotectionpolicy
        '''
        result = self._values.get("data_protection_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name to use for an Amazon SNS topic with SMS subscriptions.

        The display name must be maximum 100 characters long, including hyphens (-), underscores (_), spaces, and tabs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fifo_topic(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Set to true to create a FIFO topic.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-fifotopic
        '''
        result = self._values.get("fifo_topic")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def kms_master_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of an AWS managed customer master key (CMK) for Amazon SNS or a custom CMK.

        For more information, see `Key terms <https://docs.aws.amazon.com/sns/latest/dg/sns-server-side-encryption.html#sse-key-terms>`_ . For more examples, see ``[KeyId](https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html#API_DescribeKey_RequestParameters)`` in the *AWS Key Management Service API Reference* .

        This property applies only to `server-side-encryption <https://docs.aws.amazon.com/sns/latest/dg/sns-server-side-encryption.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-kmsmasterkeyid
        '''
        result = self._values.get("kms_master_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signature_version(self) -> typing.Optional[builtins.str]:
        '''``AWS::SNS::Topic.SignatureVersion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-signatureversion
        '''
        result = self._values.get("signature_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscription(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTopic.SubscriptionProperty, _IResolvable_a771d0ef]]]]:
        '''The Amazon SNS subscriptions (endpoints) for this topic.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-subscription
        '''
        result = self._values.get("subscription")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTopic.SubscriptionProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The list of tags to add to a new topic.

        .. epigraph::

           To be able to tag a topic on creation, you must have the ``sns:CreateTopic`` and ``sns:TagResource`` permissions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def topic_name(self) -> typing.Optional[builtins.str]:
        '''The name of the topic you want to create.

        Topic names must include only uppercase and lowercase ASCII letters, numbers, underscores, and hyphens, and must be between 1 and 256 characters long. FIFO topic names must end with ``.fifo`` .

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the topic name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-topicname
        '''
        result = self._values.get("topic_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTopicProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_sns.ITopic")
class ITopic(
    _IResource_8c1dbbbd,
    _INotificationRuleTarget_31f512df,
    typing_extensions.Protocol,
):
    '''(experimental) Represents an SNS topic.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="fifo")
    def fifo(self) -> builtins.bool:
        '''(experimental) Whether this topic is an Amazon SNS FIFO queue.

        If false, this is a standard topic.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> builtins.str:
        '''(experimental) The ARN of the topic.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> builtins.str:
        '''(experimental) The name of the topic.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addSubscription")
    def add_subscription(self, subscription: "ITopicSubscription") -> None:
        '''(experimental) Subscribe some endpoint to this topic.

        :param subscription: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        '''(experimental) Adds a statement to the IAM resource policy associated with this topic.

        If this topic was created in this stack (``new Topic``), a topic policy
        will be automatically created upon the first call to ``addToPolicy``. If
        the topic is imported (``Topic.import``), then this is a no-op.

        :param statement: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant topic publishing permissions to the given identity.

        :param identity: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Return the given named metric for this Topic.

        :param metric_name: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricNumberOfMessagesPublished")
    def metric_number_of_messages_published(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The number of messages published to your Amazon SNS topics.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricNumberOfNotificationsDelivered")
    def metric_number_of_notifications_delivered(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The number of messages successfully delivered from your Amazon SNS topics to subscribing endpoints.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricNumberOfNotificationsFailed")
    def metric_number_of_notifications_failed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The number of messages that Amazon SNS failed to deliver.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOut")
    def metric_number_of_notifications_filtered_out(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The number of messages that were rejected by subscription filter policies.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutInvalidAttributes")
    def metric_number_of_notifications_filtered_out_invalid_attributes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The number of messages that were rejected by subscription filter policies because the messages' attributes are invalid.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutNoMessageAttributes")
    def metric_number_of_notifications_filtered_out_no_message_attributes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The number of messages that were rejected by subscription filter policies because the messages have no attributes.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricPublishSize")
    def metric_publish_size(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the size of messages published through this topic.

        Average over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricSMSMonthToDateSpentUSD")
    def metric_sms_month_to_date_spent_usd(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The charges you have accrued since the start of the current calendar month for sending SMS messages.

        Maximum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricSMSSuccessRate")
    def metric_sms_success_rate(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The rate of successful SMS message deliveries.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...


class _ITopicProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
    jsii.proxy_for(_INotificationRuleTarget_31f512df), # type: ignore[misc]
):
    '''(experimental) Represents an SNS topic.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_sns.ITopic"

    @builtins.property
    @jsii.member(jsii_name="fifo")
    def fifo(self) -> builtins.bool:
        '''(experimental) Whether this topic is an Amazon SNS FIFO queue.

        If false, this is a standard topic.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.bool, jsii.get(self, "fifo"))

    @builtins.property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> builtins.str:
        '''(experimental) The ARN of the topic.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "topicArn"))

    @builtins.property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> builtins.str:
        '''(experimental) The name of the topic.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "topicName"))

    @jsii.member(jsii_name="addSubscription")
    def add_subscription(self, subscription: "ITopicSubscription") -> None:
        '''(experimental) Subscribe some endpoint to this topic.

        :param subscription: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__698303e3e465adb336bca80b15c6382915f31dcd7f9330483223b187e45a5ace)
            check_type(argname="argument subscription", value=subscription, expected_type=type_hints["subscription"])
        return typing.cast(None, jsii.invoke(self, "addSubscription", [subscription]))

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        '''(experimental) Adds a statement to the IAM resource policy associated with this topic.

        If this topic was created in this stack (``new Topic``), a topic policy
        will be automatically created upon the first call to ``addToPolicy``. If
        the topic is imported (``Topic.import``), then this is a no-op.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6082c3e9ef187a26b9e4b76adf300af2cf9494cbe6b4b9b36bca55d3b03f87b8)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(_AddToResourcePolicyResult_0fd9d2a9, jsii.invoke(self, "addToResourcePolicy", [statement]))

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant topic publishing permissions to the given identity.

        :param identity: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e818f3052fc34a37a859e6b3a22ceb5fe1678b82c449b14856a64fefac5f19)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPublish", [identity]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Return the given named metric for this Topic.

        :param metric_name: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58500a11474900ec94fffb5bca2b8143fc1a528368dd8011a76c6799805eb6c3)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricNumberOfMessagesPublished")
    def metric_number_of_messages_published(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The number of messages published to your Amazon SNS topics.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNumberOfMessagesPublished", [props]))

    @jsii.member(jsii_name="metricNumberOfNotificationsDelivered")
    def metric_number_of_notifications_delivered(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The number of messages successfully delivered from your Amazon SNS topics to subscribing endpoints.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNumberOfNotificationsDelivered", [props]))

    @jsii.member(jsii_name="metricNumberOfNotificationsFailed")
    def metric_number_of_notifications_failed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The number of messages that Amazon SNS failed to deliver.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNumberOfNotificationsFailed", [props]))

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOut")
    def metric_number_of_notifications_filtered_out(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The number of messages that were rejected by subscription filter policies.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNumberOfNotificationsFilteredOut", [props]))

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutInvalidAttributes")
    def metric_number_of_notifications_filtered_out_invalid_attributes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The number of messages that were rejected by subscription filter policies because the messages' attributes are invalid.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNumberOfNotificationsFilteredOutInvalidAttributes", [props]))

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutNoMessageAttributes")
    def metric_number_of_notifications_filtered_out_no_message_attributes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The number of messages that were rejected by subscription filter policies because the messages have no attributes.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNumberOfNotificationsFilteredOutNoMessageAttributes", [props]))

    @jsii.member(jsii_name="metricPublishSize")
    def metric_publish_size(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the size of messages published through this topic.

        Average over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricPublishSize", [props]))

    @jsii.member(jsii_name="metricSMSMonthToDateSpentUSD")
    def metric_sms_month_to_date_spent_usd(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The charges you have accrued since the start of the current calendar month for sending SMS messages.

        Maximum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSMSMonthToDateSpentUSD", [props]))

    @jsii.member(jsii_name="metricSMSSuccessRate")
    def metric_sms_success_rate(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The rate of successful SMS message deliveries.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSMSSuccessRate", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITopic).__jsii_proxy_class__ = lambda : _ITopicProxy


@jsii.interface(jsii_type="monocdk.aws_sns.ITopicSubscription")
class ITopicSubscription(typing_extensions.Protocol):
    '''(experimental) Topic subscription.

    :stability: experimental
    '''

    @jsii.member(jsii_name="bind")
    def bind(self, topic: ITopic) -> "TopicSubscriptionConfig":
        '''(experimental) Returns a configuration used to subscribe to an SNS topic.

        :param topic: topic for which subscription will be configured.

        :stability: experimental
        '''
        ...


class _ITopicSubscriptionProxy:
    '''(experimental) Topic subscription.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_sns.ITopicSubscription"

    @jsii.member(jsii_name="bind")
    def bind(self, topic: ITopic) -> "TopicSubscriptionConfig":
        '''(experimental) Returns a configuration used to subscribe to an SNS topic.

        :param topic: topic for which subscription will be configured.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__636b0eab2613ede1a35779d7da9f13be2431bb049c041f14999809c779469939)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        return typing.cast("TopicSubscriptionConfig", jsii.invoke(self, "bind", [topic]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITopicSubscription).__jsii_proxy_class__ = lambda : _ITopicSubscriptionProxy


@jsii.data_type(
    jsii_type="monocdk.aws_sns.NumericConditions",
    jsii_struct_bases=[],
    name_mapping={
        "allowlist": "allowlist",
        "between": "between",
        "between_strict": "betweenStrict",
        "greater_than": "greaterThan",
        "greater_than_or_equal_to": "greaterThanOrEqualTo",
        "less_than": "lessThan",
        "less_than_or_equal_to": "lessThanOrEqualTo",
        "whitelist": "whitelist",
    },
)
class NumericConditions:
    def __init__(
        self,
        *,
        allowlist: typing.Optional[typing.Sequence[jsii.Number]] = None,
        between: typing.Optional[typing.Union[BetweenCondition, typing.Dict[builtins.str, typing.Any]]] = None,
        between_strict: typing.Optional[typing.Union[BetweenCondition, typing.Dict[builtins.str, typing.Any]]] = None,
        greater_than: typing.Optional[jsii.Number] = None,
        greater_than_or_equal_to: typing.Optional[jsii.Number] = None,
        less_than: typing.Optional[jsii.Number] = None,
        less_than_or_equal_to: typing.Optional[jsii.Number] = None,
        whitelist: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''(experimental) Conditions that can be applied to numeric attributes.

        :param allowlist: (experimental) Match one or more values. Default: - None
        :param between: (experimental) Match values that are between the specified values. Default: - None
        :param between_strict: (experimental) Match values that are strictly between the specified values. Default: - None
        :param greater_than: (experimental) Match values that are greater than the specified value. Default: - None
        :param greater_than_or_equal_to: (experimental) Match values that are greater than or equal to the specified value. Default: - None
        :param less_than: (experimental) Match values that are less than the specified value. Default: - None
        :param less_than_or_equal_to: (experimental) Match values that are less than or equal to the specified value. Default: - None
        :param whitelist: (deprecated) Match one or more values. Default: - None

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as lambda_
            # fn: lambda.Function
            
            
            my_topic = sns.Topic(self, "MyTopic")
            
            # Lambda should receive only message matching the following conditions on attributes:
            # color: 'red' or 'orange' or begins with 'bl'
            # size: anything but 'small' or 'medium'
            # price: between 100 and 200 or greater than 300
            # store: attribute must be present
            my_topic.add_subscription(subscriptions.LambdaSubscription(fn,
                filter_policy={
                    "color": sns.SubscriptionFilter.string_filter(
                        allowlist=["red", "orange"],
                        match_prefixes=["bl"]
                    ),
                    "size": sns.SubscriptionFilter.string_filter(
                        denylist=["small", "medium"]
                    ),
                    "price": sns.SubscriptionFilter.numeric_filter(
                        between=lambda.aws_sns.BetweenCondition(start=100, stop=200),
                        greater_than=300
                    ),
                    "store": sns.SubscriptionFilter.exists_filter()
                }
            ))
        '''
        if isinstance(between, dict):
            between = BetweenCondition(**between)
        if isinstance(between_strict, dict):
            between_strict = BetweenCondition(**between_strict)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fd7a1cbc419a57014617945296ca43be7e9d4f73f66daf91d641205bf4a58cc)
            check_type(argname="argument allowlist", value=allowlist, expected_type=type_hints["allowlist"])
            check_type(argname="argument between", value=between, expected_type=type_hints["between"])
            check_type(argname="argument between_strict", value=between_strict, expected_type=type_hints["between_strict"])
            check_type(argname="argument greater_than", value=greater_than, expected_type=type_hints["greater_than"])
            check_type(argname="argument greater_than_or_equal_to", value=greater_than_or_equal_to, expected_type=type_hints["greater_than_or_equal_to"])
            check_type(argname="argument less_than", value=less_than, expected_type=type_hints["less_than"])
            check_type(argname="argument less_than_or_equal_to", value=less_than_or_equal_to, expected_type=type_hints["less_than_or_equal_to"])
            check_type(argname="argument whitelist", value=whitelist, expected_type=type_hints["whitelist"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowlist is not None:
            self._values["allowlist"] = allowlist
        if between is not None:
            self._values["between"] = between
        if between_strict is not None:
            self._values["between_strict"] = between_strict
        if greater_than is not None:
            self._values["greater_than"] = greater_than
        if greater_than_or_equal_to is not None:
            self._values["greater_than_or_equal_to"] = greater_than_or_equal_to
        if less_than is not None:
            self._values["less_than"] = less_than
        if less_than_or_equal_to is not None:
            self._values["less_than_or_equal_to"] = less_than_or_equal_to
        if whitelist is not None:
            self._values["whitelist"] = whitelist

    @builtins.property
    def allowlist(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''(experimental) Match one or more values.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("allowlist")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def between(self) -> typing.Optional[BetweenCondition]:
        '''(experimental) Match values that are between the specified values.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("between")
        return typing.cast(typing.Optional[BetweenCondition], result)

    @builtins.property
    def between_strict(self) -> typing.Optional[BetweenCondition]:
        '''(experimental) Match values that are strictly between the specified values.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("between_strict")
        return typing.cast(typing.Optional[BetweenCondition], result)

    @builtins.property
    def greater_than(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Match values that are greater than the specified value.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("greater_than")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def greater_than_or_equal_to(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Match values that are greater than or equal to the specified value.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("greater_than_or_equal_to")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def less_than(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Match values that are less than the specified value.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("less_than")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def less_than_or_equal_to(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Match values that are less than or equal to the specified value.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("less_than_or_equal_to")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def whitelist(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''(deprecated) Match one or more values.

        :default: - None

        :deprecated: use ``allowlist``

        :stability: deprecated
        '''
        result = self._values.get("whitelist")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NumericConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_sns.StringConditions",
    jsii_struct_bases=[],
    name_mapping={
        "allowlist": "allowlist",
        "blacklist": "blacklist",
        "denylist": "denylist",
        "match_prefixes": "matchPrefixes",
        "whitelist": "whitelist",
    },
)
class StringConditions:
    def __init__(
        self,
        *,
        allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
        blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
        denylist: typing.Optional[typing.Sequence[builtins.str]] = None,
        match_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Conditions that can be applied to string attributes.

        :param allowlist: (experimental) Match one or more values. Default: - None
        :param blacklist: (deprecated) Match any value that doesn't include any of the specified values. Default: - None
        :param denylist: (experimental) Match any value that doesn't include any of the specified values. Default: - None
        :param match_prefixes: (experimental) Matches values that begins with the specified prefixes. Default: - None
        :param whitelist: (deprecated) Match one or more values. Default: - None

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as lambda_
            # fn: lambda.Function
            
            
            my_topic = sns.Topic(self, "MyTopic")
            
            # Lambda should receive only message matching the following conditions on attributes:
            # color: 'red' or 'orange' or begins with 'bl'
            # size: anything but 'small' or 'medium'
            # price: between 100 and 200 or greater than 300
            # store: attribute must be present
            my_topic.add_subscription(subscriptions.LambdaSubscription(fn,
                filter_policy={
                    "color": sns.SubscriptionFilter.string_filter(
                        allowlist=["red", "orange"],
                        match_prefixes=["bl"]
                    ),
                    "size": sns.SubscriptionFilter.string_filter(
                        denylist=["small", "medium"]
                    ),
                    "price": sns.SubscriptionFilter.numeric_filter(
                        between=lambda.aws_sns.BetweenCondition(start=100, stop=200),
                        greater_than=300
                    ),
                    "store": sns.SubscriptionFilter.exists_filter()
                }
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cacb15fbe036a504f685b132a6de8eff551922d1b77c97a5017612fe7c68eed)
            check_type(argname="argument allowlist", value=allowlist, expected_type=type_hints["allowlist"])
            check_type(argname="argument blacklist", value=blacklist, expected_type=type_hints["blacklist"])
            check_type(argname="argument denylist", value=denylist, expected_type=type_hints["denylist"])
            check_type(argname="argument match_prefixes", value=match_prefixes, expected_type=type_hints["match_prefixes"])
            check_type(argname="argument whitelist", value=whitelist, expected_type=type_hints["whitelist"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowlist is not None:
            self._values["allowlist"] = allowlist
        if blacklist is not None:
            self._values["blacklist"] = blacklist
        if denylist is not None:
            self._values["denylist"] = denylist
        if match_prefixes is not None:
            self._values["match_prefixes"] = match_prefixes
        if whitelist is not None:
            self._values["whitelist"] = whitelist

    @builtins.property
    def allowlist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Match one or more values.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("allowlist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def blacklist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Match any value that doesn't include any of the specified values.

        :default: - None

        :deprecated: use ``denylist``

        :stability: deprecated
        '''
        result = self._values.get("blacklist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def denylist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Match any value that doesn't include any of the specified values.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("denylist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def match_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Matches values that begins with the specified prefixes.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("match_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Match one or more values.

        :default: - None

        :deprecated: use ``allowlist``

        :stability: deprecated
        '''
        result = self._values.get("whitelist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StringConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Subscription(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sns.Subscription",
):
    '''(experimental) A new subscription.

    Prefer to use the ``ITopic.addSubscription()`` methods to create instances of
    this class.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from monocdk.aws_kinesisfirehose import DeliveryStream
        # stream: DeliveryStream
        
        
        topic = sns.Topic(self, "Topic")
        
        sns.Subscription(self, "Subscription",
            topic=topic,
            endpoint=stream.delivery_stream_arn,
            protocol=sns.SubscriptionProtocol.FIREHOSE,
            subscription_role_arn="SAMPLE_ARN"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        topic: ITopic,
        endpoint: builtins.str,
        protocol: "SubscriptionProtocol",
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, "SubscriptionFilter"]] = None,
        raw_message_delivery: typing.Optional[builtins.bool] = None,
        region: typing.Optional[builtins.str] = None,
        subscription_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param topic: (experimental) The topic to subscribe to.
        :param endpoint: (experimental) The subscription endpoint. The meaning of this value depends on the value for 'protocol'.
        :param protocol: (experimental) What type of subscription to add.
        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered
        :param raw_message_delivery: (experimental) true if raw message delivery is enabled for the subscription. Raw messages are free of JSON formatting and can be sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple Notification Service API Reference. Default: false
        :param region: (experimental) The region where the topic resides, in the case of cross-region subscriptions. Default: - the region where the CloudFormation stack is being deployed.
        :param subscription_role_arn: (experimental) Arn of role allowing access to firehose delivery stream. Required for a firehose subscription protocol. Default: - No subscription role is provided

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ee16e53d8b186347a3d2d265470021e018e55d3b0dafa8d988976381b1a0a53)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SubscriptionProps(
            topic=topic,
            endpoint=endpoint,
            protocol=protocol,
            dead_letter_queue=dead_letter_queue,
            filter_policy=filter_policy,
            raw_message_delivery=raw_message_delivery,
            region=region,
            subscription_role_arn=subscription_role_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="deadLetterQueue")
    def dead_letter_queue(self) -> typing.Optional[_IQueue_45a01ab4]:
        '''(experimental) The DLQ associated with this subscription if present.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IQueue_45a01ab4], jsii.get(self, "deadLetterQueue"))


class SubscriptionFilter(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sns.SubscriptionFilter",
):
    '''(experimental) A subscription filter for an attribute.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as lambda_
        # fn: lambda.Function
        
        
        my_topic = sns.Topic(self, "MyTopic")
        
        # Lambda should receive only message matching the following conditions on attributes:
        # color: 'red' or 'orange' or begins with 'bl'
        # size: anything but 'small' or 'medium'
        # price: between 100 and 200 or greater than 300
        # store: attribute must be present
        my_topic.add_subscription(subscriptions.LambdaSubscription(fn,
            filter_policy={
                "color": sns.SubscriptionFilter.string_filter(
                    allowlist=["red", "orange"],
                    match_prefixes=["bl"]
                ),
                "size": sns.SubscriptionFilter.string_filter(
                    denylist=["small", "medium"]
                ),
                "price": sns.SubscriptionFilter.numeric_filter(
                    between=lambda.aws_sns.BetweenCondition(start=100, stop=200),
                    greater_than=300
                ),
                "store": sns.SubscriptionFilter.exists_filter()
            }
        ))
    '''

    def __init__(
        self,
        conditions: typing.Optional[typing.Sequence[typing.Any]] = None,
    ) -> None:
        '''
        :param conditions: conditions that specify the message attributes that should be included, excluded, matched, etc.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69001fc13cba78aaac4ba207974efbc6c8e48f13805525c1e39a20569794062b)
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
        jsii.create(self.__class__, self, [conditions])

    @jsii.member(jsii_name="existsFilter")
    @builtins.classmethod
    def exists_filter(cls) -> "SubscriptionFilter":
        '''(experimental) Returns a subscription filter for attribute key matching.

        :stability: experimental
        '''
        return typing.cast("SubscriptionFilter", jsii.sinvoke(cls, "existsFilter", []))

    @jsii.member(jsii_name="numericFilter")
    @builtins.classmethod
    def numeric_filter(
        cls,
        *,
        allowlist: typing.Optional[typing.Sequence[jsii.Number]] = None,
        between: typing.Optional[typing.Union[BetweenCondition, typing.Dict[builtins.str, typing.Any]]] = None,
        between_strict: typing.Optional[typing.Union[BetweenCondition, typing.Dict[builtins.str, typing.Any]]] = None,
        greater_than: typing.Optional[jsii.Number] = None,
        greater_than_or_equal_to: typing.Optional[jsii.Number] = None,
        less_than: typing.Optional[jsii.Number] = None,
        less_than_or_equal_to: typing.Optional[jsii.Number] = None,
        whitelist: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> "SubscriptionFilter":
        '''(experimental) Returns a subscription filter for a numeric attribute.

        :param allowlist: (experimental) Match one or more values. Default: - None
        :param between: (experimental) Match values that are between the specified values. Default: - None
        :param between_strict: (experimental) Match values that are strictly between the specified values. Default: - None
        :param greater_than: (experimental) Match values that are greater than the specified value. Default: - None
        :param greater_than_or_equal_to: (experimental) Match values that are greater than or equal to the specified value. Default: - None
        :param less_than: (experimental) Match values that are less than the specified value. Default: - None
        :param less_than_or_equal_to: (experimental) Match values that are less than or equal to the specified value. Default: - None
        :param whitelist: (deprecated) Match one or more values. Default: - None

        :stability: experimental
        '''
        numeric_conditions = NumericConditions(
            allowlist=allowlist,
            between=between,
            between_strict=between_strict,
            greater_than=greater_than,
            greater_than_or_equal_to=greater_than_or_equal_to,
            less_than=less_than,
            less_than_or_equal_to=less_than_or_equal_to,
            whitelist=whitelist,
        )

        return typing.cast("SubscriptionFilter", jsii.sinvoke(cls, "numericFilter", [numeric_conditions]))

    @jsii.member(jsii_name="stringFilter")
    @builtins.classmethod
    def string_filter(
        cls,
        *,
        allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
        blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
        denylist: typing.Optional[typing.Sequence[builtins.str]] = None,
        match_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> "SubscriptionFilter":
        '''(experimental) Returns a subscription filter for a string attribute.

        :param allowlist: (experimental) Match one or more values. Default: - None
        :param blacklist: (deprecated) Match any value that doesn't include any of the specified values. Default: - None
        :param denylist: (experimental) Match any value that doesn't include any of the specified values. Default: - None
        :param match_prefixes: (experimental) Matches values that begins with the specified prefixes. Default: - None
        :param whitelist: (deprecated) Match one or more values. Default: - None

        :stability: experimental
        '''
        string_conditions = StringConditions(
            allowlist=allowlist,
            blacklist=blacklist,
            denylist=denylist,
            match_prefixes=match_prefixes,
            whitelist=whitelist,
        )

        return typing.cast("SubscriptionFilter", jsii.sinvoke(cls, "stringFilter", [string_conditions]))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> typing.List[typing.Any]:
        '''(experimental) conditions that specify the message attributes that should be included, excluded, matched, etc.

        :stability: experimental
        '''
        return typing.cast(typing.List[typing.Any], jsii.get(self, "conditions"))


@jsii.data_type(
    jsii_type="monocdk.aws_sns.SubscriptionOptions",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint": "endpoint",
        "protocol": "protocol",
        "dead_letter_queue": "deadLetterQueue",
        "filter_policy": "filterPolicy",
        "raw_message_delivery": "rawMessageDelivery",
        "region": "region",
        "subscription_role_arn": "subscriptionRoleArn",
    },
)
class SubscriptionOptions:
    def __init__(
        self,
        *,
        endpoint: builtins.str,
        protocol: "SubscriptionProtocol",
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, SubscriptionFilter]] = None,
        raw_message_delivery: typing.Optional[builtins.bool] = None,
        region: typing.Optional[builtins.str] = None,
        subscription_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for creating a new subscription.

        :param endpoint: (experimental) The subscription endpoint. The meaning of this value depends on the value for 'protocol'.
        :param protocol: (experimental) What type of subscription to add.
        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered
        :param raw_message_delivery: (experimental) true if raw message delivery is enabled for the subscription. Raw messages are free of JSON formatting and can be sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple Notification Service API Reference. Default: false
        :param region: (experimental) The region where the topic resides, in the case of cross-region subscriptions. Default: - the region where the CloudFormation stack is being deployed.
        :param subscription_role_arn: (experimental) Arn of role allowing access to firehose delivery stream. Required for a firehose subscription protocol. Default: - No subscription role is provided

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sns as sns
            from monocdk import aws_sqs as sqs
            
            # queue: sqs.Queue
            # subscription_filter: sns.SubscriptionFilter
            
            subscription_options = sns.SubscriptionOptions(
                endpoint="endpoint",
                protocol=sns.SubscriptionProtocol.HTTP,
            
                # the properties below are optional
                dead_letter_queue=queue,
                filter_policy={
                    "filter_policy_key": subscription_filter
                },
                raw_message_delivery=False,
                region="region",
                subscription_role_arn="subscriptionRoleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2cf0c048b9573e158402c3fefe24a8e7f513d7d2ff4a87adbfbc50d37c16a9c)
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument filter_policy", value=filter_policy, expected_type=type_hints["filter_policy"])
            check_type(argname="argument raw_message_delivery", value=raw_message_delivery, expected_type=type_hints["raw_message_delivery"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument subscription_role_arn", value=subscription_role_arn, expected_type=type_hints["subscription_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint": endpoint,
            "protocol": protocol,
        }
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy
        if raw_message_delivery is not None:
            self._values["raw_message_delivery"] = raw_message_delivery
        if region is not None:
            self._values["region"] = region
        if subscription_role_arn is not None:
            self._values["subscription_role_arn"] = subscription_role_arn

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''(experimental) The subscription endpoint.

        The meaning of this value depends on the value for 'protocol'.

        :stability: experimental
        '''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> "SubscriptionProtocol":
        '''(experimental) What type of subscription to add.

        :stability: experimental
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast("SubscriptionProtocol", result)

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_45a01ab4]:
        '''(experimental) Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        :default: - No dead letter queue enabled.

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_45a01ab4], result)

    @builtins.property
    def filter_policy(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, SubscriptionFilter]]:
        '''(experimental) The filter policy.

        :default: - all messages are delivered

        :stability: experimental
        '''
        result = self._values.get("filter_policy")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, SubscriptionFilter]], result)

    @builtins.property
    def raw_message_delivery(self) -> typing.Optional[builtins.bool]:
        '''(experimental) true if raw message delivery is enabled for the subscription.

        Raw messages are free of JSON formatting and can be
        sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple
        Notification Service API Reference.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("raw_message_delivery")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region where the topic resides, in the case of cross-region subscriptions.

        :default: - the region where the CloudFormation stack is being deployed.

        :stability: experimental
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-region
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscription_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Arn of role allowing access to firehose delivery stream.

        Required for a firehose subscription protocol.

        :default: - No subscription role is provided

        :stability: experimental
        '''
        result = self._values.get("subscription_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubscriptionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_sns.SubscriptionProps",
    jsii_struct_bases=[SubscriptionOptions],
    name_mapping={
        "endpoint": "endpoint",
        "protocol": "protocol",
        "dead_letter_queue": "deadLetterQueue",
        "filter_policy": "filterPolicy",
        "raw_message_delivery": "rawMessageDelivery",
        "region": "region",
        "subscription_role_arn": "subscriptionRoleArn",
        "topic": "topic",
    },
)
class SubscriptionProps(SubscriptionOptions):
    def __init__(
        self,
        *,
        endpoint: builtins.str,
        protocol: "SubscriptionProtocol",
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, SubscriptionFilter]] = None,
        raw_message_delivery: typing.Optional[builtins.bool] = None,
        region: typing.Optional[builtins.str] = None,
        subscription_role_arn: typing.Optional[builtins.str] = None,
        topic: ITopic,
    ) -> None:
        '''(experimental) Properties for creating a new subscription.

        :param endpoint: (experimental) The subscription endpoint. The meaning of this value depends on the value for 'protocol'.
        :param protocol: (experimental) What type of subscription to add.
        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered
        :param raw_message_delivery: (experimental) true if raw message delivery is enabled for the subscription. Raw messages are free of JSON formatting and can be sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple Notification Service API Reference. Default: false
        :param region: (experimental) The region where the topic resides, in the case of cross-region subscriptions. Default: - the region where the CloudFormation stack is being deployed.
        :param subscription_role_arn: (experimental) Arn of role allowing access to firehose delivery stream. Required for a firehose subscription protocol. Default: - No subscription role is provided
        :param topic: (experimental) The topic to subscribe to.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            from monocdk.aws_kinesisfirehose import DeliveryStream
            # stream: DeliveryStream
            
            
            topic = sns.Topic(self, "Topic")
            
            sns.Subscription(self, "Subscription",
                topic=topic,
                endpoint=stream.delivery_stream_arn,
                protocol=sns.SubscriptionProtocol.FIREHOSE,
                subscription_role_arn="SAMPLE_ARN"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa7d5979ceaaa23260b5dacadeea711d436a2eb2b48cf211dfbb4fbcf7c29d1a)
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument filter_policy", value=filter_policy, expected_type=type_hints["filter_policy"])
            check_type(argname="argument raw_message_delivery", value=raw_message_delivery, expected_type=type_hints["raw_message_delivery"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument subscription_role_arn", value=subscription_role_arn, expected_type=type_hints["subscription_role_arn"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint": endpoint,
            "protocol": protocol,
            "topic": topic,
        }
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy
        if raw_message_delivery is not None:
            self._values["raw_message_delivery"] = raw_message_delivery
        if region is not None:
            self._values["region"] = region
        if subscription_role_arn is not None:
            self._values["subscription_role_arn"] = subscription_role_arn

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''(experimental) The subscription endpoint.

        The meaning of this value depends on the value for 'protocol'.

        :stability: experimental
        '''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> "SubscriptionProtocol":
        '''(experimental) What type of subscription to add.

        :stability: experimental
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast("SubscriptionProtocol", result)

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_45a01ab4]:
        '''(experimental) Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        :default: - No dead letter queue enabled.

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_45a01ab4], result)

    @builtins.property
    def filter_policy(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, SubscriptionFilter]]:
        '''(experimental) The filter policy.

        :default: - all messages are delivered

        :stability: experimental
        '''
        result = self._values.get("filter_policy")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, SubscriptionFilter]], result)

    @builtins.property
    def raw_message_delivery(self) -> typing.Optional[builtins.bool]:
        '''(experimental) true if raw message delivery is enabled for the subscription.

        Raw messages are free of JSON formatting and can be
        sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple
        Notification Service API Reference.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("raw_message_delivery")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region where the topic resides, in the case of cross-region subscriptions.

        :default: - the region where the CloudFormation stack is being deployed.

        :stability: experimental
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-region
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscription_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Arn of role allowing access to firehose delivery stream.

        Required for a firehose subscription protocol.

        :default: - No subscription role is provided

        :stability: experimental
        '''
        result = self._values.get("subscription_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def topic(self) -> ITopic:
        '''(experimental) The topic to subscribe to.

        :stability: experimental
        '''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(ITopic, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_sns.SubscriptionProtocol")
class SubscriptionProtocol(enum.Enum):
    '''(experimental) The type of subscription, controlling the type of the endpoint parameter.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from monocdk.aws_kinesisfirehose import DeliveryStream
        # stream: DeliveryStream
        
        
        topic = sns.Topic(self, "Topic")
        
        sns.Subscription(self, "Subscription",
            topic=topic,
            endpoint=stream.delivery_stream_arn,
            protocol=sns.SubscriptionProtocol.FIREHOSE,
            subscription_role_arn="SAMPLE_ARN"
        )
    '''

    HTTP = "HTTP"
    '''(experimental) JSON-encoded message is POSTED to an HTTP url.

    :stability: experimental
    '''
    HTTPS = "HTTPS"
    '''(experimental) JSON-encoded message is POSTed to an HTTPS url.

    :stability: experimental
    '''
    EMAIL = "EMAIL"
    '''(experimental) Notifications are sent via email.

    :stability: experimental
    '''
    EMAIL_JSON = "EMAIL_JSON"
    '''(experimental) Notifications are JSON-encoded and sent via mail.

    :stability: experimental
    '''
    SMS = "SMS"
    '''(experimental) Notification is delivered by SMS.

    :stability: experimental
    '''
    SQS = "SQS"
    '''(experimental) Notifications are enqueued into an SQS queue.

    :stability: experimental
    '''
    APPLICATION = "APPLICATION"
    '''(experimental) JSON-encoded notifications are sent to a mobile app endpoint.

    :stability: experimental
    '''
    LAMBDA = "LAMBDA"
    '''(experimental) Notifications trigger a Lambda function.

    :stability: experimental
    '''
    FIREHOSE = "FIREHOSE"
    '''(experimental) Notifications put records into a firehose delivery stream.

    :stability: experimental
    '''


@jsii.implements(ITopic)
class TopicBase(
    _Resource_abff4495,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_sns.TopicBase",
):
    '''(experimental) Either a new or imported Topic.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: (experimental) The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: (experimental) ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: (experimental) The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: (experimental) The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebe3d0e5b5c0fb1009e24150d13034b22f5dd836095883ddd3dafea48b0d11bd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _ResourceProps_9b554c0f(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addSubscription")
    def add_subscription(self, subscription: ITopicSubscription) -> None:
        '''(experimental) Subscribe some endpoint to this topic.

        :param subscription: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__944ccf3ec49db8acb348d756aab713c22a9eec4f064210ebb33b89c949bcfef9)
            check_type(argname="argument subscription", value=subscription, expected_type=type_hints["subscription"])
        return typing.cast(None, jsii.invoke(self, "addSubscription", [subscription]))

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        '''(experimental) Adds a statement to the IAM resource policy associated with this topic.

        If this topic was created in this stack (``new Topic``), a topic policy
        will be automatically created upon the first call to ``addToPolicy``. If
        the topic is imported (``Topic.import``), then this is a no-op.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc59dc7abc843842cc85ffb3cf133e7ff7436ef52b5c616578a617a7eaf0d376)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(_AddToResourcePolicyResult_0fd9d2a9, jsii.invoke(self, "addToResourcePolicy", [statement]))

    @jsii.member(jsii_name="bindAsNotificationRuleTarget")
    def bind_as_notification_rule_target(
        self,
        _scope: _constructs_77d1e7e8.Construct,
    ) -> _NotificationRuleTargetConfig_a582558e:
        '''(experimental) Represents a notification target That allows SNS topic to associate with this rule target.

        :param _scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bbb86f19b019f04252ee6c1ad32fd447f0e0f2c8ea3b2ac47360dc1a8146613)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(_NotificationRuleTargetConfig_a582558e, jsii.invoke(self, "bindAsNotificationRuleTarget", [_scope]))

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant topic publishing permissions to the given identity.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f63c1578e8e1f5f26cbbc7b94a7f4caf459e29f71f74b7d9f910bb767df9577)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPublish", [grantee]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Return the given named metric for this Topic.

        :param metric_name: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f6226659346e1b02f9dfc6e234aa34b984be99568cdc4d8ff5823f1108d3289)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricNumberOfMessagesPublished")
    def metric_number_of_messages_published(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The number of messages published to your Amazon SNS topics.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNumberOfMessagesPublished", [props]))

    @jsii.member(jsii_name="metricNumberOfNotificationsDelivered")
    def metric_number_of_notifications_delivered(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The number of messages successfully delivered from your Amazon SNS topics to subscribing endpoints.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNumberOfNotificationsDelivered", [props]))

    @jsii.member(jsii_name="metricNumberOfNotificationsFailed")
    def metric_number_of_notifications_failed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The number of messages that Amazon SNS failed to deliver.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNumberOfNotificationsFailed", [props]))

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOut")
    def metric_number_of_notifications_filtered_out(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The number of messages that were rejected by subscription filter policies.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNumberOfNotificationsFilteredOut", [props]))

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutInvalidAttributes")
    def metric_number_of_notifications_filtered_out_invalid_attributes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The number of messages that were rejected by subscription filter policies because the messages' attributes are invalid.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNumberOfNotificationsFilteredOutInvalidAttributes", [props]))

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutNoMessageAttributes")
    def metric_number_of_notifications_filtered_out_no_message_attributes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The number of messages that were rejected by subscription filter policies because the messages have no attributes.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNumberOfNotificationsFilteredOutNoMessageAttributes", [props]))

    @jsii.member(jsii_name="metricPublishSize")
    def metric_publish_size(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the size of messages published through this topic.

        Average over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricPublishSize", [props]))

    @jsii.member(jsii_name="metricSMSMonthToDateSpentUSD")
    def metric_sms_month_to_date_spent_usd(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The charges you have accrued since the start of the current calendar month for sending SMS messages.

        Maximum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSMSMonthToDateSpentUSD", [props]))

    @jsii.member(jsii_name="metricSMSSuccessRate")
    def metric_sms_success_rate(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The rate of successful SMS message deliveries.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSMSSuccessRate", [props]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''(experimental) Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property
    @jsii.member(jsii_name="autoCreatePolicy")
    @abc.abstractmethod
    def _auto_create_policy(self) -> builtins.bool:
        '''(experimental) Controls automatic creation of policy objects.

        Set by subclasses.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="fifo")
    @abc.abstractmethod
    def fifo(self) -> builtins.bool:
        '''(experimental) Whether this topic is an Amazon SNS FIFO queue.

        If false, this is a standard topic.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="topicArn")
    @abc.abstractmethod
    def topic_arn(self) -> builtins.str:
        '''(experimental) The ARN of the topic.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="topicName")
    @abc.abstractmethod
    def topic_name(self) -> builtins.str:
        '''(experimental) The name of the topic.

        :stability: experimental
        '''
        ...


class _TopicBaseProxy(
    TopicBase,
    jsii.proxy_for(_Resource_abff4495), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> builtins.bool:
        '''(experimental) Controls automatic creation of policy objects.

        Set by subclasses.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "autoCreatePolicy"))

    @builtins.property
    @jsii.member(jsii_name="fifo")
    def fifo(self) -> builtins.bool:
        '''(experimental) Whether this topic is an Amazon SNS FIFO queue.

        If false, this is a standard topic.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "fifo"))

    @builtins.property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> builtins.str:
        '''(experimental) The ARN of the topic.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "topicArn"))

    @builtins.property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> builtins.str:
        '''(experimental) The name of the topic.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "topicName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, TopicBase).__jsii_proxy_class__ = lambda : _TopicBaseProxy


class TopicPolicy(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sns.TopicPolicy",
):
    '''(experimental) The policy for an SNS Topic.

    Policies define the operations that are allowed on this resource.

    You almost never need to define this construct directly.

    All AWS resources that support resource policies have a method called
    ``addToResourcePolicy()``, which will automatically create a new resource
    policy if one doesn't exist yet, otherwise it will add to the existing
    policy.

    Prefer to use ``addToResourcePolicy()`` instead.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        topic = sns.Topic(self, "Topic")
        topic_policy = sns.TopicPolicy(self, "TopicPolicy",
            topics=[topic]
        )
        
        topic_policy.document.add_statements(iam.PolicyStatement(
            actions=["sns:Subscribe"],
            principals=[iam.AnyPrincipal()],
            resources=[topic.topic_arn]
        ))
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        topics: typing.Sequence[ITopic],
        policy_document: typing.Optional[_PolicyDocument_b5de5177] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param topics: (experimental) The set of topics this policy applies to.
        :param policy_document: (experimental) IAM policy document to apply to topic(s). Default: empty policy document

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5f00c0c72c3b9da3b9f2bd2b0ffbebe83cd606c7c8ec1747defb3cdf64d5b3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TopicPolicyProps(topics=topics, policy_document=policy_document)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="document")
    def document(self) -> _PolicyDocument_b5de5177:
        '''(experimental) The IAM policy document for this policy.

        :stability: experimental
        '''
        return typing.cast(_PolicyDocument_b5de5177, jsii.get(self, "document"))


@jsii.data_type(
    jsii_type="monocdk.aws_sns.TopicPolicyProps",
    jsii_struct_bases=[],
    name_mapping={"topics": "topics", "policy_document": "policyDocument"},
)
class TopicPolicyProps:
    def __init__(
        self,
        *,
        topics: typing.Sequence[ITopic],
        policy_document: typing.Optional[_PolicyDocument_b5de5177] = None,
    ) -> None:
        '''(experimental) Properties to associate SNS topics with a policy.

        :param topics: (experimental) The set of topics this policy applies to.
        :param policy_document: (experimental) IAM policy document to apply to topic(s). Default: empty policy document

        :stability: experimental
        :exampleMetadata: infused

        Example::

            topic = sns.Topic(self, "Topic")
            topic_policy = sns.TopicPolicy(self, "TopicPolicy",
                topics=[topic]
            )
            
            topic_policy.document.add_statements(iam.PolicyStatement(
                actions=["sns:Subscribe"],
                principals=[iam.AnyPrincipal()],
                resources=[topic.topic_arn]
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5923bc937499e5f8cb21264c40f270befd867f657a02f495c9ebd1dd85a0820a)
            check_type(argname="argument topics", value=topics, expected_type=type_hints["topics"])
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topics": topics,
        }
        if policy_document is not None:
            self._values["policy_document"] = policy_document

    @builtins.property
    def topics(self) -> typing.List[ITopic]:
        '''(experimental) The set of topics this policy applies to.

        :stability: experimental
        '''
        result = self._values.get("topics")
        assert result is not None, "Required property 'topics' is missing"
        return typing.cast(typing.List[ITopic], result)

    @builtins.property
    def policy_document(self) -> typing.Optional[_PolicyDocument_b5de5177]:
        '''(experimental) IAM policy document to apply to topic(s).

        :default: empty policy document

        :stability: experimental
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Optional[_PolicyDocument_b5de5177], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TopicPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_sns.TopicProps",
    jsii_struct_bases=[],
    name_mapping={
        "content_based_deduplication": "contentBasedDeduplication",
        "display_name": "displayName",
        "fifo": "fifo",
        "master_key": "masterKey",
        "topic_name": "topicName",
    },
)
class TopicProps:
    def __init__(
        self,
        *,
        content_based_deduplication: typing.Optional[builtins.bool] = None,
        display_name: typing.Optional[builtins.str] = None,
        fifo: typing.Optional[builtins.bool] = None,
        master_key: typing.Optional[_IKey_36930160] = None,
        topic_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a new SNS topic.

        :param content_based_deduplication: (experimental) Enables content-based deduplication for FIFO topics. Default: None
        :param display_name: (experimental) A developer-defined string that can be used to identify this SNS topic. Default: None
        :param fifo: (experimental) Set to true to create a FIFO topic. Default: None
        :param master_key: (experimental) A KMS Key, either managed by this CDK app, or imported. Default: None
        :param topic_name: (experimental) A name for the topic. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the topic name. For more information, see Name Type. Default: Generated name

        :stability: experimental
        :exampleMetadata: infused

        Example::

            topic = sns.Topic(self, "Topic",
                display_name="Customer subscription topic"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ae7fe9bfb3615742d3be0065101c494719d933cd9707b6c378ca4b6d33cbd11)
            check_type(argname="argument content_based_deduplication", value=content_based_deduplication, expected_type=type_hints["content_based_deduplication"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument fifo", value=fifo, expected_type=type_hints["fifo"])
            check_type(argname="argument master_key", value=master_key, expected_type=type_hints["master_key"])
            check_type(argname="argument topic_name", value=topic_name, expected_type=type_hints["topic_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if content_based_deduplication is not None:
            self._values["content_based_deduplication"] = content_based_deduplication
        if display_name is not None:
            self._values["display_name"] = display_name
        if fifo is not None:
            self._values["fifo"] = fifo
        if master_key is not None:
            self._values["master_key"] = master_key
        if topic_name is not None:
            self._values["topic_name"] = topic_name

    @builtins.property
    def content_based_deduplication(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables content-based deduplication for FIFO topics.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("content_based_deduplication")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A developer-defined string that can be used to identify this SNS topic.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fifo(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set to true to create a FIFO topic.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("fifo")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def master_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) A KMS Key, either managed by this CDK app, or imported.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("master_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def topic_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the topic.

        If you don't specify a name, AWS CloudFormation generates a unique
        physical ID and uses that ID for the topic name. For more information,
        see Name Type.

        :default: Generated name

        :stability: experimental
        '''
        result = self._values.get("topic_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TopicProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_sns.TopicSubscriptionConfig",
    jsii_struct_bases=[SubscriptionOptions],
    name_mapping={
        "endpoint": "endpoint",
        "protocol": "protocol",
        "dead_letter_queue": "deadLetterQueue",
        "filter_policy": "filterPolicy",
        "raw_message_delivery": "rawMessageDelivery",
        "region": "region",
        "subscription_role_arn": "subscriptionRoleArn",
        "subscriber_id": "subscriberId",
        "subscriber_scope": "subscriberScope",
    },
)
class TopicSubscriptionConfig(SubscriptionOptions):
    def __init__(
        self,
        *,
        endpoint: builtins.str,
        protocol: SubscriptionProtocol,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, SubscriptionFilter]] = None,
        raw_message_delivery: typing.Optional[builtins.bool] = None,
        region: typing.Optional[builtins.str] = None,
        subscription_role_arn: typing.Optional[builtins.str] = None,
        subscriber_id: builtins.str,
        subscriber_scope: typing.Optional[_Construct_e78e779f] = None,
    ) -> None:
        '''(experimental) Subscription configuration.

        :param endpoint: (experimental) The subscription endpoint. The meaning of this value depends on the value for 'protocol'.
        :param protocol: (experimental) What type of subscription to add.
        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered
        :param raw_message_delivery: (experimental) true if raw message delivery is enabled for the subscription. Raw messages are free of JSON formatting and can be sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple Notification Service API Reference. Default: false
        :param region: (experimental) The region where the topic resides, in the case of cross-region subscriptions. Default: - the region where the CloudFormation stack is being deployed.
        :param subscription_role_arn: (experimental) Arn of role allowing access to firehose delivery stream. Required for a firehose subscription protocol. Default: - No subscription role is provided
        :param subscriber_id: (experimental) The id of the SNS subscription resource created under ``scope``. In most cases, it is recommended to use the ``uniqueId`` of the topic you are subscribing to.
        :param subscriber_scope: (experimental) The scope in which to create the SNS subscription resource. Normally you'd want the subscription to be created on the consuming stack because the topic is usually referenced by the consumer's resource policy (e.g. SQS queue policy). Otherwise, it will cause a cyclic reference. If this is undefined, the subscription will be created on the topic's stack. Default: - use the topic as the scope of the subscription, in which case ``subscriberId`` must be defined.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_sns as sns
            from monocdk import aws_sqs as sqs
            
            # construct: monocdk.Construct
            # queue: sqs.Queue
            # subscription_filter: sns.SubscriptionFilter
            
            topic_subscription_config = sns.TopicSubscriptionConfig(
                endpoint="endpoint",
                protocol=sns.SubscriptionProtocol.HTTP,
                subscriber_id="subscriberId",
            
                # the properties below are optional
                dead_letter_queue=queue,
                filter_policy={
                    "filter_policy_key": subscription_filter
                },
                raw_message_delivery=False,
                region="region",
                subscriber_scope=construct,
                subscription_role_arn="subscriptionRoleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f19954a293cde016ddcf70af6650421744c961fa26042d4a8cad35d7d280df3a)
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument filter_policy", value=filter_policy, expected_type=type_hints["filter_policy"])
            check_type(argname="argument raw_message_delivery", value=raw_message_delivery, expected_type=type_hints["raw_message_delivery"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument subscription_role_arn", value=subscription_role_arn, expected_type=type_hints["subscription_role_arn"])
            check_type(argname="argument subscriber_id", value=subscriber_id, expected_type=type_hints["subscriber_id"])
            check_type(argname="argument subscriber_scope", value=subscriber_scope, expected_type=type_hints["subscriber_scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint": endpoint,
            "protocol": protocol,
            "subscriber_id": subscriber_id,
        }
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy
        if raw_message_delivery is not None:
            self._values["raw_message_delivery"] = raw_message_delivery
        if region is not None:
            self._values["region"] = region
        if subscription_role_arn is not None:
            self._values["subscription_role_arn"] = subscription_role_arn
        if subscriber_scope is not None:
            self._values["subscriber_scope"] = subscriber_scope

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''(experimental) The subscription endpoint.

        The meaning of this value depends on the value for 'protocol'.

        :stability: experimental
        '''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> SubscriptionProtocol:
        '''(experimental) What type of subscription to add.

        :stability: experimental
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(SubscriptionProtocol, result)

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_45a01ab4]:
        '''(experimental) Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        :default: - No dead letter queue enabled.

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_45a01ab4], result)

    @builtins.property
    def filter_policy(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, SubscriptionFilter]]:
        '''(experimental) The filter policy.

        :default: - all messages are delivered

        :stability: experimental
        '''
        result = self._values.get("filter_policy")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, SubscriptionFilter]], result)

    @builtins.property
    def raw_message_delivery(self) -> typing.Optional[builtins.bool]:
        '''(experimental) true if raw message delivery is enabled for the subscription.

        Raw messages are free of JSON formatting and can be
        sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple
        Notification Service API Reference.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("raw_message_delivery")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region where the topic resides, in the case of cross-region subscriptions.

        :default: - the region where the CloudFormation stack is being deployed.

        :stability: experimental
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-region
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscription_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Arn of role allowing access to firehose delivery stream.

        Required for a firehose subscription protocol.

        :default: - No subscription role is provided

        :stability: experimental
        '''
        result = self._values.get("subscription_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscriber_id(self) -> builtins.str:
        '''(experimental) The id of the SNS subscription resource created under ``scope``.

        In most
        cases, it is recommended to use the ``uniqueId`` of the topic you are
        subscribing to.

        :stability: experimental
        '''
        result = self._values.get("subscriber_id")
        assert result is not None, "Required property 'subscriber_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subscriber_scope(self) -> typing.Optional[_Construct_e78e779f]:
        '''(experimental) The scope in which to create the SNS subscription resource.

        Normally you'd
        want the subscription to be created on the consuming stack because the
        topic is usually referenced by the consumer's resource policy (e.g. SQS
        queue policy). Otherwise, it will cause a cyclic reference.

        If this is undefined, the subscription will be created on the topic's stack.

        :default: - use the topic as the scope of the subscription, in which case ``subscriberId`` must be defined.

        :stability: experimental
        '''
        result = self._values.get("subscriber_scope")
        return typing.cast(typing.Optional[_Construct_e78e779f], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TopicSubscriptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Topic(TopicBase, metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_sns.Topic"):
    '''(experimental) A new SNS topic.

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
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        content_based_deduplication: typing.Optional[builtins.bool] = None,
        display_name: typing.Optional[builtins.str] = None,
        fifo: typing.Optional[builtins.bool] = None,
        master_key: typing.Optional[_IKey_36930160] = None,
        topic_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param content_based_deduplication: (experimental) Enables content-based deduplication for FIFO topics. Default: None
        :param display_name: (experimental) A developer-defined string that can be used to identify this SNS topic. Default: None
        :param fifo: (experimental) Set to true to create a FIFO topic. Default: None
        :param master_key: (experimental) A KMS Key, either managed by this CDK app, or imported. Default: None
        :param topic_name: (experimental) A name for the topic. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the topic name. For more information, see Name Type. Default: Generated name

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c11f830efb1af0d3f166610e544a1d6643619a5f513cc71fd52dd48dc89a2380)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TopicProps(
            content_based_deduplication=content_based_deduplication,
            display_name=display_name,
            fifo=fifo,
            master_key=master_key,
            topic_name=topic_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromTopicArn")
    @builtins.classmethod
    def from_topic_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        topic_arn: builtins.str,
    ) -> ITopic:
        '''(experimental) Import an existing SNS topic provided an ARN.

        :param scope: The parent creating construct.
        :param id: The construct's name.
        :param topic_arn: topic ARN (i.e. arn:aws:sns:us-east-2:444455556666:MyTopic).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5865dd46cfb333775a4f2a775766014024dcf8d5d2570d2f3b3bb0b633fc458e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
        return typing.cast(ITopic, jsii.sinvoke(cls, "fromTopicArn", [scope, id, topic_arn]))

    @builtins.property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> builtins.bool:
        '''(experimental) Controls automatic creation of policy objects.

        Set by subclasses.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "autoCreatePolicy"))

    @builtins.property
    @jsii.member(jsii_name="fifo")
    def fifo(self) -> builtins.bool:
        '''(experimental) Whether this topic is an Amazon SNS FIFO queue.

        If false, this is a standard topic.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "fifo"))

    @builtins.property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> builtins.str:
        '''(experimental) The ARN of the topic.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "topicArn"))

    @builtins.property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> builtins.str:
        '''(experimental) The name of the topic.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "topicName"))


__all__ = [
    "BetweenCondition",
    "CfnSubscription",
    "CfnSubscriptionProps",
    "CfnTopic",
    "CfnTopicPolicy",
    "CfnTopicPolicyProps",
    "CfnTopicProps",
    "ITopic",
    "ITopicSubscription",
    "NumericConditions",
    "StringConditions",
    "Subscription",
    "SubscriptionFilter",
    "SubscriptionOptions",
    "SubscriptionProps",
    "SubscriptionProtocol",
    "Topic",
    "TopicBase",
    "TopicPolicy",
    "TopicPolicyProps",
    "TopicProps",
    "TopicSubscriptionConfig",
]

publication.publish()

def _typecheckingstub__6bcba6f40d1e40e50e482fae9fd174fa4286f24b64edbcc8abbccff860899bf4(
    *,
    start: jsii.Number,
    stop: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__076230a6f834505ef89eb5209456e37c9c0b48214e98c426a20b11b4cb09f04c(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    protocol: builtins.str,
    topic_arn: builtins.str,
    delivery_policy: typing.Any = None,
    endpoint: typing.Optional[builtins.str] = None,
    filter_policy: typing.Any = None,
    filter_policy_scope: typing.Optional[builtins.str] = None,
    raw_message_delivery: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    redrive_policy: typing.Any = None,
    region: typing.Optional[builtins.str] = None,
    subscription_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9885538e2f3d287043ce00f00c636c5005e7cfd167551ca15146c84f36df3e33(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac179251a959fc3ad80f532e50aa363fa643e59edb2f224074466159dd1b99f7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e50237dff74d5a80e5ab1010dbec724707098cea6f45efdfe548a5e1e224c20(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fae729db18712337548c7cd5cc81bf6ff3ffc30c0d8999bd6616d6801be589b(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bab8bd725e3396d322ea4f2f1993c7e081f97559cc7981b6518d15df59a1ecf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1502081a359e821747a81a7d5a46a689dd7dabde478c368d061652c67dfd1789(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a707e7eac08260016b837817369f151266569f2f65d100c2e8ff45c592d911(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb40c522c000821a88715bb6b991a7fecf77c7cd49bc8fbad68bedbfa0d8f36(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee7666af622d138685bf401be24b855f77364367065d0986499a21c4b86a21fe(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09fe21a3620e088f193f51c4eb4d8bed83d898eb8ddf000f7c4b3ec56387b131(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f678797b822d131c0c9439c597fbfc69b2c5828027ac3d240395c836689ba8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d4e9f25848ff4a63ed6f6a08ec197c226c6f9024dc1bc378a826fe07ba2d8f3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ce8b6f2cfa476a226137d16d19936b7650ee46a7f8517f06e3889d072bf452(
    *,
    protocol: builtins.str,
    topic_arn: builtins.str,
    delivery_policy: typing.Any = None,
    endpoint: typing.Optional[builtins.str] = None,
    filter_policy: typing.Any = None,
    filter_policy_scope: typing.Optional[builtins.str] = None,
    raw_message_delivery: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    redrive_policy: typing.Any = None,
    region: typing.Optional[builtins.str] = None,
    subscription_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e0ee1a44f398c754b0862d012b783ba509399f8773e351a1669d21d5c10fdf(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    content_based_deduplication: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    data_protection_policy: typing.Any = None,
    display_name: typing.Optional[builtins.str] = None,
    fifo_topic: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    kms_master_key_id: typing.Optional[builtins.str] = None,
    signature_version: typing.Optional[builtins.str] = None,
    subscription: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTopic.SubscriptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    topic_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3942ff430b75b849487eeaa6a8ccfef3aaecc185a02d36a64745ce0814ec9a8e(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08e53d41b4fe5c6f27be279f7503efdc21ef14dfc22fc05e0e3e76e5e80b59c8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__995cc9290d5ec332c766a36abeb1695afc60ab299f7553e3ab21c68fb9997216(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e547bf8efb76c461397e84eed7e885bd4e3e4e5262d669f014c88e1e25a991(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86605374120923641b3baba4b957cd29c90e96185e3468669caacdd77db9c33f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__036f330bdd9a94a17ad14b123e0cbdd57387ec44c73060154a13ce95fb9b9128(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb9e5f8b3cf159b99ed685dd542df363801765e8ba858c4ea1dee8d8db46790f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eed72c3e827fd991b83e1e49b8ead0d2b51c870ec4581af935877034f0aa356(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f324d34beb044d22ca87b6749ae40d4648f0569c39870b42f00ffa8c0d9d7d68(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTopic.SubscriptionProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__160e8825570304a6bb299a5a68a0f0585096f755e02fa3adb5384d78dd1875dd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04d803becc2a4d16646a2d546552c6f13e16d72fef9fdf7fc584605ce8545f0c(
    *,
    endpoint: builtins.str,
    protocol: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a0ac65dd92cdd283e93fece57a00ea33ebfabf45144dfa8c11d5c30bed2b325(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    policy_document: typing.Any,
    topics: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9423b268c7453eb12a77fbf95fc7a6a20c1e9ecac20fac2057cf8ef1928d7cd(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36e1cac98754a36f072ba18a88daa4d0e3e50229a9ee563200d8dbdb70ffbd2e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731efe65a5881ad9fbec7bd6dec0412f875b999626e5a760ed488c1c0f199b09(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08fc632ba09bfbef7a007383d40997e8795445e1f32a76207b520d48ed41d8c5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1287a88f078ff3e3e197070a7223a5a150b4b155b93d6b206e7eed0228f28840(
    *,
    policy_document: typing.Any,
    topics: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f94fcf9a01a467359b11c49600b39b8c173af7e61631766b3f637d5f67e708(
    *,
    content_based_deduplication: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    data_protection_policy: typing.Any = None,
    display_name: typing.Optional[builtins.str] = None,
    fifo_topic: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    kms_master_key_id: typing.Optional[builtins.str] = None,
    signature_version: typing.Optional[builtins.str] = None,
    subscription: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTopic.SubscriptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    topic_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__698303e3e465adb336bca80b15c6382915f31dcd7f9330483223b187e45a5ace(
    subscription: ITopicSubscription,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6082c3e9ef187a26b9e4b76adf300af2cf9494cbe6b4b9b36bca55d3b03f87b8(
    statement: _PolicyStatement_296fe8a3,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e818f3052fc34a37a859e6b3a22ceb5fe1678b82c449b14856a64fefac5f19(
    identity: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58500a11474900ec94fffb5bca2b8143fc1a528368dd8011a76c6799805eb6c3(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_Duration_070aa057] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_Unit_113c79f9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__636b0eab2613ede1a35779d7da9f13be2431bb049c041f14999809c779469939(
    topic: ITopic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd7a1cbc419a57014617945296ca43be7e9d4f73f66daf91d641205bf4a58cc(
    *,
    allowlist: typing.Optional[typing.Sequence[jsii.Number]] = None,
    between: typing.Optional[typing.Union[BetweenCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    between_strict: typing.Optional[typing.Union[BetweenCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    greater_than: typing.Optional[jsii.Number] = None,
    greater_than_or_equal_to: typing.Optional[jsii.Number] = None,
    less_than: typing.Optional[jsii.Number] = None,
    less_than_or_equal_to: typing.Optional[jsii.Number] = None,
    whitelist: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cacb15fbe036a504f685b132a6de8eff551922d1b77c97a5017612fe7c68eed(
    *,
    allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
    blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    denylist: typing.Optional[typing.Sequence[builtins.str]] = None,
    match_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee16e53d8b186347a3d2d265470021e018e55d3b0dafa8d988976381b1a0a53(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    topic: ITopic,
    endpoint: builtins.str,
    protocol: SubscriptionProtocol,
    dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
    filter_policy: typing.Optional[typing.Mapping[builtins.str, SubscriptionFilter]] = None,
    raw_message_delivery: typing.Optional[builtins.bool] = None,
    region: typing.Optional[builtins.str] = None,
    subscription_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69001fc13cba78aaac4ba207974efbc6c8e48f13805525c1e39a20569794062b(
    conditions: typing.Optional[typing.Sequence[typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2cf0c048b9573e158402c3fefe24a8e7f513d7d2ff4a87adbfbc50d37c16a9c(
    *,
    endpoint: builtins.str,
    protocol: SubscriptionProtocol,
    dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
    filter_policy: typing.Optional[typing.Mapping[builtins.str, SubscriptionFilter]] = None,
    raw_message_delivery: typing.Optional[builtins.bool] = None,
    region: typing.Optional[builtins.str] = None,
    subscription_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7d5979ceaaa23260b5dacadeea711d436a2eb2b48cf211dfbb4fbcf7c29d1a(
    *,
    endpoint: builtins.str,
    protocol: SubscriptionProtocol,
    dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
    filter_policy: typing.Optional[typing.Mapping[builtins.str, SubscriptionFilter]] = None,
    raw_message_delivery: typing.Optional[builtins.bool] = None,
    region: typing.Optional[builtins.str] = None,
    subscription_role_arn: typing.Optional[builtins.str] = None,
    topic: ITopic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe3d0e5b5c0fb1009e24150d13034b22f5dd836095883ddd3dafea48b0d11bd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944ccf3ec49db8acb348d756aab713c22a9eec4f064210ebb33b89c949bcfef9(
    subscription: ITopicSubscription,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc59dc7abc843842cc85ffb3cf133e7ff7436ef52b5c616578a617a7eaf0d376(
    statement: _PolicyStatement_296fe8a3,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bbb86f19b019f04252ee6c1ad32fd447f0e0f2c8ea3b2ac47360dc1a8146613(
    _scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f63c1578e8e1f5f26cbbc7b94a7f4caf459e29f71f74b7d9f910bb767df9577(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f6226659346e1b02f9dfc6e234aa34b984be99568cdc4d8ff5823f1108d3289(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_Duration_070aa057] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_Unit_113c79f9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5f00c0c72c3b9da3b9f2bd2b0ffbebe83cd606c7c8ec1747defb3cdf64d5b3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    topics: typing.Sequence[ITopic],
    policy_document: typing.Optional[_PolicyDocument_b5de5177] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5923bc937499e5f8cb21264c40f270befd867f657a02f495c9ebd1dd85a0820a(
    *,
    topics: typing.Sequence[ITopic],
    policy_document: typing.Optional[_PolicyDocument_b5de5177] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ae7fe9bfb3615742d3be0065101c494719d933cd9707b6c378ca4b6d33cbd11(
    *,
    content_based_deduplication: typing.Optional[builtins.bool] = None,
    display_name: typing.Optional[builtins.str] = None,
    fifo: typing.Optional[builtins.bool] = None,
    master_key: typing.Optional[_IKey_36930160] = None,
    topic_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19954a293cde016ddcf70af6650421744c961fa26042d4a8cad35d7d280df3a(
    *,
    endpoint: builtins.str,
    protocol: SubscriptionProtocol,
    dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
    filter_policy: typing.Optional[typing.Mapping[builtins.str, SubscriptionFilter]] = None,
    raw_message_delivery: typing.Optional[builtins.bool] = None,
    region: typing.Optional[builtins.str] = None,
    subscription_role_arn: typing.Optional[builtins.str] = None,
    subscriber_id: builtins.str,
    subscriber_scope: typing.Optional[_Construct_e78e779f] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11f830efb1af0d3f166610e544a1d6643619a5f513cc71fd52dd48dc89a2380(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    content_based_deduplication: typing.Optional[builtins.bool] = None,
    display_name: typing.Optional[builtins.str] = None,
    fifo: typing.Optional[builtins.bool] = None,
    master_key: typing.Optional[_IKey_36930160] = None,
    topic_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5865dd46cfb333775a4f2a775766014024dcf8d5d2570d2f3b3bb0b633fc458e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    topic_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
