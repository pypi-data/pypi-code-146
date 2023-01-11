'''
# Amazon OpenSearch Service Construct Library

<!--BEGIN STABILITY BANNER-->---


Features                           | Stability
-----------------------------------|----------------------------------------------------------------
CFN Resources                      | ![Stable](https://img.shields.io/badge/stable-success.svg?style=for-the-badge)
Higher level constructs for Domain | ![Stable](https://img.shields.io/badge/stable-success.svg?style=for-the-badge)

> **CFN Resources:** All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always
> stable and safe to use.

<!-- -->

> **Stable:** Higher level constructs in this module that are marked stable will not undergo any
> breaking changes. They will strictly follow the [Semantic Versioning](https://semver.org/) model.

---
<!--END STABILITY BANNER-->

See [Migrating to OpenSearch](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-elasticsearch-readme.html#migrating-to-opensearch) for migration instructions from `@aws-cdk/aws-elasticsearch` to this module, `@aws-cdk/aws-opensearchservice`.

## Quick start

Create a development cluster by simply specifying the version:

```python
dev_domain = opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0
)
```

To perform version upgrades without replacing the entire domain, specify the `enableVersionUpgrade` property.

```python
dev_domain = opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    enable_version_upgrade=True
)
```

Create a production grade cluster by also specifying things like capacity and az distribution

```python
prod_domain = opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    capacity=opensearch.CapacityConfig(
        master_nodes=5,
        data_nodes=20
    ),
    ebs=opensearch.EbsOptions(
        volume_size=20
    ),
    zone_awareness=opensearch.ZoneAwarenessConfig(
        availability_zone_count=3
    ),
    logging=opensearch.LoggingOptions(
        slow_search_log_enabled=True,
        app_log_enabled=True,
        slow_index_log_enabled=True
    )
)
```

This creates an Amazon OpenSearch Service cluster and automatically sets up log groups for
logging the domain logs and slow search logs.

## A note about SLR

Some cluster configurations (e.g VPC access) require the existence of the [`AWSServiceRoleForAmazonElasticsearchService`](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/slr.html) Service-Linked Role.

When performing such operations via the AWS Console, this SLR is created automatically when needed. However, this is not the behavior when using CloudFormation. If an SLR is needed, but doesn't exist, you will encounter a failure message simlar to:

```console
Before you can proceed, you must enable a service-linked role to give Amazon OpenSearch Service...
```

To resolve this, you need to [create](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html#create-service-linked-role) the SLR. We recommend using the AWS CLI:

```console
aws iam create-service-linked-role --aws-service-name es.amazonaws.com
```

You can also create it using the CDK, **but note that only the first application deploying this will succeed**:

```python
slr = iam.CfnServiceLinkedRole(self, "Service Linked Role",
    aws_service_name="es.amazonaws.com"
)
```

## Importing existing domains

To import an existing domain into your CDK application, use the `Domain.fromDomainEndpoint` factory method.
This method accepts a domain endpoint of an already existing domain:

```python
domain_endpoint = "https://my-domain-jcjotrt6f7otem4sqcwbch3c4u.us-east-1.es.amazonaws.com"
domain = opensearch.Domain.from_domain_endpoint(self, "ImportedDomain", domain_endpoint)
```

## Permissions

### IAM

Helper methods also exist for managing access to the domain.

```python
# fn: lambda.Function
# domain: opensearch.Domain


# Grant write access to the app-search index
domain.grant_index_write("app-search", fn)

# Grant read access to the 'app-search/_search' path
domain.grant_path_read("app-search/_search", fn)
```

## Encryption

The domain can also be created with encryption enabled:

```python
domain = opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    ebs=opensearch.EbsOptions(
        volume_size=100,
        volume_type=ec2.EbsDeviceVolumeType.GENERAL_PURPOSE_SSD
    ),
    node_to_node_encryption=True,
    encryption_at_rest=opensearch.EncryptionAtRestOptions(
        enabled=True
    )
)
```

This sets up the domain with node to node encryption and encryption at
rest. You can also choose to supply your own KMS key to use for encryption at
rest.

## VPC Support

Domains can be placed inside a VPC, providing a secure communication between Amazon OpenSearch Service and other services within the VPC without the need for an internet gateway, NAT device, or VPN connection.

> Visit [VPC Support for Amazon OpenSearch Service Domains](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vpc.html) for more details.

```python
vpc = ec2.Vpc(self, "Vpc")
domain_props = opensearch.DomainProps(
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    removal_policy=RemovalPolicy.DESTROY,
    vpc=vpc,
    # must be enabled since our VPC contains multiple private subnets.
    zone_awareness=opensearch.ZoneAwarenessConfig(
        enabled=True
    ),
    capacity=opensearch.CapacityConfig(
        # must be an even number since the default az count is 2.
        data_nodes=2
    )
)
opensearch.Domain(self, "Domain", domain_props)
```

In addition, you can use the `vpcSubnets` property to control which specific subnets will be used, and the `securityGroups` property to control
which security groups will be attached to the domain. By default, CDK will select all *private* subnets in the VPC, and create one dedicated security group.

## Metrics

Helper methods exist to access common domain metrics for example:

```python
# domain: opensearch.Domain

free_storage_space = domain.metric_free_storage_space()
master_sys_memory_utilization = domain.metric("MasterSysMemoryUtilization")
```

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## Fine grained access control

The domain can also be created with a master user configured. The password can
be supplied or dynamically created if not supplied.

```python
domain = opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    enforce_https=True,
    node_to_node_encryption=True,
    encryption_at_rest=opensearch.EncryptionAtRestOptions(
        enabled=True
    ),
    fine_grained_access_control=opensearch.AdvancedSecurityOptions(
        master_user_name="master-user"
    )
)

master_user_password = domain.master_user_password
```

## Using unsigned basic auth

For convenience, the domain can be configured to allow unsigned HTTP requests
that use basic auth. Unless the domain is configured to be part of a VPC this
means anyone can access the domain using the configured master username and
password.

To enable unsigned basic auth access the domain is configured with an access
policy that allows anyonmous requests, HTTPS required, node to node encryption,
encryption at rest and fine grained access control.

If the above settings are not set they will be configured as part of enabling
unsigned basic auth. If they are set with conflicting values, an error will be
thrown.

If no master user is configured a default master user is created with the
username `admin`.

If no password is configured a default master user password is created and
stored in the AWS Secrets Manager as secret. The secret has the prefix
`<domain id>MasterUser`.

```python
domain = opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    use_unsigned_basic_auth=True
)

master_user_password = domain.master_user_password
```

## Custom access policies

If the domain requires custom access control it can be configured either as a
constructor property, or later by means of a helper method.

For simple permissions the `accessPolicies` constructor may be sufficient:

```python
domain = opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    access_policies=[
        iam.PolicyStatement(
            actions=["es:*ESHttpPost", "es:ESHttpPut*"],
            effect=iam.Effect.ALLOW,
            principals=[iam.AccountPrincipal("123456789012")],
            resources=["*"]
        )
    ]
)
```

For more complex use-cases, for example, to set the domain up to receive data from a
[cross-account Kinesis Firehose](https://aws.amazon.com/premiumsupport/knowledge-center/kinesis-firehose-cross-account-streaming/) the `addAccessPolicies` helper method
allows for policies that include the explicit domain ARN.

```python
domain = opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0
)
domain.add_access_policies(
    iam.PolicyStatement(
        actions=["es:ESHttpPost", "es:ESHttpPut"],
        effect=iam.Effect.ALLOW,
        principals=[iam.AccountPrincipal("123456789012")],
        resources=[domain.domain_arn, f"{domain.domainArn}/*"]
    ),
    iam.PolicyStatement(
        actions=["es:ESHttpGet"],
        effect=iam.Effect.ALLOW,
        principals=[iam.AccountPrincipal("123456789012")],
        resources=[f"{domain.domainArn}/_all/_settings", f"{domain.domainArn}/_cluster/stats", f"{domain.domainArn}/index-name*/_mapping/type-name", f"{domain.domainArn}/roletest*/_mapping/roletest", f"{domain.domainArn}/_nodes", f"{domain.domainArn}/_nodes/stats", f"{domain.domainArn}/_nodes/*/stats", f"{domain.domainArn}/_stats", f"{domain.domainArn}/index-name*/_stats", f"{domain.domainArn}/roletest*/_stat"
        ]
    ))
```

## Audit logs

Audit logs can be enabled for a domain, but only when fine grained access control is enabled.

```python
domain = opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    enforce_https=True,
    node_to_node_encryption=True,
    encryption_at_rest=opensearch.EncryptionAtRestOptions(
        enabled=True
    ),
    fine_grained_access_control=opensearch.AdvancedSecurityOptions(
        master_user_name="master-user"
    ),
    logging=opensearch.LoggingOptions(
        audit_log_enabled=True,
        slow_search_log_enabled=True,
        app_log_enabled=True,
        slow_index_log_enabled=True
    )
)
```

## UltraWarm

UltraWarm nodes can be enabled to provide a cost-effective way to store large amounts of read-only data.

```python
domain = opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    capacity=opensearch.CapacityConfig(
        master_nodes=2,
        warm_nodes=2,
        warm_instance_type="ultrawarm1.medium.search"
    )
)
```

## Custom endpoint

Custom endpoints can be configured to reach the domain under a custom domain name.

```python
opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    custom_endpoint=opensearch.CustomEndpointOptions(
        domain_name="search.example.com"
    )
)
```

It is also possible to specify a custom certificate instead of the auto-generated one.

Additionally, an automatic CNAME-Record is created if a hosted zone is provided for the custom endpoint

## Advanced options

[Advanced options](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/createupdatedomains.html#createdomain-configure-advanced-options) can used to configure additional options.

```python
opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_0,
    advanced_options={
        "rest.action.multi.allow_explicit_index": "false",
        "indices.fielddata.cache.size": "25",
        "indices.query.bool.max_clause_count": "2048"
    }
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

from ._jsii import *

import aws_cdk.aws_certificatemanager as _aws_cdk_aws_certificatemanager_1662be0d
import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_9b88bb94
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_67de8e8d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_940a1ce0
import aws_cdk.aws_kms as _aws_cdk_aws_kms_e491a92b
import aws_cdk.aws_logs as _aws_cdk_aws_logs_6c4320fb
import aws_cdk.aws_route53 as _aws_cdk_aws_route53_f47b29d4
import aws_cdk.core as _aws_cdk_core_f4b25747
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opensearchservice.AdvancedSecurityOptions",
    jsii_struct_bases=[],
    name_mapping={
        "master_user_arn": "masterUserArn",
        "master_user_name": "masterUserName",
        "master_user_password": "masterUserPassword",
    },
)
class AdvancedSecurityOptions:
    def __init__(
        self,
        *,
        master_user_arn: typing.Optional[builtins.str] = None,
        master_user_name: typing.Optional[builtins.str] = None,
        master_user_password: typing.Optional[_aws_cdk_core_f4b25747.SecretValue] = None,
    ) -> None:
        '''Specifies options for fine-grained access control.

        :param master_user_arn: ARN for the master user. Only specify this or masterUserName, but not both. Default: - fine-grained access control is disabled
        :param master_user_name: Username for the master user. Only specify this or masterUserArn, but not both. Default: - fine-grained access control is disabled
        :param master_user_password: Password for the master user. You can use ``SecretValue.unsafePlainText`` to specify a password in plain text or use ``secretsmanager.Secret.fromSecretAttributes`` to reference a secret in Secrets Manager. Default: - A Secrets Manager generated password

        :exampleMetadata: infused

        Example::

            domain = opensearch.Domain(self, "Domain",
                version=opensearch.EngineVersion.OPENSEARCH_1_0,
                enforce_https=True,
                node_to_node_encryption=True,
                encryption_at_rest=opensearch.EncryptionAtRestOptions(
                    enabled=True
                ),
                fine_grained_access_control=opensearch.AdvancedSecurityOptions(
                    master_user_name="master-user"
                ),
                logging=opensearch.LoggingOptions(
                    audit_log_enabled=True,
                    slow_search_log_enabled=True,
                    app_log_enabled=True,
                    slow_index_log_enabled=True
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9663f6c508a4270e241a70dbc92c6a2ad261f30507ea62ef1fa6c2dd19e64527)
            check_type(argname="argument master_user_arn", value=master_user_arn, expected_type=type_hints["master_user_arn"])
            check_type(argname="argument master_user_name", value=master_user_name, expected_type=type_hints["master_user_name"])
            check_type(argname="argument master_user_password", value=master_user_password, expected_type=type_hints["master_user_password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if master_user_arn is not None:
            self._values["master_user_arn"] = master_user_arn
        if master_user_name is not None:
            self._values["master_user_name"] = master_user_name
        if master_user_password is not None:
            self._values["master_user_password"] = master_user_password

    @builtins.property
    def master_user_arn(self) -> typing.Optional[builtins.str]:
        '''ARN for the master user.

        Only specify this or masterUserName, but not both.

        :default: - fine-grained access control is disabled
        '''
        result = self._values.get("master_user_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_user_name(self) -> typing.Optional[builtins.str]:
        '''Username for the master user.

        Only specify this or masterUserArn, but not both.

        :default: - fine-grained access control is disabled
        '''
        result = self._values.get("master_user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_user_password(
        self,
    ) -> typing.Optional[_aws_cdk_core_f4b25747.SecretValue]:
        '''Password for the master user.

        You can use ``SecretValue.unsafePlainText`` to specify a password in plain text or
        use ``secretsmanager.Secret.fromSecretAttributes`` to reference a secret in
        Secrets Manager.

        :default: - A Secrets Manager generated password
        '''
        result = self._values.get("master_user_password")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.SecretValue], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedSecurityOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opensearchservice.CapacityConfig",
    jsii_struct_bases=[],
    name_mapping={
        "data_node_instance_type": "dataNodeInstanceType",
        "data_nodes": "dataNodes",
        "master_node_instance_type": "masterNodeInstanceType",
        "master_nodes": "masterNodes",
        "warm_instance_type": "warmInstanceType",
        "warm_nodes": "warmNodes",
    },
)
class CapacityConfig:
    def __init__(
        self,
        *,
        data_node_instance_type: typing.Optional[builtins.str] = None,
        data_nodes: typing.Optional[jsii.Number] = None,
        master_node_instance_type: typing.Optional[builtins.str] = None,
        master_nodes: typing.Optional[jsii.Number] = None,
        warm_instance_type: typing.Optional[builtins.str] = None,
        warm_nodes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Configures the capacity of the cluster such as the instance type and the number of instances.

        :param data_node_instance_type: The instance type for your data nodes, such as ``m3.medium.search``. For valid values, see `Supported Instance Types <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-instance-types.html>`_ in the Amazon OpenSearch Service Developer Guide. Default: - r5.large.search
        :param data_nodes: The number of data nodes (instances) to use in the Amazon OpenSearch Service domain. Default: - 1
        :param master_node_instance_type: The hardware configuration of the computer that hosts the dedicated master node, such as ``m3.medium.search``. For valid values, see [Supported Instance Types] (https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-instance-types.html) in the Amazon OpenSearch Service Developer Guide. Default: - r5.large.search
        :param master_nodes: The number of instances to use for the master node. Default: - no dedicated master nodes
        :param warm_instance_type: The instance type for your UltraWarm node, such as ``ultrawarm1.medium.search``. For valid values, see [UltraWarm Storage Limits] (https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#limits-ultrawarm) in the Amazon OpenSearch Service Developer Guide. Default: - ultrawarm1.medium.search
        :param warm_nodes: The number of UltraWarm nodes (instances) to use in the Amazon OpenSearch Service domain. Default: - no UltraWarm nodes

        :exampleMetadata: infused

        Example::

            domain = opensearch.Domain(self, "Domain",
                version=opensearch.EngineVersion.OPENSEARCH_1_0,
                capacity=opensearch.CapacityConfig(
                    master_nodes=2,
                    warm_nodes=2,
                    warm_instance_type="ultrawarm1.medium.search"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09e49dad680f17a1e3e914105d1c4eccf2dadf3f6193aa3a1e626f41a3ae67ee)
            check_type(argname="argument data_node_instance_type", value=data_node_instance_type, expected_type=type_hints["data_node_instance_type"])
            check_type(argname="argument data_nodes", value=data_nodes, expected_type=type_hints["data_nodes"])
            check_type(argname="argument master_node_instance_type", value=master_node_instance_type, expected_type=type_hints["master_node_instance_type"])
            check_type(argname="argument master_nodes", value=master_nodes, expected_type=type_hints["master_nodes"])
            check_type(argname="argument warm_instance_type", value=warm_instance_type, expected_type=type_hints["warm_instance_type"])
            check_type(argname="argument warm_nodes", value=warm_nodes, expected_type=type_hints["warm_nodes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_node_instance_type is not None:
            self._values["data_node_instance_type"] = data_node_instance_type
        if data_nodes is not None:
            self._values["data_nodes"] = data_nodes
        if master_node_instance_type is not None:
            self._values["master_node_instance_type"] = master_node_instance_type
        if master_nodes is not None:
            self._values["master_nodes"] = master_nodes
        if warm_instance_type is not None:
            self._values["warm_instance_type"] = warm_instance_type
        if warm_nodes is not None:
            self._values["warm_nodes"] = warm_nodes

    @builtins.property
    def data_node_instance_type(self) -> typing.Optional[builtins.str]:
        '''The instance type for your data nodes, such as ``m3.medium.search``. For valid values, see `Supported Instance Types <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-instance-types.html>`_ in the Amazon OpenSearch Service Developer Guide.

        :default: - r5.large.search
        '''
        result = self._values.get("data_node_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_nodes(self) -> typing.Optional[jsii.Number]:
        '''The number of data nodes (instances) to use in the Amazon OpenSearch Service domain.

        :default: - 1
        '''
        result = self._values.get("data_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def master_node_instance_type(self) -> typing.Optional[builtins.str]:
        '''The hardware configuration of the computer that hosts the dedicated master node, such as ``m3.medium.search``. For valid values, see [Supported Instance Types] (https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-instance-types.html) in the Amazon OpenSearch Service Developer Guide.

        :default: - r5.large.search
        '''
        result = self._values.get("master_node_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_nodes(self) -> typing.Optional[jsii.Number]:
        '''The number of instances to use for the master node.

        :default: - no dedicated master nodes
        '''
        result = self._values.get("master_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def warm_instance_type(self) -> typing.Optional[builtins.str]:
        '''The instance type for your UltraWarm node, such as ``ultrawarm1.medium.search``. For valid values, see [UltraWarm Storage Limits] (https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#limits-ultrawarm) in the Amazon OpenSearch Service Developer Guide.

        :default: - ultrawarm1.medium.search
        '''
        result = self._values.get("warm_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def warm_nodes(self) -> typing.Optional[jsii.Number]:
        '''The number of UltraWarm nodes (instances) to use in the Amazon OpenSearch Service domain.

        :default: - no UltraWarm nodes
        '''
        result = self._values.get("warm_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CapacityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnDomain(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-opensearchservice.CfnDomain",
):
    '''A CloudFormation ``AWS::OpenSearchService::Domain``.

    The AWS::OpenSearchService::Domain resource creates an Amazon OpenSearch Service domain.

    :cloudformationResource: AWS::OpenSearchService::Domain
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_opensearchservice as opensearchservice
        
        # access_policies: Any
        
        cfn_domain = opensearchservice.CfnDomain(self, "MyCfnDomain",
            access_policies=access_policies,
            advanced_options={
                "advanced_options_key": "advancedOptions"
            },
            advanced_security_options=opensearchservice.CfnDomain.AdvancedSecurityOptionsInputProperty(
                enabled=False,
                internal_user_database_enabled=False,
                master_user_options=opensearchservice.CfnDomain.MasterUserOptionsProperty(
                    master_user_arn="masterUserArn",
                    master_user_name="masterUserName",
                    master_user_password="masterUserPassword"
                )
            ),
            cluster_config=opensearchservice.CfnDomain.ClusterConfigProperty(
                dedicated_master_count=123,
                dedicated_master_enabled=False,
                dedicated_master_type="dedicatedMasterType",
                instance_count=123,
                instance_type="instanceType",
                warm_count=123,
                warm_enabled=False,
                warm_type="warmType",
                zone_awareness_config=opensearchservice.CfnDomain.ZoneAwarenessConfigProperty(
                    availability_zone_count=123
                ),
                zone_awareness_enabled=False
            ),
            cognito_options=opensearchservice.CfnDomain.CognitoOptionsProperty(
                enabled=False,
                identity_pool_id="identityPoolId",
                role_arn="roleArn",
                user_pool_id="userPoolId"
            ),
            domain_endpoint_options=opensearchservice.CfnDomain.DomainEndpointOptionsProperty(
                custom_endpoint="customEndpoint",
                custom_endpoint_certificate_arn="customEndpointCertificateArn",
                custom_endpoint_enabled=False,
                enforce_https=False,
                tls_security_policy="tlsSecurityPolicy"
            ),
            domain_name="domainName",
            ebs_options=opensearchservice.CfnDomain.EBSOptionsProperty(
                ebs_enabled=False,
                iops=123,
                throughput=123,
                volume_size=123,
                volume_type="volumeType"
            ),
            encryption_at_rest_options=opensearchservice.CfnDomain.EncryptionAtRestOptionsProperty(
                enabled=False,
                kms_key_id="kmsKeyId"
            ),
            engine_version="engineVersion",
            log_publishing_options={
                "log_publishing_options_key": opensearchservice.CfnDomain.LogPublishingOptionProperty(
                    cloud_watch_logs_log_group_arn="cloudWatchLogsLogGroupArn",
                    enabled=False
                )
            },
            node_to_node_encryption_options=opensearchservice.CfnDomain.NodeToNodeEncryptionOptionsProperty(
                enabled=False
            ),
            snapshot_options=opensearchservice.CfnDomain.SnapshotOptionsProperty(
                automated_snapshot_start_hour=123
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_options=opensearchservice.CfnDomain.VPCOptionsProperty(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"]
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        access_policies: typing.Any = None,
        advanced_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        advanced_security_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDomain.AdvancedSecurityOptionsInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        cluster_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDomain.ClusterConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        cognito_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDomain.CognitoOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        domain_endpoint_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDomain.DomainEndpointOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        ebs_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDomain.EBSOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        encryption_at_rest_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDomain.EncryptionAtRestOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        engine_version: typing.Optional[builtins.str] = None,
        log_publishing_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDomain.LogPublishingOptionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        node_to_node_encryption_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDomain.NodeToNodeEncryptionOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        snapshot_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDomain.SnapshotOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDomain.VPCOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::OpenSearchService::Domain``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param access_policies: An AWS Identity and Access Management ( IAM ) policy document that specifies who can access the OpenSearch Service domain and their permissions. For more information, see `Configuring access policies <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ac.html#ac-creating>`_ in the *Amazon OpenSearch Service Developer Guide* .
        :param advanced_options: Additional options to specify for the OpenSearch Service domain. For more information, see `AdvancedOptions <https://docs.aws.amazon.com/opensearch-service/latest/APIReference/API_CreateDomain.html#API_CreateDomain_RequestBody>`_ in the OpenSearch Service API reference.
        :param advanced_security_options: Specifies options for fine-grained access control. If you specify advanced security options, you must also enable node-to-node encryption ( `NodeToNodeEncryptionOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodetonodeencryptionoptions.html>`_ ) and encryption at rest ( `EncryptionAtRestOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html>`_ ). You must also enable ``EnforceHTTPS`` within `DomainEndpointOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html>`_ , which requires HTTPS for all traffic to the domain.
        :param cluster_config: Container for the cluster configuration of a domain.
        :param cognito_options: Configures OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards.
        :param domain_endpoint_options: Specifies additional options for the domain endpoint, such as whether to require HTTPS for all traffic or whether to use a custom endpoint rather than the default endpoint.
        :param domain_name: A name for the OpenSearch Service domain. For valid values, see the `DomainName <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/configuration-api.html#configuration-api-datatypes-domainname>`_ data type in the *Amazon OpenSearch Service Developer Guide* . If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the domain name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . Required when creating a new domain. .. epigraph:: If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param ebs_options: The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the OpenSearch Service domain. For more information, see `EBS volume size limits <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource>`_ in the *Amazon OpenSearch Service Developer Guide* .
        :param encryption_at_rest_options: Whether the domain should encrypt data at rest, and if so, the AWS KMS key to use. See `Encryption of data at rest for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/encryption-at-rest.html>`_ .
        :param engine_version: The version of OpenSearch to use. The value must be in the format ``OpenSearch_X.Y`` or ``Elasticsearch_X.Y`` . If not specified, the latest version of OpenSearch is used. For information about the versions that OpenSearch Service supports, see `Supported versions of OpenSearch and Elasticsearch <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html#choosing-version>`_ in the *Amazon OpenSearch Service Developer Guide* . If you set the `EnableVersionUpgrade <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-upgradeopensearchdomain>`_ update policy to ``true`` , you can update ``EngineVersion`` without interruption. When ``EnableVersionUpgrade`` is set to ``false`` , or is not specified, updating ``EngineVersion`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .
        :param log_publishing_options: An object with one or more of the following keys: ``SEARCH_SLOW_LOGS`` , ``ES_APPLICATION_LOGS`` , ``INDEX_SLOW_LOGS`` , ``AUDIT_LOGS`` , depending on the types of logs you want to publish. Each key needs a valid ``LogPublishingOption`` value. For the full syntax, see the `examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#aws-resource-opensearchservice-domain--examples>`_ .
        :param node_to_node_encryption_options: Specifies whether node-to-node encryption is enabled. See `Node-to-node encryption for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ntn.html>`_ .
        :param snapshot_options: *DEPRECATED* . The automated snapshot configuration for the OpenSearch Service domain indexes.
        :param tags: An arbitrary set of tags (key–value pairs) to associate with the OpenSearch Service domain.
        :param vpc_options: The virtual private cloud (VPC) configuration for the OpenSearch Service domain. For more information, see `Launching your Amazon OpenSearch Service domains within a VPC <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vpc.html>`_ in the *Amazon OpenSearch Service Developer Guide* . If you remove this entity altogether, along with its associated properties, it causes a replacement. You might encounter this scenario if you're updating your security configuration from a VPC to a public endpoint.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d8bfb3eae80cd17b709b261261abd885f782259b2c67e0a6b7b54234bbfa41f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDomainProps(
            access_policies=access_policies,
            advanced_options=advanced_options,
            advanced_security_options=advanced_security_options,
            cluster_config=cluster_config,
            cognito_options=cognito_options,
            domain_endpoint_options=domain_endpoint_options,
            domain_name=domain_name,
            ebs_options=ebs_options,
            encryption_at_rest_options=encryption_at_rest_options,
            engine_version=engine_version,
            log_publishing_options=log_publishing_options,
            node_to_node_encryption_options=node_to_node_encryption_options,
            snapshot_options=snapshot_options,
            tags=tags,
            vpc_options=vpc_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d922cc0a798d483aa0dbc1dc2f5d9b171e62be078177b79fcc1f298b0a34cd7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f8cf9b8e15dc0f9cd25846048eedfdec5b2f23e3158d3e1286d92363bbf7813)
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
        '''The Amazon Resource Name (ARN) of the domain, such as ``arn:aws:es:us-west-2:123456789012:domain/mystack-1ab2cdefghij`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrDomainEndpoint")
    def attr_domain_endpoint(self) -> builtins.str:
        '''The domain-specific endpoint used for requests to the OpenSearch APIs, such as ``search-mystack-1ab2cdefghij-ab1c2deckoyb3hofw7wpqa3cm.us-west-1.es.amazonaws.com`` .

        :cloudformationAttribute: DomainEndpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDomainEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="attrDomainEndpoints")
    def attr_domain_endpoints(self) -> _aws_cdk_core_f4b25747.IResolvable:
        '''
        :cloudformationAttribute: DomainEndpoints
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrDomainEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The resource ID.

        For example, ``123456789012/my-domain`` .

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceSoftwareOptionsAutomatedUpdateDate")
    def attr_service_software_options_automated_update_date(self) -> builtins.str:
        '''The timestamp, in Epoch time, until which you can manually request a service software update.

        After this date, we automatically update your service software.

        :cloudformationAttribute: ServiceSoftwareOptions.AutomatedUpdateDate
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceSoftwareOptionsAutomatedUpdateDate"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceSoftwareOptionsCancellable")
    def attr_service_software_options_cancellable(
        self,
    ) -> _aws_cdk_core_f4b25747.IResolvable:
        '''True if you're able to cancel your service software version update.

        False if you can't cancel your service software update.

        :cloudformationAttribute: ServiceSoftwareOptions.Cancellable
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrServiceSoftwareOptionsCancellable"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceSoftwareOptionsCurrentVersion")
    def attr_service_software_options_current_version(self) -> builtins.str:
        '''The current service software version present on the domain.

        :cloudformationAttribute: ServiceSoftwareOptions.CurrentVersion
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceSoftwareOptionsCurrentVersion"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceSoftwareOptionsDescription")
    def attr_service_software_options_description(self) -> builtins.str:
        '''A description of the service software update status.

        :cloudformationAttribute: ServiceSoftwareOptions.Description
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceSoftwareOptionsDescription"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceSoftwareOptionsNewVersion")
    def attr_service_software_options_new_version(self) -> builtins.str:
        '''The new service software version, if one is available.

        :cloudformationAttribute: ServiceSoftwareOptions.NewVersion
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceSoftwareOptionsNewVersion"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceSoftwareOptionsOptionalDeployment")
    def attr_service_software_options_optional_deployment(
        self,
    ) -> _aws_cdk_core_f4b25747.IResolvable:
        '''True if a service software is never automatically updated.

        False if a service software is automatically updated after the automated update date.

        :cloudformationAttribute: ServiceSoftwareOptions.OptionalDeployment
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrServiceSoftwareOptionsOptionalDeployment"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceSoftwareOptionsUpdateAvailable")
    def attr_service_software_options_update_available(
        self,
    ) -> _aws_cdk_core_f4b25747.IResolvable:
        '''True if you're able to update your service software version.

        False if you can't update your service software version.

        :cloudformationAttribute: ServiceSoftwareOptions.UpdateAvailable
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrServiceSoftwareOptionsUpdateAvailable"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceSoftwareOptionsUpdateStatus")
    def attr_service_software_options_update_status(self) -> builtins.str:
        '''The status of your service software update.

        :cloudformationAttribute: ServiceSoftwareOptions.UpdateStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceSoftwareOptionsUpdateStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An arbitrary set of tags (key–value pairs) to associate with the OpenSearch Service domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="accessPolicies")
    def access_policies(self) -> typing.Any:
        '''An AWS Identity and Access Management ( IAM ) policy document that specifies who can access the OpenSearch Service domain and their permissions.

        For more information, see `Configuring access policies <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ac.html#ac-creating>`_ in the *Amazon OpenSearch Service Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-accesspolicies
        '''
        return typing.cast(typing.Any, jsii.get(self, "accessPolicies"))

    @access_policies.setter
    def access_policies(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__124490f44bfc8cb9166d95f5cf1a1e143bd9c84e143ee82a84691224bd148aa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessPolicies", value)

    @builtins.property
    @jsii.member(jsii_name="advancedOptions")
    def advanced_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''Additional options to specify for the OpenSearch Service domain.

        For more information, see `AdvancedOptions <https://docs.aws.amazon.com/opensearch-service/latest/APIReference/API_CreateDomain.html#API_CreateDomain_RequestBody>`_ in the OpenSearch Service API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-advancedoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "advancedOptions"))

    @advanced_options.setter
    def advanced_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__041b6f65034582f626434a70543ffb7bbb2dfd668b7f720e4ebb46962097f571)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advancedOptions", value)

    @builtins.property
    @jsii.member(jsii_name="advancedSecurityOptions")
    def advanced_security_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.AdvancedSecurityOptionsInputProperty"]]:
        '''Specifies options for fine-grained access control.

        If you specify advanced security options, you must also enable node-to-node encryption ( `NodeToNodeEncryptionOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodetonodeencryptionoptions.html>`_ ) and encryption at rest ( `EncryptionAtRestOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html>`_ ). You must also enable ``EnforceHTTPS`` within `DomainEndpointOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html>`_ , which requires HTTPS for all traffic to the domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-advancedsecurityoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.AdvancedSecurityOptionsInputProperty"]], jsii.get(self, "advancedSecurityOptions"))

    @advanced_security_options.setter
    def advanced_security_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.AdvancedSecurityOptionsInputProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e71ab581d18d39ebfd3cb9df3c0530e66f21152477a586e1ff207563f530392a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advancedSecurityOptions", value)

    @builtins.property
    @jsii.member(jsii_name="clusterConfig")
    def cluster_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.ClusterConfigProperty"]]:
        '''Container for the cluster configuration of a domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-clusterconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.ClusterConfigProperty"]], jsii.get(self, "clusterConfig"))

    @cluster_config.setter
    def cluster_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.ClusterConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__242b992e488742e7382b665de9bc48b487807dd4416778e0aee2a1e324f8974f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterConfig", value)

    @builtins.property
    @jsii.member(jsii_name="cognitoOptions")
    def cognito_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.CognitoOptionsProperty"]]:
        '''Configures OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-cognitooptions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.CognitoOptionsProperty"]], jsii.get(self, "cognitoOptions"))

    @cognito_options.setter
    def cognito_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.CognitoOptionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3614ecc7f4b8420734656233a2f956baa143be7659f6b26ba66725f8fedbb44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cognitoOptions", value)

    @builtins.property
    @jsii.member(jsii_name="domainEndpointOptions")
    def domain_endpoint_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.DomainEndpointOptionsProperty"]]:
        '''Specifies additional options for the domain endpoint, such as whether to require HTTPS for all traffic or whether to use a custom endpoint rather than the default endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-domainendpointoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.DomainEndpointOptionsProperty"]], jsii.get(self, "domainEndpointOptions"))

    @domain_endpoint_options.setter
    def domain_endpoint_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.DomainEndpointOptionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__467d8bb30a1a9a2fe2117aef5a6d8bfb5ec07fa3bc23bbf1fbbb4597d57b7f52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainEndpointOptions", value)

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''A name for the OpenSearch Service domain.

        For valid values, see the `DomainName <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/configuration-api.html#configuration-api-datatypes-domainname>`_ data type in the *Amazon OpenSearch Service Developer Guide* . If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the domain name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .

        Required when creating a new domain.
        .. epigraph::

           If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-domainname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cdb234b06dcc6b6876f053c097db924df470823a5c55f7cf5d7bc84852f28d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="ebsOptions")
    def ebs_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.EBSOptionsProperty"]]:
        '''The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the OpenSearch Service domain.

        For more information, see `EBS volume size limits <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource>`_ in the *Amazon OpenSearch Service Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-ebsoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.EBSOptionsProperty"]], jsii.get(self, "ebsOptions"))

    @ebs_options.setter
    def ebs_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.EBSOptionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aac15720e304f08b6ec450459d7caf824fff24df602e01025bb6f94ceaee64c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ebsOptions", value)

    @builtins.property
    @jsii.member(jsii_name="encryptionAtRestOptions")
    def encryption_at_rest_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.EncryptionAtRestOptionsProperty"]]:
        '''Whether the domain should encrypt data at rest, and if so, the AWS KMS key to use.

        See `Encryption of data at rest for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/encryption-at-rest.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-encryptionatrestoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.EncryptionAtRestOptionsProperty"]], jsii.get(self, "encryptionAtRestOptions"))

    @encryption_at_rest_options.setter
    def encryption_at_rest_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.EncryptionAtRestOptionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5753eb4890b1cc9901049bc8be92991b585c1c9cc739bd9a4c920dfdfb21cac5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionAtRestOptions", value)

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The version of OpenSearch to use.

        The value must be in the format ``OpenSearch_X.Y`` or ``Elasticsearch_X.Y`` . If not specified, the latest version of OpenSearch is used. For information about the versions that OpenSearch Service supports, see `Supported versions of OpenSearch and Elasticsearch <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html#choosing-version>`_ in the *Amazon OpenSearch Service Developer Guide* .

        If you set the `EnableVersionUpgrade <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-upgradeopensearchdomain>`_ update policy to ``true`` , you can update ``EngineVersion`` without interruption. When ``EnableVersionUpgrade`` is set to ``false`` , or is not specified, updating ``EngineVersion`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-engineversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineVersion"))

    @engine_version.setter
    def engine_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cdf4c8a2f195f3245aae8f0c2d15bff93731e5f344d5047d4a81c827ade7690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineVersion", value)

    @builtins.property
    @jsii.member(jsii_name="logPublishingOptions")
    def log_publishing_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.LogPublishingOptionProperty"]]]]:
        '''An object with one or more of the following keys: ``SEARCH_SLOW_LOGS`` , ``ES_APPLICATION_LOGS`` , ``INDEX_SLOW_LOGS`` , ``AUDIT_LOGS`` , depending on the types of logs you want to publish.

        Each key needs a valid ``LogPublishingOption`` value. For the full syntax, see the `examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#aws-resource-opensearchservice-domain--examples>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-logpublishingoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.LogPublishingOptionProperty"]]]], jsii.get(self, "logPublishingOptions"))

    @log_publishing_options.setter
    def log_publishing_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.LogPublishingOptionProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62686f38ab3ab553d30950b11f210da58b70537c74ee6795d993522b28cc9f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logPublishingOptions", value)

    @builtins.property
    @jsii.member(jsii_name="nodeToNodeEncryptionOptions")
    def node_to_node_encryption_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.NodeToNodeEncryptionOptionsProperty"]]:
        '''Specifies whether node-to-node encryption is enabled.

        See `Node-to-node encryption for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ntn.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-nodetonodeencryptionoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.NodeToNodeEncryptionOptionsProperty"]], jsii.get(self, "nodeToNodeEncryptionOptions"))

    @node_to_node_encryption_options.setter
    def node_to_node_encryption_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.NodeToNodeEncryptionOptionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eed7c1edf733b2d581498f06f02e652f5a6cba31e96572ef643c85ca3d54f56b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeToNodeEncryptionOptions", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotOptions")
    def snapshot_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.SnapshotOptionsProperty"]]:
        '''*DEPRECATED* .

        The automated snapshot configuration for the OpenSearch Service domain indexes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-snapshotoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.SnapshotOptionsProperty"]], jsii.get(self, "snapshotOptions"))

    @snapshot_options.setter
    def snapshot_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.SnapshotOptionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb9e010b765cf3c33343c3ab86c8881efdc8d59ca39f83db3764a4a7ed914232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotOptions", value)

    @builtins.property
    @jsii.member(jsii_name="vpcOptions")
    def vpc_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.VPCOptionsProperty"]]:
        '''The virtual private cloud (VPC) configuration for the OpenSearch Service domain.

        For more information, see `Launching your Amazon OpenSearch Service domains within a VPC <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vpc.html>`_ in the *Amazon OpenSearch Service Developer Guide* .

        If you remove this entity altogether, along with its associated properties, it causes a replacement. You might encounter this scenario if you're updating your security configuration from a VPC to a public endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-vpcoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.VPCOptionsProperty"]], jsii.get(self, "vpcOptions"))

    @vpc_options.setter
    def vpc_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.VPCOptionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__680d80155d5ae83f04e3424363da6e02e0b84f79409cd217183b2aa29d023cc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcOptions", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opensearchservice.CfnDomain.AdvancedSecurityOptionsInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "internal_user_database_enabled": "internalUserDatabaseEnabled",
            "master_user_options": "masterUserOptions",
        },
    )
    class AdvancedSecurityOptionsInputProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            internal_user_database_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            master_user_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDomain.MasterUserOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies options for fine-grained access control.

            If you specify advanced security options, you must also enable node-to-node encryption ( `NodeToNodeEncryptionOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodetonodeencryptionoptions.html>`_ ) and encryption at rest ( `EncryptionAtRestOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html>`_ ). You must also enable ``EnforceHTTPS`` within `DomainEndpointOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html>`_ , which requires HTTPS for all traffic to the domain.

            :param enabled: True to enable fine-grained access control. You must also enable encryption of data at rest and node-to-node encryption. See `Fine-grained access control in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html>`_ .
            :param internal_user_database_enabled: True to enable the internal user database.
            :param master_user_options: Specifies information about the master user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_opensearchservice as opensearchservice
                
                advanced_security_options_input_property = opensearchservice.CfnDomain.AdvancedSecurityOptionsInputProperty(
                    enabled=False,
                    internal_user_database_enabled=False,
                    master_user_options=opensearchservice.CfnDomain.MasterUserOptionsProperty(
                        master_user_arn="masterUserArn",
                        master_user_name="masterUserName",
                        master_user_password="masterUserPassword"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8f87c66d463ead5b66c67cb7e353724ea434618eeb817a8c7242128e5591a2f4)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument internal_user_database_enabled", value=internal_user_database_enabled, expected_type=type_hints["internal_user_database_enabled"])
                check_type(argname="argument master_user_options", value=master_user_options, expected_type=type_hints["master_user_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if internal_user_database_enabled is not None:
                self._values["internal_user_database_enabled"] = internal_user_database_enabled
            if master_user_options is not None:
                self._values["master_user_options"] = master_user_options

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''True to enable fine-grained access control.

            You must also enable encryption of data at rest and node-to-node encryption. See `Fine-grained access control in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html#cfn-opensearchservice-domain-advancedsecurityoptionsinput-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def internal_user_database_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''True to enable the internal user database.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html#cfn-opensearchservice-domain-advancedsecurityoptionsinput-internaluserdatabaseenabled
            '''
            result = self._values.get("internal_user_database_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def master_user_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.MasterUserOptionsProperty"]]:
            '''Specifies information about the master user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html#cfn-opensearchservice-domain-advancedsecurityoptionsinput-masteruseroptions
            '''
            result = self._values.get("master_user_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.MasterUserOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdvancedSecurityOptionsInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opensearchservice.CfnDomain.ClusterConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dedicated_master_count": "dedicatedMasterCount",
            "dedicated_master_enabled": "dedicatedMasterEnabled",
            "dedicated_master_type": "dedicatedMasterType",
            "instance_count": "instanceCount",
            "instance_type": "instanceType",
            "warm_count": "warmCount",
            "warm_enabled": "warmEnabled",
            "warm_type": "warmType",
            "zone_awareness_config": "zoneAwarenessConfig",
            "zone_awareness_enabled": "zoneAwarenessEnabled",
        },
    )
    class ClusterConfigProperty:
        def __init__(
            self,
            *,
            dedicated_master_count: typing.Optional[jsii.Number] = None,
            dedicated_master_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            dedicated_master_type: typing.Optional[builtins.str] = None,
            instance_count: typing.Optional[jsii.Number] = None,
            instance_type: typing.Optional[builtins.str] = None,
            warm_count: typing.Optional[jsii.Number] = None,
            warm_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            warm_type: typing.Optional[builtins.str] = None,
            zone_awareness_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDomain.ZoneAwarenessConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            zone_awareness_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''The cluster configuration for the OpenSearch Service domain.

            You can specify options such as the instance type and the number of instances. For more information, see `Creating and managing Amazon OpenSearch Service domains <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/createupdatedomains.html>`_ in the *Amazon OpenSearch Service Developer Guide* .

            :param dedicated_master_count: The number of instances to use for the master node. If you specify this property, you must specify ``true`` for the ``DedicatedMasterEnabled`` property.
            :param dedicated_master_enabled: Indicates whether to use a dedicated master node for the OpenSearch Service domain. A dedicated master node is a cluster node that performs cluster management tasks, but doesn't hold data or respond to data upload requests. Dedicated master nodes offload cluster management tasks to increase the stability of your search clusters. See `Dedicated master nodes in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-dedicatedmasternodes.html>`_ .
            :param dedicated_master_type: The hardware configuration of the computer that hosts the dedicated master node, such as ``m3.medium.search`` . If you specify this property, you must specify ``true`` for the ``DedicatedMasterEnabled`` property. For valid values, see `Supported instance types in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-instance-types.html>`_ .
            :param instance_count: The number of data nodes (instances) to use in the OpenSearch Service domain.
            :param instance_type: The instance type for your data nodes, such as ``m3.medium.search`` . For valid values, see `Supported instance types in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-instance-types.html>`_ .
            :param warm_count: The number of warm nodes in the cluster.
            :param warm_enabled: Whether to enable UltraWarm storage for the cluster. See `UltraWarm storage for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ultrawarm.html>`_ .
            :param warm_type: The instance type for the cluster's warm nodes.
            :param zone_awareness_config: Specifies zone awareness configuration options. Only use if ``ZoneAwarenessEnabled`` is ``true`` .
            :param zone_awareness_enabled: Indicates whether to enable zone awareness for the OpenSearch Service domain. When you enable zone awareness, OpenSearch Service allocates the nodes and replica index shards that belong to a cluster across two Availability Zones (AZs) in the same region to prevent data loss and minimize downtime in the event of node or data center failure. Don't enable zone awareness if your cluster has no replica index shards or is a single-node cluster. For more information, see `Configuring a multi-AZ domain in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-multiaz.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_opensearchservice as opensearchservice
                
                cluster_config_property = opensearchservice.CfnDomain.ClusterConfigProperty(
                    dedicated_master_count=123,
                    dedicated_master_enabled=False,
                    dedicated_master_type="dedicatedMasterType",
                    instance_count=123,
                    instance_type="instanceType",
                    warm_count=123,
                    warm_enabled=False,
                    warm_type="warmType",
                    zone_awareness_config=opensearchservice.CfnDomain.ZoneAwarenessConfigProperty(
                        availability_zone_count=123
                    ),
                    zone_awareness_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ed78939109a8eb24a53c2761721d4eebf02f0588cdc51ed60b33c7fe73885a55)
                check_type(argname="argument dedicated_master_count", value=dedicated_master_count, expected_type=type_hints["dedicated_master_count"])
                check_type(argname="argument dedicated_master_enabled", value=dedicated_master_enabled, expected_type=type_hints["dedicated_master_enabled"])
                check_type(argname="argument dedicated_master_type", value=dedicated_master_type, expected_type=type_hints["dedicated_master_type"])
                check_type(argname="argument instance_count", value=instance_count, expected_type=type_hints["instance_count"])
                check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                check_type(argname="argument warm_count", value=warm_count, expected_type=type_hints["warm_count"])
                check_type(argname="argument warm_enabled", value=warm_enabled, expected_type=type_hints["warm_enabled"])
                check_type(argname="argument warm_type", value=warm_type, expected_type=type_hints["warm_type"])
                check_type(argname="argument zone_awareness_config", value=zone_awareness_config, expected_type=type_hints["zone_awareness_config"])
                check_type(argname="argument zone_awareness_enabled", value=zone_awareness_enabled, expected_type=type_hints["zone_awareness_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dedicated_master_count is not None:
                self._values["dedicated_master_count"] = dedicated_master_count
            if dedicated_master_enabled is not None:
                self._values["dedicated_master_enabled"] = dedicated_master_enabled
            if dedicated_master_type is not None:
                self._values["dedicated_master_type"] = dedicated_master_type
            if instance_count is not None:
                self._values["instance_count"] = instance_count
            if instance_type is not None:
                self._values["instance_type"] = instance_type
            if warm_count is not None:
                self._values["warm_count"] = warm_count
            if warm_enabled is not None:
                self._values["warm_enabled"] = warm_enabled
            if warm_type is not None:
                self._values["warm_type"] = warm_type
            if zone_awareness_config is not None:
                self._values["zone_awareness_config"] = zone_awareness_config
            if zone_awareness_enabled is not None:
                self._values["zone_awareness_enabled"] = zone_awareness_enabled

        @builtins.property
        def dedicated_master_count(self) -> typing.Optional[jsii.Number]:
            '''The number of instances to use for the master node.

            If you specify this property, you must specify ``true`` for the ``DedicatedMasterEnabled`` property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-dedicatedmastercount
            '''
            result = self._values.get("dedicated_master_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def dedicated_master_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether to use a dedicated master node for the OpenSearch Service domain.

            A dedicated master node is a cluster node that performs cluster management tasks, but doesn't hold data or respond to data upload requests. Dedicated master nodes offload cluster management tasks to increase the stability of your search clusters. See `Dedicated master nodes in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-dedicatedmasternodes.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-dedicatedmasterenabled
            '''
            result = self._values.get("dedicated_master_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def dedicated_master_type(self) -> typing.Optional[builtins.str]:
            '''The hardware configuration of the computer that hosts the dedicated master node, such as ``m3.medium.search`` . If you specify this property, you must specify ``true`` for the ``DedicatedMasterEnabled`` property. For valid values, see `Supported instance types in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-instance-types.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-dedicatedmastertype
            '''
            result = self._values.get("dedicated_master_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_count(self) -> typing.Optional[jsii.Number]:
            '''The number of data nodes (instances) to use in the OpenSearch Service domain.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-instancecount
            '''
            result = self._values.get("instance_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def instance_type(self) -> typing.Optional[builtins.str]:
            '''The instance type for your data nodes, such as ``m3.medium.search`` . For valid values, see `Supported instance types in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-instance-types.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-instancetype
            '''
            result = self._values.get("instance_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def warm_count(self) -> typing.Optional[jsii.Number]:
            '''The number of warm nodes in the cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-warmcount
            '''
            result = self._values.get("warm_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def warm_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Whether to enable UltraWarm storage for the cluster.

            See `UltraWarm storage for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ultrawarm.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-warmenabled
            '''
            result = self._values.get("warm_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def warm_type(self) -> typing.Optional[builtins.str]:
            '''The instance type for the cluster's warm nodes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-warmtype
            '''
            result = self._values.get("warm_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def zone_awareness_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.ZoneAwarenessConfigProperty"]]:
            '''Specifies zone awareness configuration options.

            Only use if ``ZoneAwarenessEnabled`` is ``true`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-zoneawarenessconfig
            '''
            result = self._values.get("zone_awareness_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDomain.ZoneAwarenessConfigProperty"]], result)

        @builtins.property
        def zone_awareness_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether to enable zone awareness for the OpenSearch Service domain.

            When you enable zone awareness, OpenSearch Service allocates the nodes and replica index shards that belong to a cluster across two Availability Zones (AZs) in the same region to prevent data loss and minimize downtime in the event of node or data center failure. Don't enable zone awareness if your cluster has no replica index shards or is a single-node cluster. For more information, see `Configuring a multi-AZ domain in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-multiaz.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-zoneawarenessenabled
            '''
            result = self._values.get("zone_awareness_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ClusterConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opensearchservice.CfnDomain.CognitoOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "identity_pool_id": "identityPoolId",
            "role_arn": "roleArn",
            "user_pool_id": "userPoolId",
        },
    )
    class CognitoOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            identity_pool_id: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            user_pool_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configures OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards.

            :param enabled: Whether to enable or disable Amazon Cognito authentication for OpenSearch Dashboards. See `Amazon Cognito authentication for OpenSearch Dashboards <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/cognito-auth.html>`_ .
            :param identity_pool_id: The Amazon Cognito identity pool ID that you want OpenSearch Service to use for OpenSearch Dashboards authentication. Required if you enabled Cognito Authentication for OpenSearch Dashboards.
            :param role_arn: The ``AmazonOpenSearchServiceCognitoAccess`` role that allows OpenSearch Service to configure your user pool and identity pool. Required if you enabled Cognito Authentication for OpenSearch Dashboards.
            :param user_pool_id: The Amazon Cognito user pool ID that you want OpenSearch Service to use for OpenSearch Dashboards authentication. Required if you enabled Cognito Authentication for OpenSearch Dashboards.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-cognitooptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_opensearchservice as opensearchservice
                
                cognito_options_property = opensearchservice.CfnDomain.CognitoOptionsProperty(
                    enabled=False,
                    identity_pool_id="identityPoolId",
                    role_arn="roleArn",
                    user_pool_id="userPoolId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__747b9bca01a1280a0776eea7463efd93d8497450ff33345130c175838f88431e)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument identity_pool_id", value=identity_pool_id, expected_type=type_hints["identity_pool_id"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if identity_pool_id is not None:
                self._values["identity_pool_id"] = identity_pool_id
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if user_pool_id is not None:
                self._values["user_pool_id"] = user_pool_id

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Whether to enable or disable Amazon Cognito authentication for OpenSearch Dashboards.

            See `Amazon Cognito authentication for OpenSearch Dashboards <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/cognito-auth.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-cognitooptions.html#cfn-opensearchservice-domain-cognitooptions-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def identity_pool_id(self) -> typing.Optional[builtins.str]:
            '''The Amazon Cognito identity pool ID that you want OpenSearch Service to use for OpenSearch Dashboards authentication.

            Required if you enabled Cognito Authentication for OpenSearch Dashboards.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-cognitooptions.html#cfn-opensearchservice-domain-cognitooptions-identitypoolid
            '''
            result = self._values.get("identity_pool_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ``AmazonOpenSearchServiceCognitoAccess`` role that allows OpenSearch Service to configure your user pool and identity pool.

            Required if you enabled Cognito Authentication for OpenSearch Dashboards.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-cognitooptions.html#cfn-opensearchservice-domain-cognitooptions-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_pool_id(self) -> typing.Optional[builtins.str]:
            '''The Amazon Cognito user pool ID that you want OpenSearch Service to use for OpenSearch Dashboards authentication.

            Required if you enabled Cognito Authentication for OpenSearch Dashboards.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-cognitooptions.html#cfn-opensearchservice-domain-cognitooptions-userpoolid
            '''
            result = self._values.get("user_pool_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CognitoOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opensearchservice.CfnDomain.DomainEndpointOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_endpoint": "customEndpoint",
            "custom_endpoint_certificate_arn": "customEndpointCertificateArn",
            "custom_endpoint_enabled": "customEndpointEnabled",
            "enforce_https": "enforceHttps",
            "tls_security_policy": "tlsSecurityPolicy",
        },
    )
    class DomainEndpointOptionsProperty:
        def __init__(
            self,
            *,
            custom_endpoint: typing.Optional[builtins.str] = None,
            custom_endpoint_certificate_arn: typing.Optional[builtins.str] = None,
            custom_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            enforce_https: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            tls_security_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies additional options for the domain endpoint, such as whether to require HTTPS for all traffic or whether to use a custom endpoint rather than the default endpoint.

            :param custom_endpoint: The fully qualified URL for your custom endpoint. Required if you enabled a custom endpoint for the domain.
            :param custom_endpoint_certificate_arn: The AWS Certificate Manager ARN for your domain's SSL/TLS certificate. Required if you enabled a custom endpoint for the domain.
            :param custom_endpoint_enabled: True to enable a custom endpoint for the domain. If enabled, you must also provide values for ``CustomEndpoint`` and ``CustomEndpointCertificateArn`` .
            :param enforce_https: True to require that all traffic to the domain arrive over HTTPS. Required if you enable fine-grained access control in `AdvancedSecurityOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .
            :param tls_security_policy: The minimum TLS version required for traffic to the domain. Valid values are TLS 1.0 (default) or 1.2:. - ``Policy-Min-TLS-1-0-2019-07`` - ``Policy-Min-TLS-1-2-2019-07``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_opensearchservice as opensearchservice
                
                domain_endpoint_options_property = opensearchservice.CfnDomain.DomainEndpointOptionsProperty(
                    custom_endpoint="customEndpoint",
                    custom_endpoint_certificate_arn="customEndpointCertificateArn",
                    custom_endpoint_enabled=False,
                    enforce_https=False,
                    tls_security_policy="tlsSecurityPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1e0f1ebd053a19a9765012da8fa39a12d4c64adc3e925edb61c05f47d6d5bafd)
                check_type(argname="argument custom_endpoint", value=custom_endpoint, expected_type=type_hints["custom_endpoint"])
                check_type(argname="argument custom_endpoint_certificate_arn", value=custom_endpoint_certificate_arn, expected_type=type_hints["custom_endpoint_certificate_arn"])
                check_type(argname="argument custom_endpoint_enabled", value=custom_endpoint_enabled, expected_type=type_hints["custom_endpoint_enabled"])
                check_type(argname="argument enforce_https", value=enforce_https, expected_type=type_hints["enforce_https"])
                check_type(argname="argument tls_security_policy", value=tls_security_policy, expected_type=type_hints["tls_security_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_endpoint is not None:
                self._values["custom_endpoint"] = custom_endpoint
            if custom_endpoint_certificate_arn is not None:
                self._values["custom_endpoint_certificate_arn"] = custom_endpoint_certificate_arn
            if custom_endpoint_enabled is not None:
                self._values["custom_endpoint_enabled"] = custom_endpoint_enabled
            if enforce_https is not None:
                self._values["enforce_https"] = enforce_https
            if tls_security_policy is not None:
                self._values["tls_security_policy"] = tls_security_policy

        @builtins.property
        def custom_endpoint(self) -> typing.Optional[builtins.str]:
            '''The fully qualified URL for your custom endpoint.

            Required if you enabled a custom endpoint for the domain.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html#cfn-opensearchservice-domain-domainendpointoptions-customendpoint
            '''
            result = self._values.get("custom_endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_endpoint_certificate_arn(self) -> typing.Optional[builtins.str]:
            '''The AWS Certificate Manager ARN for your domain's SSL/TLS certificate.

            Required if you enabled a custom endpoint for the domain.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html#cfn-opensearchservice-domain-domainendpointoptions-customendpointcertificatearn
            '''
            result = self._values.get("custom_endpoint_certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_endpoint_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''True to enable a custom endpoint for the domain.

            If enabled, you must also provide values for ``CustomEndpoint`` and ``CustomEndpointCertificateArn`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html#cfn-opensearchservice-domain-domainendpointoptions-customendpointenabled
            '''
            result = self._values.get("custom_endpoint_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def enforce_https(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''True to require that all traffic to the domain arrive over HTTPS.

            Required if you enable fine-grained access control in `AdvancedSecurityOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html#cfn-opensearchservice-domain-domainendpointoptions-enforcehttps
            '''
            result = self._values.get("enforce_https")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def tls_security_policy(self) -> typing.Optional[builtins.str]:
            '''The minimum TLS version required for traffic to the domain. Valid values are TLS 1.0 (default) or 1.2:.

            - ``Policy-Min-TLS-1-0-2019-07``
            - ``Policy-Min-TLS-1-2-2019-07``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html#cfn-opensearchservice-domain-domainendpointoptions-tlssecuritypolicy
            '''
            result = self._values.get("tls_security_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainEndpointOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opensearchservice.CfnDomain.EBSOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ebs_enabled": "ebsEnabled",
            "iops": "iops",
            "throughput": "throughput",
            "volume_size": "volumeSize",
            "volume_type": "volumeType",
        },
    )
    class EBSOptionsProperty:
        def __init__(
            self,
            *,
            ebs_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            iops: typing.Optional[jsii.Number] = None,
            throughput: typing.Optional[jsii.Number] = None,
            volume_size: typing.Optional[jsii.Number] = None,
            volume_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the OpenSearch Service domain.

            For more information, see `EBS volume size limits <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource>`_ in the *Amazon OpenSearch Service Developer Guide* .

            :param ebs_enabled: Specifies whether Amazon EBS volumes are attached to data nodes in the OpenSearch Service domain.
            :param iops: The number of I/O operations per second (IOPS) that the volume supports. This property applies only to the ``gp3`` and provisioned IOPS EBS volume types.
            :param throughput: The throughput (in MiB/s) of the EBS volumes attached to data nodes. Applies only to the ``gp3`` volume type.
            :param volume_size: The size (in GiB) of the EBS volume for each data node. The minimum and maximum size of an EBS volume depends on the EBS volume type and the instance type to which it is attached. For more information, see `EBS volume size limits <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource>`_ in the *Amazon OpenSearch Service Developer Guide* .
            :param volume_type: The EBS volume type to use with the OpenSearch Service domain. If you choose ``gp3`` , you must also specify values for ``Iops`` and ``Throughput`` . For more information about each type, see `Amazon EBS volume types <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html>`_ in the *Amazon EC2 User Guide for Linux Instances* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-ebsoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_opensearchservice as opensearchservice
                
                e_bSOptions_property = opensearchservice.CfnDomain.EBSOptionsProperty(
                    ebs_enabled=False,
                    iops=123,
                    throughput=123,
                    volume_size=123,
                    volume_type="volumeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e9ed144ec5311c74d520e94e8ae2791f77cb085510ed92685de9777bca37e53e)
                check_type(argname="argument ebs_enabled", value=ebs_enabled, expected_type=type_hints["ebs_enabled"])
                check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
                check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
                check_type(argname="argument volume_size", value=volume_size, expected_type=type_hints["volume_size"])
                check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ebs_enabled is not None:
                self._values["ebs_enabled"] = ebs_enabled
            if iops is not None:
                self._values["iops"] = iops
            if throughput is not None:
                self._values["throughput"] = throughput
            if volume_size is not None:
                self._values["volume_size"] = volume_size
            if volume_type is not None:
                self._values["volume_type"] = volume_type

        @builtins.property
        def ebs_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Specifies whether Amazon EBS volumes are attached to data nodes in the OpenSearch Service domain.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-ebsoptions.html#cfn-opensearchservice-domain-ebsoptions-ebsenabled
            '''
            result = self._values.get("ebs_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            '''The number of I/O operations per second (IOPS) that the volume supports.

            This property applies only to the ``gp3`` and provisioned IOPS EBS volume types.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-ebsoptions.html#cfn-opensearchservice-domain-ebsoptions-iops
            '''
            result = self._values.get("iops")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throughput(self) -> typing.Optional[jsii.Number]:
            '''The throughput (in MiB/s) of the EBS volumes attached to data nodes.

            Applies only to the ``gp3`` volume type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-ebsoptions.html#cfn-opensearchservice-domain-ebsoptions-throughput
            '''
            result = self._values.get("throughput")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_size(self) -> typing.Optional[jsii.Number]:
            '''The size (in GiB) of the EBS volume for each data node.

            The minimum and maximum size of an EBS volume depends on the EBS volume type and the instance type to which it is attached. For more information, see `EBS volume size limits <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource>`_ in the *Amazon OpenSearch Service Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-ebsoptions.html#cfn-opensearchservice-domain-ebsoptions-volumesize
            '''
            result = self._values.get("volume_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_type(self) -> typing.Optional[builtins.str]:
            '''The EBS volume type to use with the OpenSearch Service domain.

            If you choose ``gp3`` , you must also specify values for ``Iops`` and ``Throughput`` . For more information about each type, see `Amazon EBS volume types <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html>`_ in the *Amazon EC2 User Guide for Linux Instances* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-ebsoptions.html#cfn-opensearchservice-domain-ebsoptions-volumetype
            '''
            result = self._values.get("volume_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EBSOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opensearchservice.CfnDomain.EncryptionAtRestOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "kms_key_id": "kmsKeyId"},
    )
    class EncryptionAtRestOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            kms_key_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Whether the domain should encrypt data at rest, and if so, the AWS Key Management Service key to use.

            :param enabled: Specify ``true`` to enable encryption at rest. Required if you enable fine-grained access control in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .
            :param kms_key_id: The KMS key ID. Takes the form ``1a2a3a4-1a2a-3a4a-5a6a-1a2a3a4a5a6a`` . Required if you enable encryption at rest. You can also use ``keyAlias`` as a value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_opensearchservice as opensearchservice
                
                encryption_at_rest_options_property = opensearchservice.CfnDomain.EncryptionAtRestOptionsProperty(
                    enabled=False,
                    kms_key_id="kmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e65cc1fcde96ef2a65a601aa6c28b404f48a52192a50ccd7f9210e94f602e5c1)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Specify ``true`` to enable encryption at rest.

            Required if you enable fine-grained access control in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html#cfn-opensearchservice-domain-encryptionatrestoptions-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The KMS key ID. Takes the form ``1a2a3a4-1a2a-3a4a-5a6a-1a2a3a4a5a6a`` . Required if you enable encryption at rest.

            You can also use ``keyAlias`` as a value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html#cfn-opensearchservice-domain-encryptionatrestoptions-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionAtRestOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opensearchservice.CfnDomain.LogPublishingOptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logs_log_group_arn": "cloudWatchLogsLogGroupArn",
            "enabled": "enabled",
        },
    )
    class LogPublishingOptionProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_log_group_arn: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Specifies whether the OpenSearch Service domain publishes application, search slow logs, or index slow logs to Amazon CloudWatch.

            Each option must be an object of name ``SEARCH_SLOW_LOGS`` , ``ES_APPLICATION_LOGS`` , ``INDEX_SLOW_LOGS`` , or ``AUDIT_LOGS`` depending on the type of logs you want to publish. For the full syntax, see the `examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#aws-resource-opensearchservice-domain--examples>`_ .

            Before you enable log publishing, you need to create a CloudWatch log group and provide OpenSearch Service the correct permissions to write to it. To learn more, see `Enabling log publishing ( AWS CloudFormation) <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/createdomain-configure-slow-logs.html#createdomain-configure-slow-logs-cfn>`_ .

            :param cloud_watch_logs_log_group_arn: Specifies the CloudWatch log group to publish to. Required if you enable log publishing.
            :param enabled: If ``true`` , enables the publishing of logs to CloudWatch. Default: ``false`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-logpublishingoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_opensearchservice as opensearchservice
                
                log_publishing_option_property = opensearchservice.CfnDomain.LogPublishingOptionProperty(
                    cloud_watch_logs_log_group_arn="cloudWatchLogsLogGroupArn",
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__468b348664e23264beb9c28791bbbb254375124e79c8ec806d17c29e2654f0b4)
                check_type(argname="argument cloud_watch_logs_log_group_arn", value=cloud_watch_logs_log_group_arn, expected_type=type_hints["cloud_watch_logs_log_group_arn"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs_log_group_arn is not None:
                self._values["cloud_watch_logs_log_group_arn"] = cloud_watch_logs_log_group_arn
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def cloud_watch_logs_log_group_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the CloudWatch log group to publish to.

            Required if you enable log publishing.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-logpublishingoption.html#cfn-opensearchservice-domain-logpublishingoption-cloudwatchlogsloggrouparn
            '''
            result = self._values.get("cloud_watch_logs_log_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''If ``true`` , enables the publishing of logs to CloudWatch.

            Default: ``false`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-logpublishingoption.html#cfn-opensearchservice-domain-logpublishingoption-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogPublishingOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opensearchservice.CfnDomain.MasterUserOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "master_user_arn": "masterUserArn",
            "master_user_name": "masterUserName",
            "master_user_password": "masterUserPassword",
        },
    )
    class MasterUserOptionsProperty:
        def __init__(
            self,
            *,
            master_user_arn: typing.Optional[builtins.str] = None,
            master_user_name: typing.Optional[builtins.str] = None,
            master_user_password: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies information about the master user.

            Required if if ``InternalUserDatabaseEnabled`` is true in `AdvancedSecurityOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            :param master_user_arn: Amazon Resource Name (ARN) for the master user. The ARN can point to an IAM user or role. This property is required for Amazon Cognito to work, and it must match the role configured for Cognito. Only specify if ``InternalUserDatabaseEnabled`` is false in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .
            :param master_user_name: Username for the master user. Only specify if ``InternalUserDatabaseEnabled`` is true in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ . If you don't want to specify this value directly within the template, you can use a `dynamic reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html>`_ instead.
            :param master_user_password: Password for the master user. Only specify if ``InternalUserDatabaseEnabled`` is true in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ . If you don't want to specify this value directly within the template, you can use a `dynamic reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html>`_ instead.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-masteruseroptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_opensearchservice as opensearchservice
                
                master_user_options_property = opensearchservice.CfnDomain.MasterUserOptionsProperty(
                    master_user_arn="masterUserArn",
                    master_user_name="masterUserName",
                    master_user_password="masterUserPassword"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7cbfd5bd4a3f00831d0cb0353b1d5661d2f081018d20b97c25cf8ff4ca1d7292)
                check_type(argname="argument master_user_arn", value=master_user_arn, expected_type=type_hints["master_user_arn"])
                check_type(argname="argument master_user_name", value=master_user_name, expected_type=type_hints["master_user_name"])
                check_type(argname="argument master_user_password", value=master_user_password, expected_type=type_hints["master_user_password"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if master_user_arn is not None:
                self._values["master_user_arn"] = master_user_arn
            if master_user_name is not None:
                self._values["master_user_name"] = master_user_name
            if master_user_password is not None:
                self._values["master_user_password"] = master_user_password

        @builtins.property
        def master_user_arn(self) -> typing.Optional[builtins.str]:
            '''Amazon Resource Name (ARN) for the master user.

            The ARN can point to an IAM user or role. This property is required for Amazon Cognito to work, and it must match the role configured for Cognito. Only specify if ``InternalUserDatabaseEnabled`` is false in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-masteruseroptions.html#cfn-opensearchservice-domain-masteruseroptions-masteruserarn
            '''
            result = self._values.get("master_user_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def master_user_name(self) -> typing.Optional[builtins.str]:
            '''Username for the master user. Only specify if ``InternalUserDatabaseEnabled`` is true in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            If you don't want to specify this value directly within the template, you can use a `dynamic reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html>`_ instead.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-masteruseroptions.html#cfn-opensearchservice-domain-masteruseroptions-masterusername
            '''
            result = self._values.get("master_user_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def master_user_password(self) -> typing.Optional[builtins.str]:
            '''Password for the master user. Only specify if ``InternalUserDatabaseEnabled`` is true in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            If you don't want to specify this value directly within the template, you can use a `dynamic reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html>`_ instead.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-masteruseroptions.html#cfn-opensearchservice-domain-masteruseroptions-masteruserpassword
            '''
            result = self._values.get("master_user_password")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MasterUserOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opensearchservice.CfnDomain.NodeToNodeEncryptionOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class NodeToNodeEncryptionOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Specifies options for node-to-node encryption.

            :param enabled: Specifies to enable or disable node-to-node encryption on the domain. Required if you enable fine-grained access control in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodetonodeencryptionoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_opensearchservice as opensearchservice
                
                node_to_node_encryption_options_property = opensearchservice.CfnDomain.NodeToNodeEncryptionOptionsProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6bdc3a722fc6292f992cb4d4c8115c8ef6884a075fda2285e9605a00f9d8e009)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Specifies to enable or disable node-to-node encryption on the domain.

            Required if you enable fine-grained access control in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodetonodeencryptionoptions.html#cfn-opensearchservice-domain-nodetonodeencryptionoptions-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeToNodeEncryptionOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opensearchservice.CfnDomain.ServiceSoftwareOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "automated_update_date": "automatedUpdateDate",
            "cancellable": "cancellable",
            "current_version": "currentVersion",
            "description": "description",
            "new_version": "newVersion",
            "optional_deployment": "optionalDeployment",
            "update_available": "updateAvailable",
            "update_status": "updateStatus",
        },
    )
    class ServiceSoftwareOptionsProperty:
        def __init__(
            self,
            *,
            automated_update_date: typing.Optional[builtins.str] = None,
            cancellable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            current_version: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            new_version: typing.Optional[builtins.str] = None,
            optional_deployment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            update_available: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            update_status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The current status of the service software for an Amazon OpenSearch Service domain.

            For more information, see `Service software updates in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/service-software.html>`_ .

            :param automated_update_date: The timestamp, in Epoch time, until which you can manually request a service software update. After this date, we automatically update your service software.
            :param cancellable: True if you're able to cancel your service software version update. False if you can't cancel your service software update.
            :param current_version: The current service software version present on the domain.
            :param description: A description of the service software update status.
            :param new_version: The new service software version, if one is available.
            :param optional_deployment: True if a service software is never automatically updated. False if a service software is automatically updated after the automated update date.
            :param update_available: True if you're able to update your service software version. False if you can't update your service software version.
            :param update_status: The status of your service software update.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_opensearchservice as opensearchservice
                
                service_software_options_property = opensearchservice.CfnDomain.ServiceSoftwareOptionsProperty(
                    automated_update_date="automatedUpdateDate",
                    cancellable=False,
                    current_version="currentVersion",
                    description="description",
                    new_version="newVersion",
                    optional_deployment=False,
                    update_available=False,
                    update_status="updateStatus"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__720b21a31a155cfee7407b649b1d2f6b11a2e2ffb0b61f4aa338065e495efc2a)
                check_type(argname="argument automated_update_date", value=automated_update_date, expected_type=type_hints["automated_update_date"])
                check_type(argname="argument cancellable", value=cancellable, expected_type=type_hints["cancellable"])
                check_type(argname="argument current_version", value=current_version, expected_type=type_hints["current_version"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument new_version", value=new_version, expected_type=type_hints["new_version"])
                check_type(argname="argument optional_deployment", value=optional_deployment, expected_type=type_hints["optional_deployment"])
                check_type(argname="argument update_available", value=update_available, expected_type=type_hints["update_available"])
                check_type(argname="argument update_status", value=update_status, expected_type=type_hints["update_status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automated_update_date is not None:
                self._values["automated_update_date"] = automated_update_date
            if cancellable is not None:
                self._values["cancellable"] = cancellable
            if current_version is not None:
                self._values["current_version"] = current_version
            if description is not None:
                self._values["description"] = description
            if new_version is not None:
                self._values["new_version"] = new_version
            if optional_deployment is not None:
                self._values["optional_deployment"] = optional_deployment
            if update_available is not None:
                self._values["update_available"] = update_available
            if update_status is not None:
                self._values["update_status"] = update_status

        @builtins.property
        def automated_update_date(self) -> typing.Optional[builtins.str]:
            '''The timestamp, in Epoch time, until which you can manually request a service software update.

            After this date, we automatically update your service software.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-automatedupdatedate
            '''
            result = self._values.get("automated_update_date")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cancellable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''True if you're able to cancel your service software version update.

            False if you can't cancel your service software update.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-cancellable
            '''
            result = self._values.get("cancellable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def current_version(self) -> typing.Optional[builtins.str]:
            '''The current service software version present on the domain.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-currentversion
            '''
            result = self._values.get("current_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description of the service software update status.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def new_version(self) -> typing.Optional[builtins.str]:
            '''The new service software version, if one is available.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-newversion
            '''
            result = self._values.get("new_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def optional_deployment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''True if a service software is never automatically updated.

            False if a service software is automatically updated after the automated update date.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-optionaldeployment
            '''
            result = self._values.get("optional_deployment")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def update_available(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''True if you're able to update your service software version.

            False if you can't update your service software version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-updateavailable
            '''
            result = self._values.get("update_available")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def update_status(self) -> typing.Optional[builtins.str]:
            '''The status of your service software update.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-updatestatus
            '''
            result = self._values.get("update_status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceSoftwareOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opensearchservice.CfnDomain.SnapshotOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"automated_snapshot_start_hour": "automatedSnapshotStartHour"},
    )
    class SnapshotOptionsProperty:
        def __init__(
            self,
            *,
            automated_snapshot_start_hour: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''*DEPRECATED* .

            This setting is only relevant to domains running legacy Elasticsearch OSS versions earlier than 5.3. It does not apply to OpenSearch domains.

            The automated snapshot configuration for the OpenSearch Service domain indexes.

            :param automated_snapshot_start_hour: The hour in UTC during which the service takes an automated daily snapshot of the indexes in the OpenSearch Service domain. For example, if you specify 0, OpenSearch Service takes an automated snapshot everyday between midnight and 1 am. You can specify a value between 0 and 23.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-snapshotoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_opensearchservice as opensearchservice
                
                snapshot_options_property = opensearchservice.CfnDomain.SnapshotOptionsProperty(
                    automated_snapshot_start_hour=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b01f6bca5cd9ac1be691e3fdccc21ec99cf16fc0cdf741d31a0f37d33e1e9161)
                check_type(argname="argument automated_snapshot_start_hour", value=automated_snapshot_start_hour, expected_type=type_hints["automated_snapshot_start_hour"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automated_snapshot_start_hour is not None:
                self._values["automated_snapshot_start_hour"] = automated_snapshot_start_hour

        @builtins.property
        def automated_snapshot_start_hour(self) -> typing.Optional[jsii.Number]:
            '''The hour in UTC during which the service takes an automated daily snapshot of the indexes in the OpenSearch Service domain.

            For example, if you specify 0, OpenSearch Service takes an automated snapshot everyday between midnight and 1 am. You can specify a value between 0 and 23.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-snapshotoptions.html#cfn-opensearchservice-domain-snapshotoptions-automatedsnapshotstarthour
            '''
            result = self._values.get("automated_snapshot_start_hour")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnapshotOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opensearchservice.CfnDomain.VPCOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VPCOptionsProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The virtual private cloud (VPC) configuration for the OpenSearch Service domain.

            For more information, see `Launching your Amazon OpenSearch Service domains using a VPC <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vpc.html>`_ in the *Amazon OpenSearch Service Developer Guide* .

            :param security_group_ids: The list of security group IDs that are associated with the VPC endpoints for the domain. If you don't provide a security group ID, OpenSearch Service uses the default security group for the VPC. To learn more, see `Security groups for your VPC <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html>`_ in the *Amazon VPC User Guide* .
            :param subnet_ids: Provide one subnet ID for each Availability Zone that your domain uses. For example, you must specify three subnet IDs for a three-AZ domain. To learn more, see `VPCs and subnets <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html>`_ in the *Amazon VPC User Guide* . If you specify more than one subnet, you must also configure ``ZoneAwarenessEnabled`` and ``ZoneAwarenessConfig`` within `ClusterConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html>`_ , otherwise you'll see the error "You must specify exactly one subnet" during template creation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-vpcoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_opensearchservice as opensearchservice
                
                v_pCOptions_property = opensearchservice.CfnDomain.VPCOptionsProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__42e1db3011ae6d361340c52c4ad7597b1717df028126e25f89097ad2689b7538)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of security group IDs that are associated with the VPC endpoints for the domain.

            If you don't provide a security group ID, OpenSearch Service uses the default security group for the VPC. To learn more, see `Security groups for your VPC <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html>`_ in the *Amazon VPC User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-vpcoptions.html#cfn-opensearchservice-domain-vpcoptions-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Provide one subnet ID for each Availability Zone that your domain uses.

            For example, you must specify three subnet IDs for a three-AZ domain. To learn more, see `VPCs and subnets <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html>`_ in the *Amazon VPC User Guide* .

            If you specify more than one subnet, you must also configure ``ZoneAwarenessEnabled`` and ``ZoneAwarenessConfig`` within `ClusterConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html>`_ , otherwise you'll see the error "You must specify exactly one subnet" during template creation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-vpcoptions.html#cfn-opensearchservice-domain-vpcoptions-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VPCOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opensearchservice.CfnDomain.ZoneAwarenessConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"availability_zone_count": "availabilityZoneCount"},
    )
    class ZoneAwarenessConfigProperty:
        def __init__(
            self,
            *,
            availability_zone_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies zone awareness configuration options.

            Only use if ``ZoneAwarenessEnabled`` is ``true`` .

            :param availability_zone_count: If you enabled multiple Availability Zones (AZs), the number of AZs that you want the domain to use. Valid values are ``2`` and ``3`` . Default is 2.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-zoneawarenessconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_opensearchservice as opensearchservice
                
                zone_awareness_config_property = opensearchservice.CfnDomain.ZoneAwarenessConfigProperty(
                    availability_zone_count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c2eb69ed389f020e0e97452d58705bd6d389a453376bfc3d24e80f838a013c26)
                check_type(argname="argument availability_zone_count", value=availability_zone_count, expected_type=type_hints["availability_zone_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_zone_count is not None:
                self._values["availability_zone_count"] = availability_zone_count

        @builtins.property
        def availability_zone_count(self) -> typing.Optional[jsii.Number]:
            '''If you enabled multiple Availability Zones (AZs), the number of AZs that you want the domain to use.

            Valid values are ``2`` and ``3`` . Default is 2.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-zoneawarenessconfig.html#cfn-opensearchservice-domain-zoneawarenessconfig-availabilityzonecount
            '''
            result = self._values.get("availability_zone_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZoneAwarenessConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opensearchservice.CfnDomainProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_policies": "accessPolicies",
        "advanced_options": "advancedOptions",
        "advanced_security_options": "advancedSecurityOptions",
        "cluster_config": "clusterConfig",
        "cognito_options": "cognitoOptions",
        "domain_endpoint_options": "domainEndpointOptions",
        "domain_name": "domainName",
        "ebs_options": "ebsOptions",
        "encryption_at_rest_options": "encryptionAtRestOptions",
        "engine_version": "engineVersion",
        "log_publishing_options": "logPublishingOptions",
        "node_to_node_encryption_options": "nodeToNodeEncryptionOptions",
        "snapshot_options": "snapshotOptions",
        "tags": "tags",
        "vpc_options": "vpcOptions",
    },
)
class CfnDomainProps:
    def __init__(
        self,
        *,
        access_policies: typing.Any = None,
        advanced_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        advanced_security_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.AdvancedSecurityOptionsInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        cluster_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.ClusterConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        cognito_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.CognitoOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        domain_endpoint_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.DomainEndpointOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        ebs_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.EBSOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        encryption_at_rest_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.EncryptionAtRestOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        engine_version: typing.Optional[builtins.str] = None,
        log_publishing_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.LogPublishingOptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        node_to_node_encryption_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.NodeToNodeEncryptionOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        snapshot_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.SnapshotOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.VPCOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDomain``.

        :param access_policies: An AWS Identity and Access Management ( IAM ) policy document that specifies who can access the OpenSearch Service domain and their permissions. For more information, see `Configuring access policies <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ac.html#ac-creating>`_ in the *Amazon OpenSearch Service Developer Guide* .
        :param advanced_options: Additional options to specify for the OpenSearch Service domain. For more information, see `AdvancedOptions <https://docs.aws.amazon.com/opensearch-service/latest/APIReference/API_CreateDomain.html#API_CreateDomain_RequestBody>`_ in the OpenSearch Service API reference.
        :param advanced_security_options: Specifies options for fine-grained access control. If you specify advanced security options, you must also enable node-to-node encryption ( `NodeToNodeEncryptionOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodetonodeencryptionoptions.html>`_ ) and encryption at rest ( `EncryptionAtRestOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html>`_ ). You must also enable ``EnforceHTTPS`` within `DomainEndpointOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html>`_ , which requires HTTPS for all traffic to the domain.
        :param cluster_config: Container for the cluster configuration of a domain.
        :param cognito_options: Configures OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards.
        :param domain_endpoint_options: Specifies additional options for the domain endpoint, such as whether to require HTTPS for all traffic or whether to use a custom endpoint rather than the default endpoint.
        :param domain_name: A name for the OpenSearch Service domain. For valid values, see the `DomainName <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/configuration-api.html#configuration-api-datatypes-domainname>`_ data type in the *Amazon OpenSearch Service Developer Guide* . If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the domain name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . Required when creating a new domain. .. epigraph:: If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param ebs_options: The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the OpenSearch Service domain. For more information, see `EBS volume size limits <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource>`_ in the *Amazon OpenSearch Service Developer Guide* .
        :param encryption_at_rest_options: Whether the domain should encrypt data at rest, and if so, the AWS KMS key to use. See `Encryption of data at rest for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/encryption-at-rest.html>`_ .
        :param engine_version: The version of OpenSearch to use. The value must be in the format ``OpenSearch_X.Y`` or ``Elasticsearch_X.Y`` . If not specified, the latest version of OpenSearch is used. For information about the versions that OpenSearch Service supports, see `Supported versions of OpenSearch and Elasticsearch <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html#choosing-version>`_ in the *Amazon OpenSearch Service Developer Guide* . If you set the `EnableVersionUpgrade <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-upgradeopensearchdomain>`_ update policy to ``true`` , you can update ``EngineVersion`` without interruption. When ``EnableVersionUpgrade`` is set to ``false`` , or is not specified, updating ``EngineVersion`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .
        :param log_publishing_options: An object with one or more of the following keys: ``SEARCH_SLOW_LOGS`` , ``ES_APPLICATION_LOGS`` , ``INDEX_SLOW_LOGS`` , ``AUDIT_LOGS`` , depending on the types of logs you want to publish. Each key needs a valid ``LogPublishingOption`` value. For the full syntax, see the `examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#aws-resource-opensearchservice-domain--examples>`_ .
        :param node_to_node_encryption_options: Specifies whether node-to-node encryption is enabled. See `Node-to-node encryption for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ntn.html>`_ .
        :param snapshot_options: *DEPRECATED* . The automated snapshot configuration for the OpenSearch Service domain indexes.
        :param tags: An arbitrary set of tags (key–value pairs) to associate with the OpenSearch Service domain.
        :param vpc_options: The virtual private cloud (VPC) configuration for the OpenSearch Service domain. For more information, see `Launching your Amazon OpenSearch Service domains within a VPC <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vpc.html>`_ in the *Amazon OpenSearch Service Developer Guide* . If you remove this entity altogether, along with its associated properties, it causes a replacement. You might encounter this scenario if you're updating your security configuration from a VPC to a public endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_opensearchservice as opensearchservice
            
            # access_policies: Any
            
            cfn_domain_props = opensearchservice.CfnDomainProps(
                access_policies=access_policies,
                advanced_options={
                    "advanced_options_key": "advancedOptions"
                },
                advanced_security_options=opensearchservice.CfnDomain.AdvancedSecurityOptionsInputProperty(
                    enabled=False,
                    internal_user_database_enabled=False,
                    master_user_options=opensearchservice.CfnDomain.MasterUserOptionsProperty(
                        master_user_arn="masterUserArn",
                        master_user_name="masterUserName",
                        master_user_password="masterUserPassword"
                    )
                ),
                cluster_config=opensearchservice.CfnDomain.ClusterConfigProperty(
                    dedicated_master_count=123,
                    dedicated_master_enabled=False,
                    dedicated_master_type="dedicatedMasterType",
                    instance_count=123,
                    instance_type="instanceType",
                    warm_count=123,
                    warm_enabled=False,
                    warm_type="warmType",
                    zone_awareness_config=opensearchservice.CfnDomain.ZoneAwarenessConfigProperty(
                        availability_zone_count=123
                    ),
                    zone_awareness_enabled=False
                ),
                cognito_options=opensearchservice.CfnDomain.CognitoOptionsProperty(
                    enabled=False,
                    identity_pool_id="identityPoolId",
                    role_arn="roleArn",
                    user_pool_id="userPoolId"
                ),
                domain_endpoint_options=opensearchservice.CfnDomain.DomainEndpointOptionsProperty(
                    custom_endpoint="customEndpoint",
                    custom_endpoint_certificate_arn="customEndpointCertificateArn",
                    custom_endpoint_enabled=False,
                    enforce_https=False,
                    tls_security_policy="tlsSecurityPolicy"
                ),
                domain_name="domainName",
                ebs_options=opensearchservice.CfnDomain.EBSOptionsProperty(
                    ebs_enabled=False,
                    iops=123,
                    throughput=123,
                    volume_size=123,
                    volume_type="volumeType"
                ),
                encryption_at_rest_options=opensearchservice.CfnDomain.EncryptionAtRestOptionsProperty(
                    enabled=False,
                    kms_key_id="kmsKeyId"
                ),
                engine_version="engineVersion",
                log_publishing_options={
                    "log_publishing_options_key": opensearchservice.CfnDomain.LogPublishingOptionProperty(
                        cloud_watch_logs_log_group_arn="cloudWatchLogsLogGroupArn",
                        enabled=False
                    )
                },
                node_to_node_encryption_options=opensearchservice.CfnDomain.NodeToNodeEncryptionOptionsProperty(
                    enabled=False
                ),
                snapshot_options=opensearchservice.CfnDomain.SnapshotOptionsProperty(
                    automated_snapshot_start_hour=123
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_options=opensearchservice.CfnDomain.VPCOptionsProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86a3d8056fad835d634340f38e80e1175dbedfc662c8e4344ea597a7679dbb3f)
            check_type(argname="argument access_policies", value=access_policies, expected_type=type_hints["access_policies"])
            check_type(argname="argument advanced_options", value=advanced_options, expected_type=type_hints["advanced_options"])
            check_type(argname="argument advanced_security_options", value=advanced_security_options, expected_type=type_hints["advanced_security_options"])
            check_type(argname="argument cluster_config", value=cluster_config, expected_type=type_hints["cluster_config"])
            check_type(argname="argument cognito_options", value=cognito_options, expected_type=type_hints["cognito_options"])
            check_type(argname="argument domain_endpoint_options", value=domain_endpoint_options, expected_type=type_hints["domain_endpoint_options"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument ebs_options", value=ebs_options, expected_type=type_hints["ebs_options"])
            check_type(argname="argument encryption_at_rest_options", value=encryption_at_rest_options, expected_type=type_hints["encryption_at_rest_options"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument log_publishing_options", value=log_publishing_options, expected_type=type_hints["log_publishing_options"])
            check_type(argname="argument node_to_node_encryption_options", value=node_to_node_encryption_options, expected_type=type_hints["node_to_node_encryption_options"])
            check_type(argname="argument snapshot_options", value=snapshot_options, expected_type=type_hints["snapshot_options"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_options", value=vpc_options, expected_type=type_hints["vpc_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_policies is not None:
            self._values["access_policies"] = access_policies
        if advanced_options is not None:
            self._values["advanced_options"] = advanced_options
        if advanced_security_options is not None:
            self._values["advanced_security_options"] = advanced_security_options
        if cluster_config is not None:
            self._values["cluster_config"] = cluster_config
        if cognito_options is not None:
            self._values["cognito_options"] = cognito_options
        if domain_endpoint_options is not None:
            self._values["domain_endpoint_options"] = domain_endpoint_options
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if ebs_options is not None:
            self._values["ebs_options"] = ebs_options
        if encryption_at_rest_options is not None:
            self._values["encryption_at_rest_options"] = encryption_at_rest_options
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if log_publishing_options is not None:
            self._values["log_publishing_options"] = log_publishing_options
        if node_to_node_encryption_options is not None:
            self._values["node_to_node_encryption_options"] = node_to_node_encryption_options
        if snapshot_options is not None:
            self._values["snapshot_options"] = snapshot_options
        if tags is not None:
            self._values["tags"] = tags
        if vpc_options is not None:
            self._values["vpc_options"] = vpc_options

    @builtins.property
    def access_policies(self) -> typing.Any:
        '''An AWS Identity and Access Management ( IAM ) policy document that specifies who can access the OpenSearch Service domain and their permissions.

        For more information, see `Configuring access policies <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ac.html#ac-creating>`_ in the *Amazon OpenSearch Service Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-accesspolicies
        '''
        result = self._values.get("access_policies")
        return typing.cast(typing.Any, result)

    @builtins.property
    def advanced_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''Additional options to specify for the OpenSearch Service domain.

        For more information, see `AdvancedOptions <https://docs.aws.amazon.com/opensearch-service/latest/APIReference/API_CreateDomain.html#API_CreateDomain_RequestBody>`_ in the OpenSearch Service API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-advancedoptions
        '''
        result = self._values.get("advanced_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def advanced_security_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.AdvancedSecurityOptionsInputProperty]]:
        '''Specifies options for fine-grained access control.

        If you specify advanced security options, you must also enable node-to-node encryption ( `NodeToNodeEncryptionOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodetonodeencryptionoptions.html>`_ ) and encryption at rest ( `EncryptionAtRestOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html>`_ ). You must also enable ``EnforceHTTPS`` within `DomainEndpointOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html>`_ , which requires HTTPS for all traffic to the domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-advancedsecurityoptions
        '''
        result = self._values.get("advanced_security_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.AdvancedSecurityOptionsInputProperty]], result)

    @builtins.property
    def cluster_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.ClusterConfigProperty]]:
        '''Container for the cluster configuration of a domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-clusterconfig
        '''
        result = self._values.get("cluster_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.ClusterConfigProperty]], result)

    @builtins.property
    def cognito_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.CognitoOptionsProperty]]:
        '''Configures OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-cognitooptions
        '''
        result = self._values.get("cognito_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.CognitoOptionsProperty]], result)

    @builtins.property
    def domain_endpoint_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.DomainEndpointOptionsProperty]]:
        '''Specifies additional options for the domain endpoint, such as whether to require HTTPS for all traffic or whether to use a custom endpoint rather than the default endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-domainendpointoptions
        '''
        result = self._values.get("domain_endpoint_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.DomainEndpointOptionsProperty]], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''A name for the OpenSearch Service domain.

        For valid values, see the `DomainName <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/configuration-api.html#configuration-api-datatypes-domainname>`_ data type in the *Amazon OpenSearch Service Developer Guide* . If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the domain name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .

        Required when creating a new domain.
        .. epigraph::

           If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ebs_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.EBSOptionsProperty]]:
        '''The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the OpenSearch Service domain.

        For more information, see `EBS volume size limits <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource>`_ in the *Amazon OpenSearch Service Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-ebsoptions
        '''
        result = self._values.get("ebs_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.EBSOptionsProperty]], result)

    @builtins.property
    def encryption_at_rest_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.EncryptionAtRestOptionsProperty]]:
        '''Whether the domain should encrypt data at rest, and if so, the AWS KMS key to use.

        See `Encryption of data at rest for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/encryption-at-rest.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-encryptionatrestoptions
        '''
        result = self._values.get("encryption_at_rest_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.EncryptionAtRestOptionsProperty]], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The version of OpenSearch to use.

        The value must be in the format ``OpenSearch_X.Y`` or ``Elasticsearch_X.Y`` . If not specified, the latest version of OpenSearch is used. For information about the versions that OpenSearch Service supports, see `Supported versions of OpenSearch and Elasticsearch <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html#choosing-version>`_ in the *Amazon OpenSearch Service Developer Guide* .

        If you set the `EnableVersionUpgrade <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-upgradeopensearchdomain>`_ update policy to ``true`` , you can update ``EngineVersion`` without interruption. When ``EnableVersionUpgrade`` is set to ``false`` , or is not specified, updating ``EngineVersion`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_publishing_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.LogPublishingOptionProperty]]]]:
        '''An object with one or more of the following keys: ``SEARCH_SLOW_LOGS`` , ``ES_APPLICATION_LOGS`` , ``INDEX_SLOW_LOGS`` , ``AUDIT_LOGS`` , depending on the types of logs you want to publish.

        Each key needs a valid ``LogPublishingOption`` value. For the full syntax, see the `examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#aws-resource-opensearchservice-domain--examples>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-logpublishingoptions
        '''
        result = self._values.get("log_publishing_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.LogPublishingOptionProperty]]]], result)

    @builtins.property
    def node_to_node_encryption_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.NodeToNodeEncryptionOptionsProperty]]:
        '''Specifies whether node-to-node encryption is enabled.

        See `Node-to-node encryption for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ntn.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-nodetonodeencryptionoptions
        '''
        result = self._values.get("node_to_node_encryption_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.NodeToNodeEncryptionOptionsProperty]], result)

    @builtins.property
    def snapshot_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.SnapshotOptionsProperty]]:
        '''*DEPRECATED* .

        The automated snapshot configuration for the OpenSearch Service domain indexes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-snapshotoptions
        '''
        result = self._values.get("snapshot_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.SnapshotOptionsProperty]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An arbitrary set of tags (key–value pairs) to associate with the OpenSearch Service domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def vpc_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.VPCOptionsProperty]]:
        '''The virtual private cloud (VPC) configuration for the OpenSearch Service domain.

        For more information, see `Launching your Amazon OpenSearch Service domains within a VPC <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vpc.html>`_ in the *Amazon OpenSearch Service Developer Guide* .

        If you remove this entity altogether, along with its associated properties, it causes a replacement. You might encounter this scenario if you're updating your security configuration from a VPC to a public endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-vpcoptions
        '''
        result = self._values.get("vpc_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.VPCOptionsProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opensearchservice.CognitoOptions",
    jsii_struct_bases=[],
    name_mapping={
        "identity_pool_id": "identityPoolId",
        "role": "role",
        "user_pool_id": "userPoolId",
    },
)
class CognitoOptions:
    def __init__(
        self,
        *,
        identity_pool_id: builtins.str,
        role: _aws_cdk_aws_iam_940a1ce0.IRole,
        user_pool_id: builtins.str,
    ) -> None:
        '''Configures Amazon OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards.

        :param identity_pool_id: The Amazon Cognito identity pool ID that you want Amazon OpenSearch Service to use for OpenSearch Dashboards authentication.
        :param role: A role that allows Amazon OpenSearch Service to configure your user pool and identity pool. It must have the ``AmazonESCognitoAccess`` policy attached to it.
        :param user_pool_id: The Amazon Cognito user pool ID that you want Amazon OpenSearch Service to use for OpenSearch Dashboards authentication.

        :see: https://docs.aws.amazon.com/opensearch-service/latest/developerguide/cognito-auth.html
        :exampleMetadata: fixture=migrate-opensearch infused

        Example::

            opensearch.Domain(self, "Domain",
                cognito_dashboards_auth=opensearch.CognitoOptions(
                    identity_pool_id="test-identity-pool-id",
                    user_pool_id="test-user-pool-id",
                    role=role
                ),
                version=open_search_version
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__005d853a7ee069b215a408691cbefec960068404ab07fba9407ab8fb85f03413)
            check_type(argname="argument identity_pool_id", value=identity_pool_id, expected_type=type_hints["identity_pool_id"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "identity_pool_id": identity_pool_id,
            "role": role,
            "user_pool_id": user_pool_id,
        }

    @builtins.property
    def identity_pool_id(self) -> builtins.str:
        '''The Amazon Cognito identity pool ID that you want Amazon OpenSearch Service to use for OpenSearch Dashboards authentication.'''
        result = self._values.get("identity_pool_id")
        assert result is not None, "Required property 'identity_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> _aws_cdk_aws_iam_940a1ce0.IRole:
        '''A role that allows Amazon OpenSearch Service to configure your user pool and identity pool.

        It must have the ``AmazonESCognitoAccess`` policy attached to it.

        :see: https://docs.aws.amazon.com/opensearch-service/latest/developerguide/cognito-auth.html#cognito-auth-prereq
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.IRole, result)

    @builtins.property
    def user_pool_id(self) -> builtins.str:
        '''The Amazon Cognito user pool ID that you want Amazon OpenSearch Service to use for OpenSearch Dashboards authentication.'''
        result = self._values.get("user_pool_id")
        assert result is not None, "Required property 'user_pool_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opensearchservice.CustomEndpointOptions",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "certificate": "certificate",
        "hosted_zone": "hostedZone",
    },
)
class CustomEndpointOptions:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        certificate: typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate] = None,
        hosted_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
    ) -> None:
        '''Configures a custom domain endpoint for the Amazon OpenSearch Service domain.

        :param domain_name: The custom domain name to assign.
        :param certificate: The certificate to use. Default: - create a new one
        :param hosted_zone: The hosted zone in Route53 to create the CNAME record in. Default: - do not create a CNAME

        :exampleMetadata: infused

        Example::

            opensearch.Domain(self, "Domain",
                version=opensearch.EngineVersion.OPENSEARCH_1_0,
                custom_endpoint=opensearch.CustomEndpointOptions(
                    domain_name="search.example.com"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da8aaf8726efe2585d177d847453ee5bd7133208c41eee250796e2cb77fa4be7)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument hosted_zone", value=hosted_zone, expected_type=type_hints["hosted_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
        }
        if certificate is not None:
            self._values["certificate"] = certificate
        if hosted_zone is not None:
            self._values["hosted_zone"] = hosted_zone

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''The custom domain name to assign.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate]:
        '''The certificate to use.

        :default: - create a new one
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate], result)

    @builtins.property
    def hosted_zone(self) -> typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone]:
        '''The hosted zone in Route53 to create the CNAME record in.

        :default: - do not create a CNAME
        '''
        result = self._values.get("hosted_zone")
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomEndpointOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opensearchservice.DomainAttributes",
    jsii_struct_bases=[],
    name_mapping={"domain_arn": "domainArn", "domain_endpoint": "domainEndpoint"},
)
class DomainAttributes:
    def __init__(
        self,
        *,
        domain_arn: builtins.str,
        domain_endpoint: builtins.str,
    ) -> None:
        '''Reference to an Amazon OpenSearch Service domain.

        :param domain_arn: The ARN of the Amazon OpenSearch Service domain.
        :param domain_endpoint: The domain endpoint of the Amazon OpenSearch Service domain.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_opensearchservice as opensearchservice
            
            domain_attributes = opensearchservice.DomainAttributes(
                domain_arn="domainArn",
                domain_endpoint="domainEndpoint"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1311fcf0967428ad2f85232918c5b0744a1a64beb3f8f79a441e548c7aead055)
            check_type(argname="argument domain_arn", value=domain_arn, expected_type=type_hints["domain_arn"])
            check_type(argname="argument domain_endpoint", value=domain_endpoint, expected_type=type_hints["domain_endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_arn": domain_arn,
            "domain_endpoint": domain_endpoint,
        }

    @builtins.property
    def domain_arn(self) -> builtins.str:
        '''The ARN of the Amazon OpenSearch Service domain.'''
        result = self._values.get("domain_arn")
        assert result is not None, "Required property 'domain_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_endpoint(self) -> builtins.str:
        '''The domain endpoint of the Amazon OpenSearch Service domain.'''
        result = self._values.get("domain_endpoint")
        assert result is not None, "Required property 'domain_endpoint' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opensearchservice.DomainProps",
    jsii_struct_bases=[],
    name_mapping={
        "version": "version",
        "access_policies": "accessPolicies",
        "advanced_options": "advancedOptions",
        "automated_snapshot_start_hour": "automatedSnapshotStartHour",
        "capacity": "capacity",
        "cognito_dashboards_auth": "cognitoDashboardsAuth",
        "custom_endpoint": "customEndpoint",
        "domain_name": "domainName",
        "ebs": "ebs",
        "enable_version_upgrade": "enableVersionUpgrade",
        "encryption_at_rest": "encryptionAtRest",
        "enforce_https": "enforceHttps",
        "fine_grained_access_control": "fineGrainedAccessControl",
        "logging": "logging",
        "node_to_node_encryption": "nodeToNodeEncryption",
        "removal_policy": "removalPolicy",
        "security_groups": "securityGroups",
        "tls_security_policy": "tlsSecurityPolicy",
        "use_unsigned_basic_auth": "useUnsignedBasicAuth",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "zone_awareness": "zoneAwareness",
    },
)
class DomainProps:
    def __init__(
        self,
        *,
        version: "EngineVersion",
        access_policies: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.PolicyStatement]] = None,
        advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        automated_snapshot_start_hour: typing.Optional[jsii.Number] = None,
        capacity: typing.Optional[typing.Union[CapacityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        cognito_dashboards_auth: typing.Optional[typing.Union[CognitoOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_endpoint: typing.Optional[typing.Union[CustomEndpointOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        ebs: typing.Optional[typing.Union["EbsOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_version_upgrade: typing.Optional[builtins.bool] = None,
        encryption_at_rest: typing.Optional[typing.Union["EncryptionAtRestOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        enforce_https: typing.Optional[builtins.bool] = None,
        fine_grained_access_control: typing.Optional[typing.Union[AdvancedSecurityOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[typing.Union["LoggingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        node_to_node_encryption: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
        tls_security_policy: typing.Optional["TLSSecurityPolicy"] = None,
        use_unsigned_basic_auth: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
        zone_awareness: typing.Optional[typing.Union["ZoneAwarenessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Properties for an Amazon OpenSearch Service domain.

        :param version: The Elasticsearch/OpenSearch version that your domain will leverage.
        :param access_policies: Domain access policies. Default: - No access policies.
        :param advanced_options: Additional options to specify for the Amazon OpenSearch Service domain. Default: - no advanced options are specified
        :param automated_snapshot_start_hour: The hour in UTC during which the service takes an automated daily snapshot of the indices in the Amazon OpenSearch Service domain. Only applies for Elasticsearch versions below 5.3. Default: - Hourly automated snapshots not used
        :param capacity: The cluster capacity configuration for the Amazon OpenSearch Service domain. Default: - 1 r5.large.search data node; no dedicated master nodes.
        :param cognito_dashboards_auth: Configures Amazon OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards. Default: - Cognito not used for authentication to OpenSearch Dashboards.
        :param custom_endpoint: To configure a custom domain configure these options. If you specify a Route53 hosted zone it will create a CNAME record and use DNS validation for the certificate Default: - no custom domain endpoint will be configured
        :param domain_name: Enforces a particular physical domain name. Default: - A name will be auto-generated.
        :param ebs: The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the Amazon OpenSearch Service domain. Default: - 10 GiB General Purpose (SSD) volumes per node.
        :param enable_version_upgrade: To upgrade an Amazon OpenSearch Service domain to a new version, rather than replacing the entire domain resource, use the EnableVersionUpgrade update policy. Default: - false
        :param encryption_at_rest: Encryption at rest options for the cluster. Default: - No encryption at rest
        :param enforce_https: True to require that all traffic to the domain arrive over HTTPS. Default: - false
        :param fine_grained_access_control: Specifies options for fine-grained access control. Requires Elasticsearch version 6.7 or later or OpenSearch version 1.0 or later. Enabling fine-grained access control also requires encryption of data at rest and node-to-node encryption, along with enforced HTTPS. Default: - fine-grained access control is disabled
        :param logging: Configuration log publishing configuration options. Default: - No logs are published
        :param node_to_node_encryption: Specify true to enable node to node encryption. Requires Elasticsearch version 6.0 or later or OpenSearch version 1.0 or later. Default: - Node to node encryption is not enabled.
        :param removal_policy: Policy to apply when the domain is removed from the stack. Default: RemovalPolicy.RETAIN
        :param security_groups: The list of security groups that are associated with the VPC endpoints for the domain. Only used if ``vpc`` is specified. Default: - One new security group is created.
        :param tls_security_policy: The minimum TLS version required for traffic to the domain. Default: - TLSSecurityPolicy.TLS_1_0
        :param use_unsigned_basic_auth: Configures the domain so that unsigned basic auth is enabled. If no master user is provided a default master user with username ``admin`` and a dynamically generated password stored in KMS is created. The password can be retrieved by getting ``masterUserPassword`` from the domain instance. Setting this to true will also add an access policy that allows unsigned access, enable node to node encryption, encryption at rest. If conflicting settings are encountered (like disabling encryption at rest) enabling this setting will cause a failure. Default: - false
        :param vpc: Place the domain inside this VPC. Default: - Domain is not placed in a VPC.
        :param vpc_subnets: The specific vpc subnets the domain will be placed in. You must provide one subnet for each Availability Zone that your domain uses. For example, you must specify three subnet IDs for a three Availability Zone domain. Only used if ``vpc`` is specified. Default: - All private subnets.
        :param zone_awareness: The cluster zone awareness configuration for the Amazon OpenSearch Service domain. Default: - no zone awareness (1 AZ)

        :exampleMetadata: infused

        Example::

            domain = opensearch.Domain(self, "Domain",
                version=opensearch.EngineVersion.OPENSEARCH_1_0,
                ebs=opensearch.EbsOptions(
                    volume_size=100,
                    volume_type=ec2.EbsDeviceVolumeType.GENERAL_PURPOSE_SSD
                ),
                node_to_node_encryption=True,
                encryption_at_rest=opensearch.EncryptionAtRestOptions(
                    enabled=True
                )
            )
        '''
        if isinstance(capacity, dict):
            capacity = CapacityConfig(**capacity)
        if isinstance(cognito_dashboards_auth, dict):
            cognito_dashboards_auth = CognitoOptions(**cognito_dashboards_auth)
        if isinstance(custom_endpoint, dict):
            custom_endpoint = CustomEndpointOptions(**custom_endpoint)
        if isinstance(ebs, dict):
            ebs = EbsOptions(**ebs)
        if isinstance(encryption_at_rest, dict):
            encryption_at_rest = EncryptionAtRestOptions(**encryption_at_rest)
        if isinstance(fine_grained_access_control, dict):
            fine_grained_access_control = AdvancedSecurityOptions(**fine_grained_access_control)
        if isinstance(logging, dict):
            logging = LoggingOptions(**logging)
        if isinstance(zone_awareness, dict):
            zone_awareness = ZoneAwarenessConfig(**zone_awareness)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5db33233ff5477597442204050938b92d0810e8d0d8921b187751b5e380b16d)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument access_policies", value=access_policies, expected_type=type_hints["access_policies"])
            check_type(argname="argument advanced_options", value=advanced_options, expected_type=type_hints["advanced_options"])
            check_type(argname="argument automated_snapshot_start_hour", value=automated_snapshot_start_hour, expected_type=type_hints["automated_snapshot_start_hour"])
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument cognito_dashboards_auth", value=cognito_dashboards_auth, expected_type=type_hints["cognito_dashboards_auth"])
            check_type(argname="argument custom_endpoint", value=custom_endpoint, expected_type=type_hints["custom_endpoint"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument ebs", value=ebs, expected_type=type_hints["ebs"])
            check_type(argname="argument enable_version_upgrade", value=enable_version_upgrade, expected_type=type_hints["enable_version_upgrade"])
            check_type(argname="argument encryption_at_rest", value=encryption_at_rest, expected_type=type_hints["encryption_at_rest"])
            check_type(argname="argument enforce_https", value=enforce_https, expected_type=type_hints["enforce_https"])
            check_type(argname="argument fine_grained_access_control", value=fine_grained_access_control, expected_type=type_hints["fine_grained_access_control"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument node_to_node_encryption", value=node_to_node_encryption, expected_type=type_hints["node_to_node_encryption"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument tls_security_policy", value=tls_security_policy, expected_type=type_hints["tls_security_policy"])
            check_type(argname="argument use_unsigned_basic_auth", value=use_unsigned_basic_auth, expected_type=type_hints["use_unsigned_basic_auth"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument zone_awareness", value=zone_awareness, expected_type=type_hints["zone_awareness"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "version": version,
        }
        if access_policies is not None:
            self._values["access_policies"] = access_policies
        if advanced_options is not None:
            self._values["advanced_options"] = advanced_options
        if automated_snapshot_start_hour is not None:
            self._values["automated_snapshot_start_hour"] = automated_snapshot_start_hour
        if capacity is not None:
            self._values["capacity"] = capacity
        if cognito_dashboards_auth is not None:
            self._values["cognito_dashboards_auth"] = cognito_dashboards_auth
        if custom_endpoint is not None:
            self._values["custom_endpoint"] = custom_endpoint
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if ebs is not None:
            self._values["ebs"] = ebs
        if enable_version_upgrade is not None:
            self._values["enable_version_upgrade"] = enable_version_upgrade
        if encryption_at_rest is not None:
            self._values["encryption_at_rest"] = encryption_at_rest
        if enforce_https is not None:
            self._values["enforce_https"] = enforce_https
        if fine_grained_access_control is not None:
            self._values["fine_grained_access_control"] = fine_grained_access_control
        if logging is not None:
            self._values["logging"] = logging
        if node_to_node_encryption is not None:
            self._values["node_to_node_encryption"] = node_to_node_encryption
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if tls_security_policy is not None:
            self._values["tls_security_policy"] = tls_security_policy
        if use_unsigned_basic_auth is not None:
            self._values["use_unsigned_basic_auth"] = use_unsigned_basic_auth
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if zone_awareness is not None:
            self._values["zone_awareness"] = zone_awareness

    @builtins.property
    def version(self) -> "EngineVersion":
        '''The Elasticsearch/OpenSearch version that your domain will leverage.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast("EngineVersion", result)

    @builtins.property
    def access_policies(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_940a1ce0.PolicyStatement]]:
        '''Domain access policies.

        :default: - No access policies.
        '''
        result = self._values.get("access_policies")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_940a1ce0.PolicyStatement]], result)

    @builtins.property
    def advanced_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Additional options to specify for the Amazon OpenSearch Service domain.

        :default: - no advanced options are specified

        :see: https://docs.aws.amazon.com/opensearch-service/latest/developerguide/createupdatedomains.html#createdomain-configure-advanced-options
        '''
        result = self._values.get("advanced_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def automated_snapshot_start_hour(self) -> typing.Optional[jsii.Number]:
        '''The hour in UTC during which the service takes an automated daily snapshot of the indices in the Amazon OpenSearch Service domain.

        Only applies for Elasticsearch versions
        below 5.3.

        :default: - Hourly automated snapshots not used
        '''
        result = self._values.get("automated_snapshot_start_hour")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def capacity(self) -> typing.Optional[CapacityConfig]:
        '''The cluster capacity configuration for the Amazon OpenSearch Service domain.

        :default: - 1 r5.large.search data node; no dedicated master nodes.
        '''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional[CapacityConfig], result)

    @builtins.property
    def cognito_dashboards_auth(self) -> typing.Optional[CognitoOptions]:
        '''Configures Amazon OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards.

        :default: - Cognito not used for authentication to OpenSearch Dashboards.
        '''
        result = self._values.get("cognito_dashboards_auth")
        return typing.cast(typing.Optional[CognitoOptions], result)

    @builtins.property
    def custom_endpoint(self) -> typing.Optional[CustomEndpointOptions]:
        '''To configure a custom domain configure these options.

        If you specify a Route53 hosted zone it will create a CNAME record and use DNS validation for the certificate

        :default: - no custom domain endpoint will be configured
        '''
        result = self._values.get("custom_endpoint")
        return typing.cast(typing.Optional[CustomEndpointOptions], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''Enforces a particular physical domain name.

        :default: - A name will be auto-generated.
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ebs(self) -> typing.Optional["EbsOptions"]:
        '''The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the Amazon OpenSearch Service domain.

        :default: - 10 GiB General Purpose (SSD) volumes per node.
        '''
        result = self._values.get("ebs")
        return typing.cast(typing.Optional["EbsOptions"], result)

    @builtins.property
    def enable_version_upgrade(self) -> typing.Optional[builtins.bool]:
        '''To upgrade an Amazon OpenSearch Service domain to a new version, rather than replacing the entire domain resource, use the EnableVersionUpgrade update policy.

        :default: - false

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-upgradeopensearchdomain
        '''
        result = self._values.get("enable_version_upgrade")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def encryption_at_rest(self) -> typing.Optional["EncryptionAtRestOptions"]:
        '''Encryption at rest options for the cluster.

        :default: - No encryption at rest
        '''
        result = self._values.get("encryption_at_rest")
        return typing.cast(typing.Optional["EncryptionAtRestOptions"], result)

    @builtins.property
    def enforce_https(self) -> typing.Optional[builtins.bool]:
        '''True to require that all traffic to the domain arrive over HTTPS.

        :default: - false
        '''
        result = self._values.get("enforce_https")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def fine_grained_access_control(self) -> typing.Optional[AdvancedSecurityOptions]:
        '''Specifies options for fine-grained access control.

        Requires Elasticsearch version 6.7 or later or OpenSearch version 1.0 or later. Enabling fine-grained access control
        also requires encryption of data at rest and node-to-node encryption, along with
        enforced HTTPS.

        :default: - fine-grained access control is disabled
        '''
        result = self._values.get("fine_grained_access_control")
        return typing.cast(typing.Optional[AdvancedSecurityOptions], result)

    @builtins.property
    def logging(self) -> typing.Optional["LoggingOptions"]:
        '''Configuration log publishing configuration options.

        :default: - No logs are published
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional["LoggingOptions"], result)

    @builtins.property
    def node_to_node_encryption(self) -> typing.Optional[builtins.bool]:
        '''Specify true to enable node to node encryption.

        Requires Elasticsearch version 6.0 or later or OpenSearch version 1.0 or later.

        :default: - Node to node encryption is not enabled.
        '''
        result = self._values.get("node_to_node_encryption")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy]:
        '''Policy to apply when the domain is removed from the stack.

        :default: RemovalPolicy.RETAIN
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]]:
        '''The list of security groups that are associated with the VPC endpoints for the domain.

        Only used if ``vpc`` is specified.

        :default: - One new security group is created.

        :see: https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]], result)

    @builtins.property
    def tls_security_policy(self) -> typing.Optional["TLSSecurityPolicy"]:
        '''The minimum TLS version required for traffic to the domain.

        :default: - TLSSecurityPolicy.TLS_1_0
        '''
        result = self._values.get("tls_security_policy")
        return typing.cast(typing.Optional["TLSSecurityPolicy"], result)

    @builtins.property
    def use_unsigned_basic_auth(self) -> typing.Optional[builtins.bool]:
        '''Configures the domain so that unsigned basic auth is enabled.

        If no master user is provided a default master user
        with username ``admin`` and a dynamically generated password stored in KMS is created. The password can be retrieved
        by getting ``masterUserPassword`` from the domain instance.

        Setting this to true will also add an access policy that allows unsigned
        access, enable node to node encryption, encryption at rest. If conflicting
        settings are encountered (like disabling encryption at rest) enabling this
        setting will cause a failure.

        :default: - false
        '''
        result = self._values.get("use_unsigned_basic_auth")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''Place the domain inside this VPC.

        :default: - Domain is not placed in a VPC.

        :see: https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vpc.html
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    @builtins.property
    def vpc_subnets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection]]:
        '''The specific vpc subnets the domain will be placed in.

        You must provide one subnet for each Availability Zone
        that your domain uses. For example, you must specify three subnet IDs for a three Availability Zone
        domain.

        Only used if ``vpc`` is specified.

        :default: - All private subnets.

        :see: https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection]], result)

    @builtins.property
    def zone_awareness(self) -> typing.Optional["ZoneAwarenessConfig"]:
        '''The cluster zone awareness configuration for the Amazon OpenSearch Service domain.

        :default: - no zone awareness (1 AZ)
        '''
        result = self._values.get("zone_awareness")
        return typing.cast(typing.Optional["ZoneAwarenessConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opensearchservice.EbsOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "iops": "iops",
        "volume_size": "volumeSize",
        "volume_type": "volumeType",
    },
)
class EbsOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        iops: typing.Optional[jsii.Number] = None,
        volume_size: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.EbsDeviceVolumeType] = None,
    ) -> None:
        '''The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the Amazon OpenSearch Service domain.

        For more information, see
        [Amazon EBS]
        (https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AmazonEBS.html)
        in the Amazon Elastic Compute Cloud Developer Guide.

        :param enabled: Specifies whether Amazon EBS volumes are attached to data nodes in the Amazon OpenSearch Service domain. Default: - true
        :param iops: The number of I/O operations per second (IOPS) that the volume supports. This property applies only to the Provisioned IOPS (SSD) EBS volume type. Default: - iops are not set.
        :param volume_size: The size (in GiB) of the EBS volume for each data node. The minimum and maximum size of an EBS volume depends on the EBS volume type and the instance type to which it is attached. For valid values, see [EBS volume size limits] (https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource) in the Amazon OpenSearch Service Developer Guide. Default: 10
        :param volume_type: The EBS volume type to use with the Amazon OpenSearch Service domain, such as standard, gp2, io1. Default: gp2

        :exampleMetadata: infused

        Example::

            prod_domain = opensearch.Domain(self, "Domain",
                version=opensearch.EngineVersion.OPENSEARCH_1_0,
                capacity=opensearch.CapacityConfig(
                    master_nodes=5,
                    data_nodes=20
                ),
                ebs=opensearch.EbsOptions(
                    volume_size=20
                ),
                zone_awareness=opensearch.ZoneAwarenessConfig(
                    availability_zone_count=3
                ),
                logging=opensearch.LoggingOptions(
                    slow_search_log_enabled=True,
                    app_log_enabled=True,
                    slow_index_log_enabled=True
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59de6b8ceae867d7e5210ad73941f395a6f0255d19f42499c5bb86695c58d697)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
            check_type(argname="argument volume_size", value=volume_size, expected_type=type_hints["volume_size"])
            check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if iops is not None:
            self._values["iops"] = iops
        if volume_size is not None:
            self._values["volume_size"] = volume_size
        if volume_type is not None:
            self._values["volume_type"] = volume_type

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether Amazon EBS volumes are attached to data nodes in the Amazon OpenSearch Service domain.

        :default: - true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        '''The number of I/O operations per second (IOPS) that the volume supports.

        This property applies only to the Provisioned IOPS (SSD) EBS
        volume type.

        :default: - iops are not set.
        '''
        result = self._values.get("iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_size(self) -> typing.Optional[jsii.Number]:
        '''The size (in GiB) of the EBS volume for each data node.

        The minimum and
        maximum size of an EBS volume depends on the EBS volume type and the
        instance type to which it is attached.  For  valid values, see
        [EBS volume size limits]
        (https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource)
        in the Amazon OpenSearch Service Developer Guide.

        :default: 10
        '''
        result = self._values.get("volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.EbsDeviceVolumeType]:
        '''The EBS volume type to use with the Amazon OpenSearch Service domain, such as standard, gp2, io1.

        :default: gp2
        '''
        result = self._values.get("volume_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.EbsDeviceVolumeType], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EbsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opensearchservice.EncryptionAtRestOptions",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "kms_key": "kmsKey"},
)
class EncryptionAtRestOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
    ) -> None:
        '''Whether the domain should encrypt data at rest, and if so, the AWS Key Management Service (KMS) key to use.

        Can only be used to create a new domain,
        not update an existing one. Requires Elasticsearch version 5.1 or later or OpenSearch version 1.0 or later.

        :param enabled: Specify true to enable encryption at rest. Default: - encryption at rest is disabled.
        :param kms_key: Supply if using KMS key for encryption at rest. Default: - uses default aws/es KMS key.

        :exampleMetadata: infused

        Example::

            domain = opensearch.Domain(self, "Domain",
                version=opensearch.EngineVersion.OPENSEARCH_1_0,
                enforce_https=True,
                node_to_node_encryption=True,
                encryption_at_rest=opensearch.EncryptionAtRestOptions(
                    enabled=True
                ),
                fine_grained_access_control=opensearch.AdvancedSecurityOptions(
                    master_user_name="master-user"
                ),
                logging=opensearch.LoggingOptions(
                    audit_log_enabled=True,
                    slow_search_log_enabled=True,
                    app_log_enabled=True,
                    slow_index_log_enabled=True
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cd93a31613dd73e2bb3f8c0e61fd9490f278773cbc40539f826254aef021971)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Specify true to enable encryption at rest.

        :default: - encryption at rest is disabled.
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey]:
        '''Supply if using KMS key for encryption at rest.

        :default: - uses default aws/es KMS key.
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EncryptionAtRestOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EngineVersion(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-opensearchservice.EngineVersion",
):
    '''OpenSearch version.

    :exampleMetadata: infused

    Example::

        domain = opensearch.Domain(self, "Domain",
            version=opensearch.EngineVersion.OPENSEARCH_1_0,
            ebs=opensearch.EbsOptions(
                volume_size=100,
                volume_type=ec2.EbsDeviceVolumeType.GENERAL_PURPOSE_SSD
            ),
            node_to_node_encryption=True,
            encryption_at_rest=opensearch.EncryptionAtRestOptions(
                enabled=True
            )
        )
    '''

    @jsii.member(jsii_name="elasticsearch")
    @builtins.classmethod
    def elasticsearch(cls, version: builtins.str) -> "EngineVersion":
        '''Custom ElasticSearch version.

        :param version: custom version number.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b4d5f7b970e0509247f4d0117ef7efdbb38a51a6746f1d7913fcc5dd51f67e2)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("EngineVersion", jsii.sinvoke(cls, "elasticsearch", [version]))

    @jsii.member(jsii_name="openSearch")
    @builtins.classmethod
    def open_search(cls, version: builtins.str) -> "EngineVersion":
        '''Custom OpenSearch version.

        :param version: custom version number.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7294c705dad0adff616c7efb108f8b4bb4b655f6a4da36327ac23e1fd401f20b)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("EngineVersion", jsii.sinvoke(cls, "openSearch", [version]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_1_5")
    def ELASTICSEARCH_1_5(cls) -> "EngineVersion":
        '''AWS Elasticsearch 1.5.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_1_5"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_2_3")
    def ELASTICSEARCH_2_3(cls) -> "EngineVersion":
        '''AWS Elasticsearch 2.3.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_2_3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_5_1")
    def ELASTICSEARCH_5_1(cls) -> "EngineVersion":
        '''AWS Elasticsearch 5.1.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_5_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_5_3")
    def ELASTICSEARCH_5_3(cls) -> "EngineVersion":
        '''AWS Elasticsearch 5.3.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_5_3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_5_5")
    def ELASTICSEARCH_5_5(cls) -> "EngineVersion":
        '''AWS Elasticsearch 5.5.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_5_5"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_5_6")
    def ELASTICSEARCH_5_6(cls) -> "EngineVersion":
        '''AWS Elasticsearch 5.6.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_5_6"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_6_0")
    def ELASTICSEARCH_6_0(cls) -> "EngineVersion":
        '''AWS Elasticsearch 6.0.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_6_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_6_2")
    def ELASTICSEARCH_6_2(cls) -> "EngineVersion":
        '''AWS Elasticsearch 6.2.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_6_2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_6_3")
    def ELASTICSEARCH_6_3(cls) -> "EngineVersion":
        '''AWS Elasticsearch 6.3.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_6_3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_6_4")
    def ELASTICSEARCH_6_4(cls) -> "EngineVersion":
        '''AWS Elasticsearch 6.4.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_6_4"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_6_5")
    def ELASTICSEARCH_6_5(cls) -> "EngineVersion":
        '''AWS Elasticsearch 6.5.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_6_5"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_6_7")
    def ELASTICSEARCH_6_7(cls) -> "EngineVersion":
        '''AWS Elasticsearch 6.7.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_6_7"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_6_8")
    def ELASTICSEARCH_6_8(cls) -> "EngineVersion":
        '''AWS Elasticsearch 6.8.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_6_8"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_7_1")
    def ELASTICSEARCH_7_1(cls) -> "EngineVersion":
        '''AWS Elasticsearch 7.1.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_7_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_7_10")
    def ELASTICSEARCH_7_10(cls) -> "EngineVersion":
        '''AWS Elasticsearch 7.10.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_7_10"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_7_4")
    def ELASTICSEARCH_7_4(cls) -> "EngineVersion":
        '''AWS Elasticsearch 7.4.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_7_4"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_7_7")
    def ELASTICSEARCH_7_7(cls) -> "EngineVersion":
        '''AWS Elasticsearch 7.7.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_7_7"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_7_8")
    def ELASTICSEARCH_7_8(cls) -> "EngineVersion":
        '''AWS Elasticsearch 7.8.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_7_8"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ELASTICSEARCH_7_9")
    def ELASTICSEARCH_7_9(cls) -> "EngineVersion":
        '''AWS Elasticsearch 7.9.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "ELASTICSEARCH_7_9"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OPENSEARCH_1_0")
    def OPENSEARCH_1_0(cls) -> "EngineVersion":
        '''AWS OpenSearch 1.0.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "OPENSEARCH_1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OPENSEARCH_1_1")
    def OPENSEARCH_1_1(cls) -> "EngineVersion":
        '''AWS OpenSearch 1.1.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "OPENSEARCH_1_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OPENSEARCH_1_2")
    def OPENSEARCH_1_2(cls) -> "EngineVersion":
        '''AWS OpenSearch 1.2.'''
        return typing.cast("EngineVersion", jsii.sget(cls, "OPENSEARCH_1_2"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''engine version identifier.'''
        return typing.cast(builtins.str, jsii.get(self, "version"))


@jsii.interface(jsii_type="@aws-cdk/aws-opensearchservice.IDomain")
class IDomain(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''An interface that represents an Amazon OpenSearch Service domain - either created with the CDK, or an existing one.'''

    @builtins.property
    @jsii.member(jsii_name="domainArn")
    def domain_arn(self) -> builtins.str:
        '''Arn of the Amazon OpenSearch Service domain.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="domainEndpoint")
    def domain_endpoint(self) -> builtins.str:
        '''Endpoint of the Amazon OpenSearch Service domain.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        '''Identifier of the Amazon OpenSearch Service domain.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''Domain name of the Amazon OpenSearch Service domain.

        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grantIndexRead")
    def grant_index_read(
        self,
        index: builtins.str,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant read permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.
        '''
        ...

    @jsii.member(jsii_name="grantIndexReadWrite")
    def grant_index_read_write(
        self,
        index: builtins.str,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant read/write permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.
        '''
        ...

    @jsii.member(jsii_name="grantIndexWrite")
    def grant_index_write(
        self,
        index: builtins.str,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant write permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.
        '''
        ...

    @jsii.member(jsii_name="grantPathRead")
    def grant_path_read(
        self,
        path: builtins.str,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant read permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.
        '''
        ...

    @jsii.member(jsii_name="grantPathReadWrite")
    def grant_path_read_write(
        self,
        path: builtins.str,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant read/write permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.
        '''
        ...

    @jsii.member(jsii_name="grantPathWrite")
    def grant_path_write(
        self,
        path: builtins.str,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant write permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant read permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.
        '''
        ...

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant read/write permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.
        '''
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant write permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.
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
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Return the given named metric for this domain.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        ...

    @jsii.member(jsii_name="metricAutomatedSnapshotFailure")
    def metric_automated_snapshot_failure(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for automated snapshot failures.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        ...

    @jsii.member(jsii_name="metricClusterIndexWritesBlocked")
    def metric_cluster_index_writes_blocked(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for the cluster blocking index writes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 1 minute
        '''
        ...

    @jsii.member(jsii_name="metricClusterStatusRed")
    def metric_cluster_status_red(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for the time the cluster status is red.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        ...

    @jsii.member(jsii_name="metricClusterStatusYellow")
    def metric_cluster_status_yellow(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for the time the cluster status is yellow.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        ...

    @jsii.member(jsii_name="metricCPUUtilization")
    def metric_cpu_utilization(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for CPU utilization.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        ...

    @jsii.member(jsii_name="metricFreeStorageSpace")
    def metric_free_storage_space(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for the storage space of nodes in the cluster.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: minimum over 5 minutes
        '''
        ...

    @jsii.member(jsii_name="metricIndexingLatency")
    def metric_indexing_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for indexing latency.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: p99 over 5 minutes
        '''
        ...

    @jsii.member(jsii_name="metricJVMMemoryPressure")
    def metric_jvm_memory_pressure(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for JVM memory pressure.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        ...

    @jsii.member(jsii_name="metricKMSKeyError")
    def metric_kms_key_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for KMS key errors.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        ...

    @jsii.member(jsii_name="metricKMSKeyInaccessible")
    def metric_kms_key_inaccessible(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for KMS key being inaccessible.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        ...

    @jsii.member(jsii_name="metricMasterCPUUtilization")
    def metric_master_cpu_utilization(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for master CPU utilization.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        ...

    @jsii.member(jsii_name="metricMasterJVMMemoryPressure")
    def metric_master_jvm_memory_pressure(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for master JVM memory pressure.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        ...

    @jsii.member(jsii_name="metricNodes")
    def metric_nodes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for the number of nodes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: minimum over 1 hour
        '''
        ...

    @jsii.member(jsii_name="metricSearchableDocuments")
    def metric_searchable_documents(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for number of searchable documents.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        ...

    @jsii.member(jsii_name="metricSearchLatency")
    def metric_search_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for search latency.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: p99 over 5 minutes
        '''
        ...


class _IDomainProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''An interface that represents an Amazon OpenSearch Service domain - either created with the CDK, or an existing one.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-opensearchservice.IDomain"

    @builtins.property
    @jsii.member(jsii_name="domainArn")
    def domain_arn(self) -> builtins.str:
        '''Arn of the Amazon OpenSearch Service domain.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainArn"))

    @builtins.property
    @jsii.member(jsii_name="domainEndpoint")
    def domain_endpoint(self) -> builtins.str:
        '''Endpoint of the Amazon OpenSearch Service domain.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        '''Identifier of the Amazon OpenSearch Service domain.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainId"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''Domain name of the Amazon OpenSearch Service domain.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @jsii.member(jsii_name="grantIndexRead")
    def grant_index_read(
        self,
        index: builtins.str,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant read permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__154758356627b471cb64c1cf145eefbb40507d92a0496857f0841c0ee6eda113)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantIndexRead", [index, identity]))

    @jsii.member(jsii_name="grantIndexReadWrite")
    def grant_index_read_write(
        self,
        index: builtins.str,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant read/write permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c431a80a1158b843bc917876ade588cf9deb6792d1c4347dba425e2bdb743b68)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantIndexReadWrite", [index, identity]))

    @jsii.member(jsii_name="grantIndexWrite")
    def grant_index_write(
        self,
        index: builtins.str,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant write permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca45d262753693960fa2ea2044f8e36d2f931fc063b8707073c6058cead18769)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantIndexWrite", [index, identity]))

    @jsii.member(jsii_name="grantPathRead")
    def grant_path_read(
        self,
        path: builtins.str,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant read permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7d0b73068f96c64a2b965ffb4026bcf0aef1881edd9efd0b8c05fa14c54e16e)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantPathRead", [path, identity]))

    @jsii.member(jsii_name="grantPathReadWrite")
    def grant_path_read_write(
        self,
        path: builtins.str,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant read/write permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab6dac8bc8b57b5c161a487aa8382ec4d208186948e17d1abcf38d5c43f376f9)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantPathReadWrite", [path, identity]))

    @jsii.member(jsii_name="grantPathWrite")
    def grant_path_write(
        self,
        path: builtins.str,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant write permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__405d9581fcae9e57d3ff9e79b03fdb1a00cf51e9389b312deb5dbfa43f2f36ca)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantPathWrite", [path, identity]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant read permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d4e2800f2b5342351704cde1f02589b549bc0f8493f4ac30f2f2df97db7ed48)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantRead", [identity]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant read/write permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__add23aa82707022dd48d02a4641fb998dc92c3cc94d29ddc0cec4bb1ce746548)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantReadWrite", [identity]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant write permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5594d6783cc90d98b4fbdac1df535c1405330fca0f6f9388a5935fbf3c285638)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantWrite", [identity]))

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
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Return the given named metric for this domain.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9938780143ebac33d9de983b38db3e0f01531ffa28cceebabead4a1b983c1d75)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricAutomatedSnapshotFailure")
    def metric_automated_snapshot_failure(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for automated snapshot failures.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricAutomatedSnapshotFailure", [props]))

    @jsii.member(jsii_name="metricClusterIndexWritesBlocked")
    def metric_cluster_index_writes_blocked(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for the cluster blocking index writes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 1 minute
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricClusterIndexWritesBlocked", [props]))

    @jsii.member(jsii_name="metricClusterStatusRed")
    def metric_cluster_status_red(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for the time the cluster status is red.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricClusterStatusRed", [props]))

    @jsii.member(jsii_name="metricClusterStatusYellow")
    def metric_cluster_status_yellow(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for the time the cluster status is yellow.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricClusterStatusYellow", [props]))

    @jsii.member(jsii_name="metricCPUUtilization")
    def metric_cpu_utilization(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for CPU utilization.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricCPUUtilization", [props]))

    @jsii.member(jsii_name="metricFreeStorageSpace")
    def metric_free_storage_space(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for the storage space of nodes in the cluster.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: minimum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricFreeStorageSpace", [props]))

    @jsii.member(jsii_name="metricIndexingLatency")
    def metric_indexing_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for indexing latency.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: p99 over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricIndexingLatency", [props]))

    @jsii.member(jsii_name="metricJVMMemoryPressure")
    def metric_jvm_memory_pressure(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for JVM memory pressure.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricJVMMemoryPressure", [props]))

    @jsii.member(jsii_name="metricKMSKeyError")
    def metric_kms_key_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for KMS key errors.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricKMSKeyError", [props]))

    @jsii.member(jsii_name="metricKMSKeyInaccessible")
    def metric_kms_key_inaccessible(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for KMS key being inaccessible.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricKMSKeyInaccessible", [props]))

    @jsii.member(jsii_name="metricMasterCPUUtilization")
    def metric_master_cpu_utilization(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for master CPU utilization.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricMasterCPUUtilization", [props]))

    @jsii.member(jsii_name="metricMasterJVMMemoryPressure")
    def metric_master_jvm_memory_pressure(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for master JVM memory pressure.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricMasterJVMMemoryPressure", [props]))

    @jsii.member(jsii_name="metricNodes")
    def metric_nodes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for the number of nodes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: minimum over 1 hour
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricNodes", [props]))

    @jsii.member(jsii_name="metricSearchableDocuments")
    def metric_searchable_documents(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for number of searchable documents.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricSearchableDocuments", [props]))

    @jsii.member(jsii_name="metricSearchLatency")
    def metric_search_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for search latency.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: p99 over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricSearchLatency", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDomain).__jsii_proxy_class__ = lambda : _IDomainProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opensearchservice.LoggingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "app_log_enabled": "appLogEnabled",
        "app_log_group": "appLogGroup",
        "audit_log_enabled": "auditLogEnabled",
        "audit_log_group": "auditLogGroup",
        "slow_index_log_enabled": "slowIndexLogEnabled",
        "slow_index_log_group": "slowIndexLogGroup",
        "slow_search_log_enabled": "slowSearchLogEnabled",
        "slow_search_log_group": "slowSearchLogGroup",
    },
)
class LoggingOptions:
    def __init__(
        self,
        *,
        app_log_enabled: typing.Optional[builtins.bool] = None,
        app_log_group: typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup] = None,
        audit_log_enabled: typing.Optional[builtins.bool] = None,
        audit_log_group: typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup] = None,
        slow_index_log_enabled: typing.Optional[builtins.bool] = None,
        slow_index_log_group: typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup] = None,
        slow_search_log_enabled: typing.Optional[builtins.bool] = None,
        slow_search_log_group: typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup] = None,
    ) -> None:
        '''Configures log settings for the domain.

        :param app_log_enabled: Specify if Amazon OpenSearch Service application logging should be set up. Requires Elasticsearch version 5.1 or later or OpenSearch version 1.0 or later. Default: - false
        :param app_log_group: Log Amazon OpenSearch Service application logs to this log group. Default: - a new log group is created if app logging is enabled
        :param audit_log_enabled: Specify if Amazon OpenSearch Service audit logging should be set up. Requires Elasticsearch version 6.7 or later or OpenSearch version 1.0 or later and fine grained access control to be enabled. Default: - false
        :param audit_log_group: Log Amazon OpenSearch Service audit logs to this log group. Default: - a new log group is created if audit logging is enabled
        :param slow_index_log_enabled: Specify if slow index logging should be set up. Requires Elasticsearch version 5.1 or later or OpenSearch version 1.0 or later. Default: - false
        :param slow_index_log_group: Log slow indices to this log group. Default: - a new log group is created if slow index logging is enabled
        :param slow_search_log_enabled: Specify if slow search logging should be set up. Requires Elasticsearch version 5.1 or later or OpenSearch version 1.0 or later. Default: - false
        :param slow_search_log_group: Log slow searches to this log group. Default: - a new log group is created if slow search logging is enabled

        :exampleMetadata: infused

        Example::

            prod_domain = opensearch.Domain(self, "Domain",
                version=opensearch.EngineVersion.OPENSEARCH_1_0,
                capacity=opensearch.CapacityConfig(
                    master_nodes=5,
                    data_nodes=20
                ),
                ebs=opensearch.EbsOptions(
                    volume_size=20
                ),
                zone_awareness=opensearch.ZoneAwarenessConfig(
                    availability_zone_count=3
                ),
                logging=opensearch.LoggingOptions(
                    slow_search_log_enabled=True,
                    app_log_enabled=True,
                    slow_index_log_enabled=True
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70be678aa9f41d60ec7aa4fbb915e4bb0bd11e12c6c4db5da1cfade0267863af)
            check_type(argname="argument app_log_enabled", value=app_log_enabled, expected_type=type_hints["app_log_enabled"])
            check_type(argname="argument app_log_group", value=app_log_group, expected_type=type_hints["app_log_group"])
            check_type(argname="argument audit_log_enabled", value=audit_log_enabled, expected_type=type_hints["audit_log_enabled"])
            check_type(argname="argument audit_log_group", value=audit_log_group, expected_type=type_hints["audit_log_group"])
            check_type(argname="argument slow_index_log_enabled", value=slow_index_log_enabled, expected_type=type_hints["slow_index_log_enabled"])
            check_type(argname="argument slow_index_log_group", value=slow_index_log_group, expected_type=type_hints["slow_index_log_group"])
            check_type(argname="argument slow_search_log_enabled", value=slow_search_log_enabled, expected_type=type_hints["slow_search_log_enabled"])
            check_type(argname="argument slow_search_log_group", value=slow_search_log_group, expected_type=type_hints["slow_search_log_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if app_log_enabled is not None:
            self._values["app_log_enabled"] = app_log_enabled
        if app_log_group is not None:
            self._values["app_log_group"] = app_log_group
        if audit_log_enabled is not None:
            self._values["audit_log_enabled"] = audit_log_enabled
        if audit_log_group is not None:
            self._values["audit_log_group"] = audit_log_group
        if slow_index_log_enabled is not None:
            self._values["slow_index_log_enabled"] = slow_index_log_enabled
        if slow_index_log_group is not None:
            self._values["slow_index_log_group"] = slow_index_log_group
        if slow_search_log_enabled is not None:
            self._values["slow_search_log_enabled"] = slow_search_log_enabled
        if slow_search_log_group is not None:
            self._values["slow_search_log_group"] = slow_search_log_group

    @builtins.property
    def app_log_enabled(self) -> typing.Optional[builtins.bool]:
        '''Specify if Amazon OpenSearch Service application logging should be set up.

        Requires Elasticsearch version 5.1 or later or OpenSearch version 1.0 or later.

        :default: - false
        '''
        result = self._values.get("app_log_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def app_log_group(self) -> typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup]:
        '''Log Amazon OpenSearch Service application logs to this log group.

        :default: - a new log group is created if app logging is enabled
        '''
        result = self._values.get("app_log_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup], result)

    @builtins.property
    def audit_log_enabled(self) -> typing.Optional[builtins.bool]:
        '''Specify if Amazon OpenSearch Service audit logging should be set up.

        Requires Elasticsearch version 6.7 or later or OpenSearch version 1.0 or later and fine grained access control to be enabled.

        :default: - false
        '''
        result = self._values.get("audit_log_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def audit_log_group(self) -> typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup]:
        '''Log Amazon OpenSearch Service audit logs to this log group.

        :default: - a new log group is created if audit logging is enabled
        '''
        result = self._values.get("audit_log_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup], result)

    @builtins.property
    def slow_index_log_enabled(self) -> typing.Optional[builtins.bool]:
        '''Specify if slow index logging should be set up.

        Requires Elasticsearch version 5.1 or later or OpenSearch version 1.0 or later.

        :default: - false
        '''
        result = self._values.get("slow_index_log_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def slow_index_log_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup]:
        '''Log slow indices to this log group.

        :default: - a new log group is created if slow index logging is enabled
        '''
        result = self._values.get("slow_index_log_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup], result)

    @builtins.property
    def slow_search_log_enabled(self) -> typing.Optional[builtins.bool]:
        '''Specify if slow search logging should be set up.

        Requires Elasticsearch version 5.1 or later or OpenSearch version 1.0 or later.

        :default: - false
        '''
        result = self._values.get("slow_search_log_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def slow_search_log_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup]:
        '''Log slow searches to this log group.

        :default: - a new log group is created if slow search logging is enabled
        '''
        result = self._values.get("slow_search_log_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-opensearchservice.TLSSecurityPolicy")
class TLSSecurityPolicy(enum.Enum):
    '''The minimum TLS version required for traffic to the domain.'''

    TLS_1_0 = "TLS_1_0"
    '''Cipher suite TLS 1.0.'''
    TLS_1_2 = "TLS_1_2"
    '''Cipher suite TLS 1.2.'''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opensearchservice.ZoneAwarenessConfig",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zone_count": "availabilityZoneCount",
        "enabled": "enabled",
    },
)
class ZoneAwarenessConfig:
    def __init__(
        self,
        *,
        availability_zone_count: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Specifies zone awareness configuration options.

        :param availability_zone_count: If you enabled multiple Availability Zones (AZs), the number of AZs that you want the domain to use. Valid values are 2 and 3. Default: - 2 if zone awareness is enabled.
        :param enabled: Indicates whether to enable zone awareness for the Amazon OpenSearch Service domain. When you enable zone awareness, Amazon OpenSearch Service allocates the nodes and replica index shards that belong to a cluster across two Availability Zones (AZs) in the same region to prevent data loss and minimize downtime in the event of node or data center failure. Don't enable zone awareness if your cluster has no replica index shards or is a single-node cluster. For more information, see [Configuring a Multi-AZ Domain] (https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-multiaz.html) in the Amazon OpenSearch Service Developer Guide. Default: - false

        :exampleMetadata: infused

        Example::

            prod_domain = opensearch.Domain(self, "Domain",
                version=opensearch.EngineVersion.OPENSEARCH_1_0,
                capacity=opensearch.CapacityConfig(
                    master_nodes=5,
                    data_nodes=20
                ),
                ebs=opensearch.EbsOptions(
                    volume_size=20
                ),
                zone_awareness=opensearch.ZoneAwarenessConfig(
                    availability_zone_count=3
                ),
                logging=opensearch.LoggingOptions(
                    slow_search_log_enabled=True,
                    app_log_enabled=True,
                    slow_index_log_enabled=True
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2cab49e9c5b8a4df2f940c58aa9ddd79a4d82922c29c239444980b1bcc6bf4b)
            check_type(argname="argument availability_zone_count", value=availability_zone_count, expected_type=type_hints["availability_zone_count"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zone_count is not None:
            self._values["availability_zone_count"] = availability_zone_count
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def availability_zone_count(self) -> typing.Optional[jsii.Number]:
        '''If you enabled multiple Availability Zones (AZs), the number of AZs that you want the domain to use.

        Valid values are 2 and 3.

        :default: - 2 if zone awareness is enabled.
        '''
        result = self._values.get("availability_zone_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether to enable zone awareness for the Amazon OpenSearch Service domain.

        When you enable zone awareness, Amazon OpenSearch Service allocates the nodes and replica
        index shards that belong to a cluster across two Availability Zones (AZs)
        in the same region to prevent data loss and minimize downtime in the event
        of node or data center failure. Don't enable zone awareness if your cluster
        has no replica index shards or is a single-node cluster. For more information,
        see [Configuring a Multi-AZ Domain]
        (https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-multiaz.html)
        in the Amazon OpenSearch Service Developer Guide.

        :default: - false
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZoneAwarenessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IDomain, _aws_cdk_aws_ec2_67de8e8d.IConnectable)
class Domain(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-opensearchservice.Domain",
):
    '''Provides an Amazon OpenSearch Service domain.

    :exampleMetadata: infused

    Example::

        domain = opensearch.Domain(self, "Domain",
            version=opensearch.EngineVersion.OPENSEARCH_1_0,
            ebs=opensearch.EbsOptions(
                volume_size=100,
                volume_type=ec2.EbsDeviceVolumeType.GENERAL_PURPOSE_SSD
            ),
            node_to_node_encryption=True,
            encryption_at_rest=opensearch.EncryptionAtRestOptions(
                enabled=True
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        version: EngineVersion,
        access_policies: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.PolicyStatement]] = None,
        advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        automated_snapshot_start_hour: typing.Optional[jsii.Number] = None,
        capacity: typing.Optional[typing.Union[CapacityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        cognito_dashboards_auth: typing.Optional[typing.Union[CognitoOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_endpoint: typing.Optional[typing.Union[CustomEndpointOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        ebs: typing.Optional[typing.Union[EbsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        enable_version_upgrade: typing.Optional[builtins.bool] = None,
        encryption_at_rest: typing.Optional[typing.Union[EncryptionAtRestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        enforce_https: typing.Optional[builtins.bool] = None,
        fine_grained_access_control: typing.Optional[typing.Union[AdvancedSecurityOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[typing.Union[LoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        node_to_node_encryption: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
        tls_security_policy: typing.Optional[TLSSecurityPolicy] = None,
        use_unsigned_basic_auth: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
        zone_awareness: typing.Optional[typing.Union[ZoneAwarenessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: The Elasticsearch/OpenSearch version that your domain will leverage.
        :param access_policies: Domain access policies. Default: - No access policies.
        :param advanced_options: Additional options to specify for the Amazon OpenSearch Service domain. Default: - no advanced options are specified
        :param automated_snapshot_start_hour: The hour in UTC during which the service takes an automated daily snapshot of the indices in the Amazon OpenSearch Service domain. Only applies for Elasticsearch versions below 5.3. Default: - Hourly automated snapshots not used
        :param capacity: The cluster capacity configuration for the Amazon OpenSearch Service domain. Default: - 1 r5.large.search data node; no dedicated master nodes.
        :param cognito_dashboards_auth: Configures Amazon OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards. Default: - Cognito not used for authentication to OpenSearch Dashboards.
        :param custom_endpoint: To configure a custom domain configure these options. If you specify a Route53 hosted zone it will create a CNAME record and use DNS validation for the certificate Default: - no custom domain endpoint will be configured
        :param domain_name: Enforces a particular physical domain name. Default: - A name will be auto-generated.
        :param ebs: The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the Amazon OpenSearch Service domain. Default: - 10 GiB General Purpose (SSD) volumes per node.
        :param enable_version_upgrade: To upgrade an Amazon OpenSearch Service domain to a new version, rather than replacing the entire domain resource, use the EnableVersionUpgrade update policy. Default: - false
        :param encryption_at_rest: Encryption at rest options for the cluster. Default: - No encryption at rest
        :param enforce_https: True to require that all traffic to the domain arrive over HTTPS. Default: - false
        :param fine_grained_access_control: Specifies options for fine-grained access control. Requires Elasticsearch version 6.7 or later or OpenSearch version 1.0 or later. Enabling fine-grained access control also requires encryption of data at rest and node-to-node encryption, along with enforced HTTPS. Default: - fine-grained access control is disabled
        :param logging: Configuration log publishing configuration options. Default: - No logs are published
        :param node_to_node_encryption: Specify true to enable node to node encryption. Requires Elasticsearch version 6.0 or later or OpenSearch version 1.0 or later. Default: - Node to node encryption is not enabled.
        :param removal_policy: Policy to apply when the domain is removed from the stack. Default: RemovalPolicy.RETAIN
        :param security_groups: The list of security groups that are associated with the VPC endpoints for the domain. Only used if ``vpc`` is specified. Default: - One new security group is created.
        :param tls_security_policy: The minimum TLS version required for traffic to the domain. Default: - TLSSecurityPolicy.TLS_1_0
        :param use_unsigned_basic_auth: Configures the domain so that unsigned basic auth is enabled. If no master user is provided a default master user with username ``admin`` and a dynamically generated password stored in KMS is created. The password can be retrieved by getting ``masterUserPassword`` from the domain instance. Setting this to true will also add an access policy that allows unsigned access, enable node to node encryption, encryption at rest. If conflicting settings are encountered (like disabling encryption at rest) enabling this setting will cause a failure. Default: - false
        :param vpc: Place the domain inside this VPC. Default: - Domain is not placed in a VPC.
        :param vpc_subnets: The specific vpc subnets the domain will be placed in. You must provide one subnet for each Availability Zone that your domain uses. For example, you must specify three subnet IDs for a three Availability Zone domain. Only used if ``vpc`` is specified. Default: - All private subnets.
        :param zone_awareness: The cluster zone awareness configuration for the Amazon OpenSearch Service domain. Default: - no zone awareness (1 AZ)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f1a9d05f3f30ee0463b637624b1b2ff65dcfb2ca7e1812cabfa2db4fa0310a9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DomainProps(
            version=version,
            access_policies=access_policies,
            advanced_options=advanced_options,
            automated_snapshot_start_hour=automated_snapshot_start_hour,
            capacity=capacity,
            cognito_dashboards_auth=cognito_dashboards_auth,
            custom_endpoint=custom_endpoint,
            domain_name=domain_name,
            ebs=ebs,
            enable_version_upgrade=enable_version_upgrade,
            encryption_at_rest=encryption_at_rest,
            enforce_https=enforce_https,
            fine_grained_access_control=fine_grained_access_control,
            logging=logging,
            node_to_node_encryption=node_to_node_encryption,
            removal_policy=removal_policy,
            security_groups=security_groups,
            tls_security_policy=tls_security_policy,
            use_unsigned_basic_auth=use_unsigned_basic_auth,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
            zone_awareness=zone_awareness,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromDomainAttributes")
    @builtins.classmethod
    def from_domain_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        domain_arn: builtins.str,
        domain_endpoint: builtins.str,
    ) -> IDomain:
        '''Creates a domain construct that represents an external domain.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param domain_arn: The ARN of the Amazon OpenSearch Service domain.
        :param domain_endpoint: The domain endpoint of the Amazon OpenSearch Service domain.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dcd5a14bd283abea946b904876ca0ed1dcae1faf2a596b5815089eca45974cd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = DomainAttributes(
            domain_arn=domain_arn, domain_endpoint=domain_endpoint
        )

        return typing.cast(IDomain, jsii.sinvoke(cls, "fromDomainAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromDomainEndpoint")
    @builtins.classmethod
    def from_domain_endpoint(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        domain_endpoint: builtins.str,
    ) -> IDomain:
        '''Creates a domain construct that represents an external domain via domain endpoint.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param domain_endpoint: The domain's endpoint.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e90fbc1d5ddcfb4b38ad319535ce4a3d6dc4c4cd7fd47f50f4cabe975e90c7c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument domain_endpoint", value=domain_endpoint, expected_type=type_hints["domain_endpoint"])
        return typing.cast(IDomain, jsii.sinvoke(cls, "fromDomainEndpoint", [scope, id, domain_endpoint]))

    @jsii.member(jsii_name="addAccessPolicies")
    def add_access_policies(
        self,
        *access_policy_statements: _aws_cdk_aws_iam_940a1ce0.PolicyStatement,
    ) -> None:
        '''Add policy statements to the domain access policy.

        :param access_policy_statements: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b772037660425e6a8436f6516d62145875674ff1bea486a8c9a4cc0204a97107)
            check_type(argname="argument access_policy_statements", value=access_policy_statements, expected_type=typing.Tuple[type_hints["access_policy_statements"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addAccessPolicies", [*access_policy_statements]))

    @jsii.member(jsii_name="grantIndexRead")
    def grant_index_read(
        self,
        index: builtins.str,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant read permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ed7af745c35ccbfc7d89381475d15972f44a9504e19cc5295d2d57fe19f6884)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantIndexRead", [index, identity]))

    @jsii.member(jsii_name="grantIndexReadWrite")
    def grant_index_read_write(
        self,
        index: builtins.str,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant read/write permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be78c8f0c8113e612f28c82d3574a3b24833aafe52cdb0bc039c4bb2f518b8e8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantIndexReadWrite", [index, identity]))

    @jsii.member(jsii_name="grantIndexWrite")
    def grant_index_write(
        self,
        index: builtins.str,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant write permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7a2fc087ab97c6607a56da8e329df429b8679db521bdd39584120377cc5ca97)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantIndexWrite", [index, identity]))

    @jsii.member(jsii_name="grantPathRead")
    def grant_path_read(
        self,
        path: builtins.str,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant read permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff234922defecc238abfb81ef4c8ccd1ed7630e513b64631b34ff0265196420)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantPathRead", [path, identity]))

    @jsii.member(jsii_name="grantPathReadWrite")
    def grant_path_read_write(
        self,
        path: builtins.str,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant read/write permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5587a92a52830897ebc88b531e06de37c5ff9ded885692e58a98b9580fb92eb4)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantPathReadWrite", [path, identity]))

    @jsii.member(jsii_name="grantPathWrite")
    def grant_path_write(
        self,
        path: builtins.str,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant write permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__134bc9072df45210b7b032d40fa58f617003ec9ad96c4533fc9651c8069201ca)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantPathWrite", [path, identity]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant read permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80cda93c959869d61f0d3a6a10e7322f22fcd23de1d846ce4dce21edbaf98161)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantRead", [identity]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant read/write permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45352bd7d92475d75ad2b34ba73c51f26a90f2e9d1454e70d81be9215d8bea6e)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantReadWrite", [identity]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant write permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a025f18643464ab5b722c6bbd540f69976176fe10c52265e0d86f6e56d641e)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantWrite", [identity]))

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
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Return the given named metric for this domain.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33a0afd3e74cdb03b0f84cfed4d295b0bffee98d99ac2090c00ca3c4fca0ba0c)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricAutomatedSnapshotFailure")
    def metric_automated_snapshot_failure(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for automated snapshot failures.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricAutomatedSnapshotFailure", [props]))

    @jsii.member(jsii_name="metricClusterIndexWritesBlocked")
    def metric_cluster_index_writes_blocked(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for the cluster blocking index writes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 1 minute
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricClusterIndexWritesBlocked", [props]))

    @jsii.member(jsii_name="metricClusterStatusRed")
    def metric_cluster_status_red(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for the time the cluster status is red.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricClusterStatusRed", [props]))

    @jsii.member(jsii_name="metricClusterStatusYellow")
    def metric_cluster_status_yellow(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for the time the cluster status is yellow.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricClusterStatusYellow", [props]))

    @jsii.member(jsii_name="metricCPUUtilization")
    def metric_cpu_utilization(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for CPU utilization.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricCPUUtilization", [props]))

    @jsii.member(jsii_name="metricFreeStorageSpace")
    def metric_free_storage_space(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for the storage space of nodes in the cluster.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: minimum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricFreeStorageSpace", [props]))

    @jsii.member(jsii_name="metricIndexingLatency")
    def metric_indexing_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for indexing latency.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: p99 over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricIndexingLatency", [props]))

    @jsii.member(jsii_name="metricJVMMemoryPressure")
    def metric_jvm_memory_pressure(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for JVM memory pressure.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricJVMMemoryPressure", [props]))

    @jsii.member(jsii_name="metricKMSKeyError")
    def metric_kms_key_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for KMS key errors.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricKMSKeyError", [props]))

    @jsii.member(jsii_name="metricKMSKeyInaccessible")
    def metric_kms_key_inaccessible(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for KMS key being inaccessible.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricKMSKeyInaccessible", [props]))

    @jsii.member(jsii_name="metricMasterCPUUtilization")
    def metric_master_cpu_utilization(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for master CPU utilization.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricMasterCPUUtilization", [props]))

    @jsii.member(jsii_name="metricMasterJVMMemoryPressure")
    def metric_master_jvm_memory_pressure(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for master JVM memory pressure.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricMasterJVMMemoryPressure", [props]))

    @jsii.member(jsii_name="metricNodes")
    def metric_nodes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for the number of nodes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: minimum over 1 hour
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricNodes", [props]))

    @jsii.member(jsii_name="metricSearchableDocuments")
    def metric_searchable_documents(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for number of searchable documents.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricSearchableDocuments", [props]))

    @jsii.member(jsii_name="metricSearchLatency")
    def metric_search_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Metric for search latency.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: p99 over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricSearchLatency", [props]))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_67de8e8d.Connections:
        '''Manages network connections to the domain.

        This will throw an error in case the domain
        is not placed inside a VPC.
        '''
        return typing.cast(_aws_cdk_aws_ec2_67de8e8d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="domainArn")
    def domain_arn(self) -> builtins.str:
        '''Arn of the Amazon OpenSearch Service domain.'''
        return typing.cast(builtins.str, jsii.get(self, "domainArn"))

    @builtins.property
    @jsii.member(jsii_name="domainEndpoint")
    def domain_endpoint(self) -> builtins.str:
        '''Endpoint of the Amazon OpenSearch Service domain.'''
        return typing.cast(builtins.str, jsii.get(self, "domainEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        '''Identifier of the Amazon OpenSearch Service domain.'''
        return typing.cast(builtins.str, jsii.get(self, "domainId"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''Domain name of the Amazon OpenSearch Service domain.'''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="appLogGroup")
    def app_log_group(self) -> typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup]:
        '''Log group that application logs are logged to.

        :attribute: true
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup], jsii.get(self, "appLogGroup"))

    @builtins.property
    @jsii.member(jsii_name="auditLogGroup")
    def audit_log_group(self) -> typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup]:
        '''Log group that audit logs are logged to.

        :attribute: true
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup], jsii.get(self, "auditLogGroup"))

    @builtins.property
    @jsii.member(jsii_name="masterUserPassword")
    def master_user_password(
        self,
    ) -> typing.Optional[_aws_cdk_core_f4b25747.SecretValue]:
        '''Master user password if fine grained access control is configured.'''
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.SecretValue], jsii.get(self, "masterUserPassword"))

    @builtins.property
    @jsii.member(jsii_name="slowIndexLogGroup")
    def slow_index_log_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup]:
        '''Log group that slow indices are logged to.

        :attribute: true
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup], jsii.get(self, "slowIndexLogGroup"))

    @builtins.property
    @jsii.member(jsii_name="slowSearchLogGroup")
    def slow_search_log_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup]:
        '''Log group that slow searches are logged to.

        :attribute: true
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup], jsii.get(self, "slowSearchLogGroup"))


__all__ = [
    "AdvancedSecurityOptions",
    "CapacityConfig",
    "CfnDomain",
    "CfnDomainProps",
    "CognitoOptions",
    "CustomEndpointOptions",
    "Domain",
    "DomainAttributes",
    "DomainProps",
    "EbsOptions",
    "EncryptionAtRestOptions",
    "EngineVersion",
    "IDomain",
    "LoggingOptions",
    "TLSSecurityPolicy",
    "ZoneAwarenessConfig",
]

publication.publish()

def _typecheckingstub__9663f6c508a4270e241a70dbc92c6a2ad261f30507ea62ef1fa6c2dd19e64527(
    *,
    master_user_arn: typing.Optional[builtins.str] = None,
    master_user_name: typing.Optional[builtins.str] = None,
    master_user_password: typing.Optional[_aws_cdk_core_f4b25747.SecretValue] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e49dad680f17a1e3e914105d1c4eccf2dadf3f6193aa3a1e626f41a3ae67ee(
    *,
    data_node_instance_type: typing.Optional[builtins.str] = None,
    data_nodes: typing.Optional[jsii.Number] = None,
    master_node_instance_type: typing.Optional[builtins.str] = None,
    master_nodes: typing.Optional[jsii.Number] = None,
    warm_instance_type: typing.Optional[builtins.str] = None,
    warm_nodes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d8bfb3eae80cd17b709b261261abd885f782259b2c67e0a6b7b54234bbfa41f(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    access_policies: typing.Any = None,
    advanced_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    advanced_security_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.AdvancedSecurityOptionsInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cluster_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.ClusterConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cognito_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.CognitoOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    domain_endpoint_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.DomainEndpointOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    domain_name: typing.Optional[builtins.str] = None,
    ebs_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.EBSOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption_at_rest_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.EncryptionAtRestOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    engine_version: typing.Optional[builtins.str] = None,
    log_publishing_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.LogPublishingOptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    node_to_node_encryption_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.NodeToNodeEncryptionOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    snapshot_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.SnapshotOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.VPCOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d922cc0a798d483aa0dbc1dc2f5d9b171e62be078177b79fcc1f298b0a34cd7(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f8cf9b8e15dc0f9cd25846048eedfdec5b2f23e3158d3e1286d92363bbf7813(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__124490f44bfc8cb9166d95f5cf1a1e143bd9c84e143ee82a84691224bd148aa7(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041b6f65034582f626434a70543ffb7bbb2dfd668b7f720e4ebb46962097f571(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e71ab581d18d39ebfd3cb9df3c0530e66f21152477a586e1ff207563f530392a(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.AdvancedSecurityOptionsInputProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__242b992e488742e7382b665de9bc48b487807dd4416778e0aee2a1e324f8974f(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.ClusterConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3614ecc7f4b8420734656233a2f956baa143be7659f6b26ba66725f8fedbb44(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.CognitoOptionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467d8bb30a1a9a2fe2117aef5a6d8bfb5ec07fa3bc23bbf1fbbb4597d57b7f52(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.DomainEndpointOptionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cdb234b06dcc6b6876f053c097db924df470823a5c55f7cf5d7bc84852f28d0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aac15720e304f08b6ec450459d7caf824fff24df602e01025bb6f94ceaee64c(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.EBSOptionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5753eb4890b1cc9901049bc8be92991b585c1c9cc739bd9a4c920dfdfb21cac5(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.EncryptionAtRestOptionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cdf4c8a2f195f3245aae8f0c2d15bff93731e5f344d5047d4a81c827ade7690(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62686f38ab3ab553d30950b11f210da58b70537c74ee6795d993522b28cc9f44(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.LogPublishingOptionProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eed7c1edf733b2d581498f06f02e652f5a6cba31e96572ef643c85ca3d54f56b(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.NodeToNodeEncryptionOptionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb9e010b765cf3c33343c3ab86c8881efdc8d59ca39f83db3764a4a7ed914232(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.SnapshotOptionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__680d80155d5ae83f04e3424363da6e02e0b84f79409cd217183b2aa29d023cc3(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDomain.VPCOptionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f87c66d463ead5b66c67cb7e353724ea434618eeb817a8c7242128e5591a2f4(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    internal_user_database_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    master_user_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.MasterUserOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed78939109a8eb24a53c2761721d4eebf02f0588cdc51ed60b33c7fe73885a55(
    *,
    dedicated_master_count: typing.Optional[jsii.Number] = None,
    dedicated_master_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    dedicated_master_type: typing.Optional[builtins.str] = None,
    instance_count: typing.Optional[jsii.Number] = None,
    instance_type: typing.Optional[builtins.str] = None,
    warm_count: typing.Optional[jsii.Number] = None,
    warm_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    warm_type: typing.Optional[builtins.str] = None,
    zone_awareness_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.ZoneAwarenessConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    zone_awareness_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__747b9bca01a1280a0776eea7463efd93d8497450ff33345130c175838f88431e(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    identity_pool_id: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    user_pool_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e0f1ebd053a19a9765012da8fa39a12d4c64adc3e925edb61c05f47d6d5bafd(
    *,
    custom_endpoint: typing.Optional[builtins.str] = None,
    custom_endpoint_certificate_arn: typing.Optional[builtins.str] = None,
    custom_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    enforce_https: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    tls_security_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ed144ec5311c74d520e94e8ae2791f77cb085510ed92685de9777bca37e53e(
    *,
    ebs_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    iops: typing.Optional[jsii.Number] = None,
    throughput: typing.Optional[jsii.Number] = None,
    volume_size: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e65cc1fcde96ef2a65a601aa6c28b404f48a52192a50ccd7f9210e94f602e5c1(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468b348664e23264beb9c28791bbbb254375124e79c8ec806d17c29e2654f0b4(
    *,
    cloud_watch_logs_log_group_arn: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cbfd5bd4a3f00831d0cb0353b1d5661d2f081018d20b97c25cf8ff4ca1d7292(
    *,
    master_user_arn: typing.Optional[builtins.str] = None,
    master_user_name: typing.Optional[builtins.str] = None,
    master_user_password: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bdc3a722fc6292f992cb4d4c8115c8ef6884a075fda2285e9605a00f9d8e009(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__720b21a31a155cfee7407b649b1d2f6b11a2e2ffb0b61f4aa338065e495efc2a(
    *,
    automated_update_date: typing.Optional[builtins.str] = None,
    cancellable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    current_version: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    new_version: typing.Optional[builtins.str] = None,
    optional_deployment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    update_available: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    update_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01f6bca5cd9ac1be691e3fdccc21ec99cf16fc0cdf741d31a0f37d33e1e9161(
    *,
    automated_snapshot_start_hour: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e1db3011ae6d361340c52c4ad7597b1717df028126e25f89097ad2689b7538(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2eb69ed389f020e0e97452d58705bd6d389a453376bfc3d24e80f838a013c26(
    *,
    availability_zone_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86a3d8056fad835d634340f38e80e1175dbedfc662c8e4344ea597a7679dbb3f(
    *,
    access_policies: typing.Any = None,
    advanced_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    advanced_security_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.AdvancedSecurityOptionsInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cluster_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.ClusterConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cognito_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.CognitoOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    domain_endpoint_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.DomainEndpointOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    domain_name: typing.Optional[builtins.str] = None,
    ebs_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.EBSOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption_at_rest_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.EncryptionAtRestOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    engine_version: typing.Optional[builtins.str] = None,
    log_publishing_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.LogPublishingOptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    node_to_node_encryption_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.NodeToNodeEncryptionOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    snapshot_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.SnapshotOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDomain.VPCOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__005d853a7ee069b215a408691cbefec960068404ab07fba9407ab8fb85f03413(
    *,
    identity_pool_id: builtins.str,
    role: _aws_cdk_aws_iam_940a1ce0.IRole,
    user_pool_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da8aaf8726efe2585d177d847453ee5bd7133208c41eee250796e2cb77fa4be7(
    *,
    domain_name: builtins.str,
    certificate: typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate] = None,
    hosted_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1311fcf0967428ad2f85232918c5b0744a1a64beb3f8f79a441e548c7aead055(
    *,
    domain_arn: builtins.str,
    domain_endpoint: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5db33233ff5477597442204050938b92d0810e8d0d8921b187751b5e380b16d(
    *,
    version: EngineVersion,
    access_policies: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.PolicyStatement]] = None,
    advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    automated_snapshot_start_hour: typing.Optional[jsii.Number] = None,
    capacity: typing.Optional[typing.Union[CapacityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cognito_dashboards_auth: typing.Optional[typing.Union[CognitoOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_endpoint: typing.Optional[typing.Union[CustomEndpointOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    domain_name: typing.Optional[builtins.str] = None,
    ebs: typing.Optional[typing.Union[EbsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_version_upgrade: typing.Optional[builtins.bool] = None,
    encryption_at_rest: typing.Optional[typing.Union[EncryptionAtRestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    enforce_https: typing.Optional[builtins.bool] = None,
    fine_grained_access_control: typing.Optional[typing.Union[AdvancedSecurityOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    logging: typing.Optional[typing.Union[LoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    node_to_node_encryption: typing.Optional[builtins.bool] = None,
    removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
    tls_security_policy: typing.Optional[TLSSecurityPolicy] = None,
    use_unsigned_basic_auth: typing.Optional[builtins.bool] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    zone_awareness: typing.Optional[typing.Union[ZoneAwarenessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59de6b8ceae867d7e5210ad73941f395a6f0255d19f42499c5bb86695c58d697(
    *,
    enabled: typing.Optional[builtins.bool] = None,
    iops: typing.Optional[jsii.Number] = None,
    volume_size: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.EbsDeviceVolumeType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd93a31613dd73e2bb3f8c0e61fd9490f278773cbc40539f826254aef021971(
    *,
    enabled: typing.Optional[builtins.bool] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4d5f7b970e0509247f4d0117ef7efdbb38a51a6746f1d7913fcc5dd51f67e2(
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7294c705dad0adff616c7efb108f8b4bb4b655f6a4da36327ac23e1fd401f20b(
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__154758356627b471cb64c1cf145eefbb40507d92a0496857f0841c0ee6eda113(
    index: builtins.str,
    identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c431a80a1158b843bc917876ade588cf9deb6792d1c4347dba425e2bdb743b68(
    index: builtins.str,
    identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca45d262753693960fa2ea2044f8e36d2f931fc063b8707073c6058cead18769(
    index: builtins.str,
    identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7d0b73068f96c64a2b965ffb4026bcf0aef1881edd9efd0b8c05fa14c54e16e(
    path: builtins.str,
    identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab6dac8bc8b57b5c161a487aa8382ec4d208186948e17d1abcf38d5c43f376f9(
    path: builtins.str,
    identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405d9581fcae9e57d3ff9e79b03fdb1a00cf51e9389b312deb5dbfa43f2f36ca(
    path: builtins.str,
    identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4e2800f2b5342351704cde1f02589b549bc0f8493f4ac30f2f2df97db7ed48(
    identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__add23aa82707022dd48d02a4641fb998dc92c3cc94d29ddc0cec4bb1ce746548(
    identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5594d6783cc90d98b4fbdac1df535c1405330fca0f6f9388a5935fbf3c285638(
    identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9938780143ebac33d9de983b38db3e0f01531ffa28cceebabead4a1b983c1d75(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70be678aa9f41d60ec7aa4fbb915e4bb0bd11e12c6c4db5da1cfade0267863af(
    *,
    app_log_enabled: typing.Optional[builtins.bool] = None,
    app_log_group: typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup] = None,
    audit_log_enabled: typing.Optional[builtins.bool] = None,
    audit_log_group: typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup] = None,
    slow_index_log_enabled: typing.Optional[builtins.bool] = None,
    slow_index_log_group: typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup] = None,
    slow_search_log_enabled: typing.Optional[builtins.bool] = None,
    slow_search_log_group: typing.Optional[_aws_cdk_aws_logs_6c4320fb.ILogGroup] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2cab49e9c5b8a4df2f940c58aa9ddd79a4d82922c29c239444980b1bcc6bf4b(
    *,
    availability_zone_count: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f1a9d05f3f30ee0463b637624b1b2ff65dcfb2ca7e1812cabfa2db4fa0310a9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    version: EngineVersion,
    access_policies: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.PolicyStatement]] = None,
    advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    automated_snapshot_start_hour: typing.Optional[jsii.Number] = None,
    capacity: typing.Optional[typing.Union[CapacityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cognito_dashboards_auth: typing.Optional[typing.Union[CognitoOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_endpoint: typing.Optional[typing.Union[CustomEndpointOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    domain_name: typing.Optional[builtins.str] = None,
    ebs: typing.Optional[typing.Union[EbsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_version_upgrade: typing.Optional[builtins.bool] = None,
    encryption_at_rest: typing.Optional[typing.Union[EncryptionAtRestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    enforce_https: typing.Optional[builtins.bool] = None,
    fine_grained_access_control: typing.Optional[typing.Union[AdvancedSecurityOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    logging: typing.Optional[typing.Union[LoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    node_to_node_encryption: typing.Optional[builtins.bool] = None,
    removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
    tls_security_policy: typing.Optional[TLSSecurityPolicy] = None,
    use_unsigned_basic_auth: typing.Optional[builtins.bool] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    zone_awareness: typing.Optional[typing.Union[ZoneAwarenessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dcd5a14bd283abea946b904876ca0ed1dcae1faf2a596b5815089eca45974cd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domain_arn: builtins.str,
    domain_endpoint: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e90fbc1d5ddcfb4b38ad319535ce4a3d6dc4c4cd7fd47f50f4cabe975e90c7c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    domain_endpoint: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b772037660425e6a8436f6516d62145875674ff1bea486a8c9a4cc0204a97107(
    *access_policy_statements: _aws_cdk_aws_iam_940a1ce0.PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed7af745c35ccbfc7d89381475d15972f44a9504e19cc5295d2d57fe19f6884(
    index: builtins.str,
    identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be78c8f0c8113e612f28c82d3574a3b24833aafe52cdb0bc039c4bb2f518b8e8(
    index: builtins.str,
    identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7a2fc087ab97c6607a56da8e329df429b8679db521bdd39584120377cc5ca97(
    index: builtins.str,
    identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff234922defecc238abfb81ef4c8ccd1ed7630e513b64631b34ff0265196420(
    path: builtins.str,
    identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5587a92a52830897ebc88b531e06de37c5ff9ded885692e58a98b9580fb92eb4(
    path: builtins.str,
    identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134bc9072df45210b7b032d40fa58f617003ec9ad96c4533fc9651c8069201ca(
    path: builtins.str,
    identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80cda93c959869d61f0d3a6a10e7322f22fcd23de1d846ce4dce21edbaf98161(
    identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45352bd7d92475d75ad2b34ba73c51f26a90f2e9d1454e70d81be9215d8bea6e(
    identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a025f18643464ab5b722c6bbd540f69976176fe10c52265e0d86f6e56d641e(
    identity: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a0afd3e74cdb03b0f84cfed4d295b0bffee98d99ac2090c00ca3c4fca0ba0c(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass
