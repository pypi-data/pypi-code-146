'''
# `google_pubsub_subscription`

Refer to the Terraform Registory for docs: [`google_pubsub_subscription`](https://www.terraform.io/docs/providers/google/r/pubsub_subscription).
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

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class PubsubSubscription(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubSubscription.PubsubSubscription",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription google_pubsub_subscription}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        topic: builtins.str,
        ack_deadline_seconds: typing.Optional[jsii.Number] = None,
        bigquery_config: typing.Optional[typing.Union["PubsubSubscriptionBigqueryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_policy: typing.Optional[typing.Union["PubsubSubscriptionDeadLetterPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_exactly_once_delivery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_message_ordering: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expiration_policy: typing.Optional[typing.Union["PubsubSubscriptionExpirationPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        filter: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        message_retention_duration: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        push_config: typing.Optional[typing.Union["PubsubSubscriptionPushConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        retain_acked_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retry_policy: typing.Optional[typing.Union["PubsubSubscriptionRetryPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["PubsubSubscriptionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription google_pubsub_subscription} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the subscription. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#name PubsubSubscription#name}
        :param topic: A reference to a Topic resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#topic PubsubSubscription#topic}
        :param ack_deadline_seconds: This value is the maximum time after a subscriber receives a message before the subscriber should acknowledge the message. After message delivery but before the ack deadline expires and before the message is acknowledged, it is an outstanding message and will not be delivered again during that time (on a best-effort basis). For pull subscriptions, this value is used as the initial value for the ack deadline. To override this value for a given message, call subscriptions.modifyAckDeadline with the corresponding ackId if using pull. The minimum custom deadline you can specify is 10 seconds. The maximum custom deadline you can specify is 600 seconds (10 minutes). If this parameter is 0, a default value of 10 seconds is used. For push delivery, this value is also used to set the request timeout for the call to the push endpoint. If the subscriber never acknowledges the message, the Pub/Sub system will eventually redeliver the message. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#ack_deadline_seconds PubsubSubscription#ack_deadline_seconds}
        :param bigquery_config: bigquery_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#bigquery_config PubsubSubscription#bigquery_config}
        :param dead_letter_policy: dead_letter_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#dead_letter_policy PubsubSubscription#dead_letter_policy}
        :param enable_exactly_once_delivery: If 'true', Pub/Sub provides the following guarantees for the delivery of a message with a given value of messageId on this Subscriptions': - The message sent to a subscriber is guaranteed not to be resent before the message's acknowledgement deadline expires. - An acknowledged message will not be resent to a subscriber. Note that subscribers may still receive multiple copies of a message when 'enable_exactly_once_delivery' is true if the message was published multiple times by a publisher client. These copies are considered distinct by Pub/Sub and have distinct messageId values Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#enable_exactly_once_delivery PubsubSubscription#enable_exactly_once_delivery}
        :param enable_message_ordering: If 'true', messages published with the same orderingKey in PubsubMessage will be delivered to the subscribers in the order in which they are received by the Pub/Sub system. Otherwise, they may be delivered in any order. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#enable_message_ordering PubsubSubscription#enable_message_ordering}
        :param expiration_policy: expiration_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#expiration_policy PubsubSubscription#expiration_policy}
        :param filter: The subscription only delivers the messages that match the filter. Pub/Sub automatically acknowledges the messages that don't match the filter. You can filter messages by their attributes. The maximum length of a filter is 256 bytes. After creating the subscription, you can't modify the filter. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#filter PubsubSubscription#filter}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#id PubsubSubscription#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A set of key/value label pairs to assign to this Subscription. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#labels PubsubSubscription#labels}
        :param message_retention_duration: How long to retain unacknowledged messages in the subscription's backlog, from the moment a message is published. If retain_acked_messages is true, then this also configures the retention of acknowledged messages, and thus configures how far back in time a subscriptions.seek can be done. Defaults to 7 days. Cannot be more than 7 days ('"604800s"') or less than 10 minutes ('"600s"'). A duration in seconds with up to nine fractional digits, terminated by 's'. Example: '"600.5s"'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#message_retention_duration PubsubSubscription#message_retention_duration}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#project PubsubSubscription#project}.
        :param push_config: push_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#push_config PubsubSubscription#push_config}
        :param retain_acked_messages: Indicates whether to retain acknowledged messages. If 'true', then messages are not expunged from the subscription's backlog, even if they are acknowledged, until they fall out of the messageRetentionDuration window. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#retain_acked_messages PubsubSubscription#retain_acked_messages}
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#retry_policy PubsubSubscription#retry_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#timeouts PubsubSubscription#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb73e60b4f5ecae42fe012d5aa09e8d0ff3c370556a0dbbf77c811f8b64e690)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PubsubSubscriptionConfig(
            name=name,
            topic=topic,
            ack_deadline_seconds=ack_deadline_seconds,
            bigquery_config=bigquery_config,
            dead_letter_policy=dead_letter_policy,
            enable_exactly_once_delivery=enable_exactly_once_delivery,
            enable_message_ordering=enable_message_ordering,
            expiration_policy=expiration_policy,
            filter=filter,
            id=id,
            labels=labels,
            message_retention_duration=message_retention_duration,
            project=project,
            push_config=push_config,
            retain_acked_messages=retain_acked_messages,
            retry_policy=retry_policy,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putBigqueryConfig")
    def put_bigquery_config(
        self,
        *,
        table: builtins.str,
        drop_unknown_fields: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_topic_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        write_metadata: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param table: The name of the table to which to write data, of the form {projectId}:{datasetId}.{tableId}. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#table PubsubSubscription#table}
        :param drop_unknown_fields: When true and useTopicSchema is true, any fields that are a part of the topic schema that are not part of the BigQuery table schema are dropped when writing to BigQuery. Otherwise, the schemas must be kept in sync and any messages with extra fields are not written and remain in the subscription's backlog. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#drop_unknown_fields PubsubSubscription#drop_unknown_fields}
        :param use_topic_schema: When true, use the topic's schema as the columns to write to in BigQuery, if it exists. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#use_topic_schema PubsubSubscription#use_topic_schema}
        :param write_metadata: When true, write the subscription name, messageId, publishTime, attributes, and orderingKey to additional columns in the table. The subscription name, messageId, and publishTime fields are put in their own columns while all other message properties (other than data) are written to a JSON object in the attributes column. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#write_metadata PubsubSubscription#write_metadata}
        '''
        value = PubsubSubscriptionBigqueryConfig(
            table=table,
            drop_unknown_fields=drop_unknown_fields,
            use_topic_schema=use_topic_schema,
            write_metadata=write_metadata,
        )

        return typing.cast(None, jsii.invoke(self, "putBigqueryConfig", [value]))

    @jsii.member(jsii_name="putDeadLetterPolicy")
    def put_dead_letter_policy(
        self,
        *,
        dead_letter_topic: typing.Optional[builtins.str] = None,
        max_delivery_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param dead_letter_topic: The name of the topic to which dead letter messages should be published. Format is 'projects/{project}/topics/{topic}'. The Cloud Pub/Sub service account associated with the enclosing subscription's parent project (i.e., service-{project_number}@gcp-sa-pubsub.iam.gserviceaccount.com) must have permission to Publish() to this topic. The operation will fail if the topic does not exist. Users should ensure that there is a subscription attached to this topic since messages published to a topic with no subscriptions are lost. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#dead_letter_topic PubsubSubscription#dead_letter_topic}
        :param max_delivery_attempts: The maximum number of delivery attempts for any message. The value must be between 5 and 100. The number of delivery attempts is defined as 1 + (the sum of number of NACKs and number of times the acknowledgement deadline has been exceeded for the message). A NACK is any call to ModifyAckDeadline with a 0 deadline. Note that client libraries may automatically extend ack_deadlines. This field will be honored on a best effort basis. If this parameter is 0, a default value of 5 is used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#max_delivery_attempts PubsubSubscription#max_delivery_attempts}
        '''
        value = PubsubSubscriptionDeadLetterPolicy(
            dead_letter_topic=dead_letter_topic,
            max_delivery_attempts=max_delivery_attempts,
        )

        return typing.cast(None, jsii.invoke(self, "putDeadLetterPolicy", [value]))

    @jsii.member(jsii_name="putExpirationPolicy")
    def put_expiration_policy(self, *, ttl: builtins.str) -> None:
        '''
        :param ttl: Specifies the "time-to-live" duration for an associated resource. The resource expires if it is not active for a period of ttl. If ttl is not set, the associated resource never expires. A duration in seconds with up to nine fractional digits, terminated by 's'. Example - "3.5s". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#ttl PubsubSubscription#ttl}
        '''
        value = PubsubSubscriptionExpirationPolicy(ttl=ttl)

        return typing.cast(None, jsii.invoke(self, "putExpirationPolicy", [value]))

    @jsii.member(jsii_name="putPushConfig")
    def put_push_config(
        self,
        *,
        push_endpoint: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        oidc_token: typing.Optional[typing.Union["PubsubSubscriptionPushConfigOidcToken", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param push_endpoint: A URL locating the endpoint to which messages should be pushed. For example, a Webhook endpoint might use "https://example.com/push". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#push_endpoint PubsubSubscription#push_endpoint}
        :param attributes: Endpoint configuration attributes. Every endpoint has a set of API supported attributes that can be used to control different aspects of the message delivery. The currently supported attribute is x-goog-version, which you can use to change the format of the pushed message. This attribute indicates the version of the data expected by the endpoint. This controls the shape of the pushed message (i.e., its fields and metadata). The endpoint version is based on the version of the Pub/Sub API. If not present during the subscriptions.create call, it will default to the version of the API used to make such call. If not present during a subscriptions.modifyPushConfig call, its value will not be changed. subscriptions.get calls will always return a valid version, even if the subscription was created without this attribute. The possible values for this attribute are: - v1beta1: uses the push format defined in the v1beta1 Pub/Sub API. - v1 or v1beta2: uses the push format defined in the v1 Pub/Sub API. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#attributes PubsubSubscription#attributes}
        :param oidc_token: oidc_token block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#oidc_token PubsubSubscription#oidc_token}
        '''
        value = PubsubSubscriptionPushConfig(
            push_endpoint=push_endpoint, attributes=attributes, oidc_token=oidc_token
        )

        return typing.cast(None, jsii.invoke(self, "putPushConfig", [value]))

    @jsii.member(jsii_name="putRetryPolicy")
    def put_retry_policy(
        self,
        *,
        maximum_backoff: typing.Optional[builtins.str] = None,
        minimum_backoff: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param maximum_backoff: The maximum delay between consecutive deliveries of a given message. Value should be between 0 and 600 seconds. Defaults to 600 seconds. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#maximum_backoff PubsubSubscription#maximum_backoff}
        :param minimum_backoff: The minimum delay between consecutive deliveries of a given message. Value should be between 0 and 600 seconds. Defaults to 10 seconds. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#minimum_backoff PubsubSubscription#minimum_backoff}
        '''
        value = PubsubSubscriptionRetryPolicy(
            maximum_backoff=maximum_backoff, minimum_backoff=minimum_backoff
        )

        return typing.cast(None, jsii.invoke(self, "putRetryPolicy", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#create PubsubSubscription#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#delete PubsubSubscription#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#update PubsubSubscription#update}.
        '''
        value = PubsubSubscriptionTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAckDeadlineSeconds")
    def reset_ack_deadline_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAckDeadlineSeconds", []))

    @jsii.member(jsii_name="resetBigqueryConfig")
    def reset_bigquery_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigqueryConfig", []))

    @jsii.member(jsii_name="resetDeadLetterPolicy")
    def reset_dead_letter_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeadLetterPolicy", []))

    @jsii.member(jsii_name="resetEnableExactlyOnceDelivery")
    def reset_enable_exactly_once_delivery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableExactlyOnceDelivery", []))

    @jsii.member(jsii_name="resetEnableMessageOrdering")
    def reset_enable_message_ordering(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableMessageOrdering", []))

    @jsii.member(jsii_name="resetExpirationPolicy")
    def reset_expiration_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationPolicy", []))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMessageRetentionDuration")
    def reset_message_retention_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageRetentionDuration", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPushConfig")
    def reset_push_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPushConfig", []))

    @jsii.member(jsii_name="resetRetainAckedMessages")
    def reset_retain_acked_messages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetainAckedMessages", []))

    @jsii.member(jsii_name="resetRetryPolicy")
    def reset_retry_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryPolicy", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryConfig")
    def bigquery_config(self) -> "PubsubSubscriptionBigqueryConfigOutputReference":
        return typing.cast("PubsubSubscriptionBigqueryConfigOutputReference", jsii.get(self, "bigqueryConfig"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterPolicy")
    def dead_letter_policy(self) -> "PubsubSubscriptionDeadLetterPolicyOutputReference":
        return typing.cast("PubsubSubscriptionDeadLetterPolicyOutputReference", jsii.get(self, "deadLetterPolicy"))

    @builtins.property
    @jsii.member(jsii_name="expirationPolicy")
    def expiration_policy(self) -> "PubsubSubscriptionExpirationPolicyOutputReference":
        return typing.cast("PubsubSubscriptionExpirationPolicyOutputReference", jsii.get(self, "expirationPolicy"))

    @builtins.property
    @jsii.member(jsii_name="pushConfig")
    def push_config(self) -> "PubsubSubscriptionPushConfigOutputReference":
        return typing.cast("PubsubSubscriptionPushConfigOutputReference", jsii.get(self, "pushConfig"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicy")
    def retry_policy(self) -> "PubsubSubscriptionRetryPolicyOutputReference":
        return typing.cast("PubsubSubscriptionRetryPolicyOutputReference", jsii.get(self, "retryPolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "PubsubSubscriptionTimeoutsOutputReference":
        return typing.cast("PubsubSubscriptionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="ackDeadlineSecondsInput")
    def ack_deadline_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ackDeadlineSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryConfigInput")
    def bigquery_config_input(
        self,
    ) -> typing.Optional["PubsubSubscriptionBigqueryConfig"]:
        return typing.cast(typing.Optional["PubsubSubscriptionBigqueryConfig"], jsii.get(self, "bigqueryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterPolicyInput")
    def dead_letter_policy_input(
        self,
    ) -> typing.Optional["PubsubSubscriptionDeadLetterPolicy"]:
        return typing.cast(typing.Optional["PubsubSubscriptionDeadLetterPolicy"], jsii.get(self, "deadLetterPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="enableExactlyOnceDeliveryInput")
    def enable_exactly_once_delivery_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableExactlyOnceDeliveryInput"))

    @builtins.property
    @jsii.member(jsii_name="enableMessageOrderingInput")
    def enable_message_ordering_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableMessageOrderingInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationPolicyInput")
    def expiration_policy_input(
        self,
    ) -> typing.Optional["PubsubSubscriptionExpirationPolicy"]:
        return typing.cast(typing.Optional["PubsubSubscriptionExpirationPolicy"], jsii.get(self, "expirationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="messageRetentionDurationInput")
    def message_retention_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageRetentionDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="pushConfigInput")
    def push_config_input(self) -> typing.Optional["PubsubSubscriptionPushConfig"]:
        return typing.cast(typing.Optional["PubsubSubscriptionPushConfig"], jsii.get(self, "pushConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="retainAckedMessagesInput")
    def retain_acked_messages_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "retainAckedMessagesInput"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicyInput")
    def retry_policy_input(self) -> typing.Optional["PubsubSubscriptionRetryPolicy"]:
        return typing.cast(typing.Optional["PubsubSubscriptionRetryPolicy"], jsii.get(self, "retryPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["PubsubSubscriptionTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["PubsubSubscriptionTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="ackDeadlineSeconds")
    def ack_deadline_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ackDeadlineSeconds"))

    @ack_deadline_seconds.setter
    def ack_deadline_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f79fada8cfc7d86128e0bbc231aaa39694a32752760cae7645cb41b953ac4920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ackDeadlineSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="enableExactlyOnceDelivery")
    def enable_exactly_once_delivery(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableExactlyOnceDelivery"))

    @enable_exactly_once_delivery.setter
    def enable_exactly_once_delivery(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fdea49cf58d01e7bce29c7b7432ce554c77a7b17402232df2332448c48e2321)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableExactlyOnceDelivery", value)

    @builtins.property
    @jsii.member(jsii_name="enableMessageOrdering")
    def enable_message_ordering(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableMessageOrdering"))

    @enable_message_ordering.setter
    def enable_message_ordering(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6debdc10872e0939fed92282d675a309cce283acd8ce30130a7c8d169a7c2890)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableMessageOrdering", value)

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b74a163985e79c73248b97db56b457f317b5fdfa2e74be38dad5187070ed443)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96e1d9fca5b351219c5e4fce95191d6e44003159444e19f40b81604eb3386a99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c156d186c1380871f13cf64295a3237c08b80c56e3a95802d6bbde4292d012)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="messageRetentionDuration")
    def message_retention_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageRetentionDuration"))

    @message_retention_duration.setter
    def message_retention_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ab63036a82c125d972166528926debd1e510c47dd98cac21257c0f92d9e6514)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageRetentionDuration", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25568ff0be28bd135bb8b84769ad12be989362053053e23deeace99c0134ce06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d69c6fe4a2ff4e7f03badc56a6f1837a169b7e91c8ab1107ab8a71c32fa94789)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="retainAckedMessages")
    def retain_acked_messages(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "retainAckedMessages"))

    @retain_acked_messages.setter
    def retain_acked_messages(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eeabf8f1affa5925469c9e25a3e979c1e0a4e583470023c0a2346a5a32fd29c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retainAckedMessages", value)

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e48d34795bac76a34a7bb7e40be3e23cb1d8a593988b96b4dd3bff24e55b30ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubSubscription.PubsubSubscriptionBigqueryConfig",
    jsii_struct_bases=[],
    name_mapping={
        "table": "table",
        "drop_unknown_fields": "dropUnknownFields",
        "use_topic_schema": "useTopicSchema",
        "write_metadata": "writeMetadata",
    },
)
class PubsubSubscriptionBigqueryConfig:
    def __init__(
        self,
        *,
        table: builtins.str,
        drop_unknown_fields: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_topic_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        write_metadata: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param table: The name of the table to which to write data, of the form {projectId}:{datasetId}.{tableId}. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#table PubsubSubscription#table}
        :param drop_unknown_fields: When true and useTopicSchema is true, any fields that are a part of the topic schema that are not part of the BigQuery table schema are dropped when writing to BigQuery. Otherwise, the schemas must be kept in sync and any messages with extra fields are not written and remain in the subscription's backlog. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#drop_unknown_fields PubsubSubscription#drop_unknown_fields}
        :param use_topic_schema: When true, use the topic's schema as the columns to write to in BigQuery, if it exists. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#use_topic_schema PubsubSubscription#use_topic_schema}
        :param write_metadata: When true, write the subscription name, messageId, publishTime, attributes, and orderingKey to additional columns in the table. The subscription name, messageId, and publishTime fields are put in their own columns while all other message properties (other than data) are written to a JSON object in the attributes column. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#write_metadata PubsubSubscription#write_metadata}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f39c9a5725f46e7b56540966cfec18f1b3a2d4ae94c3107914273062c2523d)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
            check_type(argname="argument drop_unknown_fields", value=drop_unknown_fields, expected_type=type_hints["drop_unknown_fields"])
            check_type(argname="argument use_topic_schema", value=use_topic_schema, expected_type=type_hints["use_topic_schema"])
            check_type(argname="argument write_metadata", value=write_metadata, expected_type=type_hints["write_metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table": table,
        }
        if drop_unknown_fields is not None:
            self._values["drop_unknown_fields"] = drop_unknown_fields
        if use_topic_schema is not None:
            self._values["use_topic_schema"] = use_topic_schema
        if write_metadata is not None:
            self._values["write_metadata"] = write_metadata

    @builtins.property
    def table(self) -> builtins.str:
        '''The name of the table to which to write data, of the form {projectId}:{datasetId}.{tableId}.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#table PubsubSubscription#table}
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def drop_unknown_fields(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true and useTopicSchema is true, any fields that are a part of the topic schema that are not part of the BigQuery table schema are dropped when writing to BigQuery.

        Otherwise, the schemas must be kept in sync and any messages with extra fields are not written and remain in the subscription's backlog.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#drop_unknown_fields PubsubSubscription#drop_unknown_fields}
        '''
        result = self._values.get("drop_unknown_fields")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_topic_schema(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, use the topic's schema as the columns to write to in BigQuery, if it exists.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#use_topic_schema PubsubSubscription#use_topic_schema}
        '''
        result = self._values.get("use_topic_schema")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def write_metadata(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, write the subscription name, messageId, publishTime, attributes, and orderingKey to additional columns in the table.

        The subscription name, messageId, and publishTime fields are put in their own columns while all other message properties (other than data) are written to a JSON object in the attributes column.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#write_metadata PubsubSubscription#write_metadata}
        '''
        result = self._values.get("write_metadata")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubSubscriptionBigqueryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubSubscriptionBigqueryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubSubscription.PubsubSubscriptionBigqueryConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b839e50cc188b0a6e4811e375019d43ded5a397d8b32eda51f7de41abf65334)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDropUnknownFields")
    def reset_drop_unknown_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDropUnknownFields", []))

    @jsii.member(jsii_name="resetUseTopicSchema")
    def reset_use_topic_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseTopicSchema", []))

    @jsii.member(jsii_name="resetWriteMetadata")
    def reset_write_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriteMetadata", []))

    @builtins.property
    @jsii.member(jsii_name="dropUnknownFieldsInput")
    def drop_unknown_fields_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dropUnknownFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="tableInput")
    def table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableInput"))

    @builtins.property
    @jsii.member(jsii_name="useTopicSchemaInput")
    def use_topic_schema_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useTopicSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="writeMetadataInput")
    def write_metadata_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "writeMetadataInput"))

    @builtins.property
    @jsii.member(jsii_name="dropUnknownFields")
    def drop_unknown_fields(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dropUnknownFields"))

    @drop_unknown_fields.setter
    def drop_unknown_fields(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62c9e3c585a0d6e29ce5696fd058432e511bc901943fcf0962254f751657fc6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dropUnknownFields", value)

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "table"))

    @table.setter
    def table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ae55f2870924477c045f9a0c2c12e7ec98a6a6c69c8f4e31df43500c21f4f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "table", value)

    @builtins.property
    @jsii.member(jsii_name="useTopicSchema")
    def use_topic_schema(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useTopicSchema"))

    @use_topic_schema.setter
    def use_topic_schema(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77c3d33f7b381368d0cc788e1e4634978820d4fb9f92aa09113886cbd9281bdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useTopicSchema", value)

    @builtins.property
    @jsii.member(jsii_name="writeMetadata")
    def write_metadata(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "writeMetadata"))

    @write_metadata.setter
    def write_metadata(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__785b5c2497d10b34d7edc5cffd546cc9d02180c11508487c51e34de4ce68032f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeMetadata", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PubsubSubscriptionBigqueryConfig]:
        return typing.cast(typing.Optional[PubsubSubscriptionBigqueryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubSubscriptionBigqueryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f855018a191cdb107f6b393b4c97a7686d5bcae41fd1fb269504016526ea6c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubSubscription.PubsubSubscriptionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "topic": "topic",
        "ack_deadline_seconds": "ackDeadlineSeconds",
        "bigquery_config": "bigqueryConfig",
        "dead_letter_policy": "deadLetterPolicy",
        "enable_exactly_once_delivery": "enableExactlyOnceDelivery",
        "enable_message_ordering": "enableMessageOrdering",
        "expiration_policy": "expirationPolicy",
        "filter": "filter",
        "id": "id",
        "labels": "labels",
        "message_retention_duration": "messageRetentionDuration",
        "project": "project",
        "push_config": "pushConfig",
        "retain_acked_messages": "retainAckedMessages",
        "retry_policy": "retryPolicy",
        "timeouts": "timeouts",
    },
)
class PubsubSubscriptionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        name: builtins.str,
        topic: builtins.str,
        ack_deadline_seconds: typing.Optional[jsii.Number] = None,
        bigquery_config: typing.Optional[typing.Union[PubsubSubscriptionBigqueryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_policy: typing.Optional[typing.Union["PubsubSubscriptionDeadLetterPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_exactly_once_delivery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_message_ordering: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expiration_policy: typing.Optional[typing.Union["PubsubSubscriptionExpirationPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        filter: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        message_retention_duration: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        push_config: typing.Optional[typing.Union["PubsubSubscriptionPushConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        retain_acked_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retry_policy: typing.Optional[typing.Union["PubsubSubscriptionRetryPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["PubsubSubscriptionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the subscription. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#name PubsubSubscription#name}
        :param topic: A reference to a Topic resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#topic PubsubSubscription#topic}
        :param ack_deadline_seconds: This value is the maximum time after a subscriber receives a message before the subscriber should acknowledge the message. After message delivery but before the ack deadline expires and before the message is acknowledged, it is an outstanding message and will not be delivered again during that time (on a best-effort basis). For pull subscriptions, this value is used as the initial value for the ack deadline. To override this value for a given message, call subscriptions.modifyAckDeadline with the corresponding ackId if using pull. The minimum custom deadline you can specify is 10 seconds. The maximum custom deadline you can specify is 600 seconds (10 minutes). If this parameter is 0, a default value of 10 seconds is used. For push delivery, this value is also used to set the request timeout for the call to the push endpoint. If the subscriber never acknowledges the message, the Pub/Sub system will eventually redeliver the message. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#ack_deadline_seconds PubsubSubscription#ack_deadline_seconds}
        :param bigquery_config: bigquery_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#bigquery_config PubsubSubscription#bigquery_config}
        :param dead_letter_policy: dead_letter_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#dead_letter_policy PubsubSubscription#dead_letter_policy}
        :param enable_exactly_once_delivery: If 'true', Pub/Sub provides the following guarantees for the delivery of a message with a given value of messageId on this Subscriptions': - The message sent to a subscriber is guaranteed not to be resent before the message's acknowledgement deadline expires. - An acknowledged message will not be resent to a subscriber. Note that subscribers may still receive multiple copies of a message when 'enable_exactly_once_delivery' is true if the message was published multiple times by a publisher client. These copies are considered distinct by Pub/Sub and have distinct messageId values Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#enable_exactly_once_delivery PubsubSubscription#enable_exactly_once_delivery}
        :param enable_message_ordering: If 'true', messages published with the same orderingKey in PubsubMessage will be delivered to the subscribers in the order in which they are received by the Pub/Sub system. Otherwise, they may be delivered in any order. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#enable_message_ordering PubsubSubscription#enable_message_ordering}
        :param expiration_policy: expiration_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#expiration_policy PubsubSubscription#expiration_policy}
        :param filter: The subscription only delivers the messages that match the filter. Pub/Sub automatically acknowledges the messages that don't match the filter. You can filter messages by their attributes. The maximum length of a filter is 256 bytes. After creating the subscription, you can't modify the filter. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#filter PubsubSubscription#filter}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#id PubsubSubscription#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A set of key/value label pairs to assign to this Subscription. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#labels PubsubSubscription#labels}
        :param message_retention_duration: How long to retain unacknowledged messages in the subscription's backlog, from the moment a message is published. If retain_acked_messages is true, then this also configures the retention of acknowledged messages, and thus configures how far back in time a subscriptions.seek can be done. Defaults to 7 days. Cannot be more than 7 days ('"604800s"') or less than 10 minutes ('"600s"'). A duration in seconds with up to nine fractional digits, terminated by 's'. Example: '"600.5s"'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#message_retention_duration PubsubSubscription#message_retention_duration}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#project PubsubSubscription#project}.
        :param push_config: push_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#push_config PubsubSubscription#push_config}
        :param retain_acked_messages: Indicates whether to retain acknowledged messages. If 'true', then messages are not expunged from the subscription's backlog, even if they are acknowledged, until they fall out of the messageRetentionDuration window. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#retain_acked_messages PubsubSubscription#retain_acked_messages}
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#retry_policy PubsubSubscription#retry_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#timeouts PubsubSubscription#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bigquery_config, dict):
            bigquery_config = PubsubSubscriptionBigqueryConfig(**bigquery_config)
        if isinstance(dead_letter_policy, dict):
            dead_letter_policy = PubsubSubscriptionDeadLetterPolicy(**dead_letter_policy)
        if isinstance(expiration_policy, dict):
            expiration_policy = PubsubSubscriptionExpirationPolicy(**expiration_policy)
        if isinstance(push_config, dict):
            push_config = PubsubSubscriptionPushConfig(**push_config)
        if isinstance(retry_policy, dict):
            retry_policy = PubsubSubscriptionRetryPolicy(**retry_policy)
        if isinstance(timeouts, dict):
            timeouts = PubsubSubscriptionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de1798ee3c0d5ed896be2263ac8658e32c83c1f308d43d5a1a0b3f1a4cf01972)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument ack_deadline_seconds", value=ack_deadline_seconds, expected_type=type_hints["ack_deadline_seconds"])
            check_type(argname="argument bigquery_config", value=bigquery_config, expected_type=type_hints["bigquery_config"])
            check_type(argname="argument dead_letter_policy", value=dead_letter_policy, expected_type=type_hints["dead_letter_policy"])
            check_type(argname="argument enable_exactly_once_delivery", value=enable_exactly_once_delivery, expected_type=type_hints["enable_exactly_once_delivery"])
            check_type(argname="argument enable_message_ordering", value=enable_message_ordering, expected_type=type_hints["enable_message_ordering"])
            check_type(argname="argument expiration_policy", value=expiration_policy, expected_type=type_hints["expiration_policy"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument message_retention_duration", value=message_retention_duration, expected_type=type_hints["message_retention_duration"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument push_config", value=push_config, expected_type=type_hints["push_config"])
            check_type(argname="argument retain_acked_messages", value=retain_acked_messages, expected_type=type_hints["retain_acked_messages"])
            check_type(argname="argument retry_policy", value=retry_policy, expected_type=type_hints["retry_policy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "topic": topic,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if ack_deadline_seconds is not None:
            self._values["ack_deadline_seconds"] = ack_deadline_seconds
        if bigquery_config is not None:
            self._values["bigquery_config"] = bigquery_config
        if dead_letter_policy is not None:
            self._values["dead_letter_policy"] = dead_letter_policy
        if enable_exactly_once_delivery is not None:
            self._values["enable_exactly_once_delivery"] = enable_exactly_once_delivery
        if enable_message_ordering is not None:
            self._values["enable_message_ordering"] = enable_message_ordering
        if expiration_policy is not None:
            self._values["expiration_policy"] = expiration_policy
        if filter is not None:
            self._values["filter"] = filter
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if message_retention_duration is not None:
            self._values["message_retention_duration"] = message_retention_duration
        if project is not None:
            self._values["project"] = project
        if push_config is not None:
            self._values["push_config"] = push_config
        if retain_acked_messages is not None:
            self._values["retain_acked_messages"] = retain_acked_messages
        if retry_policy is not None:
            self._values["retry_policy"] = retry_policy
        if timeouts is not None:
            self._values["timeouts"] = timeouts

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the subscription.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#name PubsubSubscription#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''A reference to a Topic resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#topic PubsubSubscription#topic}
        '''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ack_deadline_seconds(self) -> typing.Optional[jsii.Number]:
        '''This value is the maximum time after a subscriber receives a message before the subscriber should acknowledge the message.

        After message
        delivery but before the ack deadline expires and before the message is
        acknowledged, it is an outstanding message and will not be delivered
        again during that time (on a best-effort basis).

        For pull subscriptions, this value is used as the initial value for
        the ack deadline. To override this value for a given message, call
        subscriptions.modifyAckDeadline with the corresponding ackId if using
        pull. The minimum custom deadline you can specify is 10 seconds. The
        maximum custom deadline you can specify is 600 seconds (10 minutes).
        If this parameter is 0, a default value of 10 seconds is used.

        For push delivery, this value is also used to set the request timeout
        for the call to the push endpoint.

        If the subscriber never acknowledges the message, the Pub/Sub system
        will eventually redeliver the message.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#ack_deadline_seconds PubsubSubscription#ack_deadline_seconds}
        '''
        result = self._values.get("ack_deadline_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bigquery_config(self) -> typing.Optional[PubsubSubscriptionBigqueryConfig]:
        '''bigquery_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#bigquery_config PubsubSubscription#bigquery_config}
        '''
        result = self._values.get("bigquery_config")
        return typing.cast(typing.Optional[PubsubSubscriptionBigqueryConfig], result)

    @builtins.property
    def dead_letter_policy(
        self,
    ) -> typing.Optional["PubsubSubscriptionDeadLetterPolicy"]:
        '''dead_letter_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#dead_letter_policy PubsubSubscription#dead_letter_policy}
        '''
        result = self._values.get("dead_letter_policy")
        return typing.cast(typing.Optional["PubsubSubscriptionDeadLetterPolicy"], result)

    @builtins.property
    def enable_exactly_once_delivery(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If 'true', Pub/Sub provides the following guarantees for the delivery of a message with a given value of messageId on this Subscriptions':  - The message sent to a subscriber is guaranteed not to be resent before the message's acknowledgement deadline expires.

        - An acknowledged message will not be resent to a subscriber.

        Note that subscribers may still receive multiple copies of a message when 'enable_exactly_once_delivery'
        is true if the message was published multiple times by a publisher client. These copies are considered distinct by Pub/Sub and have distinct messageId values

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#enable_exactly_once_delivery PubsubSubscription#enable_exactly_once_delivery}
        '''
        result = self._values.get("enable_exactly_once_delivery")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_message_ordering(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If 'true', messages published with the same orderingKey in PubsubMessage will be delivered to the subscribers in the order in which they are received by the Pub/Sub system.

        Otherwise, they
        may be delivered in any order.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#enable_message_ordering PubsubSubscription#enable_message_ordering}
        '''
        result = self._values.get("enable_message_ordering")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expiration_policy(
        self,
    ) -> typing.Optional["PubsubSubscriptionExpirationPolicy"]:
        '''expiration_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#expiration_policy PubsubSubscription#expiration_policy}
        '''
        result = self._values.get("expiration_policy")
        return typing.cast(typing.Optional["PubsubSubscriptionExpirationPolicy"], result)

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        '''The subscription only delivers the messages that match the filter.

        Pub/Sub automatically acknowledges the messages that don't match the filter. You can filter messages
        by their attributes. The maximum length of a filter is 256 bytes. After creating the subscription,
        you can't modify the filter.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#filter PubsubSubscription#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#id PubsubSubscription#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs to assign to this Subscription.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#labels PubsubSubscription#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def message_retention_duration(self) -> typing.Optional[builtins.str]:
        '''How long to retain unacknowledged messages in the subscription's backlog, from the moment a message is published.

        If
        retain_acked_messages is true, then this also configures the retention
        of acknowledged messages, and thus configures how far back in time a
        subscriptions.seek can be done. Defaults to 7 days. Cannot be more
        than 7 days ('"604800s"') or less than 10 minutes ('"600s"').

        A duration in seconds with up to nine fractional digits, terminated
        by 's'. Example: '"600.5s"'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#message_retention_duration PubsubSubscription#message_retention_duration}
        '''
        result = self._values.get("message_retention_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#project PubsubSubscription#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def push_config(self) -> typing.Optional["PubsubSubscriptionPushConfig"]:
        '''push_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#push_config PubsubSubscription#push_config}
        '''
        result = self._values.get("push_config")
        return typing.cast(typing.Optional["PubsubSubscriptionPushConfig"], result)

    @builtins.property
    def retain_acked_messages(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether to retain acknowledged messages.

        If 'true', then
        messages are not expunged from the subscription's backlog, even if
        they are acknowledged, until they fall out of the
        messageRetentionDuration window.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#retain_acked_messages PubsubSubscription#retain_acked_messages}
        '''
        result = self._values.get("retain_acked_messages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retry_policy(self) -> typing.Optional["PubsubSubscriptionRetryPolicy"]:
        '''retry_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#retry_policy PubsubSubscription#retry_policy}
        '''
        result = self._values.get("retry_policy")
        return typing.cast(typing.Optional["PubsubSubscriptionRetryPolicy"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["PubsubSubscriptionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#timeouts PubsubSubscription#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["PubsubSubscriptionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubSubscriptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubSubscription.PubsubSubscriptionDeadLetterPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "dead_letter_topic": "deadLetterTopic",
        "max_delivery_attempts": "maxDeliveryAttempts",
    },
)
class PubsubSubscriptionDeadLetterPolicy:
    def __init__(
        self,
        *,
        dead_letter_topic: typing.Optional[builtins.str] = None,
        max_delivery_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param dead_letter_topic: The name of the topic to which dead letter messages should be published. Format is 'projects/{project}/topics/{topic}'. The Cloud Pub/Sub service account associated with the enclosing subscription's parent project (i.e., service-{project_number}@gcp-sa-pubsub.iam.gserviceaccount.com) must have permission to Publish() to this topic. The operation will fail if the topic does not exist. Users should ensure that there is a subscription attached to this topic since messages published to a topic with no subscriptions are lost. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#dead_letter_topic PubsubSubscription#dead_letter_topic}
        :param max_delivery_attempts: The maximum number of delivery attempts for any message. The value must be between 5 and 100. The number of delivery attempts is defined as 1 + (the sum of number of NACKs and number of times the acknowledgement deadline has been exceeded for the message). A NACK is any call to ModifyAckDeadline with a 0 deadline. Note that client libraries may automatically extend ack_deadlines. This field will be honored on a best effort basis. If this parameter is 0, a default value of 5 is used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#max_delivery_attempts PubsubSubscription#max_delivery_attempts}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a51901d54cc642a24d7baaef0a2740d1e8bb6752c66245c32776cc3b1a77840)
            check_type(argname="argument dead_letter_topic", value=dead_letter_topic, expected_type=type_hints["dead_letter_topic"])
            check_type(argname="argument max_delivery_attempts", value=max_delivery_attempts, expected_type=type_hints["max_delivery_attempts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dead_letter_topic is not None:
            self._values["dead_letter_topic"] = dead_letter_topic
        if max_delivery_attempts is not None:
            self._values["max_delivery_attempts"] = max_delivery_attempts

    @builtins.property
    def dead_letter_topic(self) -> typing.Optional[builtins.str]:
        '''The name of the topic to which dead letter messages should be published. Format is 'projects/{project}/topics/{topic}'.

        The Cloud Pub/Sub service account associated with the enclosing subscription's
        parent project (i.e.,
        service-{project_number}@gcp-sa-pubsub.iam.gserviceaccount.com) must have
        permission to Publish() to this topic.

        The operation will fail if the topic does not exist.
        Users should ensure that there is a subscription attached to this topic
        since messages published to a topic with no subscriptions are lost.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#dead_letter_topic PubsubSubscription#dead_letter_topic}
        '''
        result = self._values.get("dead_letter_topic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_delivery_attempts(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of delivery attempts for any message. The value must be between 5 and 100.

        The number of delivery attempts is defined as 1 + (the sum of number of
        NACKs and number of times the acknowledgement deadline has been exceeded for the message).

        A NACK is any call to ModifyAckDeadline with a 0 deadline. Note that
        client libraries may automatically extend ack_deadlines.

        This field will be honored on a best effort basis.

        If this parameter is 0, a default value of 5 is used.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#max_delivery_attempts PubsubSubscription#max_delivery_attempts}
        '''
        result = self._values.get("max_delivery_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubSubscriptionDeadLetterPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubSubscriptionDeadLetterPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubSubscription.PubsubSubscriptionDeadLetterPolicyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abfa1907f5e37879bb5d7fe36963863d38ed385634d194a938914100a9fc7880)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDeadLetterTopic")
    def reset_dead_letter_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeadLetterTopic", []))

    @jsii.member(jsii_name="resetMaxDeliveryAttempts")
    def reset_max_delivery_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxDeliveryAttempts", []))

    @builtins.property
    @jsii.member(jsii_name="deadLetterTopicInput")
    def dead_letter_topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deadLetterTopicInput"))

    @builtins.property
    @jsii.member(jsii_name="maxDeliveryAttemptsInput")
    def max_delivery_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxDeliveryAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterTopic")
    def dead_letter_topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deadLetterTopic"))

    @dead_letter_topic.setter
    def dead_letter_topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92676cecae1f8529062080b3f72a138c44f87ffa539d5d1938c110e7d677cb1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deadLetterTopic", value)

    @builtins.property
    @jsii.member(jsii_name="maxDeliveryAttempts")
    def max_delivery_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDeliveryAttempts"))

    @max_delivery_attempts.setter
    def max_delivery_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__286a3851d0b8ff59405364bafb995787ed07058daa5a11f091c0ec344e617068)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDeliveryAttempts", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PubsubSubscriptionDeadLetterPolicy]:
        return typing.cast(typing.Optional[PubsubSubscriptionDeadLetterPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubSubscriptionDeadLetterPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0936b324fa2b6e035ac1bfd91317979516ec459fb8aba9e22be0b472aba4fc84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubSubscription.PubsubSubscriptionExpirationPolicy",
    jsii_struct_bases=[],
    name_mapping={"ttl": "ttl"},
)
class PubsubSubscriptionExpirationPolicy:
    def __init__(self, *, ttl: builtins.str) -> None:
        '''
        :param ttl: Specifies the "time-to-live" duration for an associated resource. The resource expires if it is not active for a period of ttl. If ttl is not set, the associated resource never expires. A duration in seconds with up to nine fractional digits, terminated by 's'. Example - "3.5s". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#ttl PubsubSubscription#ttl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da7ffe71b5f1095a6c429727aa339882cd003a60cbbf301517112bcbabdf430)
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ttl": ttl,
        }

    @builtins.property
    def ttl(self) -> builtins.str:
        '''Specifies the "time-to-live" duration for an associated resource.

        The
        resource expires if it is not active for a period of ttl.
        If ttl is not set, the associated resource never expires.
        A duration in seconds with up to nine fractional digits, terminated by 's'.
        Example - "3.5s".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#ttl PubsubSubscription#ttl}
        '''
        result = self._values.get("ttl")
        assert result is not None, "Required property 'ttl' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubSubscriptionExpirationPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubSubscriptionExpirationPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubSubscription.PubsubSubscriptionExpirationPolicyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1277eb3fe748ae470523243cddb266910507c63308a864d7518844471fcbe151)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86435fd264bfd46f1826934df5f31ba20c9b3b13414331977c7f20bb3bdcecee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PubsubSubscriptionExpirationPolicy]:
        return typing.cast(typing.Optional[PubsubSubscriptionExpirationPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubSubscriptionExpirationPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a029f4f3f6f07add08d3e5b9d28385ccedbf696f59d03ca8a0f43acbb690ad04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubSubscription.PubsubSubscriptionPushConfig",
    jsii_struct_bases=[],
    name_mapping={
        "push_endpoint": "pushEndpoint",
        "attributes": "attributes",
        "oidc_token": "oidcToken",
    },
)
class PubsubSubscriptionPushConfig:
    def __init__(
        self,
        *,
        push_endpoint: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        oidc_token: typing.Optional[typing.Union["PubsubSubscriptionPushConfigOidcToken", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param push_endpoint: A URL locating the endpoint to which messages should be pushed. For example, a Webhook endpoint might use "https://example.com/push". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#push_endpoint PubsubSubscription#push_endpoint}
        :param attributes: Endpoint configuration attributes. Every endpoint has a set of API supported attributes that can be used to control different aspects of the message delivery. The currently supported attribute is x-goog-version, which you can use to change the format of the pushed message. This attribute indicates the version of the data expected by the endpoint. This controls the shape of the pushed message (i.e., its fields and metadata). The endpoint version is based on the version of the Pub/Sub API. If not present during the subscriptions.create call, it will default to the version of the API used to make such call. If not present during a subscriptions.modifyPushConfig call, its value will not be changed. subscriptions.get calls will always return a valid version, even if the subscription was created without this attribute. The possible values for this attribute are: - v1beta1: uses the push format defined in the v1beta1 Pub/Sub API. - v1 or v1beta2: uses the push format defined in the v1 Pub/Sub API. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#attributes PubsubSubscription#attributes}
        :param oidc_token: oidc_token block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#oidc_token PubsubSubscription#oidc_token}
        '''
        if isinstance(oidc_token, dict):
            oidc_token = PubsubSubscriptionPushConfigOidcToken(**oidc_token)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__899956e81b839ae768b7e3c847ce251298453f5b615c8933e6ee2726b19a5203)
            check_type(argname="argument push_endpoint", value=push_endpoint, expected_type=type_hints["push_endpoint"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument oidc_token", value=oidc_token, expected_type=type_hints["oidc_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "push_endpoint": push_endpoint,
        }
        if attributes is not None:
            self._values["attributes"] = attributes
        if oidc_token is not None:
            self._values["oidc_token"] = oidc_token

    @builtins.property
    def push_endpoint(self) -> builtins.str:
        '''A URL locating the endpoint to which messages should be pushed. For example, a Webhook endpoint might use "https://example.com/push".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#push_endpoint PubsubSubscription#push_endpoint}
        '''
        result = self._values.get("push_endpoint")
        assert result is not None, "Required property 'push_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Endpoint configuration attributes.

        Every endpoint has a set of API supported attributes that can
        be used to control different aspects of the message delivery.

        The currently supported attribute is x-goog-version, which you
        can use to change the format of the pushed message. This
        attribute indicates the version of the data expected by
        the endpoint. This controls the shape of the pushed message
        (i.e., its fields and metadata). The endpoint version is
        based on the version of the Pub/Sub API.

        If not present during the subscriptions.create call,
        it will default to the version of the API used to make
        such call. If not present during a subscriptions.modifyPushConfig
        call, its value will not be changed. subscriptions.get
        calls will always return a valid version, even if the
        subscription was created without this attribute.

        The possible values for this attribute are:

        - v1beta1: uses the push format defined in the v1beta1 Pub/Sub API.
        - v1 or v1beta2: uses the push format defined in the v1 Pub/Sub API.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#attributes PubsubSubscription#attributes}
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def oidc_token(self) -> typing.Optional["PubsubSubscriptionPushConfigOidcToken"]:
        '''oidc_token block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#oidc_token PubsubSubscription#oidc_token}
        '''
        result = self._values.get("oidc_token")
        return typing.cast(typing.Optional["PubsubSubscriptionPushConfigOidcToken"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubSubscriptionPushConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubSubscription.PubsubSubscriptionPushConfigOidcToken",
    jsii_struct_bases=[],
    name_mapping={
        "service_account_email": "serviceAccountEmail",
        "audience": "audience",
    },
)
class PubsubSubscriptionPushConfigOidcToken:
    def __init__(
        self,
        *,
        service_account_email: builtins.str,
        audience: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account_email: Service account email to be used for generating the OIDC token. The caller (for subscriptions.create, subscriptions.patch, and subscriptions.modifyPushConfig RPCs) must have the iam.serviceAccounts.actAs permission for the service account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#service_account_email PubsubSubscription#service_account_email}
        :param audience: Audience to be used when generating OIDC token. The audience claim identifies the recipients that the JWT is intended for. The audience value is a single case-sensitive string. Having multiple values (array) for the audience field is not supported. More info about the OIDC JWT token audience here: https://tools.ietf.org/html/rfc7519#section-4.1.3 Note: if not specified, the Push endpoint URL will be used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#audience PubsubSubscription#audience}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeb03fed608fd46cfb10fedfd42b8e8352a19f5f46439aebb97e7337da02e2f0)
            check_type(argname="argument service_account_email", value=service_account_email, expected_type=type_hints["service_account_email"])
            check_type(argname="argument audience", value=audience, expected_type=type_hints["audience"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_account_email": service_account_email,
        }
        if audience is not None:
            self._values["audience"] = audience

    @builtins.property
    def service_account_email(self) -> builtins.str:
        '''Service account email to be used for generating the OIDC token.

        The caller (for subscriptions.create, subscriptions.patch, and
        subscriptions.modifyPushConfig RPCs) must have the
        iam.serviceAccounts.actAs permission for the service account.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#service_account_email PubsubSubscription#service_account_email}
        '''
        result = self._values.get("service_account_email")
        assert result is not None, "Required property 'service_account_email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def audience(self) -> typing.Optional[builtins.str]:
        '''Audience to be used when generating OIDC token.

        The audience claim
        identifies the recipients that the JWT is intended for. The audience
        value is a single case-sensitive string. Having multiple values (array)
        for the audience field is not supported. More info about the OIDC JWT
        token audience here: https://tools.ietf.org/html/rfc7519#section-4.1.3
        Note: if not specified, the Push endpoint URL will be used.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#audience PubsubSubscription#audience}
        '''
        result = self._values.get("audience")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubSubscriptionPushConfigOidcToken(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubSubscriptionPushConfigOidcTokenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubSubscription.PubsubSubscriptionPushConfigOidcTokenOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4ab07a06fe312a72018ac1c8ae77733f3769865bbf8eea2990383b232b94f1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAudience")
    def reset_audience(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudience", []))

    @builtins.property
    @jsii.member(jsii_name="audienceInput")
    def audience_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audienceInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmailInput")
    def service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="audience")
    def audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audience"))

    @audience.setter
    def audience(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bfa8b8f409585281b97f86f402c3b90259162f7d51662ac58d0befa5b4ca1af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audience", value)

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e567aa3094670391240eef893a4e1fc4ddb29b4dcbbf57673ea53813907fcdc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PubsubSubscriptionPushConfigOidcToken]:
        return typing.cast(typing.Optional[PubsubSubscriptionPushConfigOidcToken], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubSubscriptionPushConfigOidcToken],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2abd54add37b826a5f4e2b4f403e01148691f07f09d674e93d7a315f8a0e2f22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class PubsubSubscriptionPushConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubSubscription.PubsubSubscriptionPushConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a393199850ab7be9a8b7639cc78c7aa191d17457a341ffceb20ed442a458c911)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOidcToken")
    def put_oidc_token(
        self,
        *,
        service_account_email: builtins.str,
        audience: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account_email: Service account email to be used for generating the OIDC token. The caller (for subscriptions.create, subscriptions.patch, and subscriptions.modifyPushConfig RPCs) must have the iam.serviceAccounts.actAs permission for the service account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#service_account_email PubsubSubscription#service_account_email}
        :param audience: Audience to be used when generating OIDC token. The audience claim identifies the recipients that the JWT is intended for. The audience value is a single case-sensitive string. Having multiple values (array) for the audience field is not supported. More info about the OIDC JWT token audience here: https://tools.ietf.org/html/rfc7519#section-4.1.3 Note: if not specified, the Push endpoint URL will be used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#audience PubsubSubscription#audience}
        '''
        value = PubsubSubscriptionPushConfigOidcToken(
            service_account_email=service_account_email, audience=audience
        )

        return typing.cast(None, jsii.invoke(self, "putOidcToken", [value]))

    @jsii.member(jsii_name="resetAttributes")
    def reset_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributes", []))

    @jsii.member(jsii_name="resetOidcToken")
    def reset_oidc_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOidcToken", []))

    @builtins.property
    @jsii.member(jsii_name="oidcToken")
    def oidc_token(self) -> PubsubSubscriptionPushConfigOidcTokenOutputReference:
        return typing.cast(PubsubSubscriptionPushConfigOidcTokenOutputReference, jsii.get(self, "oidcToken"))

    @builtins.property
    @jsii.member(jsii_name="attributesInput")
    def attributes_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "attributesInput"))

    @builtins.property
    @jsii.member(jsii_name="oidcTokenInput")
    def oidc_token_input(
        self,
    ) -> typing.Optional[PubsubSubscriptionPushConfigOidcToken]:
        return typing.cast(typing.Optional[PubsubSubscriptionPushConfigOidcToken], jsii.get(self, "oidcTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="pushEndpointInput")
    def push_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pushEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "attributes"))

    @attributes.setter
    def attributes(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0314890d9de1cc06f1c52f92b163bd696511a7c20a5fb1c1c74a2169a925a798)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributes", value)

    @builtins.property
    @jsii.member(jsii_name="pushEndpoint")
    def push_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pushEndpoint"))

    @push_endpoint.setter
    def push_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b713df0df09a35f4719e902a0fd317228d3c36248b8c532ad781cb97b55c630d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pushEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PubsubSubscriptionPushConfig]:
        return typing.cast(typing.Optional[PubsubSubscriptionPushConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubSubscriptionPushConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab58650e2881c3091f3c9e2f363b8b089615b84a48eaff9bcbae612c91e406a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubSubscription.PubsubSubscriptionRetryPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "maximum_backoff": "maximumBackoff",
        "minimum_backoff": "minimumBackoff",
    },
)
class PubsubSubscriptionRetryPolicy:
    def __init__(
        self,
        *,
        maximum_backoff: typing.Optional[builtins.str] = None,
        minimum_backoff: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param maximum_backoff: The maximum delay between consecutive deliveries of a given message. Value should be between 0 and 600 seconds. Defaults to 600 seconds. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#maximum_backoff PubsubSubscription#maximum_backoff}
        :param minimum_backoff: The minimum delay between consecutive deliveries of a given message. Value should be between 0 and 600 seconds. Defaults to 10 seconds. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#minimum_backoff PubsubSubscription#minimum_backoff}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63b62b07d538875d10584d8870759daba4e4a4d1f311a702bdbbf720e1f9226c)
            check_type(argname="argument maximum_backoff", value=maximum_backoff, expected_type=type_hints["maximum_backoff"])
            check_type(argname="argument minimum_backoff", value=minimum_backoff, expected_type=type_hints["minimum_backoff"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if maximum_backoff is not None:
            self._values["maximum_backoff"] = maximum_backoff
        if minimum_backoff is not None:
            self._values["minimum_backoff"] = minimum_backoff

    @builtins.property
    def maximum_backoff(self) -> typing.Optional[builtins.str]:
        '''The maximum delay between consecutive deliveries of a given message.

        Value should be between 0 and 600 seconds. Defaults to 600 seconds.
        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#maximum_backoff PubsubSubscription#maximum_backoff}
        '''
        result = self._values.get("maximum_backoff")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum_backoff(self) -> typing.Optional[builtins.str]:
        '''The minimum delay between consecutive deliveries of a given message.

        Value should be between 0 and 600 seconds. Defaults to 10 seconds.
        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#minimum_backoff PubsubSubscription#minimum_backoff}
        '''
        result = self._values.get("minimum_backoff")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubSubscriptionRetryPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubSubscriptionRetryPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubSubscription.PubsubSubscriptionRetryPolicyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__993e075d6a566c3ead7c1a69ec4a3fbe104cfd69ba5ab8061b2d76558b7f2c33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaximumBackoff")
    def reset_maximum_backoff(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBackoff", []))

    @jsii.member(jsii_name="resetMinimumBackoff")
    def reset_minimum_backoff(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumBackoff", []))

    @builtins.property
    @jsii.member(jsii_name="maximumBackoffInput")
    def maximum_backoff_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maximumBackoffInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumBackoffInput")
    def minimum_backoff_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimumBackoffInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBackoff")
    def maximum_backoff(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maximumBackoff"))

    @maximum_backoff.setter
    def maximum_backoff(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__298b5928026bb8a00862187e04fb3811fa9315ad4b431fa69c5d74bde4e0f98d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBackoff", value)

    @builtins.property
    @jsii.member(jsii_name="minimumBackoff")
    def minimum_backoff(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumBackoff"))

    @minimum_backoff.setter
    def minimum_backoff(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f63f0185fc46d188d0ed692f201d719542f407abf184dcf2f293897250aeaafe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumBackoff", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PubsubSubscriptionRetryPolicy]:
        return typing.cast(typing.Optional[PubsubSubscriptionRetryPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubSubscriptionRetryPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc6ce7c32fde7e8e3a01b2dc8fb5968474ae9b61ec7a2681e7566a46db87cb36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubSubscription.PubsubSubscriptionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class PubsubSubscriptionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#create PubsubSubscription#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#delete PubsubSubscription#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#update PubsubSubscription#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9b89ec72f0a17778fb5f2dc2081f2526d432aa6fa0e0e0d5103b2804536b1dd)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#create PubsubSubscription#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#delete PubsubSubscription#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/pubsub_subscription#update PubsubSubscription#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubSubscriptionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubSubscriptionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubSubscription.PubsubSubscriptionTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68dc0d4763a7ba319499e51bb30ec74235c3edda42350a7a12d7439b723b1278)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3dafff59c0f3c6ef5e1edbd7fd15edcab7a7e61a0d9edf8643f2c21f1bed22c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee2cf68d3bf5361bceb5b1143efa7dd740f659c1f881f90311031e06a29954e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fc5dcf7ef2c4494a81f9e848e304d383abb925e89582dba66f474df1a991b0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[PubsubSubscriptionTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[PubsubSubscriptionTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[PubsubSubscriptionTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8450f76368df970928b73200cd13bd4224182d4b17d119e5bc9f2ee5925b11f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "PubsubSubscription",
    "PubsubSubscriptionBigqueryConfig",
    "PubsubSubscriptionBigqueryConfigOutputReference",
    "PubsubSubscriptionConfig",
    "PubsubSubscriptionDeadLetterPolicy",
    "PubsubSubscriptionDeadLetterPolicyOutputReference",
    "PubsubSubscriptionExpirationPolicy",
    "PubsubSubscriptionExpirationPolicyOutputReference",
    "PubsubSubscriptionPushConfig",
    "PubsubSubscriptionPushConfigOidcToken",
    "PubsubSubscriptionPushConfigOidcTokenOutputReference",
    "PubsubSubscriptionPushConfigOutputReference",
    "PubsubSubscriptionRetryPolicy",
    "PubsubSubscriptionRetryPolicyOutputReference",
    "PubsubSubscriptionTimeouts",
    "PubsubSubscriptionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0fb73e60b4f5ecae42fe012d5aa09e8d0ff3c370556a0dbbf77c811f8b64e690(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    topic: builtins.str,
    ack_deadline_seconds: typing.Optional[jsii.Number] = None,
    bigquery_config: typing.Optional[typing.Union[PubsubSubscriptionBigqueryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_policy: typing.Optional[typing.Union[PubsubSubscriptionDeadLetterPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_exactly_once_delivery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_message_ordering: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expiration_policy: typing.Optional[typing.Union[PubsubSubscriptionExpirationPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    filter: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    message_retention_duration: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    push_config: typing.Optional[typing.Union[PubsubSubscriptionPushConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    retain_acked_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retry_policy: typing.Optional[typing.Union[PubsubSubscriptionRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[PubsubSubscriptionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f79fada8cfc7d86128e0bbc231aaa39694a32752760cae7645cb41b953ac4920(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fdea49cf58d01e7bce29c7b7432ce554c77a7b17402232df2332448c48e2321(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6debdc10872e0939fed92282d675a309cce283acd8ce30130a7c8d169a7c2890(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b74a163985e79c73248b97db56b457f317b5fdfa2e74be38dad5187070ed443(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e1d9fca5b351219c5e4fce95191d6e44003159444e19f40b81604eb3386a99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c156d186c1380871f13cf64295a3237c08b80c56e3a95802d6bbde4292d012(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab63036a82c125d972166528926debd1e510c47dd98cac21257c0f92d9e6514(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25568ff0be28bd135bb8b84769ad12be989362053053e23deeace99c0134ce06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d69c6fe4a2ff4e7f03badc56a6f1837a169b7e91c8ab1107ab8a71c32fa94789(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eeabf8f1affa5925469c9e25a3e979c1e0a4e583470023c0a2346a5a32fd29c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e48d34795bac76a34a7bb7e40be3e23cb1d8a593988b96b4dd3bff24e55b30ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f39c9a5725f46e7b56540966cfec18f1b3a2d4ae94c3107914273062c2523d(
    *,
    table: builtins.str,
    drop_unknown_fields: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_topic_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    write_metadata: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b839e50cc188b0a6e4811e375019d43ded5a397d8b32eda51f7de41abf65334(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c9e3c585a0d6e29ce5696fd058432e511bc901943fcf0962254f751657fc6b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ae55f2870924477c045f9a0c2c12e7ec98a6a6c69c8f4e31df43500c21f4f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c3d33f7b381368d0cc788e1e4634978820d4fb9f92aa09113886cbd9281bdd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__785b5c2497d10b34d7edc5cffd546cc9d02180c11508487c51e34de4ce68032f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f855018a191cdb107f6b393b4c97a7686d5bcae41fd1fb269504016526ea6c1(
    value: typing.Optional[PubsubSubscriptionBigqueryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de1798ee3c0d5ed896be2263ac8658e32c83c1f308d43d5a1a0b3f1a4cf01972(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    topic: builtins.str,
    ack_deadline_seconds: typing.Optional[jsii.Number] = None,
    bigquery_config: typing.Optional[typing.Union[PubsubSubscriptionBigqueryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_policy: typing.Optional[typing.Union[PubsubSubscriptionDeadLetterPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_exactly_once_delivery: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_message_ordering: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expiration_policy: typing.Optional[typing.Union[PubsubSubscriptionExpirationPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    filter: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    message_retention_duration: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    push_config: typing.Optional[typing.Union[PubsubSubscriptionPushConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    retain_acked_messages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retry_policy: typing.Optional[typing.Union[PubsubSubscriptionRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[PubsubSubscriptionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a51901d54cc642a24d7baaef0a2740d1e8bb6752c66245c32776cc3b1a77840(
    *,
    dead_letter_topic: typing.Optional[builtins.str] = None,
    max_delivery_attempts: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abfa1907f5e37879bb5d7fe36963863d38ed385634d194a938914100a9fc7880(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92676cecae1f8529062080b3f72a138c44f87ffa539d5d1938c110e7d677cb1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286a3851d0b8ff59405364bafb995787ed07058daa5a11f091c0ec344e617068(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0936b324fa2b6e035ac1bfd91317979516ec459fb8aba9e22be0b472aba4fc84(
    value: typing.Optional[PubsubSubscriptionDeadLetterPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da7ffe71b5f1095a6c429727aa339882cd003a60cbbf301517112bcbabdf430(
    *,
    ttl: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1277eb3fe748ae470523243cddb266910507c63308a864d7518844471fcbe151(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86435fd264bfd46f1826934df5f31ba20c9b3b13414331977c7f20bb3bdcecee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a029f4f3f6f07add08d3e5b9d28385ccedbf696f59d03ca8a0f43acbb690ad04(
    value: typing.Optional[PubsubSubscriptionExpirationPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__899956e81b839ae768b7e3c847ce251298453f5b615c8933e6ee2726b19a5203(
    *,
    push_endpoint: builtins.str,
    attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    oidc_token: typing.Optional[typing.Union[PubsubSubscriptionPushConfigOidcToken, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb03fed608fd46cfb10fedfd42b8e8352a19f5f46439aebb97e7337da02e2f0(
    *,
    service_account_email: builtins.str,
    audience: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ab07a06fe312a72018ac1c8ae77733f3769865bbf8eea2990383b232b94f1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bfa8b8f409585281b97f86f402c3b90259162f7d51662ac58d0befa5b4ca1af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e567aa3094670391240eef893a4e1fc4ddb29b4dcbbf57673ea53813907fcdc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2abd54add37b826a5f4e2b4f403e01148691f07f09d674e93d7a315f8a0e2f22(
    value: typing.Optional[PubsubSubscriptionPushConfigOidcToken],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a393199850ab7be9a8b7639cc78c7aa191d17457a341ffceb20ed442a458c911(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0314890d9de1cc06f1c52f92b163bd696511a7c20a5fb1c1c74a2169a925a798(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b713df0df09a35f4719e902a0fd317228d3c36248b8c532ad781cb97b55c630d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab58650e2881c3091f3c9e2f363b8b089615b84a48eaff9bcbae612c91e406a(
    value: typing.Optional[PubsubSubscriptionPushConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63b62b07d538875d10584d8870759daba4e4a4d1f311a702bdbbf720e1f9226c(
    *,
    maximum_backoff: typing.Optional[builtins.str] = None,
    minimum_backoff: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__993e075d6a566c3ead7c1a69ec4a3fbe104cfd69ba5ab8061b2d76558b7f2c33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__298b5928026bb8a00862187e04fb3811fa9315ad4b431fa69c5d74bde4e0f98d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f63f0185fc46d188d0ed692f201d719542f407abf184dcf2f293897250aeaafe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc6ce7c32fde7e8e3a01b2dc8fb5968474ae9b61ec7a2681e7566a46db87cb36(
    value: typing.Optional[PubsubSubscriptionRetryPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b89ec72f0a17778fb5f2dc2081f2526d432aa6fa0e0e0d5103b2804536b1dd(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68dc0d4763a7ba319499e51bb30ec74235c3edda42350a7a12d7439b723b1278(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3dafff59c0f3c6ef5e1edbd7fd15edcab7a7e61a0d9edf8643f2c21f1bed22c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee2cf68d3bf5361bceb5b1143efa7dd740f659c1f881f90311031e06a29954e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc5dcf7ef2c4494a81f9e848e304d383abb925e89582dba66f474df1a991b0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8450f76368df970928b73200cd13bd4224182d4b17d119e5bc9f2ee5925b11f6(
    value: typing.Optional[typing.Union[PubsubSubscriptionTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
