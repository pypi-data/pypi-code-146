'''
# AWS::KafkaConnect Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_kafkaconnect as kafkaconnect
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for KafkaConnect construct libraries](https://constructs.dev/search?q=kafkaconnect)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::KafkaConnect resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_KafkaConnect.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::KafkaConnect](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_KafkaConnect.html).

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

from ._jsii import *

import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnConnector(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector",
):
    '''A CloudFormation ``AWS::KafkaConnect::Connector``.

    Creates a connector using the specified properties.

    :cloudformationResource: AWS::KafkaConnect::Connector
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_kafkaconnect as kafkaconnect
        
        cfn_connector = kafkaconnect.CfnConnector(self, "MyCfnConnector",
            capacity=kafkaconnect.CfnConnector.CapacityProperty(
                auto_scaling=kafkaconnect.CfnConnector.AutoScalingProperty(
                    max_worker_count=123,
                    mcu_count=123,
                    min_worker_count=123,
                    scale_in_policy=kafkaconnect.CfnConnector.ScaleInPolicyProperty(
                        cpu_utilization_percentage=123
                    ),
                    scale_out_policy=kafkaconnect.CfnConnector.ScaleOutPolicyProperty(
                        cpu_utilization_percentage=123
                    )
                ),
                provisioned_capacity=kafkaconnect.CfnConnector.ProvisionedCapacityProperty(
                    worker_count=123,
        
                    # the properties below are optional
                    mcu_count=123
                )
            ),
            connector_configuration={
                "connector_configuration_key": "connectorConfiguration"
            },
            connector_name="connectorName",
            kafka_cluster=kafkaconnect.CfnConnector.KafkaClusterProperty(
                apache_kafka_cluster=kafkaconnect.CfnConnector.ApacheKafkaClusterProperty(
                    bootstrap_servers="bootstrapServers",
                    vpc=kafkaconnect.CfnConnector.VpcProperty(
                        security_groups=["securityGroups"],
                        subnets=["subnets"]
                    )
                )
            ),
            kafka_cluster_client_authentication=kafkaconnect.CfnConnector.KafkaClusterClientAuthenticationProperty(
                authentication_type="authenticationType"
            ),
            kafka_cluster_encryption_in_transit=kafkaconnect.CfnConnector.KafkaClusterEncryptionInTransitProperty(
                encryption_type="encryptionType"
            ),
            kafka_connect_version="kafkaConnectVersion",
            plugins=[kafkaconnect.CfnConnector.PluginProperty(
                custom_plugin=kafkaconnect.CfnConnector.CustomPluginProperty(
                    custom_plugin_arn="customPluginArn",
                    revision=123
                )
            )],
            service_execution_role_arn="serviceExecutionRoleArn",
        
            # the properties below are optional
            connector_description="connectorDescription",
            log_delivery=kafkaconnect.CfnConnector.LogDeliveryProperty(
                worker_log_delivery=kafkaconnect.CfnConnector.WorkerLogDeliveryProperty(
                    cloud_watch_logs=kafkaconnect.CfnConnector.CloudWatchLogsLogDeliveryProperty(
                        enabled=False,
        
                        # the properties below are optional
                        log_group="logGroup"
                    ),
                    firehose=kafkaconnect.CfnConnector.FirehoseLogDeliveryProperty(
                        enabled=False,
        
                        # the properties below are optional
                        delivery_stream="deliveryStream"
                    ),
                    s3=kafkaconnect.CfnConnector.S3LogDeliveryProperty(
                        enabled=False,
        
                        # the properties below are optional
                        bucket="bucket",
                        prefix="prefix"
                    )
                )
            ),
            worker_configuration=kafkaconnect.CfnConnector.WorkerConfigurationProperty(
                revision=123,
                worker_configuration_arn="workerConfigurationArn"
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        capacity: typing.Union[typing.Union["CfnConnector.CapacityProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        connector_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]],
        connector_name: builtins.str,
        kafka_cluster: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConnector.KafkaClusterProperty", typing.Dict[builtins.str, typing.Any]]],
        kafka_cluster_client_authentication: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConnector.KafkaClusterClientAuthenticationProperty", typing.Dict[builtins.str, typing.Any]]],
        kafka_cluster_encryption_in_transit: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConnector.KafkaClusterEncryptionInTransitProperty", typing.Dict[builtins.str, typing.Any]]],
        kafka_connect_version: builtins.str,
        plugins: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConnector.PluginProperty", typing.Dict[builtins.str, typing.Any]]]]],
        service_execution_role_arn: builtins.str,
        connector_description: typing.Optional[builtins.str] = None,
        log_delivery: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConnector.LogDeliveryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        worker_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConnector.WorkerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::KafkaConnect::Connector``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param capacity: The connector's compute capacity settings.
        :param connector_configuration: The configuration of the connector.
        :param connector_name: The name of the connector.
        :param kafka_cluster: The details of the Apache Kafka cluster to which the connector is connected.
        :param kafka_cluster_client_authentication: The type of client authentication used to connect to the Apache Kafka cluster. The value is NONE when no client authentication is used.
        :param kafka_cluster_encryption_in_transit: Details of encryption in transit to the Apache Kafka cluster.
        :param kafka_connect_version: The version of Kafka Connect. It has to be compatible with both the Apache Kafka cluster's version and the plugins.
        :param plugins: Specifies which plugin to use for the connector. You must specify a single-element list. Amazon MSK Connect does not currently support specifying multiple plugins.
        :param service_execution_role_arn: The Amazon Resource Name (ARN) of the IAM role used by the connector to access Amazon Web Services resources.
        :param connector_description: The description of the connector.
        :param log_delivery: The settings for delivering connector logs to Amazon CloudWatch Logs.
        :param worker_configuration: The worker configurations that are in use with the connector.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e1edb3d5529b80129194a27d0464190749f3cb401d20fb34ec9206ff4276b8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnConnectorProps(
            capacity=capacity,
            connector_configuration=connector_configuration,
            connector_name=connector_name,
            kafka_cluster=kafka_cluster,
            kafka_cluster_client_authentication=kafka_cluster_client_authentication,
            kafka_cluster_encryption_in_transit=kafka_cluster_encryption_in_transit,
            kafka_connect_version=kafka_connect_version,
            plugins=plugins,
            service_execution_role_arn=service_execution_role_arn,
            connector_description=connector_description,
            log_delivery=log_delivery,
            worker_configuration=worker_configuration,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7ce2cc9abbc11e456a6e8f5856bb709af51a33c182c203c517e0f5485569e84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5392fcba97b4da8c28b76df652c11cad7f8ba1a405a7493c78b1d537b5612316)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrConnectorArn")
    def attr_connector_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the newly created connector.

        :cloudformationAttribute: ConnectorArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConnectorArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="capacity")
    def capacity(
        self,
    ) -> typing.Union["CfnConnector.CapacityProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''The connector's compute capacity settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-capacity
        '''
        return typing.cast(typing.Union["CfnConnector.CapacityProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "capacity"))

    @capacity.setter
    def capacity(
        self,
        value: typing.Union["CfnConnector.CapacityProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f9eaf3d4c43df956ba6290f0ac0ddbac1e813bb929ede281fec5c5228cc3131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacity", value)

    @builtins.property
    @jsii.member(jsii_name="connectorConfiguration")
    def connector_configuration(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]:
        '''The configuration of the connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-connectorconfiguration
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "connectorConfiguration"))

    @connector_configuration.setter
    def connector_configuration(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daba67fa009e2e07571999ae9fe0490330127df3d621f4d3212bf1596fcbfa11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="connectorName")
    def connector_name(self) -> builtins.str:
        '''The name of the connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-connectorname
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectorName"))

    @connector_name.setter
    def connector_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__987f60634306e38d5192d4b0aa0817566f1942a4b9b1792c54c9605c27605865)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorName", value)

    @builtins.property
    @jsii.member(jsii_name="kafkaCluster")
    def kafka_cluster(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.KafkaClusterProperty"]:
        '''The details of the Apache Kafka cluster to which the connector is connected.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-kafkacluster
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.KafkaClusterProperty"], jsii.get(self, "kafkaCluster"))

    @kafka_cluster.setter
    def kafka_cluster(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.KafkaClusterProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2904f48bec9068c1558ab8d57318e02c37f077cc732b7bf70fcc80a602c46c57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kafkaCluster", value)

    @builtins.property
    @jsii.member(jsii_name="kafkaClusterClientAuthentication")
    def kafka_cluster_client_authentication(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.KafkaClusterClientAuthenticationProperty"]:
        '''The type of client authentication used to connect to the Apache Kafka cluster.

        The value is NONE when no client authentication is used.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-kafkaclusterclientauthentication
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.KafkaClusterClientAuthenticationProperty"], jsii.get(self, "kafkaClusterClientAuthentication"))

    @kafka_cluster_client_authentication.setter
    def kafka_cluster_client_authentication(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.KafkaClusterClientAuthenticationProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5159d4ee8b022ca5c92de664ab7af238a2808dd87d9235ad451b1afeb196ed74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kafkaClusterClientAuthentication", value)

    @builtins.property
    @jsii.member(jsii_name="kafkaClusterEncryptionInTransit")
    def kafka_cluster_encryption_in_transit(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.KafkaClusterEncryptionInTransitProperty"]:
        '''Details of encryption in transit to the Apache Kafka cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-kafkaclusterencryptionintransit
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.KafkaClusterEncryptionInTransitProperty"], jsii.get(self, "kafkaClusterEncryptionInTransit"))

    @kafka_cluster_encryption_in_transit.setter
    def kafka_cluster_encryption_in_transit(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.KafkaClusterEncryptionInTransitProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b4016b0d04d557f24748b4c1642a276edc4c4bb3a4e97340b93b991b8a37675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kafkaClusterEncryptionInTransit", value)

    @builtins.property
    @jsii.member(jsii_name="kafkaConnectVersion")
    def kafka_connect_version(self) -> builtins.str:
        '''The version of Kafka Connect.

        It has to be compatible with both the Apache Kafka cluster's version and the plugins.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-kafkaconnectversion
        '''
        return typing.cast(builtins.str, jsii.get(self, "kafkaConnectVersion"))

    @kafka_connect_version.setter
    def kafka_connect_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc7e20c8942f254bf13d02aa91599ee5d47b83e5b21bd79b0eb855877320742c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kafkaConnectVersion", value)

    @builtins.property
    @jsii.member(jsii_name="plugins")
    def plugins(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.PluginProperty"]]]:
        '''Specifies which plugin to use for the connector.

        You must specify a single-element list. Amazon MSK Connect does not currently support specifying multiple plugins.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-plugins
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.PluginProperty"]]], jsii.get(self, "plugins"))

    @plugins.setter
    def plugins(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.PluginProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f6eefbf825b07358e48dd33a2b95b41130308c6f22090da7835d5501166f4ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "plugins", value)

    @builtins.property
    @jsii.member(jsii_name="serviceExecutionRoleArn")
    def service_execution_role_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the IAM role used by the connector to access Amazon Web Services resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-serviceexecutionrolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceExecutionRoleArn"))

    @service_execution_role_arn.setter
    def service_execution_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3acab356d74a0880b17835cfd16ca00af6db7da1839496d36a23f0db5ba41dc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceExecutionRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="connectorDescription")
    def connector_description(self) -> typing.Optional[builtins.str]:
        '''The description of the connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-connectordescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorDescription"))

    @connector_description.setter
    def connector_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17a8f576cdc665b2bd66368c3871685a8eab74f0da2fe6545e29cddab7ddf705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorDescription", value)

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def log_delivery(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.LogDeliveryProperty"]]:
        '''The settings for delivering connector logs to Amazon CloudWatch Logs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-logdelivery
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.LogDeliveryProperty"]], jsii.get(self, "logDelivery"))

    @log_delivery.setter
    def log_delivery(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.LogDeliveryProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__689e8652a48b7b08dd0afc54a28258d7fb4b674388bd6069aad65c8882c29b8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logDelivery", value)

    @builtins.property
    @jsii.member(jsii_name="workerConfiguration")
    def worker_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.WorkerConfigurationProperty"]]:
        '''The worker configurations that are in use with the connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-workerconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.WorkerConfigurationProperty"]], jsii.get(self, "workerConfiguration"))

    @worker_configuration.setter
    def worker_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.WorkerConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50b25953311169416850d5d9bac90b75c6abe6ef29e2ff6c007e5ae32e0e6516)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.ApacheKafkaClusterProperty",
        jsii_struct_bases=[],
        name_mapping={"bootstrap_servers": "bootstrapServers", "vpc": "vpc"},
    )
    class ApacheKafkaClusterProperty:
        def __init__(
            self,
            *,
            bootstrap_servers: builtins.str,
            vpc: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConnector.VpcProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''The details of the Apache Kafka cluster to which the connector is connected.

            :param bootstrap_servers: The bootstrap servers of the cluster.
            :param vpc: Details of an Amazon VPC which has network connectivity to the Apache Kafka cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-apachekafkacluster.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                apache_kafka_cluster_property = kafkaconnect.CfnConnector.ApacheKafkaClusterProperty(
                    bootstrap_servers="bootstrapServers",
                    vpc=kafkaconnect.CfnConnector.VpcProperty(
                        security_groups=["securityGroups"],
                        subnets=["subnets"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5dabe30b088bb7bd2ee12c8005a9559c5d39597f148ff9e88801524bffe4fa29)
                check_type(argname="argument bootstrap_servers", value=bootstrap_servers, expected_type=type_hints["bootstrap_servers"])
                check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bootstrap_servers": bootstrap_servers,
                "vpc": vpc,
            }

        @builtins.property
        def bootstrap_servers(self) -> builtins.str:
            '''The bootstrap servers of the cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-apachekafkacluster.html#cfn-kafkaconnect-connector-apachekafkacluster-bootstrapservers
            '''
            result = self._values.get("bootstrap_servers")
            assert result is not None, "Required property 'bootstrap_servers' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def vpc(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.VpcProperty"]:
            '''Details of an Amazon VPC which has network connectivity to the Apache Kafka cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-apachekafkacluster.html#cfn-kafkaconnect-connector-apachekafkacluster-vpc
            '''
            result = self._values.get("vpc")
            assert result is not None, "Required property 'vpc' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.VpcProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApacheKafkaClusterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.AutoScalingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_worker_count": "maxWorkerCount",
            "mcu_count": "mcuCount",
            "min_worker_count": "minWorkerCount",
            "scale_in_policy": "scaleInPolicy",
            "scale_out_policy": "scaleOutPolicy",
        },
    )
    class AutoScalingProperty:
        def __init__(
            self,
            *,
            max_worker_count: jsii.Number,
            mcu_count: jsii.Number,
            min_worker_count: jsii.Number,
            scale_in_policy: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConnector.ScaleInPolicyProperty", typing.Dict[builtins.str, typing.Any]]],
            scale_out_policy: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConnector.ScaleOutPolicyProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Specifies how the connector scales.

            :param max_worker_count: The maximum number of workers allocated to the connector.
            :param mcu_count: The number of microcontroller units (MCUs) allocated to each connector worker. The valid values are 1,2,4,8.
            :param min_worker_count: The minimum number of workers allocated to the connector.
            :param scale_in_policy: The sacle-in policy for the connector.
            :param scale_out_policy: The sacle-out policy for the connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-autoscaling.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                auto_scaling_property = kafkaconnect.CfnConnector.AutoScalingProperty(
                    max_worker_count=123,
                    mcu_count=123,
                    min_worker_count=123,
                    scale_in_policy=kafkaconnect.CfnConnector.ScaleInPolicyProperty(
                        cpu_utilization_percentage=123
                    ),
                    scale_out_policy=kafkaconnect.CfnConnector.ScaleOutPolicyProperty(
                        cpu_utilization_percentage=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e9b94c0209a48b85ffeae598a4f7cfd9117260afc0f52a80b7a7a1877510ae0c)
                check_type(argname="argument max_worker_count", value=max_worker_count, expected_type=type_hints["max_worker_count"])
                check_type(argname="argument mcu_count", value=mcu_count, expected_type=type_hints["mcu_count"])
                check_type(argname="argument min_worker_count", value=min_worker_count, expected_type=type_hints["min_worker_count"])
                check_type(argname="argument scale_in_policy", value=scale_in_policy, expected_type=type_hints["scale_in_policy"])
                check_type(argname="argument scale_out_policy", value=scale_out_policy, expected_type=type_hints["scale_out_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "max_worker_count": max_worker_count,
                "mcu_count": mcu_count,
                "min_worker_count": min_worker_count,
                "scale_in_policy": scale_in_policy,
                "scale_out_policy": scale_out_policy,
            }

        @builtins.property
        def max_worker_count(self) -> jsii.Number:
            '''The maximum number of workers allocated to the connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-autoscaling.html#cfn-kafkaconnect-connector-autoscaling-maxworkercount
            '''
            result = self._values.get("max_worker_count")
            assert result is not None, "Required property 'max_worker_count' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def mcu_count(self) -> jsii.Number:
            '''The number of microcontroller units (MCUs) allocated to each connector worker.

            The valid values are 1,2,4,8.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-autoscaling.html#cfn-kafkaconnect-connector-autoscaling-mcucount
            '''
            result = self._values.get("mcu_count")
            assert result is not None, "Required property 'mcu_count' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def min_worker_count(self) -> jsii.Number:
            '''The minimum number of workers allocated to the connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-autoscaling.html#cfn-kafkaconnect-connector-autoscaling-minworkercount
            '''
            result = self._values.get("min_worker_count")
            assert result is not None, "Required property 'min_worker_count' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def scale_in_policy(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.ScaleInPolicyProperty"]:
            '''The sacle-in policy for the connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-autoscaling.html#cfn-kafkaconnect-connector-autoscaling-scaleinpolicy
            '''
            result = self._values.get("scale_in_policy")
            assert result is not None, "Required property 'scale_in_policy' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.ScaleInPolicyProperty"], result)

        @builtins.property
        def scale_out_policy(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.ScaleOutPolicyProperty"]:
            '''The sacle-out policy for the connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-autoscaling.html#cfn-kafkaconnect-connector-autoscaling-scaleoutpolicy
            '''
            result = self._values.get("scale_out_policy")
            assert result is not None, "Required property 'scale_out_policy' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.ScaleOutPolicyProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoScalingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.CapacityProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_scaling": "autoScaling",
            "provisioned_capacity": "provisionedCapacity",
        },
    )
    class CapacityProperty:
        def __init__(
            self,
            *,
            auto_scaling: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConnector.AutoScalingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            provisioned_capacity: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConnector.ProvisionedCapacityProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about the capacity of the connector, whether it is auto scaled or provisioned.

            :param auto_scaling: Information about the auto scaling parameters for the connector.
            :param provisioned_capacity: Details about a fixed capacity allocated to a connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-capacity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                capacity_property = kafkaconnect.CfnConnector.CapacityProperty(
                    auto_scaling=kafkaconnect.CfnConnector.AutoScalingProperty(
                        max_worker_count=123,
                        mcu_count=123,
                        min_worker_count=123,
                        scale_in_policy=kafkaconnect.CfnConnector.ScaleInPolicyProperty(
                            cpu_utilization_percentage=123
                        ),
                        scale_out_policy=kafkaconnect.CfnConnector.ScaleOutPolicyProperty(
                            cpu_utilization_percentage=123
                        )
                    ),
                    provisioned_capacity=kafkaconnect.CfnConnector.ProvisionedCapacityProperty(
                        worker_count=123,
                
                        # the properties below are optional
                        mcu_count=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ac00b85fd7dd7a7b89fc29c5176ec6b10c5fe9aeff1afe746b2329ac11edfa7e)
                check_type(argname="argument auto_scaling", value=auto_scaling, expected_type=type_hints["auto_scaling"])
                check_type(argname="argument provisioned_capacity", value=provisioned_capacity, expected_type=type_hints["provisioned_capacity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_scaling is not None:
                self._values["auto_scaling"] = auto_scaling
            if provisioned_capacity is not None:
                self._values["provisioned_capacity"] = provisioned_capacity

        @builtins.property
        def auto_scaling(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.AutoScalingProperty"]]:
            '''Information about the auto scaling parameters for the connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-capacity.html#cfn-kafkaconnect-connector-capacity-autoscaling
            '''
            result = self._values.get("auto_scaling")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.AutoScalingProperty"]], result)

        @builtins.property
        def provisioned_capacity(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.ProvisionedCapacityProperty"]]:
            '''Details about a fixed capacity allocated to a connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-capacity.html#cfn-kafkaconnect-connector-capacity-provisionedcapacity
            '''
            result = self._values.get("provisioned_capacity")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.ProvisionedCapacityProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.CloudWatchLogsLogDeliveryProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "log_group": "logGroup"},
    )
    class CloudWatchLogsLogDeliveryProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
            log_group: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The settings for delivering connector logs to Amazon CloudWatch Logs.

            :param enabled: Whether log delivery to Amazon CloudWatch Logs is enabled.
            :param log_group: The name of the CloudWatch log group that is the destination for log delivery.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-cloudwatchlogslogdelivery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                cloud_watch_logs_log_delivery_property = kafkaconnect.CfnConnector.CloudWatchLogsLogDeliveryProperty(
                    enabled=False,
                
                    # the properties below are optional
                    log_group="logGroup"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9806eda86391fb5101bcd9cf55d390ca7e98533215522cef1b97fc570fa0a2c3)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "enabled": enabled,
            }
            if log_group is not None:
                self._values["log_group"] = log_group

        @builtins.property
        def enabled(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''Whether log delivery to Amazon CloudWatch Logs is enabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-cloudwatchlogslogdelivery.html#cfn-kafkaconnect-connector-cloudwatchlogslogdelivery-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        @builtins.property
        def log_group(self) -> typing.Optional[builtins.str]:
            '''The name of the CloudWatch log group that is the destination for log delivery.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-cloudwatchlogslogdelivery.html#cfn-kafkaconnect-connector-cloudwatchlogslogdelivery-loggroup
            '''
            result = self._values.get("log_group")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsLogDeliveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.CustomPluginProperty",
        jsii_struct_bases=[],
        name_mapping={"custom_plugin_arn": "customPluginArn", "revision": "revision"},
    )
    class CustomPluginProperty:
        def __init__(
            self,
            *,
            custom_plugin_arn: builtins.str,
            revision: jsii.Number,
        ) -> None:
            '''A plugin is an AWS resource that contains the code that defines a connector's logic.

            :param custom_plugin_arn: The Amazon Resource Name (ARN) of the custom plugin.
            :param revision: The revision of the custom plugin.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-customplugin.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                custom_plugin_property = kafkaconnect.CfnConnector.CustomPluginProperty(
                    custom_plugin_arn="customPluginArn",
                    revision=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7b83b2d8c6c84901292e0f1b433a485c3bfe24f4665eb0b646fad5803510dd88)
                check_type(argname="argument custom_plugin_arn", value=custom_plugin_arn, expected_type=type_hints["custom_plugin_arn"])
                check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "custom_plugin_arn": custom_plugin_arn,
                "revision": revision,
            }

        @builtins.property
        def custom_plugin_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the custom plugin.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-customplugin.html#cfn-kafkaconnect-connector-customplugin-custompluginarn
            '''
            result = self._values.get("custom_plugin_arn")
            assert result is not None, "Required property 'custom_plugin_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def revision(self) -> jsii.Number:
            '''The revision of the custom plugin.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-customplugin.html#cfn-kafkaconnect-connector-customplugin-revision
            '''
            result = self._values.get("revision")
            assert result is not None, "Required property 'revision' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomPluginProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.FirehoseLogDeliveryProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "delivery_stream": "deliveryStream"},
    )
    class FirehoseLogDeliveryProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
            delivery_stream: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The settings for delivering logs to Amazon Kinesis Data Firehose.

            :param enabled: Specifies whether connector logs get delivered to Amazon Kinesis Data Firehose.
            :param delivery_stream: The name of the Kinesis Data Firehose delivery stream that is the destination for log delivery.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-firehoselogdelivery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                firehose_log_delivery_property = kafkaconnect.CfnConnector.FirehoseLogDeliveryProperty(
                    enabled=False,
                
                    # the properties below are optional
                    delivery_stream="deliveryStream"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d0e82c6f82c80af96dc1291c65337690e076283bed1f50d22122d8eebb899286)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "enabled": enabled,
            }
            if delivery_stream is not None:
                self._values["delivery_stream"] = delivery_stream

        @builtins.property
        def enabled(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''Specifies whether connector logs get delivered to Amazon Kinesis Data Firehose.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-firehoselogdelivery.html#cfn-kafkaconnect-connector-firehoselogdelivery-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        @builtins.property
        def delivery_stream(self) -> typing.Optional[builtins.str]:
            '''The name of the Kinesis Data Firehose delivery stream that is the destination for log delivery.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-firehoselogdelivery.html#cfn-kafkaconnect-connector-firehoselogdelivery-deliverystream
            '''
            result = self._values.get("delivery_stream")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FirehoseLogDeliveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.KafkaClusterClientAuthenticationProperty",
        jsii_struct_bases=[],
        name_mapping={"authentication_type": "authenticationType"},
    )
    class KafkaClusterClientAuthenticationProperty:
        def __init__(self, *, authentication_type: builtins.str) -> None:
            '''The client authentication information used in order to authenticate with the Apache Kafka cluster.

            :param authentication_type: The type of client authentication used to connect to the Apache Kafka cluster. Value NONE means that no client authentication is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-kafkaclusterclientauthentication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                kafka_cluster_client_authentication_property = kafkaconnect.CfnConnector.KafkaClusterClientAuthenticationProperty(
                    authentication_type="authenticationType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e507e39a6a7602c0cdfaaa469e0435270c5f5504f7599f6253d5c5277fccb13c)
                check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "authentication_type": authentication_type,
            }

        @builtins.property
        def authentication_type(self) -> builtins.str:
            '''The type of client authentication used to connect to the Apache Kafka cluster.

            Value NONE means that no client authentication is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-kafkaclusterclientauthentication.html#cfn-kafkaconnect-connector-kafkaclusterclientauthentication-authenticationtype
            '''
            result = self._values.get("authentication_type")
            assert result is not None, "Required property 'authentication_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KafkaClusterClientAuthenticationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.KafkaClusterEncryptionInTransitProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption_type": "encryptionType"},
    )
    class KafkaClusterEncryptionInTransitProperty:
        def __init__(self, *, encryption_type: builtins.str) -> None:
            '''Details of encryption in transit to the Apache Kafka cluster.

            :param encryption_type: The type of encryption in transit to the Apache Kafka cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-kafkaclusterencryptionintransit.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                kafka_cluster_encryption_in_transit_property = kafkaconnect.CfnConnector.KafkaClusterEncryptionInTransitProperty(
                    encryption_type="encryptionType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a682e6ce9f496be129502b1758d9886e0cf64dec39989ccc16abd8e8008ed915)
                check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "encryption_type": encryption_type,
            }

        @builtins.property
        def encryption_type(self) -> builtins.str:
            '''The type of encryption in transit to the Apache Kafka cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-kafkaclusterencryptionintransit.html#cfn-kafkaconnect-connector-kafkaclusterencryptionintransit-encryptiontype
            '''
            result = self._values.get("encryption_type")
            assert result is not None, "Required property 'encryption_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KafkaClusterEncryptionInTransitProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.KafkaClusterProperty",
        jsii_struct_bases=[],
        name_mapping={"apache_kafka_cluster": "apacheKafkaCluster"},
    )
    class KafkaClusterProperty:
        def __init__(
            self,
            *,
            apache_kafka_cluster: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConnector.ApacheKafkaClusterProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''The details of the Apache Kafka cluster to which the connector is connected.

            :param apache_kafka_cluster: The Apache Kafka cluster to which the connector is connected.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-kafkacluster.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                kafka_cluster_property = kafkaconnect.CfnConnector.KafkaClusterProperty(
                    apache_kafka_cluster=kafkaconnect.CfnConnector.ApacheKafkaClusterProperty(
                        bootstrap_servers="bootstrapServers",
                        vpc=kafkaconnect.CfnConnector.VpcProperty(
                            security_groups=["securityGroups"],
                            subnets=["subnets"]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__90f4cbb443ac141daa7834dd8f90b9a289eda7b5af4911d65a2893401e2d01cb)
                check_type(argname="argument apache_kafka_cluster", value=apache_kafka_cluster, expected_type=type_hints["apache_kafka_cluster"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "apache_kafka_cluster": apache_kafka_cluster,
            }

        @builtins.property
        def apache_kafka_cluster(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.ApacheKafkaClusterProperty"]:
            '''The Apache Kafka cluster to which the connector is connected.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-kafkacluster.html#cfn-kafkaconnect-connector-kafkacluster-apachekafkacluster
            '''
            result = self._values.get("apache_kafka_cluster")
            assert result is not None, "Required property 'apache_kafka_cluster' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.ApacheKafkaClusterProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KafkaClusterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.LogDeliveryProperty",
        jsii_struct_bases=[],
        name_mapping={"worker_log_delivery": "workerLogDelivery"},
    )
    class LogDeliveryProperty:
        def __init__(
            self,
            *,
            worker_log_delivery: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConnector.WorkerLogDeliveryProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Details about log delivery.

            :param worker_log_delivery: The workers can send worker logs to different destination types. This configuration specifies the details of these destinations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-logdelivery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                log_delivery_property = kafkaconnect.CfnConnector.LogDeliveryProperty(
                    worker_log_delivery=kafkaconnect.CfnConnector.WorkerLogDeliveryProperty(
                        cloud_watch_logs=kafkaconnect.CfnConnector.CloudWatchLogsLogDeliveryProperty(
                            enabled=False,
                
                            # the properties below are optional
                            log_group="logGroup"
                        ),
                        firehose=kafkaconnect.CfnConnector.FirehoseLogDeliveryProperty(
                            enabled=False,
                
                            # the properties below are optional
                            delivery_stream="deliveryStream"
                        ),
                        s3=kafkaconnect.CfnConnector.S3LogDeliveryProperty(
                            enabled=False,
                
                            # the properties below are optional
                            bucket="bucket",
                            prefix="prefix"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__09708796cb367b27269ef7238c058470df510c6dc85bb4707c0284b18563e5f5)
                check_type(argname="argument worker_log_delivery", value=worker_log_delivery, expected_type=type_hints["worker_log_delivery"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "worker_log_delivery": worker_log_delivery,
            }

        @builtins.property
        def worker_log_delivery(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.WorkerLogDeliveryProperty"]:
            '''The workers can send worker logs to different destination types.

            This configuration specifies the details of these destinations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-logdelivery.html#cfn-kafkaconnect-connector-logdelivery-workerlogdelivery
            '''
            result = self._values.get("worker_log_delivery")
            assert result is not None, "Required property 'worker_log_delivery' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.WorkerLogDeliveryProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogDeliveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.PluginProperty",
        jsii_struct_bases=[],
        name_mapping={"custom_plugin": "customPlugin"},
    )
    class PluginProperty:
        def __init__(
            self,
            *,
            custom_plugin: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConnector.CustomPluginProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''A plugin is an AWS resource that contains the code that defines your connector logic.

            :param custom_plugin: Details about a custom plugin.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-plugin.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                plugin_property = kafkaconnect.CfnConnector.PluginProperty(
                    custom_plugin=kafkaconnect.CfnConnector.CustomPluginProperty(
                        custom_plugin_arn="customPluginArn",
                        revision=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cdf3ff7d08d60292f7cc3f7fbb5a010fdb4d130229365a90f2d6ad5cab08d93b)
                check_type(argname="argument custom_plugin", value=custom_plugin, expected_type=type_hints["custom_plugin"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "custom_plugin": custom_plugin,
            }

        @builtins.property
        def custom_plugin(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.CustomPluginProperty"]:
            '''Details about a custom plugin.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-plugin.html#cfn-kafkaconnect-connector-plugin-customplugin
            '''
            result = self._values.get("custom_plugin")
            assert result is not None, "Required property 'custom_plugin' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.CustomPluginProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PluginProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.ProvisionedCapacityProperty",
        jsii_struct_bases=[],
        name_mapping={"worker_count": "workerCount", "mcu_count": "mcuCount"},
    )
    class ProvisionedCapacityProperty:
        def __init__(
            self,
            *,
            worker_count: jsii.Number,
            mcu_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Details about a connector's provisioned capacity.

            :param worker_count: The number of workers that are allocated to the connector.
            :param mcu_count: The number of microcontroller units (MCUs) allocated to each connector worker. The valid values are 1,2,4,8.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-provisionedcapacity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                provisioned_capacity_property = kafkaconnect.CfnConnector.ProvisionedCapacityProperty(
                    worker_count=123,
                
                    # the properties below are optional
                    mcu_count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6dd251940e0a2c765a29f41c670ed29af29e795a7aec06a1f44698681b4301bb)
                check_type(argname="argument worker_count", value=worker_count, expected_type=type_hints["worker_count"])
                check_type(argname="argument mcu_count", value=mcu_count, expected_type=type_hints["mcu_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "worker_count": worker_count,
            }
            if mcu_count is not None:
                self._values["mcu_count"] = mcu_count

        @builtins.property
        def worker_count(self) -> jsii.Number:
            '''The number of workers that are allocated to the connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-provisionedcapacity.html#cfn-kafkaconnect-connector-provisionedcapacity-workercount
            '''
            result = self._values.get("worker_count")
            assert result is not None, "Required property 'worker_count' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def mcu_count(self) -> typing.Optional[jsii.Number]:
            '''The number of microcontroller units (MCUs) allocated to each connector worker.

            The valid values are 1,2,4,8.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-provisionedcapacity.html#cfn-kafkaconnect-connector-provisionedcapacity-mcucount
            '''
            result = self._values.get("mcu_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisionedCapacityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.S3LogDeliveryProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "bucket": "bucket", "prefix": "prefix"},
    )
    class S3LogDeliveryProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
            bucket: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Details about delivering logs to Amazon S3.

            :param enabled: Specifies whether connector logs get sent to the specified Amazon S3 destination.
            :param bucket: The name of the S3 bucket that is the destination for log delivery.
            :param prefix: The S3 prefix that is the destination for log delivery.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-s3logdelivery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                s3_log_delivery_property = kafkaconnect.CfnConnector.S3LogDeliveryProperty(
                    enabled=False,
                
                    # the properties below are optional
                    bucket="bucket",
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f88f4ea961fff582feea3c86961cebd1fd7d2b9cb355c98f50a1481fe592d58a)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "enabled": enabled,
            }
            if bucket is not None:
                self._values["bucket"] = bucket
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def enabled(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''Specifies whether connector logs get sent to the specified Amazon S3 destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-s3logdelivery.html#cfn-kafkaconnect-connector-s3logdelivery-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The name of the S3 bucket that is the destination for log delivery.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-s3logdelivery.html#cfn-kafkaconnect-connector-s3logdelivery-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''The S3 prefix that is the destination for log delivery.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-s3logdelivery.html#cfn-kafkaconnect-connector-s3logdelivery-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LogDeliveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.ScaleInPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"cpu_utilization_percentage": "cpuUtilizationPercentage"},
    )
    class ScaleInPolicyProperty:
        def __init__(self, *, cpu_utilization_percentage: jsii.Number) -> None:
            '''The scale-in policy for the connector.

            :param cpu_utilization_percentage: Specifies the CPU utilization percentage threshold at which you want connector scale in to be triggered.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-scaleinpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                scale_in_policy_property = kafkaconnect.CfnConnector.ScaleInPolicyProperty(
                    cpu_utilization_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cbe6ff153c08ad549e5a45bd5a0438c16678d9eb9bd10465dd398e19f6f6a954)
                check_type(argname="argument cpu_utilization_percentage", value=cpu_utilization_percentage, expected_type=type_hints["cpu_utilization_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cpu_utilization_percentage": cpu_utilization_percentage,
            }

        @builtins.property
        def cpu_utilization_percentage(self) -> jsii.Number:
            '''Specifies the CPU utilization percentage threshold at which you want connector scale in to be triggered.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-scaleinpolicy.html#cfn-kafkaconnect-connector-scaleinpolicy-cpuutilizationpercentage
            '''
            result = self._values.get("cpu_utilization_percentage")
            assert result is not None, "Required property 'cpu_utilization_percentage' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScaleInPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.ScaleOutPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"cpu_utilization_percentage": "cpuUtilizationPercentage"},
    )
    class ScaleOutPolicyProperty:
        def __init__(self, *, cpu_utilization_percentage: jsii.Number) -> None:
            '''The scale-out policy for the connector.

            :param cpu_utilization_percentage: The CPU utilization percentage threshold at which you want connector scale out to be triggered.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-scaleoutpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                scale_out_policy_property = kafkaconnect.CfnConnector.ScaleOutPolicyProperty(
                    cpu_utilization_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__24073addbe78614f0277a915f96ad75aa9eba698dba47fba48923e30282cc2ea)
                check_type(argname="argument cpu_utilization_percentage", value=cpu_utilization_percentage, expected_type=type_hints["cpu_utilization_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cpu_utilization_percentage": cpu_utilization_percentage,
            }

        @builtins.property
        def cpu_utilization_percentage(self) -> jsii.Number:
            '''The CPU utilization percentage threshold at which you want connector scale out to be triggered.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-scaleoutpolicy.html#cfn-kafkaconnect-connector-scaleoutpolicy-cpuutilizationpercentage
            '''
            result = self._values.get("cpu_utilization_percentage")
            assert result is not None, "Required property 'cpu_utilization_percentage' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScaleOutPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.VpcProperty",
        jsii_struct_bases=[],
        name_mapping={"security_groups": "securityGroups", "subnets": "subnets"},
    )
    class VpcProperty:
        def __init__(
            self,
            *,
            security_groups: typing.Sequence[builtins.str],
            subnets: typing.Sequence[builtins.str],
        ) -> None:
            '''Information about the VPC in which the connector resides.

            :param security_groups: The security groups for the connector.
            :param subnets: The subnets for the connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-vpc.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                vpc_property = kafkaconnect.CfnConnector.VpcProperty(
                    security_groups=["securityGroups"],
                    subnets=["subnets"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4bf3a3a2e13475a55e453fcf8dda8b6622052bcf1cc91884fb3cb093038cdc60)
                check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
                check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "security_groups": security_groups,
                "subnets": subnets,
            }

        @builtins.property
        def security_groups(self) -> typing.List[builtins.str]:
            '''The security groups for the connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-vpc.html#cfn-kafkaconnect-connector-vpc-securitygroups
            '''
            result = self._values.get("security_groups")
            assert result is not None, "Required property 'security_groups' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def subnets(self) -> typing.List[builtins.str]:
            '''The subnets for the connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-vpc.html#cfn-kafkaconnect-connector-vpc-subnets
            '''
            result = self._values.get("subnets")
            assert result is not None, "Required property 'subnets' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.WorkerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "revision": "revision",
            "worker_configuration_arn": "workerConfigurationArn",
        },
    )
    class WorkerConfigurationProperty:
        def __init__(
            self,
            *,
            revision: jsii.Number,
            worker_configuration_arn: builtins.str,
        ) -> None:
            '''The configuration of the workers, which are the processes that run the connector logic.

            :param revision: The revision of the worker configuration.
            :param worker_configuration_arn: The Amazon Resource Name (ARN) of the worker configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-workerconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                worker_configuration_property = kafkaconnect.CfnConnector.WorkerConfigurationProperty(
                    revision=123,
                    worker_configuration_arn="workerConfigurationArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__187013179663794250fadab97ae34febfcb6f0cddf82b5af3c96e0383b284e2f)
                check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
                check_type(argname="argument worker_configuration_arn", value=worker_configuration_arn, expected_type=type_hints["worker_configuration_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "revision": revision,
                "worker_configuration_arn": worker_configuration_arn,
            }

        @builtins.property
        def revision(self) -> jsii.Number:
            '''The revision of the worker configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-workerconfiguration.html#cfn-kafkaconnect-connector-workerconfiguration-revision
            '''
            result = self._values.get("revision")
            assert result is not None, "Required property 'revision' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def worker_configuration_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the worker configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-workerconfiguration.html#cfn-kafkaconnect-connector-workerconfiguration-workerconfigurationarn
            '''
            result = self._values.get("worker_configuration_arn")
            assert result is not None, "Required property 'worker_configuration_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.WorkerLogDeliveryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logs": "cloudWatchLogs",
            "firehose": "firehose",
            "s3": "s3",
        },
    )
    class WorkerLogDeliveryProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConnector.CloudWatchLogsLogDeliveryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            firehose: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConnector.FirehoseLogDeliveryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConnector.S3LogDeliveryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Workers can send worker logs to different destination types.

            This configuration specifies the details of these destinations.

            :param cloud_watch_logs: Details about delivering logs to Amazon CloudWatch Logs.
            :param firehose: Details about delivering logs to Amazon Kinesis Data Firehose.
            :param s3: Details about delivering logs to Amazon S3.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-workerlogdelivery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                worker_log_delivery_property = kafkaconnect.CfnConnector.WorkerLogDeliveryProperty(
                    cloud_watch_logs=kafkaconnect.CfnConnector.CloudWatchLogsLogDeliveryProperty(
                        enabled=False,
                
                        # the properties below are optional
                        log_group="logGroup"
                    ),
                    firehose=kafkaconnect.CfnConnector.FirehoseLogDeliveryProperty(
                        enabled=False,
                
                        # the properties below are optional
                        delivery_stream="deliveryStream"
                    ),
                    s3=kafkaconnect.CfnConnector.S3LogDeliveryProperty(
                        enabled=False,
                
                        # the properties below are optional
                        bucket="bucket",
                        prefix="prefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__86946fa0b3ddea7b1aa7f3ec595a3c18954a4921e88cbadb55e6fb01ed6d346a)
                check_type(argname="argument cloud_watch_logs", value=cloud_watch_logs, expected_type=type_hints["cloud_watch_logs"])
                check_type(argname="argument firehose", value=firehose, expected_type=type_hints["firehose"])
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs is not None:
                self._values["cloud_watch_logs"] = cloud_watch_logs
            if firehose is not None:
                self._values["firehose"] = firehose
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def cloud_watch_logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.CloudWatchLogsLogDeliveryProperty"]]:
            '''Details about delivering logs to Amazon CloudWatch Logs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-workerlogdelivery.html#cfn-kafkaconnect-connector-workerlogdelivery-cloudwatchlogs
            '''
            result = self._values.get("cloud_watch_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.CloudWatchLogsLogDeliveryProperty"]], result)

        @builtins.property
        def firehose(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.FirehoseLogDeliveryProperty"]]:
            '''Details about delivering logs to Amazon Kinesis Data Firehose.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-workerlogdelivery.html#cfn-kafkaconnect-connector-workerlogdelivery-firehose
            '''
            result = self._values.get("firehose")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.FirehoseLogDeliveryProperty"]], result)

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.S3LogDeliveryProperty"]]:
            '''Details about delivering logs to Amazon S3.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-workerlogdelivery.html#cfn-kafkaconnect-connector-workerlogdelivery-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnector.S3LogDeliveryProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkerLogDeliveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnectorProps",
    jsii_struct_bases=[],
    name_mapping={
        "capacity": "capacity",
        "connector_configuration": "connectorConfiguration",
        "connector_name": "connectorName",
        "kafka_cluster": "kafkaCluster",
        "kafka_cluster_client_authentication": "kafkaClusterClientAuthentication",
        "kafka_cluster_encryption_in_transit": "kafkaClusterEncryptionInTransit",
        "kafka_connect_version": "kafkaConnectVersion",
        "plugins": "plugins",
        "service_execution_role_arn": "serviceExecutionRoleArn",
        "connector_description": "connectorDescription",
        "log_delivery": "logDelivery",
        "worker_configuration": "workerConfiguration",
    },
)
class CfnConnectorProps:
    def __init__(
        self,
        *,
        capacity: typing.Union[typing.Union[CfnConnector.CapacityProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        connector_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]],
        connector_name: builtins.str,
        kafka_cluster: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.KafkaClusterProperty, typing.Dict[builtins.str, typing.Any]]],
        kafka_cluster_client_authentication: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.KafkaClusterClientAuthenticationProperty, typing.Dict[builtins.str, typing.Any]]],
        kafka_cluster_encryption_in_transit: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.KafkaClusterEncryptionInTransitProperty, typing.Dict[builtins.str, typing.Any]]],
        kafka_connect_version: builtins.str,
        plugins: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.PluginProperty, typing.Dict[builtins.str, typing.Any]]]]],
        service_execution_role_arn: builtins.str,
        connector_description: typing.Optional[builtins.str] = None,
        log_delivery: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.LogDeliveryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        worker_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.WorkerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnConnector``.

        :param capacity: The connector's compute capacity settings.
        :param connector_configuration: The configuration of the connector.
        :param connector_name: The name of the connector.
        :param kafka_cluster: The details of the Apache Kafka cluster to which the connector is connected.
        :param kafka_cluster_client_authentication: The type of client authentication used to connect to the Apache Kafka cluster. The value is NONE when no client authentication is used.
        :param kafka_cluster_encryption_in_transit: Details of encryption in transit to the Apache Kafka cluster.
        :param kafka_connect_version: The version of Kafka Connect. It has to be compatible with both the Apache Kafka cluster's version and the plugins.
        :param plugins: Specifies which plugin to use for the connector. You must specify a single-element list. Amazon MSK Connect does not currently support specifying multiple plugins.
        :param service_execution_role_arn: The Amazon Resource Name (ARN) of the IAM role used by the connector to access Amazon Web Services resources.
        :param connector_description: The description of the connector.
        :param log_delivery: The settings for delivering connector logs to Amazon CloudWatch Logs.
        :param worker_configuration: The worker configurations that are in use with the connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_kafkaconnect as kafkaconnect
            
            cfn_connector_props = kafkaconnect.CfnConnectorProps(
                capacity=kafkaconnect.CfnConnector.CapacityProperty(
                    auto_scaling=kafkaconnect.CfnConnector.AutoScalingProperty(
                        max_worker_count=123,
                        mcu_count=123,
                        min_worker_count=123,
                        scale_in_policy=kafkaconnect.CfnConnector.ScaleInPolicyProperty(
                            cpu_utilization_percentage=123
                        ),
                        scale_out_policy=kafkaconnect.CfnConnector.ScaleOutPolicyProperty(
                            cpu_utilization_percentage=123
                        )
                    ),
                    provisioned_capacity=kafkaconnect.CfnConnector.ProvisionedCapacityProperty(
                        worker_count=123,
            
                        # the properties below are optional
                        mcu_count=123
                    )
                ),
                connector_configuration={
                    "connector_configuration_key": "connectorConfiguration"
                },
                connector_name="connectorName",
                kafka_cluster=kafkaconnect.CfnConnector.KafkaClusterProperty(
                    apache_kafka_cluster=kafkaconnect.CfnConnector.ApacheKafkaClusterProperty(
                        bootstrap_servers="bootstrapServers",
                        vpc=kafkaconnect.CfnConnector.VpcProperty(
                            security_groups=["securityGroups"],
                            subnets=["subnets"]
                        )
                    )
                ),
                kafka_cluster_client_authentication=kafkaconnect.CfnConnector.KafkaClusterClientAuthenticationProperty(
                    authentication_type="authenticationType"
                ),
                kafka_cluster_encryption_in_transit=kafkaconnect.CfnConnector.KafkaClusterEncryptionInTransitProperty(
                    encryption_type="encryptionType"
                ),
                kafka_connect_version="kafkaConnectVersion",
                plugins=[kafkaconnect.CfnConnector.PluginProperty(
                    custom_plugin=kafkaconnect.CfnConnector.CustomPluginProperty(
                        custom_plugin_arn="customPluginArn",
                        revision=123
                    )
                )],
                service_execution_role_arn="serviceExecutionRoleArn",
            
                # the properties below are optional
                connector_description="connectorDescription",
                log_delivery=kafkaconnect.CfnConnector.LogDeliveryProperty(
                    worker_log_delivery=kafkaconnect.CfnConnector.WorkerLogDeliveryProperty(
                        cloud_watch_logs=kafkaconnect.CfnConnector.CloudWatchLogsLogDeliveryProperty(
                            enabled=False,
            
                            # the properties below are optional
                            log_group="logGroup"
                        ),
                        firehose=kafkaconnect.CfnConnector.FirehoseLogDeliveryProperty(
                            enabled=False,
            
                            # the properties below are optional
                            delivery_stream="deliveryStream"
                        ),
                        s3=kafkaconnect.CfnConnector.S3LogDeliveryProperty(
                            enabled=False,
            
                            # the properties below are optional
                            bucket="bucket",
                            prefix="prefix"
                        )
                    )
                ),
                worker_configuration=kafkaconnect.CfnConnector.WorkerConfigurationProperty(
                    revision=123,
                    worker_configuration_arn="workerConfigurationArn"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__333a53b3b4a4ba19c2a87c33d683c29acf1be4abed556c4e3ece6257ae80605a)
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument connector_configuration", value=connector_configuration, expected_type=type_hints["connector_configuration"])
            check_type(argname="argument connector_name", value=connector_name, expected_type=type_hints["connector_name"])
            check_type(argname="argument kafka_cluster", value=kafka_cluster, expected_type=type_hints["kafka_cluster"])
            check_type(argname="argument kafka_cluster_client_authentication", value=kafka_cluster_client_authentication, expected_type=type_hints["kafka_cluster_client_authentication"])
            check_type(argname="argument kafka_cluster_encryption_in_transit", value=kafka_cluster_encryption_in_transit, expected_type=type_hints["kafka_cluster_encryption_in_transit"])
            check_type(argname="argument kafka_connect_version", value=kafka_connect_version, expected_type=type_hints["kafka_connect_version"])
            check_type(argname="argument plugins", value=plugins, expected_type=type_hints["plugins"])
            check_type(argname="argument service_execution_role_arn", value=service_execution_role_arn, expected_type=type_hints["service_execution_role_arn"])
            check_type(argname="argument connector_description", value=connector_description, expected_type=type_hints["connector_description"])
            check_type(argname="argument log_delivery", value=log_delivery, expected_type=type_hints["log_delivery"])
            check_type(argname="argument worker_configuration", value=worker_configuration, expected_type=type_hints["worker_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capacity": capacity,
            "connector_configuration": connector_configuration,
            "connector_name": connector_name,
            "kafka_cluster": kafka_cluster,
            "kafka_cluster_client_authentication": kafka_cluster_client_authentication,
            "kafka_cluster_encryption_in_transit": kafka_cluster_encryption_in_transit,
            "kafka_connect_version": kafka_connect_version,
            "plugins": plugins,
            "service_execution_role_arn": service_execution_role_arn,
        }
        if connector_description is not None:
            self._values["connector_description"] = connector_description
        if log_delivery is not None:
            self._values["log_delivery"] = log_delivery
        if worker_configuration is not None:
            self._values["worker_configuration"] = worker_configuration

    @builtins.property
    def capacity(
        self,
    ) -> typing.Union[CfnConnector.CapacityProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''The connector's compute capacity settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-capacity
        '''
        result = self._values.get("capacity")
        assert result is not None, "Required property 'capacity' is missing"
        return typing.cast(typing.Union[CfnConnector.CapacityProperty, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def connector_configuration(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]:
        '''The configuration of the connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-connectorconfiguration
        '''
        result = self._values.get("connector_configuration")
        assert result is not None, "Required property 'connector_configuration' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def connector_name(self) -> builtins.str:
        '''The name of the connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-connectorname
        '''
        result = self._values.get("connector_name")
        assert result is not None, "Required property 'connector_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kafka_cluster(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnector.KafkaClusterProperty]:
        '''The details of the Apache Kafka cluster to which the connector is connected.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-kafkacluster
        '''
        result = self._values.get("kafka_cluster")
        assert result is not None, "Required property 'kafka_cluster' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnector.KafkaClusterProperty], result)

    @builtins.property
    def kafka_cluster_client_authentication(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnector.KafkaClusterClientAuthenticationProperty]:
        '''The type of client authentication used to connect to the Apache Kafka cluster.

        The value is NONE when no client authentication is used.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-kafkaclusterclientauthentication
        '''
        result = self._values.get("kafka_cluster_client_authentication")
        assert result is not None, "Required property 'kafka_cluster_client_authentication' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnector.KafkaClusterClientAuthenticationProperty], result)

    @builtins.property
    def kafka_cluster_encryption_in_transit(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnector.KafkaClusterEncryptionInTransitProperty]:
        '''Details of encryption in transit to the Apache Kafka cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-kafkaclusterencryptionintransit
        '''
        result = self._values.get("kafka_cluster_encryption_in_transit")
        assert result is not None, "Required property 'kafka_cluster_encryption_in_transit' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnector.KafkaClusterEncryptionInTransitProperty], result)

    @builtins.property
    def kafka_connect_version(self) -> builtins.str:
        '''The version of Kafka Connect.

        It has to be compatible with both the Apache Kafka cluster's version and the plugins.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-kafkaconnectversion
        '''
        result = self._values.get("kafka_connect_version")
        assert result is not None, "Required property 'kafka_connect_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def plugins(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnector.PluginProperty]]]:
        '''Specifies which plugin to use for the connector.

        You must specify a single-element list. Amazon MSK Connect does not currently support specifying multiple plugins.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-plugins
        '''
        result = self._values.get("plugins")
        assert result is not None, "Required property 'plugins' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnector.PluginProperty]]], result)

    @builtins.property
    def service_execution_role_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the IAM role used by the connector to access Amazon Web Services resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-serviceexecutionrolearn
        '''
        result = self._values.get("service_execution_role_arn")
        assert result is not None, "Required property 'service_execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connector_description(self) -> typing.Optional[builtins.str]:
        '''The description of the connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-connectordescription
        '''
        result = self._values.get("connector_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_delivery(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnector.LogDeliveryProperty]]:
        '''The settings for delivering connector logs to Amazon CloudWatch Logs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-logdelivery
        '''
        result = self._values.get("log_delivery")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnector.LogDeliveryProperty]], result)

    @builtins.property
    def worker_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnector.WorkerConfigurationProperty]]:
        '''The worker configurations that are in use with the connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-workerconfiguration
        '''
        result = self._values.get("worker_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnector.WorkerConfigurationProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnConnector",
    "CfnConnectorProps",
]

publication.publish()

def _typecheckingstub__04e1edb3d5529b80129194a27d0464190749f3cb401d20fb34ec9206ff4276b8(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    capacity: typing.Union[typing.Union[CfnConnector.CapacityProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    connector_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]],
    connector_name: builtins.str,
    kafka_cluster: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.KafkaClusterProperty, typing.Dict[builtins.str, typing.Any]]],
    kafka_cluster_client_authentication: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.KafkaClusterClientAuthenticationProperty, typing.Dict[builtins.str, typing.Any]]],
    kafka_cluster_encryption_in_transit: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.KafkaClusterEncryptionInTransitProperty, typing.Dict[builtins.str, typing.Any]]],
    kafka_connect_version: builtins.str,
    plugins: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.PluginProperty, typing.Dict[builtins.str, typing.Any]]]]],
    service_execution_role_arn: builtins.str,
    connector_description: typing.Optional[builtins.str] = None,
    log_delivery: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.LogDeliveryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    worker_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.WorkerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ce2cc9abbc11e456a6e8f5856bb709af51a33c182c203c517e0f5485569e84(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5392fcba97b4da8c28b76df652c11cad7f8ba1a405a7493c78b1d537b5612316(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f9eaf3d4c43df956ba6290f0ac0ddbac1e813bb929ede281fec5c5228cc3131(
    value: typing.Union[CfnConnector.CapacityProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daba67fa009e2e07571999ae9fe0490330127df3d621f4d3212bf1596fcbfa11(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__987f60634306e38d5192d4b0aa0817566f1942a4b9b1792c54c9605c27605865(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2904f48bec9068c1558ab8d57318e02c37f077cc732b7bf70fcc80a602c46c57(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnector.KafkaClusterProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5159d4ee8b022ca5c92de664ab7af238a2808dd87d9235ad451b1afeb196ed74(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnector.KafkaClusterClientAuthenticationProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b4016b0d04d557f24748b4c1642a276edc4c4bb3a4e97340b93b991b8a37675(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnector.KafkaClusterEncryptionInTransitProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7e20c8942f254bf13d02aa91599ee5d47b83e5b21bd79b0eb855877320742c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f6eefbf825b07358e48dd33a2b95b41130308c6f22090da7835d5501166f4ef(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnector.PluginProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3acab356d74a0880b17835cfd16ca00af6db7da1839496d36a23f0db5ba41dc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a8f576cdc665b2bd66368c3871685a8eab74f0da2fe6545e29cddab7ddf705(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__689e8652a48b7b08dd0afc54a28258d7fb4b674388bd6069aad65c8882c29b8a(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnector.LogDeliveryProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b25953311169416850d5d9bac90b75c6abe6ef29e2ff6c007e5ae32e0e6516(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnector.WorkerConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dabe30b088bb7bd2ee12c8005a9559c5d39597f148ff9e88801524bffe4fa29(
    *,
    bootstrap_servers: builtins.str,
    vpc: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.VpcProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b94c0209a48b85ffeae598a4f7cfd9117260afc0f52a80b7a7a1877510ae0c(
    *,
    max_worker_count: jsii.Number,
    mcu_count: jsii.Number,
    min_worker_count: jsii.Number,
    scale_in_policy: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.ScaleInPolicyProperty, typing.Dict[builtins.str, typing.Any]]],
    scale_out_policy: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.ScaleOutPolicyProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac00b85fd7dd7a7b89fc29c5176ec6b10c5fe9aeff1afe746b2329ac11edfa7e(
    *,
    auto_scaling: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.AutoScalingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    provisioned_capacity: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.ProvisionedCapacityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9806eda86391fb5101bcd9cf55d390ca7e98533215522cef1b97fc570fa0a2c3(
    *,
    enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    log_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b83b2d8c6c84901292e0f1b433a485c3bfe24f4665eb0b646fad5803510dd88(
    *,
    custom_plugin_arn: builtins.str,
    revision: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e82c6f82c80af96dc1291c65337690e076283bed1f50d22122d8eebb899286(
    *,
    enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    delivery_stream: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e507e39a6a7602c0cdfaaa469e0435270c5f5504f7599f6253d5c5277fccb13c(
    *,
    authentication_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a682e6ce9f496be129502b1758d9886e0cf64dec39989ccc16abd8e8008ed915(
    *,
    encryption_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f4cbb443ac141daa7834dd8f90b9a289eda7b5af4911d65a2893401e2d01cb(
    *,
    apache_kafka_cluster: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.ApacheKafkaClusterProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09708796cb367b27269ef7238c058470df510c6dc85bb4707c0284b18563e5f5(
    *,
    worker_log_delivery: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.WorkerLogDeliveryProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdf3ff7d08d60292f7cc3f7fbb5a010fdb4d130229365a90f2d6ad5cab08d93b(
    *,
    custom_plugin: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.CustomPluginProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd251940e0a2c765a29f41c670ed29af29e795a7aec06a1f44698681b4301bb(
    *,
    worker_count: jsii.Number,
    mcu_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f88f4ea961fff582feea3c86961cebd1fd7d2b9cb355c98f50a1481fe592d58a(
    *,
    enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    bucket: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe6ff153c08ad549e5a45bd5a0438c16678d9eb9bd10465dd398e19f6f6a954(
    *,
    cpu_utilization_percentage: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24073addbe78614f0277a915f96ad75aa9eba698dba47fba48923e30282cc2ea(
    *,
    cpu_utilization_percentage: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf3a3a2e13475a55e453fcf8dda8b6622052bcf1cc91884fb3cb093038cdc60(
    *,
    security_groups: typing.Sequence[builtins.str],
    subnets: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187013179663794250fadab97ae34febfcb6f0cddf82b5af3c96e0383b284e2f(
    *,
    revision: jsii.Number,
    worker_configuration_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86946fa0b3ddea7b1aa7f3ec595a3c18954a4921e88cbadb55e6fb01ed6d346a(
    *,
    cloud_watch_logs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.CloudWatchLogsLogDeliveryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    firehose: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.FirehoseLogDeliveryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.S3LogDeliveryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333a53b3b4a4ba19c2a87c33d683c29acf1be4abed556c4e3ece6257ae80605a(
    *,
    capacity: typing.Union[typing.Union[CfnConnector.CapacityProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    connector_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]],
    connector_name: builtins.str,
    kafka_cluster: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.KafkaClusterProperty, typing.Dict[builtins.str, typing.Any]]],
    kafka_cluster_client_authentication: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.KafkaClusterClientAuthenticationProperty, typing.Dict[builtins.str, typing.Any]]],
    kafka_cluster_encryption_in_transit: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.KafkaClusterEncryptionInTransitProperty, typing.Dict[builtins.str, typing.Any]]],
    kafka_connect_version: builtins.str,
    plugins: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.PluginProperty, typing.Dict[builtins.str, typing.Any]]]]],
    service_execution_role_arn: builtins.str,
    connector_description: typing.Optional[builtins.str] = None,
    log_delivery: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.LogDeliveryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    worker_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnector.WorkerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
