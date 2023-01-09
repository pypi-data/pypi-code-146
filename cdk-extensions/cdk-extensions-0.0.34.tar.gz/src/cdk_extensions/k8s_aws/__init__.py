'''
# K8S AWS Construct Library

Provides Kubernetes resources for integrating with AWS services.

## Fargate Logging

Fargate logging causes the output of pods running on EKS Farget to be sent to a logging service for storage and review.

By default, logs are written to CloudWatch Logs.

Enable Fargate logging on an EKS cluster:

```
declare const cluster: eks.FargateCluster;

const logger = new k8s_aws.FargateLogger(this, 'logger', {
    cluster: cluster,
    fargateProfiles: [
        cluster.defaultProfile
    ]
});
```

Permissions for sending logs to their configured destination are added to the Fargate profiles associated with the logger.

When adding new Fargate Profiles be sure to associate them with the logger to ensure they have sufficient permissions to write logs.

```
declare const profile: eks.FargateProfile;
declare const logger: k8s_aws.FargateLogger;

logger.addFargateProfile(profile);
```

Configure logging to write to a Kinesis Firehose delivery stream:

```
declare const cluster: eks.FargateCluster;
declare const deliveryStream: kinesis_hirehose.DeliveryStream;

const logger = new k8s_aws.FargateLogger(this, 'logger', {
    cluster: cluster,
    fargateProfiles: [
        cluster.defaultProfile
    ],
    outputs: [
        k8s_aws.FluentBitOutput.kinesisFirehose(k8s_aws.FluentBitMatch.ALL, deliveryStream);
    ]
});
```

Configure logging to write to a Kinesis data stream:

```
declare const cluster: eks.FargateCluster;
declare const stream: kinesis.Stream;

const logger = new k8s_aws.FargateLogger(this, 'logger', {
    cluster: cluster,
    fargateProfiles: [
        cluster.defaultProfile
    ],
    outputs: [
        k8s_aws.FluentBitOutput.kinesis(k8s_aws.FluentBitMatch.ALL, stream);
    ]
});
```

Configure logging to write to an OpenSearch domain:

```
declare const cluster: eks.FargateCluster;
declare const domain: opensearch.Domain;

const logger = new k8s_aws.FargateLogger(this, 'logger', {
    cluster: cluster,
    fargateProfiles: [
        cluster.defaultProfile
    ],
    outputs: [
        k8s_aws.FluentBitOutput.opensearch(k8s_aws.FluentBitMatch.ALL, domain);
    ]
});
```

Filter out log messages matching the AWS load balancer health check user agent:

```
declare const logger: k8s_aws.FargateLogger;

logger.addFilter(k8s_aws.FluentBitFilter.grep(k8s_aws.FluentBitMatch.ALL, {
    exclude: true,
    key: 'log',
    regex: 'ELB-HealthChecker'
}));
```

## Container Insights

[AWS Container Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContainerInsights.html) provides advanced diagnostic and performance metrics for your containerized applications running on AWS. For EKS cluster, Container Insights is provided by using [AWS Distro for OpenTelemetry](https://aws.amazon.com/blogs/containers/introducing-amazon-cloudwatch-container-insights-for-amazon-eks-fargate-using-aws-distro-for-opentelemetry/).

To enable Container Insights for pods running on your EKS cluster:

```
declare const cluster: eks.Cluster;

const collector = new k8s_aws.AdotCollector(this, 'adot-collector', {
    cluster: cluster
});
```

## Route 53

Enable management of Route 53 hosted zones for ingress and service hosts:

```
declare const cluster: eks.Cluster;

const manager = new k8s_aws.Route53Dns(this, 'route53-dns', {
    cluster: cluster
});
```

Only enable managment of Route 53 DNS to only records that end with `example.com`:

```
declare const manager: k8s_aws.Route53Dns;

manager.addDomainFilter('example.com');
```

Only allow management for hosted zones that are tagged with `managed-dns=enabled`:

```
declare const manager: k8s_aws.Route53Dns;

manager.addZoneTag({
    key: 'managed-dns',
    value: 'enabled'
});
```

Only allow creates and updates of DNS records and not deletes:

```
declare const cluster: eks.Cluster;

const manager = new k8s_aws.Route53Dns(this, 'route53-dns', {
    cluster: cluster,
    syncPolicy: ExternalDnsSyncPolicy.UPSERT_ONLY
});
```

## Secrets Manager

Enable synchronization of specific secret between Secrets Manager and Kubernetes:

```
declare const cluster: eks.Cluster;

const operator = new k8s_aws.ExternalSecretsOperator(this, 'external-secrets', {
    cluster: cluster
});
```

To tell the external secrets operator to synchronise a secret:

```
declase const operator: k8s_aws.ExternalSecretsOperator;
declare const secret: secretsmanager.Secret;

operator.registerSecretsManagerSecret('sychronized-secret', secret);
```

Give the secret a human friendly name in Kubernetes:

```
declase const operator: k8s_aws.ExternalSecretsOperator;
declare const secret: secretsmanager.Secret;

operator.registerSecretsManagerSecret('sychronized-secret', secret, {
    name: 'database-secret'
});
```

Only import specific JSON keys from a secret:

```
declase const operator: k8s_aws.ExternalSecretsOperator;
declare const secret: secretsmanager.Secret;

operator.registerSecretsManagerSecret('sychronized-secret', secret, {
    fields: [
        { kubernetesKey: 'username' },
        { kubernetesKey: 'password' },
    ]
});
```

Map secret fields that need to be different between Secrets Manager and Kubernetes.

```
declase const operator: k8s_aws.ExternalSecretsOperator;
declare const secret: secretsmanager.Secret;

operator.registerSecretsManagerSecret('sychronized-secret', secret, {
    fields: [
        {
            kubernetesKey: 'user',
            remoteKey: 'username',
        },
        {
            kubernetesKey: 'pass',
            remoteKey: 'password'
        },
    ]
});
```

## Echoserver

A basic Kubernetes test service that can be used for testing Kubernetes cluster integrations.

This is a simple HTTP service that listens for incoming requests and echo details of requests back to the user.

Log messages are produced for each request and provide a convenient way to test logging filter and output configurations.

To create an echoserver service:

```
declare const cluster: eks.Cluster;

const echoserver = new k8s_aws.Echoserver(this, 'echoserver', {
    cluster: cluster
});
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

import aws_cdk
import aws_cdk.aws_ec2
import aws_cdk.aws_eks
import aws_cdk.aws_iam
import aws_cdk.aws_kinesis
import aws_cdk.aws_logs
import aws_cdk.aws_opensearchservice
import aws_cdk.aws_secretsmanager
import aws_cdk.aws_ssm
import constructs
from ..core import DataSize as _DataSize_d20aaece
from ..kinesis_firehose import IDeliveryStream as _IDeliveryStream_cf5feed7
from ..route53 import (
    Domain as _Domain_165656f2,
    DomainDiscovery as _DomainDiscovery_440eb9b9,
    IDnsResolvable as _IDnsResolvable_adf49001,
)


class AdotCollector(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.AdotCollector",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster: aws_cdk.aws_eks.ICluster,
        create_namespace: typing.Optional[builtins.bool] = None,
        namespace: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the AdotCollector class.

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the resource and used in resource naming. Must be unique within the context of 'scope'.
        :param cluster: The EKS cluster where the ADOT Collector will be deployed.
        :param create_namespace: Flag wich sets whether the deploy of the ADOT collector should include creating the Kubernetes namespace the service will be deployed to. Default: true
        :param namespace: The Kubernetes namespace where resources related to the ADOT collector will be created. Default: {@link AdotCollector.DEFAULT_NAMESPACE}
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AdotCollector.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AdotCollectorProps(
            cluster=cluster,
            create_namespace=create_namespace,
            namespace=namespace,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_NAMESPACE")
    def DEFAULT_NAMESPACE(cls) -> builtins.str:
        '''The default Kubernetes namespace where resources related to the ADOT collector will be created if no overriding input is provided.'''
        return typing.cast(builtins.str, jsii.sget(cls, "DEFAULT_NAMESPACE"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_eks.ICluster:
        '''The EKS cluster where the ADOT Collector will be deployed.

        :group: Inputs
        '''
        return typing.cast(aws_cdk.aws_eks.ICluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="createNamespace")
    def create_namespace(self) -> builtins.bool:
        '''Flag wich sets whether the deploy of the ADOT collector should include creating the Kubernetes namespace the service will be deployed to.

        :group: Inputs
        '''
        return typing.cast(builtins.bool, jsii.get(self, "createNamespace"))

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> aws_cdk.aws_eks.KubernetesManifest:
        '''The Kubernetes manifest used to deploy the ADOT Collector.

        :group: Resources
        '''
        return typing.cast(aws_cdk.aws_eks.KubernetesManifest, jsii.get(self, "manifest"))

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        '''The Kubernetes namespace where resources related to the ADOT collector will be created.

        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> aws_cdk.aws_eks.ServiceAccount:
        '''The Kubernetes service account that allows the ADOT collector to gather metric information and publish it to CloudWatch.

        :group: Resources
        '''
        return typing.cast(aws_cdk.aws_eks.ServiceAccount, jsii.get(self, "serviceAccount"))


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.AdotCollectorProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "cluster": "cluster",
        "create_namespace": "createNamespace",
        "namespace": "namespace",
    },
)
class AdotCollectorProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        cluster: aws_cdk.aws_eks.ICluster,
        create_namespace: typing.Optional[builtins.bool] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Condifuration for the AdorCollector resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param cluster: The EKS cluster where the ADOT Collector will be deployed.
        :param create_namespace: Flag wich sets whether the deploy of the ADOT collector should include creating the Kubernetes namespace the service will be deployed to. Default: true
        :param namespace: The Kubernetes namespace where resources related to the ADOT collector will be created. Default: {@link AdotCollector.DEFAULT_NAMESPACE}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AdotCollectorProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument create_namespace", value=create_namespace, expected_type=type_hints["create_namespace"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if create_namespace is not None:
            self._values["create_namespace"] = create_namespace
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster(self) -> aws_cdk.aws_eks.ICluster:
        '''The EKS cluster where the ADOT Collector will be deployed.'''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_eks.ICluster, result)

    @builtins.property
    def create_namespace(self) -> typing.Optional[builtins.bool]:
        '''Flag wich sets whether the deploy of the ADOT collector should include creating the Kubernetes namespace the service will be deployed to.

        :default: true
        '''
        result = self._values.get("create_namespace")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The Kubernetes namespace where resources related to the ADOT collector will be created.

        :default: {@link AdotCollector.DEFAULT_NAMESPACE}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdotCollectorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.AppendedRecord",
    jsii_struct_bases=[],
    name_mapping={"field_name": "fieldName", "value": "value"},
)
class AppendedRecord:
    def __init__(self, *, field_name: builtins.str, value: builtins.str) -> None:
        '''Represents a record field to be added by the record modifier Fluent Bit filter plugin.

        :param field_name: The name of the field to be added.
        :param value: The value that the added field should be set to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AppendedRecord.__init__)
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[str, typing.Any] = {
            "field_name": field_name,
            "value": value,
        }

    @builtins.property
    def field_name(self) -> builtins.str:
        '''The name of the field to be added.'''
        result = self._values.get("field_name")
        assert result is not None, "Required property 'field_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value that the added field should be set to.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppendedRecord(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.AwsSecretStoreProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "cluster": "cluster",
        "service": "service",
        "name": "name",
        "namespace": "namespace",
    },
)
class AwsSecretStoreProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        cluster: aws_cdk.aws_eks.ICluster,
        service: builtins.str,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration options for adding a new secret store resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param cluster: The EKS cluster where the secret store should be created.
        :param service: The name of the service provider backing the secret store.
        :param name: A human friendly name for the secret store.
        :param namespace: The Kubernetes namespace where the secret store should be created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AwsSecretStoreProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
            "service": service,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster(self) -> aws_cdk.aws_eks.ICluster:
        '''The EKS cluster where the secret store should be created.'''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_eks.ICluster, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''The name of the service provider backing the secret store.'''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A human friendly name for the secret store.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The Kubernetes namespace where the secret store should be created.'''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsSecretStoreProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_ec2.IConnectable, _IDnsResolvable_adf49001)
class Echoserver(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.Echoserver",
):
    '''Creates a simple Kubernetes test service using the Google echoserver test image.

    The server listens for incoming web requests and echos the details of the
    request back to the user. Each request results in output being written to
    the Docker log providing a convenient way to test logging setup.

    :see: `Google echoserver image repository <https://console.cloud.google.com/gcr/images/google-containers/GLOBAL/echoserver>`_
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster: aws_cdk.aws_eks.ICluster,
        domain_discovery: typing.Optional[_DomainDiscovery_440eb9b9] = None,
        load_balancer_subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        replicas: typing.Optional[jsii.Number] = None,
        security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subdomain: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the Echoserver class.

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the resource and used in resource naming. Must be unique within the context of 'scope'.
        :param cluster: The EKS Cluster where the service should be deployed.
        :param domain_discovery: Determines the behavior of automatic DNS discovery and configuration. Default: DomainDiscovery.PUBLIC
        :param load_balancer_subnets: The subnets where the load balancer should be created.
        :param name: The name of the Kubernetes service to be created. Default: 'echoserver'
        :param namespace: The Kubernetes namespace where the service should be created. Default: 'default'
        :param port: The port which netcat should listen on. Default: 80
        :param replicas: The number of replicas that should exist. Default: 1
        :param security_groups: The Security groups which should be applied to the service.
        :param subdomain: A subdomain that should be prefixed to the beginning of all registered domains.
        :param tag: The Docker tag specifying the version of echoserver to use.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Echoserver.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EchoserverProps(
            cluster=cluster,
            domain_discovery=domain_discovery,
            load_balancer_subnets=load_balancer_subnets,
            name=name,
            namespace=namespace,
            port=port,
            replicas=replicas,
            security_groups=security_groups,
            subdomain=subdomain,
            tag=tag,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="registerDomain")
    def register_domain(self, domain: _Domain_165656f2) -> None:
        '''
        :param domain: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Echoserver.register_domain)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
        return typing.cast(None, jsii.invoke(self, "registerDomain", [domain]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_DOMAIN_DISCOVERY")
    def DEFAULT_DOMAIN_DISCOVERY(cls) -> _DomainDiscovery_440eb9b9:
        '''The default setting controlling how automatic DNS configuration should behave if none is provided as input.'''
        return typing.cast(_DomainDiscovery_440eb9b9, jsii.sget(cls, "DEFAULT_DOMAIN_DISCOVERY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_LOAD_BALANCER_SUBNETS")
    def DEFAULT_LOAD_BALANCER_SUBNETS(cls) -> aws_cdk.aws_ec2.SubnetSelection:
        '''Default subnet selection that will be used if none is provided as input.'''
        return typing.cast(aws_cdk.aws_ec2.SubnetSelection, jsii.sget(cls, "DEFAULT_LOAD_BALANCER_SUBNETS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_NAME")
    def DEFAULT_NAME(cls) -> builtins.str:
        '''Default name of the Kubernetes service that will be created if none is provided as input.'''
        return typing.cast(builtins.str, jsii.sget(cls, "DEFAULT_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_NAMESPACE")
    def DEFAULT_NAMESPACE(cls) -> builtins.str:
        '''Default Kubernetes namespace where the service will be created if none is provided as input.'''
        return typing.cast(builtins.str, jsii.sget(cls, "DEFAULT_NAMESPACE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_PORT")
    def DEFAULT_PORT(cls) -> jsii.Number:
        '''Default port where the service will be accessible if none is provided as input.'''
        return typing.cast(jsii.Number, jsii.sget(cls, "DEFAULT_PORT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_REPLICAS")
    def DEFAULT_REPLICAS(cls) -> jsii.Number:
        '''Default number of replicas that should be running is none is provided as input.'''
        return typing.cast(jsii.Number, jsii.sget(cls, "DEFAULT_REPLICAS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_REPOSITORY")
    def DEFAULT_REPOSITORY(cls) -> builtins.str:
        '''The Docker repository where the echoserver image will be pulled from.'''
        return typing.cast(builtins.str, jsii.sget(cls, "DEFAULT_REPOSITORY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_TAG")
    def DEFAULT_TAG(cls) -> builtins.str:
        '''The default Docker tag of the image to use if none is provided as input.'''
        return typing.cast(builtins.str, jsii.sget(cls, "DEFAULT_TAG"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_eks.ICluster:
        '''The EKS Cluster where the service should be deployed.

        :group: Inputs
        '''
        return typing.cast(aws_cdk.aws_eks.ICluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        '''Access for network connections.

        :group: IConnectable
        '''
        return typing.cast(aws_cdk.aws_ec2.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="domainDiscovery")
    def domain_discovery(self) -> _DomainDiscovery_440eb9b9:
        '''Determines the behavior of automatic DNS discovery and configuration.

        :group: IDnsResolvable
        '''
        return typing.cast(_DomainDiscovery_440eb9b9, jsii.get(self, "domainDiscovery"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerSubnets")
    def load_balancer_subnets(self) -> aws_cdk.aws_ec2.SubnetSelection:
        '''The subnets where the load balancer should be created..

        :group: Inputs
        '''
        return typing.cast(aws_cdk.aws_ec2.SubnetSelection, jsii.get(self, "loadBalancerSubnets"))

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> aws_cdk.aws_eks.KubernetesManifest:
        '''The Kubernetes manifest that creates the ConfigMap that Fargate uses to configure logging.

        :group: Resources
        '''
        return typing.cast(aws_cdk.aws_eks.KubernetesManifest, jsii.get(self, "manifest"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the Kubernetes service to be created.

        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        '''The Kubernetes namespace where the service should be created.

        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        '''The port which netcat should listen on.

        :group: Inputs
        '''
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="replicas")
    def replicas(self) -> jsii.Number:
        '''The number of replicas that should exist.

        :group: Inputs
        '''
        return typing.cast(jsii.Number, jsii.get(self, "replicas"))

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        '''The Docker tag specifying the version of echoserver to use.

        :see: `Google echoserver image repository <https://console.cloud.google.com/gcr/images/google-containers/GLOBAL/echoserver>`_
        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @builtins.property
    @jsii.member(jsii_name="subdomain")
    def subdomain(self) -> typing.Optional[builtins.str]:
        '''A subdomain that should be prefixed to the beginning of all registered domains.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subdomain"))


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.EchoserverProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "cluster": "cluster",
        "domain_discovery": "domainDiscovery",
        "load_balancer_subnets": "loadBalancerSubnets",
        "name": "name",
        "namespace": "namespace",
        "port": "port",
        "replicas": "replicas",
        "security_groups": "securityGroups",
        "subdomain": "subdomain",
        "tag": "tag",
    },
)
class EchoserverProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        cluster: aws_cdk.aws_eks.ICluster,
        domain_discovery: typing.Optional[_DomainDiscovery_440eb9b9] = None,
        load_balancer_subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        replicas: typing.Optional[jsii.Number] = None,
        security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subdomain: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for the Echoserver resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param cluster: The EKS Cluster where the service should be deployed.
        :param domain_discovery: Determines the behavior of automatic DNS discovery and configuration. Default: DomainDiscovery.PUBLIC
        :param load_balancer_subnets: The subnets where the load balancer should be created.
        :param name: The name of the Kubernetes service to be created. Default: 'echoserver'
        :param namespace: The Kubernetes namespace where the service should be created. Default: 'default'
        :param port: The port which netcat should listen on. Default: 80
        :param replicas: The number of replicas that should exist. Default: 1
        :param security_groups: The Security groups which should be applied to the service.
        :param subdomain: A subdomain that should be prefixed to the beginning of all registered domains.
        :param tag: The Docker tag specifying the version of echoserver to use.
        '''
        if isinstance(load_balancer_subnets, dict):
            load_balancer_subnets = aws_cdk.aws_ec2.SubnetSelection(**load_balancer_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(EchoserverProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument domain_discovery", value=domain_discovery, expected_type=type_hints["domain_discovery"])
            check_type(argname="argument load_balancer_subnets", value=load_balancer_subnets, expected_type=type_hints["load_balancer_subnets"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument replicas", value=replicas, expected_type=type_hints["replicas"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subdomain", value=subdomain, expected_type=type_hints["subdomain"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if domain_discovery is not None:
            self._values["domain_discovery"] = domain_discovery
        if load_balancer_subnets is not None:
            self._values["load_balancer_subnets"] = load_balancer_subnets
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace
        if port is not None:
            self._values["port"] = port
        if replicas is not None:
            self._values["replicas"] = replicas
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subdomain is not None:
            self._values["subdomain"] = subdomain
        if tag is not None:
            self._values["tag"] = tag

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster(self) -> aws_cdk.aws_eks.ICluster:
        '''The EKS Cluster where the service should be deployed.'''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_eks.ICluster, result)

    @builtins.property
    def domain_discovery(self) -> typing.Optional[_DomainDiscovery_440eb9b9]:
        '''Determines the behavior of automatic DNS discovery and configuration.

        :default: DomainDiscovery.PUBLIC
        '''
        result = self._values.get("domain_discovery")
        return typing.cast(typing.Optional[_DomainDiscovery_440eb9b9], result)

    @builtins.property
    def load_balancer_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        '''The subnets where the load balancer should be created.'''
        result = self._values.get("load_balancer_subnets")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the Kubernetes service to be created.

        :default: 'echoserver'
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The Kubernetes namespace where the service should be created.

        :default: 'default'
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port which netcat should listen on.

        :default: 80
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def replicas(self) -> typing.Optional[jsii.Number]:
        '''The number of replicas that should exist.

        :default: 1
        '''
        result = self._values.get("replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        '''The Security groups which should be applied to the service.'''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]], result)

    @builtins.property
    def subdomain(self) -> typing.Optional[builtins.str]:
        '''A subdomain that should be prefixed to the beginning of all registered domains.'''
        result = self._values.get("subdomain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''The Docker tag specifying the version of echoserver to use.

        :see: `Google echoserver image repository <https://console.cloud.google.com/gcr/images/google-containers/GLOBAL/echoserver>`_
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EchoserverProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.k8s_aws.ElasticsearchCompressionFormat")
class ElasticsearchCompressionFormat(enum.Enum):
    GZIP = "GZIP"
    '''Gzip compression format.'''


class ElasticsearchOutputBufferSize(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.ElasticsearchOutputBufferSize",
):
    '''Represents the size of the Elasticsearch output buffer to be used by Fluent Bit.'''

    @jsii.member(jsii_name="bytes")
    @builtins.classmethod
    def bytes(cls, size: _DataSize_d20aaece) -> "ElasticsearchOutputBufferSize":
        '''Set the output buffer to a specified data size.

        :param size: The size of the output buffer.

        :return:

        An output buffer size object representing the specified buffer
        size.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ElasticsearchOutputBufferSize.bytes)
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
        return typing.cast("ElasticsearchOutputBufferSize", jsii.sinvoke(cls, "bytes", [size]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, value: builtins.str) -> "ElasticsearchOutputBufferSize":
        '''An escape hatch that allows an arbitrary value to be set for the Elasticsearch buffer output property.

        :param value: The value to use for the Elasticsearch buffer output property.

        :return:

        A ``ElasticsearchOutputBufferSize`` object representing the
        passed value.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ElasticsearchOutputBufferSize.of)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ElasticsearchOutputBufferSize", jsii.sinvoke(cls, "of", [value]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UNLIMITED")
    def UNLIMITED(cls) -> "ElasticsearchOutputBufferSize":
        '''Set the output buffer size to unlimited.'''
        return typing.cast("ElasticsearchOutputBufferSize", jsii.sget(cls, "UNLIMITED"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        '''The value to use for the Elasticsearch buffer output property.'''
        return typing.cast(builtins.str, jsii.get(self, "value"))


class EmitterStorageType(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.EmitterStorageType",
):
    '''Define a buffering mechanism for the new records created by the rewrite tag Fluent Bit filter plugin.'''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, name: builtins.str) -> "EmitterStorageType":
        '''An escape hatch that allows for specifying a custom value for the rewrite tag plugin's ``Emitter_Storage.type`` field.

        :param name: The name of the buffering type to use.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(EmitterStorageType.of)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("EmitterStorageType", jsii.sinvoke(cls, "of", [name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="FILESYSTEM")
    def FILESYSTEM(cls) -> "EmitterStorageType":
        '''Buffer records on the filesystem.

        This is recommended if the destination for new records generated might
        face backpressure due to latency or slow network speeds.
        '''
        return typing.cast("EmitterStorageType", jsii.sget(cls, "FILESYSTEM"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MEMORY")
    def MEMORY(cls) -> "EmitterStorageType":
        '''Buffer records in memory.

        This is the default behavior.
        '''
        return typing.cast("EmitterStorageType", jsii.sget(cls, "MEMORY"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the emitter storage type as it should appear in the plugin configuration file.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.enum(jsii_type="cdk-extensions.k8s_aws.ExternalDnsLogFormat")
class ExternalDnsLogFormat(enum.Enum):
    '''The format external dns should use to output logs.'''

    JSON = "JSON"
    '''Output logs will be written as JSON objects.'''
    TEXT = "TEXT"
    '''Output logs will be written in plain text.'''


@jsii.enum(jsii_type="cdk-extensions.k8s_aws.ExternalDnsLogLevel")
class ExternalDnsLogLevel(enum.Enum):
    '''Verbosity of the logs generated by the external-dns service.'''

    PANIC = "PANIC"
    '''Set log level to 'panic'.'''
    DEBUG = "DEBUG"
    '''Set log level to 'debug'.'''
    INFO = "INFO"
    '''Set log level to 'info'.'''
    WARNING = "WARNING"
    '''Set log level to 'warning'.'''
    ERROR = "ERROR"
    '''Set log level to 'error'.'''
    FATAL = "FATAL"
    '''Set log level to 'fatal'.'''
    TRACE = "TRACE"
    '''Set log level to 'trace'.'''


class ExternalDnsRegistry(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.ExternalDnsRegistry",
):
    '''Helper class that provides access to the available ExternalDns registry options.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="awsServiceDiscovery")
    @builtins.classmethod
    def aws_service_discovery(cls) -> "AwsServiceDiscoveryRegistry":
        '''An ExternalDNS registry that tracks DNS record ownership information using AWS Service Discovery.

        :return:

        A ExternalDNS registry object configured to use AWS Cloud Map
        for ownership information.

        :see: `AWS Cloud Map <https://docs.aws.amazon.com/cloud-map/latest/dg/what-is-cloud-map.html>`_
        '''
        return typing.cast("AwsServiceDiscoveryRegistry", jsii.sinvoke(cls, "awsServiceDiscovery", []))

    @jsii.member(jsii_name="noop")
    @builtins.classmethod
    def noop(cls) -> "NoopRegistry":
        '''A placeholder ExternalDNS registry that says ExternalDNS should use not use a registry.

        When configuring ExternalDNS without a registry, the service has no idea
        the original creator and maintainer of DNS records. This means that
        there are likely to be conflicts if there are multiple services that
        could create or change DNS records in the same zone.

        :return:

        An object that instructs ExternalDNS to not store record
        ownership information and will perform record updates without
        validation.
        '''
        return typing.cast("NoopRegistry", jsii.sinvoke(cls, "noop", []))

    @jsii.member(jsii_name="txt")
    @builtins.classmethod
    def txt(
        cls,
        *,
        owner_id: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> "TxtRegistry":
        '''An ExternalDNS registry that tracks DNS record ownership information using DNS TXT records.

        :param owner_id: A unique identifier that is used to establish ownership of managed DNS records. Prevents conflicts in the event of multiple clusters running external-dns. Default: Unique address of the owning CDK node.
        :param prefix: A prefix to be added top TXT ownership records. By default, the ownership record is a TXT record with the same name as the managed record that was created. This causes issues as some record types (CNAME's) do not allow duplicate records of a different type. This prefix is used to prevent such name collissions while still allowing DNS ownership records to be created. Default: 'edns.''

        :return:

        A ExternalDNS registry object configured to use DNS TXT records
        for ownership information.

        :see: `About TXT records <https://support.google.com/a/answer/2716800?hl=en>`_
        '''
        options = TxtRegistryOptions(owner_id=owner_id, prefix=prefix)

        return typing.cast("TxtRegistry", jsii.sinvoke(cls, "txt", [options]))


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.ExternalDnsRegistryConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "registry_type": "registryType",
        "permissions": "permissions",
        "properties": "properties",
    },
)
class ExternalDnsRegistryConfiguration:
    def __init__(
        self,
        *,
        registry_type: builtins.str,
        permissions: typing.Optional[typing.Sequence[aws_cdk.aws_iam.PolicyStatement]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''
        :param registry_type: 
        :param permissions: 
        :param properties: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ExternalDnsRegistryConfiguration.__init__)
            check_type(argname="argument registry_type", value=registry_type, expected_type=type_hints["registry_type"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[str, typing.Any] = {
            "registry_type": registry_type,
        }
        if permissions is not None:
            self._values["permissions"] = permissions
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def registry_type(self) -> builtins.str:
        result = self._values.get("registry_type")
        assert result is not None, "Required property 'registry_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def permissions(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalDnsRegistryConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.k8s_aws.ExternalDnsSyncPolicy")
class ExternalDnsSyncPolicy(enum.Enum):
    '''Controls the operations ExternalDNS will perform on the records it manages.'''

    SYNC = "SYNC"
    '''Full sync mode.

    Records will be created, updated, and deleted based on the
    statis of their backing resources on the Kubernetes cluster.
    '''
    UPSERT_ONLY = "UPSERT_ONLY"
    '''Only allow create and update operations.

    Records will have their values
    set based on the status of their backing Kubernetes resources, however if
    those resources are removed the DNS records will be retained, set to their
    last configured value.
    '''


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.ExternalDnsZoneTag",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class ExternalDnsZoneTag:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''Specifies a tag that can be used to restrict which Hosted Zone external-dns will have access to.

        :param key: The name of the tag to filter on.
        :param value: The value of the tag to filter on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ExternalDnsZoneTag.__init__)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''The name of the tag to filter on.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value of the tag to filter on.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalDnsZoneTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.k8s_aws.ExternalDnsZoneType")
class ExternalDnsZoneType(enum.Enum):
    '''Controls the types of Hosted Zones external DNS will create records for.'''

    ALL = "ALL"
    '''Create DNS records for both public and private hosted zones.'''
    PRIVATE = "PRIVATE"
    '''Only create DNS records for private hosted zones.'''
    PUBLIC = "PUBLIC"
    '''Only create DNS records for public hosted zones.'''


class ExternalSecret(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.ExternalSecret",
):
    '''Represents a Kubernetes secret that is being synchronized from an external provider.

    On a technical level, provides the configuration for how the external
    secrets operator service should manage the synchronization of the Kubernetes
    secret.
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster: aws_cdk.aws_eks.ICluster,
        secret_store: "ISecretStore",
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        refresh_interval: typing.Optional[aws_cdk.Duration] = None,
        secrets: typing.Optional[typing.Sequence["ISecretReference"]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the ExternalSecret class.

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the resource and used in resource naming. Must be unique within the context of 'scope'.
        :param cluster: The EKS cluster where the secret should be created.
        :param secret_store: The Kubernetes secret store resource that provides details and permissions to use for importing secrets from the provider.
        :param name: The name to use for the Kubernetes secret resource when it is synchronized into the cluster.
        :param namespace: The name where the synchronized secret should be created.
        :param refresh_interval: The frequency at which synchronization should occur.
        :param secrets: The secrets to synchronize into this Kubernetes secret. If multiple secrets are provided their fields will be merged.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ExternalSecret.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ExternalSecretProps(
            cluster=cluster,
            secret_store=secret_store,
            name=name,
            namespace=namespace,
            refresh_interval=refresh_interval,
            secrets=secrets,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addSecret")
    def add_secret(self, secret: "ISecretReference") -> "ExternalSecret":
        '''Adds a provider secret reference to the synchronized Kubernetes secret.

        For external secrets that reference multiple provider secrets the keys of
        all provider secrets will be merged into the single Kubernetes secret.

        :param secret: The provider secret to reference.

        :return: The external secret resoiurce where the reference was added.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ExternalSecret.add_secret)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        return typing.cast("ExternalSecret", jsii.invoke(self, "addSecret", [secret]))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_eks.ICluster:
        '''The EKS cluster where the secret should be created.

        :group: Inputs
        '''
        return typing.cast(aws_cdk.aws_eks.ICluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> aws_cdk.aws_eks.KubernetesManifest:
        '''The Kubernetes manifest defining the configuration of how to synchronize the Kubernetes secret from the provider secrets.

        :group: Resources
        '''
        return typing.cast(aws_cdk.aws_eks.KubernetesManifest, jsii.get(self, "manifest"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name to use for the Kubernetes secret resource when it is synchronized into the cluster.

        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        '''The name of the Kubernetes secret.'''
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(self) -> typing.List["ISecretReference"]:
        '''The collection of referenced provider secrets that are referenced in the Kubernetes secret.

        :group: Inputs
        '''
        return typing.cast(typing.List["ISecretReference"], jsii.get(self, "secrets"))

    @builtins.property
    @jsii.member(jsii_name="secretStore")
    def secret_store(self) -> "ISecretStore":
        '''The Kubernetes secret store resource that provides details and permissions to use for importing secrets from the provider.

        :group: Inputs
        '''
        return typing.cast("ISecretStore", jsii.get(self, "secretStore"))

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The name where the synchronized secret should be created.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespace"))

    @builtins.property
    @jsii.member(jsii_name="refreshInterval")
    def refresh_interval(self) -> typing.Optional[aws_cdk.Duration]:
        '''The frequency at which synchronization should occur.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[aws_cdk.Duration], jsii.get(self, "refreshInterval"))


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.ExternalSecretOptions",
    jsii_struct_bases=[],
    name_mapping={"fields": "fields", "name": "name"},
)
class ExternalSecretOptions:
    def __init__(
        self,
        *,
        fields: typing.Optional[typing.Sequence[typing.Union["SecretFieldReference", typing.Dict[str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration options for adding a Kubernetes secret synced from an external provider to Kubernetes.

        :param fields: A collection of field mappings that tells the external secrets operator the structure of the Kubernetes secret to create and which how fields in the Kubernetes secret should map to fields in the secret from the external secret provider. Default: The Kubernetes secret will mirror the fields from the secret in the external provider.
        :param name: The name of the Kubernetes secret that will be created, as it will appear from within the Kubernetes cluster. Default: A name will be auto-generated.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ExternalSecretOptions.__init__)
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[str, typing.Any] = {}
        if fields is not None:
            self._values["fields"] = fields
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def fields(self) -> typing.Optional[typing.List["SecretFieldReference"]]:
        '''A collection of field mappings that tells the external secrets operator the structure of the Kubernetes secret to create and which how fields in the Kubernetes secret should map to fields in the secret from the external secret provider.

        :default:

        The Kubernetes secret will mirror the fields from the secret in
        the external provider.
        '''
        result = self._values.get("fields")
        return typing.cast(typing.Optional[typing.List["SecretFieldReference"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the Kubernetes secret that will be created, as it will appear from within the Kubernetes cluster.

        :default: A name will be auto-generated.
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalSecretOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.ExternalSecretProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "cluster": "cluster",
        "secret_store": "secretStore",
        "name": "name",
        "namespace": "namespace",
        "refresh_interval": "refreshInterval",
        "secrets": "secrets",
    },
)
class ExternalSecretProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        cluster: aws_cdk.aws_eks.ICluster,
        secret_store: "ISecretStore",
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        refresh_interval: typing.Optional[aws_cdk.Duration] = None,
        secrets: typing.Optional[typing.Sequence["ISecretReference"]] = None,
    ) -> None:
        '''Configuration for the ExternalSecret resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param cluster: The EKS cluster where the secret should be created.
        :param secret_store: The Kubernetes secret store resource that provides details and permissions to use for importing secrets from the provider.
        :param name: The name to use for the Kubernetes secret resource when it is synchronized into the cluster.
        :param namespace: The name where the synchronized secret should be created.
        :param refresh_interval: The frequency at which synchronization should occur.
        :param secrets: The secrets to synchronize into this Kubernetes secret. If multiple secrets are provided their fields will be merged.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ExternalSecretProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument secret_store", value=secret_store, expected_type=type_hints["secret_store"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument refresh_interval", value=refresh_interval, expected_type=type_hints["refresh_interval"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
            "secret_store": secret_store,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace
        if refresh_interval is not None:
            self._values["refresh_interval"] = refresh_interval
        if secrets is not None:
            self._values["secrets"] = secrets

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster(self) -> aws_cdk.aws_eks.ICluster:
        '''The EKS cluster where the secret should be created.'''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_eks.ICluster, result)

    @builtins.property
    def secret_store(self) -> "ISecretStore":
        '''The Kubernetes secret store resource that provides details and permissions to use for importing secrets from the provider.'''
        result = self._values.get("secret_store")
        assert result is not None, "Required property 'secret_store' is missing"
        return typing.cast("ISecretStore", result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name to use for the Kubernetes secret resource when it is synchronized into the cluster.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The name where the synchronized secret should be created.'''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def refresh_interval(self) -> typing.Optional[aws_cdk.Duration]:
        '''The frequency at which synchronization should occur.'''
        result = self._values.get("refresh_interval")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def secrets(self) -> typing.Optional[typing.List["ISecretReference"]]:
        '''The secrets to synchronize into this Kubernetes secret.

        If multiple secrets are provided their fields will be merged.
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.List["ISecretReference"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalSecretProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalSecretsOperator(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.ExternalSecretsOperator",
):
    '''External Secrets Operator is a Kubernetes operator that integrates external secret management systems like AWS Secrets Manager, HashiCorp Vault, Google Secrets Manager, Azure Key Vault and many more.

    The operator reads
    information from external APIs and automatically injects the values into a
    Kubernetes Secret.

    :see: `External Secrets Website <https://external-secrets.io/>`_
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster: aws_cdk.aws_eks.Cluster,
        create_namespace: typing.Optional[builtins.bool] = None,
        namespace: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the ExternalSecretsOperator class.

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the resource and used in resource naming. Must be unique within the context of 'scope'.
        :param cluster: The EKS cluster where the external secrets operator should be installed.
        :param create_namespace: Determines the behavior when the service is deployed to a namespace that doesn't already exist on the EKS cluster. When this flag is ``true`` and the namespace doesn't exist, the namespace will be created automatically. When this flag is ``false`` and the namespace doesn't exist, an error will occur and resource creation will fail. Default: true
        :param namespace: The Kubernetes namespace where the external secrets operator service should be installed and configured. Default: {@link ExternalSecretsOperator.DEFAULT_NAMESPACE}
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ExternalSecretsOperator.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ExternalSecretsOperatorProps(
            cluster=cluster,
            create_namespace=create_namespace,
            namespace=namespace,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="registerSecretsManagerSecret")
    def register_secrets_manager_secret(
        self,
        id: builtins.str,
        secret: aws_cdk.aws_secretsmanager.ISecret,
        *,
        namespace: typing.Optional[builtins.str] = None,
        fields: typing.Optional[typing.Sequence[typing.Union["SecretFieldReference", typing.Dict[str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> ExternalSecret:
        '''Registers a Secrets Manager secret with the external secrets operator, enabling syncing from the Secrets Manager secret into Kubernetes.

        :param id: A name to be associated with the resource and used in resource naming. Must be unique within for each secrets manager secret within a Kubernetes namespace.
        :param secret: The Secrets Manager secret to enable syncing for.
        :param namespace: The Kubernetes namespace where the synced secret should be created. Default: 'default'
        :param fields: A collection of field mappings that tells the external secrets operator the structure of the Kubernetes secret to create and which how fields in the Kubernetes secret should map to fields in the secret from the external secret provider. Default: The Kubernetes secret will mirror the fields from the secret in the external provider.
        :param name: The name of the Kubernetes secret that will be created, as it will appear from within the Kubernetes cluster. Default: A name will be auto-generated.

        :return: The external secret object that was created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ExternalSecretsOperator.register_secrets_manager_secret)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        options = NamespacedExternalSecretOptions(
            namespace=namespace, fields=fields, name=name
        )

        return typing.cast(ExternalSecret, jsii.invoke(self, "registerSecretsManagerSecret", [id, secret, options]))

    @jsii.member(jsii_name="registerSsmParameterSecret")
    def register_ssm_parameter_secret(
        self,
        id: builtins.str,
        parameter: aws_cdk.aws_ssm.IParameter,
        *,
        namespace: typing.Optional[builtins.str] = None,
        fields: typing.Optional[typing.Sequence[typing.Union["SecretFieldReference", typing.Dict[str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> ExternalSecret:
        '''Registers a Systems Manager parameter with the external secrets operator, enabling syncing from the Systems Manager parameter into Kubernetes.

        :param id: A name to be associated with the resource and used in resource naming. Must be unique within for each Systems Manager parameter within a Kubernetes namespace.
        :param parameter: The Systems Manager parameter to enable syncing for.
        :param namespace: The Kubernetes namespace where the synced secret should be created. Default: 'default'
        :param fields: A collection of field mappings that tells the external secrets operator the structure of the Kubernetes secret to create and which how fields in the Kubernetes secret should map to fields in the secret from the external secret provider. Default: The Kubernetes secret will mirror the fields from the secret in the external provider.
        :param name: The name of the Kubernetes secret that will be created, as it will appear from within the Kubernetes cluster. Default: A name will be auto-generated.

        :return: The external secret object that was created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ExternalSecretsOperator.register_ssm_parameter_secret)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
        options = NamespacedExternalSecretOptions(
            namespace=namespace, fields=fields, name=name
        )

        return typing.cast(ExternalSecret, jsii.invoke(self, "registerSsmParameterSecret", [id, parameter, options]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CHART_NAME")
    def CHART_NAME(cls) -> builtins.str:
        '''The name of the Helm chart to install from the Helm repository.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CHART_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CHART_REPOSITORY")
    def CHART_REPOSITORY(cls) -> builtins.str:
        '''The URL of the Helm repository that hostys the Helm charts used to install the externalk secrets operator service.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CHART_REPOSITORY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_NAMESPACE")
    def DEFAULT_NAMESPACE(cls) -> builtins.str:
        '''The default Kubernetes namespace where the external secrets operator service should be installed and configured if no overriding input is provided.'''
        return typing.cast(builtins.str, jsii.sget(cls, "DEFAULT_NAMESPACE"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_eks.Cluster:
        '''The EKS cluster where the external secrets operator service should be installed and configured.

        :group: Inputs
        '''
        return typing.cast(aws_cdk.aws_eks.Cluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="helmChart")
    def helm_chart(self) -> aws_cdk.aws_eks.HelmChart:
        '''The Helm chart the manages the installation and configuration of the external secrets operator service.

        :group: Resources
        '''
        return typing.cast(aws_cdk.aws_eks.HelmChart, jsii.get(self, "helmChart"))

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        '''The Kubernetes namespace where the external secrets operator service should be installed and configured.

        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @builtins.property
    @jsii.member(jsii_name="createNamespace")
    def create_namespace(self) -> typing.Optional[builtins.bool]:
        '''Determines the behavior when the service is deployed to a namespace that doesn't already exist on the EKS cluster.

        When this flag is ``true`` and the namespace doesn't exist, the namespace
        will be created automatically.

        When this flag is ``false`` and the namespace doesn't exist, an error will
        occur and resource creation will fail.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "createNamespace"))


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.ExternalSecretsOperatorProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "cluster": "cluster",
        "create_namespace": "createNamespace",
        "namespace": "namespace",
    },
)
class ExternalSecretsOperatorProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        cluster: aws_cdk.aws_eks.Cluster,
        create_namespace: typing.Optional[builtins.bool] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for the ExternalSecretsOperator resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param cluster: The EKS cluster where the external secrets operator should be installed.
        :param create_namespace: Determines the behavior when the service is deployed to a namespace that doesn't already exist on the EKS cluster. When this flag is ``true`` and the namespace doesn't exist, the namespace will be created automatically. When this flag is ``false`` and the namespace doesn't exist, an error will occur and resource creation will fail. Default: true
        :param namespace: The Kubernetes namespace where the external secrets operator service should be installed and configured. Default: {@link ExternalSecretsOperator.DEFAULT_NAMESPACE}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ExternalSecretsOperatorProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument create_namespace", value=create_namespace, expected_type=type_hints["create_namespace"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if create_namespace is not None:
            self._values["create_namespace"] = create_namespace
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster(self) -> aws_cdk.aws_eks.Cluster:
        '''The EKS cluster where the external secrets operator should be installed.'''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_eks.Cluster, result)

    @builtins.property
    def create_namespace(self) -> typing.Optional[builtins.bool]:
        '''Determines the behavior when the service is deployed to a namespace that doesn't already exist on the EKS cluster.

        When this flag is ``true`` and the namespace doesn't exist, the namespace
        will be created automatically.

        When this flag is ``false`` and the namespace doesn't exist, an error will
        occur and resource creation will fail.

        :default: true
        '''
        result = self._values.get("create_namespace")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The Kubernetes namespace where the external secrets operator service should be installed and configured.

        :default: {@link ExternalSecretsOperator.DEFAULT_NAMESPACE}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalSecretsOperatorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FargateLogger(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FargateLogger",
):
    '''Creates a ConfigMap that configures logging for containers running in EKS on Fargate.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster: aws_cdk.aws_eks.ICluster,
        fargate_profiles: typing.Optional[typing.Sequence[aws_cdk.aws_eks.FargateProfile]] = None,
        filters: typing.Optional[typing.Sequence["IFluentBitFilterPlugin"]] = None,
        log_group: typing.Optional[aws_cdk.aws_logs.ILogGroup] = None,
        outputs: typing.Optional[typing.Sequence["IFluentBitOutputPlugin"]] = None,
        parsers: typing.Optional[typing.Sequence["IFluentBitParserPlugin"]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the FargateLogger class.

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the resource and used in resource naming. Must be unique within the context of 'scope'.
        :param cluster: The EKS Cluster to configure Fargate logging for.
        :param fargate_profiles: A default list of Fargate profiles that should have permissions configured. Alternatively profiles can be added at any time by calling ``addProfile``.
        :param filters: The filters that should be applied to logs being processed.
        :param log_group: The CloudWatch log group where Farget container logs will be sent.
        :param outputs: The output destinations where logs should be written.
        :param parsers: The parsers to be used when reading log files.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FargateLogger.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FargateLoggerProps(
            cluster=cluster,
            fargate_profiles=fargate_profiles,
            filters=filters,
            log_group=log_group,
            outputs=outputs,
            parsers=parsers,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addFargateProfile")
    def add_fargate_profile(
        self,
        profile: aws_cdk.aws_eks.FargateProfile,
    ) -> "FargateLogger":
        '''
        :param profile: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FargateLogger.add_fargate_profile)
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
        return typing.cast("FargateLogger", jsii.invoke(self, "addFargateProfile", [profile]))

    @jsii.member(jsii_name="addFilter")
    def add_filter(self, filter: "IFluentBitFilterPlugin") -> "FargateLogger":
        '''
        :param filter: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FargateLogger.add_filter)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        return typing.cast("FargateLogger", jsii.invoke(self, "addFilter", [filter]))

    @jsii.member(jsii_name="addOutput")
    def add_output(self, output: "IFluentBitOutputPlugin") -> "FargateLogger":
        '''
        :param output: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FargateLogger.add_output)
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
        return typing.cast("FargateLogger", jsii.invoke(self, "addOutput", [output]))

    @jsii.member(jsii_name="addParser")
    def add_parser(self, parser: "IFluentBitParserPlugin") -> "FargateLogger":
        '''
        :param parser: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FargateLogger.add_parser)
            check_type(argname="argument parser", value=parser, expected_type=type_hints["parser"])
        return typing.cast("FargateLogger", jsii.invoke(self, "addParser", [parser]))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_eks.ICluster:
        '''The EKS cluster where Fargate logging is being configured.

        :group: Inputs
        '''
        return typing.cast(aws_cdk.aws_eks.ICluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="filters")
    def filters(self) -> typing.List["IFluentBitFilterPlugin"]:
        '''Collection of Fluent Bit filter plugins being configured for logging.

        :group: Inputs
        '''
        return typing.cast(typing.List["IFluentBitFilterPlugin"], jsii.get(self, "filters"))

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> aws_cdk.aws_eks.KubernetesManifest:
        '''The Kubernetes manifest that creates the ConfigMap that Fargate uses to configure logging.

        :group: Resources
        '''
        return typing.cast(aws_cdk.aws_eks.KubernetesManifest, jsii.get(self, "manifest"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> typing.List["IFluentBitOutputPlugin"]:
        '''Collection of Fluent Bit output plugins being configured for logging.

        :group: Inputs
        '''
        return typing.cast(typing.List["IFluentBitOutputPlugin"], jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="parsers")
    def parsers(self) -> typing.List["IFluentBitParserPlugin"]:
        '''Collection of Fluent Bit parser plugins being configured for logging.

        :group: Inputs
        '''
        return typing.cast(typing.List["IFluentBitParserPlugin"], jsii.get(self, "parsers"))


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FargateLoggerOptions",
    jsii_struct_bases=[],
    name_mapping={
        "fargate_profiles": "fargateProfiles",
        "filters": "filters",
        "log_group": "logGroup",
        "outputs": "outputs",
        "parsers": "parsers",
    },
)
class FargateLoggerOptions:
    def __init__(
        self,
        *,
        fargate_profiles: typing.Optional[typing.Sequence[aws_cdk.aws_eks.FargateProfile]] = None,
        filters: typing.Optional[typing.Sequence["IFluentBitFilterPlugin"]] = None,
        log_group: typing.Optional[aws_cdk.aws_logs.ILogGroup] = None,
        outputs: typing.Optional[typing.Sequence["IFluentBitOutputPlugin"]] = None,
        parsers: typing.Optional[typing.Sequence["IFluentBitParserPlugin"]] = None,
    ) -> None:
        '''Optional configuration for the FargateLogger resource.

        :param fargate_profiles: A default list of Fargate profiles that should have permissions configured. Alternatively profiles can be added at any time by calling ``addProfile``.
        :param filters: The filters that should be applied to logs being processed.
        :param log_group: The CloudWatch log group where Farget container logs will be sent.
        :param outputs: The output destinations where logs should be written.
        :param parsers: The parsers to be used when reading log files.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FargateLoggerOptions.__init__)
            check_type(argname="argument fargate_profiles", value=fargate_profiles, expected_type=type_hints["fargate_profiles"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument outputs", value=outputs, expected_type=type_hints["outputs"])
            check_type(argname="argument parsers", value=parsers, expected_type=type_hints["parsers"])
        self._values: typing.Dict[str, typing.Any] = {}
        if fargate_profiles is not None:
            self._values["fargate_profiles"] = fargate_profiles
        if filters is not None:
            self._values["filters"] = filters
        if log_group is not None:
            self._values["log_group"] = log_group
        if outputs is not None:
            self._values["outputs"] = outputs
        if parsers is not None:
            self._values["parsers"] = parsers

    @builtins.property
    def fargate_profiles(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_eks.FargateProfile]]:
        '''A default list of Fargate profiles that should have permissions configured.

        Alternatively profiles can be added at any time by calling
        ``addProfile``.
        '''
        result = self._values.get("fargate_profiles")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_eks.FargateProfile]], result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List["IFluentBitFilterPlugin"]]:
        '''The filters that should be applied to logs being processed.'''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List["IFluentBitFilterPlugin"]], result)

    @builtins.property
    def log_group(self) -> typing.Optional[aws_cdk.aws_logs.ILogGroup]:
        '''The CloudWatch log group where Farget container logs will be sent.'''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[aws_cdk.aws_logs.ILogGroup], result)

    @builtins.property
    def outputs(self) -> typing.Optional[typing.List["IFluentBitOutputPlugin"]]:
        '''The output destinations where logs should be written.'''
        result = self._values.get("outputs")
        return typing.cast(typing.Optional[typing.List["IFluentBitOutputPlugin"]], result)

    @builtins.property
    def parsers(self) -> typing.Optional[typing.List["IFluentBitParserPlugin"]]:
        '''The parsers to be used when reading log files.'''
        result = self._values.get("parsers")
        return typing.cast(typing.Optional[typing.List["IFluentBitParserPlugin"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FargateLoggerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FargateLoggerProps",
    jsii_struct_bases=[FargateLoggerOptions, aws_cdk.ResourceProps],
    name_mapping={
        "fargate_profiles": "fargateProfiles",
        "filters": "filters",
        "log_group": "logGroup",
        "outputs": "outputs",
        "parsers": "parsers",
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "cluster": "cluster",
    },
)
class FargateLoggerProps(FargateLoggerOptions, aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        fargate_profiles: typing.Optional[typing.Sequence[aws_cdk.aws_eks.FargateProfile]] = None,
        filters: typing.Optional[typing.Sequence["IFluentBitFilterPlugin"]] = None,
        log_group: typing.Optional[aws_cdk.aws_logs.ILogGroup] = None,
        outputs: typing.Optional[typing.Sequence["IFluentBitOutputPlugin"]] = None,
        parsers: typing.Optional[typing.Sequence["IFluentBitParserPlugin"]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        cluster: aws_cdk.aws_eks.ICluster,
    ) -> None:
        '''Required configuration for the Fargate logger resource.

        :param fargate_profiles: A default list of Fargate profiles that should have permissions configured. Alternatively profiles can be added at any time by calling ``addProfile``.
        :param filters: The filters that should be applied to logs being processed.
        :param log_group: The CloudWatch log group where Farget container logs will be sent.
        :param outputs: The output destinations where logs should be written.
        :param parsers: The parsers to be used when reading log files.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param cluster: The EKS Cluster to configure Fargate logging for.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FargateLoggerProps.__init__)
            check_type(argname="argument fargate_profiles", value=fargate_profiles, expected_type=type_hints["fargate_profiles"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument outputs", value=outputs, expected_type=type_hints["outputs"])
            check_type(argname="argument parsers", value=parsers, expected_type=type_hints["parsers"])
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
        }
        if fargate_profiles is not None:
            self._values["fargate_profiles"] = fargate_profiles
        if filters is not None:
            self._values["filters"] = filters
        if log_group is not None:
            self._values["log_group"] = log_group
        if outputs is not None:
            self._values["outputs"] = outputs
        if parsers is not None:
            self._values["parsers"] = parsers
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def fargate_profiles(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_eks.FargateProfile]]:
        '''A default list of Fargate profiles that should have permissions configured.

        Alternatively profiles can be added at any time by calling
        ``addProfile``.
        '''
        result = self._values.get("fargate_profiles")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_eks.FargateProfile]], result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List["IFluentBitFilterPlugin"]]:
        '''The filters that should be applied to logs being processed.'''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List["IFluentBitFilterPlugin"]], result)

    @builtins.property
    def log_group(self) -> typing.Optional[aws_cdk.aws_logs.ILogGroup]:
        '''The CloudWatch log group where Farget container logs will be sent.'''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[aws_cdk.aws_logs.ILogGroup], result)

    @builtins.property
    def outputs(self) -> typing.Optional[typing.List["IFluentBitOutputPlugin"]]:
        '''The output destinations where logs should be written.'''
        result = self._values.get("outputs")
        return typing.cast(typing.Optional[typing.List["IFluentBitOutputPlugin"]], result)

    @builtins.property
    def parsers(self) -> typing.Optional[typing.List["IFluentBitParserPlugin"]]:
        '''The parsers to be used when reading log files.'''
        result = self._values.get("parsers")
        return typing.cast(typing.Optional[typing.List["IFluentBitParserPlugin"]], result)

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster(self) -> aws_cdk.aws_eks.ICluster:
        '''The EKS Cluster to configure Fargate logging for.'''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_eks.ICluster, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FargateLoggerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FluentBitFilter(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitFilter",
):
    '''Standard filter options which can be applied to Fluent Bit to control the output and formatting of logs.

    Filters change the structure of log records by doing things like adding
    metadata to a record, restructuring a record, or adding and removing fields.
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="appendFields")
    @builtins.classmethod
    def append_fields(
        cls,
        match: "FluentBitMatch",
        *records: AppendedRecord,
    ) -> "IFluentBitFilterPlugin":
        '''Creates a filter that adds fields to a record that matches the given pattern.

        :param match: A pattern filtering to which records the filter should be applied.
        :param records: The fields to be added to matched records.

        :return:

        A filter object that can be applied to the Fluent Bit
        configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitFilter.append_fields)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument records", value=records, expected_type=typing.Tuple[type_hints["records"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IFluentBitFilterPlugin", jsii.sinvoke(cls, "appendFields", [match, *records]))

    @jsii.member(jsii_name="blacklistFields")
    @builtins.classmethod
    def blacklist_fields(
        cls,
        match: "FluentBitMatch",
        *fields: builtins.str,
    ) -> "IFluentBitFilterPlugin":
        '''Creates a filter that removes a set of fields from any records that match a given pattern.

        :param match: A pattern filtering to which records the filter should be applied.
        :param fields: The fields which should be removed from the record if they are present.

        :return:

        A filter object that can be applied to the Fluent Bit
        configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitFilter.blacklist_fields)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument fields", value=fields, expected_type=typing.Tuple[type_hints["fields"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IFluentBitFilterPlugin", jsii.sinvoke(cls, "blacklistFields", [match, *fields]))

    @jsii.member(jsii_name="grep")
    @builtins.classmethod
    def grep(
        cls,
        match: "FluentBitMatch",
        *,
        key: builtins.str,
        regex: builtins.str,
        exclude: typing.Optional[builtins.bool] = None,
    ) -> "IFluentBitFilterPlugin":
        '''Filters log entries based on a pattern.

        Log entries can be removed and
        not forwarded based on whether they match or do not match the given
        pattern.

        :param match: A pattern filtering to which records the filter should be applied.
        :param key: The key of the fields which you want to filter using the regex.
        :param regex: The regular expression to apply to the specified field.
        :param exclude: Whether the matched expression should exclude or include records from being output. When this is true, only records that match the given expression will be output. When this is false, only records that do not match the given expression will be output. Default: false

        :return:

        A filter object that can be applied to the Fluent Bit
        configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitFilter.grep)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
        pattern = FluentBitGrepRegex(key=key, regex=regex, exclude=exclude)

        return typing.cast("IFluentBitFilterPlugin", jsii.sinvoke(cls, "grep", [match, pattern]))

    @jsii.member(jsii_name="kubernetes")
    @builtins.classmethod
    def kubernetes(cls, match: "FluentBitMatch") -> "IFluentBitFilterPlugin":
        '''Adds Kubernetes metadata to output records including pod information, labels, etc..

        :param match: A pattern filtering to which records the filter should be applied.

        :return:

        A filter object that can be applied to the Fluent Bit
        configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitFilter.kubernetes)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
        return typing.cast("IFluentBitFilterPlugin", jsii.sinvoke(cls, "kubernetes", [match]))

    @jsii.member(jsii_name="lift")
    @builtins.classmethod
    def lift(
        cls,
        match: "FluentBitMatch",
        nested_under: builtins.str,
    ) -> "IFluentBitFilterPlugin":
        '''Lifts nested fields in a record up to their parent object.

        :param match: A pattern filtering to which records the filter should be applied.
        :param nested_under: The record object under which you want to lift fields.

        :return:

        A filter object that can be applied to the Fluent Bit
        configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitFilter.lift)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument nested_under", value=nested_under, expected_type=type_hints["nested_under"])
        return typing.cast("IFluentBitFilterPlugin", jsii.sinvoke(cls, "lift", [match, nested_under]))

    @jsii.member(jsii_name="modify")
    @builtins.classmethod
    def modify(
        cls,
        match: "FluentBitMatch",
        *operations: "ModifyOperation",
    ) -> "IFluentBitFilterPlugin":
        '''Applies various transformations to matched records including adding, removing, copying, and renaming fields.

        :param match: A pattern filtering to which records the filter should be applied.
        :param operations: The operations to apply to the matched records.

        :return:

        A filter object that can be applied to the Fluent Bit
        configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitFilter.modify)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument operations", value=operations, expected_type=typing.Tuple[type_hints["operations"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IFluentBitFilterPlugin", jsii.sinvoke(cls, "modify", [match, *operations]))

    @jsii.member(jsii_name="nest")
    @builtins.classmethod
    def nest(
        cls,
        match: "FluentBitMatch",
        nest_under: builtins.str,
        *fields: builtins.str,
    ) -> "IFluentBitFilterPlugin":
        '''Nests a set of fields in a record under into a specified object.

        :param match: A pattern filtering to which records the filter should be applied.
        :param nest_under: The record object under which you want to nest matched fields.
        :param fields: The fields to nest under the specified object.

        :return:

        A filter object that can be applied to the Fluent Bit
        configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitFilter.nest)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument nest_under", value=nest_under, expected_type=type_hints["nest_under"])
            check_type(argname="argument fields", value=fields, expected_type=typing.Tuple[type_hints["fields"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IFluentBitFilterPlugin", jsii.sinvoke(cls, "nest", [match, nest_under, *fields]))

    @jsii.member(jsii_name="parser")
    @builtins.classmethod
    def parser(
        cls,
        match: "FluentBitMatch",
        key: builtins.str,
        *parsers: "IFluentBitParserPlugin",
    ) -> "IFluentBitFilterPlugin":
        '''Applies a set of parsers to matched records.

        The parser is used to read the input record and set structured fields in
        the output.

        :param match: A pattern filtering to which records the filter should be applied.
        :param key: The key of the field to be parsed.
        :param parsers: The parser plugins to use to read matched records.

        :return:

        A filter object that can be applied to the Fluent Bit
        configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitFilter.parser)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument parsers", value=parsers, expected_type=typing.Tuple[type_hints["parsers"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IFluentBitFilterPlugin", jsii.sinvoke(cls, "parser", [match, key, *parsers]))

    @jsii.member(jsii_name="rewriteTag")
    @builtins.classmethod
    def rewrite_tag(
        cls,
        match: "FluentBitMatch",
        *rules: "RewriteTagRule",
    ) -> "IFluentBitFilterPlugin":
        '''Allows modification of tags set by the input configuration to affect the routing of when records are output.

        :param match: A pattern filtering to which records the filter should be applied.
        :param rules: The rules that define the matching criteria of format of the tag for the matching record.

        :return:

        A filter object that can be applied to the Fluent Bit
        configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitFilter.rewrite_tag)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument rules", value=rules, expected_type=typing.Tuple[type_hints["rules"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IFluentBitFilterPlugin", jsii.sinvoke(cls, "rewriteTag", [match, *rules]))

    @jsii.member(jsii_name="throttle")
    @builtins.classmethod
    def throttle(
        cls,
        match: "FluentBitMatch",
        interval: aws_cdk.Duration,
        rate: jsii.Number,
        window: jsii.Number,
    ) -> "IFluentBitFilterPlugin":
        '''Sets an average rate of messages that are allowed to be output over a configured period of time.

        When the rate of messages surpasses the configured limits messages will
        be dropped.

        :param match: A pattern filtering to which records the filter should be applied.
        :param interval: The interval of time over rate should be sampled to calculate an average.
        :param rate: The average amount of messages over a given period.
        :param window: Amount of intervals to calculate average over.

        :return:

        A filter object that can be applied to the Fluent Bit
        configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitFilter.throttle)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument rate", value=rate, expected_type=type_hints["rate"])
            check_type(argname="argument window", value=window, expected_type=type_hints["window"])
        return typing.cast("IFluentBitFilterPlugin", jsii.sinvoke(cls, "throttle", [match, interval, rate, window]))

    @jsii.member(jsii_name="whitelistFields")
    @builtins.classmethod
    def whitelist_fields(
        cls,
        match: "FluentBitMatch",
        *fields: builtins.str,
    ) -> "IFluentBitFilterPlugin":
        '''Creates a filter that removes all fields in a record that are not approved.

        :param match: A pattern filtering to which records the filter should be applied.
        :param fields: The fields which are allowed to appear in the output record.

        :return:

        A filter object that can be applied to the Fluent Bit
        configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitFilter.whitelist_fields)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument fields", value=fields, expected_type=typing.Tuple[type_hints["fields"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IFluentBitFilterPlugin", jsii.sinvoke(cls, "whitelistFields", [match, *fields]))


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitFilterPluginCommonOptions",
    jsii_struct_bases=[],
    name_mapping={"match": "match"},
)
class FluentBitFilterPluginCommonOptions:
    def __init__(self, *, match: typing.Optional["FluentBitMatch"] = None) -> None:
        '''Configuration options that apply to all Fluent Bit output plugins.

        :param match: The pattern to match for records that this output should apply to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitFilterPluginCommonOptions.__init__)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
        self._values: typing.Dict[str, typing.Any] = {}
        if match is not None:
            self._values["match"] = match

    @builtins.property
    def match(self) -> typing.Optional["FluentBitMatch"]:
        '''The pattern to match for records that this output should apply to.'''
        result = self._values.get("match")
        return typing.cast(typing.Optional["FluentBitMatch"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitFilterPluginCommonOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitGrepFilterOptions",
    jsii_struct_bases=[FluentBitFilterPluginCommonOptions],
    name_mapping={"match": "match", "pattern": "pattern"},
)
class FluentBitGrepFilterOptions(FluentBitFilterPluginCommonOptions):
    def __init__(
        self,
        *,
        match: typing.Optional["FluentBitMatch"] = None,
        pattern: typing.Union["FluentBitGrepRegex", typing.Dict[str, typing.Any]],
    ) -> None:
        '''Options for configuring the Grep Fluent Bit filter plugin.

        :param match: The pattern to match for records that this output should apply to.
        :param pattern: The pattern to use for filtering records processed by the plugin.

        :see: `Grep Plugin Documention <https://docs.fluentbit.io/manual/pipeline/filters/grep>`_
        '''
        if isinstance(pattern, dict):
            pattern = FluentBitGrepRegex(**pattern)
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitGrepFilterOptions.__init__)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        self._values: typing.Dict[str, typing.Any] = {
            "pattern": pattern,
        }
        if match is not None:
            self._values["match"] = match

    @builtins.property
    def match(self) -> typing.Optional["FluentBitMatch"]:
        '''The pattern to match for records that this output should apply to.'''
        result = self._values.get("match")
        return typing.cast(typing.Optional["FluentBitMatch"], result)

    @builtins.property
    def pattern(self) -> "FluentBitGrepRegex":
        '''The pattern to use for filtering records processed by the plugin.'''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast("FluentBitGrepRegex", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitGrepFilterOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitGrepRegex",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "regex": "regex", "exclude": "exclude"},
)
class FluentBitGrepRegex:
    def __init__(
        self,
        *,
        key: builtins.str,
        regex: builtins.str,
        exclude: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Configures a pattern to match against a Fluent Bit record.

        :param key: The key of the fields which you want to filter using the regex.
        :param regex: The regular expression to apply to the specified field.
        :param exclude: Whether the matched expression should exclude or include records from being output. When this is true, only records that match the given expression will be output. When this is false, only records that do not match the given expression will be output. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitGrepRegex.__init__)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
        self._values: typing.Dict[str, typing.Any] = {
            "key": key,
            "regex": regex,
        }
        if exclude is not None:
            self._values["exclude"] = exclude

    @builtins.property
    def key(self) -> builtins.str:
        '''The key of the fields which you want to filter using the regex.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def regex(self) -> builtins.str:
        '''The regular expression to apply to the specified field.'''
        result = self._values.get("regex")
        assert result is not None, "Required property 'regex' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exclude(self) -> typing.Optional[builtins.bool]:
        '''Whether the matched expression should exclude or include records from being output.

        When this is true, only records that match the given expression will be
        output.

        When this is false, only records that do not match the given expression
        will be output.

        :default: false
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitGrepRegex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitKubernetesFilterOptions",
    jsii_struct_bases=[FluentBitFilterPluginCommonOptions],
    name_mapping={
        "match": "match",
        "annotations": "annotations",
        "buffer_size": "bufferSize",
        "cache_use_docker_id": "cacheUseDockerId",
        "dns_retries": "dnsRetries",
        "dns_wait_time": "dnsWaitTime",
        "dummy_meta": "dummyMeta",
        "k8s_logging_exclude": "k8sLoggingExclude",
        "k8s_logging_parser": "k8sLoggingParser",
        "keep_log": "keepLog",
        "kube_ca_file": "kubeCaFile",
        "kube_ca_path": "kubeCaPath",
        "kubelet_host": "kubeletHost",
        "kubelet_port": "kubeletPort",
        "kube_meta_cache_ttl": "kubeMetaCacheTtl",
        "kube_meta_preload_cache_dir": "kubeMetaPreloadCacheDir",
        "kube_tag_prefix": "kubeTagPrefix",
        "kube_token_command": "kubeTokenCommand",
        "kube_token_file": "kubeTokenFile",
        "kube_token_ttl": "kubeTokenTtl",
        "kube_url": "kubeUrl",
        "labels": "labels",
        "merge_log": "mergeLog",
        "merge_log_key": "mergeLogKey",
        "merge_log_trim": "mergeLogTrim",
        "merge_parser": "mergeParser",
        "regex_parser": "regexParser",
        "tls_debug": "tlsDebug",
        "tls_verify": "tlsVerify",
        "use_journal": "useJournal",
        "use_kubelet": "useKubelet",
    },
)
class FluentBitKubernetesFilterOptions(FluentBitFilterPluginCommonOptions):
    def __init__(
        self,
        *,
        match: typing.Optional["FluentBitMatch"] = None,
        annotations: typing.Optional[builtins.bool] = None,
        buffer_size: typing.Optional[_DataSize_d20aaece] = None,
        cache_use_docker_id: typing.Optional[builtins.bool] = None,
        dns_retries: typing.Optional[jsii.Number] = None,
        dns_wait_time: typing.Optional[aws_cdk.Duration] = None,
        dummy_meta: typing.Optional[builtins.bool] = None,
        k8s_logging_exclude: typing.Optional[builtins.bool] = None,
        k8s_logging_parser: typing.Optional[builtins.bool] = None,
        keep_log: typing.Optional[builtins.bool] = None,
        kube_ca_file: typing.Optional[builtins.str] = None,
        kube_ca_path: typing.Optional[builtins.str] = None,
        kubelet_host: typing.Optional[builtins.str] = None,
        kubelet_port: typing.Optional[jsii.Number] = None,
        kube_meta_cache_ttl: typing.Optional[aws_cdk.Duration] = None,
        kube_meta_preload_cache_dir: typing.Optional[builtins.str] = None,
        kube_tag_prefix: typing.Optional[builtins.str] = None,
        kube_token_command: typing.Optional[builtins.str] = None,
        kube_token_file: typing.Optional[builtins.str] = None,
        kube_token_ttl: typing.Optional[aws_cdk.Duration] = None,
        kube_url: typing.Optional[builtins.str] = None,
        labels: typing.Optional[builtins.bool] = None,
        merge_log: typing.Optional[builtins.bool] = None,
        merge_log_key: typing.Optional[builtins.str] = None,
        merge_log_trim: typing.Optional[builtins.bool] = None,
        merge_parser: typing.Optional[builtins.str] = None,
        regex_parser: typing.Optional[builtins.str] = None,
        tls_debug: typing.Optional[jsii.Number] = None,
        tls_verify: typing.Optional[builtins.bool] = None,
        use_journal: typing.Optional[builtins.bool] = None,
        use_kubelet: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Options for configuring the Kubernetes Fluent Bit filter plugin.

        :param match: The pattern to match for records that this output should apply to.
        :param annotations: Include Kubernetes resource annotations in the extra metadata. Default: true
        :param buffer_size: Set the buffer size for HTTP client when reading responses from Kubernetes API server. A value of 0 results in no limit, and the buffer will expand as-needed. Note that if pod specifications exceed the buffer limit, the API response will be discarded when retrieving metadata, and some kubernetes metadata will fail to be injected to the logs. Default: 32k
        :param cache_use_docker_id: When enabled, metadata will be fetched from K8s when docker_id is changed. Default: false
        :param dns_retries: DNS lookup retries N times until the network starts working. Default: 6
        :param dns_wait_time: DNS lookup interval between network status checks. Default: 30 seconds
        :param dummy_meta: If set, use dummy-meta data (for test/dev purposes). Default: false
        :param k8s_logging_exclude: Allow Kubernetes Pods to exclude their logs from the log processor. Default: false
        :param k8s_logging_parser: Allow Kubernetes Pods to suggest a pre-defined Parser. Default: false
        :param keep_log: When ``keepLog`` is disabled, the log field is removed from the incoming message once it has been successfully merged (``mergeLog`` must be enabled as well). Default: true
        :param kube_ca_file: CA certificate file. Default: '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
        :param kube_ca_path: Absolute path to scan for certificate files.
        :param kubelet_host: Kubelet host using for HTTP request, this only works when ``useKubelet`` is enabled.
        :param kubelet_port: Kubelet port using for HTTP request, this only works when ``useKubelet`` is enabled. Default: 10250
        :param kube_meta_cache_ttl: Configurable TTL for K8s cached metadata. By default, it is set to 0 which means TTL for cache entries is disabled and cache entries are evicted at random when capacity is reached. In order to enable this option, you should set the number to a time interval. Default: 0
        :param kube_meta_preload_cache_dir: If set, Kubernetes meta-data can be cached/pre-loaded from files in JSON format in this directory, named as namespace-pod.meta.
        :param kube_tag_prefix: When the source records comes from Tail input plugin, this option allows to specify what's the prefix used in Tail configuration. Default: 'kube.var.log.containers.'
        :param kube_token_command: Command to get Kubernetes authorization token. If you want to manually choose a command to get it, you can set the command here. For example, run running the following to get the token using aws-cli:: aws-iam-authenticator -i your-cluster-name token --token-only This option is currently Linux-only.
        :param kube_token_file: Token file. Default: '/var/run/secrets/kubernetes.io/serviceaccount/token'
        :param kube_token_ttl: Configurable 'time to live' for the K8s token. After this time, the token is reloaded from ``kubeTokenFile`` or the ``kubeTokenCommand``. Default: 10 minutes
        :param kube_url: API Server end-point. Default: 'https://kubernetes.default.svc/'
        :param labels: Include Kubernetes resource labels in the extra metadata. Default: true
        :param merge_log: When enabled, it checks if the ``log`` field content is a JSON string map, if so, it append the map fields as part of the log structure. Default: false
        :param merge_log_key: When ``mergeLog`` is enabled, the filter tries to assume the ``log`` field from the incoming message is a JSON string message and make a structured representation of it at the same level of the ``log`` field in the map. Now if ``mergeLogKey`` is set (a string name), all the new structured fields taken from the original ``log`` content are inserted under the new key.
        :param merge_log_trim: When Merge_Log is enabled, trim (remove possible \\n or \\r) field values. Default: true
        :param merge_parser: Optional parser name to specify how to parse the data contained in the log key. Recommended use is for developers or testing only.
        :param regex_parser: Set an alternative Parser to process record Tag and extract pod_name, namespace_name, container_name and docker_id. The parser must be registered in a parsers file.
        :param tls_debug: Debug level between 0 (nothing) and 4 (every detail). Default: -1
        :param tls_verify: When enabled, turns on certificate validation when connecting to the Kubernetes API server. Default: true
        :param use_journal: When enabled, the filter reads logs coming in Journald format. Default: false
        :param use_kubelet: This is an optional feature flag to get metadata information from kubelet instead of calling Kube Server API to enhance the log. Default: false

        :see: `Kubernetes Plugin Documention <https://docs.fluentbit.io/manual/pipeline/filters/kubernetes>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitKubernetesFilterOptions.__init__)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument buffer_size", value=buffer_size, expected_type=type_hints["buffer_size"])
            check_type(argname="argument cache_use_docker_id", value=cache_use_docker_id, expected_type=type_hints["cache_use_docker_id"])
            check_type(argname="argument dns_retries", value=dns_retries, expected_type=type_hints["dns_retries"])
            check_type(argname="argument dns_wait_time", value=dns_wait_time, expected_type=type_hints["dns_wait_time"])
            check_type(argname="argument dummy_meta", value=dummy_meta, expected_type=type_hints["dummy_meta"])
            check_type(argname="argument k8s_logging_exclude", value=k8s_logging_exclude, expected_type=type_hints["k8s_logging_exclude"])
            check_type(argname="argument k8s_logging_parser", value=k8s_logging_parser, expected_type=type_hints["k8s_logging_parser"])
            check_type(argname="argument keep_log", value=keep_log, expected_type=type_hints["keep_log"])
            check_type(argname="argument kube_ca_file", value=kube_ca_file, expected_type=type_hints["kube_ca_file"])
            check_type(argname="argument kube_ca_path", value=kube_ca_path, expected_type=type_hints["kube_ca_path"])
            check_type(argname="argument kubelet_host", value=kubelet_host, expected_type=type_hints["kubelet_host"])
            check_type(argname="argument kubelet_port", value=kubelet_port, expected_type=type_hints["kubelet_port"])
            check_type(argname="argument kube_meta_cache_ttl", value=kube_meta_cache_ttl, expected_type=type_hints["kube_meta_cache_ttl"])
            check_type(argname="argument kube_meta_preload_cache_dir", value=kube_meta_preload_cache_dir, expected_type=type_hints["kube_meta_preload_cache_dir"])
            check_type(argname="argument kube_tag_prefix", value=kube_tag_prefix, expected_type=type_hints["kube_tag_prefix"])
            check_type(argname="argument kube_token_command", value=kube_token_command, expected_type=type_hints["kube_token_command"])
            check_type(argname="argument kube_token_file", value=kube_token_file, expected_type=type_hints["kube_token_file"])
            check_type(argname="argument kube_token_ttl", value=kube_token_ttl, expected_type=type_hints["kube_token_ttl"])
            check_type(argname="argument kube_url", value=kube_url, expected_type=type_hints["kube_url"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument merge_log", value=merge_log, expected_type=type_hints["merge_log"])
            check_type(argname="argument merge_log_key", value=merge_log_key, expected_type=type_hints["merge_log_key"])
            check_type(argname="argument merge_log_trim", value=merge_log_trim, expected_type=type_hints["merge_log_trim"])
            check_type(argname="argument merge_parser", value=merge_parser, expected_type=type_hints["merge_parser"])
            check_type(argname="argument regex_parser", value=regex_parser, expected_type=type_hints["regex_parser"])
            check_type(argname="argument tls_debug", value=tls_debug, expected_type=type_hints["tls_debug"])
            check_type(argname="argument tls_verify", value=tls_verify, expected_type=type_hints["tls_verify"])
            check_type(argname="argument use_journal", value=use_journal, expected_type=type_hints["use_journal"])
            check_type(argname="argument use_kubelet", value=use_kubelet, expected_type=type_hints["use_kubelet"])
        self._values: typing.Dict[str, typing.Any] = {}
        if match is not None:
            self._values["match"] = match
        if annotations is not None:
            self._values["annotations"] = annotations
        if buffer_size is not None:
            self._values["buffer_size"] = buffer_size
        if cache_use_docker_id is not None:
            self._values["cache_use_docker_id"] = cache_use_docker_id
        if dns_retries is not None:
            self._values["dns_retries"] = dns_retries
        if dns_wait_time is not None:
            self._values["dns_wait_time"] = dns_wait_time
        if dummy_meta is not None:
            self._values["dummy_meta"] = dummy_meta
        if k8s_logging_exclude is not None:
            self._values["k8s_logging_exclude"] = k8s_logging_exclude
        if k8s_logging_parser is not None:
            self._values["k8s_logging_parser"] = k8s_logging_parser
        if keep_log is not None:
            self._values["keep_log"] = keep_log
        if kube_ca_file is not None:
            self._values["kube_ca_file"] = kube_ca_file
        if kube_ca_path is not None:
            self._values["kube_ca_path"] = kube_ca_path
        if kubelet_host is not None:
            self._values["kubelet_host"] = kubelet_host
        if kubelet_port is not None:
            self._values["kubelet_port"] = kubelet_port
        if kube_meta_cache_ttl is not None:
            self._values["kube_meta_cache_ttl"] = kube_meta_cache_ttl
        if kube_meta_preload_cache_dir is not None:
            self._values["kube_meta_preload_cache_dir"] = kube_meta_preload_cache_dir
        if kube_tag_prefix is not None:
            self._values["kube_tag_prefix"] = kube_tag_prefix
        if kube_token_command is not None:
            self._values["kube_token_command"] = kube_token_command
        if kube_token_file is not None:
            self._values["kube_token_file"] = kube_token_file
        if kube_token_ttl is not None:
            self._values["kube_token_ttl"] = kube_token_ttl
        if kube_url is not None:
            self._values["kube_url"] = kube_url
        if labels is not None:
            self._values["labels"] = labels
        if merge_log is not None:
            self._values["merge_log"] = merge_log
        if merge_log_key is not None:
            self._values["merge_log_key"] = merge_log_key
        if merge_log_trim is not None:
            self._values["merge_log_trim"] = merge_log_trim
        if merge_parser is not None:
            self._values["merge_parser"] = merge_parser
        if regex_parser is not None:
            self._values["regex_parser"] = regex_parser
        if tls_debug is not None:
            self._values["tls_debug"] = tls_debug
        if tls_verify is not None:
            self._values["tls_verify"] = tls_verify
        if use_journal is not None:
            self._values["use_journal"] = use_journal
        if use_kubelet is not None:
            self._values["use_kubelet"] = use_kubelet

    @builtins.property
    def match(self) -> typing.Optional["FluentBitMatch"]:
        '''The pattern to match for records that this output should apply to.'''
        result = self._values.get("match")
        return typing.cast(typing.Optional["FluentBitMatch"], result)

    @builtins.property
    def annotations(self) -> typing.Optional[builtins.bool]:
        '''Include Kubernetes resource annotations in the extra metadata.

        :default: true
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def buffer_size(self) -> typing.Optional[_DataSize_d20aaece]:
        '''Set the buffer size for HTTP client when reading responses from Kubernetes API server.

        A value of 0 results in no limit, and the buffer will expand as-needed.

        Note that if pod specifications exceed the buffer limit, the API
        response will be discarded when retrieving metadata, and some kubernetes
        metadata will fail to be injected to the logs.

        :default: 32k
        '''
        result = self._values.get("buffer_size")
        return typing.cast(typing.Optional[_DataSize_d20aaece], result)

    @builtins.property
    def cache_use_docker_id(self) -> typing.Optional[builtins.bool]:
        '''When enabled, metadata will be fetched from K8s when docker_id is changed.

        :default: false
        '''
        result = self._values.get("cache_use_docker_id")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dns_retries(self) -> typing.Optional[jsii.Number]:
        '''DNS lookup retries N times until the network starts working.

        :default: 6
        '''
        result = self._values.get("dns_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dns_wait_time(self) -> typing.Optional[aws_cdk.Duration]:
        '''DNS lookup interval between network status checks.

        :default: 30 seconds
        '''
        result = self._values.get("dns_wait_time")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def dummy_meta(self) -> typing.Optional[builtins.bool]:
        '''If set, use dummy-meta data (for test/dev purposes).

        :default: false
        '''
        result = self._values.get("dummy_meta")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def k8s_logging_exclude(self) -> typing.Optional[builtins.bool]:
        '''Allow Kubernetes Pods to exclude their logs from the log processor.

        :default: false
        '''
        result = self._values.get("k8s_logging_exclude")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def k8s_logging_parser(self) -> typing.Optional[builtins.bool]:
        '''Allow Kubernetes Pods to suggest a pre-defined Parser.

        :default: false
        '''
        result = self._values.get("k8s_logging_parser")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def keep_log(self) -> typing.Optional[builtins.bool]:
        '''When ``keepLog`` is disabled, the log field is removed from the incoming message once it has been successfully merged (``mergeLog`` must be enabled as well).

        :default: true
        '''
        result = self._values.get("keep_log")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def kube_ca_file(self) -> typing.Optional[builtins.str]:
        '''CA certificate file.

        :default: '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
        '''
        result = self._values.get("kube_ca_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kube_ca_path(self) -> typing.Optional[builtins.str]:
        '''Absolute path to scan for certificate files.'''
        result = self._values.get("kube_ca_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kubelet_host(self) -> typing.Optional[builtins.str]:
        '''Kubelet host using for HTTP request, this only works when ``useKubelet`` is enabled.'''
        result = self._values.get("kubelet_host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kubelet_port(self) -> typing.Optional[jsii.Number]:
        '''Kubelet port using for HTTP request, this only works when ``useKubelet`` is enabled.

        :default: 10250
        '''
        result = self._values.get("kubelet_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kube_meta_cache_ttl(self) -> typing.Optional[aws_cdk.Duration]:
        '''Configurable TTL for K8s cached metadata.

        By default, it is set to 0 which means TTL for cache entries is disabled
        and cache entries are evicted at random when capacity is reached.

        In order to enable this option, you should set the number to a time
        interval.

        :default: 0
        '''
        result = self._values.get("kube_meta_cache_ttl")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def kube_meta_preload_cache_dir(self) -> typing.Optional[builtins.str]:
        '''If set, Kubernetes meta-data can be cached/pre-loaded from files in JSON format in this directory, named as namespace-pod.meta.'''
        result = self._values.get("kube_meta_preload_cache_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kube_tag_prefix(self) -> typing.Optional[builtins.str]:
        '''When the source records comes from Tail input plugin, this option allows to specify what's the prefix used in Tail configuration.

        :default: 'kube.var.log.containers.'
        '''
        result = self._values.get("kube_tag_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kube_token_command(self) -> typing.Optional[builtins.str]:
        '''Command to get Kubernetes authorization token.

        If you want to manually choose a command to get it, you can set the
        command here.

        For example, run running the following to get the token using aws-cli::

           aws-iam-authenticator -i your-cluster-name token --token-only

        This option is currently Linux-only.
        '''
        result = self._values.get("kube_token_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kube_token_file(self) -> typing.Optional[builtins.str]:
        '''Token file.

        :default: '/var/run/secrets/kubernetes.io/serviceaccount/token'
        '''
        result = self._values.get("kube_token_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kube_token_ttl(self) -> typing.Optional[aws_cdk.Duration]:
        '''Configurable 'time to live' for the K8s token.

        After this time, the token is reloaded from ``kubeTokenFile`` or the
        ``kubeTokenCommand``.

        :default: 10 minutes
        '''
        result = self._values.get("kube_token_ttl")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def kube_url(self) -> typing.Optional[builtins.str]:
        '''API Server end-point.

        :default: 'https://kubernetes.default.svc/'
        '''
        result = self._values.get("kube_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[builtins.bool]:
        '''Include Kubernetes resource labels in the extra metadata.

        :default: true
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def merge_log(self) -> typing.Optional[builtins.bool]:
        '''When enabled, it checks if the ``log`` field content is a JSON string map, if so, it append the map fields as part of the log structure.

        :default: false
        '''
        result = self._values.get("merge_log")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def merge_log_key(self) -> typing.Optional[builtins.str]:
        '''When ``mergeLog`` is enabled, the filter tries to assume the ``log`` field from the incoming message is a JSON string message and make a structured representation of it at the same level of the ``log`` field in the map.

        Now if ``mergeLogKey`` is set (a string name), all the new structured
        fields taken from the original ``log`` content are inserted under the new
        key.
        '''
        result = self._values.get("merge_log_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def merge_log_trim(self) -> typing.Optional[builtins.bool]:
        '''When Merge_Log is enabled, trim (remove possible \\n or \\r) field values.

        :default: true
        '''
        result = self._values.get("merge_log_trim")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def merge_parser(self) -> typing.Optional[builtins.str]:
        '''Optional parser name to specify how to parse the data contained in the log key.

        Recommended use is for developers or testing only.
        '''
        result = self._values.get("merge_parser")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regex_parser(self) -> typing.Optional[builtins.str]:
        '''Set an alternative Parser to process record Tag and extract pod_name, namespace_name, container_name and docker_id.

        The parser must be registered in a parsers file.

        :see: `Parsers File <https://github.com/fluent/fluent-bit/blob/master/conf/parsers.conf>`_
        '''
        result = self._values.get("regex_parser")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls_debug(self) -> typing.Optional[jsii.Number]:
        '''Debug level between 0 (nothing) and 4 (every detail).

        :default: -1
        '''
        result = self._values.get("tls_debug")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tls_verify(self) -> typing.Optional[builtins.bool]:
        '''When enabled, turns on certificate validation when connecting to the Kubernetes API server.

        :default: true
        '''
        result = self._values.get("tls_verify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def use_journal(self) -> typing.Optional[builtins.bool]:
        '''When enabled, the filter reads logs coming in Journald format.

        :default: false
        '''
        result = self._values.get("use_journal")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def use_kubelet(self) -> typing.Optional[builtins.bool]:
        '''This is an optional feature flag to get metadata information from kubelet instead of calling Kube Server API to enhance the log.

        :default: false

        :see: `Kube API heavy traffic issue for large cluster <https://docs.fluentbit.io/manual/pipeline/filters/kubernetes#optional-feature-using-kubelet-to-get-metadata>`_
        '''
        result = self._values.get("use_kubelet")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitKubernetesFilterOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FluentBitLogGroupOutput(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitLogGroupOutput",
):
    '''Represents valid log group output configuration options to be used by Fluent Bit when writing to CloudWatch Logs.'''

    @jsii.member(jsii_name="create")
    @builtins.classmethod
    def create(cls) -> "FluentBitLogGroupOutput":
        '''Sets a flag saying that a log group should be created automatically.

        Depending on the configuration of the plugin, this flag will either cause
        permissions to be granted for Fluent Bit to create the log group itself or
        the plugin CDK resource will create a Log Group and use that as the
        destination.

        :return:

        A FluentBitLogGroupOutput object representing the configured log
        group destination.
        '''
        return typing.cast("FluentBitLogGroupOutput", jsii.sinvoke(cls, "create", []))

    @jsii.member(jsii_name="fromLogGroup")
    @builtins.classmethod
    def from_log_group(
        cls,
        log_group: aws_cdk.aws_logs.ILogGroup,
    ) -> "FluentBitLogGroupOutput":
        '''Sets the destination log group to a LogGroup CDK resource.

        :param log_group: The log group where output records should be written.

        :return:

        A FluentBitLogGroupOutput object representing the configured log
        group destination.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitLogGroupOutput.from_log_group)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("FluentBitLogGroupOutput", jsii.sinvoke(cls, "fromLogGroup", [log_group]))

    @jsii.member(jsii_name="fromName")
    @builtins.classmethod
    def from_name(
        cls,
        name: builtins.str,
        create: typing.Optional[builtins.bool] = None,
    ) -> "FluentBitLogGroupOutput":
        '''Sets the destination for logs to the named log group.

        :param name: The name of the log group where output records should be written.
        :param create: -

        :return:

        A FluentBitLogGroupOutput object representing the configured log
        group destination.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitLogGroupOutput.from_name)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
        return typing.cast("FluentBitLogGroupOutput", jsii.sinvoke(cls, "fromName", [name, create]))

    @builtins.property
    @jsii.member(jsii_name="autoCreate")
    def auto_create(self) -> typing.Optional[builtins.bool]:
        '''Flag that determines whether or not a log group should be automatically created.'''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "autoCreate"))

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> typing.Optional[aws_cdk.aws_logs.ILogGroup]:
        '''A log group resource object to use as the destination.'''
        return typing.cast(typing.Optional[aws_cdk.aws_logs.ILogGroup], jsii.get(self, "logGroup"))

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''The name for the log group that should be used for output records.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupName"))


class FluentBitLogStreamOutput(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitLogStreamOutput",
):
    '''Represents valid log stream output configuration options to be used by Fluent Bit when writing to CloudWatch Logs.'''

    @jsii.member(jsii_name="fromLogStream")
    @builtins.classmethod
    def from_log_stream(
        cls,
        log_stream: aws_cdk.aws_logs.ILogStream,
    ) -> "FluentBitLogStreamOutput":
        '''Sets output to be a log stream resource object.

        :param log_stream: The log stream where records should be written.

        :return:

        A FluentBitLogStreamOutput object representing the configured
        log stream destination.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitLogStreamOutput.from_log_stream)
            check_type(argname="argument log_stream", value=log_stream, expected_type=type_hints["log_stream"])
        return typing.cast("FluentBitLogStreamOutput", jsii.sinvoke(cls, "fromLogStream", [log_stream]))

    @jsii.member(jsii_name="fromName")
    @builtins.classmethod
    def from_name(cls, name: builtins.str) -> "FluentBitLogStreamOutput":
        '''Sets output to a named log stream.

        If a log stream with the given name doesn't exist in the configured log
        group a log stream with the given name will be created.

        :param name: The name of the log stream where records should be written.

        :return:

        A FluentBitLogStreamOutput object representing the configured
        log stream destination.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitLogStreamOutput.from_name)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("FluentBitLogStreamOutput", jsii.sinvoke(cls, "fromName", [name]))

    @jsii.member(jsii_name="fromPrefix")
    @builtins.classmethod
    def from_prefix(cls, prefix: builtins.str) -> "FluentBitLogStreamOutput":
        '''Sets output to a prefixed log stream.

        Log streams will be created on a per-pod basis with the name oof the log
        streams starting with the provided prefix.

        :param prefix: The prefix for log streams which will be created.

        :return:

        A FluentBitLogStreamOutput object representing the configured
        log stream destination.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitLogStreamOutput.from_prefix)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        return typing.cast("FluentBitLogStreamOutput", jsii.sinvoke(cls, "fromPrefix", [prefix]))

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''The name of the log stream where records should be created.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamName"))

    @builtins.property
    @jsii.member(jsii_name="logStreamPrefix")
    def log_stream_prefix(self) -> typing.Optional[builtins.str]:
        '''The prefix for log streams that will be created on a per-pod basis.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamPrefix"))


class FluentBitMatch(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitMatch",
):
    '''Represents a filter that can be applied to Filter and Output plugins that scopes down what records the given filter should apply to.'''

    @jsii.member(jsii_name="glob")
    @builtins.classmethod
    def glob(cls, pattern: builtins.str) -> "FluentBitMatch":
        '''Creates a match pattern that supports basic wildcard matching using the star character (``*``).

        :param pattern: The pattern to use to match against the tags of an incoming record. It's case sensitive and support the star (``*``) character as a wildcard.

        :return: A match object representing the given pattern.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitMatch.glob)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast("FluentBitMatch", jsii.sinvoke(cls, "glob", [pattern]))

    @jsii.member(jsii_name="regex")
    @builtins.classmethod
    def regex(cls, pattern: builtins.str) -> "FluentBitMatch":
        '''Creates a match pattern that supports full regex matching.

        :param pattern: A regular expression to match against the tags of incoming records.

        :return: A match object representing the given pattern.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitMatch.regex)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast("FluentBitMatch", jsii.sinvoke(cls, "regex", [pattern]))

    @jsii.member(jsii_name="toObject")
    def to_object(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Creates a record object that can be used to represent the match in Fluent Bit configuration files.

        :return: The object that can be used to represent this match object.
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.invoke(self, "toObject", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Creates a string representation of this match object that reflects how it will appear in a Fluent Bit configuration file.

        :return: A string representation of this match.
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ALL")
    def ALL(cls) -> "FluentBitMatch":
        '''Represents a pattern that will match all log entries.'''
        return typing.cast("FluentBitMatch", jsii.sget(cls, "ALL"))

    @builtins.property
    @jsii.member(jsii_name="evaluator")
    def evaluator(self) -> "FluentBitMatchEvaluator":
        '''The pattern matching syntax to use when evaluating incoming tags.

        :group: Inputs
        '''
        return typing.cast("FluentBitMatchEvaluator", jsii.get(self, "evaluator"))

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        '''The pattern to compare against the tags of incoming records.

        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "pattern"))


@jsii.enum(jsii_type="cdk-extensions.k8s_aws.FluentBitMatchEvaluator")
class FluentBitMatchEvaluator(enum.Enum):
    '''Matching patterns supported by Fluent Bit plugins for scoping down incoming records.'''

    GLOB = "GLOB"
    '''A basic pattern match supporting the star (``*``) character as a wildcard.'''
    REGEX = "REGEX"
    '''Full pattern matching using regular expressions.'''


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitModifyFilterOptions",
    jsii_struct_bases=[FluentBitFilterPluginCommonOptions],
    name_mapping={
        "match": "match",
        "conditions": "conditions",
        "operations": "operations",
    },
)
class FluentBitModifyFilterOptions(FluentBitFilterPluginCommonOptions):
    def __init__(
        self,
        *,
        match: typing.Optional[FluentBitMatch] = None,
        conditions: typing.Optional[typing.Sequence["ModifyCondition"]] = None,
        operations: typing.Optional[typing.Sequence["ModifyOperation"]] = None,
    ) -> None:
        '''Options for configuring the Modify Fluent Bit filter plugin.

        :param match: The pattern to match for records that this output should apply to.
        :param conditions: 
        :param operations: 

        :see: `Modify Plugin Documention <https://docs.fluentbit.io/manual/pipeline/filters/modify>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitModifyFilterOptions.__init__)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument operations", value=operations, expected_type=type_hints["operations"])
        self._values: typing.Dict[str, typing.Any] = {}
        if match is not None:
            self._values["match"] = match
        if conditions is not None:
            self._values["conditions"] = conditions
        if operations is not None:
            self._values["operations"] = operations

    @builtins.property
    def match(self) -> typing.Optional[FluentBitMatch]:
        '''The pattern to match for records that this output should apply to.'''
        result = self._values.get("match")
        return typing.cast(typing.Optional[FluentBitMatch], result)

    @builtins.property
    def conditions(self) -> typing.Optional[typing.List["ModifyCondition"]]:
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[typing.List["ModifyCondition"]], result)

    @builtins.property
    def operations(self) -> typing.Optional[typing.List["ModifyOperation"]]:
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.List["ModifyOperation"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitModifyFilterOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitNestFilterOptions",
    jsii_struct_bases=[FluentBitFilterPluginCommonOptions],
    name_mapping={
        "match": "match",
        "operation": "operation",
        "add_prefix": "addPrefix",
        "remove_prefix": "removePrefix",
    },
)
class FluentBitNestFilterOptions(FluentBitFilterPluginCommonOptions):
    def __init__(
        self,
        *,
        match: typing.Optional[FluentBitMatch] = None,
        operation: "NestFilterOperation",
        add_prefix: typing.Optional[builtins.str] = None,
        remove_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Options for configuring the Nest Fluent Bit filter plugin.

        :param match: The pattern to match for records that this output should apply to.
        :param operation: The operation the filter will perform.
        :param add_prefix: Prefix affected keys with this string.
        :param remove_prefix: Remove prefix from affected keys if it matches this string.

        :see: `Nest Plugin Documention <https://docs.fluentbit.io/manual/pipeline/filters/nest>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitNestFilterOptions.__init__)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
            check_type(argname="argument add_prefix", value=add_prefix, expected_type=type_hints["add_prefix"])
            check_type(argname="argument remove_prefix", value=remove_prefix, expected_type=type_hints["remove_prefix"])
        self._values: typing.Dict[str, typing.Any] = {
            "operation": operation,
        }
        if match is not None:
            self._values["match"] = match
        if add_prefix is not None:
            self._values["add_prefix"] = add_prefix
        if remove_prefix is not None:
            self._values["remove_prefix"] = remove_prefix

    @builtins.property
    def match(self) -> typing.Optional[FluentBitMatch]:
        '''The pattern to match for records that this output should apply to.'''
        result = self._values.get("match")
        return typing.cast(typing.Optional[FluentBitMatch], result)

    @builtins.property
    def operation(self) -> "NestFilterOperation":
        '''The operation the filter will perform.'''
        result = self._values.get("operation")
        assert result is not None, "Required property 'operation' is missing"
        return typing.cast("NestFilterOperation", result)

    @builtins.property
    def add_prefix(self) -> typing.Optional[builtins.str]:
        '''Prefix affected keys with this string.'''
        result = self._values.get("add_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remove_prefix(self) -> typing.Optional[builtins.str]:
        '''Remove prefix from affected keys if it matches this string.'''
        result = self._values.get("remove_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitNestFilterOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FluentBitOutput(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitOutput",
):
    '''Common options that allow configuration of destinations where Fluent Bit should send records after processing.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="cloudwatchLogs")
    @builtins.classmethod
    def cloudwatch_logs(
        cls,
        match: FluentBitMatch,
        log_group: aws_cdk.aws_logs.ILogGroup,
    ) -> "IFluentBitOutputPlugin":
        '''Sends matched records to a CloudWatch Logs log group.

        :param match: A pattern filtering to which records the output should be applied.
        :param log_group: The log group where matched records should be sent.

        :return:

        An output filter object that can be applied to the Fluent Bit
        configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitOutput.cloudwatch_logs)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("IFluentBitOutputPlugin", jsii.sinvoke(cls, "cloudwatchLogs", [match, log_group]))

    @jsii.member(jsii_name="kinesis")
    @builtins.classmethod
    def kinesis(
        cls,
        match: FluentBitMatch,
        stream: aws_cdk.aws_kinesis.IStream,
    ) -> "IFluentBitOutputPlugin":
        '''Sends matched records to a Kinesis data stream.

        :param match: A pattern filtering to which records the output should be applied.
        :param stream: The Kinesis stream where matched records should be sent.

        :return:

        An output filter object that can be applied to the Fluent Bit
        configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitOutput.kinesis)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
        return typing.cast("IFluentBitOutputPlugin", jsii.sinvoke(cls, "kinesis", [match, stream]))

    @jsii.member(jsii_name="kinesisFirehose")
    @builtins.classmethod
    def kinesis_firehose(
        cls,
        match: FluentBitMatch,
        delivery_stream: _IDeliveryStream_cf5feed7,
    ) -> "IFluentBitOutputPlugin":
        '''Sends matched records to a Kinesis Firehose delivery stream.

        :param match: A pattern filtering to which records the output should be applied.
        :param delivery_stream: The Firehose delivery stream where matched records should be sent.

        :return:

        An output filter object that can be applied to the Fluent Bit
        configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitOutput.kinesis_firehose)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("IFluentBitOutputPlugin", jsii.sinvoke(cls, "kinesisFirehose", [match, delivery_stream]))

    @jsii.member(jsii_name="opensearch")
    @builtins.classmethod
    def opensearch(
        cls,
        match: FluentBitMatch,
        domain: aws_cdk.aws_opensearchservice.IDomain,
    ) -> "IFluentBitOutputPlugin":
        '''Sends matched records to an OpenSearch domain.

        :param match: A pattern filtering to which records the output should be applied.
        :param domain: The OpenSearch domain where matched records should be sent.

        :return:

        An output filter object that can be applied to the Fluent Bit
        configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitOutput.opensearch)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
        return typing.cast("IFluentBitOutputPlugin", jsii.sinvoke(cls, "opensearch", [match, domain]))


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitOutputPluginCommonOptions",
    jsii_struct_bases=[],
    name_mapping={"match": "match"},
)
class FluentBitOutputPluginCommonOptions:
    def __init__(self, *, match: typing.Optional[FluentBitMatch] = None) -> None:
        '''Configuration options that apply to all Fluent Bit output plugins.

        :param match: The pattern to match for records that this output should apply to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitOutputPluginCommonOptions.__init__)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
        self._values: typing.Dict[str, typing.Any] = {}
        if match is not None:
            self._values["match"] = match

    @builtins.property
    def match(self) -> typing.Optional[FluentBitMatch]:
        '''The pattern to match for records that this output should apply to.'''
        result = self._values.get("match")
        return typing.cast(typing.Optional[FluentBitMatch], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitOutputPluginCommonOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FluentBitParser(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitParser",
):
    '''Standard parse comfigurations which can be applied to Fluent Bit to allow for parsing data from incoming records.

    The records to which parsers are applied is controlled using the parser
    filter.

    :see: {@link FluentBitParserFilter}
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="json")
    @builtins.classmethod
    def json(cls, name: builtins.str) -> "IFluentBitParserPlugin":
        '''Creates a parser that processes records that are formatted in JSON.

        :param name: The name of the parser which will be used for referencing it in other configurations.

        :return:

        A parser object that can be applied to the Fluent Bit
        configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitParser.json)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("IFluentBitParserPlugin", jsii.sinvoke(cls, "json", [name]))

    @jsii.member(jsii_name="logfmt")
    @builtins.classmethod
    def logfmt(cls, name: builtins.str) -> "IFluentBitParserPlugin":
        '''Creates a parser that processes records that are formatted using the ``logfmt`` standard.

        :param name: The name of the parser which will be used for referencing it in other configurations.

        :return:

        A parser object that can be applied to the Fluent Bit
        configuration.

        :see: `Golang logfmt documentation <https://pkg.go.dev/github.com/kr/logfmt>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitParser.logfmt)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("IFluentBitParserPlugin", jsii.sinvoke(cls, "logfmt", [name]))

    @jsii.member(jsii_name="ltsv")
    @builtins.classmethod
    def ltsv(cls, name: builtins.str) -> "IFluentBitParserPlugin":
        '''Creates a parser that processes records that are formatted using the ``ltsv`` standard.

        :param name: The name of the parser which will be used for referencing it in other configurations.

        :return:

        A parser object that can be applied to the Fluent Bit
        configuration.

        :see: `LTSV <http://ltsv.org/>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitParser.ltsv)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("IFluentBitParserPlugin", jsii.sinvoke(cls, "ltsv", [name]))

    @jsii.member(jsii_name="regex")
    @builtins.classmethod
    def regex(cls, name: builtins.str, regex: builtins.str) -> "IFluentBitParserPlugin":
        '''Creates a parser that uses regular expressions to parse incoming records.

        :param name: The name of the parser which will be used for referencing it in other configurations.
        :param regex: The regular expression to use to parse records.

        :return:

        A parser object that can be applied to the Fluent Bit
        configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitParser.regex)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
        return typing.cast("IFluentBitParserPlugin", jsii.sinvoke(cls, "regex", [name, regex]))


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitParserFilterOptions",
    jsii_struct_bases=[FluentBitFilterPluginCommonOptions],
    name_mapping={
        "match": "match",
        "key_name": "keyName",
        "parsers": "parsers",
        "preserve_key": "preserveKey",
        "reserve_data": "reserveData",
    },
)
class FluentBitParserFilterOptions(FluentBitFilterPluginCommonOptions):
    def __init__(
        self,
        *,
        match: typing.Optional[FluentBitMatch] = None,
        key_name: builtins.str,
        parsers: typing.Optional[typing.Sequence["IFluentBitParserPlugin"]] = None,
        preserve_key: typing.Optional[builtins.bool] = None,
        reserve_data: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Options for configuring the Parser Fluent Bit filter plugin.

        :param match: The pattern to match for records that this output should apply to.
        :param key_name: Specify field name in record to parse.
        :param parsers: The parsers to use to interpret the field.
        :param preserve_key: Keep original ``keyName`` field in the parsed result. If ``false``, the field will be removed. Default: false
        :param reserve_data: Keep all other original fields in the parsed result. If ``false``, all other original fields will be removed. Default: false

        :see: `Parser Plugin Documention <https://docs.fluentbit.io/manual/pipeline/filters/parser>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitParserFilterOptions.__init__)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument parsers", value=parsers, expected_type=type_hints["parsers"])
            check_type(argname="argument preserve_key", value=preserve_key, expected_type=type_hints["preserve_key"])
            check_type(argname="argument reserve_data", value=reserve_data, expected_type=type_hints["reserve_data"])
        self._values: typing.Dict[str, typing.Any] = {
            "key_name": key_name,
        }
        if match is not None:
            self._values["match"] = match
        if parsers is not None:
            self._values["parsers"] = parsers
        if preserve_key is not None:
            self._values["preserve_key"] = preserve_key
        if reserve_data is not None:
            self._values["reserve_data"] = reserve_data

    @builtins.property
    def match(self) -> typing.Optional[FluentBitMatch]:
        '''The pattern to match for records that this output should apply to.'''
        result = self._values.get("match")
        return typing.cast(typing.Optional[FluentBitMatch], result)

    @builtins.property
    def key_name(self) -> builtins.str:
        '''Specify field name in record to parse.'''
        result = self._values.get("key_name")
        assert result is not None, "Required property 'key_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parsers(self) -> typing.Optional[typing.List["IFluentBitParserPlugin"]]:
        '''The parsers to use to interpret the field.'''
        result = self._values.get("parsers")
        return typing.cast(typing.Optional[typing.List["IFluentBitParserPlugin"]], result)

    @builtins.property
    def preserve_key(self) -> typing.Optional[builtins.bool]:
        '''Keep original ``keyName`` field in the parsed result.

        If ``false``, the field will be removed.

        :default: false
        '''
        result = self._values.get("preserve_key")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def reserve_data(self) -> typing.Optional[builtins.bool]:
        '''Keep all other original fields in the parsed result.

        If ``false``, all other original fields will be removed.

        :default: false
        '''
        result = self._values.get("reserve_data")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitParserFilterOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitParserPluginCommonOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class FluentBitParserPluginCommonOptions:
    def __init__(self) -> None:
        '''Configuration options that apply to all Fluent Bit parser plugins.'''
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitParserPluginCommonOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitPluginCommonOptions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "plugin_type": "pluginType"},
)
class FluentBitPluginCommonOptions:
    def __init__(
        self,
        *,
        name: builtins.str,
        plugin_type: "FluentBitPluginType",
    ) -> None:
        '''Options that are applicable to all Fluent Bit Plugins regardless of type.

        :param name: The name of the fluent bit plugin.
        :param plugin_type: Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitPluginCommonOptions.__init__)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument plugin_type", value=plugin_type, expected_type=type_hints["plugin_type"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "plugin_type": plugin_type,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the fluent bit plugin.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def plugin_type(self) -> "FluentBitPluginType":
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.'''
        result = self._values.get("plugin_type")
        assert result is not None, "Required property 'plugin_type' is missing"
        return typing.cast("FluentBitPluginType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitPluginCommonOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.k8s_aws.FluentBitPluginType")
class FluentBitPluginType(enum.Enum):
    '''The types of Fluent Bit plugins that can be configured.'''

    FILTER = "FILTER"
    '''A plugin that transforms or filters records.'''
    OUTPUT = "OUTPUT"
    '''A plugin that configures where output should be sent.'''
    PARSER = "PARSER"
    '''A plugin that read data from input objects into structured objects.'''


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitRecordModifierFilterOptions",
    jsii_struct_bases=[FluentBitFilterPluginCommonOptions],
    name_mapping={
        "match": "match",
        "allow": "allow",
        "records": "records",
        "remove": "remove",
    },
)
class FluentBitRecordModifierFilterOptions(FluentBitFilterPluginCommonOptions):
    def __init__(
        self,
        *,
        match: typing.Optional[FluentBitMatch] = None,
        allow: typing.Optional[typing.Sequence[builtins.str]] = None,
        records: typing.Optional[typing.Sequence[typing.Union[AppendedRecord, typing.Dict[str, typing.Any]]]] = None,
        remove: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Options for configuring the Record Modifier Fluent Bit filter plugin.

        :param match: The pattern to match for records that this output should apply to.
        :param allow: If a tag is not match, that field is removed.
        :param records: Add fields to the output.
        :param remove: If a tag is match, that field is removed.

        :see: `Record Modifier Plugin Documention <https://docs.fluentbit.io/manual/pipeline/filters/record-modifier>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitRecordModifierFilterOptions.__init__)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument allow", value=allow, expected_type=type_hints["allow"])
            check_type(argname="argument records", value=records, expected_type=type_hints["records"])
            check_type(argname="argument remove", value=remove, expected_type=type_hints["remove"])
        self._values: typing.Dict[str, typing.Any] = {}
        if match is not None:
            self._values["match"] = match
        if allow is not None:
            self._values["allow"] = allow
        if records is not None:
            self._values["records"] = records
        if remove is not None:
            self._values["remove"] = remove

    @builtins.property
    def match(self) -> typing.Optional[FluentBitMatch]:
        '''The pattern to match for records that this output should apply to.'''
        result = self._values.get("match")
        return typing.cast(typing.Optional[FluentBitMatch], result)

    @builtins.property
    def allow(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If a tag is not match, that field is removed.'''
        result = self._values.get("allow")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def records(self) -> typing.Optional[typing.List[AppendedRecord]]:
        '''Add fields to the output.'''
        result = self._values.get("records")
        return typing.cast(typing.Optional[typing.List[AppendedRecord]], result)

    @builtins.property
    def remove(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If a tag is match, that field is removed.'''
        result = self._values.get("remove")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitRecordModifierFilterOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitRegexParserOptions",
    jsii_struct_bases=[FluentBitParserPluginCommonOptions],
    name_mapping={
        "regex": "regex",
        "skip_empty_values": "skipEmptyValues",
        "time_format": "timeFormat",
        "time_key": "timeKey",
        "types": "types",
    },
)
class FluentBitRegexParserOptions(FluentBitParserPluginCommonOptions):
    def __init__(
        self,
        *,
        regex: builtins.str,
        skip_empty_values: typing.Optional[builtins.bool] = None,
        time_format: typing.Optional[builtins.str] = None,
        time_key: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Mapping[builtins.str, "ParserPluginDataType"]] = None,
    ) -> None:
        '''Options for configuring the Regex Fluent Bit parser plugin.

        :param regex: The regular expression to use to parse the incoming records. Use regex group names to define the name of fields being captured.
        :param skip_empty_values: If enabled, the parser ignores empty value of the record.
        :param time_format: Defines the format of the timestamp on the inbound record.
        :param time_key: The key under which timestamp information for the inbound record is given.
        :param types: Maps group names matched by the regex to the data types they should be interpreted as.

        :see: `Regex Plugin Documention <https://docs.fluentbit.io/manual/pipeline/parsers/regular-expression>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitRegexParserOptions.__init__)
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument skip_empty_values", value=skip_empty_values, expected_type=type_hints["skip_empty_values"])
            check_type(argname="argument time_format", value=time_format, expected_type=type_hints["time_format"])
            check_type(argname="argument time_key", value=time_key, expected_type=type_hints["time_key"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[str, typing.Any] = {
            "regex": regex,
        }
        if skip_empty_values is not None:
            self._values["skip_empty_values"] = skip_empty_values
        if time_format is not None:
            self._values["time_format"] = time_format
        if time_key is not None:
            self._values["time_key"] = time_key
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def regex(self) -> builtins.str:
        '''The regular expression to use to parse the incoming records.

        Use regex group names to define the name of fields being captured.
        '''
        result = self._values.get("regex")
        assert result is not None, "Required property 'regex' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def skip_empty_values(self) -> typing.Optional[builtins.bool]:
        '''If enabled, the parser ignores empty value of the record.'''
        result = self._values.get("skip_empty_values")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def time_format(self) -> typing.Optional[builtins.str]:
        '''Defines the format of the timestamp on the inbound record.

        :see: `strftime <http://man7.org/linux/man-pages/man3/strftime.3.html>`_
        '''
        result = self._values.get("time_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_key(self) -> typing.Optional[builtins.str]:
        '''The key under which timestamp information for the inbound record is given.'''
        result = self._values.get("time_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def types(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "ParserPluginDataType"]]:
        '''Maps group names matched by the regex to the data types they should be interpreted as.'''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "ParserPluginDataType"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitRegexParserOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitRewriteTagFilterOptions",
    jsii_struct_bases=[FluentBitFilterPluginCommonOptions],
    name_mapping={
        "match": "match",
        "emitter_mem_buf_limit": "emitterMemBufLimit",
        "emitter_name": "emitterName",
        "emitter_storage_type": "emitterStorageType",
        "rules": "rules",
    },
)
class FluentBitRewriteTagFilterOptions(FluentBitFilterPluginCommonOptions):
    def __init__(
        self,
        *,
        match: typing.Optional[FluentBitMatch] = None,
        emitter_mem_buf_limit: typing.Optional[_DataSize_d20aaece] = None,
        emitter_name: typing.Optional[builtins.str] = None,
        emitter_storage_type: typing.Optional[EmitterStorageType] = None,
        rules: typing.Optional[typing.Sequence[typing.Union["RewriteTagRule", typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''Options for configuring the Parser Fluent Bit filter plugin.

        :param match: The pattern to match for records that this output should apply to.
        :param emitter_mem_buf_limit: Set a limit on the amount of memory the tag rewrite emitter can consume if the outputs provide backpressure. Default: 10M
        :param emitter_name: When the filter emits a record under the new Tag, there is an internal emitter plugin that takes care of the job. Since this emitter expose metrics as any other component of the pipeline, you can use this property to configure an optional name for it.
        :param emitter_storage_type: Define a buffering mechanism for the new records created. Note these records are part of the emitter plugin.
        :param rules: Defines the matching criteria and the format of the Tag for the matching record.

        :see: `Parser Plugin Documention <https://docs.fluentbit.io/manual/pipeline/filters/parser>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitRewriteTagFilterOptions.__init__)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument emitter_mem_buf_limit", value=emitter_mem_buf_limit, expected_type=type_hints["emitter_mem_buf_limit"])
            check_type(argname="argument emitter_name", value=emitter_name, expected_type=type_hints["emitter_name"])
            check_type(argname="argument emitter_storage_type", value=emitter_storage_type, expected_type=type_hints["emitter_storage_type"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[str, typing.Any] = {}
        if match is not None:
            self._values["match"] = match
        if emitter_mem_buf_limit is not None:
            self._values["emitter_mem_buf_limit"] = emitter_mem_buf_limit
        if emitter_name is not None:
            self._values["emitter_name"] = emitter_name
        if emitter_storage_type is not None:
            self._values["emitter_storage_type"] = emitter_storage_type
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def match(self) -> typing.Optional[FluentBitMatch]:
        '''The pattern to match for records that this output should apply to.'''
        result = self._values.get("match")
        return typing.cast(typing.Optional[FluentBitMatch], result)

    @builtins.property
    def emitter_mem_buf_limit(self) -> typing.Optional[_DataSize_d20aaece]:
        '''Set a limit on the amount of memory the tag rewrite emitter can consume if the outputs provide backpressure.

        :default: 10M
        '''
        result = self._values.get("emitter_mem_buf_limit")
        return typing.cast(typing.Optional[_DataSize_d20aaece], result)

    @builtins.property
    def emitter_name(self) -> typing.Optional[builtins.str]:
        '''When the filter emits a record under the new Tag, there is an internal emitter plugin that takes care of the job.

        Since this emitter expose
        metrics as any other component of the pipeline, you can use this
        property to configure an optional name for it.
        '''
        result = self._values.get("emitter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def emitter_storage_type(self) -> typing.Optional[EmitterStorageType]:
        '''Define a buffering mechanism for the new records created.

        Note these records are part of the emitter plugin.
        '''
        result = self._values.get("emitter_storage_type")
        return typing.cast(typing.Optional[EmitterStorageType], result)

    @builtins.property
    def rules(self) -> typing.Optional[typing.List["RewriteTagRule"]]:
        '''Defines the matching criteria and the format of the Tag for the matching record.'''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.List["RewriteTagRule"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitRewriteTagFilterOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitThrottleFilterOptions",
    jsii_struct_bases=[FluentBitFilterPluginCommonOptions],
    name_mapping={
        "match": "match",
        "interval": "interval",
        "print_status": "printStatus",
        "rate": "rate",
        "window": "window",
    },
)
class FluentBitThrottleFilterOptions(FluentBitFilterPluginCommonOptions):
    def __init__(
        self,
        *,
        match: typing.Optional[FluentBitMatch] = None,
        interval: typing.Optional[aws_cdk.Duration] = None,
        print_status: typing.Optional[builtins.bool] = None,
        rate: typing.Optional[jsii.Number] = None,
        window: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Options for configuring the Throttle Fluent Bit filter plugin.

        :param match: The pattern to match for records that this output should apply to.
        :param interval: Time interval.
        :param print_status: Whether to print status messages with current rate and the limits to information logs.
        :param rate: Amount of messages for the time.
        :param window: Amount of intervals to calculate average over. Default: 5

        :see: `Throttle Plugin Documention <https://docs.fluentbit.io/manual/pipeline/filters/throttle>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitThrottleFilterOptions.__init__)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument print_status", value=print_status, expected_type=type_hints["print_status"])
            check_type(argname="argument rate", value=rate, expected_type=type_hints["rate"])
            check_type(argname="argument window", value=window, expected_type=type_hints["window"])
        self._values: typing.Dict[str, typing.Any] = {}
        if match is not None:
            self._values["match"] = match
        if interval is not None:
            self._values["interval"] = interval
        if print_status is not None:
            self._values["print_status"] = print_status
        if rate is not None:
            self._values["rate"] = rate
        if window is not None:
            self._values["window"] = window

    @builtins.property
    def match(self) -> typing.Optional[FluentBitMatch]:
        '''The pattern to match for records that this output should apply to.'''
        result = self._values.get("match")
        return typing.cast(typing.Optional[FluentBitMatch], result)

    @builtins.property
    def interval(self) -> typing.Optional[aws_cdk.Duration]:
        '''Time interval.'''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def print_status(self) -> typing.Optional[builtins.bool]:
        '''Whether to print status messages with current rate and the limits to information logs.'''
        result = self._values.get("print_status")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def rate(self) -> typing.Optional[jsii.Number]:
        '''Amount of messages for the time.'''
        result = self._values.get("rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def window(self) -> typing.Optional[jsii.Number]:
        '''Amount of intervals to calculate average over.

        :default: 5
        '''
        result = self._values.get("window")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitThrottleFilterOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="cdk-extensions.k8s_aws.IExternalDnsRegistry")
class IExternalDnsRegistry(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="registryType")
    def registry_type(self) -> builtins.str:
        ...

    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> ExternalDnsRegistryConfiguration:
        '''
        :param scope: -
        '''
        ...


class _IExternalDnsRegistryProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.k8s_aws.IExternalDnsRegistry"

    @builtins.property
    @jsii.member(jsii_name="registryType")
    def registry_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registryType"))

    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> ExternalDnsRegistryConfiguration:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IExternalDnsRegistry.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(ExternalDnsRegistryConfiguration, jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IExternalDnsRegistry).__jsii_proxy_class__ = lambda : _IExternalDnsRegistryProxy


@jsii.interface(jsii_type="cdk-extensions.k8s_aws.IFluentBitPlugin")
class IFluentBitPlugin(typing_extensions.Protocol):
    '''Represents a Fluent Bit plugin that allows for configuration of options and can be used to configure logging from containers.'''

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the fluent bit plugin.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="pluginType")
    def plugin_type(self) -> builtins.str:
        '''The type of fluent bit plugin.'''
        ...

    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> "ResolvedFluentBitConfiguration":
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.

        :param scope: -
        '''
        ...


class _IFluentBitPluginProxy:
    '''Represents a Fluent Bit plugin that allows for configuration of options and can be used to configure logging from containers.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.k8s_aws.IFluentBitPlugin"

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the fluent bit plugin.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="pluginType")
    def plugin_type(self) -> builtins.str:
        '''The type of fluent bit plugin.'''
        return typing.cast(builtins.str, jsii.get(self, "pluginType"))

    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> "ResolvedFluentBitConfiguration":
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.

        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IFluentBitPlugin.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("ResolvedFluentBitConfiguration", jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFluentBitPlugin).__jsii_proxy_class__ = lambda : _IFluentBitPluginProxy


@jsii.interface(jsii_type="cdk-extensions.k8s_aws.INestFilterOperation")
class INestFilterOperation(typing_extensions.Protocol):
    '''Represents an operation with excludive options that can be performed by the Fluent Bit Nest filter plugin.'''

    @builtins.property
    @jsii.member(jsii_name="fields")
    def fields(self) -> typing.Mapping[builtins.str, typing.List[builtins.str]]:
        ...

    @builtins.property
    @jsii.member(jsii_name="operation")
    def operation(self) -> "NestFilterOperationType":
        ...


class _INestFilterOperationProxy:
    '''Represents an operation with excludive options that can be performed by the Fluent Bit Nest filter plugin.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.k8s_aws.INestFilterOperation"

    @builtins.property
    @jsii.member(jsii_name="fields")
    def fields(self) -> typing.Mapping[builtins.str, typing.List[builtins.str]]:
        return typing.cast(typing.Mapping[builtins.str, typing.List[builtins.str]], jsii.get(self, "fields"))

    @builtins.property
    @jsii.member(jsii_name="operation")
    def operation(self) -> "NestFilterOperationType":
        return typing.cast("NestFilterOperationType", jsii.get(self, "operation"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INestFilterOperation).__jsii_proxy_class__ = lambda : _INestFilterOperationProxy


@jsii.interface(jsii_type="cdk-extensions.k8s_aws.ISecretReference")
class ISecretReference(typing_extensions.Protocol):
    '''Represents a resource the can be synchronized into a Kubernetes secret.'''

    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> "SecretReferenceConfiguration":
        '''Gets the configuration details for the resource being sychronized in a form that can be universally used to create the synchronization configuration.

        :param scope: The scope of the construct that will be configuring the synchronization configuration.
        '''
        ...


class _ISecretReferenceProxy:
    '''Represents a resource the can be synchronized into a Kubernetes secret.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.k8s_aws.ISecretReference"

    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> "SecretReferenceConfiguration":
        '''Gets the configuration details for the resource being sychronized in a form that can be universally used to create the synchronization configuration.

        :param scope: The scope of the construct that will be configuring the synchronization configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ISecretReference.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("SecretReferenceConfiguration", jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISecretReference).__jsii_proxy_class__ = lambda : _ISecretReferenceProxy


@jsii.interface(jsii_type="cdk-extensions.k8s_aws.ISecretStore")
class ISecretStore(constructs.IDependable, typing_extensions.Protocol):
    '''Represents a Kubernetes secret store resource.'''

    @builtins.property
    @jsii.member(jsii_name="secretStoreName")
    def secret_store_name(self) -> builtins.str:
        '''The name of the secret store as it appears in Kubernetes.'''
        ...


class _ISecretStoreProxy(
    jsii.proxy_for(constructs.IDependable), # type: ignore[misc]
):
    '''Represents a Kubernetes secret store resource.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.k8s_aws.ISecretStore"

    @builtins.property
    @jsii.member(jsii_name="secretStoreName")
    def secret_store_name(self) -> builtins.str:
        '''The name of the secret store as it appears in Kubernetes.'''
        return typing.cast(builtins.str, jsii.get(self, "secretStoreName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISecretStore).__jsii_proxy_class__ = lambda : _ISecretStoreProxy


@jsii.enum(jsii_type="cdk-extensions.k8s_aws.KinesisFirehoseCompressionFormat")
class KinesisFirehoseCompressionFormat(enum.Enum):
    ARROW = "ARROW"
    '''The Apache Arrow compression format.

    Only available if the Fluent Fit service being used to send logs to
    Firehose had Apache Arrow enabled at compile time.
    '''
    GZIP = "GZIP"
    '''Gzip compression format.'''


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.LiftOptions",
    jsii_struct_bases=[],
    name_mapping={"nested_under": "nestedUnder"},
)
class LiftOptions:
    def __init__(self, *, nested_under: builtins.str) -> None:
        '''
        :param nested_under: Lift records nested under the this key.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LiftOptions.__init__)
            check_type(argname="argument nested_under", value=nested_under, expected_type=type_hints["nested_under"])
        self._values: typing.Dict[str, typing.Any] = {
            "nested_under": nested_under,
        }

    @builtins.property
    def nested_under(self) -> builtins.str:
        '''Lift records nested under the this key.'''
        result = self._values.get("nested_under")
        assert result is not None, "Required property 'nested_under' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LiftOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.k8s_aws.MetadataPolicy")
class MetadataPolicy(enum.Enum):
    '''Options for fetching tags/labels from provider secrets.'''

    FETCH = "FETCH"
    '''Fetch tags/labels from provider secrets.'''
    NONE = "NONE"
    '''Do not fetch tags/labels from provider secrets.'''


class ModifyCondition(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.ModifyCondition",
):
    @jsii.member(jsii_name="aKeyMatches")
    @builtins.classmethod
    def a_key_matches(cls, regex: builtins.str) -> "ModifyCondition":
        '''Condition that returns true if any key matches a specified regular expression.

        :param regex: The regular expression to evaluate against field keys.

        :return: A ModifyCondition object representing the condition.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyCondition.a_key_matches)
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
        return typing.cast("ModifyCondition", jsii.sinvoke(cls, "aKeyMatches", [regex]))

    @jsii.member(jsii_name="keyDoesNotExists")
    @builtins.classmethod
    def key_does_not_exists(cls, key: builtins.str) -> "ModifyCondition":
        '''Condition that returns true if a specified key does not exist.

        :param key: The key to check for existence.

        :return: A ModifyCondition object representing the condition.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyCondition.key_does_not_exists)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast("ModifyCondition", jsii.sinvoke(cls, "keyDoesNotExists", [key]))

    @jsii.member(jsii_name="keyExists")
    @builtins.classmethod
    def key_exists(cls, key: builtins.str) -> "ModifyCondition":
        '''Condition that returns true if a specified key exists.

        :param key: The key to check for existence.

        :return: A ModifyCondition object representing the condition.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyCondition.key_exists)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast("ModifyCondition", jsii.sinvoke(cls, "keyExists", [key]))

    @jsii.member(jsii_name="keyValueDoesNotEqual")
    @builtins.classmethod
    def key_value_does_not_equal(
        cls,
        key: builtins.str,
        value: builtins.str,
    ) -> "ModifyCondition":
        '''Condition that returns true if a specified key exists and its value does not match the specified value.

        :param key: The key to check for existence.
        :param value: The value to check for the given key.

        :return: A ModifyCondition object representing the condition.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyCondition.key_value_does_not_equal)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ModifyCondition", jsii.sinvoke(cls, "keyValueDoesNotEqual", [key, value]))

    @jsii.member(jsii_name="keyValueDoesNotMatch")
    @builtins.classmethod
    def key_value_does_not_match(
        cls,
        key: builtins.str,
        value: builtins.str,
    ) -> "ModifyCondition":
        '''Condition that returns true if a specified key exists and its value does not match the specified regular expression.

        :param key: The key to check for existence.
        :param value: The regular expression to check for the given key.

        :return: A ModifyCondition object representing the condition.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyCondition.key_value_does_not_match)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ModifyCondition", jsii.sinvoke(cls, "keyValueDoesNotMatch", [key, value]))

    @jsii.member(jsii_name="keyValueEquals")
    @builtins.classmethod
    def key_value_equals(
        cls,
        key: builtins.str,
        value: builtins.str,
    ) -> "ModifyCondition":
        '''Condition that returns true if a specified key exists and its value matches the specified value.

        :param key: The key to check for existence.
        :param value: The value to match for the given key.

        :return: A ModifyCondition object representing the condition.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyCondition.key_value_equals)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ModifyCondition", jsii.sinvoke(cls, "keyValueEquals", [key, value]))

    @jsii.member(jsii_name="keyValueMatches")
    @builtins.classmethod
    def key_value_matches(
        cls,
        key: builtins.str,
        value: builtins.str,
    ) -> "ModifyCondition":
        '''Condition that returns true if a specified key exists and its value matches the specified regular expression.

        :param key: The key to check for existence.
        :param value: The regular expression to match for the given key.

        :return: A ModifyCondition object representing the condition.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyCondition.key_value_matches)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ModifyCondition", jsii.sinvoke(cls, "keyValueMatches", [key, value]))

    @jsii.member(jsii_name="matchingKeysDoNotHaveMatchingValues")
    @builtins.classmethod
    def matching_keys_do_not_have_matching_values(
        cls,
        key: builtins.str,
        value: builtins.str,
    ) -> "ModifyCondition":
        '''Condition that returns true if all keys matching a specified regular expression have values that do not match another regular expression.

        :param key: The regular expression to use to filter keys.
        :param value: The regular expression to check the value of fields.

        :return: A ModifyCondition object representing the condition.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyCondition.matching_keys_do_not_have_matching_values)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ModifyCondition", jsii.sinvoke(cls, "matchingKeysDoNotHaveMatchingValues", [key, value]))

    @jsii.member(jsii_name="matchingKeysHaveMatchingValues")
    @builtins.classmethod
    def matching_keys_have_matching_values(
        cls,
        key: builtins.str,
        value: builtins.str,
    ) -> "ModifyCondition":
        '''Condition that returns true if all keys matching a specified regular expression have values that match another regular expression.

        :param key: The regular expression to use to filter keys.
        :param value: The regular expression to check the value of fields.

        :return: A ModifyCondition object representing the condition.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyCondition.matching_keys_have_matching_values)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ModifyCondition", jsii.sinvoke(cls, "matchingKeysHaveMatchingValues", [key, value]))

    @jsii.member(jsii_name="noKeyMatches")
    @builtins.classmethod
    def no_key_matches(cls, regex: builtins.str) -> "ModifyCondition":
        '''Condition that returns true if no key matches a specified regular expression.

        :param regex: The regular expression to evaluate against field keys.

        :return: A ModifyCondition object representing the condition.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyCondition.no_key_matches)
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
        return typing.cast("ModifyCondition", jsii.sinvoke(cls, "noKeyMatches", [regex]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls,
        condition: builtins.str,
        args: typing.Sequence[builtins.str],
    ) -> "ModifyCondition":
        '''An escape hatch method that allows fo defining custom conditions to be evaluated by the modify Fluent Bit filter plugin.

        :param condition: The name of the condition to be evaluated.
        :param args: The arguments to the operation.

        :return: A ModifyCondition object representing the options provided.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyCondition.of)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
        return typing.cast("ModifyCondition", jsii.sinvoke(cls, "of", [condition, args]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Gets a string representation of the arguments of this condition for use in a Fluent Bit plugin field.

        :return: A fluent bit value string.
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        '''Collection of arguments that apply to the condition.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        '''The name of the condition being evaluated.'''
        return typing.cast(builtins.str, jsii.get(self, "condition"))


class ModifyOperation(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.ModifyOperation",
):
    @jsii.member(jsii_name="add")
    @builtins.classmethod
    def add(cls, key: builtins.str, value: builtins.str) -> "ModifyOperation":
        '''Sets a field in the output to a specific value.

        If a field with the same name already exists it will be kept as is.

        :param key: The key name of the field to set.
        :param value: The value to set for the specified field.

        :return: A ModifyOperation object representing the add operation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyOperation.add)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ModifyOperation", jsii.sinvoke(cls, "add", [key, value]))

    @jsii.member(jsii_name="copy")
    @builtins.classmethod
    def copy(
        cls,
        original_key: builtins.str,
        new_key: builtins.str,
    ) -> "ModifyOperation":
        '''Copies a field from the input to a field with a new name if the field exists and a field with the new name does not exist.

        If a field with the new name already exists it is overwritten.

        :param original_key: The key in the input to be copied.
        :param new_key: The new name of the field to be copied to.

        :return: A ModifyOperation object representing the copy operation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyOperation.copy)
            check_type(argname="argument original_key", value=original_key, expected_type=type_hints["original_key"])
            check_type(argname="argument new_key", value=new_key, expected_type=type_hints["new_key"])
        return typing.cast("ModifyOperation", jsii.sinvoke(cls, "copy", [original_key, new_key]))

    @jsii.member(jsii_name="hardCopy")
    @builtins.classmethod
    def hard_copy(
        cls,
        original_key: builtins.str,
        new_key: builtins.str,
    ) -> "ModifyOperation":
        '''Copies a field from the input to a field with a new name if the field exists and a field with the new name does not exist.

        :param original_key: The key in the input to be copied.
        :param new_key: The new name of the field to be copied to.

        :return: A ModifyOperation object representing the copy operation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyOperation.hard_copy)
            check_type(argname="argument original_key", value=original_key, expected_type=type_hints["original_key"])
            check_type(argname="argument new_key", value=new_key, expected_type=type_hints["new_key"])
        return typing.cast("ModifyOperation", jsii.sinvoke(cls, "hardCopy", [original_key, new_key]))

    @jsii.member(jsii_name="hardRename")
    @builtins.classmethod
    def hard_rename(
        cls,
        original_key: builtins.str,
        renamed_key: builtins.str,
    ) -> "ModifyOperation":
        '''Renames a field from the input if the field exists.

        If a field with the desired name already exists it is overwritten.

        :param original_key: The key in the input to be renamed.
        :param renamed_key: The new name of the key in the output.

        :return: A ModifyOperation object representing the rename operation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyOperation.hard_rename)
            check_type(argname="argument original_key", value=original_key, expected_type=type_hints["original_key"])
            check_type(argname="argument renamed_key", value=renamed_key, expected_type=type_hints["renamed_key"])
        return typing.cast("ModifyOperation", jsii.sinvoke(cls, "hardRename", [original_key, renamed_key]))

    @jsii.member(jsii_name="moveToEnd")
    @builtins.classmethod
    def move_to_end(cls, key: builtins.str) -> "ModifyOperation":
        '''Moves fiels matching the given wildcard key to the end of the message.

        :param key: The wildcard to to match.

        :return: A ModifyOperation object representing the move operation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyOperation.move_to_end)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast("ModifyOperation", jsii.sinvoke(cls, "moveToEnd", [key]))

    @jsii.member(jsii_name="moveToStart")
    @builtins.classmethod
    def move_to_start(cls, key: builtins.str) -> "ModifyOperation":
        '''Moves fiels matching the given wildcard key to the start of the message.

        :param key: The wildcard to to match.

        :return: A ModifyOperation object representing the move operation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyOperation.move_to_start)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast("ModifyOperation", jsii.sinvoke(cls, "moveToStart", [key]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls,
        operation: builtins.str,
        args: typing.Sequence[builtins.str],
    ) -> "ModifyOperation":
        '''An escape hatch method that allows fo defining custom operations to be performed by the modify Fluent Bit filter plugin.

        :param operation: The name of the operation to be performed.
        :param args: The arguments to the operation.

        :return: A ModifyOperation object representing the options provided.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyOperation.of)
            check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
        return typing.cast("ModifyOperation", jsii.sinvoke(cls, "of", [operation, args]))

    @jsii.member(jsii_name="remove")
    @builtins.classmethod
    def remove(cls, key: builtins.str) -> "ModifyOperation":
        '''Removes a field in the output with a specific key.

        :param key: The key name of the field to remove.

        :return: A ModifyOperation object representing the remove operation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyOperation.remove)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast("ModifyOperation", jsii.sinvoke(cls, "remove", [key]))

    @jsii.member(jsii_name="removeRegex")
    @builtins.classmethod
    def remove_regex(cls, regex: builtins.str) -> "ModifyOperation":
        '''Removes all fields in the output matching the regular expression.

        :param regex: The regular expression specifying which fields to remove.

        :return: A ModifyOperation object representing the remove operation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyOperation.remove_regex)
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
        return typing.cast("ModifyOperation", jsii.sinvoke(cls, "removeRegex", [regex]))

    @jsii.member(jsii_name="removeWildcard")
    @builtins.classmethod
    def remove_wildcard(cls, key: builtins.str) -> "ModifyOperation":
        '''Removes all fields in the output matching the wildcard key.

        :param key: The wildcard expression specifying which fields to remove.

        :return: A ModifyOperation object representing the remove operation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyOperation.remove_wildcard)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast("ModifyOperation", jsii.sinvoke(cls, "removeWildcard", [key]))

    @jsii.member(jsii_name="rename")
    @builtins.classmethod
    def rename(
        cls,
        original_key: builtins.str,
        renamed_key: builtins.str,
    ) -> "ModifyOperation":
        '''Renames a field from the input if the field exists and a field with the new name does not exist.

        :param original_key: The key in the input to be renamed.
        :param renamed_key: The new name of the key in the output.

        :return: A ModifyOperation object representing the rename operation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyOperation.rename)
            check_type(argname="argument original_key", value=original_key, expected_type=type_hints["original_key"])
            check_type(argname="argument renamed_key", value=renamed_key, expected_type=type_hints["renamed_key"])
        return typing.cast("ModifyOperation", jsii.sinvoke(cls, "rename", [original_key, renamed_key]))

    @jsii.member(jsii_name="set")
    @builtins.classmethod
    def set(cls, key: builtins.str, value: builtins.str) -> "ModifyOperation":
        '''Sets a field in the output to a specific value.

        If a field with the same name already exists it will be overridden with
        the specified value.

        :param key: The key name of the field to set.
        :param value: The value to set for the specified field.

        :return: A ModifyOperation object representing the set operation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ModifyOperation.set)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ModifyOperation", jsii.sinvoke(cls, "set", [key, value]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Gets a string representation of the arguments of this operation for use in a Fluent Bit plugin field.

        :return: A fluent bit value string.
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        '''Collection of arguments that apply to the operation.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @builtins.property
    @jsii.member(jsii_name="operation")
    def operation(self) -> builtins.str:
        '''The name of the operation being performed.'''
        return typing.cast(builtins.str, jsii.get(self, "operation"))


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.NamespacedExternalSecretOptions",
    jsii_struct_bases=[ExternalSecretOptions],
    name_mapping={"fields": "fields", "name": "name", "namespace": "namespace"},
)
class NamespacedExternalSecretOptions(ExternalSecretOptions):
    def __init__(
        self,
        *,
        fields: typing.Optional[typing.Sequence[typing.Union["SecretFieldReference", typing.Dict[str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration options for adding a Kubernetes secret synced from an external provider to a specific Kubernetes namespace.

        :param fields: A collection of field mappings that tells the external secrets operator the structure of the Kubernetes secret to create and which how fields in the Kubernetes secret should map to fields in the secret from the external secret provider. Default: The Kubernetes secret will mirror the fields from the secret in the external provider.
        :param name: The name of the Kubernetes secret that will be created, as it will appear from within the Kubernetes cluster. Default: A name will be auto-generated.
        :param namespace: The Kubernetes namespace where the synced secret should be created. Default: 'default'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NamespacedExternalSecretOptions.__init__)
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[str, typing.Any] = {}
        if fields is not None:
            self._values["fields"] = fields
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def fields(self) -> typing.Optional[typing.List["SecretFieldReference"]]:
        '''A collection of field mappings that tells the external secrets operator the structure of the Kubernetes secret to create and which how fields in the Kubernetes secret should map to fields in the secret from the external secret provider.

        :default:

        The Kubernetes secret will mirror the fields from the secret in
        the external provider.
        '''
        result = self._values.get("fields")
        return typing.cast(typing.Optional[typing.List["SecretFieldReference"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the Kubernetes secret that will be created, as it will appear from within the Kubernetes cluster.

        :default: A name will be auto-generated.
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The Kubernetes namespace where the synced secret should be created.

        :default: 'default'
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NamespacedExternalSecretOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(INestFilterOperation)
class NestFilterOperation(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.NestFilterOperation",
):
    '''Operations with exclusive options that can be performed by the Fluent Bit Nest filter plugin.'''

    @jsii.member(jsii_name="lift")
    @builtins.classmethod
    def lift(cls, *, nested_under: builtins.str) -> INestFilterOperation:
        '''
        :param nested_under: Lift records nested under the this key.
        '''
        options = LiftOptions(nested_under=nested_under)

        return typing.cast(INestFilterOperation, jsii.sinvoke(cls, "lift", [options]))

    @jsii.member(jsii_name="nest")
    @builtins.classmethod
    def nest(
        cls,
        *,
        nest_under: builtins.str,
        wildcards: typing.Sequence[builtins.str],
    ) -> INestFilterOperation:
        '''
        :param nest_under: Nest records matching ``wildcard`` under this key.
        :param wildcards: Nest records which field matches this wildcard,.
        '''
        options = NestOptions(nest_under=nest_under, wildcards=wildcards)

        return typing.cast(INestFilterOperation, jsii.sinvoke(cls, "nest", [options]))

    @builtins.property
    @jsii.member(jsii_name="fields")
    def fields(self) -> typing.Mapping[builtins.str, typing.List[builtins.str]]:
        '''The fields representing configuration options for the operation.'''
        return typing.cast(typing.Mapping[builtins.str, typing.List[builtins.str]], jsii.get(self, "fields"))

    @builtins.property
    @jsii.member(jsii_name="operation")
    def operation(self) -> "NestFilterOperationType":
        '''The type of operation to be performed.'''
        return typing.cast("NestFilterOperationType", jsii.get(self, "operation"))


@jsii.enum(jsii_type="cdk-extensions.k8s_aws.NestFilterOperationType")
class NestFilterOperationType(enum.Enum):
    '''The modes that the Fluent Bit Nest filter plugin can work in.'''

    LIFT = "LIFT"
    '''Lift data from a nested object.'''
    NEST = "NEST"
    '''Nest data into a specified object.'''


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.NestOptions",
    jsii_struct_bases=[],
    name_mapping={"nest_under": "nestUnder", "wildcards": "wildcards"},
)
class NestOptions:
    def __init__(
        self,
        *,
        nest_under: builtins.str,
        wildcards: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param nest_under: Nest records matching ``wildcard`` under this key.
        :param wildcards: Nest records which field matches this wildcard,.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NestOptions.__init__)
            check_type(argname="argument nest_under", value=nest_under, expected_type=type_hints["nest_under"])
            check_type(argname="argument wildcards", value=wildcards, expected_type=type_hints["wildcards"])
        self._values: typing.Dict[str, typing.Any] = {
            "nest_under": nest_under,
            "wildcards": wildcards,
        }

    @builtins.property
    def nest_under(self) -> builtins.str:
        '''Nest records matching ``wildcard`` under this key.'''
        result = self._values.get("nest_under")
        assert result is not None, "Required property 'nest_under' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def wildcards(self) -> typing.List[builtins.str]:
        '''Nest records which field matches this wildcard,.'''
        result = self._values.get("wildcards")
        assert result is not None, "Required property 'wildcards' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NestOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IExternalDnsRegistry)
class NoopRegistry(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.NoopRegistry",
):
    '''A placeholder ExternalDNS registry that says ExternalDNS should use not use a registry.

    When configuring ExternalDNS without a registry, the service has no idea the
    original creator and maintainer of DNS records. This means that there are
    likely to be conflicts if there are multiple services that could create or
    change DNS records in the same zone.
    '''

    def __init__(self) -> None:
        '''Creates a new instance of the NoopRegistry class.'''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: constructs.IConstruct) -> ExternalDnsRegistryConfiguration:
        '''Generates an object with all the information needed to use the registry in a given CDK scope.

        :param _scope: The CDK resource that is configuring ExternalDNS.

        :return:

        A configuration object representing the implementation of this
        registry.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NoopRegistry.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(ExternalDnsRegistryConfiguration, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="registryType")
    def registry_type(self) -> builtins.str:
        '''The type name of ExternalDNS registry.'''
        return typing.cast(builtins.str, jsii.get(self, "registryType"))


class OpenSearchOutputBufferSize(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.OpenSearchOutputBufferSize",
):
    '''Represents the size of the OpenSeach output buffer to be used by Fluent Bit.'''

    @jsii.member(jsii_name="bytes")
    @builtins.classmethod
    def bytes(cls, size: _DataSize_d20aaece) -> "OpenSearchOutputBufferSize":
        '''Set the output buffer to a specified data size.

        :param size: The size of the output buffer.

        :return:

        An output buffer size object representing the specified buffer
        size.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(OpenSearchOutputBufferSize.bytes)
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
        return typing.cast("OpenSearchOutputBufferSize", jsii.sinvoke(cls, "bytes", [size]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, value: builtins.str) -> "OpenSearchOutputBufferSize":
        '''An escape hatch that allows an arbitrary value to be set for the OpenSearch buffer output property.

        :param value: The value to use for the OpenSearch buffer output property.

        :return:

        A ``OpenSearchOutputBufferSize`` object representing the passed
        value.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(OpenSearchOutputBufferSize.of)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("OpenSearchOutputBufferSize", jsii.sinvoke(cls, "of", [value]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UNLIMITED")
    def UNLIMITED(cls) -> "OpenSearchOutputBufferSize":
        '''Set the output buffer size to unlimited.'''
        return typing.cast("OpenSearchOutputBufferSize", jsii.sget(cls, "UNLIMITED"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        '''The value to use for the OpenSearch buffer output property.'''
        return typing.cast(builtins.str, jsii.get(self, "value"))


class ParserPluginDataType(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.ParserPluginDataType",
):
    '''Represents the various types of data that can be mapped in Fluent Bit using a parser plugin.'''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, name: builtins.str) -> "ParserPluginDataType":
        '''An escape hatch method that allow specifying arbitrary custom data types.

        :param name: The name of the data type.

        :return: An object representing the data type.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ParserPluginDataType.of)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("ParserPluginDataType", jsii.sinvoke(cls, "of", [name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="BOOL")
    def BOOL(cls) -> "ParserPluginDataType":
        '''Object that is true or false.'''
        return typing.cast("ParserPluginDataType", jsii.sget(cls, "BOOL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="FLOAT")
    def FLOAT(cls) -> "ParserPluginDataType":
        '''Floating point number values.'''
        return typing.cast("ParserPluginDataType", jsii.sget(cls, "FLOAT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HEX")
    def HEX(cls) -> "ParserPluginDataType":
        '''Hexidecimal number values.'''
        return typing.cast("ParserPluginDataType", jsii.sget(cls, "HEX"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="INTEGER")
    def INTEGER(cls) -> "ParserPluginDataType":
        '''While number values.'''
        return typing.cast("ParserPluginDataType", jsii.sget(cls, "INTEGER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LOGFMT")
    def LOGFMT(cls) -> "ParserPluginDataType":
        '''Logfmt formatted data.

        :see: `Golang logfmt documentation <https://pkg.go.dev/github.com/kr/logfmt>`_
        '''
        return typing.cast("ParserPluginDataType", jsii.sget(cls, "LOGFMT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LTSV")
    def LTSV(cls) -> "ParserPluginDataType":
        '''Labeled tab-separated values.

        :see: `LTSV <http://ltsv.org/>`_
        '''
        return typing.cast("ParserPluginDataType", jsii.sget(cls, "LTSV"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REGEX")
    def REGEX(cls) -> "ParserPluginDataType":
        '''Regular expression.'''
        return typing.cast("ParserPluginDataType", jsii.sget(cls, "REGEX"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="STRING")
    def STRING(cls) -> "ParserPluginDataType":
        '''Text data.'''
        return typing.cast("ParserPluginDataType", jsii.sget(cls, "STRING"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the data type.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.ResolvedFluentBitConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "config_file": "configFile",
        "parsers": "parsers",
        "permissions": "permissions",
    },
)
class ResolvedFluentBitConfiguration:
    def __init__(
        self,
        *,
        config_file: builtins.str,
        parsers: typing.Optional[typing.Sequence["IFluentBitParserPlugin"]] = None,
        permissions: typing.Optional[typing.Sequence[aws_cdk.aws_iam.PolicyStatement]] = None,
    ) -> None:
        '''The output of a Fluent Bit configuration object for consumption be the resource configuring Fluent Bit.

        :param config_file: The configuration rended as a configuration file that can be read by the Fluent Bit service.
        :param parsers: A list of parsers referenced by this plugin.
        :param permissions: IAM permissions required by resources that will be using this plugin.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ResolvedFluentBitConfiguration.__init__)
            check_type(argname="argument config_file", value=config_file, expected_type=type_hints["config_file"])
            check_type(argname="argument parsers", value=parsers, expected_type=type_hints["parsers"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
        self._values: typing.Dict[str, typing.Any] = {
            "config_file": config_file,
        }
        if parsers is not None:
            self._values["parsers"] = parsers
        if permissions is not None:
            self._values["permissions"] = permissions

    @builtins.property
    def config_file(self) -> builtins.str:
        '''The configuration rended as a configuration file that can be read by the Fluent Bit service.'''
        result = self._values.get("config_file")
        assert result is not None, "Required property 'config_file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parsers(self) -> typing.Optional[typing.List["IFluentBitParserPlugin"]]:
        '''A list of parsers referenced by this plugin.'''
        result = self._values.get("parsers")
        return typing.cast(typing.Optional[typing.List["IFluentBitParserPlugin"]], result)

    @builtins.property
    def permissions(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        '''IAM permissions required by resources that will be using this plugin.'''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResolvedFluentBitConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.RewriteTagRule",
    jsii_struct_bases=[],
    name_mapping={"keep": "keep", "key": "key", "new_tag": "newTag", "regex": "regex"},
)
class RewriteTagRule:
    def __init__(
        self,
        *,
        keep: builtins.bool,
        key: builtins.str,
        new_tag: builtins.str,
        regex: builtins.str,
    ) -> None:
        '''Defines the matching criteria and the format of the Tag for the rewrite tag Fluent Bit filter plugin.

        :param keep: If a rule matches a rule the filter will emit a copy of the record with the new defined Tag. The property keep takes a boolean value to define if the original record with the old Tag must be preserved and continue in the pipeline or just be discarded.
        :param key: The key represents the name of the record key that holds the value that we want to use to match our regular expression. A key name is specified and prefixed with a ``$``.
        :param new_tag: If a regular expression has matched the value of the defined key in the rule, we are ready to compose a new Tag for that specific record. The tag is a concatenated string that can contain any of the following characters: ``a-z,A-Z,0-9`` and ``.-,``.
        :param regex: Using a simple regular expression we can specify a matching pattern to use against the value of the key specified, also we can take advantage of group capturing to create custom placeholder values.

        :see: `Rules <https://docs.fluentbit.io/manual/pipeline/filters/rewrite-tag#rules>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RewriteTagRule.__init__)
            check_type(argname="argument keep", value=keep, expected_type=type_hints["keep"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument new_tag", value=new_tag, expected_type=type_hints["new_tag"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
        self._values: typing.Dict[str, typing.Any] = {
            "keep": keep,
            "key": key,
            "new_tag": new_tag,
            "regex": regex,
        }

    @builtins.property
    def keep(self) -> builtins.bool:
        '''If a rule matches a rule the filter will emit a copy of the record with the new defined Tag.

        The property keep takes a boolean value to define if the original
        record with the old Tag must be preserved and continue in the pipeline
        or just be discarded.

        :see: `Keep <https://docs.fluentbit.io/manual/pipeline/filters/rewrite-tag#keep>`_
        '''
        result = self._values.get("keep")
        assert result is not None, "Required property 'keep' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''The key represents the name of the record key that holds the value that we want to use to match our regular expression.

        A key name is specified and prefixed with a ``$``.

        :see: `Key <https://docs.fluentbit.io/manual/pipeline/filters/rewrite-tag#key>`_
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def new_tag(self) -> builtins.str:
        '''If a regular expression has matched the value of the defined key in the rule, we are ready to compose a new Tag for that specific record.

        The tag is a concatenated string that can contain any of the following
        characters: ``a-z,A-Z,0-9`` and ``.-,``.

        :see: `New Tag <https://docs.fluentbit.io/manual/pipeline/filters/rewrite-tag#new-tag>`_
        '''
        result = self._values.get("new_tag")
        assert result is not None, "Required property 'new_tag' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def regex(self) -> builtins.str:
        '''Using a simple regular expression we can specify a matching pattern to use against the value of the key specified, also we can take advantage of group capturing to create custom placeholder values.

        :see: `Rubular regex tester <https://rubular.com/>`_
        '''
        result = self._values.get("regex")
        assert result is not None, "Required property 'regex' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RewriteTagRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Route53Dns(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.Route53Dns",
):
    '''External DNS is a Kubernetes service that make Kubernetes resources dicoverable via public DNS servers.

    It retrieves a list of resources
    (Services, Ingresses, etc.) from the Kubernetes API to determine a desired
    list of DNS records and configures DNS providers accordingly.

    The version provided here specifically targets Amazon's Route 53 service and
    all options provded are for configuring Route 53. After being installed
    external-dns will create and manage Route 53 DNS records automatically to
    allow easy network access to your pods and services.

    :see: `Kubernetes SIGs <https://github.com/kubernetes-sigs/external-dns>`_
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster: aws_cdk.aws_eks.ICluster,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        api_retries: typing.Optional[jsii.Number] = None,
        batch_change_size: typing.Optional[jsii.Number] = None,
        domain_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        evaluate_target_health: typing.Optional[builtins.bool] = None,
        log_format: typing.Optional[ExternalDnsLogFormat] = None,
        log_level: typing.Optional[ExternalDnsLogLevel] = None,
        namespace: typing.Optional[builtins.str] = None,
        prefer_cname: typing.Optional[builtins.bool] = None,
        record_ownership_registry: typing.Optional[IExternalDnsRegistry] = None,
        replica_count: typing.Optional[jsii.Number] = None,
        sync_policy: typing.Optional[ExternalDnsSyncPolicy] = None,
        zone_tags: typing.Optional[typing.Sequence[typing.Union[ExternalDnsZoneTag, typing.Dict[str, typing.Any]]]] = None,
        zone_type: typing.Optional[ExternalDnsZoneType] = None,
    ) -> None:
        '''Creates a new instance of the Route53Dns class.

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the resource and used in resource naming. Must be unique within the context of 'scope'.
        :param cluster: The EKS cluster where external-dns should be deployed.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param api_retries: Maximum number of retries for AWS API calls before giving up. Default: 3
        :param batch_change_size: Set the maximum number of changes that will be applied in each batch. Default: 1000
        :param domain_filter: Limits possible target zones by domain suffixes.
        :param evaluate_target_health: Sets a flag determining whether the health of the backend service should be evaluated when determining DNS routing.
        :param log_format: Sets the output format external dns will use when generating logs. Default: {@link ExternalDnsLogLevel.JSON}
        :param log_level: Controls the verbosity of logs generated using the external-dns service. Default: {@link ExternalDnsLogLevel.INFO}
        :param namespace: The Kubernetes namespace where the service should be deployed. Default: 'kube-system'
        :param prefer_cname: When true, alias records will be avoided and CNAME records will be used instead. Default: false
        :param record_ownership_registry: Registry specifying how ExternalDNS should track record ownership. Without a registry to track record ownership, External has no way to know which records it owns and manages and which are owned and managed by a different service. This can cause conflicts if there are multiple instances of External DNS running or if there are other services managing DNS records in similar zones as the different services could try to make conflicting changes due to lacking a shared state. Default: A TXT registry configured with defaults.
        :param replica_count: Desired number of ExternalDNS replicas. Default: 1
        :param sync_policy: Controls the operations ExternalDNS will perform on the records it manages. Default: {@link ExternalDnsSyncPolicy.SYNC}
        :param zone_tags: A set of tags that can be used to restrict which hosted zones external DNS will make changes to.
        :param zone_type: Controls the types of hosted zones external-dns will create records for. Default: ExternalDnsZoneType.ALL
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Route53Dns.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = Route53DnsProps(
            cluster=cluster,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
            api_retries=api_retries,
            batch_change_size=batch_change_size,
            domain_filter=domain_filter,
            evaluate_target_health=evaluate_target_health,
            log_format=log_format,
            log_level=log_level,
            namespace=namespace,
            prefer_cname=prefer_cname,
            record_ownership_registry=record_ownership_registry,
            replica_count=replica_count,
            sync_policy=sync_policy,
            zone_tags=zone_tags,
            zone_type=zone_type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addDomainFilter")
    def add_domain_filter(self, domain: builtins.str) -> "Route53Dns":
        '''Adds a domain to the domain filter list.

        The domain filter list acts as a whitelist for the domains/hosted zones
        which external-dns will manage.

        When domains are added to the domain filter list, external-dns will only
        create and manage records when their domain ends in with a domain that has
        been approved.

        :param domain: The domain to be added to the whitelist.

        :return:

        The external-dns service object that the domain filter was added
        for.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Route53Dns.add_domain_filter)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
        return typing.cast("Route53Dns", jsii.invoke(self, "addDomainFilter", [domain]))

    @jsii.member(jsii_name="addZoneTag")
    def add_zone_tag(self, *, key: builtins.str, value: builtins.str) -> "Route53Dns":
        '''Adds a zone tag filter to the external DNS service.

        When zone tags are provided only Routew 53 Hosted Zones that have matching
        tags will be managed by external DNS.

        :param key: The name of the tag to filter on.
        :param value: The value of the tag to filter on.

        :return: The external-dns service object that the zone tag was added for.
        '''
        tag = ExternalDnsZoneTag(key=key, value=value)

        return typing.cast("Route53Dns", jsii.invoke(self, "addZoneTag", [tag]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CHART_NAME")
    def CHART_NAME(cls) -> builtins.str:
        '''The name of the external-dns Helm chart.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CHART_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CHART_REPOSITORY")
    def CHART_REPOSITORY(cls) -> builtins.str:
        '''The Helm repository providing the chart to be used for installing the external-dns service.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CHART_REPOSITORY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_NAMESPACE")
    def DEFAULT_NAMESPACE(cls) -> builtins.str:
        '''The default Kubernetes namespace where external-dns will be installed if an alternative isn't given as input.'''
        return typing.cast(builtins.str, jsii.sget(cls, "DEFAULT_NAMESPACE"))

    @builtins.property
    @jsii.member(jsii_name="chart")
    def chart(self) -> aws_cdk.aws_eks.HelmChart:
        '''The Helm chart that provides the installation of external-dns.

        :group: Resources
        '''
        return typing.cast(aws_cdk.aws_eks.HelmChart, jsii.get(self, "chart"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_eks.ICluster:
        '''The EKS cluster where external-dns should be deployed.

        :group: Inputs
        '''
        return typing.cast(aws_cdk.aws_eks.ICluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="domainFilter")
    def domain_filter(self) -> typing.List[builtins.str]:
        '''The domain suffixes that control which hosted zones external-dns is allowed to make changes for.

        :group: Inputs
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domainFilter"))

    @builtins.property
    @jsii.member(jsii_name="recordOwnershipRegistry")
    def record_ownership_registry(self) -> IExternalDnsRegistry:
        '''Registry specifying how ExternalDNS should track record ownership.

        Without a registry to track record ownership, External has no way to know
        which records it owns and manages and which are owned and managed by a
        different service.

        This can cause conflicts if there are multiple instances of External DNS
        running or if there are other services managing DNS records in similar
        zones as the different services could try to make conflicting changes due
        to lacking a shared state.

        :group: Inputs
        '''
        return typing.cast(IExternalDnsRegistry, jsii.get(self, "recordOwnershipRegistry"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        '''Override the default region external-dns uses when calling AWS API's.

        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> aws_cdk.aws_eks.ServiceAccount:
        '''The Kubernetes service account that is linked with the IAM Role that allows external-dns to make changes on your behalf.

        :group: Resources
        '''
        return typing.cast(aws_cdk.aws_eks.ServiceAccount, jsii.get(self, "serviceAccount"))

    @builtins.property
    @jsii.member(jsii_name="zoneTags")
    def zone_tags(self) -> typing.List[ExternalDnsZoneTag]:
        '''The AWS tags that control which hosted zones external-dns is allowed to make changes for.

        :group: Inputs
        '''
        return typing.cast(typing.List[ExternalDnsZoneTag], jsii.get(self, "zoneTags"))

    @builtins.property
    @jsii.member(jsii_name="apiRetries")
    def api_retries(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of retries for AWS API calls before giving up.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "apiRetries"))

    @builtins.property
    @jsii.member(jsii_name="batchChangeSize")
    def batch_change_size(self) -> typing.Optional[jsii.Number]:
        '''Set the maximum number of changes that will be applied in each batch.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "batchChangeSize"))

    @builtins.property
    @jsii.member(jsii_name="evaluateTargetHealth")
    def evaluate_target_health(self) -> typing.Optional[builtins.bool]:
        '''Sets a flag determining whether the health of the backend service should be evaluated when determining DNS routing.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "evaluateTargetHealth"))

    @builtins.property
    @jsii.member(jsii_name="logFormat")
    def log_format(self) -> typing.Optional[ExternalDnsLogFormat]:
        '''Sets the output format external dns will use when generating logs.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[ExternalDnsLogFormat], jsii.get(self, "logFormat"))

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> typing.Optional[ExternalDnsLogLevel]:
        '''Controls the verbosity of logs generated using the external-dns service.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[ExternalDnsLogLevel], jsii.get(self, "logLevel"))

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The Kubernetes namespace where the service should be deployed.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespace"))

    @builtins.property
    @jsii.member(jsii_name="preferCname")
    def prefer_cname(self) -> typing.Optional[builtins.bool]:
        '''When true, alias records will be avoided and CNAME records will be used instead.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "preferCname"))

    @builtins.property
    @jsii.member(jsii_name="replicaCount")
    def replica_count(self) -> typing.Optional[jsii.Number]:
        '''Desired number of ExternalDNS replicas.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicaCount"))

    @builtins.property
    @jsii.member(jsii_name="syncPolicy")
    def sync_policy(self) -> typing.Optional[ExternalDnsSyncPolicy]:
        '''Controls the operations ExternalDNS will perform on the records it manages.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[ExternalDnsSyncPolicy], jsii.get(self, "syncPolicy"))

    @builtins.property
    @jsii.member(jsii_name="zoneType")
    def zone_type(self) -> typing.Optional[ExternalDnsZoneType]:
        '''Controls the types of hosted zones external-dns will create records for.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[ExternalDnsZoneType], jsii.get(self, "zoneType"))


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.Route53DnsOptions",
    jsii_struct_bases=[],
    name_mapping={
        "api_retries": "apiRetries",
        "batch_change_size": "batchChangeSize",
        "domain_filter": "domainFilter",
        "evaluate_target_health": "evaluateTargetHealth",
        "log_format": "logFormat",
        "log_level": "logLevel",
        "namespace": "namespace",
        "prefer_cname": "preferCname",
        "record_ownership_registry": "recordOwnershipRegistry",
        "region": "region",
        "replica_count": "replicaCount",
        "sync_policy": "syncPolicy",
        "zone_tags": "zoneTags",
        "zone_type": "zoneType",
    },
)
class Route53DnsOptions:
    def __init__(
        self,
        *,
        api_retries: typing.Optional[jsii.Number] = None,
        batch_change_size: typing.Optional[jsii.Number] = None,
        domain_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        evaluate_target_health: typing.Optional[builtins.bool] = None,
        log_format: typing.Optional[ExternalDnsLogFormat] = None,
        log_level: typing.Optional[ExternalDnsLogLevel] = None,
        namespace: typing.Optional[builtins.str] = None,
        prefer_cname: typing.Optional[builtins.bool] = None,
        record_ownership_registry: typing.Optional[IExternalDnsRegistry] = None,
        region: typing.Optional[builtins.str] = None,
        replica_count: typing.Optional[jsii.Number] = None,
        sync_policy: typing.Optional[ExternalDnsSyncPolicy] = None,
        zone_tags: typing.Optional[typing.Sequence[typing.Union[ExternalDnsZoneTag, typing.Dict[str, typing.Any]]]] = None,
        zone_type: typing.Optional[ExternalDnsZoneType] = None,
    ) -> None:
        '''Optional configuration for the Route53Dns resource.

        :param api_retries: Maximum number of retries for AWS API calls before giving up. Default: 3
        :param batch_change_size: Set the maximum number of changes that will be applied in each batch. Default: 1000
        :param domain_filter: Limits possible target zones by domain suffixes.
        :param evaluate_target_health: Sets a flag determining whether the health of the backend service should be evaluated when determining DNS routing.
        :param log_format: Sets the output format external dns will use when generating logs. Default: {@link ExternalDnsLogLevel.JSON}
        :param log_level: Controls the verbosity of logs generated using the external-dns service. Default: {@link ExternalDnsLogLevel.INFO}
        :param namespace: The Kubernetes namespace where the service should be deployed. Default: 'kube-system'
        :param prefer_cname: When true, alias records will be avoided and CNAME records will be used instead. Default: false
        :param record_ownership_registry: Registry specifying how ExternalDNS should track record ownership. Without a registry to track record ownership, External has no way to know which records it owns and manages and which are owned and managed by a different service. This can cause conflicts if there are multiple instances of External DNS running or if there are other services managing DNS records in similar zones as the different services could try to make conflicting changes due to lacking a shared state. Default: A TXT registry configured with defaults.
        :param region: Override the default region external-dns uses when calling AWS API's.
        :param replica_count: Desired number of ExternalDNS replicas. Default: 1
        :param sync_policy: Controls the operations ExternalDNS will perform on the records it manages. Default: {@link ExternalDnsSyncPolicy.SYNC}
        :param zone_tags: A set of tags that can be used to restrict which hosted zones external DNS will make changes to.
        :param zone_type: Controls the types of hosted zones external-dns will create records for. Default: ExternalDnsZoneType.ALL
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Route53DnsOptions.__init__)
            check_type(argname="argument api_retries", value=api_retries, expected_type=type_hints["api_retries"])
            check_type(argname="argument batch_change_size", value=batch_change_size, expected_type=type_hints["batch_change_size"])
            check_type(argname="argument domain_filter", value=domain_filter, expected_type=type_hints["domain_filter"])
            check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
            check_type(argname="argument log_format", value=log_format, expected_type=type_hints["log_format"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument prefer_cname", value=prefer_cname, expected_type=type_hints["prefer_cname"])
            check_type(argname="argument record_ownership_registry", value=record_ownership_registry, expected_type=type_hints["record_ownership_registry"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument replica_count", value=replica_count, expected_type=type_hints["replica_count"])
            check_type(argname="argument sync_policy", value=sync_policy, expected_type=type_hints["sync_policy"])
            check_type(argname="argument zone_tags", value=zone_tags, expected_type=type_hints["zone_tags"])
            check_type(argname="argument zone_type", value=zone_type, expected_type=type_hints["zone_type"])
        self._values: typing.Dict[str, typing.Any] = {}
        if api_retries is not None:
            self._values["api_retries"] = api_retries
        if batch_change_size is not None:
            self._values["batch_change_size"] = batch_change_size
        if domain_filter is not None:
            self._values["domain_filter"] = domain_filter
        if evaluate_target_health is not None:
            self._values["evaluate_target_health"] = evaluate_target_health
        if log_format is not None:
            self._values["log_format"] = log_format
        if log_level is not None:
            self._values["log_level"] = log_level
        if namespace is not None:
            self._values["namespace"] = namespace
        if prefer_cname is not None:
            self._values["prefer_cname"] = prefer_cname
        if record_ownership_registry is not None:
            self._values["record_ownership_registry"] = record_ownership_registry
        if region is not None:
            self._values["region"] = region
        if replica_count is not None:
            self._values["replica_count"] = replica_count
        if sync_policy is not None:
            self._values["sync_policy"] = sync_policy
        if zone_tags is not None:
            self._values["zone_tags"] = zone_tags
        if zone_type is not None:
            self._values["zone_type"] = zone_type

    @builtins.property
    def api_retries(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of retries for AWS API calls before giving up.

        :default: 3
        '''
        result = self._values.get("api_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def batch_change_size(self) -> typing.Optional[jsii.Number]:
        '''Set the maximum number of changes that will be applied in each batch.

        :default: 1000
        '''
        result = self._values.get("batch_change_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def domain_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Limits possible target zones by domain suffixes.'''
        result = self._values.get("domain_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def evaluate_target_health(self) -> typing.Optional[builtins.bool]:
        '''Sets a flag determining whether the health of the backend service should be evaluated when determining DNS routing.'''
        result = self._values.get("evaluate_target_health")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def log_format(self) -> typing.Optional[ExternalDnsLogFormat]:
        '''Sets the output format external dns will use when generating logs.

        :default: {@link ExternalDnsLogLevel.JSON}
        '''
        result = self._values.get("log_format")
        return typing.cast(typing.Optional[ExternalDnsLogFormat], result)

    @builtins.property
    def log_level(self) -> typing.Optional[ExternalDnsLogLevel]:
        '''Controls the verbosity of logs generated using the external-dns service.

        :default: {@link ExternalDnsLogLevel.INFO}
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[ExternalDnsLogLevel], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The Kubernetes namespace where the service should be deployed.

        :default: 'kube-system'
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefer_cname(self) -> typing.Optional[builtins.bool]:
        '''When true, alias records will be avoided and CNAME records will be used instead.

        :default: false
        '''
        result = self._values.get("prefer_cname")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def record_ownership_registry(self) -> typing.Optional[IExternalDnsRegistry]:
        '''Registry specifying how ExternalDNS should track record ownership.

        Without a registry to track record ownership, External has no way to know
        which records it owns and manages and which are owned and managed by a
        different service.

        This can cause conflicts if there are multiple instances of External DNS
        running or if there are other services managing DNS records in similar
        zones as the different services could try to make conflicting changes due
        to lacking a shared state.

        :default: A TXT registry configured with defaults.
        '''
        result = self._values.get("record_ownership_registry")
        return typing.cast(typing.Optional[IExternalDnsRegistry], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Override the default region external-dns uses when calling AWS API's.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replica_count(self) -> typing.Optional[jsii.Number]:
        '''Desired number of ExternalDNS replicas.

        :default: 1
        '''
        result = self._values.get("replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sync_policy(self) -> typing.Optional[ExternalDnsSyncPolicy]:
        '''Controls the operations ExternalDNS will perform on the records it manages.

        :default: {@link ExternalDnsSyncPolicy.SYNC}
        '''
        result = self._values.get("sync_policy")
        return typing.cast(typing.Optional[ExternalDnsSyncPolicy], result)

    @builtins.property
    def zone_tags(self) -> typing.Optional[typing.List[ExternalDnsZoneTag]]:
        '''A set of tags that can be used to restrict which hosted zones external DNS will make changes to.'''
        result = self._values.get("zone_tags")
        return typing.cast(typing.Optional[typing.List[ExternalDnsZoneTag]], result)

    @builtins.property
    def zone_type(self) -> typing.Optional[ExternalDnsZoneType]:
        '''Controls the types of hosted zones external-dns will create records for.

        :default: ExternalDnsZoneType.ALL
        '''
        result = self._values.get("zone_type")
        return typing.cast(typing.Optional[ExternalDnsZoneType], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Route53DnsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.Route53DnsProps",
    jsii_struct_bases=[aws_cdk.ResourceProps, Route53DnsOptions],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "api_retries": "apiRetries",
        "batch_change_size": "batchChangeSize",
        "domain_filter": "domainFilter",
        "evaluate_target_health": "evaluateTargetHealth",
        "log_format": "logFormat",
        "log_level": "logLevel",
        "namespace": "namespace",
        "prefer_cname": "preferCname",
        "record_ownership_registry": "recordOwnershipRegistry",
        "replica_count": "replicaCount",
        "sync_policy": "syncPolicy",
        "zone_tags": "zoneTags",
        "zone_type": "zoneType",
        "cluster": "cluster",
    },
)
class Route53DnsProps(aws_cdk.ResourceProps, Route53DnsOptions):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        api_retries: typing.Optional[jsii.Number] = None,
        batch_change_size: typing.Optional[jsii.Number] = None,
        domain_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        evaluate_target_health: typing.Optional[builtins.bool] = None,
        log_format: typing.Optional[ExternalDnsLogFormat] = None,
        log_level: typing.Optional[ExternalDnsLogLevel] = None,
        namespace: typing.Optional[builtins.str] = None,
        prefer_cname: typing.Optional[builtins.bool] = None,
        record_ownership_registry: typing.Optional[IExternalDnsRegistry] = None,
        replica_count: typing.Optional[jsii.Number] = None,
        sync_policy: typing.Optional[ExternalDnsSyncPolicy] = None,
        zone_tags: typing.Optional[typing.Sequence[typing.Union[ExternalDnsZoneTag, typing.Dict[str, typing.Any]]]] = None,
        zone_type: typing.Optional[ExternalDnsZoneType] = None,
        cluster: aws_cdk.aws_eks.ICluster,
    ) -> None:
        '''Full configuration for the Route53Dns resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: Override the default region external-dns uses when calling AWS API's.
        :param api_retries: Maximum number of retries for AWS API calls before giving up. Default: 3
        :param batch_change_size: Set the maximum number of changes that will be applied in each batch. Default: 1000
        :param domain_filter: Limits possible target zones by domain suffixes.
        :param evaluate_target_health: Sets a flag determining whether the health of the backend service should be evaluated when determining DNS routing.
        :param log_format: Sets the output format external dns will use when generating logs. Default: {@link ExternalDnsLogLevel.JSON}
        :param log_level: Controls the verbosity of logs generated using the external-dns service. Default: {@link ExternalDnsLogLevel.INFO}
        :param namespace: The Kubernetes namespace where the service should be deployed. Default: 'kube-system'
        :param prefer_cname: When true, alias records will be avoided and CNAME records will be used instead. Default: false
        :param record_ownership_registry: Registry specifying how ExternalDNS should track record ownership. Without a registry to track record ownership, External has no way to know which records it owns and manages and which are owned and managed by a different service. This can cause conflicts if there are multiple instances of External DNS running or if there are other services managing DNS records in similar zones as the different services could try to make conflicting changes due to lacking a shared state. Default: A TXT registry configured with defaults.
        :param replica_count: Desired number of ExternalDNS replicas. Default: 1
        :param sync_policy: Controls the operations ExternalDNS will perform on the records it manages. Default: {@link ExternalDnsSyncPolicy.SYNC}
        :param zone_tags: A set of tags that can be used to restrict which hosted zones external DNS will make changes to.
        :param zone_type: Controls the types of hosted zones external-dns will create records for. Default: ExternalDnsZoneType.ALL
        :param cluster: The EKS cluster where external-dns should be deployed.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Route53DnsProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument api_retries", value=api_retries, expected_type=type_hints["api_retries"])
            check_type(argname="argument batch_change_size", value=batch_change_size, expected_type=type_hints["batch_change_size"])
            check_type(argname="argument domain_filter", value=domain_filter, expected_type=type_hints["domain_filter"])
            check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
            check_type(argname="argument log_format", value=log_format, expected_type=type_hints["log_format"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument prefer_cname", value=prefer_cname, expected_type=type_hints["prefer_cname"])
            check_type(argname="argument record_ownership_registry", value=record_ownership_registry, expected_type=type_hints["record_ownership_registry"])
            check_type(argname="argument replica_count", value=replica_count, expected_type=type_hints["replica_count"])
            check_type(argname="argument sync_policy", value=sync_policy, expected_type=type_hints["sync_policy"])
            check_type(argname="argument zone_tags", value=zone_tags, expected_type=type_hints["zone_tags"])
            check_type(argname="argument zone_type", value=zone_type, expected_type=type_hints["zone_type"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if api_retries is not None:
            self._values["api_retries"] = api_retries
        if batch_change_size is not None:
            self._values["batch_change_size"] = batch_change_size
        if domain_filter is not None:
            self._values["domain_filter"] = domain_filter
        if evaluate_target_health is not None:
            self._values["evaluate_target_health"] = evaluate_target_health
        if log_format is not None:
            self._values["log_format"] = log_format
        if log_level is not None:
            self._values["log_level"] = log_level
        if namespace is not None:
            self._values["namespace"] = namespace
        if prefer_cname is not None:
            self._values["prefer_cname"] = prefer_cname
        if record_ownership_registry is not None:
            self._values["record_ownership_registry"] = record_ownership_registry
        if replica_count is not None:
            self._values["replica_count"] = replica_count
        if sync_policy is not None:
            self._values["sync_policy"] = sync_policy
        if zone_tags is not None:
            self._values["zone_tags"] = zone_tags
        if zone_type is not None:
            self._values["zone_type"] = zone_type

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Override the default region external-dns uses when calling AWS API's.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_retries(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of retries for AWS API calls before giving up.

        :default: 3
        '''
        result = self._values.get("api_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def batch_change_size(self) -> typing.Optional[jsii.Number]:
        '''Set the maximum number of changes that will be applied in each batch.

        :default: 1000
        '''
        result = self._values.get("batch_change_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def domain_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Limits possible target zones by domain suffixes.'''
        result = self._values.get("domain_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def evaluate_target_health(self) -> typing.Optional[builtins.bool]:
        '''Sets a flag determining whether the health of the backend service should be evaluated when determining DNS routing.'''
        result = self._values.get("evaluate_target_health")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def log_format(self) -> typing.Optional[ExternalDnsLogFormat]:
        '''Sets the output format external dns will use when generating logs.

        :default: {@link ExternalDnsLogLevel.JSON}
        '''
        result = self._values.get("log_format")
        return typing.cast(typing.Optional[ExternalDnsLogFormat], result)

    @builtins.property
    def log_level(self) -> typing.Optional[ExternalDnsLogLevel]:
        '''Controls the verbosity of logs generated using the external-dns service.

        :default: {@link ExternalDnsLogLevel.INFO}
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[ExternalDnsLogLevel], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The Kubernetes namespace where the service should be deployed.

        :default: 'kube-system'
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefer_cname(self) -> typing.Optional[builtins.bool]:
        '''When true, alias records will be avoided and CNAME records will be used instead.

        :default: false
        '''
        result = self._values.get("prefer_cname")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def record_ownership_registry(self) -> typing.Optional[IExternalDnsRegistry]:
        '''Registry specifying how ExternalDNS should track record ownership.

        Without a registry to track record ownership, External has no way to know
        which records it owns and manages and which are owned and managed by a
        different service.

        This can cause conflicts if there are multiple instances of External DNS
        running or if there are other services managing DNS records in similar
        zones as the different services could try to make conflicting changes due
        to lacking a shared state.

        :default: A TXT registry configured with defaults.
        '''
        result = self._values.get("record_ownership_registry")
        return typing.cast(typing.Optional[IExternalDnsRegistry], result)

    @builtins.property
    def replica_count(self) -> typing.Optional[jsii.Number]:
        '''Desired number of ExternalDNS replicas.

        :default: 1
        '''
        result = self._values.get("replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sync_policy(self) -> typing.Optional[ExternalDnsSyncPolicy]:
        '''Controls the operations ExternalDNS will perform on the records it manages.

        :default: {@link ExternalDnsSyncPolicy.SYNC}
        '''
        result = self._values.get("sync_policy")
        return typing.cast(typing.Optional[ExternalDnsSyncPolicy], result)

    @builtins.property
    def zone_tags(self) -> typing.Optional[typing.List[ExternalDnsZoneTag]]:
        '''A set of tags that can be used to restrict which hosted zones external DNS will make changes to.'''
        result = self._values.get("zone_tags")
        return typing.cast(typing.Optional[typing.List[ExternalDnsZoneTag]], result)

    @builtins.property
    def zone_type(self) -> typing.Optional[ExternalDnsZoneType]:
        '''Controls the types of hosted zones external-dns will create records for.

        :default: ExternalDnsZoneType.ALL
        '''
        result = self._values.get("zone_type")
        return typing.cast(typing.Optional[ExternalDnsZoneType], result)

    @builtins.property
    def cluster(self) -> aws_cdk.aws_eks.ICluster:
        '''The EKS cluster where external-dns should be deployed.'''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_eks.ICluster, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Route53DnsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.SecretFieldReference",
    jsii_struct_bases=[],
    name_mapping={
        "kubernetes_key": "kubernetesKey",
        "metadata_policy": "metadataPolicy",
        "remote_key": "remoteKey",
    },
)
class SecretFieldReference:
    def __init__(
        self,
        *,
        kubernetes_key: builtins.str,
        metadata_policy: typing.Optional[MetadataPolicy] = None,
        remote_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Options for how to synchronize a specific field in a secret being imported.

        :param kubernetes_key: The name of the data key to be used for the field in the imported Kubernetes secret.
        :param metadata_policy: Policy for fetching tags/labels from provider secrets.
        :param remote_key: The JSON key for the field in the secret being imported.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SecretFieldReference.__init__)
            check_type(argname="argument kubernetes_key", value=kubernetes_key, expected_type=type_hints["kubernetes_key"])
            check_type(argname="argument metadata_policy", value=metadata_policy, expected_type=type_hints["metadata_policy"])
            check_type(argname="argument remote_key", value=remote_key, expected_type=type_hints["remote_key"])
        self._values: typing.Dict[str, typing.Any] = {
            "kubernetes_key": kubernetes_key,
        }
        if metadata_policy is not None:
            self._values["metadata_policy"] = metadata_policy
        if remote_key is not None:
            self._values["remote_key"] = remote_key

    @builtins.property
    def kubernetes_key(self) -> builtins.str:
        '''The name of the data key to be used for the field in the imported Kubernetes secret.'''
        result = self._values.get("kubernetes_key")
        assert result is not None, "Required property 'kubernetes_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metadata_policy(self) -> typing.Optional[MetadataPolicy]:
        '''Policy for fetching tags/labels from provider secrets.'''
        result = self._values.get("metadata_policy")
        return typing.cast(typing.Optional[MetadataPolicy], result)

    @builtins.property
    def remote_key(self) -> typing.Optional[builtins.str]:
        '''The JSON key for the field in the secret being imported.'''
        result = self._values.get("remote_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretFieldReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.SecretReferenceConfiguration",
    jsii_struct_bases=[],
    name_mapping={"remote_ref": "remoteRef", "fields": "fields"},
)
class SecretReferenceConfiguration:
    def __init__(
        self,
        *,
        remote_ref: builtins.str,
        fields: typing.Optional[typing.Sequence[typing.Union[SecretFieldReference, typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''Configuration detailing how secrets are to be synchronized.

        :param remote_ref: The ID of the secret to be imported from the provider.
        :param fields: A mapping of fields and per field options to use when synchronizing a secret from a provider.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SecretReferenceConfiguration.__init__)
            check_type(argname="argument remote_ref", value=remote_ref, expected_type=type_hints["remote_ref"])
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
        self._values: typing.Dict[str, typing.Any] = {
            "remote_ref": remote_ref,
        }
        if fields is not None:
            self._values["fields"] = fields

    @builtins.property
    def remote_ref(self) -> builtins.str:
        '''The ID of the secret to be imported from the provider.'''
        result = self._values.get("remote_ref")
        assert result is not None, "Required property 'remote_ref' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fields(self) -> typing.Optional[typing.List[SecretFieldReference]]:
        '''A mapping of fields and per field options to use when synchronizing a secret from a provider.'''
        result = self._values.get("fields")
        return typing.cast(typing.Optional[typing.List[SecretFieldReference]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretReferenceConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISecretReference)
class SecretsManagerReference(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.SecretsManagerReference",
):
    '''Defines a reference for importing and synchronizing a Secrets Manager secret to a Kubernetes secret.'''

    def __init__(
        self,
        secret: aws_cdk.aws_secretsmanager.ISecret,
        *,
        fields: typing.Optional[typing.Sequence[typing.Union[SecretFieldReference, typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''Creates a new instance of the SecretsManagerReference class.

        :param secret: The secret being referenced to import into Kubernetes.
        :param fields: Defines a mapping of how JSON keys in the Secrets Manager secret should appear in the imported Kubernetes secret.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SecretsManagerReference.__init__)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        options = SecretsManagerReferenceOptions(fields=fields)

        jsii.create(self.__class__, self, [secret, options])

    @jsii.member(jsii_name="addFieldMapping")
    def add_field_mapping(
        self,
        *,
        kubernetes_key: builtins.str,
        metadata_policy: typing.Optional[MetadataPolicy] = None,
        remote_key: typing.Optional[builtins.str] = None,
    ) -> "SecretsManagerReference":
        '''Adds a field mapping that specifies how a field from a Secrets Manager JSON secret should be mapped into the imported Kubernetes secret.

        :param kubernetes_key: The name of the data key to be used for the field in the imported Kubernetes secret.
        :param metadata_policy: Policy for fetching tags/labels from provider secrets.
        :param remote_key: The JSON key for the field in the secret being imported.

        :return: The ``SecretsManagerReference`` where the mapping was added.
        '''
        field = SecretFieldReference(
            kubernetes_key=kubernetes_key,
            metadata_policy=metadata_policy,
            remote_key=remote_key,
        )

        return typing.cast("SecretsManagerReference", jsii.invoke(self, "addFieldMapping", [field]))

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: constructs.IConstruct) -> SecretReferenceConfiguration:
        '''Binds the reference to an object that is in charge of generating the manifest for the external secret.

        :param _scope: The construct that will consume the generated configuration.

        :return:

        A configuration object providing the details needed to build
        the external secret Kubernetes resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SecretsManagerReference.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(SecretReferenceConfiguration, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="fields")
    def fields(self) -> typing.List[SecretFieldReference]:
        '''An array of field mappings which will be applied to this secret reference when mapping keys from SecretsManager JSON objects to keys in the imported secret.'''
        return typing.cast(typing.List[SecretFieldReference], jsii.get(self, "fields"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''The secret being referenced to import into Kubernetes.'''
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, jsii.get(self, "secret"))


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.SecretsManagerReferenceOptions",
    jsii_struct_bases=[],
    name_mapping={"fields": "fields"},
)
class SecretsManagerReferenceOptions:
    def __init__(
        self,
        *,
        fields: typing.Optional[typing.Sequence[typing.Union[SecretFieldReference, typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''Configuration options for referencing a Secrets Manager secret as a Kubernetes secret.

        :param fields: Defines a mapping of how JSON keys in the Secrets Manager secret should appear in the imported Kubernetes secret.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SecretsManagerReferenceOptions.__init__)
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
        self._values: typing.Dict[str, typing.Any] = {}
        if fields is not None:
            self._values["fields"] = fields

    @builtins.property
    def fields(self) -> typing.Optional[typing.List[SecretFieldReference]]:
        '''Defines a mapping of how JSON keys in the Secrets Manager secret should appear in the imported Kubernetes secret.'''
        result = self._values.get("fields")
        return typing.cast(typing.Optional[typing.List[SecretFieldReference]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretsManagerReferenceOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.SecretsManagerSecretStoreProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "cluster": "cluster",
        "name": "name",
        "namespace": "namespace",
    },
)
class SecretsManagerSecretStoreProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        cluster: aws_cdk.aws_eks.ICluster,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration options for adding a new secret store resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param cluster: The EKS cluster where the secret store should be created.
        :param name: A human friendly name for the secret store.
        :param namespace: The Kubernetes namespace where the secret store should be created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SecretsManagerSecretStoreProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster(self) -> aws_cdk.aws_eks.ICluster:
        '''The EKS cluster where the secret store should be created.'''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_eks.ICluster, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A human friendly name for the secret store.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The Kubernetes namespace where the secret store should be created.'''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretsManagerSecretStoreProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISecretReference)
class SsmParameterReference(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.SsmParameterReference",
):
    '''Defines a reference for importing and synchronizing an SSM parameter to a Kubernetes secret.'''

    def __init__(
        self,
        parameter: aws_cdk.aws_ssm.IParameter,
        *,
        fields: typing.Optional[typing.Sequence[typing.Union[SecretFieldReference, typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''Creates a new instance of the SsmParameterReference class.

        :param parameter: The SSM parameter being referenced to import into Kubernetes.
        :param fields: Defines a mapping of how JSON keys in the SSM parameter should appear in the imported Kubernetes secret.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SsmParameterReference.__init__)
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
        options = SsmParameterReferenceOptions(fields=fields)

        jsii.create(self.__class__, self, [parameter, options])

    @jsii.member(jsii_name="addFieldMapping")
    def add_field_mapping(
        self,
        *,
        kubernetes_key: builtins.str,
        metadata_policy: typing.Optional[MetadataPolicy] = None,
        remote_key: typing.Optional[builtins.str] = None,
    ) -> "SsmParameterReference":
        '''Adds a field mapping that specifies how a field from an SSM JSON parameter should be mapped into the imported Kubernetes secret.

        :param kubernetes_key: The name of the data key to be used for the field in the imported Kubernetes secret.
        :param metadata_policy: Policy for fetching tags/labels from provider secrets.
        :param remote_key: The JSON key for the field in the secret being imported.

        :return: The ``SsmParameterReference`` where the mapping was added.
        '''
        field = SecretFieldReference(
            kubernetes_key=kubernetes_key,
            metadata_policy=metadata_policy,
            remote_key=remote_key,
        )

        return typing.cast("SsmParameterReference", jsii.invoke(self, "addFieldMapping", [field]))

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: constructs.IConstruct) -> SecretReferenceConfiguration:
        '''Binds the reference to an object that is in charge of generating the manifest for the external secret.

        :param _scope: The construct that will consume the generated configuration.

        :return:

        A configuration object providing the details needed to build
        the external secret Kubernetes resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SsmParameterReference.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(SecretReferenceConfiguration, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="fields")
    def fields(self) -> typing.List[SecretFieldReference]:
        '''An array of field mappings which will be applied to this secret reference when mapping keys from SSM parameter JSON objects to keys in the imported secret.'''
        return typing.cast(typing.List[SecretFieldReference], jsii.get(self, "fields"))

    @builtins.property
    @jsii.member(jsii_name="parameter")
    def parameter(self) -> aws_cdk.aws_ssm.IParameter:
        '''The SSM parameter being referenced to import into Kubernetes.'''
        return typing.cast(aws_cdk.aws_ssm.IParameter, jsii.get(self, "parameter"))


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.SsmParameterReferenceOptions",
    jsii_struct_bases=[],
    name_mapping={"fields": "fields"},
)
class SsmParameterReferenceOptions:
    def __init__(
        self,
        *,
        fields: typing.Optional[typing.Sequence[typing.Union[SecretFieldReference, typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''Configuration options for referencing an SSM parameter as a Kubernetes secret.

        :param fields: Defines a mapping of how JSON keys in the SSM parameter should appear in the imported Kubernetes secret.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SsmParameterReferenceOptions.__init__)
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
        self._values: typing.Dict[str, typing.Any] = {}
        if fields is not None:
            self._values["fields"] = fields

    @builtins.property
    def fields(self) -> typing.Optional[typing.List[SecretFieldReference]]:
        '''Defines a mapping of how JSON keys in the SSM parameter should appear in the imported Kubernetes secret.'''
        result = self._values.get("fields")
        return typing.cast(typing.Optional[typing.List[SecretFieldReference]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmParameterReferenceOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.SsmParameterSecretStoreProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "cluster": "cluster",
        "name": "name",
        "namespace": "namespace",
    },
)
class SsmParameterSecretStoreProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        cluster: aws_cdk.aws_eks.ICluster,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration options for adding a new secret store resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param cluster: The EKS cluster where the secret store should be created.
        :param name: A human friendly name for the secret store.
        :param namespace: The Kubernetes namespace where the secret store should be created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SsmParameterSecretStoreProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster(self) -> aws_cdk.aws_eks.ICluster:
        '''The EKS cluster where the secret store should be created.'''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_eks.ICluster, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A human friendly name for the secret store.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The Kubernetes namespace where the secret store should be created.'''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsmParameterSecretStoreProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IExternalDnsRegistry)
class TxtRegistry(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.TxtRegistry",
):
    '''An ExternalDNS registry that tracks DNS record ownership information using DNS TXT records.

    :see: `About TXT records <https://support.google.com/a/answer/2716800?hl=en>`_
    '''

    def __init__(
        self,
        *,
        owner_id: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the NoopRegistry class.

        :param owner_id: A unique identifier that is used to establish ownership of managed DNS records. Prevents conflicts in the event of multiple clusters running external-dns. Default: Unique address of the owning CDK node.
        :param prefix: A prefix to be added top TXT ownership records. By default, the ownership record is a TXT record with the same name as the managed record that was created. This causes issues as some record types (CNAME's) do not allow duplicate records of a different type. This prefix is used to prevent such name collissions while still allowing DNS ownership records to be created. Default: 'edns.''
        '''
        options = TxtRegistryOptions(owner_id=owner_id, prefix=prefix)

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> ExternalDnsRegistryConfiguration:
        '''Generates an object with all the information needed to use the registry in a given CDK scope.

        :param scope: The CDK resource that is configuring ExternalDNS.

        :return:

        A configuration object representing the implementation of this
        registry.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TxtRegistry.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(ExternalDnsRegistryConfiguration, jsii.invoke(self, "bind", [scope]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_PREFIX")
    def DEFAULT_PREFIX(cls) -> builtins.str:
        '''The default prefix to append to TXT ownership records creates for the registry.'''
        return typing.cast(builtins.str, jsii.sget(cls, "DEFAULT_PREFIX"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NO_PREFIX")
    def NO_PREFIX(cls) -> builtins.str:
        '''A special value that specifies ExternalDNS should not use any prefix when creating TXT ownership records.

        This is not recommended as it is likely to cause issues with record
        creation and management with some record types that do not allow other
        records with the same name and different types to exist (CNAME's).

        However, if this behavior is desired this value can be passed as the
        prefix to override the default behavior with will set a prefix if none
        is provided as input.
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "NO_PREFIX"))

    @builtins.property
    @jsii.member(jsii_name="registryType")
    def registry_type(self) -> builtins.str:
        '''The type name of ExternalDNS registry.'''
        return typing.cast(builtins.str, jsii.get(self, "registryType"))

    @builtins.property
    @jsii.member(jsii_name="ownerId")
    def owner_id(self) -> typing.Optional[builtins.str]:
        '''A unique identifier that is used to establish ownership of managed DNS records.

        Prevents conflicts in the event of multiple clusters running external-dns.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerId"))

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> typing.Optional[builtins.str]:
        '''A prefix to be added top TXT ownership records.

        By default, the ownership record is a TXT record with the same name as the
        managed record that was created. This causes issues as some record types
        (CNAME's) do not allow duplicate records of a different type.

        This prefix is used to prevent such name collissions while still allowing
        DNS ownership records to be created.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefix"))


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.TxtRegistryOptions",
    jsii_struct_bases=[],
    name_mapping={"owner_id": "ownerId", "prefix": "prefix"},
)
class TxtRegistryOptions:
    def __init__(
        self,
        *,
        owner_id: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration options for setting up a TXT registry for ExternalDNS.

        :param owner_id: A unique identifier that is used to establish ownership of managed DNS records. Prevents conflicts in the event of multiple clusters running external-dns. Default: Unique address of the owning CDK node.
        :param prefix: A prefix to be added top TXT ownership records. By default, the ownership record is a TXT record with the same name as the managed record that was created. This causes issues as some record types (CNAME's) do not allow duplicate records of a different type. This prefix is used to prevent such name collissions while still allowing DNS ownership records to be created. Default: 'edns.''
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TxtRegistryOptions.__init__)
            check_type(argname="argument owner_id", value=owner_id, expected_type=type_hints["owner_id"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[str, typing.Any] = {}
        if owner_id is not None:
            self._values["owner_id"] = owner_id
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def owner_id(self) -> typing.Optional[builtins.str]:
        '''A unique identifier that is used to establish ownership of managed DNS records.

        Prevents conflicts in the event of multiple clusters running external-dns.

        :default: Unique address of the owning CDK node.
        '''
        result = self._values.get("owner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''A prefix to be added top TXT ownership records.

        By default, the ownership record is a TXT record with the same name as the
        managed record that was created. This causes issues as some record types
        (CNAME's) do not allow duplicate records of a different type.

        This prefix is used to prevent such name collissions while still allowing
        DNS ownership records to be created.

        :default: 'edns.''
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TxtRegistryOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISecretStore)
class AwsSecretStore(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.AwsSecretStore",
):
    '''A generic class representing secret store that is backed by an AWS service.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster: aws_cdk.aws_eks.ICluster,
        service: builtins.str,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the AwsSecretStore class.

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the resource and used in resource naming. Must be unique within the context of 'scope'.
        :param cluster: The EKS cluster where the secret store should be created.
        :param service: The name of the service provider backing the secret store.
        :param name: A human friendly name for the secret store.
        :param namespace: The Kubernetes namespace where the secret store should be created.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AwsSecretStore.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AwsSecretStoreProps(
            cluster=cluster,
            service=service,
            name=name,
            namespace=namespace,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="NAME_VALIDATOR_REGEX")
    def NAME_VALIDATOR_REGEX(cls) -> builtins.str:
        '''The regex pattern used to validate secret store names.'''
        return typing.cast(builtins.str, jsii.sget(cls, "NAME_VALIDATOR_REGEX"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_eks.ICluster:
        '''The EKS cluster where the secret store should be created.

        :group: Inputs
        '''
        return typing.cast(aws_cdk.aws_eks.ICluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> aws_cdk.aws_eks.KubernetesManifest:
        '''The Kubernetes manifest that defines the secret store.

        :group: Resources
        '''
        return typing.cast(aws_cdk.aws_eks.KubernetesManifest, jsii.get(self, "manifest"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A human friendly name for the secret store.

        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        '''The Kubernetes namespace where the secret store should be created.

        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @builtins.property
    @jsii.member(jsii_name="secretStoreName")
    def secret_store_name(self) -> builtins.str:
        '''The name of the secret store as it appears in Kubernetes.'''
        return typing.cast(builtins.str, jsii.get(self, "secretStoreName"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        '''The name of the service provider backing the secret store.

        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> aws_cdk.aws_eks.ServiceAccount:
        '''A Kubernetes service account mapped to an IAM role that provides the necessary permissions to sychronize secrets from an AWS rpvoder.

        :group: Resources
        '''
        return typing.cast(aws_cdk.aws_eks.ServiceAccount, jsii.get(self, "serviceAccount"))


@jsii.implements(IExternalDnsRegistry)
class AwsServiceDiscoveryRegistry(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.AwsServiceDiscoveryRegistry",
):
    '''An ExternalDNS registry that tracks DNS record ownership information using AWS Service Discovery.

    :see: `AWS Cloud Map <https://docs.aws.amazon.com/cloud-map/latest/dg/what-is-cloud-map.html>`_
    '''

    def __init__(self) -> None:
        '''Creates a new instance of the AwsServiceDiscoveryRegistry class.'''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> ExternalDnsRegistryConfiguration:
        '''Generates an object with all the information needed to use the registry in a given CDK scope.

        :param scope: The CDK resource that is configuring ExternalDNS.

        :return:

        A configuration object representing the implementation of this
        registry.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AwsServiceDiscoveryRegistry.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(ExternalDnsRegistryConfiguration, jsii.invoke(self, "bind", [scope]))

    @builtins.property
    @jsii.member(jsii_name="registryType")
    def registry_type(self) -> builtins.str:
        '''The type name of ExternalDNS registry.'''
        return typing.cast(builtins.str, jsii.get(self, "registryType"))


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitCloudWatchLogsOutputOptions",
    jsii_struct_bases=[FluentBitOutputPluginCommonOptions],
    name_mapping={
        "match": "match",
        "auto_create_group": "autoCreateGroup",
        "auto_retry_requests": "autoRetryRequests",
        "endpoint": "endpoint",
        "log_format": "logFormat",
        "log_group": "logGroup",
        "log_group_template": "logGroupTemplate",
        "log_key": "logKey",
        "log_retention": "logRetention",
        "log_stream": "logStream",
        "log_stream_template": "logStreamTemplate",
        "metric_dimensions": "metricDimensions",
        "metric_namespace": "metricNamespace",
        "region": "region",
        "role": "role",
        "sts_endpoint": "stsEndpoint",
    },
)
class FluentBitCloudWatchLogsOutputOptions(FluentBitOutputPluginCommonOptions):
    def __init__(
        self,
        *,
        match: typing.Optional[FluentBitMatch] = None,
        auto_create_group: typing.Optional[builtins.bool] = None,
        auto_retry_requests: typing.Optional[builtins.bool] = None,
        endpoint: typing.Optional[builtins.str] = None,
        log_format: typing.Optional[builtins.str] = None,
        log_group: typing.Optional[FluentBitLogGroupOutput] = None,
        log_group_template: typing.Optional[builtins.str] = None,
        log_key: typing.Optional[builtins.str] = None,
        log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
        log_stream: typing.Optional[FluentBitLogStreamOutput] = None,
        log_stream_template: typing.Optional[builtins.str] = None,
        metric_dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metric_namespace: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        sts_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Options for configuring the CloudWatch Logs Fluent Bit output plugin.

        :param match: The pattern to match for records that this output should apply to.
        :param auto_create_group: Automatically create the log group. Default: false
        :param auto_retry_requests: Immediately retry failed requests to AWS services once. This option does not affect the normal Fluent Bit retry mechanism with backoff. Instead, it enables an immediate retry with no delay for networking errors, which may help improve throughput when there are transient/random networking issues. Default: true
        :param endpoint: Specify a custom endpoint for the CloudWatch Logs API.
        :param log_format: An optional parameter that can be used to tell CloudWatch the format of the data. A value of json/emf enables CloudWatch to extract custom metrics embedded in a JSON payload.
        :param log_group: The CloudWatch Log Group configuration for output records.
        :param log_group_template: Template for Log Group name using Fluent Bit record_accessor syntax. This field is optional and if configured it overrides the configured Log Group. If the template translation fails, an error is logged and the provided Log Group (which is still required) is used instead.
        :param log_key: By default, the whole log record will be sent to CloudWatch. If you specify a key name with this option, then only the value of that key will be sent to CloudWatch.
        :param log_retention: If set to a number greater than zero, and newly create log group's retention policy is set to this many days.
        :param log_stream: The CloudWatch LogStream configuration for outbound records.
        :param log_stream_template: Template for Log Stream name using Fluent Bit record accessor syntax. This field is optional and if configured it overrides the other log stream options. If the template translation fails, an error is logged and the logStream or logStreamPrefix are used instead (and thus one of those fields is still required to be configured).
        :param metric_dimensions: A list of lists containing the dimension keys that will be applied to all metrics. The values within a dimension set MUST also be members on the root-node.
        :param metric_namespace: An optional string representing the CloudWatch namespace for the metrics.
        :param region: The AWS region.
        :param role: ARN of an IAM role to assume (for cross account access).
        :param sts_endpoint: Specify a custom STS endpoint for the AWS STS API.

        :see: `CloudWatch Logs Plugin Documention <https://docs.fluentbit.io/manual/pipeline/outputs/cloudwatch>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitCloudWatchLogsOutputOptions.__init__)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument auto_create_group", value=auto_create_group, expected_type=type_hints["auto_create_group"])
            check_type(argname="argument auto_retry_requests", value=auto_retry_requests, expected_type=type_hints["auto_retry_requests"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument log_format", value=log_format, expected_type=type_hints["log_format"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument log_group_template", value=log_group_template, expected_type=type_hints["log_group_template"])
            check_type(argname="argument log_key", value=log_key, expected_type=type_hints["log_key"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument log_stream", value=log_stream, expected_type=type_hints["log_stream"])
            check_type(argname="argument log_stream_template", value=log_stream_template, expected_type=type_hints["log_stream_template"])
            check_type(argname="argument metric_dimensions", value=metric_dimensions, expected_type=type_hints["metric_dimensions"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument sts_endpoint", value=sts_endpoint, expected_type=type_hints["sts_endpoint"])
        self._values: typing.Dict[str, typing.Any] = {}
        if match is not None:
            self._values["match"] = match
        if auto_create_group is not None:
            self._values["auto_create_group"] = auto_create_group
        if auto_retry_requests is not None:
            self._values["auto_retry_requests"] = auto_retry_requests
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if log_format is not None:
            self._values["log_format"] = log_format
        if log_group is not None:
            self._values["log_group"] = log_group
        if log_group_template is not None:
            self._values["log_group_template"] = log_group_template
        if log_key is not None:
            self._values["log_key"] = log_key
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if log_stream is not None:
            self._values["log_stream"] = log_stream
        if log_stream_template is not None:
            self._values["log_stream_template"] = log_stream_template
        if metric_dimensions is not None:
            self._values["metric_dimensions"] = metric_dimensions
        if metric_namespace is not None:
            self._values["metric_namespace"] = metric_namespace
        if region is not None:
            self._values["region"] = region
        if role is not None:
            self._values["role"] = role
        if sts_endpoint is not None:
            self._values["sts_endpoint"] = sts_endpoint

    @builtins.property
    def match(self) -> typing.Optional[FluentBitMatch]:
        '''The pattern to match for records that this output should apply to.'''
        result = self._values.get("match")
        return typing.cast(typing.Optional[FluentBitMatch], result)

    @builtins.property
    def auto_create_group(self) -> typing.Optional[builtins.bool]:
        '''Automatically create the log group.

        :default: false
        '''
        result = self._values.get("auto_create_group")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_retry_requests(self) -> typing.Optional[builtins.bool]:
        '''Immediately retry failed requests to AWS services once.

        This option does
        not affect the normal Fluent Bit retry mechanism with backoff. Instead,
        it enables an immediate retry with no delay for networking errors, which
        may help improve throughput when there are transient/random networking
        issues.

        :default: true
        '''
        result = self._values.get("auto_retry_requests")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''Specify a custom endpoint for the CloudWatch Logs API.'''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_format(self) -> typing.Optional[builtins.str]:
        '''An optional parameter that can be used to tell CloudWatch the format of the data.

        A value of json/emf enables CloudWatch to extract custom
        metrics embedded in a JSON payload.

        :see: `Embedded Metric Format <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format_Specification.html>`_
        '''
        result = self._values.get("log_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group(self) -> typing.Optional[FluentBitLogGroupOutput]:
        '''The CloudWatch Log Group configuration for output records.'''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[FluentBitLogGroupOutput], result)

    @builtins.property
    def log_group_template(self) -> typing.Optional[builtins.str]:
        '''Template for Log Group name using Fluent Bit record_accessor syntax.

        This field is optional and if configured it overrides the configured Log
        Group.

        If the template translation fails, an error is logged and the provided
        Log Group (which is still required) is used instead.

        :see: `Fluent Bit record accessor snytax <https://docs.fluentbit.io/manual/administration/configuring-fluent-bit/classic-mode/record-accessor>`_
        '''
        result = self._values.get("log_group_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_key(self) -> typing.Optional[builtins.str]:
        '''By default, the whole log record will be sent to CloudWatch.

        If you
        specify a key name with this option, then only the value of that key
        will be sent to CloudWatch.
        '''
        result = self._values.get("log_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_retention(self) -> typing.Optional[aws_cdk.aws_logs.RetentionDays]:
        '''If set to a number greater than zero, and newly create log group's retention policy is set to this many days.'''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[aws_cdk.aws_logs.RetentionDays], result)

    @builtins.property
    def log_stream(self) -> typing.Optional[FluentBitLogStreamOutput]:
        '''The CloudWatch LogStream configuration for outbound records.'''
        result = self._values.get("log_stream")
        return typing.cast(typing.Optional[FluentBitLogStreamOutput], result)

    @builtins.property
    def log_stream_template(self) -> typing.Optional[builtins.str]:
        '''Template for Log Stream name using Fluent Bit record accessor syntax.

        This field is optional and if configured it overrides the other log
        stream options. If the template translation fails, an error is logged
        and the logStream or logStreamPrefix are used instead (and thus one of
        those fields is still required to be configured).

        :see: `Fluent Bit record accessor snytax <https://docs.fluentbit.io/manual/administration/configuring-fluent-bit/classic-mode/record-accessor>`_
        '''
        result = self._values.get("log_stream_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metric_dimensions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of lists containing the dimension keys that will be applied to all metrics.

        The values within a dimension set MUST also be members on
        the root-node.

        :see: `Dimensions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Dimension>`_
        '''
        result = self._values.get("metric_dimensions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metric_namespace(self) -> typing.Optional[builtins.str]:
        '''An optional string representing the CloudWatch namespace for the metrics.

        :see: `Metric Tutorial <https://docs.fluentbit.io/manual/pipeline/outputs/cloudwatch#metrics-tutorial>`_
        '''
        result = self._values.get("metric_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''ARN of an IAM role to assume (for cross account access).'''
        result = self._values.get("role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    @builtins.property
    def sts_endpoint(self) -> typing.Optional[builtins.str]:
        '''Specify a custom STS endpoint for the AWS STS API.'''
        result = self._values.get("sts_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitCloudWatchLogsOutputOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitElasticsearchOutputOptions",
    jsii_struct_bases=[FluentBitOutputPluginCommonOptions],
    name_mapping={
        "match": "match",
        "host": "host",
        "aws_auth": "awsAuth",
        "aws_external_id": "awsExternalId",
        "aws_region": "awsRegion",
        "aws_role": "awsRole",
        "aws_sts_endpoint": "awsStsEndpoint",
        "buffer_size": "bufferSize",
        "cloud_auth": "cloudAuth",
        "cloud_id": "cloudId",
        "compress": "compress",
        "current_time_index": "currentTimeIndex",
        "generate_id": "generateId",
        "http_passwd": "httpPasswd",
        "http_user": "httpUser",
        "id_key": "idKey",
        "include_tag_key": "includeTagKey",
        "index": "index",
        "logstash_date_format": "logstashDateFormat",
        "logstash_format": "logstashFormat",
        "logstash_prefix": "logstashPrefix",
        "logstash_prefix_key": "logstashPrefixKey",
        "path": "path",
        "pipeline": "pipeline",
        "port": "port",
        "replace_dots": "replaceDots",
        "suppress_type_name": "suppressTypeName",
        "tag_key": "tagKey",
        "time_key": "timeKey",
        "time_key_format": "timeKeyFormat",
        "time_key_nanos": "timeKeyNanos",
        "trace_error": "traceError",
        "trace_output": "traceOutput",
        "type": "type",
        "workers": "workers",
        "write_operation": "writeOperation",
    },
)
class FluentBitElasticsearchOutputOptions(FluentBitOutputPluginCommonOptions):
    def __init__(
        self,
        *,
        match: typing.Optional[FluentBitMatch] = None,
        host: builtins.str,
        aws_auth: typing.Optional[builtins.bool] = None,
        aws_external_id: typing.Optional[builtins.str] = None,
        aws_region: typing.Optional[builtins.str] = None,
        aws_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        aws_sts_endpoint: typing.Optional[builtins.str] = None,
        buffer_size: typing.Optional[ElasticsearchOutputBufferSize] = None,
        cloud_auth: typing.Optional[builtins.str] = None,
        cloud_id: typing.Optional[builtins.str] = None,
        compress: typing.Optional[ElasticsearchCompressionFormat] = None,
        current_time_index: typing.Optional[builtins.bool] = None,
        generate_id: typing.Optional[builtins.bool] = None,
        http_passwd: typing.Optional[builtins.str] = None,
        http_user: typing.Optional[builtins.str] = None,
        id_key: typing.Optional[builtins.str] = None,
        include_tag_key: typing.Optional[builtins.bool] = None,
        index: typing.Optional[builtins.str] = None,
        logstash_date_format: typing.Optional[builtins.str] = None,
        logstash_format: typing.Optional[builtins.bool] = None,
        logstash_prefix: typing.Optional[builtins.str] = None,
        logstash_prefix_key: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        pipeline: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        replace_dots: typing.Optional[builtins.bool] = None,
        suppress_type_name: typing.Optional[builtins.bool] = None,
        tag_key: typing.Optional[builtins.str] = None,
        time_key: typing.Optional[builtins.str] = None,
        time_key_format: typing.Optional[builtins.str] = None,
        time_key_nanos: typing.Optional[builtins.bool] = None,
        trace_error: typing.Optional[builtins.bool] = None,
        trace_output: typing.Optional[builtins.bool] = None,
        type: typing.Optional[builtins.str] = None,
        workers: typing.Optional[jsii.Number] = None,
        write_operation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Options for configuring the Elasticsearch Fluent Bit output plugin.

        :param match: The pattern to match for records that this output should apply to.
        :param host: IP address or hostname of the target Elasticsearch instance.
        :param aws_auth: Enable AWS Sigv4 Authentication for Amazon Elasticsearch Service. Default: false
        :param aws_external_id: External ID for the AWS IAM Role specified with ``awsRole``.
        :param aws_region: Specify the AWS region for Elasticsearch Service.
        :param aws_role: AWS IAM Role to assume to put records to your Amazon cluster.
        :param aws_sts_endpoint: Specify the custom sts endpoint to be used with STS API for Amazon Elasticsearch Service.
        :param buffer_size: Specify the buffer size used to read the response from the Elasticsearch HTTP service. This option is useful for debugging purposes where is required to read full responses, note that response size grows depending of the number of records inserted.
        :param cloud_auth: Specify the credentials to use to connect to Elastic's Elasticsearch Service running on Elastic Cloud.
        :param cloud_id: If you are using Elastic's Elasticsearch Service you can specify the cloud_id of the cluster running.
        :param compress: Set payload compression mechanism.
        :param current_time_index: Use current time for index generation instead of message record. Default: false
        :param generate_id: When enabled, generate ``_id`` for outgoing records. This prevents duplicate records when retrying.
        :param http_passwd: Password for user defined in ``httpUser``.
        :param http_user: Optional username credential for access.
        :param id_key: If set, ``_id`` will be the value of the key from incoming record and ``generateId`` option is ignored.
        :param include_tag_key: When enabled, it append the Tag name to the record.
        :param index: Index name. Default: 'fluent-bit
        :param logstash_date_format: Time format (based on strftime) to generate the second part of the Index name. Default: '%Y.%m.%d'
        :param logstash_format: Enable Logstash format compatibility. Default: false
        :param logstash_prefix: When ``logstashFormat`` is enabled, the Index name is composed using a prefix and the date, e.g: If ``logstashPrefix`` is equals to 'mydata' your index will become 'mydata-YYYY.MM.DD'. The last string appended belongs to the date when the data is being generated. Default: 'logstash'
        :param logstash_prefix_key: When included: the value in the record that belongs to the key will be looked up and over-write the ``logstashPrefix`` for index generation. If the key/value is not found in the record then the ``logstashPrefix`` option will act as a fallback. Nested keys are not supported (if desired, you can use the nest filter plugin to remove nesting)
        :param path: Elasticsearch accepts new data on HTTP query path "/_bulk". But it is also possible to serve Elasticsearch behind a reverse proxy on a subpath. This option defines such path on the fluent-bit side. It simply adds a path prefix in the indexing HTTP POST URI..
        :param pipeline: Elasticsearch allows to setup filters called pipelines. This option allows to define which pipeline the database should use.
        :param port: TCP port of the target Elasticsearch instance. Default: 9200
        :param replace_dots: When enabled, replace field name dots with underscore. Default: false
        :param suppress_type_name: When enabled, mapping types is removed and ``type`` option is ignored. Default: false
        :param tag_key: When ``includeTagKey`` is enabled, this property defines the key name for the tag. Default: '_flb-key'
        :param time_key: When ``logstashFormat`` is enabled, each record will get a new timestamp field. The``timeKey`` property defines the name of that field. Default: '
        :param time_key_format: When ``logstashFormat`` is enabled, this property defines the format of the timestamp. Default: '%Y-%m-%dT%H:%M:%S'
        :param time_key_nanos: When ``logstashFormat`` is enabled, enabling this property sends nanosecond precision timestamps. Default: false
        :param trace_error: When enabled print the Elasticsearch API calls to stdout when Elasticsearch returns an error (for diag only). Default: false
        :param trace_output: When enabled print the Elasticsearch API calls to stdout (for diag only). Default: false
        :param type: Type name. Default: '_doc'
        :param workers: Enables dedicated thread(s) for this output. Default: 2
        :param write_operation: Operation to use to write in bulk requests. Default: 'create'

        :see: `Opensearch Plugin Documention <https://docs.fluentbit.io/manual/pipeline/outputs/elasticsearch>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitElasticsearchOutputOptions.__init__)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument aws_auth", value=aws_auth, expected_type=type_hints["aws_auth"])
            check_type(argname="argument aws_external_id", value=aws_external_id, expected_type=type_hints["aws_external_id"])
            check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
            check_type(argname="argument aws_role", value=aws_role, expected_type=type_hints["aws_role"])
            check_type(argname="argument aws_sts_endpoint", value=aws_sts_endpoint, expected_type=type_hints["aws_sts_endpoint"])
            check_type(argname="argument buffer_size", value=buffer_size, expected_type=type_hints["buffer_size"])
            check_type(argname="argument cloud_auth", value=cloud_auth, expected_type=type_hints["cloud_auth"])
            check_type(argname="argument cloud_id", value=cloud_id, expected_type=type_hints["cloud_id"])
            check_type(argname="argument compress", value=compress, expected_type=type_hints["compress"])
            check_type(argname="argument current_time_index", value=current_time_index, expected_type=type_hints["current_time_index"])
            check_type(argname="argument generate_id", value=generate_id, expected_type=type_hints["generate_id"])
            check_type(argname="argument http_passwd", value=http_passwd, expected_type=type_hints["http_passwd"])
            check_type(argname="argument http_user", value=http_user, expected_type=type_hints["http_user"])
            check_type(argname="argument id_key", value=id_key, expected_type=type_hints["id_key"])
            check_type(argname="argument include_tag_key", value=include_tag_key, expected_type=type_hints["include_tag_key"])
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument logstash_date_format", value=logstash_date_format, expected_type=type_hints["logstash_date_format"])
            check_type(argname="argument logstash_format", value=logstash_format, expected_type=type_hints["logstash_format"])
            check_type(argname="argument logstash_prefix", value=logstash_prefix, expected_type=type_hints["logstash_prefix"])
            check_type(argname="argument logstash_prefix_key", value=logstash_prefix_key, expected_type=type_hints["logstash_prefix_key"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument pipeline", value=pipeline, expected_type=type_hints["pipeline"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument replace_dots", value=replace_dots, expected_type=type_hints["replace_dots"])
            check_type(argname="argument suppress_type_name", value=suppress_type_name, expected_type=type_hints["suppress_type_name"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument time_key", value=time_key, expected_type=type_hints["time_key"])
            check_type(argname="argument time_key_format", value=time_key_format, expected_type=type_hints["time_key_format"])
            check_type(argname="argument time_key_nanos", value=time_key_nanos, expected_type=type_hints["time_key_nanos"])
            check_type(argname="argument trace_error", value=trace_error, expected_type=type_hints["trace_error"])
            check_type(argname="argument trace_output", value=trace_output, expected_type=type_hints["trace_output"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument workers", value=workers, expected_type=type_hints["workers"])
            check_type(argname="argument write_operation", value=write_operation, expected_type=type_hints["write_operation"])
        self._values: typing.Dict[str, typing.Any] = {
            "host": host,
        }
        if match is not None:
            self._values["match"] = match
        if aws_auth is not None:
            self._values["aws_auth"] = aws_auth
        if aws_external_id is not None:
            self._values["aws_external_id"] = aws_external_id
        if aws_region is not None:
            self._values["aws_region"] = aws_region
        if aws_role is not None:
            self._values["aws_role"] = aws_role
        if aws_sts_endpoint is not None:
            self._values["aws_sts_endpoint"] = aws_sts_endpoint
        if buffer_size is not None:
            self._values["buffer_size"] = buffer_size
        if cloud_auth is not None:
            self._values["cloud_auth"] = cloud_auth
        if cloud_id is not None:
            self._values["cloud_id"] = cloud_id
        if compress is not None:
            self._values["compress"] = compress
        if current_time_index is not None:
            self._values["current_time_index"] = current_time_index
        if generate_id is not None:
            self._values["generate_id"] = generate_id
        if http_passwd is not None:
            self._values["http_passwd"] = http_passwd
        if http_user is not None:
            self._values["http_user"] = http_user
        if id_key is not None:
            self._values["id_key"] = id_key
        if include_tag_key is not None:
            self._values["include_tag_key"] = include_tag_key
        if index is not None:
            self._values["index"] = index
        if logstash_date_format is not None:
            self._values["logstash_date_format"] = logstash_date_format
        if logstash_format is not None:
            self._values["logstash_format"] = logstash_format
        if logstash_prefix is not None:
            self._values["logstash_prefix"] = logstash_prefix
        if logstash_prefix_key is not None:
            self._values["logstash_prefix_key"] = logstash_prefix_key
        if path is not None:
            self._values["path"] = path
        if pipeline is not None:
            self._values["pipeline"] = pipeline
        if port is not None:
            self._values["port"] = port
        if replace_dots is not None:
            self._values["replace_dots"] = replace_dots
        if suppress_type_name is not None:
            self._values["suppress_type_name"] = suppress_type_name
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if time_key is not None:
            self._values["time_key"] = time_key
        if time_key_format is not None:
            self._values["time_key_format"] = time_key_format
        if time_key_nanos is not None:
            self._values["time_key_nanos"] = time_key_nanos
        if trace_error is not None:
            self._values["trace_error"] = trace_error
        if trace_output is not None:
            self._values["trace_output"] = trace_output
        if type is not None:
            self._values["type"] = type
        if workers is not None:
            self._values["workers"] = workers
        if write_operation is not None:
            self._values["write_operation"] = write_operation

    @builtins.property
    def match(self) -> typing.Optional[FluentBitMatch]:
        '''The pattern to match for records that this output should apply to.'''
        result = self._values.get("match")
        return typing.cast(typing.Optional[FluentBitMatch], result)

    @builtins.property
    def host(self) -> builtins.str:
        '''IP address or hostname of the target Elasticsearch instance.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_auth(self) -> typing.Optional[builtins.bool]:
        '''Enable AWS Sigv4 Authentication for Amazon Elasticsearch Service.

        :default: false
        '''
        result = self._values.get("aws_auth")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def aws_external_id(self) -> typing.Optional[builtins.str]:
        '''External ID for the AWS IAM Role specified with ``awsRole``.'''
        result = self._values.get("aws_external_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_region(self) -> typing.Optional[builtins.str]:
        '''Specify the AWS region for Elasticsearch Service.'''
        result = self._values.get("aws_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''AWS IAM Role to assume to put records to your Amazon cluster.'''
        result = self._values.get("aws_role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    @builtins.property
    def aws_sts_endpoint(self) -> typing.Optional[builtins.str]:
        '''Specify the custom sts endpoint to be used with STS API for Amazon Elasticsearch Service.'''
        result = self._values.get("aws_sts_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def buffer_size(self) -> typing.Optional[ElasticsearchOutputBufferSize]:
        '''Specify the buffer size used to read the response from the Elasticsearch HTTP service.

        This option is useful for debugging purposes where is
        required to read full responses, note that response size grows depending
        of the number of records inserted.
        '''
        result = self._values.get("buffer_size")
        return typing.cast(typing.Optional[ElasticsearchOutputBufferSize], result)

    @builtins.property
    def cloud_auth(self) -> typing.Optional[builtins.str]:
        '''Specify the credentials to use to connect to Elastic's Elasticsearch Service running on Elastic Cloud.'''
        result = self._values.get("cloud_auth")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_id(self) -> typing.Optional[builtins.str]:
        '''If you are using Elastic's Elasticsearch Service you can specify the cloud_id of the cluster running.'''
        result = self._values.get("cloud_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compress(self) -> typing.Optional[ElasticsearchCompressionFormat]:
        '''Set payload compression mechanism.'''
        result = self._values.get("compress")
        return typing.cast(typing.Optional[ElasticsearchCompressionFormat], result)

    @builtins.property
    def current_time_index(self) -> typing.Optional[builtins.bool]:
        '''Use current time for index generation instead of message record.

        :default: false
        '''
        result = self._values.get("current_time_index")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def generate_id(self) -> typing.Optional[builtins.bool]:
        '''When enabled, generate ``_id`` for outgoing records.

        This prevents duplicate
        records when retrying.
        '''
        result = self._values.get("generate_id")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def http_passwd(self) -> typing.Optional[builtins.str]:
        '''Password for user defined in ``httpUser``.'''
        result = self._values.get("http_passwd")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_user(self) -> typing.Optional[builtins.str]:
        '''Optional username credential for access.'''
        result = self._values.get("http_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id_key(self) -> typing.Optional[builtins.str]:
        '''If set, ``_id`` will be the value of the key from incoming record and ``generateId`` option is ignored.'''
        result = self._values.get("id_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_tag_key(self) -> typing.Optional[builtins.bool]:
        '''When enabled, it append the Tag name to the record.'''
        result = self._values.get("include_tag_key")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def index(self) -> typing.Optional[builtins.str]:
        '''Index name.

        :default: 'fluent-bit
        '''
        result = self._values.get("index")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logstash_date_format(self) -> typing.Optional[builtins.str]:
        '''Time format (based on strftime) to generate the second part of the Index name.

        :default: '%Y.%m.%d'

        :see: `strftime <http://man7.org/linux/man-pages/man3/strftime.3.html>`_
        '''
        result = self._values.get("logstash_date_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logstash_format(self) -> typing.Optional[builtins.bool]:
        '''Enable Logstash format compatibility.

        :default: false
        '''
        result = self._values.get("logstash_format")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def logstash_prefix(self) -> typing.Optional[builtins.str]:
        '''When ``logstashFormat`` is enabled, the Index name is composed using a prefix and the date, e.g: If ``logstashPrefix`` is equals to 'mydata' your index will become 'mydata-YYYY.MM.DD'.

        The last string appended belongs to the date when the data is being
        generated.

        :default: 'logstash'
        '''
        result = self._values.get("logstash_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logstash_prefix_key(self) -> typing.Optional[builtins.str]:
        '''When included: the value in the record that belongs to the key will be looked up and over-write the ``logstashPrefix`` for index generation.

        If
        the key/value is not found in the record then the ``logstashPrefix`` option
        will act as a fallback.

        Nested keys are not supported (if desired, you can use the nest filter
        plugin to remove nesting)
        '''
        result = self._values.get("logstash_prefix_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Elasticsearch accepts new data on HTTP query path "/_bulk".

        But it is
        also possible to serve Elasticsearch behind a reverse proxy on a
        subpath. This option defines such path on the fluent-bit side. It
        simply adds a path prefix in the indexing HTTP POST URI..
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pipeline(self) -> typing.Optional[builtins.str]:
        '''Elasticsearch allows to setup filters called pipelines.

        This option
        allows to define which pipeline the database should use.
        '''
        result = self._values.get("pipeline")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''TCP port of the target Elasticsearch instance.

        :default: 9200
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def replace_dots(self) -> typing.Optional[builtins.bool]:
        '''When enabled, replace field name dots with underscore.

        :default: false
        '''
        result = self._values.get("replace_dots")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def suppress_type_name(self) -> typing.Optional[builtins.bool]:
        '''When enabled, mapping types is removed and ``type`` option is ignored.

        :default: false
        '''
        result = self._values.get("suppress_type_name")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''When ``includeTagKey`` is enabled, this property defines the key name for the tag.

        :default: '_flb-key'
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_key(self) -> typing.Optional[builtins.str]:
        '''When ``logstashFormat`` is enabled, each record will get a new timestamp field.

        The``timeKey`` property defines the name of that field.

        :default: '

        :timestamp: '
        '''
        result = self._values.get("time_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_key_format(self) -> typing.Optional[builtins.str]:
        '''When ``logstashFormat`` is enabled, this property defines the format of the timestamp.

        :default: '%Y-%m-%dT%H:%M:%S'

        :see: `strftime <http://man7.org/linux/man-pages/man3/strftime.3.html>`_
        '''
        result = self._values.get("time_key_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_key_nanos(self) -> typing.Optional[builtins.bool]:
        '''When ``logstashFormat`` is enabled, enabling this property sends nanosecond precision timestamps.

        :default: false
        '''
        result = self._values.get("time_key_nanos")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def trace_error(self) -> typing.Optional[builtins.bool]:
        '''When enabled print the Elasticsearch API calls to stdout when Elasticsearch returns an error (for diag only).

        :default: false
        '''
        result = self._values.get("trace_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def trace_output(self) -> typing.Optional[builtins.bool]:
        '''When enabled print the Elasticsearch API calls to stdout (for diag only).

        :default: false
        '''
        result = self._values.get("trace_output")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type name.

        :default: '_doc'
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workers(self) -> typing.Optional[jsii.Number]:
        '''Enables dedicated thread(s) for this output.

        :default: 2
        '''
        result = self._values.get("workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def write_operation(self) -> typing.Optional[builtins.str]:
        '''Operation to use to write in bulk requests.

        :default: 'create'
        '''
        result = self._values.get("write_operation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitElasticsearchOutputOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitJsonParserOptions",
    jsii_struct_bases=[FluentBitParserPluginCommonOptions],
    name_mapping={"time_format": "timeFormat", "time_key": "timeKey"},
)
class FluentBitJsonParserOptions(FluentBitParserPluginCommonOptions):
    def __init__(
        self,
        *,
        time_format: typing.Optional[builtins.str] = None,
        time_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Options for configuring the JSON Fluent Bit parser plugin.

        :param time_format: Defines the format of the timestamp on the inbound record.
        :param time_key: The key under which timestamp information for the inbound record is given.

        :see: `JSON Plugin Documention <https://docs.fluentbit.io/manual/pipeline/parsers/json>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitJsonParserOptions.__init__)
            check_type(argname="argument time_format", value=time_format, expected_type=type_hints["time_format"])
            check_type(argname="argument time_key", value=time_key, expected_type=type_hints["time_key"])
        self._values: typing.Dict[str, typing.Any] = {}
        if time_format is not None:
            self._values["time_format"] = time_format
        if time_key is not None:
            self._values["time_key"] = time_key

    @builtins.property
    def time_format(self) -> typing.Optional[builtins.str]:
        '''Defines the format of the timestamp on the inbound record.

        :see: `strftime <http://man7.org/linux/man-pages/man3/strftime.3.html>`_
        '''
        result = self._values.get("time_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_key(self) -> typing.Optional[builtins.str]:
        '''The key under which timestamp information for the inbound record is given.'''
        result = self._values.get("time_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitJsonParserOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitKinesisFirehoseOutputOptions",
    jsii_struct_bases=[FluentBitOutputPluginCommonOptions],
    name_mapping={
        "match": "match",
        "auto_retry_requests": "autoRetryRequests",
        "compression": "compression",
        "delivery_stream": "deliveryStream",
        "endpoint": "endpoint",
        "log_key": "logKey",
        "region": "region",
        "role": "role",
        "sts_endpoint": "stsEndpoint",
        "time_key": "timeKey",
        "time_key_format": "timeKeyFormat",
    },
)
class FluentBitKinesisFirehoseOutputOptions(FluentBitOutputPluginCommonOptions):
    def __init__(
        self,
        *,
        match: typing.Optional[FluentBitMatch] = None,
        auto_retry_requests: typing.Optional[builtins.bool] = None,
        compression: typing.Optional[KinesisFirehoseCompressionFormat] = None,
        delivery_stream: typing.Optional[_IDeliveryStream_cf5feed7] = None,
        endpoint: typing.Optional[builtins.str] = None,
        log_key: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        sts_endpoint: typing.Optional[builtins.str] = None,
        time_key: typing.Optional[builtins.str] = None,
        time_key_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Options for configuring the Kinesis Firehose Fluent Bit output plugin.

        :param match: The pattern to match for records that this output should apply to.
        :param auto_retry_requests: Immediately retry failed requests to AWS services once. This option does not affect the normal Fluent Bit retry mechanism with backoff. Instead, it enables an immediate retry with no delay for networking errors, which may help improve throughput when there are transient/random networking issues. Default: true
        :param compression: Compression type for Firehose records. Each log record is individually compressed and sent to Firehose.
        :param delivery_stream: The Kinesis Firehose Delivery stream that you want log records sent to.
        :param endpoint: Specify a custom endpoint for the Firehose API.
        :param log_key: By default, the whole log record will be sent to Firehose. If you specify a key name with this option, then only the value of that key will be sent to Firehose.
        :param region: The AWS region.
        :param role: ARN of an IAM role to assume (for cross account access).
        :param sts_endpoint: Specify a custom STS endpoint for the AWS STS API.
        :param time_key: Add the timestamp to the record under this key.
        :param time_key_format: A strftime compliant format string for the timestamp. Default: '%Y-%m-%dT%H:%M:%S'

        :see: `Kinesis Firehose Plugin Documention <https://docs.fluentbit.io/manual/pipeline/outputs/firehose>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitKinesisFirehoseOutputOptions.__init__)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument auto_retry_requests", value=auto_retry_requests, expected_type=type_hints["auto_retry_requests"])
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument log_key", value=log_key, expected_type=type_hints["log_key"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument sts_endpoint", value=sts_endpoint, expected_type=type_hints["sts_endpoint"])
            check_type(argname="argument time_key", value=time_key, expected_type=type_hints["time_key"])
            check_type(argname="argument time_key_format", value=time_key_format, expected_type=type_hints["time_key_format"])
        self._values: typing.Dict[str, typing.Any] = {}
        if match is not None:
            self._values["match"] = match
        if auto_retry_requests is not None:
            self._values["auto_retry_requests"] = auto_retry_requests
        if compression is not None:
            self._values["compression"] = compression
        if delivery_stream is not None:
            self._values["delivery_stream"] = delivery_stream
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if log_key is not None:
            self._values["log_key"] = log_key
        if region is not None:
            self._values["region"] = region
        if role is not None:
            self._values["role"] = role
        if sts_endpoint is not None:
            self._values["sts_endpoint"] = sts_endpoint
        if time_key is not None:
            self._values["time_key"] = time_key
        if time_key_format is not None:
            self._values["time_key_format"] = time_key_format

    @builtins.property
    def match(self) -> typing.Optional[FluentBitMatch]:
        '''The pattern to match for records that this output should apply to.'''
        result = self._values.get("match")
        return typing.cast(typing.Optional[FluentBitMatch], result)

    @builtins.property
    def auto_retry_requests(self) -> typing.Optional[builtins.bool]:
        '''Immediately retry failed requests to AWS services once.

        This option does
        not affect the normal Fluent Bit retry mechanism with backoff. Instead,
        it enables an immediate retry with no delay for networking errors, which
        may help improve throughput when there are transient/random networking
        issues.

        :default: true
        '''
        result = self._values.get("auto_retry_requests")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def compression(self) -> typing.Optional[KinesisFirehoseCompressionFormat]:
        '''Compression type for Firehose records.

        Each log record is individually
        compressed and sent to Firehose.
        '''
        result = self._values.get("compression")
        return typing.cast(typing.Optional[KinesisFirehoseCompressionFormat], result)

    @builtins.property
    def delivery_stream(self) -> typing.Optional[_IDeliveryStream_cf5feed7]:
        '''The Kinesis Firehose Delivery stream that you want log records sent to.'''
        result = self._values.get("delivery_stream")
        return typing.cast(typing.Optional[_IDeliveryStream_cf5feed7], result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''Specify a custom endpoint for the Firehose API.'''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_key(self) -> typing.Optional[builtins.str]:
        '''By default, the whole log record will be sent to Firehose.

        If you
        specify a key name with this option, then only the value of that key
        will be sent to Firehose.
        '''
        result = self._values.get("log_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''ARN of an IAM role to assume (for cross account access).'''
        result = self._values.get("role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    @builtins.property
    def sts_endpoint(self) -> typing.Optional[builtins.str]:
        '''Specify a custom STS endpoint for the AWS STS API.'''
        result = self._values.get("sts_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_key(self) -> typing.Optional[builtins.str]:
        '''Add the timestamp to the record under this key.'''
        result = self._values.get("time_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_key_format(self) -> typing.Optional[builtins.str]:
        '''A strftime compliant format string for the timestamp.

        :default: '%Y-%m-%dT%H:%M:%S'
        '''
        result = self._values.get("time_key_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitKinesisFirehoseOutputOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitKinesisOutputOptions",
    jsii_struct_bases=[FluentBitOutputPluginCommonOptions],
    name_mapping={
        "match": "match",
        "auto_retry_requests": "autoRetryRequests",
        "endpoint": "endpoint",
        "log_key": "logKey",
        "region": "region",
        "role": "role",
        "stream": "stream",
        "sts_endpoint": "stsEndpoint",
        "time_key": "timeKey",
        "time_key_format": "timeKeyFormat",
    },
)
class FluentBitKinesisOutputOptions(FluentBitOutputPluginCommonOptions):
    def __init__(
        self,
        *,
        match: typing.Optional[FluentBitMatch] = None,
        auto_retry_requests: typing.Optional[builtins.bool] = None,
        endpoint: typing.Optional[builtins.str] = None,
        log_key: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        stream: typing.Optional[aws_cdk.aws_kinesis.IStream] = None,
        sts_endpoint: typing.Optional[builtins.str] = None,
        time_key: typing.Optional[builtins.str] = None,
        time_key_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Options for configuring the Kinesis Data Streams Fluent Bit output plugin.

        :param match: The pattern to match for records that this output should apply to.
        :param auto_retry_requests: Immediately retry failed requests to AWS services once. This option does not affect the normal Fluent Bit retry mechanism with backoff. Instead, it enables an immediate retry with no delay for networking errors, which may help improve throughput when there are transient/random networking issues. Default: true
        :param endpoint: Specify a custom endpoint for the Firehose API.
        :param log_key: By default, the whole log record will be sent to Firehose. If you specify a key name with this option, then only the value of that key will be sent to Firehose.
        :param region: The AWS region.
        :param role: ARN of an IAM role to assume (for cross account access).
        :param stream: The name of the Kinesis Streams Delivery stream that you want log records sent to.
        :param sts_endpoint: Specify a custom STS endpoint for the AWS STS API.
        :param time_key: Add the timestamp to the record under this key.
        :param time_key_format: A strftime compliant format string for the timestamp. Default: '%Y-%m-%dT%H:%M:%S'

        :see: `Kinesis Streams Plugin Documention <https://docs.fluentbit.io/manual/pipeline/outputs/kinesis>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitKinesisOutputOptions.__init__)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument auto_retry_requests", value=auto_retry_requests, expected_type=type_hints["auto_retry_requests"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument log_key", value=log_key, expected_type=type_hints["log_key"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
            check_type(argname="argument sts_endpoint", value=sts_endpoint, expected_type=type_hints["sts_endpoint"])
            check_type(argname="argument time_key", value=time_key, expected_type=type_hints["time_key"])
            check_type(argname="argument time_key_format", value=time_key_format, expected_type=type_hints["time_key_format"])
        self._values: typing.Dict[str, typing.Any] = {}
        if match is not None:
            self._values["match"] = match
        if auto_retry_requests is not None:
            self._values["auto_retry_requests"] = auto_retry_requests
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if log_key is not None:
            self._values["log_key"] = log_key
        if region is not None:
            self._values["region"] = region
        if role is not None:
            self._values["role"] = role
        if stream is not None:
            self._values["stream"] = stream
        if sts_endpoint is not None:
            self._values["sts_endpoint"] = sts_endpoint
        if time_key is not None:
            self._values["time_key"] = time_key
        if time_key_format is not None:
            self._values["time_key_format"] = time_key_format

    @builtins.property
    def match(self) -> typing.Optional[FluentBitMatch]:
        '''The pattern to match for records that this output should apply to.'''
        result = self._values.get("match")
        return typing.cast(typing.Optional[FluentBitMatch], result)

    @builtins.property
    def auto_retry_requests(self) -> typing.Optional[builtins.bool]:
        '''Immediately retry failed requests to AWS services once.

        This option does
        not affect the normal Fluent Bit retry mechanism with backoff. Instead,
        it enables an immediate retry with no delay for networking errors, which
        may help improve throughput when there are transient/random networking
        issues.

        :default: true
        '''
        result = self._values.get("auto_retry_requests")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''Specify a custom endpoint for the Firehose API.'''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_key(self) -> typing.Optional[builtins.str]:
        '''By default, the whole log record will be sent to Firehose.

        If you
        specify a key name with this option, then only the value of that key
        will be sent to Firehose.
        '''
        result = self._values.get("log_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''ARN of an IAM role to assume (for cross account access).'''
        result = self._values.get("role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    @builtins.property
    def stream(self) -> typing.Optional[aws_cdk.aws_kinesis.IStream]:
        '''The name of the Kinesis Streams Delivery stream that you want log records sent to.'''
        result = self._values.get("stream")
        return typing.cast(typing.Optional[aws_cdk.aws_kinesis.IStream], result)

    @builtins.property
    def sts_endpoint(self) -> typing.Optional[builtins.str]:
        '''Specify a custom STS endpoint for the AWS STS API.'''
        result = self._values.get("sts_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_key(self) -> typing.Optional[builtins.str]:
        '''Add the timestamp to the record under this key.'''
        result = self._values.get("time_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_key_format(self) -> typing.Optional[builtins.str]:
        '''A strftime compliant format string for the timestamp.

        :default: '%Y-%m-%dT%H:%M:%S'
        '''
        result = self._values.get("time_key_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitKinesisOutputOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitLogfmtParserOptions",
    jsii_struct_bases=[FluentBitParserPluginCommonOptions],
    name_mapping={
        "time_format": "timeFormat",
        "time_key": "timeKey",
        "types": "types",
    },
)
class FluentBitLogfmtParserOptions(FluentBitParserPluginCommonOptions):
    def __init__(
        self,
        *,
        time_format: typing.Optional[builtins.str] = None,
        time_key: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Mapping[builtins.str, ParserPluginDataType]] = None,
    ) -> None:
        '''Options for configuring the logfmt Fluent Bit parser plugin.

        :param time_format: Defines the format of the timestamp on the inbound record.
        :param time_key: The key under which timestamp information for the inbound record is given.
        :param types: Maps group names matched by the regex to the data types they should be interpreted as.

        :see: `Logfmt Plugin Documention <https://docs.fluentbit.io/manual/pipeline/parsers/logfmt>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitLogfmtParserOptions.__init__)
            check_type(argname="argument time_format", value=time_format, expected_type=type_hints["time_format"])
            check_type(argname="argument time_key", value=time_key, expected_type=type_hints["time_key"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[str, typing.Any] = {}
        if time_format is not None:
            self._values["time_format"] = time_format
        if time_key is not None:
            self._values["time_key"] = time_key
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def time_format(self) -> typing.Optional[builtins.str]:
        '''Defines the format of the timestamp on the inbound record.

        :see: `strftime <http://man7.org/linux/man-pages/man3/strftime.3.html>`_
        '''
        result = self._values.get("time_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_key(self) -> typing.Optional[builtins.str]:
        '''The key under which timestamp information for the inbound record is given.'''
        result = self._values.get("time_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def types(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, ParserPluginDataType]]:
        '''Maps group names matched by the regex to the data types they should be interpreted as.'''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, ParserPluginDataType]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitLogfmtParserOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitLtsvParserOptions",
    jsii_struct_bases=[FluentBitParserPluginCommonOptions],
    name_mapping={
        "time_format": "timeFormat",
        "time_key": "timeKey",
        "types": "types",
    },
)
class FluentBitLtsvParserOptions(FluentBitParserPluginCommonOptions):
    def __init__(
        self,
        *,
        time_format: typing.Optional[builtins.str] = None,
        time_key: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Mapping[builtins.str, ParserPluginDataType]] = None,
    ) -> None:
        '''Options for configuring the LTSV Fluent Bit parser plugin.

        :param time_format: Defines the format of the timestamp on the inbound record.
        :param time_key: The key under which timestamp information for the inbound record is given.
        :param types: Maps group names matched by the regex to the data types they should be interpreted as.

        :see: `LTSV Plugin Documention <https://docs.fluentbit.io/manual/pipeline/parsers/ltsv>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitLtsvParserOptions.__init__)
            check_type(argname="argument time_format", value=time_format, expected_type=type_hints["time_format"])
            check_type(argname="argument time_key", value=time_key, expected_type=type_hints["time_key"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[str, typing.Any] = {}
        if time_format is not None:
            self._values["time_format"] = time_format
        if time_key is not None:
            self._values["time_key"] = time_key
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def time_format(self) -> typing.Optional[builtins.str]:
        '''Defines the format of the timestamp on the inbound record.

        :see: `strftime <http://man7.org/linux/man-pages/man3/strftime.3.html>`_
        '''
        result = self._values.get("time_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_key(self) -> typing.Optional[builtins.str]:
        '''The key under which timestamp information for the inbound record is given.'''
        result = self._values.get("time_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def types(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, ParserPluginDataType]]:
        '''Maps group names matched by the regex to the data types they should be interpreted as.'''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, ParserPluginDataType]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitLtsvParserOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.k8s_aws.FluentBitOpenSearchOutputOptions",
    jsii_struct_bases=[FluentBitOutputPluginCommonOptions],
    name_mapping={
        "match": "match",
        "domain": "domain",
        "aws_auth": "awsAuth",
        "aws_external_id": "awsExternalId",
        "aws_region": "awsRegion",
        "aws_role": "awsRole",
        "aws_sts_endpoint": "awsStsEndpoint",
        "buffer_size": "bufferSize",
        "current_time_index": "currentTimeIndex",
        "generate_id": "generateId",
        "host": "host",
        "http_passwd": "httpPasswd",
        "http_user": "httpUser",
        "id_key": "idKey",
        "include_tag_key": "includeTagKey",
        "index": "index",
        "logstash_date_format": "logstashDateFormat",
        "logstash_format": "logstashFormat",
        "logstash_prefix": "logstashPrefix",
        "logstash_prefix_key": "logstashPrefixKey",
        "path": "path",
        "pipeline": "pipeline",
        "port": "port",
        "replace_dots": "replaceDots",
        "suppress_type_name": "suppressTypeName",
        "tag_key": "tagKey",
        "time_key": "timeKey",
        "time_key_format": "timeKeyFormat",
        "time_key_nanos": "timeKeyNanos",
        "trace_error": "traceError",
        "trace_output": "traceOutput",
        "type": "type",
        "workers": "workers",
        "write_operation": "writeOperation",
    },
)
class FluentBitOpenSearchOutputOptions(FluentBitOutputPluginCommonOptions):
    def __init__(
        self,
        *,
        match: typing.Optional[FluentBitMatch] = None,
        domain: aws_cdk.aws_opensearchservice.IDomain,
        aws_auth: typing.Optional[builtins.bool] = None,
        aws_external_id: typing.Optional[builtins.str] = None,
        aws_region: typing.Optional[builtins.str] = None,
        aws_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        aws_sts_endpoint: typing.Optional[builtins.str] = None,
        buffer_size: typing.Optional[OpenSearchOutputBufferSize] = None,
        current_time_index: typing.Optional[builtins.bool] = None,
        generate_id: typing.Optional[builtins.bool] = None,
        host: typing.Optional[builtins.str] = None,
        http_passwd: typing.Optional[builtins.str] = None,
        http_user: typing.Optional[builtins.str] = None,
        id_key: typing.Optional[builtins.str] = None,
        include_tag_key: typing.Optional[builtins.bool] = None,
        index: typing.Optional[builtins.str] = None,
        logstash_date_format: typing.Optional[builtins.str] = None,
        logstash_format: typing.Optional[builtins.bool] = None,
        logstash_prefix: typing.Optional[builtins.str] = None,
        logstash_prefix_key: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        pipeline: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        replace_dots: typing.Optional[builtins.bool] = None,
        suppress_type_name: typing.Optional[builtins.bool] = None,
        tag_key: typing.Optional[builtins.str] = None,
        time_key: typing.Optional[builtins.str] = None,
        time_key_format: typing.Optional[builtins.str] = None,
        time_key_nanos: typing.Optional[builtins.bool] = None,
        trace_error: typing.Optional[builtins.bool] = None,
        trace_output: typing.Optional[builtins.bool] = None,
        type: typing.Optional[builtins.str] = None,
        workers: typing.Optional[jsii.Number] = None,
        write_operation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Options for configuring the OpenSearch Fluent Bit output plugin.

        :param match: The pattern to match for records that this output should apply to.
        :param domain: The Opensearch domain to which logs should be shipped.
        :param aws_auth: Enable AWS Sigv4 Authentication for Amazon OpenSearch Service. Default: false
        :param aws_external_id: External ID for the AWS IAM Role specified with ``awsRole``.
        :param aws_region: Specify the AWS region for Amazon OpenSearch Service.
        :param aws_role: AWS IAM Role to assume to put records to your Amazon cluster.
        :param aws_sts_endpoint: Specify the custom sts endpoint to be used with STS API for Amazon OpenSearch Service.
        :param buffer_size: Specify the buffer size used to read the response from the OpenSearch HTTP service. This option is useful for debugging purposes where is required to read full responses, note that response size grows depending of the number of records inserted.
        :param current_time_index: Use current time for index generation instead of message record. Default: false
        :param generate_id: When enabled, generate ``_id`` for outgoing records. This prevents duplicate records when retrying.
        :param host: IP address or hostname of the target OpenSearch instance.
        :param http_passwd: Password for user defined in ``httpUser``.
        :param http_user: Optional username credential for access.
        :param id_key: If set, ``_id`` will be the value of the key from incoming record and ``generateId`` option is ignored.
        :param include_tag_key: When enabled, it append the Tag name to the record.
        :param index: Index name. Default: 'fluent-bit
        :param logstash_date_format: Time format (based on strftime) to generate the second part of the Index name. Default: '%Y.%m.%d'
        :param logstash_format: Enable Logstash format compatibility. Default: false
        :param logstash_prefix: When ``logstashFormat`` is enabled, the Index name is composed using a prefix and the date, e.g: If ``logstashPrefix`` is equals to 'mydata' your index will become 'mydata-YYYY.MM.DD'. The last string appended belongs to the date when the data is being generated. Default: 'logstash'
        :param logstash_prefix_key: When included: the value in the record that belongs to the key will be looked up and over-write the ``logstashPrefix`` for index generation. If the key/value is not found in the record then the ``logstashPrefix`` option will act as a fallback. Nested keys are not supported (if desired, you can use the nest filter plugin to remove nesting)
        :param path: OpenSearch accepts new data on HTTP query path "/_bulk". But it is also possible to serve OpenSearch behind a reverse proxy on a subpath. This option defines such path on the fluent-bit side. It simply adds a path prefix in the indexing HTTP POST URI..
        :param pipeline: OpenSearch allows to setup filters called pipelines. This option allows to define which pipeline the database should use.
        :param port: TCP port of the target OpenSearch instance. Default: 9200
        :param replace_dots: When enabled, replace field name dots with underscore. Default: false
        :param suppress_type_name: When enabled, mapping types is removed and ``type`` option is ignored. Default: false
        :param tag_key: When ``includeTagKey`` is enabled, this property defines the key name for the tag. Default: '_flb-key'
        :param time_key: When ``logstashFormat`` is enabled, each record will get a new timestamp field. The``timeKey`` property defines the name of that field. Default: '
        :param time_key_format: When ``logstashFormat`` is enabled, this property defines the format of the timestamp. Default: '%Y-%m-%dT%H:%M:%S'
        :param time_key_nanos: When ``logstashFormat`` is enabled, enabling this property sends nanosecond precision timestamps. Default: false
        :param trace_error: When enabled print the OpenSearch API calls to stdout when OpenSearch returns an error (for diag only). Default: false
        :param trace_output: When enabled print the OpenSearch API calls to stdout (for diag only). Default: false
        :param type: Type name. Default: '_doc'
        :param workers: Enables dedicated thread(s) for this output. Default: 2
        :param write_operation: Operation to use to write in bulk requests. Default: 'create'

        :see: `OpenSearch Plugin Documention <https://docs.fluentbit.io/manual/pipeline/outputs/opensearch>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitOpenSearchOutputOptions.__init__)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument aws_auth", value=aws_auth, expected_type=type_hints["aws_auth"])
            check_type(argname="argument aws_external_id", value=aws_external_id, expected_type=type_hints["aws_external_id"])
            check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
            check_type(argname="argument aws_role", value=aws_role, expected_type=type_hints["aws_role"])
            check_type(argname="argument aws_sts_endpoint", value=aws_sts_endpoint, expected_type=type_hints["aws_sts_endpoint"])
            check_type(argname="argument buffer_size", value=buffer_size, expected_type=type_hints["buffer_size"])
            check_type(argname="argument current_time_index", value=current_time_index, expected_type=type_hints["current_time_index"])
            check_type(argname="argument generate_id", value=generate_id, expected_type=type_hints["generate_id"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument http_passwd", value=http_passwd, expected_type=type_hints["http_passwd"])
            check_type(argname="argument http_user", value=http_user, expected_type=type_hints["http_user"])
            check_type(argname="argument id_key", value=id_key, expected_type=type_hints["id_key"])
            check_type(argname="argument include_tag_key", value=include_tag_key, expected_type=type_hints["include_tag_key"])
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument logstash_date_format", value=logstash_date_format, expected_type=type_hints["logstash_date_format"])
            check_type(argname="argument logstash_format", value=logstash_format, expected_type=type_hints["logstash_format"])
            check_type(argname="argument logstash_prefix", value=logstash_prefix, expected_type=type_hints["logstash_prefix"])
            check_type(argname="argument logstash_prefix_key", value=logstash_prefix_key, expected_type=type_hints["logstash_prefix_key"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument pipeline", value=pipeline, expected_type=type_hints["pipeline"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument replace_dots", value=replace_dots, expected_type=type_hints["replace_dots"])
            check_type(argname="argument suppress_type_name", value=suppress_type_name, expected_type=type_hints["suppress_type_name"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument time_key", value=time_key, expected_type=type_hints["time_key"])
            check_type(argname="argument time_key_format", value=time_key_format, expected_type=type_hints["time_key_format"])
            check_type(argname="argument time_key_nanos", value=time_key_nanos, expected_type=type_hints["time_key_nanos"])
            check_type(argname="argument trace_error", value=trace_error, expected_type=type_hints["trace_error"])
            check_type(argname="argument trace_output", value=trace_output, expected_type=type_hints["trace_output"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument workers", value=workers, expected_type=type_hints["workers"])
            check_type(argname="argument write_operation", value=write_operation, expected_type=type_hints["write_operation"])
        self._values: typing.Dict[str, typing.Any] = {
            "domain": domain,
        }
        if match is not None:
            self._values["match"] = match
        if aws_auth is not None:
            self._values["aws_auth"] = aws_auth
        if aws_external_id is not None:
            self._values["aws_external_id"] = aws_external_id
        if aws_region is not None:
            self._values["aws_region"] = aws_region
        if aws_role is not None:
            self._values["aws_role"] = aws_role
        if aws_sts_endpoint is not None:
            self._values["aws_sts_endpoint"] = aws_sts_endpoint
        if buffer_size is not None:
            self._values["buffer_size"] = buffer_size
        if current_time_index is not None:
            self._values["current_time_index"] = current_time_index
        if generate_id is not None:
            self._values["generate_id"] = generate_id
        if host is not None:
            self._values["host"] = host
        if http_passwd is not None:
            self._values["http_passwd"] = http_passwd
        if http_user is not None:
            self._values["http_user"] = http_user
        if id_key is not None:
            self._values["id_key"] = id_key
        if include_tag_key is not None:
            self._values["include_tag_key"] = include_tag_key
        if index is not None:
            self._values["index"] = index
        if logstash_date_format is not None:
            self._values["logstash_date_format"] = logstash_date_format
        if logstash_format is not None:
            self._values["logstash_format"] = logstash_format
        if logstash_prefix is not None:
            self._values["logstash_prefix"] = logstash_prefix
        if logstash_prefix_key is not None:
            self._values["logstash_prefix_key"] = logstash_prefix_key
        if path is not None:
            self._values["path"] = path
        if pipeline is not None:
            self._values["pipeline"] = pipeline
        if port is not None:
            self._values["port"] = port
        if replace_dots is not None:
            self._values["replace_dots"] = replace_dots
        if suppress_type_name is not None:
            self._values["suppress_type_name"] = suppress_type_name
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if time_key is not None:
            self._values["time_key"] = time_key
        if time_key_format is not None:
            self._values["time_key_format"] = time_key_format
        if time_key_nanos is not None:
            self._values["time_key_nanos"] = time_key_nanos
        if trace_error is not None:
            self._values["trace_error"] = trace_error
        if trace_output is not None:
            self._values["trace_output"] = trace_output
        if type is not None:
            self._values["type"] = type
        if workers is not None:
            self._values["workers"] = workers
        if write_operation is not None:
            self._values["write_operation"] = write_operation

    @builtins.property
    def match(self) -> typing.Optional[FluentBitMatch]:
        '''The pattern to match for records that this output should apply to.'''
        result = self._values.get("match")
        return typing.cast(typing.Optional[FluentBitMatch], result)

    @builtins.property
    def domain(self) -> aws_cdk.aws_opensearchservice.IDomain:
        '''The Opensearch domain to which logs should be shipped.'''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(aws_cdk.aws_opensearchservice.IDomain, result)

    @builtins.property
    def aws_auth(self) -> typing.Optional[builtins.bool]:
        '''Enable AWS Sigv4 Authentication for Amazon OpenSearch Service.

        :default: false
        '''
        result = self._values.get("aws_auth")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def aws_external_id(self) -> typing.Optional[builtins.str]:
        '''External ID for the AWS IAM Role specified with ``awsRole``.'''
        result = self._values.get("aws_external_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_region(self) -> typing.Optional[builtins.str]:
        '''Specify the AWS region for Amazon OpenSearch Service.'''
        result = self._values.get("aws_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''AWS IAM Role to assume to put records to your Amazon cluster.'''
        result = self._values.get("aws_role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    @builtins.property
    def aws_sts_endpoint(self) -> typing.Optional[builtins.str]:
        '''Specify the custom sts endpoint to be used with STS API for Amazon OpenSearch Service.'''
        result = self._values.get("aws_sts_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def buffer_size(self) -> typing.Optional[OpenSearchOutputBufferSize]:
        '''Specify the buffer size used to read the response from the OpenSearch HTTP service.

        This option is useful for debugging purposes where is
        required to read full responses, note that response size grows depending
        of the number of records inserted.
        '''
        result = self._values.get("buffer_size")
        return typing.cast(typing.Optional[OpenSearchOutputBufferSize], result)

    @builtins.property
    def current_time_index(self) -> typing.Optional[builtins.bool]:
        '''Use current time for index generation instead of message record.

        :default: false
        '''
        result = self._values.get("current_time_index")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def generate_id(self) -> typing.Optional[builtins.bool]:
        '''When enabled, generate ``_id`` for outgoing records.

        This prevents duplicate
        records when retrying.
        '''
        result = self._values.get("generate_id")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''IP address or hostname of the target OpenSearch instance.'''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_passwd(self) -> typing.Optional[builtins.str]:
        '''Password for user defined in ``httpUser``.'''
        result = self._values.get("http_passwd")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_user(self) -> typing.Optional[builtins.str]:
        '''Optional username credential for access.'''
        result = self._values.get("http_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id_key(self) -> typing.Optional[builtins.str]:
        '''If set, ``_id`` will be the value of the key from incoming record and ``generateId`` option is ignored.'''
        result = self._values.get("id_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_tag_key(self) -> typing.Optional[builtins.bool]:
        '''When enabled, it append the Tag name to the record.'''
        result = self._values.get("include_tag_key")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def index(self) -> typing.Optional[builtins.str]:
        '''Index name.

        :default: 'fluent-bit
        '''
        result = self._values.get("index")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logstash_date_format(self) -> typing.Optional[builtins.str]:
        '''Time format (based on strftime) to generate the second part of the Index name.

        :default: '%Y.%m.%d'

        :see: `strftime <http://man7.org/linux/man-pages/man3/strftime.3.html>`_
        '''
        result = self._values.get("logstash_date_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logstash_format(self) -> typing.Optional[builtins.bool]:
        '''Enable Logstash format compatibility.

        :default: false
        '''
        result = self._values.get("logstash_format")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def logstash_prefix(self) -> typing.Optional[builtins.str]:
        '''When ``logstashFormat`` is enabled, the Index name is composed using a prefix and the date, e.g: If ``logstashPrefix`` is equals to 'mydata' your index will become 'mydata-YYYY.MM.DD'.

        The last string appended belongs to the date when the data is being
        generated.

        :default: 'logstash'
        '''
        result = self._values.get("logstash_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logstash_prefix_key(self) -> typing.Optional[builtins.str]:
        '''When included: the value in the record that belongs to the key will be looked up and over-write the ``logstashPrefix`` for index generation.

        If
        the key/value is not found in the record then the ``logstashPrefix`` option
        will act as a fallback.

        Nested keys are not supported (if desired, you can use the nest filter
        plugin to remove nesting)
        '''
        result = self._values.get("logstash_prefix_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''OpenSearch accepts new data on HTTP query path "/_bulk".

        But it is also
        possible to serve OpenSearch behind a reverse proxy on a subpath. This
        option defines such path on the fluent-bit side. It simply adds a path
        prefix in the indexing HTTP POST URI..
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pipeline(self) -> typing.Optional[builtins.str]:
        '''OpenSearch allows to setup filters called pipelines.

        This option allows
        to define which pipeline the database should use.
        '''
        result = self._values.get("pipeline")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''TCP port of the target OpenSearch instance.

        :default: 9200
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def replace_dots(self) -> typing.Optional[builtins.bool]:
        '''When enabled, replace field name dots with underscore.

        :default: false
        '''
        result = self._values.get("replace_dots")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def suppress_type_name(self) -> typing.Optional[builtins.bool]:
        '''When enabled, mapping types is removed and ``type`` option is ignored.

        :default: false
        '''
        result = self._values.get("suppress_type_name")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''When ``includeTagKey`` is enabled, this property defines the key name for the tag.

        :default: '_flb-key'
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_key(self) -> typing.Optional[builtins.str]:
        '''When ``logstashFormat`` is enabled, each record will get a new timestamp field.

        The``timeKey`` property defines the name of that field.

        :default: '

        :timestamp: '
        '''
        result = self._values.get("time_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_key_format(self) -> typing.Optional[builtins.str]:
        '''When ``logstashFormat`` is enabled, this property defines the format of the timestamp.

        :default: '%Y-%m-%dT%H:%M:%S'

        :see: `strftime <http://man7.org/linux/man-pages/man3/strftime.3.html>`_
        '''
        result = self._values.get("time_key_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_key_nanos(self) -> typing.Optional[builtins.bool]:
        '''When ``logstashFormat`` is enabled, enabling this property sends nanosecond precision timestamps.

        :default: false
        '''
        result = self._values.get("time_key_nanos")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def trace_error(self) -> typing.Optional[builtins.bool]:
        '''When enabled print the OpenSearch API calls to stdout when OpenSearch returns an error (for diag only).

        :default: false
        '''
        result = self._values.get("trace_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def trace_output(self) -> typing.Optional[builtins.bool]:
        '''When enabled print the OpenSearch API calls to stdout (for diag only).

        :default: false
        '''
        result = self._values.get("trace_output")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type name.

        :default: '_doc'
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workers(self) -> typing.Optional[jsii.Number]:
        '''Enables dedicated thread(s) for this output.

        :default: 2
        '''
        result = self._values.get("workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def write_operation(self) -> typing.Optional[builtins.str]:
        '''Operation to use to write in bulk requests.

        :default: 'create'
        '''
        result = self._values.get("write_operation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FluentBitOpenSearchOutputOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IFluentBitPlugin)
class FluentBitPlugin(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-extensions.k8s_aws.FluentBitPlugin",
):
    '''A Fluent Bit plugin that allows for configuration of options and can be used to configure logging from containers.'''

    def __init__(self, *, name: builtins.str, plugin_type: FluentBitPluginType) -> None:
        '''Creates a new instance of the FluentBitPlugin class.

        :param name: The name of the fluent bit plugin.
        :param plugin_type: Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.
        '''
        options = FluentBitPluginCommonOptions(name=name, plugin_type=plugin_type)

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, scope: constructs.IConstruct) -> ResolvedFluentBitConfiguration:
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.

        :param scope: The construct configuring logging using Fluent Bit.

        :return:

        A configuration for the plugin that con be used by the resource
        configuring logging.
        '''
        ...

    @jsii.member(jsii_name="renderConfigFile")
    def _render_config_file(
        self,
        config: typing.Mapping[builtins.str, typing.Any],
    ) -> builtins.str:
        '''
        :param config: The configuration properties to render into a Fluent Bit configuration file.

        :return: A fluent bit config file representation of the passed properties.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitPlugin._render_config_file)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
        return typing.cast(builtins.str, jsii.invoke(self, "renderConfigFile", [config]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the fluent bit plugin.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="pluginType")
    def plugin_type(self) -> builtins.str:
        '''The type of fluent bit plugin.'''
        return typing.cast(builtins.str, jsii.get(self, "pluginType"))


class _FluentBitPluginProxy(FluentBitPlugin):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> ResolvedFluentBitConfiguration:
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.

        :param scope: The construct configuring logging using Fluent Bit.

        :return:

        A configuration for the plugin that con be used by the resource
        configuring logging.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitPlugin.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(ResolvedFluentBitConfiguration, jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, FluentBitPlugin).__jsii_proxy_class__ = lambda : _FluentBitPluginProxy


@jsii.interface(jsii_type="cdk-extensions.k8s_aws.IFluentBitFilterPlugin")
class IFluentBitFilterPlugin(IFluentBitPlugin, typing_extensions.Protocol):
    '''Represents a Fluent Bit plugin that controls log filtering and metadata.'''

    pass


class _IFluentBitFilterPluginProxy(
    jsii.proxy_for(IFluentBitPlugin), # type: ignore[misc]
):
    '''Represents a Fluent Bit plugin that controls log filtering and metadata.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.k8s_aws.IFluentBitFilterPlugin"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFluentBitFilterPlugin).__jsii_proxy_class__ = lambda : _IFluentBitFilterPluginProxy


@jsii.interface(jsii_type="cdk-extensions.k8s_aws.IFluentBitOutputPlugin")
class IFluentBitOutputPlugin(IFluentBitPlugin, typing_extensions.Protocol):
    '''Represents a Fluent Bit plugin that controls log output to a given destination.'''

    pass


class _IFluentBitOutputPluginProxy(
    jsii.proxy_for(IFluentBitPlugin), # type: ignore[misc]
):
    '''Represents a Fluent Bit plugin that controls log output to a given destination.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.k8s_aws.IFluentBitOutputPlugin"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFluentBitOutputPlugin).__jsii_proxy_class__ = lambda : _IFluentBitOutputPluginProxy


@jsii.interface(jsii_type="cdk-extensions.k8s_aws.IFluentBitParserPlugin")
class IFluentBitParserPlugin(IFluentBitPlugin, typing_extensions.Protocol):
    '''Represents a Fluent Bit plugin that parses inbound records to populate fields.'''

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        ...


class _IFluentBitParserPluginProxy(
    jsii.proxy_for(IFluentBitPlugin), # type: ignore[misc]
):
    '''Represents a Fluent Bit plugin that parses inbound records to populate fields.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.k8s_aws.IFluentBitParserPlugin"

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "format"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFluentBitParserPlugin).__jsii_proxy_class__ = lambda : _IFluentBitParserPluginProxy


class SecretsManagerSecretStore(
    AwsSecretStore,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.SecretsManagerSecretStore",
):
    '''A secret store that allows secrets from AWS Secrets Managers to be synchronized into Kubernetes as Kubernetes secrets.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster: aws_cdk.aws_eks.ICluster,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the SecretsManagerSecretStore class.

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the resource and used in resource naming. Must be unique within the context of 'scope'.
        :param cluster: The EKS cluster where the secret store should be created.
        :param name: A human friendly name for the secret store.
        :param namespace: The Kubernetes namespace where the secret store should be created.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SecretsManagerSecretStore.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SecretsManagerSecretStoreProps(
            cluster=cluster,
            name=name,
            namespace=namespace,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addSecret")
    def add_secret(
        self,
        id: builtins.str,
        secret: aws_cdk.aws_secretsmanager.ISecret,
        *,
        fields: typing.Optional[typing.Sequence[typing.Union[SecretFieldReference, typing.Dict[str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> ExternalSecret:
        '''Registers a new Secrets Manager secret to be synchronized into Kubernetes.

        :param id: The ID of the secret import configuration in the CDK construct tree. The configuration is placed under the Secrets Manager secret it synchronizes and so must be unique per secret.
        :param secret: The Secrets Manager secret to synchronize into Kubernetes.
        :param fields: A collection of field mappings that tells the external secrets operator the structure of the Kubernetes secret to create and which how fields in the Kubernetes secret should map to fields in the secret from the external secret provider. Default: The Kubernetes secret will mirror the fields from the secret in the external provider.
        :param name: The name of the Kubernetes secret that will be created, as it will appear from within the Kubernetes cluster. Default: A name will be auto-generated.

        :return: The external secret configuration that was added.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SecretsManagerSecretStore.add_secret)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        options = ExternalSecretOptions(fields=fields, name=name)

        return typing.cast(ExternalSecret, jsii.invoke(self, "addSecret", [id, secret, options]))


class SsmParameterSecretStore(
    AwsSecretStore,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.SsmParameterSecretStore",
):
    '''A secret store that allows parameters from Systems Manager to be synchronized into Kubernetes as Kubernetes secrets.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster: aws_cdk.aws_eks.ICluster,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the SsmParameterSecretStore class.

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the resource and used in resource naming. Must be unique within the context of 'scope'.
        :param cluster: The EKS cluster where the secret store should be created.
        :param name: A human friendly name for the secret store.
        :param namespace: The Kubernetes namespace where the secret store should be created.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SsmParameterSecretStore.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SsmParameterSecretStoreProps(
            cluster=cluster,
            name=name,
            namespace=namespace,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addSecret")
    def add_secret(
        self,
        id: builtins.str,
        parameter: aws_cdk.aws_ssm.IParameter,
        *,
        fields: typing.Optional[typing.Sequence[typing.Union[SecretFieldReference, typing.Dict[str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> ExternalSecret:
        '''Registers a new SSSM parameter to be synchronized into Kubernetes.

        :param id: The ID of the secret import configuration in the CDK construct tree. The configuration is placed under the SSM parameter it synchronizes and so must be unique per secret.
        :param parameter: The SSM parameter to synchronize into Kubernetes.
        :param fields: A collection of field mappings that tells the external secrets operator the structure of the Kubernetes secret to create and which how fields in the Kubernetes secret should map to fields in the secret from the external secret provider. Default: The Kubernetes secret will mirror the fields from the secret in the external provider.
        :param name: The name of the Kubernetes secret that will be created, as it will appear from within the Kubernetes cluster. Default: A name will be auto-generated.

        :return: The external secret configuration that was added.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SsmParameterSecretStore.add_secret)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
        options = ExternalSecretOptions(fields=fields, name=name)

        return typing.cast(ExternalSecret, jsii.invoke(self, "addSecret", [id, parameter, options]))


@jsii.implements(IFluentBitFilterPlugin)
class FluentBitFilterPluginBase(
    FluentBitPlugin,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-extensions.k8s_aws.FluentBitFilterPluginBase",
):
    def __init__(
        self,
        name: builtins.str,
        *,
        match: typing.Optional[FluentBitMatch] = None,
    ) -> None:
        '''Creates a new instance of the FluentBitOutputPlugin class.

        :param name: The name of the output plugin to configure.
        :param match: The pattern to match for records that this output should apply to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitFilterPluginBase.__init__)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        options = FluentBitFilterPluginCommonOptions(match=match)

        jsii.create(self.__class__, self, [name, options])

    @jsii.member(jsii_name="renderConfigFile")
    def _render_config_file(
        self,
        config: typing.Mapping[builtins.str, typing.Any],
    ) -> builtins.str:
        '''Renders a Fluent Bit configuration file for the plugin.

        :param config: The configuration options to render into a configuration file.

        :return: A rendered plugin configuration file.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitFilterPluginBase._render_config_file)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
        return typing.cast(builtins.str, jsii.invoke(self, "renderConfigFile", [config]))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> FluentBitMatch:
        '''The pattern to match for records that this output should apply to.

        :group: Inputs
        '''
        return typing.cast(FluentBitMatch, jsii.get(self, "match"))


class _FluentBitFilterPluginBaseProxy(
    FluentBitFilterPluginBase,
    jsii.proxy_for(FluentBitPlugin), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, FluentBitFilterPluginBase).__jsii_proxy_class__ = lambda : _FluentBitFilterPluginBaseProxy


class FluentBitGrepFilter(
    FluentBitFilterPluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitGrepFilter",
):
    '''A Fluent Bit filter that allows log records to be kept or discarded based on whether they match a given regular expression or not.'''

    def __init__(
        self,
        *,
        pattern: typing.Union[FluentBitGrepRegex, typing.Dict[str, typing.Any]],
        match: typing.Optional[FluentBitMatch] = None,
    ) -> None:
        '''Creates a new instance of the FluentBitKinesisFirehoseOutput class.

        :param pattern: The pattern to use for filtering records processed by the plugin.
        :param match: The pattern to match for records that this output should apply to.
        '''
        options = FluentBitGrepFilterOptions(pattern=pattern, match=match)

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: constructs.IConstruct) -> ResolvedFluentBitConfiguration:
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.

        :param _scope: The construct configuring logging using Fluent Bit.

        :return:

        A configuration for the plugin that con be used by the resource
        configuring logging.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitGrepFilter.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(ResolvedFluentBitConfiguration, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> FluentBitGrepRegex:
        '''The pattern to use for filtering records processed by the plugin.

        :group: Inputs
        '''
        return typing.cast(FluentBitGrepRegex, jsii.get(self, "pattern"))


class FluentBitKubernetesFilter(
    FluentBitFilterPluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitKubernetesFilter",
):
    '''A Fluent Bit filter that allows log records to be annotated with Kubernetes metadata based on the containers that generated them.'''

    def __init__(
        self,
        *,
        annotations: typing.Optional[builtins.bool] = None,
        buffer_size: typing.Optional[_DataSize_d20aaece] = None,
        cache_use_docker_id: typing.Optional[builtins.bool] = None,
        dns_retries: typing.Optional[jsii.Number] = None,
        dns_wait_time: typing.Optional[aws_cdk.Duration] = None,
        dummy_meta: typing.Optional[builtins.bool] = None,
        k8s_logging_exclude: typing.Optional[builtins.bool] = None,
        k8s_logging_parser: typing.Optional[builtins.bool] = None,
        keep_log: typing.Optional[builtins.bool] = None,
        kube_ca_file: typing.Optional[builtins.str] = None,
        kube_ca_path: typing.Optional[builtins.str] = None,
        kubelet_host: typing.Optional[builtins.str] = None,
        kubelet_port: typing.Optional[jsii.Number] = None,
        kube_meta_cache_ttl: typing.Optional[aws_cdk.Duration] = None,
        kube_meta_preload_cache_dir: typing.Optional[builtins.str] = None,
        kube_tag_prefix: typing.Optional[builtins.str] = None,
        kube_token_command: typing.Optional[builtins.str] = None,
        kube_token_file: typing.Optional[builtins.str] = None,
        kube_token_ttl: typing.Optional[aws_cdk.Duration] = None,
        kube_url: typing.Optional[builtins.str] = None,
        labels: typing.Optional[builtins.bool] = None,
        merge_log: typing.Optional[builtins.bool] = None,
        merge_log_key: typing.Optional[builtins.str] = None,
        merge_log_trim: typing.Optional[builtins.bool] = None,
        merge_parser: typing.Optional[builtins.str] = None,
        regex_parser: typing.Optional[builtins.str] = None,
        tls_debug: typing.Optional[jsii.Number] = None,
        tls_verify: typing.Optional[builtins.bool] = None,
        use_journal: typing.Optional[builtins.bool] = None,
        use_kubelet: typing.Optional[builtins.bool] = None,
        match: typing.Optional[FluentBitMatch] = None,
    ) -> None:
        '''Creates a new instance of the FluentBitKubernetesFilter class.

        :param annotations: Include Kubernetes resource annotations in the extra metadata. Default: true
        :param buffer_size: Set the buffer size for HTTP client when reading responses from Kubernetes API server. A value of 0 results in no limit, and the buffer will expand as-needed. Note that if pod specifications exceed the buffer limit, the API response will be discarded when retrieving metadata, and some kubernetes metadata will fail to be injected to the logs. Default: 32k
        :param cache_use_docker_id: When enabled, metadata will be fetched from K8s when docker_id is changed. Default: false
        :param dns_retries: DNS lookup retries N times until the network starts working. Default: 6
        :param dns_wait_time: DNS lookup interval between network status checks. Default: 30 seconds
        :param dummy_meta: If set, use dummy-meta data (for test/dev purposes). Default: false
        :param k8s_logging_exclude: Allow Kubernetes Pods to exclude their logs from the log processor. Default: false
        :param k8s_logging_parser: Allow Kubernetes Pods to suggest a pre-defined Parser. Default: false
        :param keep_log: When ``keepLog`` is disabled, the log field is removed from the incoming message once it has been successfully merged (``mergeLog`` must be enabled as well). Default: true
        :param kube_ca_file: CA certificate file. Default: '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
        :param kube_ca_path: Absolute path to scan for certificate files.
        :param kubelet_host: Kubelet host using for HTTP request, this only works when ``useKubelet`` is enabled.
        :param kubelet_port: Kubelet port using for HTTP request, this only works when ``useKubelet`` is enabled. Default: 10250
        :param kube_meta_cache_ttl: Configurable TTL for K8s cached metadata. By default, it is set to 0 which means TTL for cache entries is disabled and cache entries are evicted at random when capacity is reached. In order to enable this option, you should set the number to a time interval. Default: 0
        :param kube_meta_preload_cache_dir: If set, Kubernetes meta-data can be cached/pre-loaded from files in JSON format in this directory, named as namespace-pod.meta.
        :param kube_tag_prefix: When the source records comes from Tail input plugin, this option allows to specify what's the prefix used in Tail configuration. Default: 'kube.var.log.containers.'
        :param kube_token_command: Command to get Kubernetes authorization token. If you want to manually choose a command to get it, you can set the command here. For example, run running the following to get the token using aws-cli:: aws-iam-authenticator -i your-cluster-name token --token-only This option is currently Linux-only.
        :param kube_token_file: Token file. Default: '/var/run/secrets/kubernetes.io/serviceaccount/token'
        :param kube_token_ttl: Configurable 'time to live' for the K8s token. After this time, the token is reloaded from ``kubeTokenFile`` or the ``kubeTokenCommand``. Default: 10 minutes
        :param kube_url: API Server end-point. Default: 'https://kubernetes.default.svc/'
        :param labels: Include Kubernetes resource labels in the extra metadata. Default: true
        :param merge_log: When enabled, it checks if the ``log`` field content is a JSON string map, if so, it append the map fields as part of the log structure. Default: false
        :param merge_log_key: When ``mergeLog`` is enabled, the filter tries to assume the ``log`` field from the incoming message is a JSON string message and make a structured representation of it at the same level of the ``log`` field in the map. Now if ``mergeLogKey`` is set (a string name), all the new structured fields taken from the original ``log`` content are inserted under the new key.
        :param merge_log_trim: When Merge_Log is enabled, trim (remove possible \\n or \\r) field values. Default: true
        :param merge_parser: Optional parser name to specify how to parse the data contained in the log key. Recommended use is for developers or testing only.
        :param regex_parser: Set an alternative Parser to process record Tag and extract pod_name, namespace_name, container_name and docker_id. The parser must be registered in a parsers file.
        :param tls_debug: Debug level between 0 (nothing) and 4 (every detail). Default: -1
        :param tls_verify: When enabled, turns on certificate validation when connecting to the Kubernetes API server. Default: true
        :param use_journal: When enabled, the filter reads logs coming in Journald format. Default: false
        :param use_kubelet: This is an optional feature flag to get metadata information from kubelet instead of calling Kube Server API to enhance the log. Default: false
        :param match: The pattern to match for records that this output should apply to.
        '''
        options = FluentBitKubernetesFilterOptions(
            annotations=annotations,
            buffer_size=buffer_size,
            cache_use_docker_id=cache_use_docker_id,
            dns_retries=dns_retries,
            dns_wait_time=dns_wait_time,
            dummy_meta=dummy_meta,
            k8s_logging_exclude=k8s_logging_exclude,
            k8s_logging_parser=k8s_logging_parser,
            keep_log=keep_log,
            kube_ca_file=kube_ca_file,
            kube_ca_path=kube_ca_path,
            kubelet_host=kubelet_host,
            kubelet_port=kubelet_port,
            kube_meta_cache_ttl=kube_meta_cache_ttl,
            kube_meta_preload_cache_dir=kube_meta_preload_cache_dir,
            kube_tag_prefix=kube_tag_prefix,
            kube_token_command=kube_token_command,
            kube_token_file=kube_token_file,
            kube_token_ttl=kube_token_ttl,
            kube_url=kube_url,
            labels=labels,
            merge_log=merge_log,
            merge_log_key=merge_log_key,
            merge_log_trim=merge_log_trim,
            merge_parser=merge_parser,
            regex_parser=regex_parser,
            tls_debug=tls_debug,
            tls_verify=tls_verify,
            use_journal=use_journal,
            use_kubelet=use_kubelet,
            match=match,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: constructs.IConstruct) -> ResolvedFluentBitConfiguration:
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.

        :param _scope: The construct configuring logging using Fluent Bit.

        :return:

        A configuration for the plugin that con be used by the resource
        configuring logging.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitKubernetesFilter.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(ResolvedFluentBitConfiguration, jsii.invoke(self, "bind", [_scope]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PLUGIN_NAME")
    def PLUGIN_NAME(cls) -> builtins.str:
        '''The name of the plugin as it will appear in the fluent bit configuration.'''
        return typing.cast(builtins.str, jsii.sget(cls, "PLUGIN_NAME"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Optional[builtins.bool]:
        '''Include Kubernetes resource annotations in the extra metadata.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "annotations"))

    @builtins.property
    @jsii.member(jsii_name="bufferSize")
    def buffer_size(self) -> typing.Optional[_DataSize_d20aaece]:
        '''Set the buffer size for HTTP client when reading responses from Kubernetes API server.

        A value of 0 results in no limit, and the buffer will expand as-needed.

        Note that if pod specifications exceed the buffer limit, the API
        response will be discarded when retrieving metadata, and some kubernetes
        metadata will fail to be injected to the logs.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[_DataSize_d20aaece], jsii.get(self, "bufferSize"))

    @builtins.property
    @jsii.member(jsii_name="cacheUseDockerId")
    def cache_use_docker_id(self) -> typing.Optional[builtins.bool]:
        '''When enabled, metadata will be fetched from K8s when docker_id is changed.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "cacheUseDockerId"))

    @builtins.property
    @jsii.member(jsii_name="dnsRetries")
    def dns_retries(self) -> typing.Optional[jsii.Number]:
        '''DNS lookup retries N times until the network starts working.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dnsRetries"))

    @builtins.property
    @jsii.member(jsii_name="dnsWaitTime")
    def dns_wait_time(self) -> typing.Optional[aws_cdk.Duration]:
        '''DNS lookup interval between network status checks.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[aws_cdk.Duration], jsii.get(self, "dnsWaitTime"))

    @builtins.property
    @jsii.member(jsii_name="dummyMeta")
    def dummy_meta(self) -> typing.Optional[builtins.bool]:
        '''If set, use dummy-meta data (for test/dev purposes).

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "dummyMeta"))

    @builtins.property
    @jsii.member(jsii_name="k8sLoggingExclude")
    def k8s_logging_exclude(self) -> typing.Optional[builtins.bool]:
        '''Allow Kubernetes Pods to exclude their logs from the log processor.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "k8sLoggingExclude"))

    @builtins.property
    @jsii.member(jsii_name="k8sLoggingParser")
    def k8s_logging_parser(self) -> typing.Optional[builtins.bool]:
        '''Allow Kubernetes Pods to suggest a pre-defined Parser.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "k8sLoggingParser"))

    @builtins.property
    @jsii.member(jsii_name="keepLog")
    def keep_log(self) -> typing.Optional[builtins.bool]:
        '''When ``keepLog`` is disabled, the log field is removed from the incoming message once it has been successfully merged (``mergeLog`` must be enabled as well).

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "keepLog"))

    @builtins.property
    @jsii.member(jsii_name="kubeCaFile")
    def kube_ca_file(self) -> typing.Optional[builtins.str]:
        '''CA certificate file.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubeCaFile"))

    @builtins.property
    @jsii.member(jsii_name="kubeCaPath")
    def kube_ca_path(self) -> typing.Optional[builtins.str]:
        '''Absolute path to scan for certificate files.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubeCaPath"))

    @builtins.property
    @jsii.member(jsii_name="kubeletHost")
    def kubelet_host(self) -> typing.Optional[builtins.str]:
        '''Kubelet host using for HTTP request, this only works when ``useKubelet`` is enabled.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubeletHost"))

    @builtins.property
    @jsii.member(jsii_name="kubeletPort")
    def kubelet_port(self) -> typing.Optional[jsii.Number]:
        '''Kubelet port using for HTTP request, this only works when ``useKubelet`` is enabled.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "kubeletPort"))

    @builtins.property
    @jsii.member(jsii_name="kubeMetaCacheTtl")
    def kube_meta_cache_ttl(self) -> typing.Optional[aws_cdk.Duration]:
        '''Configurable TTL for K8s cached metadata.

        By default, it is set to 0 which means TTL for cache entries is disabled
        and cache entries are evicted at random when capacity is reached.

        In order to enable this option, you should set the number to a time
        interval.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[aws_cdk.Duration], jsii.get(self, "kubeMetaCacheTtl"))

    @builtins.property
    @jsii.member(jsii_name="kubeMetaPreloadCacheDir")
    def kube_meta_preload_cache_dir(self) -> typing.Optional[builtins.str]:
        '''If set, Kubernetes meta-data can be cached/pre-loaded from files in JSON format in this directory, named as namespace-pod.meta.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubeMetaPreloadCacheDir"))

    @builtins.property
    @jsii.member(jsii_name="kubeTagPrefix")
    def kube_tag_prefix(self) -> typing.Optional[builtins.str]:
        '''When the source records comes from Tail input plugin, this option allows to specify what's the prefix used in Tail configuration.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubeTagPrefix"))

    @builtins.property
    @jsii.member(jsii_name="kubeTokenCommand")
    def kube_token_command(self) -> typing.Optional[builtins.str]:
        '''Command to get Kubernetes authorization token.

        If you want to manually choose a command to get it, you can set the
        command here.

        For example, run running the following to get the token using aws-cli::

           aws-iam-authenticator -i your-cluster-name token --token-only

        This option is currently Linux-only.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubeTokenCommand"))

    @builtins.property
    @jsii.member(jsii_name="kubeTokenFile")
    def kube_token_file(self) -> typing.Optional[builtins.str]:
        '''Token file.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubeTokenFile"))

    @builtins.property
    @jsii.member(jsii_name="kubeTokenTtl")
    def kube_token_ttl(self) -> typing.Optional[aws_cdk.Duration]:
        '''Configurable 'time to live' for the K8s token.

        After this time, the token is reloaded from ``kubeTokenFile`` or the
        ``kubeTokenCommand``.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[aws_cdk.Duration], jsii.get(self, "kubeTokenTtl"))

    @builtins.property
    @jsii.member(jsii_name="kubeUrl")
    def kube_url(self) -> typing.Optional[builtins.str]:
        '''API Server end-point.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubeUrl"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Optional[builtins.bool]:
        '''Include Kubernetes resource labels in the extra metadata.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="mergeLog")
    def merge_log(self) -> typing.Optional[builtins.bool]:
        '''When enabled, it checks if the ``log`` field content is a JSON string map, if so, it append the map fields as part of the log structure.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "mergeLog"))

    @builtins.property
    @jsii.member(jsii_name="mergeLogKey")
    def merge_log_key(self) -> typing.Optional[builtins.str]:
        '''When ``mergeLog`` is enabled, the filter tries to assume the ``log`` field from the incoming message is a JSON string message and make a structured representation of it at the same level of the ``log`` field in the map.

        Now if ``mergeLogKey`` is set (a string name), all the new structured
        fields taken from the original ``log`` content are inserted under the new
        key.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mergeLogKey"))

    @builtins.property
    @jsii.member(jsii_name="mergeLogTrim")
    def merge_log_trim(self) -> typing.Optional[builtins.bool]:
        '''When Merge_Log is enabled, trim (remove possible \\n or \\r) field values.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "mergeLogTrim"))

    @builtins.property
    @jsii.member(jsii_name="mergeParser")
    def merge_parser(self) -> typing.Optional[builtins.str]:
        '''Optional parser name to specify how to parse the data contained in the log key.

        Recommended use is for developers or testing only.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mergeParser"))

    @builtins.property
    @jsii.member(jsii_name="regexParser")
    def regex_parser(self) -> typing.Optional[builtins.str]:
        '''Set an alternative Parser to process record Tag and extract pod_name, namespace_name, container_name and docker_id.

        The parser must be registered in a parsers file.

        :see: `Parsers File <https://github.com/fluent/fluent-bit/blob/master/conf/parsers.conf>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regexParser"))

    @builtins.property
    @jsii.member(jsii_name="tlsDebug")
    def tls_debug(self) -> typing.Optional[jsii.Number]:
        '''Debug level between 0 (nothing) and 4 (every detail).

        :group: Inputs
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tlsDebug"))

    @builtins.property
    @jsii.member(jsii_name="tlsVerify")
    def tls_verify(self) -> typing.Optional[builtins.bool]:
        '''When enabled, turns on certificate validation when connecting to the Kubernetes API server.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "tlsVerify"))

    @builtins.property
    @jsii.member(jsii_name="useJournal")
    def use_journal(self) -> typing.Optional[builtins.bool]:
        '''When enabled, the filter reads logs coming in Journald format.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "useJournal"))

    @builtins.property
    @jsii.member(jsii_name="useKubelet")
    def use_kubelet(self) -> typing.Optional[builtins.bool]:
        '''This is an optional feature flag to get metadata information from kubelet instead of calling Kube Server API to enhance the log.

        :see: `Kube API heavy traffic issue for large cluster <https://docs.fluentbit.io/manual/pipeline/filters/kubernetes#optional-feature-using-kubelet-to-get-metadata>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "useKubelet"))


class FluentBitModifyFilter(
    FluentBitFilterPluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitModifyFilter",
):
    '''A Fluent Bit filter that allows changing records using rules and conditions.'''

    def __init__(
        self,
        *,
        conditions: typing.Optional[typing.Sequence[ModifyCondition]] = None,
        operations: typing.Optional[typing.Sequence[ModifyOperation]] = None,
        match: typing.Optional[FluentBitMatch] = None,
    ) -> None:
        '''Creates a new instance of the FluentBitModifyFilter class.

        :param conditions: 
        :param operations: 
        :param match: The pattern to match for records that this output should apply to.
        '''
        options = FluentBitModifyFilterOptions(
            conditions=conditions, operations=operations, match=match
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="addCondition")
    def add_condition(self, condition: ModifyCondition) -> "FluentBitModifyFilter":
        '''Adds a new condition to the modify filter.

        All conditions must evaluate to ``true`` in order for operations are
        performed.

        If one or more conditions do not evaluate to true, no conditions are
        performed.

        :param condition: The condition to add to the filter.

        :return: The modify filter to which the condition was added.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitModifyFilter.add_condition)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
        return typing.cast("FluentBitModifyFilter", jsii.invoke(self, "addCondition", [condition]))

    @jsii.member(jsii_name="addOperation")
    def add_operation(self, operation: ModifyOperation) -> "FluentBitModifyFilter":
        '''Adds a new operation to the modify filter.

        :param operation: The operation to add to the filter.

        :return: The modify filter to which the operation was added.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitModifyFilter.add_operation)
            check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
        return typing.cast("FluentBitModifyFilter", jsii.invoke(self, "addOperation", [operation]))

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: constructs.IConstruct) -> ResolvedFluentBitConfiguration:
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.

        :param _scope: The construct configuring logging using Fluent Bit.

        :return:

        A configuration for the plugin that con be used by the resource
        configuring logging.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitModifyFilter.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(ResolvedFluentBitConfiguration, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> typing.List[ModifyCondition]:
        '''Collection of conditions to apply for the filter.'''
        return typing.cast(typing.List[ModifyCondition], jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(self) -> typing.List[ModifyOperation]:
        '''Collection of operations to apply for the filter.'''
        return typing.cast(typing.List[ModifyOperation], jsii.get(self, "operations"))


class FluentBitNestFilter(
    FluentBitFilterPluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitNestFilter",
):
    '''A Fluent Bit filter that allows operating on or with nested data.'''

    def __init__(
        self,
        *,
        operation: NestFilterOperation,
        add_prefix: typing.Optional[builtins.str] = None,
        remove_prefix: typing.Optional[builtins.str] = None,
        match: typing.Optional[FluentBitMatch] = None,
    ) -> None:
        '''Creates a new instance of the FluentBitNestFilter class.

        :param operation: The operation the filter will perform.
        :param add_prefix: Prefix affected keys with this string.
        :param remove_prefix: Remove prefix from affected keys if it matches this string.
        :param match: The pattern to match for records that this output should apply to.
        '''
        options = FluentBitNestFilterOptions(
            operation=operation,
            add_prefix=add_prefix,
            remove_prefix=remove_prefix,
            match=match,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: constructs.IConstruct) -> ResolvedFluentBitConfiguration:
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.

        :param _scope: The construct configuring logging using Fluent Bit.

        :return:

        A configuration for the plugin that con be used by the resource
        configuring logging.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitNestFilter.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(ResolvedFluentBitConfiguration, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="operation")
    def operation(self) -> NestFilterOperation:
        '''Operation specific details for the plugin.'''
        return typing.cast(NestFilterOperation, jsii.get(self, "operation"))

    @builtins.property
    @jsii.member(jsii_name="addPrefix")
    def add_prefix(self) -> typing.Optional[builtins.str]:
        '''Prefix affected keys with this string.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addPrefix"))

    @builtins.property
    @jsii.member(jsii_name="removePrefix")
    def remove_prefix(self) -> typing.Optional[builtins.str]:
        '''Remove prefix from affected keys if it matches this string.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "removePrefix"))


@jsii.implements(IFluentBitOutputPlugin)
class FluentBitOutputPluginBase(
    FluentBitPlugin,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-extensions.k8s_aws.FluentBitOutputPluginBase",
):
    '''Represents a Fluent Bit plugin that controls log output to a given destination.'''

    def __init__(
        self,
        name: builtins.str,
        *,
        match: typing.Optional[FluentBitMatch] = None,
    ) -> None:
        '''Creates a new instance of the FluentBitOutputPlugin class.

        :param name: The name of the output plugin to configure.
        :param match: The pattern to match for records that this output should apply to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitOutputPluginBase.__init__)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        options = FluentBitOutputPluginCommonOptions(match=match)

        jsii.create(self.__class__, self, [name, options])

    @jsii.member(jsii_name="renderConfigFile")
    def _render_config_file(
        self,
        config: typing.Mapping[builtins.str, typing.Any],
    ) -> builtins.str:
        '''Renders a Fluent Bit configuration file for the plugin.

        :param config: The configuration options to render into a configuration file.

        :return: A rendered plugin configuration file.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitOutputPluginBase._render_config_file)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
        return typing.cast(builtins.str, jsii.invoke(self, "renderConfigFile", [config]))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> FluentBitMatch:
        '''The pattern to match for records that this output should apply to.

        :group: Inputs
        '''
        return typing.cast(FluentBitMatch, jsii.get(self, "match"))


class _FluentBitOutputPluginBaseProxy(
    FluentBitOutputPluginBase,
    jsii.proxy_for(FluentBitPlugin), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, FluentBitOutputPluginBase).__jsii_proxy_class__ = lambda : _FluentBitOutputPluginBaseProxy


class FluentBitParserFilter(
    FluentBitFilterPluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitParserFilter",
):
    '''A Fluent Bit filter that allows parsing of fields in event records.'''

    def __init__(
        self,
        *,
        key_name: builtins.str,
        parsers: typing.Optional[typing.Sequence[IFluentBitParserPlugin]] = None,
        preserve_key: typing.Optional[builtins.bool] = None,
        reserve_data: typing.Optional[builtins.bool] = None,
        match: typing.Optional[FluentBitMatch] = None,
    ) -> None:
        '''Creates a new instance of the FluentBitParserFilter class.

        :param key_name: Specify field name in record to parse.
        :param parsers: The parsers to use to interpret the field.
        :param preserve_key: Keep original ``keyName`` field in the parsed result. If ``false``, the field will be removed. Default: false
        :param reserve_data: Keep all other original fields in the parsed result. If ``false``, all other original fields will be removed. Default: false
        :param match: The pattern to match for records that this output should apply to.
        '''
        options = FluentBitParserFilterOptions(
            key_name=key_name,
            parsers=parsers,
            preserve_key=preserve_key,
            reserve_data=reserve_data,
            match=match,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="addParser")
    def add_parser(self, parser: IFluentBitParserPlugin) -> "FluentBitParserFilter":
        '''Adds a new parser to apply to matched log entries.

        :param parser: The parser to use for matched log entries.

        :return: The parser filter that the parser plugin was registered with.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitParserFilter.add_parser)
            check_type(argname="argument parser", value=parser, expected_type=type_hints["parser"])
        return typing.cast("FluentBitParserFilter", jsii.invoke(self, "addParser", [parser]))

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: constructs.IConstruct) -> ResolvedFluentBitConfiguration:
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.

        :param _scope: The construct configuring logging using Fluent Bit.

        :return:

        A configuration for the plugin that con be used by the resource
        configuring logging.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitParserFilter.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(ResolvedFluentBitConfiguration, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="keyName")
    def key_name(self) -> builtins.str:
        '''Specify field name in record to parse.'''
        return typing.cast(builtins.str, jsii.get(self, "keyName"))

    @builtins.property
    @jsii.member(jsii_name="parsers")
    def parsers(self) -> typing.List[IFluentBitParserPlugin]:
        '''Collection of the parsers that should be used to evaluate the filter.'''
        return typing.cast(typing.List[IFluentBitParserPlugin], jsii.get(self, "parsers"))

    @builtins.property
    @jsii.member(jsii_name="preserveKey")
    def preserve_key(self) -> typing.Optional[builtins.bool]:
        '''Keep original ``keyName`` field in the parsed result.

        If ``false``, the field will be removed.

        :default: false
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "preserveKey"))

    @builtins.property
    @jsii.member(jsii_name="reserveData")
    def reserve_data(self) -> typing.Optional[builtins.bool]:
        '''Keep all other original fields in the parsed result.

        If ``false``, all other original fields will be removed.

        :default: false
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "reserveData"))


@jsii.implements(IFluentBitParserPlugin)
class FluentBitParserPluginBase(
    FluentBitPlugin,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-extensions.k8s_aws.FluentBitParserPluginBase",
):
    '''Represents a Fluent Bit plugin that parses inbound records to populate fields.'''

    def __init__(self, name: builtins.str, format: builtins.str) -> None:
        '''Creates a new instance of the FluentBitParserPlugin class.

        :param name: The name of the output plugin to configure.
        :param format: The data format that the parser extracts records from.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitParserPluginBase.__init__)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
        _options = FluentBitParserPluginCommonOptions()

        jsii.create(self.__class__, self, [name, format, _options])

    @jsii.member(jsii_name="renderConfigFile")
    def _render_config_file(
        self,
        config: typing.Mapping[builtins.str, typing.Any],
    ) -> builtins.str:
        '''Renders a Fluent Bit configuration file for the plugin.

        :param config: The configuration options to render into a configuration file.

        :return: A rendered plugin configuration file.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitParserPluginBase._render_config_file)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
        return typing.cast(builtins.str, jsii.invoke(self, "renderConfigFile", [config]))

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        '''The data format that the parser extracts records from.

        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "format"))


class _FluentBitParserPluginBaseProxy(
    FluentBitParserPluginBase,
    jsii.proxy_for(FluentBitPlugin), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, FluentBitParserPluginBase).__jsii_proxy_class__ = lambda : _FluentBitParserPluginBaseProxy


class FluentBitRecordModifierFilter(
    FluentBitFilterPluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitRecordModifierFilter",
):
    '''A Fluent Bit filter that allows appending fields or excluding specific fields.'''

    def __init__(
        self,
        *,
        allow: typing.Optional[typing.Sequence[builtins.str]] = None,
        records: typing.Optional[typing.Sequence[typing.Union[AppendedRecord, typing.Dict[str, typing.Any]]]] = None,
        remove: typing.Optional[typing.Sequence[builtins.str]] = None,
        match: typing.Optional[FluentBitMatch] = None,
    ) -> None:
        '''Creates a new instance of the FluentBitRecordModifierFilter class.

        :param allow: If a tag is not match, that field is removed.
        :param records: Add fields to the output.
        :param remove: If a tag is match, that field is removed.
        :param match: The pattern to match for records that this output should apply to.
        '''
        options = FluentBitRecordModifierFilterOptions(
            allow=allow, records=records, remove=remove, match=match
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="addAllow")
    def add_allow(self, tag: builtins.str) -> "FluentBitRecordModifierFilter":
        '''Adds a tag to be allowed on a matched input record.

        If a tag is not matched it is removed.

        :param tag: The tag to add to the allow list.

        :return:

        The record modifier filter that the tag plugin was registered
        with.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitRecordModifierFilter.add_allow)
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        return typing.cast("FluentBitRecordModifierFilter", jsii.invoke(self, "addAllow", [tag]))

    @jsii.member(jsii_name="addRecord")
    def add_record(
        self,
        *,
        field_name: builtins.str,
        value: builtins.str,
    ) -> "FluentBitRecordModifierFilter":
        '''Add a record to be appended to matched events.

        :param field_name: The name of the field to be added.
        :param value: The value that the added field should be set to.

        :return:

        The record modifier filter that the tag plugin was registered
        with.
        '''
        record = AppendedRecord(field_name=field_name, value=value)

        return typing.cast("FluentBitRecordModifierFilter", jsii.invoke(self, "addRecord", [record]))

    @jsii.member(jsii_name="addRemove")
    def add_remove(self, tag: builtins.str) -> "FluentBitRecordModifierFilter":
        '''Adds a tag to be removed on a matched input record.

        If a tag is matched it is removed.

        :param tag: The tag to add to the allow list.

        :return:

        The record modifier filter that the tag plugin was registered
        with.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitRecordModifierFilter.add_remove)
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        return typing.cast("FluentBitRecordModifierFilter", jsii.invoke(self, "addRemove", [tag]))

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: constructs.IConstruct) -> ResolvedFluentBitConfiguration:
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.

        :param _scope: The construct configuring logging using Fluent Bit.

        :return:

        A configuration for the plugin that con be used by the resource
        configuring logging.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitRecordModifierFilter.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(ResolvedFluentBitConfiguration, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="allow")
    def allow(self) -> typing.List[builtins.str]:
        '''Collection of tags that are allowed on a matched input record.

        If a tag is not matched it is removed.
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allow"))

    @builtins.property
    @jsii.member(jsii_name="records")
    def records(self) -> typing.List[AppendedRecord]:
        '''Collection of the records to be appending to matched input.'''
        return typing.cast(typing.List[AppendedRecord], jsii.get(self, "records"))

    @builtins.property
    @jsii.member(jsii_name="remove")
    def remove(self) -> typing.List[builtins.str]:
        '''Collection of tags to exclude from a matched input record.

        If a tag is matched it is removed.
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "remove"))


class FluentBitRegexParser(
    FluentBitParserPluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitRegexParser",
):
    '''A Fluent Bit filter that parsed inbound messages using regular expressions.'''

    def __init__(
        self,
        name: builtins.str,
        *,
        regex: builtins.str,
        skip_empty_values: typing.Optional[builtins.bool] = None,
        time_format: typing.Optional[builtins.str] = None,
        time_key: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Mapping[builtins.str, ParserPluginDataType]] = None,
    ) -> None:
        '''Creates a new instance of the FluentBitLtsvParser class.

        :param name: -
        :param regex: The regular expression to use to parse the incoming records. Use regex group names to define the name of fields being captured.
        :param skip_empty_values: If enabled, the parser ignores empty value of the record.
        :param time_format: Defines the format of the timestamp on the inbound record.
        :param time_key: The key under which timestamp information for the inbound record is given.
        :param types: Maps group names matched by the regex to the data types they should be interpreted as.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitRegexParser.__init__)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        options = FluentBitRegexParserOptions(
            regex=regex,
            skip_empty_values=skip_empty_values,
            time_format=time_format,
            time_key=time_key,
            types=types,
        )

        jsii.create(self.__class__, self, [name, options])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: constructs.IConstruct) -> ResolvedFluentBitConfiguration:
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.

        :param _scope: The construct configuring logging using Fluent Bit.

        :return:

        A configuration for the plugin that con be used by the resource
        configuring logging.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitRegexParser.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(ResolvedFluentBitConfiguration, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> builtins.str:
        '''The regular expression to use to parse the incoming records.

        Use regex group names to define the name of fields being captured.

        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "regex"))

    @builtins.property
    @jsii.member(jsii_name="skipEmptyValues")
    def skip_empty_values(self) -> typing.Optional[builtins.bool]:
        '''If enabled, the parser ignores empty value of the record.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "skipEmptyValues"))

    @builtins.property
    @jsii.member(jsii_name="timeFormat")
    def time_format(self) -> typing.Optional[builtins.str]:
        '''Defines the format of the timestamp on the inbound record.

        :see: `strftime <http://man7.org/linux/man-pages/man3/strftime.3.html>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeFormat"))

    @builtins.property
    @jsii.member(jsii_name="timeKey")
    def time_key(self) -> typing.Optional[builtins.str]:
        '''The key under which timestamp information for the inbound record is given.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeKey"))

    @builtins.property
    @jsii.member(jsii_name="types")
    def types(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, ParserPluginDataType]]:
        '''Maps group names matched by the regex to the data types they should be interpreted as.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, ParserPluginDataType]], jsii.get(self, "types"))


class FluentBitRewriteTagFilter(
    FluentBitFilterPluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitRewriteTagFilter",
):
    '''A Fluent Bit filter that allows parsing of fields in event records.'''

    def __init__(
        self,
        *,
        emitter_mem_buf_limit: typing.Optional[_DataSize_d20aaece] = None,
        emitter_name: typing.Optional[builtins.str] = None,
        emitter_storage_type: typing.Optional[EmitterStorageType] = None,
        rules: typing.Optional[typing.Sequence[typing.Union[RewriteTagRule, typing.Dict[str, typing.Any]]]] = None,
        match: typing.Optional[FluentBitMatch] = None,
    ) -> None:
        '''Creates a new instance of the FluentBitRewriteTagFilter class.

        :param emitter_mem_buf_limit: Set a limit on the amount of memory the tag rewrite emitter can consume if the outputs provide backpressure. Default: 10M
        :param emitter_name: When the filter emits a record under the new Tag, there is an internal emitter plugin that takes care of the job. Since this emitter expose metrics as any other component of the pipeline, you can use this property to configure an optional name for it.
        :param emitter_storage_type: Define a buffering mechanism for the new records created. Note these records are part of the emitter plugin.
        :param rules: Defines the matching criteria and the format of the Tag for the matching record.
        :param match: The pattern to match for records that this output should apply to.
        '''
        options = FluentBitRewriteTagFilterOptions(
            emitter_mem_buf_limit=emitter_mem_buf_limit,
            emitter_name=emitter_name,
            emitter_storage_type=emitter_storage_type,
            rules=rules,
            match=match,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="addRule")
    def add_rule(
        self,
        *,
        keep: builtins.bool,
        key: builtins.str,
        new_tag: builtins.str,
        regex: builtins.str,
    ) -> "FluentBitRewriteTagFilter":
        '''Adds a new rule to apply to matched log entries.

        :param keep: If a rule matches a rule the filter will emit a copy of the record with the new defined Tag. The property keep takes a boolean value to define if the original record with the old Tag must be preserved and continue in the pipeline or just be discarded.
        :param key: The key represents the name of the record key that holds the value that we want to use to match our regular expression. A key name is specified and prefixed with a ``$``.
        :param new_tag: If a regular expression has matched the value of the defined key in the rule, we are ready to compose a new Tag for that specific record. The tag is a concatenated string that can contain any of the following characters: ``a-z,A-Z,0-9`` and ``.-,``.
        :param regex: Using a simple regular expression we can specify a matching pattern to use against the value of the key specified, also we can take advantage of group capturing to create custom placeholder values.

        :return: The parser filter that the parser plugin was registered with.
        '''
        rule = RewriteTagRule(keep=keep, key=key, new_tag=new_tag, regex=regex)

        return typing.cast("FluentBitRewriteTagFilter", jsii.invoke(self, "addRule", [rule]))

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: constructs.IConstruct) -> ResolvedFluentBitConfiguration:
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.

        :param _scope: The construct configuring logging using Fluent Bit.

        :return:

        A configuration for the plugin that con be used by the resource
        configuring logging.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitRewriteTagFilter.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(ResolvedFluentBitConfiguration, jsii.invoke(self, "bind", [_scope]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PLUGIN_NAME")
    def PLUGIN_NAME(cls) -> builtins.str:
        '''The name of the plugin as it will appear in the fluent bit configuration.'''
        return typing.cast(builtins.str, jsii.sget(cls, "PLUGIN_NAME"))

    @builtins.property
    @jsii.member(jsii_name="emitterName")
    def emitter_name(self) -> builtins.str:
        '''When the filter emits a record under the new Tag, there is an internal emitter plugin that takes care of the job.

        Since this emitter expose
        metrics as any other component of the pipeline, you can use this
        property to configure an optional name for it.

        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "emitterName"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> typing.List[RewriteTagRule]:
        '''Collection of rules defining matching criteria and the format of the tag for the matching record.

        :group: Inputs
        '''
        return typing.cast(typing.List[RewriteTagRule], jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="emitterMemBufLimit")
    def emitter_mem_buf_limit(self) -> typing.Optional[_DataSize_d20aaece]:
        '''Set a limit on the amount of memory the tag rewrite emitter can consume if the outputs provide backpressure.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[_DataSize_d20aaece], jsii.get(self, "emitterMemBufLimit"))

    @builtins.property
    @jsii.member(jsii_name="emitterStorageType")
    def emitter_storage_type(self) -> typing.Optional[EmitterStorageType]:
        '''Define a buffering mechanism for the new records created.

        Note these records are part of the emitter plugin.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[EmitterStorageType], jsii.get(self, "emitterStorageType"))


class FluentBitThrottleFilter(
    FluentBitFilterPluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitThrottleFilter",
):
    '''A Fluent Bit filter that sets the average *Rate* of messages per *Interval*, based on leaky bucket and sliding window algorithm.

    In case of overflood,
    it will leak within certain rate.
    '''

    def __init__(
        self,
        *,
        interval: typing.Optional[aws_cdk.Duration] = None,
        print_status: typing.Optional[builtins.bool] = None,
        rate: typing.Optional[jsii.Number] = None,
        window: typing.Optional[jsii.Number] = None,
        match: typing.Optional[FluentBitMatch] = None,
    ) -> None:
        '''Creates a new instance of the FluentBitThrottleFilter class.

        :param interval: Time interval.
        :param print_status: Whether to print status messages with current rate and the limits to information logs.
        :param rate: Amount of messages for the time.
        :param window: Amount of intervals to calculate average over. Default: 5
        :param match: The pattern to match for records that this output should apply to.
        '''
        options = FluentBitThrottleFilterOptions(
            interval=interval,
            print_status=print_status,
            rate=rate,
            window=window,
            match=match,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: constructs.IConstruct) -> ResolvedFluentBitConfiguration:
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.

        :param _scope: The construct configuring logging using Fluent Bit.

        :return:

        A configuration for the plugin that con be used by the resource
        configuring logging.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitThrottleFilter.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(ResolvedFluentBitConfiguration, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> aws_cdk.Duration:
        '''Time interval.

        :group: Inputs
        '''
        return typing.cast(aws_cdk.Duration, jsii.get(self, "interval"))

    @builtins.property
    @jsii.member(jsii_name="rate")
    def rate(self) -> jsii.Number:
        '''Amount of messages for the time.

        :group: Inputs
        '''
        return typing.cast(jsii.Number, jsii.get(self, "rate"))

    @builtins.property
    @jsii.member(jsii_name="window")
    def window(self) -> jsii.Number:
        '''Amount of intervals to calculate average over.

        :group: Inputs
        '''
        return typing.cast(jsii.Number, jsii.get(self, "window"))

    @builtins.property
    @jsii.member(jsii_name="printStatus")
    def print_status(self) -> typing.Optional[builtins.bool]:
        '''Whether to print status messages with current rate and the limits to information logs.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "printStatus"))


class FluentBitCloudWatchLogsOutput(
    FluentBitOutputPluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitCloudWatchLogsOutput",
):
    '''Represents configuration for outputing logs from Fluent Bit to CloudWatch Logs.'''

    def __init__(
        self,
        *,
        auto_create_group: typing.Optional[builtins.bool] = None,
        auto_retry_requests: typing.Optional[builtins.bool] = None,
        endpoint: typing.Optional[builtins.str] = None,
        log_format: typing.Optional[builtins.str] = None,
        log_group: typing.Optional[FluentBitLogGroupOutput] = None,
        log_group_template: typing.Optional[builtins.str] = None,
        log_key: typing.Optional[builtins.str] = None,
        log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
        log_stream: typing.Optional[FluentBitLogStreamOutput] = None,
        log_stream_template: typing.Optional[builtins.str] = None,
        metric_dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metric_namespace: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        sts_endpoint: typing.Optional[builtins.str] = None,
        match: typing.Optional[FluentBitMatch] = None,
    ) -> None:
        '''Creates a new instance of the FluentBitCloudWatchLogsOutput class.

        :param auto_create_group: Automatically create the log group. Default: false
        :param auto_retry_requests: Immediately retry failed requests to AWS services once. This option does not affect the normal Fluent Bit retry mechanism with backoff. Instead, it enables an immediate retry with no delay for networking errors, which may help improve throughput when there are transient/random networking issues. Default: true
        :param endpoint: Specify a custom endpoint for the CloudWatch Logs API.
        :param log_format: An optional parameter that can be used to tell CloudWatch the format of the data. A value of json/emf enables CloudWatch to extract custom metrics embedded in a JSON payload.
        :param log_group: The CloudWatch Log Group configuration for output records.
        :param log_group_template: Template for Log Group name using Fluent Bit record_accessor syntax. This field is optional and if configured it overrides the configured Log Group. If the template translation fails, an error is logged and the provided Log Group (which is still required) is used instead.
        :param log_key: By default, the whole log record will be sent to CloudWatch. If you specify a key name with this option, then only the value of that key will be sent to CloudWatch.
        :param log_retention: If set to a number greater than zero, and newly create log group's retention policy is set to this many days.
        :param log_stream: The CloudWatch LogStream configuration for outbound records.
        :param log_stream_template: Template for Log Stream name using Fluent Bit record accessor syntax. This field is optional and if configured it overrides the other log stream options. If the template translation fails, an error is logged and the logStream or logStreamPrefix are used instead (and thus one of those fields is still required to be configured).
        :param metric_dimensions: A list of lists containing the dimension keys that will be applied to all metrics. The values within a dimension set MUST also be members on the root-node.
        :param metric_namespace: An optional string representing the CloudWatch namespace for the metrics.
        :param region: The AWS region.
        :param role: ARN of an IAM role to assume (for cross account access).
        :param sts_endpoint: Specify a custom STS endpoint for the AWS STS API.
        :param match: The pattern to match for records that this output should apply to.
        '''
        options = FluentBitCloudWatchLogsOutputOptions(
            auto_create_group=auto_create_group,
            auto_retry_requests=auto_retry_requests,
            endpoint=endpoint,
            log_format=log_format,
            log_group=log_group,
            log_group_template=log_group_template,
            log_key=log_key,
            log_retention=log_retention,
            log_stream=log_stream,
            log_stream_template=log_stream_template,
            metric_dimensions=metric_dimensions,
            metric_namespace=metric_namespace,
            region=region,
            role=role,
            sts_endpoint=sts_endpoint,
            match=match,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> ResolvedFluentBitConfiguration:
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.

        :param scope: The construct configuring logging using Fluent Bit.

        :return:

        A configuration for the plugin that con be used by the resource
        configuring logging.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitCloudWatchLogsOutput.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(ResolvedFluentBitConfiguration, jsii.invoke(self, "bind", [scope]))

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> FluentBitLogGroupOutput:
        '''The CloudWatch Log Group configuration for output records.'''
        return typing.cast(FluentBitLogGroupOutput, jsii.get(self, "logGroup"))

    @builtins.property
    @jsii.member(jsii_name="logStream")
    def log_stream(self) -> FluentBitLogStreamOutput:
        '''The CloudWatch LogStream configuration for outbound records.'''
        return typing.cast(FluentBitLogStreamOutput, jsii.get(self, "logStream"))

    @builtins.property
    @jsii.member(jsii_name="autoCreateGroup")
    def auto_create_group(self) -> typing.Optional[builtins.bool]:
        '''Automatically create the log group.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "autoCreateGroup"))

    @builtins.property
    @jsii.member(jsii_name="autoRetryRequests")
    def auto_retry_requests(self) -> typing.Optional[builtins.bool]:
        '''Immediately retry failed requests to AWS services once.

        This option does
        not affect the normal Fluent Bit retry mechanism with backoff. Instead,
        it enables an immediate retry with no delay for networking errors, which
        may help improve throughput when there are transient/random networking
        issues.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "autoRetryRequests"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''Specify a custom endpoint for the CloudWatch Logs API.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="logFormat")
    def log_format(self) -> typing.Optional[builtins.str]:
        '''An optional parameter that can be used to tell CloudWatch the format of the data.

        A value of json/emf enables CloudWatch to extract custom
        metrics embedded in a JSON payload.

        :see: `Embedded Metric Format <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format_Specification.html>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logFormat"))

    @builtins.property
    @jsii.member(jsii_name="logGroupTemplate")
    def log_group_template(self) -> typing.Optional[builtins.str]:
        '''Template for Log Group name using Fluent Bit record_accessor syntax.

        This field is optional and if configured it overrides the configured Log
        Group.

        If the template translation fails, an error is logged and the provided
        Log Group (which is still required) is used instead.

        :see: `Fluent Bit record accessor snytax <https://docs.fluentbit.io/manual/administration/configuring-fluent-bit/classic-mode/record-accessor>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupTemplate"))

    @builtins.property
    @jsii.member(jsii_name="logKey")
    def log_key(self) -> typing.Optional[builtins.str]:
        '''By default, the whole log record will be sent to CloudWatch.

        If you
        specify a key name with this option, then only the value of that key
        will be sent to CloudWatch.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logKey"))

    @builtins.property
    @jsii.member(jsii_name="logRetention")
    def log_retention(self) -> typing.Optional[aws_cdk.aws_logs.RetentionDays]:
        '''If set to a number greater than zero, and newly create log group's retention policy is set to this many days.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_logs.RetentionDays], jsii.get(self, "logRetention"))

    @builtins.property
    @jsii.member(jsii_name="logStreamTemplate")
    def log_stream_template(self) -> typing.Optional[builtins.str]:
        '''Template for Log Stream name using Fluent Bit record accessor syntax.

        This field is optional and if configured it overrides the other log
        stream options. If the template translation fails, an error is logged
        and the logStream or logStreamPrefix are used instead (and thus one of
        those fields is still required to be configured).

        :see: `Fluent Bit record accessor snytax <https://docs.fluentbit.io/manual/administration/configuring-fluent-bit/classic-mode/record-accessor>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamTemplate"))

    @builtins.property
    @jsii.member(jsii_name="metricDimensions")
    def metric_dimensions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of lists containing the dimension keys that will be applied to all metrics.

        The values within a dimension set MUST also be members on
        the root-node.

        :see: `Dimensions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Dimension>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "metricDimensions"))

    @builtins.property
    @jsii.member(jsii_name="metricNamespace")
    def metric_namespace(self) -> typing.Optional[builtins.str]:
        '''An optional string representing the CloudWatch namespace for the metrics.

        :see: `Metric Tutorial <https://docs.fluentbit.io/manual/pipeline/outputs/cloudwatch#metrics-tutorial>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricNamespace"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''ARN of an IAM role to assume (for cross account access).

        :group: Inputs
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="stsEndpoint")
    def sts_endpoint(self) -> typing.Optional[builtins.str]:
        '''Specify a custom STS endpoint for the AWS STS API.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stsEndpoint"))


class FluentBitElasticsearchOutput(
    FluentBitOutputPluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitElasticsearchOutput",
):
    def __init__(
        self,
        *,
        host: builtins.str,
        aws_auth: typing.Optional[builtins.bool] = None,
        aws_external_id: typing.Optional[builtins.str] = None,
        aws_region: typing.Optional[builtins.str] = None,
        aws_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        aws_sts_endpoint: typing.Optional[builtins.str] = None,
        buffer_size: typing.Optional[ElasticsearchOutputBufferSize] = None,
        cloud_auth: typing.Optional[builtins.str] = None,
        cloud_id: typing.Optional[builtins.str] = None,
        compress: typing.Optional[ElasticsearchCompressionFormat] = None,
        current_time_index: typing.Optional[builtins.bool] = None,
        generate_id: typing.Optional[builtins.bool] = None,
        http_passwd: typing.Optional[builtins.str] = None,
        http_user: typing.Optional[builtins.str] = None,
        id_key: typing.Optional[builtins.str] = None,
        include_tag_key: typing.Optional[builtins.bool] = None,
        index: typing.Optional[builtins.str] = None,
        logstash_date_format: typing.Optional[builtins.str] = None,
        logstash_format: typing.Optional[builtins.bool] = None,
        logstash_prefix: typing.Optional[builtins.str] = None,
        logstash_prefix_key: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        pipeline: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        replace_dots: typing.Optional[builtins.bool] = None,
        suppress_type_name: typing.Optional[builtins.bool] = None,
        tag_key: typing.Optional[builtins.str] = None,
        time_key: typing.Optional[builtins.str] = None,
        time_key_format: typing.Optional[builtins.str] = None,
        time_key_nanos: typing.Optional[builtins.bool] = None,
        trace_error: typing.Optional[builtins.bool] = None,
        trace_output: typing.Optional[builtins.bool] = None,
        type: typing.Optional[builtins.str] = None,
        workers: typing.Optional[jsii.Number] = None,
        write_operation: typing.Optional[builtins.str] = None,
        match: typing.Optional[FluentBitMatch] = None,
    ) -> None:
        '''Creates a new instance of the FluentBitKinesisFirehoseOutput class.

        :param host: IP address or hostname of the target Elasticsearch instance.
        :param aws_auth: Enable AWS Sigv4 Authentication for Amazon Elasticsearch Service. Default: false
        :param aws_external_id: External ID for the AWS IAM Role specified with ``awsRole``.
        :param aws_region: Specify the AWS region for Elasticsearch Service.
        :param aws_role: AWS IAM Role to assume to put records to your Amazon cluster.
        :param aws_sts_endpoint: Specify the custom sts endpoint to be used with STS API for Amazon Elasticsearch Service.
        :param buffer_size: Specify the buffer size used to read the response from the Elasticsearch HTTP service. This option is useful for debugging purposes where is required to read full responses, note that response size grows depending of the number of records inserted.
        :param cloud_auth: Specify the credentials to use to connect to Elastic's Elasticsearch Service running on Elastic Cloud.
        :param cloud_id: If you are using Elastic's Elasticsearch Service you can specify the cloud_id of the cluster running.
        :param compress: Set payload compression mechanism.
        :param current_time_index: Use current time for index generation instead of message record. Default: false
        :param generate_id: When enabled, generate ``_id`` for outgoing records. This prevents duplicate records when retrying.
        :param http_passwd: Password for user defined in ``httpUser``.
        :param http_user: Optional username credential for access.
        :param id_key: If set, ``_id`` will be the value of the key from incoming record and ``generateId`` option is ignored.
        :param include_tag_key: When enabled, it append the Tag name to the record.
        :param index: Index name. Default: 'fluent-bit
        :param logstash_date_format: Time format (based on strftime) to generate the second part of the Index name. Default: '%Y.%m.%d'
        :param logstash_format: Enable Logstash format compatibility. Default: false
        :param logstash_prefix: When ``logstashFormat`` is enabled, the Index name is composed using a prefix and the date, e.g: If ``logstashPrefix`` is equals to 'mydata' your index will become 'mydata-YYYY.MM.DD'. The last string appended belongs to the date when the data is being generated. Default: 'logstash'
        :param logstash_prefix_key: When included: the value in the record that belongs to the key will be looked up and over-write the ``logstashPrefix`` for index generation. If the key/value is not found in the record then the ``logstashPrefix`` option will act as a fallback. Nested keys are not supported (if desired, you can use the nest filter plugin to remove nesting)
        :param path: Elasticsearch accepts new data on HTTP query path "/_bulk". But it is also possible to serve Elasticsearch behind a reverse proxy on a subpath. This option defines such path on the fluent-bit side. It simply adds a path prefix in the indexing HTTP POST URI..
        :param pipeline: Elasticsearch allows to setup filters called pipelines. This option allows to define which pipeline the database should use.
        :param port: TCP port of the target Elasticsearch instance. Default: 9200
        :param replace_dots: When enabled, replace field name dots with underscore. Default: false
        :param suppress_type_name: When enabled, mapping types is removed and ``type`` option is ignored. Default: false
        :param tag_key: When ``includeTagKey`` is enabled, this property defines the key name for the tag. Default: '_flb-key'
        :param time_key: When ``logstashFormat`` is enabled, each record will get a new timestamp field. The``timeKey`` property defines the name of that field. Default: '
        :param time_key_format: When ``logstashFormat`` is enabled, this property defines the format of the timestamp. Default: '%Y-%m-%dT%H:%M:%S'
        :param time_key_nanos: When ``logstashFormat`` is enabled, enabling this property sends nanosecond precision timestamps. Default: false
        :param trace_error: When enabled print the Elasticsearch API calls to stdout when Elasticsearch returns an error (for diag only). Default: false
        :param trace_output: When enabled print the Elasticsearch API calls to stdout (for diag only). Default: false
        :param type: Type name. Default: '_doc'
        :param workers: Enables dedicated thread(s) for this output. Default: 2
        :param write_operation: Operation to use to write in bulk requests. Default: 'create'
        :param match: The pattern to match for records that this output should apply to.
        '''
        options = FluentBitElasticsearchOutputOptions(
            host=host,
            aws_auth=aws_auth,
            aws_external_id=aws_external_id,
            aws_region=aws_region,
            aws_role=aws_role,
            aws_sts_endpoint=aws_sts_endpoint,
            buffer_size=buffer_size,
            cloud_auth=cloud_auth,
            cloud_id=cloud_id,
            compress=compress,
            current_time_index=current_time_index,
            generate_id=generate_id,
            http_passwd=http_passwd,
            http_user=http_user,
            id_key=id_key,
            include_tag_key=include_tag_key,
            index=index,
            logstash_date_format=logstash_date_format,
            logstash_format=logstash_format,
            logstash_prefix=logstash_prefix,
            logstash_prefix_key=logstash_prefix_key,
            path=path,
            pipeline=pipeline,
            port=port,
            replace_dots=replace_dots,
            suppress_type_name=suppress_type_name,
            tag_key=tag_key,
            time_key=time_key,
            time_key_format=time_key_format,
            time_key_nanos=time_key_nanos,
            trace_error=trace_error,
            trace_output=trace_output,
            type=type,
            workers=workers,
            write_operation=write_operation,
            match=match,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: constructs.IConstruct) -> ResolvedFluentBitConfiguration:
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.

        :param _scope: The construct configuring logging using Fluent Bit.

        :return:

        A configuration for the plugin that con be used by the resource
        configuring logging.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitElasticsearchOutput.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(ResolvedFluentBitConfiguration, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        '''IP address or hostname of the target Elasticsearch instance.

        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @builtins.property
    @jsii.member(jsii_name="awsAuth")
    def aws_auth(self) -> typing.Optional[builtins.bool]:
        '''Enable AWS Sigv4 Authentication for Amazon Elasticsearch Service.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "awsAuth"))

    @builtins.property
    @jsii.member(jsii_name="awsExternalId")
    def aws_external_id(self) -> typing.Optional[builtins.str]:
        '''External ID for the AWS IAM Role specified with ``awsRole``.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsExternalId"))

    @builtins.property
    @jsii.member(jsii_name="awsRegion")
    def aws_region(self) -> typing.Optional[builtins.str]:
        '''Specify the AWS region for Elasticsearch Service.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsRegion"))

    @builtins.property
    @jsii.member(jsii_name="awsRole")
    def aws_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''AWS IAM Role to assume to put records to your Amazon cluster.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], jsii.get(self, "awsRole"))

    @builtins.property
    @jsii.member(jsii_name="awsStsEndpoint")
    def aws_sts_endpoint(self) -> typing.Optional[builtins.str]:
        '''Specify the custom sts endpoint to be used with STS API for Amazon Elasticsearch Service.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsStsEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="bufferSize")
    def buffer_size(self) -> typing.Optional[ElasticsearchOutputBufferSize]:
        '''Specify the buffer size used to read the response from the Elasticsearch HTTP service.

        This option is useful for debugging purposes where is
        required to read full responses, note that response size grows depending
        of the number of records inserted.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[ElasticsearchOutputBufferSize], jsii.get(self, "bufferSize"))

    @builtins.property
    @jsii.member(jsii_name="cloudAuth")
    def cloud_auth(self) -> typing.Optional[builtins.str]:
        '''Specify the credentials to use to connect to Elastic's Elasticsearch Service running on Elastic Cloud.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudAuth"))

    @builtins.property
    @jsii.member(jsii_name="cloudId")
    def cloud_id(self) -> typing.Optional[builtins.str]:
        '''If you are using Elastic's Elasticsearch Service you can specify the cloud_id of the cluster running.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudId"))

    @builtins.property
    @jsii.member(jsii_name="compress")
    def compress(self) -> typing.Optional[ElasticsearchCompressionFormat]:
        '''Set payload compression mechanism.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[ElasticsearchCompressionFormat], jsii.get(self, "compress"))

    @builtins.property
    @jsii.member(jsii_name="currentTimeIndex")
    def current_time_index(self) -> typing.Optional[builtins.bool]:
        '''Use current time for index generation instead of message record.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "currentTimeIndex"))

    @builtins.property
    @jsii.member(jsii_name="generateId")
    def generate_id(self) -> typing.Optional[builtins.bool]:
        '''When enabled, generate ``_id`` for outgoing records.

        This prevents duplicate
        records when retrying.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "generateId"))

    @builtins.property
    @jsii.member(jsii_name="httpPasswd")
    def http_passwd(self) -> typing.Optional[builtins.str]:
        '''Password for user defined in ``httpUser``.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpPasswd"))

    @builtins.property
    @jsii.member(jsii_name="httpUser")
    def http_user(self) -> typing.Optional[builtins.str]:
        '''Optional username credential for access.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpUser"))

    @builtins.property
    @jsii.member(jsii_name="idKey")
    def id_key(self) -> typing.Optional[builtins.str]:
        '''If set, ``_id`` will be the value of the key from incoming record and ``generateId`` option is ignored.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idKey"))

    @builtins.property
    @jsii.member(jsii_name="includeTagKey")
    def include_tag_key(self) -> typing.Optional[builtins.bool]:
        '''When enabled, it append the Tag name to the record.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "includeTagKey"))

    @builtins.property
    @jsii.member(jsii_name="index")
    def index(self) -> typing.Optional[builtins.str]:
        '''Index name.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "index"))

    @builtins.property
    @jsii.member(jsii_name="logstashDateFormat")
    def logstash_date_format(self) -> typing.Optional[builtins.str]:
        '''Time format (based on strftime) to generate the second part of the Index name.

        :see: `strftime <http://man7.org/linux/man-pages/man3/strftime.3.html>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logstashDateFormat"))

    @builtins.property
    @jsii.member(jsii_name="logstashFormat")
    def logstash_format(self) -> typing.Optional[builtins.bool]:
        '''Enable Logstash format compatibility.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "logstashFormat"))

    @builtins.property
    @jsii.member(jsii_name="logstashPrefix")
    def logstash_prefix(self) -> typing.Optional[builtins.str]:
        '''When ``logstashFormat`` is enabled, the Index name is composed using a prefix and the date, e.g: If ``logstashPrefix`` is equals to 'mydata' your index will become 'mydata-YYYY.MM.DD'.

        The last string appended belongs to the date when the data is being
        generated.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logstashPrefix"))

    @builtins.property
    @jsii.member(jsii_name="logstashPrefixKey")
    def logstash_prefix_key(self) -> typing.Optional[builtins.str]:
        '''When included: the value in the record that belongs to the key will be looked up and over-write the ``logstashPrefix`` for index generation.

        If
        the key/value is not found in the record then the ``logstashPrefix`` option
        will act as a fallback.

        Nested keys are not supported (if desired, you can use the nest filter
        plugin to remove nesting).

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logstashPrefixKey"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''Elasticsearch accepts new data on HTTP query path "/_bulk".

        But it is
        also possible to serve Elasticsearch behind a reverse proxy on a
        subpath. This option defines such path on the fluent-bit side. It
        simply adds a path prefix in the indexing HTTP POST URI.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="pipeline")
    def pipeline(self) -> typing.Optional[builtins.str]:
        '''Elasticsearch allows to setup filters called pipelines.

        This option
        allows to define which pipeline the database should use.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pipeline"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        '''TCP port of the target Elasticsearch instance.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="replaceDots")
    def replace_dots(self) -> typing.Optional[builtins.bool]:
        '''When enabled, replace field name dots with underscore.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "replaceDots"))

    @builtins.property
    @jsii.member(jsii_name="suppressTypeName")
    def suppress_type_name(self) -> typing.Optional[builtins.bool]:
        '''When enabled, mapping types is removed and ``type`` option is ignored.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "suppressTypeName"))

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''When ``includeTagKey`` is enabled, this property defines the key name for the tag.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKey"))

    @builtins.property
    @jsii.member(jsii_name="timeKey")
    def time_key(self) -> typing.Optional[builtins.str]:
        '''When ``logstashFormat`` is enabled, each record will get a new timestamp field.

        The``timeKey`` property defines the name of that field.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeKey"))

    @builtins.property
    @jsii.member(jsii_name="timeKeyFormat")
    def time_key_format(self) -> typing.Optional[builtins.str]:
        '''When ``logstashFormat`` is enabled, this property defines the format of the timestamp.

        :see: `strftime <http://man7.org/linux/man-pages/man3/strftime.3.html>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeKeyFormat"))

    @builtins.property
    @jsii.member(jsii_name="timeKeyNanos")
    def time_key_nanos(self) -> typing.Optional[builtins.bool]:
        '''When ``logstashFormat`` is enabled, enabling this property sends nanosecond precision timestamps.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "timeKeyNanos"))

    @builtins.property
    @jsii.member(jsii_name="traceError")
    def trace_error(self) -> typing.Optional[builtins.bool]:
        '''When enabled print the Elasticsearch API calls to stdout when Elasticsearch returns an error (for diag only).

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "traceError"))

    @builtins.property
    @jsii.member(jsii_name="traceOutput")
    def trace_output(self) -> typing.Optional[builtins.bool]:
        '''When enabled print the Elasticsearch API calls to stdout (for diag only).

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "traceOutput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        '''Type name.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="workers")
    def workers(self) -> typing.Optional[jsii.Number]:
        '''Enables dedicated thread(s) for this output.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "workers"))

    @builtins.property
    @jsii.member(jsii_name="writeOperation")
    def write_operation(self) -> typing.Optional[builtins.str]:
        '''Operation to use to write in bulk requests.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "writeOperation"))


class FluentBitJsonParser(
    FluentBitParserPluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitJsonParser",
):
    '''A Fluent Bit filter that parsed inbound messages in JSON format.'''

    def __init__(
        self,
        name: builtins.str,
        *,
        time_format: typing.Optional[builtins.str] = None,
        time_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the FluentBitJsonParser class.

        :param name: -
        :param time_format: Defines the format of the timestamp on the inbound record.
        :param time_key: The key under which timestamp information for the inbound record is given.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitJsonParser.__init__)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        options = FluentBitJsonParserOptions(
            time_format=time_format, time_key=time_key
        )

        jsii.create(self.__class__, self, [name, options])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: constructs.IConstruct) -> ResolvedFluentBitConfiguration:
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.

        :param _scope: The construct configuring logging using Fluent Bit.

        :return:

        A configuration for the plugin that con be used by the resource
        configuring logging.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitJsonParser.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(ResolvedFluentBitConfiguration, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="timeFormat")
    def time_format(self) -> typing.Optional[builtins.str]:
        '''Defines the format of the timestamp on the inbound record.

        :see: `strftime <http://man7.org/linux/man-pages/man3/strftime.3.html>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeFormat"))

    @builtins.property
    @jsii.member(jsii_name="timeKey")
    def time_key(self) -> typing.Optional[builtins.str]:
        '''The key under which timestamp information for the inbound record is given.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeKey"))


class FluentBitKinesisFirehoseOutput(
    FluentBitOutputPluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitKinesisFirehoseOutput",
):
    '''Represents configuration for outputing logs from Fluent Bit to Kinesis Firehose.'''

    def __init__(
        self,
        *,
        auto_retry_requests: typing.Optional[builtins.bool] = None,
        compression: typing.Optional[KinesisFirehoseCompressionFormat] = None,
        delivery_stream: typing.Optional[_IDeliveryStream_cf5feed7] = None,
        endpoint: typing.Optional[builtins.str] = None,
        log_key: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        sts_endpoint: typing.Optional[builtins.str] = None,
        time_key: typing.Optional[builtins.str] = None,
        time_key_format: typing.Optional[builtins.str] = None,
        match: typing.Optional[FluentBitMatch] = None,
    ) -> None:
        '''Creates a new instance of the FluentBitKinesisFirehoseOutput class.

        :param auto_retry_requests: Immediately retry failed requests to AWS services once. This option does not affect the normal Fluent Bit retry mechanism with backoff. Instead, it enables an immediate retry with no delay for networking errors, which may help improve throughput when there are transient/random networking issues. Default: true
        :param compression: Compression type for Firehose records. Each log record is individually compressed and sent to Firehose.
        :param delivery_stream: The Kinesis Firehose Delivery stream that you want log records sent to.
        :param endpoint: Specify a custom endpoint for the Firehose API.
        :param log_key: By default, the whole log record will be sent to Firehose. If you specify a key name with this option, then only the value of that key will be sent to Firehose.
        :param region: The AWS region.
        :param role: ARN of an IAM role to assume (for cross account access).
        :param sts_endpoint: Specify a custom STS endpoint for the AWS STS API.
        :param time_key: Add the timestamp to the record under this key.
        :param time_key_format: A strftime compliant format string for the timestamp. Default: '%Y-%m-%dT%H:%M:%S'
        :param match: The pattern to match for records that this output should apply to.
        '''
        options = FluentBitKinesisFirehoseOutputOptions(
            auto_retry_requests=auto_retry_requests,
            compression=compression,
            delivery_stream=delivery_stream,
            endpoint=endpoint,
            log_key=log_key,
            region=region,
            role=role,
            sts_endpoint=sts_endpoint,
            time_key=time_key,
            time_key_format=time_key_format,
            match=match,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> ResolvedFluentBitConfiguration:
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.

        :param scope: The construct configuring logging using Fluent Bit.

        :return:

        A configuration for the plugin that con be used by the resource
        configuring logging.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitKinesisFirehoseOutput.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(ResolvedFluentBitConfiguration, jsii.invoke(self, "bind", [scope]))

    @builtins.property
    @jsii.member(jsii_name="autoRetryRequests")
    def auto_retry_requests(self) -> typing.Optional[builtins.bool]:
        '''Immediately retry failed requests to AWS services once.

        This option does
        not affect the normal Fluent Bit retry mechanism with backoff. Instead,
        it enables an immediate retry with no delay for networking errors, which
        may help improve throughput when there are transient/random networking
        issues.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "autoRetryRequests"))

    @builtins.property
    @jsii.member(jsii_name="compression")
    def compression(self) -> typing.Optional[KinesisFirehoseCompressionFormat]:
        '''Compression type for Firehose records.

        Each log record is individually
        compressed and sent to Firehose.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[KinesisFirehoseCompressionFormat], jsii.get(self, "compression"))

    @builtins.property
    @jsii.member(jsii_name="deliveryStream")
    def delivery_stream(self) -> typing.Optional[_IDeliveryStream_cf5feed7]:
        '''The Kinesis Firehose Delivery stream that you want log records sent to.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[_IDeliveryStream_cf5feed7], jsii.get(self, "deliveryStream"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''Specify a custom endpoint for the Firehose API.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="logKey")
    def log_key(self) -> typing.Optional[builtins.str]:
        '''By default, the whole log record will be sent to Firehose.

        If you
        specify a key name with this option, then only the value of that key
        will be sent to Firehose.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logKey"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''ARN of an IAM role to assume (for cross account access).

        :group: Inputs
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="stsEndpoint")
    def sts_endpoint(self) -> typing.Optional[builtins.str]:
        '''Specify a custom STS endpoint for the AWS STS API.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stsEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="timeKey")
    def time_key(self) -> typing.Optional[builtins.str]:
        '''Add the timestamp to the record under this key.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeKey"))

    @builtins.property
    @jsii.member(jsii_name="timeKeyFormat")
    def time_key_format(self) -> typing.Optional[builtins.str]:
        '''A strftime compliant format string for the timestamp.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeKeyFormat"))


class FluentBitKinesisOutput(
    FluentBitOutputPluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitKinesisOutput",
):
    '''Represents configuration for outputing logs from Fluent Bit to Kinesis Data Streams.'''

    def __init__(
        self,
        *,
        auto_retry_requests: typing.Optional[builtins.bool] = None,
        endpoint: typing.Optional[builtins.str] = None,
        log_key: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        stream: typing.Optional[aws_cdk.aws_kinesis.IStream] = None,
        sts_endpoint: typing.Optional[builtins.str] = None,
        time_key: typing.Optional[builtins.str] = None,
        time_key_format: typing.Optional[builtins.str] = None,
        match: typing.Optional[FluentBitMatch] = None,
    ) -> None:
        '''Creates a new instance of the FluentBitKinesisOutput class.

        :param auto_retry_requests: Immediately retry failed requests to AWS services once. This option does not affect the normal Fluent Bit retry mechanism with backoff. Instead, it enables an immediate retry with no delay for networking errors, which may help improve throughput when there are transient/random networking issues. Default: true
        :param endpoint: Specify a custom endpoint for the Firehose API.
        :param log_key: By default, the whole log record will be sent to Firehose. If you specify a key name with this option, then only the value of that key will be sent to Firehose.
        :param region: The AWS region.
        :param role: ARN of an IAM role to assume (for cross account access).
        :param stream: The name of the Kinesis Streams Delivery stream that you want log records sent to.
        :param sts_endpoint: Specify a custom STS endpoint for the AWS STS API.
        :param time_key: Add the timestamp to the record under this key.
        :param time_key_format: A strftime compliant format string for the timestamp. Default: '%Y-%m-%dT%H:%M:%S'
        :param match: The pattern to match for records that this output should apply to.
        '''
        options = FluentBitKinesisOutputOptions(
            auto_retry_requests=auto_retry_requests,
            endpoint=endpoint,
            log_key=log_key,
            region=region,
            role=role,
            stream=stream,
            sts_endpoint=sts_endpoint,
            time_key=time_key,
            time_key_format=time_key_format,
            match=match,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> ResolvedFluentBitConfiguration:
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.

        :param scope: The construct configuring logging using Fluent Bit.

        :return:

        A configuration for the plugin that con be used by the resource
        configuring logging.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitKinesisOutput.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(ResolvedFluentBitConfiguration, jsii.invoke(self, "bind", [scope]))

    @builtins.property
    @jsii.member(jsii_name="autoRetryRequests")
    def auto_retry_requests(self) -> typing.Optional[builtins.bool]:
        '''Immediately retry failed requests to AWS services once.

        This option does
        not affect the normal Fluent Bit retry mechanism with backoff. Instead,
        it enables an immediate retry with no delay for networking errors, which
        may help improve throughput when there are transient/random networking
        issues.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "autoRetryRequests"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''Specify a custom endpoint for the Firehose API.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="logKey")
    def log_key(self) -> typing.Optional[builtins.str]:
        '''By default, the whole log record will be sent to Firehose.

        If you
        specify a key name with this option, then only the value of that key
        will be sent to Firehose.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logKey"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''ARN of an IAM role to assume (for cross account access).

        :group: Inputs
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="stream")
    def stream(self) -> typing.Optional[aws_cdk.aws_kinesis.IStream]:
        '''The name of the Kinesis Streams Delivery stream that you want log records sent to.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_kinesis.IStream], jsii.get(self, "stream"))

    @builtins.property
    @jsii.member(jsii_name="stsEndpoint")
    def sts_endpoint(self) -> typing.Optional[builtins.str]:
        '''Specify a custom STS endpoint for the AWS STS API.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stsEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="timeKey")
    def time_key(self) -> typing.Optional[builtins.str]:
        '''Add the timestamp to the record under this key.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeKey"))

    @builtins.property
    @jsii.member(jsii_name="timeKeyFormat")
    def time_key_format(self) -> typing.Optional[builtins.str]:
        '''A strftime compliant format string for the timestamp.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeKeyFormat"))


class FluentBitLogfmtParser(
    FluentBitParserPluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitLogfmtParser",
):
    '''A Fluent Bit filter that parsed inbound messages in LTSV format.'''

    def __init__(
        self,
        name: builtins.str,
        *,
        time_format: typing.Optional[builtins.str] = None,
        time_key: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Mapping[builtins.str, ParserPluginDataType]] = None,
    ) -> None:
        '''Creates a new instance of the FluentBitLogfmtParser class.

        :param name: -
        :param time_format: Defines the format of the timestamp on the inbound record.
        :param time_key: The key under which timestamp information for the inbound record is given.
        :param types: Maps group names matched by the regex to the data types they should be interpreted as.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitLogfmtParser.__init__)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        options = FluentBitLogfmtParserOptions(
            time_format=time_format, time_key=time_key, types=types
        )

        jsii.create(self.__class__, self, [name, options])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: constructs.IConstruct) -> ResolvedFluentBitConfiguration:
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.

        :param _scope: The construct configuring logging using Fluent Bit.

        :return:

        A configuration for the plugin that con be used by the resource
        configuring logging.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitLogfmtParser.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(ResolvedFluentBitConfiguration, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="timeFormat")
    def time_format(self) -> typing.Optional[builtins.str]:
        '''Defines the format of the timestamp on the inbound record.

        :see: `strftime <http://man7.org/linux/man-pages/man3/strftime.3.html>`_
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeFormat"))

    @builtins.property
    @jsii.member(jsii_name="timeKey")
    def time_key(self) -> typing.Optional[builtins.str]:
        '''The key under which timestamp information for the inbound record is given.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeKey"))

    @builtins.property
    @jsii.member(jsii_name="types")
    def types(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, ParserPluginDataType]]:
        '''Maps group names matched by the regex to the data types they should be interpreted as.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, ParserPluginDataType]], jsii.get(self, "types"))


class FluentBitLtsvParser(
    FluentBitParserPluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitLtsvParser",
):
    '''A Fluent Bit filter that parsed inbound messages in LTSV format.'''

    def __init__(
        self,
        name: builtins.str,
        *,
        time_format: typing.Optional[builtins.str] = None,
        time_key: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Mapping[builtins.str, ParserPluginDataType]] = None,
    ) -> None:
        '''Creates a new instance of the FluentBitLtsvParser class.

        :param name: -
        :param time_format: Defines the format of the timestamp on the inbound record.
        :param time_key: The key under which timestamp information for the inbound record is given.
        :param types: Maps group names matched by the regex to the data types they should be interpreted as.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitLtsvParser.__init__)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        options = FluentBitLtsvParserOptions(
            time_format=time_format, time_key=time_key, types=types
        )

        jsii.create(self.__class__, self, [name, options])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: constructs.IConstruct) -> ResolvedFluentBitConfiguration:
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.

        :param _scope: The construct configuring logging using Fluent Bit.

        :return:

        A configuration for the plugin that con be used by the resource
        configuring logging.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitLtsvParser.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(ResolvedFluentBitConfiguration, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="timeFormat")
    def time_format(self) -> typing.Optional[builtins.str]:
        '''Defines the format of the timestamp on the inbound record.

        :default: Inputs

        :see: `strftime <http://man7.org/linux/man-pages/man3/strftime.3.html>`_
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeFormat"))

    @builtins.property
    @jsii.member(jsii_name="timeKey")
    def time_key(self) -> typing.Optional[builtins.str]:
        '''The key under which timestamp information for the inbound record is given.

        :default: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeKey"))

    @builtins.property
    @jsii.member(jsii_name="types")
    def types(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, ParserPluginDataType]]:
        '''Maps group names matched by the regex to the data types they should be interpreted as.

        :default: Inputs
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, ParserPluginDataType]], jsii.get(self, "types"))


class FluentBitOpenSearchOutput(
    FluentBitOutputPluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.k8s_aws.FluentBitOpenSearchOutput",
):
    def __init__(
        self,
        *,
        domain: aws_cdk.aws_opensearchservice.IDomain,
        aws_auth: typing.Optional[builtins.bool] = None,
        aws_external_id: typing.Optional[builtins.str] = None,
        aws_region: typing.Optional[builtins.str] = None,
        aws_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        aws_sts_endpoint: typing.Optional[builtins.str] = None,
        buffer_size: typing.Optional[OpenSearchOutputBufferSize] = None,
        current_time_index: typing.Optional[builtins.bool] = None,
        generate_id: typing.Optional[builtins.bool] = None,
        host: typing.Optional[builtins.str] = None,
        http_passwd: typing.Optional[builtins.str] = None,
        http_user: typing.Optional[builtins.str] = None,
        id_key: typing.Optional[builtins.str] = None,
        include_tag_key: typing.Optional[builtins.bool] = None,
        index: typing.Optional[builtins.str] = None,
        logstash_date_format: typing.Optional[builtins.str] = None,
        logstash_format: typing.Optional[builtins.bool] = None,
        logstash_prefix: typing.Optional[builtins.str] = None,
        logstash_prefix_key: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        pipeline: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        replace_dots: typing.Optional[builtins.bool] = None,
        suppress_type_name: typing.Optional[builtins.bool] = None,
        tag_key: typing.Optional[builtins.str] = None,
        time_key: typing.Optional[builtins.str] = None,
        time_key_format: typing.Optional[builtins.str] = None,
        time_key_nanos: typing.Optional[builtins.bool] = None,
        trace_error: typing.Optional[builtins.bool] = None,
        trace_output: typing.Optional[builtins.bool] = None,
        type: typing.Optional[builtins.str] = None,
        workers: typing.Optional[jsii.Number] = None,
        write_operation: typing.Optional[builtins.str] = None,
        match: typing.Optional[FluentBitMatch] = None,
    ) -> None:
        '''Creates a new instance of the FluentBitOpenSearchOutput class.

        :param domain: The Opensearch domain to which logs should be shipped.
        :param aws_auth: Enable AWS Sigv4 Authentication for Amazon OpenSearch Service. Default: false
        :param aws_external_id: External ID for the AWS IAM Role specified with ``awsRole``.
        :param aws_region: Specify the AWS region for Amazon OpenSearch Service.
        :param aws_role: AWS IAM Role to assume to put records to your Amazon cluster.
        :param aws_sts_endpoint: Specify the custom sts endpoint to be used with STS API for Amazon OpenSearch Service.
        :param buffer_size: Specify the buffer size used to read the response from the OpenSearch HTTP service. This option is useful for debugging purposes where is required to read full responses, note that response size grows depending of the number of records inserted.
        :param current_time_index: Use current time for index generation instead of message record. Default: false
        :param generate_id: When enabled, generate ``_id`` for outgoing records. This prevents duplicate records when retrying.
        :param host: IP address or hostname of the target OpenSearch instance.
        :param http_passwd: Password for user defined in ``httpUser``.
        :param http_user: Optional username credential for access.
        :param id_key: If set, ``_id`` will be the value of the key from incoming record and ``generateId`` option is ignored.
        :param include_tag_key: When enabled, it append the Tag name to the record.
        :param index: Index name. Default: 'fluent-bit
        :param logstash_date_format: Time format (based on strftime) to generate the second part of the Index name. Default: '%Y.%m.%d'
        :param logstash_format: Enable Logstash format compatibility. Default: false
        :param logstash_prefix: When ``logstashFormat`` is enabled, the Index name is composed using a prefix and the date, e.g: If ``logstashPrefix`` is equals to 'mydata' your index will become 'mydata-YYYY.MM.DD'. The last string appended belongs to the date when the data is being generated. Default: 'logstash'
        :param logstash_prefix_key: When included: the value in the record that belongs to the key will be looked up and over-write the ``logstashPrefix`` for index generation. If the key/value is not found in the record then the ``logstashPrefix`` option will act as a fallback. Nested keys are not supported (if desired, you can use the nest filter plugin to remove nesting)
        :param path: OpenSearch accepts new data on HTTP query path "/_bulk". But it is also possible to serve OpenSearch behind a reverse proxy on a subpath. This option defines such path on the fluent-bit side. It simply adds a path prefix in the indexing HTTP POST URI..
        :param pipeline: OpenSearch allows to setup filters called pipelines. This option allows to define which pipeline the database should use.
        :param port: TCP port of the target OpenSearch instance. Default: 9200
        :param replace_dots: When enabled, replace field name dots with underscore. Default: false
        :param suppress_type_name: When enabled, mapping types is removed and ``type`` option is ignored. Default: false
        :param tag_key: When ``includeTagKey`` is enabled, this property defines the key name for the tag. Default: '_flb-key'
        :param time_key: When ``logstashFormat`` is enabled, each record will get a new timestamp field. The``timeKey`` property defines the name of that field. Default: '
        :param time_key_format: When ``logstashFormat`` is enabled, this property defines the format of the timestamp. Default: '%Y-%m-%dT%H:%M:%S'
        :param time_key_nanos: When ``logstashFormat`` is enabled, enabling this property sends nanosecond precision timestamps. Default: false
        :param trace_error: When enabled print the OpenSearch API calls to stdout when OpenSearch returns an error (for diag only). Default: false
        :param trace_output: When enabled print the OpenSearch API calls to stdout (for diag only). Default: false
        :param type: Type name. Default: '_doc'
        :param workers: Enables dedicated thread(s) for this output. Default: 2
        :param write_operation: Operation to use to write in bulk requests. Default: 'create'
        :param match: The pattern to match for records that this output should apply to.
        '''
        options = FluentBitOpenSearchOutputOptions(
            domain=domain,
            aws_auth=aws_auth,
            aws_external_id=aws_external_id,
            aws_region=aws_region,
            aws_role=aws_role,
            aws_sts_endpoint=aws_sts_endpoint,
            buffer_size=buffer_size,
            current_time_index=current_time_index,
            generate_id=generate_id,
            host=host,
            http_passwd=http_passwd,
            http_user=http_user,
            id_key=id_key,
            include_tag_key=include_tag_key,
            index=index,
            logstash_date_format=logstash_date_format,
            logstash_format=logstash_format,
            logstash_prefix=logstash_prefix,
            logstash_prefix_key=logstash_prefix_key,
            path=path,
            pipeline=pipeline,
            port=port,
            replace_dots=replace_dots,
            suppress_type_name=suppress_type_name,
            tag_key=tag_key,
            time_key=time_key,
            time_key_format=time_key_format,
            time_key_nanos=time_key_nanos,
            trace_error=trace_error,
            trace_output=trace_output,
            type=type,
            workers=workers,
            write_operation=write_operation,
            match=match,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> ResolvedFluentBitConfiguration:
        '''Builds a configuration for this plugin and returns the details for consumtion by a resource that is configuring logging.

        :param scope: The construct configuring logging using Fluent Bit.

        :return:

        A configuration for the plugin that con be used by the resource
        configuring logging.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FluentBitOpenSearchOutput.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(ResolvedFluentBitConfiguration, jsii.invoke(self, "bind", [scope]))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> aws_cdk.aws_opensearchservice.IDomain:
        '''The Opensearch domain to which logs should be shipped.

        :group: Inputs
        '''
        return typing.cast(aws_cdk.aws_opensearchservice.IDomain, jsii.get(self, "domain"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        '''TCP port of the target OpenSearch instance.

        :group: Inputs
        '''
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="awsAuth")
    def aws_auth(self) -> typing.Optional[builtins.bool]:
        '''Enable AWS Sigv4 Authentication for Amazon OpenSearch Service.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "awsAuth"))

    @builtins.property
    @jsii.member(jsii_name="awsExternalId")
    def aws_external_id(self) -> typing.Optional[builtins.str]:
        '''External ID for the AWS IAM Role specified with ``awsRole``.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsExternalId"))

    @builtins.property
    @jsii.member(jsii_name="awsRegion")
    def aws_region(self) -> typing.Optional[builtins.str]:
        '''Specify the AWS region for Amazon OpenSearch Service.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsRegion"))

    @builtins.property
    @jsii.member(jsii_name="awsRole")
    def aws_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''AWS IAM Role to assume to put records to your Amazon cluster.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], jsii.get(self, "awsRole"))

    @builtins.property
    @jsii.member(jsii_name="awsStsEndpoint")
    def aws_sts_endpoint(self) -> typing.Optional[builtins.str]:
        '''Specify the custom sts endpoint to be used with STS API for Amazon OpenSearch Service.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsStsEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="bufferSize")
    def buffer_size(self) -> typing.Optional[OpenSearchOutputBufferSize]:
        '''Specify the buffer size used to read the response from the OpenSearch HTTP service.

        This option is useful for debugging purposes where is
        required to read full responses, note that response size grows depending
        of the number of records inserted.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[OpenSearchOutputBufferSize], jsii.get(self, "bufferSize"))

    @builtins.property
    @jsii.member(jsii_name="currentTimeIndex")
    def current_time_index(self) -> typing.Optional[builtins.bool]:
        '''Use current time for index generation instead of message record.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "currentTimeIndex"))

    @builtins.property
    @jsii.member(jsii_name="generateId")
    def generate_id(self) -> typing.Optional[builtins.bool]:
        '''When enabled, generate ``_id`` for outgoing records.

        This prevents duplicate
        records when retrying.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "generateId"))

    @builtins.property
    @jsii.member(jsii_name="httpPasswd")
    def http_passwd(self) -> typing.Optional[builtins.str]:
        '''Password for user defined in ``httpUser``.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpPasswd"))

    @builtins.property
    @jsii.member(jsii_name="httpUser")
    def http_user(self) -> typing.Optional[builtins.str]:
        '''Optional username credential for access.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpUser"))

    @builtins.property
    @jsii.member(jsii_name="idKey")
    def id_key(self) -> typing.Optional[builtins.str]:
        '''If set, ``_id`` will be the value of the key from incoming record and ``generateId`` option is ignored.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idKey"))

    @builtins.property
    @jsii.member(jsii_name="includeTagKey")
    def include_tag_key(self) -> typing.Optional[builtins.bool]:
        '''When enabled, it append the Tag name to the record.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "includeTagKey"))

    @builtins.property
    @jsii.member(jsii_name="index")
    def index(self) -> typing.Optional[builtins.str]:
        '''Index name.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "index"))

    @builtins.property
    @jsii.member(jsii_name="logstashDateFormat")
    def logstash_date_format(self) -> typing.Optional[builtins.str]:
        '''Time format (based on strftime) to generate the second part of the Index name.

        :see: `strftime <http://man7.org/linux/man-pages/man3/strftime.3.html>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logstashDateFormat"))

    @builtins.property
    @jsii.member(jsii_name="logstashFormat")
    def logstash_format(self) -> typing.Optional[builtins.bool]:
        '''Enable Logstash format compatibility.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "logstashFormat"))

    @builtins.property
    @jsii.member(jsii_name="logstashPrefix")
    def logstash_prefix(self) -> typing.Optional[builtins.str]:
        '''When ``logstashFormat`` is enabled, the Index name is composed using a prefix and the date, e.g: If ``logstashPrefix`` is equals to 'mydata' your index will become 'mydata-YYYY.MM.DD'.

        The last string appended belongs to the date when the data is being
        generated.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logstashPrefix"))

    @builtins.property
    @jsii.member(jsii_name="logstashPrefixKey")
    def logstash_prefix_key(self) -> typing.Optional[builtins.str]:
        '''When included: the value in the record that belongs to the key will be looked up and over-write the ``logstashPrefix`` for index generation.

        If
        the key/value is not found in the record then the ``logstashPrefix`` option
        will act as a fallback.

        Nested keys are not supported (if desired, you can use the nest filter
        plugin to remove nesting).

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logstashPrefixKey"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''OpenSearch accepts new data on HTTP query path "/_bulk".

        But it is also
        possible to serve OpenSearch behind a reverse proxy on a subpath. This
        option defines such path on the fluent-bit side. It simply adds a path
        prefix in the indexing HTTP POST URI.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="pipeline")
    def pipeline(self) -> typing.Optional[builtins.str]:
        '''OpenSearch allows to setup filters called pipelines.

        This option allows
        to define which pipeline the database should use.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pipeline"))

    @builtins.property
    @jsii.member(jsii_name="replaceDots")
    def replace_dots(self) -> typing.Optional[builtins.bool]:
        '''When enabled, replace field name dots with underscore.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "replaceDots"))

    @builtins.property
    @jsii.member(jsii_name="suppressTypeName")
    def suppress_type_name(self) -> typing.Optional[builtins.bool]:
        '''When enabled, mapping types is removed and ``type`` option is ignored.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "suppressTypeName"))

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''When ``includeTagKey`` is enabled, this property defines the key name for the tag.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKey"))

    @builtins.property
    @jsii.member(jsii_name="timeKey")
    def time_key(self) -> typing.Optional[builtins.str]:
        '''When ``logstashFormat`` is enabled, each record will get a new timestamp field.

        The``timeKey`` property defines the name of that field.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeKey"))

    @builtins.property
    @jsii.member(jsii_name="timeKeyFormat")
    def time_key_format(self) -> typing.Optional[builtins.str]:
        '''When ``logstashFormat`` is enabled, this property defines the format of the timestamp.

        :see: `strftime <http://man7.org/linux/man-pages/man3/strftime.3.html>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeKeyFormat"))

    @builtins.property
    @jsii.member(jsii_name="timeKeyNanos")
    def time_key_nanos(self) -> typing.Optional[builtins.bool]:
        '''When ``logstashFormat`` is enabled, enabling this property sends nanosecond precision timestamps.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "timeKeyNanos"))

    @builtins.property
    @jsii.member(jsii_name="traceError")
    def trace_error(self) -> typing.Optional[builtins.bool]:
        '''When enabled print the OpenSearch API calls to stdout when OpenSearch returns an error (for diag only).

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "traceError"))

    @builtins.property
    @jsii.member(jsii_name="traceOutput")
    def trace_output(self) -> typing.Optional[builtins.bool]:
        '''When enabled print the OpenSearch API calls to stdout (for diag only).

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "traceOutput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        '''Type name.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="workers")
    def workers(self) -> typing.Optional[jsii.Number]:
        '''Enables dedicated thread(s) for this output.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "workers"))

    @builtins.property
    @jsii.member(jsii_name="writeOperation")
    def write_operation(self) -> typing.Optional[builtins.str]:
        '''Operation to use to write in bulk requests.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "writeOperation"))


__all__ = [
    "AdotCollector",
    "AdotCollectorProps",
    "AppendedRecord",
    "AwsSecretStore",
    "AwsSecretStoreProps",
    "AwsServiceDiscoveryRegistry",
    "Echoserver",
    "EchoserverProps",
    "ElasticsearchCompressionFormat",
    "ElasticsearchOutputBufferSize",
    "EmitterStorageType",
    "ExternalDnsLogFormat",
    "ExternalDnsLogLevel",
    "ExternalDnsRegistry",
    "ExternalDnsRegistryConfiguration",
    "ExternalDnsSyncPolicy",
    "ExternalDnsZoneTag",
    "ExternalDnsZoneType",
    "ExternalSecret",
    "ExternalSecretOptions",
    "ExternalSecretProps",
    "ExternalSecretsOperator",
    "ExternalSecretsOperatorProps",
    "FargateLogger",
    "FargateLoggerOptions",
    "FargateLoggerProps",
    "FluentBitCloudWatchLogsOutput",
    "FluentBitCloudWatchLogsOutputOptions",
    "FluentBitElasticsearchOutput",
    "FluentBitElasticsearchOutputOptions",
    "FluentBitFilter",
    "FluentBitFilterPluginBase",
    "FluentBitFilterPluginCommonOptions",
    "FluentBitGrepFilter",
    "FluentBitGrepFilterOptions",
    "FluentBitGrepRegex",
    "FluentBitJsonParser",
    "FluentBitJsonParserOptions",
    "FluentBitKinesisFirehoseOutput",
    "FluentBitKinesisFirehoseOutputOptions",
    "FluentBitKinesisOutput",
    "FluentBitKinesisOutputOptions",
    "FluentBitKubernetesFilter",
    "FluentBitKubernetesFilterOptions",
    "FluentBitLogGroupOutput",
    "FluentBitLogStreamOutput",
    "FluentBitLogfmtParser",
    "FluentBitLogfmtParserOptions",
    "FluentBitLtsvParser",
    "FluentBitLtsvParserOptions",
    "FluentBitMatch",
    "FluentBitMatchEvaluator",
    "FluentBitModifyFilter",
    "FluentBitModifyFilterOptions",
    "FluentBitNestFilter",
    "FluentBitNestFilterOptions",
    "FluentBitOpenSearchOutput",
    "FluentBitOpenSearchOutputOptions",
    "FluentBitOutput",
    "FluentBitOutputPluginBase",
    "FluentBitOutputPluginCommonOptions",
    "FluentBitParser",
    "FluentBitParserFilter",
    "FluentBitParserFilterOptions",
    "FluentBitParserPluginBase",
    "FluentBitParserPluginCommonOptions",
    "FluentBitPlugin",
    "FluentBitPluginCommonOptions",
    "FluentBitPluginType",
    "FluentBitRecordModifierFilter",
    "FluentBitRecordModifierFilterOptions",
    "FluentBitRegexParser",
    "FluentBitRegexParserOptions",
    "FluentBitRewriteTagFilter",
    "FluentBitRewriteTagFilterOptions",
    "FluentBitThrottleFilter",
    "FluentBitThrottleFilterOptions",
    "IExternalDnsRegistry",
    "IFluentBitFilterPlugin",
    "IFluentBitOutputPlugin",
    "IFluentBitParserPlugin",
    "IFluentBitPlugin",
    "INestFilterOperation",
    "ISecretReference",
    "ISecretStore",
    "KinesisFirehoseCompressionFormat",
    "LiftOptions",
    "MetadataPolicy",
    "ModifyCondition",
    "ModifyOperation",
    "NamespacedExternalSecretOptions",
    "NestFilterOperation",
    "NestFilterOperationType",
    "NestOptions",
    "NoopRegistry",
    "OpenSearchOutputBufferSize",
    "ParserPluginDataType",
    "ResolvedFluentBitConfiguration",
    "RewriteTagRule",
    "Route53Dns",
    "Route53DnsOptions",
    "Route53DnsProps",
    "SecretFieldReference",
    "SecretReferenceConfiguration",
    "SecretsManagerReference",
    "SecretsManagerReferenceOptions",
    "SecretsManagerSecretStore",
    "SecretsManagerSecretStoreProps",
    "SsmParameterReference",
    "SsmParameterReferenceOptions",
    "SsmParameterSecretStore",
    "SsmParameterSecretStoreProps",
    "TxtRegistry",
    "TxtRegistryOptions",
]

publication.publish()
