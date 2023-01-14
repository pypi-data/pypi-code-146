'''
# `aws_lambda_event_source_mapping`

Refer to the Terraform Registory for docs: [`aws_lambda_event_source_mapping`](https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping).
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


class LambdaEventSourceMapping(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMapping",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping aws_lambda_event_source_mapping}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        function_name: builtins.str,
        amazon_managed_kafka_event_source_config: typing.Optional[typing.Union["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_function_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        destination_config: typing.Optional[typing.Union["LambdaEventSourceMappingDestinationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        event_source_arn: typing.Optional[builtins.str] = None,
        filter_criteria: typing.Optional[typing.Union["LambdaEventSourceMappingFilterCriteria", typing.Dict[builtins.str, typing.Any]]] = None,
        function_response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        queues: typing.Optional[typing.Sequence[builtins.str]] = None,
        self_managed_event_source: typing.Optional[typing.Union["LambdaEventSourceMappingSelfManagedEventSource", typing.Dict[builtins.str, typing.Any]]] = None,
        self_managed_kafka_event_source_config: typing.Optional[typing.Union["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        source_access_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingSourceAccessConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        starting_position: typing.Optional[builtins.str] = None,
        starting_position_timestamp: typing.Optional[builtins.str] = None,
        topics: typing.Optional[typing.Sequence[builtins.str]] = None,
        tumbling_window_in_seconds: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping aws_lambda_event_source_mapping} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param function_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#function_name LambdaEventSourceMapping#function_name}.
        :param amazon_managed_kafka_event_source_config: amazon_managed_kafka_event_source_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#amazon_managed_kafka_event_source_config LambdaEventSourceMapping#amazon_managed_kafka_event_source_config}
        :param batch_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#batch_size LambdaEventSourceMapping#batch_size}.
        :param bisect_batch_on_function_error: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#bisect_batch_on_function_error LambdaEventSourceMapping#bisect_batch_on_function_error}.
        :param destination_config: destination_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#destination_config LambdaEventSourceMapping#destination_config}
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#enabled LambdaEventSourceMapping#enabled}.
        :param event_source_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#event_source_arn LambdaEventSourceMapping#event_source_arn}.
        :param filter_criteria: filter_criteria block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#filter_criteria LambdaEventSourceMapping#filter_criteria}
        :param function_response_types: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#function_response_types LambdaEventSourceMapping#function_response_types}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#id LambdaEventSourceMapping#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#maximum_batching_window_in_seconds LambdaEventSourceMapping#maximum_batching_window_in_seconds}.
        :param maximum_record_age_in_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#maximum_record_age_in_seconds LambdaEventSourceMapping#maximum_record_age_in_seconds}.
        :param maximum_retry_attempts: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#maximum_retry_attempts LambdaEventSourceMapping#maximum_retry_attempts}.
        :param parallelization_factor: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#parallelization_factor LambdaEventSourceMapping#parallelization_factor}.
        :param queues: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#queues LambdaEventSourceMapping#queues}.
        :param self_managed_event_source: self_managed_event_source block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#self_managed_event_source LambdaEventSourceMapping#self_managed_event_source}
        :param self_managed_kafka_event_source_config: self_managed_kafka_event_source_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#self_managed_kafka_event_source_config LambdaEventSourceMapping#self_managed_kafka_event_source_config}
        :param source_access_configuration: source_access_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#source_access_configuration LambdaEventSourceMapping#source_access_configuration}
        :param starting_position: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#starting_position LambdaEventSourceMapping#starting_position}.
        :param starting_position_timestamp: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#starting_position_timestamp LambdaEventSourceMapping#starting_position_timestamp}.
        :param topics: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#topics LambdaEventSourceMapping#topics}.
        :param tumbling_window_in_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#tumbling_window_in_seconds LambdaEventSourceMapping#tumbling_window_in_seconds}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a47aa757339e69266d744016f1501724d691ed438cc3614599356c063048c58)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LambdaEventSourceMappingConfig(
            function_name=function_name,
            amazon_managed_kafka_event_source_config=amazon_managed_kafka_event_source_config,
            batch_size=batch_size,
            bisect_batch_on_function_error=bisect_batch_on_function_error,
            destination_config=destination_config,
            enabled=enabled,
            event_source_arn=event_source_arn,
            filter_criteria=filter_criteria,
            function_response_types=function_response_types,
            id=id,
            maximum_batching_window_in_seconds=maximum_batching_window_in_seconds,
            maximum_record_age_in_seconds=maximum_record_age_in_seconds,
            maximum_retry_attempts=maximum_retry_attempts,
            parallelization_factor=parallelization_factor,
            queues=queues,
            self_managed_event_source=self_managed_event_source,
            self_managed_kafka_event_source_config=self_managed_kafka_event_source_config,
            source_access_configuration=source_access_configuration,
            starting_position=starting_position,
            starting_position_timestamp=starting_position_timestamp,
            topics=topics,
            tumbling_window_in_seconds=tumbling_window_in_seconds,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putAmazonManagedKafkaEventSourceConfig")
    def put_amazon_managed_kafka_event_source_config(
        self,
        *,
        consumer_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param consumer_group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#consumer_group_id LambdaEventSourceMapping#consumer_group_id}.
        '''
        value = LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig(
            consumer_group_id=consumer_group_id
        )

        return typing.cast(None, jsii.invoke(self, "putAmazonManagedKafkaEventSourceConfig", [value]))

    @jsii.member(jsii_name="putDestinationConfig")
    def put_destination_config(
        self,
        *,
        on_failure: typing.Optional[typing.Union["LambdaEventSourceMappingDestinationConfigOnFailure", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param on_failure: on_failure block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#on_failure LambdaEventSourceMapping#on_failure}
        '''
        value = LambdaEventSourceMappingDestinationConfig(on_failure=on_failure)

        return typing.cast(None, jsii.invoke(self, "putDestinationConfig", [value]))

    @jsii.member(jsii_name="putFilterCriteria")
    def put_filter_criteria(
        self,
        *,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingFilterCriteriaFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param filter: filter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#filter LambdaEventSourceMapping#filter}
        '''
        value = LambdaEventSourceMappingFilterCriteria(filter=filter)

        return typing.cast(None, jsii.invoke(self, "putFilterCriteria", [value]))

    @jsii.member(jsii_name="putSelfManagedEventSource")
    def put_self_managed_event_source(
        self,
        *,
        endpoints: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param endpoints: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#endpoints LambdaEventSourceMapping#endpoints}.
        '''
        value = LambdaEventSourceMappingSelfManagedEventSource(endpoints=endpoints)

        return typing.cast(None, jsii.invoke(self, "putSelfManagedEventSource", [value]))

    @jsii.member(jsii_name="putSelfManagedKafkaEventSourceConfig")
    def put_self_managed_kafka_event_source_config(
        self,
        *,
        consumer_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param consumer_group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#consumer_group_id LambdaEventSourceMapping#consumer_group_id}.
        '''
        value = LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig(
            consumer_group_id=consumer_group_id
        )

        return typing.cast(None, jsii.invoke(self, "putSelfManagedKafkaEventSourceConfig", [value]))

    @jsii.member(jsii_name="putSourceAccessConfiguration")
    def put_source_access_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingSourceAccessConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbca3ef7ec0a8a1ad9afd45f93ea620f3993ef54f83d3249a3bb02da154137a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSourceAccessConfiguration", [value]))

    @jsii.member(jsii_name="resetAmazonManagedKafkaEventSourceConfig")
    def reset_amazon_managed_kafka_event_source_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmazonManagedKafkaEventSourceConfig", []))

    @jsii.member(jsii_name="resetBatchSize")
    def reset_batch_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchSize", []))

    @jsii.member(jsii_name="resetBisectBatchOnFunctionError")
    def reset_bisect_batch_on_function_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBisectBatchOnFunctionError", []))

    @jsii.member(jsii_name="resetDestinationConfig")
    def reset_destination_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationConfig", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEventSourceArn")
    def reset_event_source_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventSourceArn", []))

    @jsii.member(jsii_name="resetFilterCriteria")
    def reset_filter_criteria(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterCriteria", []))

    @jsii.member(jsii_name="resetFunctionResponseTypes")
    def reset_function_response_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunctionResponseTypes", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaximumBatchingWindowInSeconds")
    def reset_maximum_batching_window_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBatchingWindowInSeconds", []))

    @jsii.member(jsii_name="resetMaximumRecordAgeInSeconds")
    def reset_maximum_record_age_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumRecordAgeInSeconds", []))

    @jsii.member(jsii_name="resetMaximumRetryAttempts")
    def reset_maximum_retry_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumRetryAttempts", []))

    @jsii.member(jsii_name="resetParallelizationFactor")
    def reset_parallelization_factor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelizationFactor", []))

    @jsii.member(jsii_name="resetQueues")
    def reset_queues(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueues", []))

    @jsii.member(jsii_name="resetSelfManagedEventSource")
    def reset_self_managed_event_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelfManagedEventSource", []))

    @jsii.member(jsii_name="resetSelfManagedKafkaEventSourceConfig")
    def reset_self_managed_kafka_event_source_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelfManagedKafkaEventSourceConfig", []))

    @jsii.member(jsii_name="resetSourceAccessConfiguration")
    def reset_source_access_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceAccessConfiguration", []))

    @jsii.member(jsii_name="resetStartingPosition")
    def reset_starting_position(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartingPosition", []))

    @jsii.member(jsii_name="resetStartingPositionTimestamp")
    def reset_starting_position_timestamp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartingPositionTimestamp", []))

    @jsii.member(jsii_name="resetTopics")
    def reset_topics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopics", []))

    @jsii.member(jsii_name="resetTumblingWindowInSeconds")
    def reset_tumbling_window_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTumblingWindowInSeconds", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="amazonManagedKafkaEventSourceConfig")
    def amazon_managed_kafka_event_source_config(
        self,
    ) -> "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigOutputReference":
        return typing.cast("LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigOutputReference", jsii.get(self, "amazonManagedKafkaEventSourceConfig"))

    @builtins.property
    @jsii.member(jsii_name="destinationConfig")
    def destination_config(
        self,
    ) -> "LambdaEventSourceMappingDestinationConfigOutputReference":
        return typing.cast("LambdaEventSourceMappingDestinationConfigOutputReference", jsii.get(self, "destinationConfig"))

    @builtins.property
    @jsii.member(jsii_name="filterCriteria")
    def filter_criteria(
        self,
    ) -> "LambdaEventSourceMappingFilterCriteriaOutputReference":
        return typing.cast("LambdaEventSourceMappingFilterCriteriaOutputReference", jsii.get(self, "filterCriteria"))

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionArn"))

    @builtins.property
    @jsii.member(jsii_name="lastModified")
    def last_modified(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModified"))

    @builtins.property
    @jsii.member(jsii_name="lastProcessingResult")
    def last_processing_result(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastProcessingResult"))

    @builtins.property
    @jsii.member(jsii_name="selfManagedEventSource")
    def self_managed_event_source(
        self,
    ) -> "LambdaEventSourceMappingSelfManagedEventSourceOutputReference":
        return typing.cast("LambdaEventSourceMappingSelfManagedEventSourceOutputReference", jsii.get(self, "selfManagedEventSource"))

    @builtins.property
    @jsii.member(jsii_name="selfManagedKafkaEventSourceConfig")
    def self_managed_kafka_event_source_config(
        self,
    ) -> "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigOutputReference":
        return typing.cast("LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigOutputReference", jsii.get(self, "selfManagedKafkaEventSourceConfig"))

    @builtins.property
    @jsii.member(jsii_name="sourceAccessConfiguration")
    def source_access_configuration(
        self,
    ) -> "LambdaEventSourceMappingSourceAccessConfigurationList":
        return typing.cast("LambdaEventSourceMappingSourceAccessConfigurationList", jsii.get(self, "sourceAccessConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateTransitionReason")
    def state_transition_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateTransitionReason"))

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

    @builtins.property
    @jsii.member(jsii_name="amazonManagedKafkaEventSourceConfigInput")
    def amazon_managed_kafka_event_source_config_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig"], jsii.get(self, "amazonManagedKafkaEventSourceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSizeInput")
    def batch_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "batchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="bisectBatchOnFunctionErrorInput")
    def bisect_batch_on_function_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bisectBatchOnFunctionErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationConfigInput")
    def destination_config_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingDestinationConfig"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingDestinationConfig"], jsii.get(self, "destinationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="eventSourceArnInput")
    def event_source_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventSourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="filterCriteriaInput")
    def filter_criteria_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingFilterCriteria"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingFilterCriteria"], jsii.get(self, "filterCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="functionNameInput")
    def function_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="functionResponseTypesInput")
    def function_response_types_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "functionResponseTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSecondsInput")
    def maximum_batching_window_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumBatchingWindowInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumRecordAgeInSecondsInput")
    def maximum_record_age_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumRecordAgeInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumRetryAttemptsInput")
    def maximum_retry_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumRetryAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelizationFactorInput")
    def parallelization_factor_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "parallelizationFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="queuesInput")
    def queues_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queuesInput"))

    @builtins.property
    @jsii.member(jsii_name="selfManagedEventSourceInput")
    def self_managed_event_source_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingSelfManagedEventSource"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingSelfManagedEventSource"], jsii.get(self, "selfManagedEventSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="selfManagedKafkaEventSourceConfigInput")
    def self_managed_kafka_event_source_config_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig"], jsii.get(self, "selfManagedKafkaEventSourceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceAccessConfigurationInput")
    def source_access_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSourceAccessConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSourceAccessConfiguration"]]], jsii.get(self, "sourceAccessConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionInput")
    def starting_position_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startingPositionInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionTimestampInput")
    def starting_position_timestamp_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startingPositionTimestampInput"))

    @builtins.property
    @jsii.member(jsii_name="topicsInput")
    def topics_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "topicsInput"))

    @builtins.property
    @jsii.member(jsii_name="tumblingWindowInSecondsInput")
    def tumbling_window_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tumblingWindowInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSize")
    def batch_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "batchSize"))

    @batch_size.setter
    def batch_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__541561415b9451234dacc6dcb3a8b7a5fe5fd4a7af017fb0f870e1133ddc8646)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchSize", value)

    @builtins.property
    @jsii.member(jsii_name="bisectBatchOnFunctionError")
    def bisect_batch_on_function_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bisectBatchOnFunctionError"))

    @bisect_batch_on_function_error.setter
    def bisect_batch_on_function_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad19047a73254501ebee29526fb3b3ad7cda341fd1a4cd8b5086fa0f976d6612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bisectBatchOnFunctionError", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad70d04d1e3f4cf084aa26ef29f1c7c59724e7c8f8976d27fdbc698db3e55742)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="eventSourceArn")
    def event_source_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventSourceArn"))

    @event_source_arn.setter
    def event_source_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25dc16d1d8da84542069b020c23aec363f4216cc95a98064d54479c7dab33671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventSourceArn", value)

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionName"))

    @function_name.setter
    def function_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c5007634a0b77af02f6cadca8b2bcbbf8db9b6272bd817bc2fce50c7cb023f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionName", value)

    @builtins.property
    @jsii.member(jsii_name="functionResponseTypes")
    def function_response_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "functionResponseTypes"))

    @function_response_types.setter
    def function_response_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f1bd5ee9b15aa474173407dbbfbf9105cbeaa5930dedf098446736fd5afff22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionResponseTypes", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39050b5f603238cbae08d6e92e8499f00f28afbb26311d2e2847848f7c3e7591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSeconds")
    def maximum_batching_window_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBatchingWindowInSeconds"))

    @maximum_batching_window_in_seconds.setter
    def maximum_batching_window_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__007a021ea006cac974f544b05437524be45ecbbea5b8a78164d858df1dc784e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBatchingWindowInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="maximumRecordAgeInSeconds")
    def maximum_record_age_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumRecordAgeInSeconds"))

    @maximum_record_age_in_seconds.setter
    def maximum_record_age_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf5f5ae47a9906e08465db2184f08779fa1689cac2e02f711eb8c53f6f79d981)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumRecordAgeInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="maximumRetryAttempts")
    def maximum_retry_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumRetryAttempts"))

    @maximum_retry_attempts.setter
    def maximum_retry_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3d838cef1136da132b8bc289f46ead1c226ed7f67d9c262aee72948e00c30a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumRetryAttempts", value)

    @builtins.property
    @jsii.member(jsii_name="parallelizationFactor")
    def parallelization_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parallelizationFactor"))

    @parallelization_factor.setter
    def parallelization_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__287ea91a1d6fb462d2b2456cdd406eb601a97f2e9ed98fa645d53ae38934ef73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelizationFactor", value)

    @builtins.property
    @jsii.member(jsii_name="queues")
    def queues(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queues"))

    @queues.setter
    def queues(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b7dc53557152da3e91935d8f0830c85c6557f96bccb8abe011af284497cd7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queues", value)

    @builtins.property
    @jsii.member(jsii_name="startingPosition")
    def starting_position(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startingPosition"))

    @starting_position.setter
    def starting_position(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d34d647942528ee7ce024140746bc344b6c6ac28931ecc0006604fcd0e246a10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingPosition", value)

    @builtins.property
    @jsii.member(jsii_name="startingPositionTimestamp")
    def starting_position_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startingPositionTimestamp"))

    @starting_position_timestamp.setter
    def starting_position_timestamp(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b0493ea45885b9b7252fcddb33c43c5209138dda3596a7e1c80907cdbf97fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingPositionTimestamp", value)

    @builtins.property
    @jsii.member(jsii_name="topics")
    def topics(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "topics"))

    @topics.setter
    def topics(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d057d80fb2aaa0997a9ee926dbe4dac093c30664f420d247f34f0689c8a100b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topics", value)

    @builtins.property
    @jsii.member(jsii_name="tumblingWindowInSeconds")
    def tumbling_window_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tumblingWindowInSeconds"))

    @tumbling_window_in_seconds.setter
    def tumbling_window_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57fc9d9b567503596648cb9a88e55911cf97c51725effa41974546916a0638b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tumblingWindowInSeconds", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig",
    jsii_struct_bases=[],
    name_mapping={"consumer_group_id": "consumerGroupId"},
)
class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig:
    def __init__(
        self,
        *,
        consumer_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param consumer_group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#consumer_group_id LambdaEventSourceMapping#consumer_group_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae07895fe3063469b17db40b7a275858ff5d4c6bffee563124c804bda7c3861)
            check_type(argname="argument consumer_group_id", value=consumer_group_id, expected_type=type_hints["consumer_group_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if consumer_group_id is not None:
            self._values["consumer_group_id"] = consumer_group_id

    @builtins.property
    def consumer_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#consumer_group_id LambdaEventSourceMapping#consumer_group_id}.'''
        result = self._values.get("consumer_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3357452e9a4b48f8661e21aa1beb11ae1098859cc02011d784871e61b0bd1ab2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConsumerGroupId")
    def reset_consumer_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerGroupId", []))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupIdInput")
    def consumer_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupId")
    def consumer_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerGroupId"))

    @consumer_group_id.setter
    def consumer_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1bbd65537fdf9a8bed47da88de63a4724981a8abad1ec09f1ca2dc00d76ccf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__241b103203a35602f493d8495dce6ae9d90c439c6faa223564d7a63305710b64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "function_name": "functionName",
        "amazon_managed_kafka_event_source_config": "amazonManagedKafkaEventSourceConfig",
        "batch_size": "batchSize",
        "bisect_batch_on_function_error": "bisectBatchOnFunctionError",
        "destination_config": "destinationConfig",
        "enabled": "enabled",
        "event_source_arn": "eventSourceArn",
        "filter_criteria": "filterCriteria",
        "function_response_types": "functionResponseTypes",
        "id": "id",
        "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
        "maximum_record_age_in_seconds": "maximumRecordAgeInSeconds",
        "maximum_retry_attempts": "maximumRetryAttempts",
        "parallelization_factor": "parallelizationFactor",
        "queues": "queues",
        "self_managed_event_source": "selfManagedEventSource",
        "self_managed_kafka_event_source_config": "selfManagedKafkaEventSourceConfig",
        "source_access_configuration": "sourceAccessConfiguration",
        "starting_position": "startingPosition",
        "starting_position_timestamp": "startingPositionTimestamp",
        "topics": "topics",
        "tumbling_window_in_seconds": "tumblingWindowInSeconds",
    },
)
class LambdaEventSourceMappingConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        function_name: builtins.str,
        amazon_managed_kafka_event_source_config: typing.Optional[typing.Union[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_function_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        destination_config: typing.Optional[typing.Union["LambdaEventSourceMappingDestinationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        event_source_arn: typing.Optional[builtins.str] = None,
        filter_criteria: typing.Optional[typing.Union["LambdaEventSourceMappingFilterCriteria", typing.Dict[builtins.str, typing.Any]]] = None,
        function_response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        queues: typing.Optional[typing.Sequence[builtins.str]] = None,
        self_managed_event_source: typing.Optional[typing.Union["LambdaEventSourceMappingSelfManagedEventSource", typing.Dict[builtins.str, typing.Any]]] = None,
        self_managed_kafka_event_source_config: typing.Optional[typing.Union["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        source_access_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingSourceAccessConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        starting_position: typing.Optional[builtins.str] = None,
        starting_position_timestamp: typing.Optional[builtins.str] = None,
        topics: typing.Optional[typing.Sequence[builtins.str]] = None,
        tumbling_window_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param function_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#function_name LambdaEventSourceMapping#function_name}.
        :param amazon_managed_kafka_event_source_config: amazon_managed_kafka_event_source_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#amazon_managed_kafka_event_source_config LambdaEventSourceMapping#amazon_managed_kafka_event_source_config}
        :param batch_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#batch_size LambdaEventSourceMapping#batch_size}.
        :param bisect_batch_on_function_error: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#bisect_batch_on_function_error LambdaEventSourceMapping#bisect_batch_on_function_error}.
        :param destination_config: destination_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#destination_config LambdaEventSourceMapping#destination_config}
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#enabled LambdaEventSourceMapping#enabled}.
        :param event_source_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#event_source_arn LambdaEventSourceMapping#event_source_arn}.
        :param filter_criteria: filter_criteria block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#filter_criteria LambdaEventSourceMapping#filter_criteria}
        :param function_response_types: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#function_response_types LambdaEventSourceMapping#function_response_types}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#id LambdaEventSourceMapping#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#maximum_batching_window_in_seconds LambdaEventSourceMapping#maximum_batching_window_in_seconds}.
        :param maximum_record_age_in_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#maximum_record_age_in_seconds LambdaEventSourceMapping#maximum_record_age_in_seconds}.
        :param maximum_retry_attempts: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#maximum_retry_attempts LambdaEventSourceMapping#maximum_retry_attempts}.
        :param parallelization_factor: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#parallelization_factor LambdaEventSourceMapping#parallelization_factor}.
        :param queues: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#queues LambdaEventSourceMapping#queues}.
        :param self_managed_event_source: self_managed_event_source block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#self_managed_event_source LambdaEventSourceMapping#self_managed_event_source}
        :param self_managed_kafka_event_source_config: self_managed_kafka_event_source_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#self_managed_kafka_event_source_config LambdaEventSourceMapping#self_managed_kafka_event_source_config}
        :param source_access_configuration: source_access_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#source_access_configuration LambdaEventSourceMapping#source_access_configuration}
        :param starting_position: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#starting_position LambdaEventSourceMapping#starting_position}.
        :param starting_position_timestamp: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#starting_position_timestamp LambdaEventSourceMapping#starting_position_timestamp}.
        :param topics: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#topics LambdaEventSourceMapping#topics}.
        :param tumbling_window_in_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#tumbling_window_in_seconds LambdaEventSourceMapping#tumbling_window_in_seconds}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(amazon_managed_kafka_event_source_config, dict):
            amazon_managed_kafka_event_source_config = LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig(**amazon_managed_kafka_event_source_config)
        if isinstance(destination_config, dict):
            destination_config = LambdaEventSourceMappingDestinationConfig(**destination_config)
        if isinstance(filter_criteria, dict):
            filter_criteria = LambdaEventSourceMappingFilterCriteria(**filter_criteria)
        if isinstance(self_managed_event_source, dict):
            self_managed_event_source = LambdaEventSourceMappingSelfManagedEventSource(**self_managed_event_source)
        if isinstance(self_managed_kafka_event_source_config, dict):
            self_managed_kafka_event_source_config = LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig(**self_managed_kafka_event_source_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64877458e53fece918bfc3ada09bc9c10e559b190aa510fbe6c6c28a73b186fa)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument amazon_managed_kafka_event_source_config", value=amazon_managed_kafka_event_source_config, expected_type=type_hints["amazon_managed_kafka_event_source_config"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument bisect_batch_on_function_error", value=bisect_batch_on_function_error, expected_type=type_hints["bisect_batch_on_function_error"])
            check_type(argname="argument destination_config", value=destination_config, expected_type=type_hints["destination_config"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument event_source_arn", value=event_source_arn, expected_type=type_hints["event_source_arn"])
            check_type(argname="argument filter_criteria", value=filter_criteria, expected_type=type_hints["filter_criteria"])
            check_type(argname="argument function_response_types", value=function_response_types, expected_type=type_hints["function_response_types"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
            check_type(argname="argument maximum_record_age_in_seconds", value=maximum_record_age_in_seconds, expected_type=type_hints["maximum_record_age_in_seconds"])
            check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
            check_type(argname="argument parallelization_factor", value=parallelization_factor, expected_type=type_hints["parallelization_factor"])
            check_type(argname="argument queues", value=queues, expected_type=type_hints["queues"])
            check_type(argname="argument self_managed_event_source", value=self_managed_event_source, expected_type=type_hints["self_managed_event_source"])
            check_type(argname="argument self_managed_kafka_event_source_config", value=self_managed_kafka_event_source_config, expected_type=type_hints["self_managed_kafka_event_source_config"])
            check_type(argname="argument source_access_configuration", value=source_access_configuration, expected_type=type_hints["source_access_configuration"])
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
            check_type(argname="argument starting_position_timestamp", value=starting_position_timestamp, expected_type=type_hints["starting_position_timestamp"])
            check_type(argname="argument topics", value=topics, expected_type=type_hints["topics"])
            check_type(argname="argument tumbling_window_in_seconds", value=tumbling_window_in_seconds, expected_type=type_hints["tumbling_window_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_name": function_name,
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
        if amazon_managed_kafka_event_source_config is not None:
            self._values["amazon_managed_kafka_event_source_config"] = amazon_managed_kafka_event_source_config
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if bisect_batch_on_function_error is not None:
            self._values["bisect_batch_on_function_error"] = bisect_batch_on_function_error
        if destination_config is not None:
            self._values["destination_config"] = destination_config
        if enabled is not None:
            self._values["enabled"] = enabled
        if event_source_arn is not None:
            self._values["event_source_arn"] = event_source_arn
        if filter_criteria is not None:
            self._values["filter_criteria"] = filter_criteria
        if function_response_types is not None:
            self._values["function_response_types"] = function_response_types
        if id is not None:
            self._values["id"] = id
        if maximum_batching_window_in_seconds is not None:
            self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
        if maximum_record_age_in_seconds is not None:
            self._values["maximum_record_age_in_seconds"] = maximum_record_age_in_seconds
        if maximum_retry_attempts is not None:
            self._values["maximum_retry_attempts"] = maximum_retry_attempts
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor
        if queues is not None:
            self._values["queues"] = queues
        if self_managed_event_source is not None:
            self._values["self_managed_event_source"] = self_managed_event_source
        if self_managed_kafka_event_source_config is not None:
            self._values["self_managed_kafka_event_source_config"] = self_managed_kafka_event_source_config
        if source_access_configuration is not None:
            self._values["source_access_configuration"] = source_access_configuration
        if starting_position is not None:
            self._values["starting_position"] = starting_position
        if starting_position_timestamp is not None:
            self._values["starting_position_timestamp"] = starting_position_timestamp
        if topics is not None:
            self._values["topics"] = topics
        if tumbling_window_in_seconds is not None:
            self._values["tumbling_window_in_seconds"] = tumbling_window_in_seconds

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
    def function_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#function_name LambdaEventSourceMapping#function_name}.'''
        result = self._values.get("function_name")
        assert result is not None, "Required property 'function_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def amazon_managed_kafka_event_source_config(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig]:
        '''amazon_managed_kafka_event_source_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#amazon_managed_kafka_event_source_config LambdaEventSourceMapping#amazon_managed_kafka_event_source_config}
        '''
        result = self._values.get("amazon_managed_kafka_event_source_config")
        return typing.cast(typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig], result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#batch_size LambdaEventSourceMapping#batch_size}.'''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bisect_batch_on_function_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#bisect_batch_on_function_error LambdaEventSourceMapping#bisect_batch_on_function_error}.'''
        result = self._values.get("bisect_batch_on_function_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def destination_config(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingDestinationConfig"]:
        '''destination_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#destination_config LambdaEventSourceMapping#destination_config}
        '''
        result = self._values.get("destination_config")
        return typing.cast(typing.Optional["LambdaEventSourceMappingDestinationConfig"], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#enabled LambdaEventSourceMapping#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def event_source_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#event_source_arn LambdaEventSourceMapping#event_source_arn}.'''
        result = self._values.get("event_source_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_criteria(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingFilterCriteria"]:
        '''filter_criteria block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#filter_criteria LambdaEventSourceMapping#filter_criteria}
        '''
        result = self._values.get("filter_criteria")
        return typing.cast(typing.Optional["LambdaEventSourceMappingFilterCriteria"], result)

    @builtins.property
    def function_response_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#function_response_types LambdaEventSourceMapping#function_response_types}.'''
        result = self._values.get("function_response_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#id LambdaEventSourceMapping#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#maximum_batching_window_in_seconds LambdaEventSourceMapping#maximum_batching_window_in_seconds}.'''
        result = self._values.get("maximum_batching_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_record_age_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#maximum_record_age_in_seconds LambdaEventSourceMapping#maximum_record_age_in_seconds}.'''
        result = self._values.get("maximum_record_age_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#maximum_retry_attempts LambdaEventSourceMapping#maximum_retry_attempts}.'''
        result = self._values.get("maximum_retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#parallelization_factor LambdaEventSourceMapping#parallelization_factor}.'''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def queues(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#queues LambdaEventSourceMapping#queues}.'''
        result = self._values.get("queues")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def self_managed_event_source(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingSelfManagedEventSource"]:
        '''self_managed_event_source block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#self_managed_event_source LambdaEventSourceMapping#self_managed_event_source}
        '''
        result = self._values.get("self_managed_event_source")
        return typing.cast(typing.Optional["LambdaEventSourceMappingSelfManagedEventSource"], result)

    @builtins.property
    def self_managed_kafka_event_source_config(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig"]:
        '''self_managed_kafka_event_source_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#self_managed_kafka_event_source_config LambdaEventSourceMapping#self_managed_kafka_event_source_config}
        '''
        result = self._values.get("self_managed_kafka_event_source_config")
        return typing.cast(typing.Optional["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig"], result)

    @builtins.property
    def source_access_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSourceAccessConfiguration"]]]:
        '''source_access_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#source_access_configuration LambdaEventSourceMapping#source_access_configuration}
        '''
        result = self._values.get("source_access_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSourceAccessConfiguration"]]], result)

    @builtins.property
    def starting_position(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#starting_position LambdaEventSourceMapping#starting_position}.'''
        result = self._values.get("starting_position")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def starting_position_timestamp(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#starting_position_timestamp LambdaEventSourceMapping#starting_position_timestamp}.'''
        result = self._values.get("starting_position_timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def topics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#topics LambdaEventSourceMapping#topics}.'''
        result = self._values.get("topics")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tumbling_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#tumbling_window_in_seconds LambdaEventSourceMapping#tumbling_window_in_seconds}.'''
        result = self._values.get("tumbling_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingDestinationConfig",
    jsii_struct_bases=[],
    name_mapping={"on_failure": "onFailure"},
)
class LambdaEventSourceMappingDestinationConfig:
    def __init__(
        self,
        *,
        on_failure: typing.Optional[typing.Union["LambdaEventSourceMappingDestinationConfigOnFailure", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param on_failure: on_failure block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#on_failure LambdaEventSourceMapping#on_failure}
        '''
        if isinstance(on_failure, dict):
            on_failure = LambdaEventSourceMappingDestinationConfigOnFailure(**on_failure)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34c9f0b388f168ec909930e18b64b0a89faae7ed714a8203b33b39f48bab681d)
            check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if on_failure is not None:
            self._values["on_failure"] = on_failure

    @builtins.property
    def on_failure(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingDestinationConfigOnFailure"]:
        '''on_failure block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#on_failure LambdaEventSourceMapping#on_failure}
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional["LambdaEventSourceMappingDestinationConfigOnFailure"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingDestinationConfigOnFailure",
    jsii_struct_bases=[],
    name_mapping={"destination_arn": "destinationArn"},
)
class LambdaEventSourceMappingDestinationConfigOnFailure:
    def __init__(self, *, destination_arn: builtins.str) -> None:
        '''
        :param destination_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#destination_arn LambdaEventSourceMapping#destination_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__576a0eba521c801c96c7b1d9547be6e63b7785dee36315d6db7b6a0550009ad5)
            check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_arn": destination_arn,
        }

    @builtins.property
    def destination_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#destination_arn LambdaEventSourceMapping#destination_arn}.'''
        result = self._values.get("destination_arn")
        assert result is not None, "Required property 'destination_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingDestinationConfigOnFailure(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingDestinationConfigOnFailureOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingDestinationConfigOnFailureOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__630832b3b534625a424221bfde5f786d1f1ffddad0ec9ee2a876df687e46e79f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationArnInput")
    def destination_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationArnInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationArn"))

    @destination_arn.setter
    def destination_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d22489075dff3e3357b483770d6dc55130727cbc7b3314afe0c6aeb655319289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingDestinationConfigOnFailure]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingDestinationConfigOnFailure], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingDestinationConfigOnFailure],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a40dd6edecd910b3198907903ed7799a03005028da09ae5c3710c7263d48230)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LambdaEventSourceMappingDestinationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingDestinationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ca1586fcbfe56ac8f4bc2aa11b4c789896b8f4134a70754c4671233ee4f5f50)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOnFailure")
    def put_on_failure(self, *, destination_arn: builtins.str) -> None:
        '''
        :param destination_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#destination_arn LambdaEventSourceMapping#destination_arn}.
        '''
        value = LambdaEventSourceMappingDestinationConfigOnFailure(
            destination_arn=destination_arn
        )

        return typing.cast(None, jsii.invoke(self, "putOnFailure", [value]))

    @jsii.member(jsii_name="resetOnFailure")
    def reset_on_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnFailure", []))

    @builtins.property
    @jsii.member(jsii_name="onFailure")
    def on_failure(
        self,
    ) -> LambdaEventSourceMappingDestinationConfigOnFailureOutputReference:
        return typing.cast(LambdaEventSourceMappingDestinationConfigOnFailureOutputReference, jsii.get(self, "onFailure"))

    @builtins.property
    @jsii.member(jsii_name="onFailureInput")
    def on_failure_input(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingDestinationConfigOnFailure]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingDestinationConfigOnFailure], jsii.get(self, "onFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingDestinationConfig]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingDestinationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingDestinationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b8f60294131cc23ff467227e1e80d5a38227b46da9e8e8c60bfb37f82aa8c95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingFilterCriteria",
    jsii_struct_bases=[],
    name_mapping={"filter": "filter"},
)
class LambdaEventSourceMappingFilterCriteria:
    def __init__(
        self,
        *,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingFilterCriteriaFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param filter: filter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#filter LambdaEventSourceMapping#filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d530693652faef12942656056ae1f83a1f26c650fdda463d012d77ba0938fadb)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter is not None:
            self._values["filter"] = filter

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingFilterCriteriaFilter"]]]:
        '''filter block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#filter LambdaEventSourceMapping#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingFilterCriteriaFilter"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingFilterCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingFilterCriteriaFilter",
    jsii_struct_bases=[],
    name_mapping={"pattern": "pattern"},
)
class LambdaEventSourceMappingFilterCriteriaFilter:
    def __init__(self, *, pattern: typing.Optional[builtins.str] = None) -> None:
        '''
        :param pattern: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#pattern LambdaEventSourceMapping#pattern}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eaa4309d2e4ea68d137970b0d83165fe3985ebb4115164a7e2a3154ad8dfbfd)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pattern is not None:
            self._values["pattern"] = pattern

    @builtins.property
    def pattern(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#pattern LambdaEventSourceMapping#pattern}.'''
        result = self._values.get("pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingFilterCriteriaFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingFilterCriteriaFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingFilterCriteriaFilterList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d706b5ee3016a7a4ec9c9eadfbc14972d08c40fbcf17ffb761b1c7275c744e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LambdaEventSourceMappingFilterCriteriaFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1175ebc8244990f76740bc49fb76932046078924e37d8f1692ce9bf28a07d7e9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LambdaEventSourceMappingFilterCriteriaFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f053edf2d14673ea9287bdb68915dc2dfc815f22a29ff944c2e0dc414dffad3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa126ca9964bd3aa4fcb977332863782ad6ae733b6d3751c885280f21ffe98ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c371c6014487911232332acb2e8eeac5c1569af1b2464330d3014d5e21ef694)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingFilterCriteriaFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingFilterCriteriaFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingFilterCriteriaFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fdb04d9150902e1b8a2871fbd91e652493a1766a47ef9f3c0595a283979a0cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LambdaEventSourceMappingFilterCriteriaFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingFilterCriteriaFilterOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f501d48e5274adca1b7fcc603ac574a40c9a2dc8779689d6a1928974b68423a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPattern")
    def reset_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPattern", []))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__214652ec66555668b8bc5a979d45f9b2df52dc741b0765be58a0a239c663407a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LambdaEventSourceMappingFilterCriteriaFilter, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LambdaEventSourceMappingFilterCriteriaFilter, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LambdaEventSourceMappingFilterCriteriaFilter, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d64bf7f51af4a6978326e1aef1f95a6ad437ee14d4282c65c5b4dfb403739cda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LambdaEventSourceMappingFilterCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingFilterCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf90e99296b6b0836dcd21cfedbd96cba0de8817c28b86fe45e5a81d3e9a4a52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingFilterCriteriaFilter, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fed9484a7553309c5a38b3ad891206d0ade480e84f9da82d9b030b886c21c93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> LambdaEventSourceMappingFilterCriteriaFilterList:
        return typing.cast(LambdaEventSourceMappingFilterCriteriaFilterList, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingFilterCriteriaFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingFilterCriteriaFilter]]], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LambdaEventSourceMappingFilterCriteria]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingFilterCriteria], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingFilterCriteria],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1a02ab1e31c47b64c90e7cc7060e5f525711e57eba08e73753d9d15400fd741)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedEventSource",
    jsii_struct_bases=[],
    name_mapping={"endpoints": "endpoints"},
)
class LambdaEventSourceMappingSelfManagedEventSource:
    def __init__(
        self,
        *,
        endpoints: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param endpoints: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#endpoints LambdaEventSourceMapping#endpoints}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f718d9f0c61db275ede06a61fe886dc168521189524bb83565d3da9c025c48e)
            check_type(argname="argument endpoints", value=endpoints, expected_type=type_hints["endpoints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoints": endpoints,
        }

    @builtins.property
    def endpoints(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#endpoints LambdaEventSourceMapping#endpoints}.'''
        result = self._values.get("endpoints")
        assert result is not None, "Required property 'endpoints' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingSelfManagedEventSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingSelfManagedEventSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedEventSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bbba2764bd988b4a816a46955500ec7a6c7dceed523e5314b7a48586e45340a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="endpointsInput")
    def endpoints_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "endpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="endpoints")
    def endpoints(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "endpoints"))

    @endpoints.setter
    def endpoints(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a076c1f8baac0f9ff5ba3dd8e69a900b577e74be7cfbec5ccc8f488fec1896c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoints", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingSelfManagedEventSource]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingSelfManagedEventSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingSelfManagedEventSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca82dd2b84242acad82c6883bebd93cea9346581689399f883727e4d44589776)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig",
    jsii_struct_bases=[],
    name_mapping={"consumer_group_id": "consumerGroupId"},
)
class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig:
    def __init__(
        self,
        *,
        consumer_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param consumer_group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#consumer_group_id LambdaEventSourceMapping#consumer_group_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__552f5accfcb9ea14c92bd78af097762e0ae1236cab5d2bb2ad88f563414bb309)
            check_type(argname="argument consumer_group_id", value=consumer_group_id, expected_type=type_hints["consumer_group_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if consumer_group_id is not None:
            self._values["consumer_group_id"] = consumer_group_id

    @builtins.property
    def consumer_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#consumer_group_id LambdaEventSourceMapping#consumer_group_id}.'''
        result = self._values.get("consumer_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6356265f44a9462aff0a0bd5cf3e3da9ce2261f824f5f7b98d1fb4c80bbd090)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConsumerGroupId")
    def reset_consumer_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerGroupId", []))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupIdInput")
    def consumer_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupId")
    def consumer_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerGroupId"))

    @consumer_group_id.setter
    def consumer_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8e960270f5884b70648a3fbbbed56d1d11a13b177ec49f5c07bbf4b60b5495b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f35651559ea6accdc41caeff6ea91750ce0e9c62392d3992ac409086f2b8948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSourceAccessConfiguration",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "uri": "uri"},
)
class LambdaEventSourceMappingSourceAccessConfiguration:
    def __init__(self, *, type: builtins.str, uri: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#type LambdaEventSourceMapping#type}.
        :param uri: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#uri LambdaEventSourceMapping#uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f749b47122b9bf8627a73e0d68e5a12071defd185889c6b9ee5024d6d0c56ea)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "uri": uri,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#type LambdaEventSourceMapping#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/lambda_event_source_mapping#uri LambdaEventSourceMapping#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingSourceAccessConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingSourceAccessConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSourceAccessConfigurationList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8985b422c6d88695b44d933886ca9236f32f376829c246b1e7e4f8bd9fb0c6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LambdaEventSourceMappingSourceAccessConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3117b2e2f4b8c616c5d264161ea71f205c9701d6f1194bd911b60fc3e2532446)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LambdaEventSourceMappingSourceAccessConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09481dd8d0fb3245e87c3a245d04ad5551bc07042668b540b4d99249ddd29acc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94cf9718d242637fcc2263e8bd7fa6113232cd77ad3331c35acbbb244616b686)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf65c356a4bc87ab20d9a5752ecf6033bfdca646bf56efe47922d4fdfe27562e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSourceAccessConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSourceAccessConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSourceAccessConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__765cea81bf496ba1278e49377193052e975811a5f5751600a86f4ce142ee14c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LambdaEventSourceMappingSourceAccessConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSourceAccessConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9c89a4840a4763b1e73653623afb28787f2069fae0f8c4db3f43215aec63322)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebeffa72cc48a3625370697e7bd01c77b8bec050369175e629c752caed6cd786)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70eb273fc598e283b663c20be432cb6f94be8b6d5caf501372dd5a423329b91e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LambdaEventSourceMappingSourceAccessConfiguration, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LambdaEventSourceMappingSourceAccessConfiguration, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LambdaEventSourceMappingSourceAccessConfiguration, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa0313df950f6ce97798b4c90f261a746c6902efc9988912c017a7ce589b97e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "LambdaEventSourceMapping",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigOutputReference",
    "LambdaEventSourceMappingConfig",
    "LambdaEventSourceMappingDestinationConfig",
    "LambdaEventSourceMappingDestinationConfigOnFailure",
    "LambdaEventSourceMappingDestinationConfigOnFailureOutputReference",
    "LambdaEventSourceMappingDestinationConfigOutputReference",
    "LambdaEventSourceMappingFilterCriteria",
    "LambdaEventSourceMappingFilterCriteriaFilter",
    "LambdaEventSourceMappingFilterCriteriaFilterList",
    "LambdaEventSourceMappingFilterCriteriaFilterOutputReference",
    "LambdaEventSourceMappingFilterCriteriaOutputReference",
    "LambdaEventSourceMappingSelfManagedEventSource",
    "LambdaEventSourceMappingSelfManagedEventSourceOutputReference",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigOutputReference",
    "LambdaEventSourceMappingSourceAccessConfiguration",
    "LambdaEventSourceMappingSourceAccessConfigurationList",
    "LambdaEventSourceMappingSourceAccessConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__4a47aa757339e69266d744016f1501724d691ed438cc3614599356c063048c58(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    function_name: builtins.str,
    amazon_managed_kafka_event_source_config: typing.Optional[typing.Union[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    batch_size: typing.Optional[jsii.Number] = None,
    bisect_batch_on_function_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    destination_config: typing.Optional[typing.Union[LambdaEventSourceMappingDestinationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    event_source_arn: typing.Optional[builtins.str] = None,
    filter_criteria: typing.Optional[typing.Union[LambdaEventSourceMappingFilterCriteria, typing.Dict[builtins.str, typing.Any]]] = None,
    function_response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
    queues: typing.Optional[typing.Sequence[builtins.str]] = None,
    self_managed_event_source: typing.Optional[typing.Union[LambdaEventSourceMappingSelfManagedEventSource, typing.Dict[builtins.str, typing.Any]]] = None,
    self_managed_kafka_event_source_config: typing.Optional[typing.Union[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    source_access_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingSourceAccessConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    starting_position: typing.Optional[builtins.str] = None,
    starting_position_timestamp: typing.Optional[builtins.str] = None,
    topics: typing.Optional[typing.Sequence[builtins.str]] = None,
    tumbling_window_in_seconds: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__cbca3ef7ec0a8a1ad9afd45f93ea620f3993ef54f83d3249a3bb02da154137a0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingSourceAccessConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__541561415b9451234dacc6dcb3a8b7a5fe5fd4a7af017fb0f870e1133ddc8646(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad19047a73254501ebee29526fb3b3ad7cda341fd1a4cd8b5086fa0f976d6612(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad70d04d1e3f4cf084aa26ef29f1c7c59724e7c8f8976d27fdbc698db3e55742(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25dc16d1d8da84542069b020c23aec363f4216cc95a98064d54479c7dab33671(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c5007634a0b77af02f6cadca8b2bcbbf8db9b6272bd817bc2fce50c7cb023f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f1bd5ee9b15aa474173407dbbfbf9105cbeaa5930dedf098446736fd5afff22(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39050b5f603238cbae08d6e92e8499f00f28afbb26311d2e2847848f7c3e7591(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__007a021ea006cac974f544b05437524be45ecbbea5b8a78164d858df1dc784e7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf5f5ae47a9906e08465db2184f08779fa1689cac2e02f711eb8c53f6f79d981(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d838cef1136da132b8bc289f46ead1c226ed7f67d9c262aee72948e00c30a1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__287ea91a1d6fb462d2b2456cdd406eb601a97f2e9ed98fa645d53ae38934ef73(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b7dc53557152da3e91935d8f0830c85c6557f96bccb8abe011af284497cd7a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d34d647942528ee7ce024140746bc344b6c6ac28931ecc0006604fcd0e246a10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b0493ea45885b9b7252fcddb33c43c5209138dda3596a7e1c80907cdbf97fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d057d80fb2aaa0997a9ee926dbe4dac093c30664f420d247f34f0689c8a100b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57fc9d9b567503596648cb9a88e55911cf97c51725effa41974546916a0638b3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae07895fe3063469b17db40b7a275858ff5d4c6bffee563124c804bda7c3861(
    *,
    consumer_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3357452e9a4b48f8661e21aa1beb11ae1098859cc02011d784871e61b0bd1ab2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1bbd65537fdf9a8bed47da88de63a4724981a8abad1ec09f1ca2dc00d76ccf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241b103203a35602f493d8495dce6ae9d90c439c6faa223564d7a63305710b64(
    value: typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64877458e53fece918bfc3ada09bc9c10e559b190aa510fbe6c6c28a73b186fa(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    function_name: builtins.str,
    amazon_managed_kafka_event_source_config: typing.Optional[typing.Union[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    batch_size: typing.Optional[jsii.Number] = None,
    bisect_batch_on_function_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    destination_config: typing.Optional[typing.Union[LambdaEventSourceMappingDestinationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    event_source_arn: typing.Optional[builtins.str] = None,
    filter_criteria: typing.Optional[typing.Union[LambdaEventSourceMappingFilterCriteria, typing.Dict[builtins.str, typing.Any]]] = None,
    function_response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
    queues: typing.Optional[typing.Sequence[builtins.str]] = None,
    self_managed_event_source: typing.Optional[typing.Union[LambdaEventSourceMappingSelfManagedEventSource, typing.Dict[builtins.str, typing.Any]]] = None,
    self_managed_kafka_event_source_config: typing.Optional[typing.Union[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    source_access_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingSourceAccessConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    starting_position: typing.Optional[builtins.str] = None,
    starting_position_timestamp: typing.Optional[builtins.str] = None,
    topics: typing.Optional[typing.Sequence[builtins.str]] = None,
    tumbling_window_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34c9f0b388f168ec909930e18b64b0a89faae7ed714a8203b33b39f48bab681d(
    *,
    on_failure: typing.Optional[typing.Union[LambdaEventSourceMappingDestinationConfigOnFailure, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__576a0eba521c801c96c7b1d9547be6e63b7785dee36315d6db7b6a0550009ad5(
    *,
    destination_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630832b3b534625a424221bfde5f786d1f1ffddad0ec9ee2a876df687e46e79f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d22489075dff3e3357b483770d6dc55130727cbc7b3314afe0c6aeb655319289(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a40dd6edecd910b3198907903ed7799a03005028da09ae5c3710c7263d48230(
    value: typing.Optional[LambdaEventSourceMappingDestinationConfigOnFailure],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca1586fcbfe56ac8f4bc2aa11b4c789896b8f4134a70754c4671233ee4f5f50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8f60294131cc23ff467227e1e80d5a38227b46da9e8e8c60bfb37f82aa8c95(
    value: typing.Optional[LambdaEventSourceMappingDestinationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d530693652faef12942656056ae1f83a1f26c650fdda463d012d77ba0938fadb(
    *,
    filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingFilterCriteriaFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eaa4309d2e4ea68d137970b0d83165fe3985ebb4115164a7e2a3154ad8dfbfd(
    *,
    pattern: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d706b5ee3016a7a4ec9c9eadfbc14972d08c40fbcf17ffb761b1c7275c744e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1175ebc8244990f76740bc49fb76932046078924e37d8f1692ce9bf28a07d7e9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f053edf2d14673ea9287bdb68915dc2dfc815f22a29ff944c2e0dc414dffad3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa126ca9964bd3aa4fcb977332863782ad6ae733b6d3751c885280f21ffe98ad(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c371c6014487911232332acb2e8eeac5c1569af1b2464330d3014d5e21ef694(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fdb04d9150902e1b8a2871fbd91e652493a1766a47ef9f3c0595a283979a0cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingFilterCriteriaFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f501d48e5274adca1b7fcc603ac574a40c9a2dc8779689d6a1928974b68423a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__214652ec66555668b8bc5a979d45f9b2df52dc741b0765be58a0a239c663407a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64bf7f51af4a6978326e1aef1f95a6ad437ee14d4282c65c5b4dfb403739cda(
    value: typing.Optional[typing.Union[LambdaEventSourceMappingFilterCriteriaFilter, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf90e99296b6b0836dcd21cfedbd96cba0de8817c28b86fe45e5a81d3e9a4a52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fed9484a7553309c5a38b3ad891206d0ade480e84f9da82d9b030b886c21c93(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingFilterCriteriaFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1a02ab1e31c47b64c90e7cc7060e5f525711e57eba08e73753d9d15400fd741(
    value: typing.Optional[LambdaEventSourceMappingFilterCriteria],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f718d9f0c61db275ede06a61fe886dc168521189524bb83565d3da9c025c48e(
    *,
    endpoints: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbba2764bd988b4a816a46955500ec7a6c7dceed523e5314b7a48586e45340a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a076c1f8baac0f9ff5ba3dd8e69a900b577e74be7cfbec5ccc8f488fec1896c6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca82dd2b84242acad82c6883bebd93cea9346581689399f883727e4d44589776(
    value: typing.Optional[LambdaEventSourceMappingSelfManagedEventSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552f5accfcb9ea14c92bd78af097762e0ae1236cab5d2bb2ad88f563414bb309(
    *,
    consumer_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6356265f44a9462aff0a0bd5cf3e3da9ce2261f824f5f7b98d1fb4c80bbd090(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8e960270f5884b70648a3fbbbed56d1d11a13b177ec49f5c07bbf4b60b5495b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f35651559ea6accdc41caeff6ea91750ce0e9c62392d3992ac409086f2b8948(
    value: typing.Optional[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f749b47122b9bf8627a73e0d68e5a12071defd185889c6b9ee5024d6d0c56ea(
    *,
    type: builtins.str,
    uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8985b422c6d88695b44d933886ca9236f32f376829c246b1e7e4f8bd9fb0c6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3117b2e2f4b8c616c5d264161ea71f205c9701d6f1194bd911b60fc3e2532446(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09481dd8d0fb3245e87c3a245d04ad5551bc07042668b540b4d99249ddd29acc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94cf9718d242637fcc2263e8bd7fa6113232cd77ad3331c35acbbb244616b686(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf65c356a4bc87ab20d9a5752ecf6033bfdca646bf56efe47922d4fdfe27562e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__765cea81bf496ba1278e49377193052e975811a5f5751600a86f4ce142ee14c3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSourceAccessConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c89a4840a4763b1e73653623afb28787f2069fae0f8c4db3f43215aec63322(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebeffa72cc48a3625370697e7bd01c77b8bec050369175e629c752caed6cd786(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70eb273fc598e283b663c20be432cb6f94be8b6d5caf501372dd5a423329b91e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0313df950f6ce97798b4c90f261a746c6902efc9988912c017a7ce589b97e7(
    value: typing.Optional[typing.Union[LambdaEventSourceMappingSourceAccessConfiguration, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
